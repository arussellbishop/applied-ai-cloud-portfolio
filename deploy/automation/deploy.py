#!/usr/bin/python3 -I
"""Root-owned forced-command receiver. Install separately; never execute repo code."""
import fcntl
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import time
import threading
import urllib.request

BASE = Path('/opt/portfolio-deploy')
REPO = 'arussellbishop/applied-ai-cloud-portfolio'
WORKFLOWS = ('docs.yml', 'quality.yml', 'container.yml', 'security.yml')
BG = BASE / 'bluegreen'
MIN_AVAILABLE_MIB = 384
SERVICES = ('portfolio', 'api')


def fetch(url, limit=8_000_000):
    request = urllib.request.Request(url, headers={'User-Agent': 'portfolio-deploy'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('response exceeds size limit')
    return data


def api(path):
    return json.loads(fetch('https://api.github.com/repos/' + REPO + '/' + path))


def verify_ci(sha):
    if api('git/ref/heads/main')['object']['sha'] != sha:
        raise ValueError('only the current main commit is deployable')
    for workflow in WORKFLOWS:
        runs = api(f'actions/workflows/{workflow}/runs?branch=main&event=push&head_sha={sha}&per_page=10')['workflow_runs']
        if not runs or runs[0]['head_sha'] != sha or runs[0]['conclusion'] != 'success':
            raise ValueError('CI gate failed: ' + workflow)


def extract_site(data, destination):
    count = total = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if len(path.parts) < 3 or path.parts[1] != 'site':
                continue
            relative = PurePosixPath(*path.parts[2:])
            if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk():
                raise ValueError('unsafe archive path')
            if member.isdir():
                continue
            if not member.isfile() or relative.suffix.lower() not in {'.html', '.md', '.css', '.js', '.svg', '.png', '.jpg', '.ico', '.txt'}:
                raise ValueError('unsupported site entry')
            count += 1
            total += member.size
            if count > 500 or total > 8_000_000:
                raise ValueError('site exceeds size limit')
            target = destination / str(relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
            target.chmod(0o644)
    if not (destination / 'index.html').is_file():
        raise ValueError('missing index.html')


class Resources:
    def __init__(self):
        self.stop = threading.Event()
        self.unsafe = False
        self.minimum = 1_000_000
        self.peak_used = 0
        self.thread = threading.Thread(target=self.watch, daemon=True)

    def sample(self):
        values = {line.split(':')[0]: int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()}
        available = values['MemAvailable'] / 1024
        self.minimum = min(self.minimum, available)
        self.peak_used = max(self.peak_used, (values['MemTotal'] - values['MemAvailable']) / 1024)
        self.unsafe |= available < MIN_AVAILABLE_MIB

    def watch(self):
        while not self.stop.wait(0.25):
            self.sample()

    def check(self):
        self.sample()
        if self.unsafe:
            raise RuntimeError(f'Unsafe memory pressure: minimum available {self.minimum:.1f} MiB')


RESOURCES = None


def run(*args, input=None, safety=True, timeout=180):
    if safety and RESOURCES:
        RESOURCES.check()
    process = subprocess.Popen(args, stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    started = time.monotonic()
    try:
        payload = input
        while True:
            try:
                output, _ = process.communicate(payload, timeout=0.5)
                break
            except subprocess.TimeoutExpired:
                payload = None
                if safety and RESOURCES:
                    RESOURCES.check()
                if time.monotonic() - started > timeout:
                    raise TimeoutError('command timed out: ' + args[0])
        if process.returncode:
            raise RuntimeError(output.decode(errors='replace')[-4000:])
        return output
    except BaseException:
        process.kill()
        process.communicate()
        raise


def atomic_json(path, value):
    temporary = path.with_suffix('.next')
    with temporary.open('w') as file:
        json.dump(value, file, indent=2)
        file.flush()
        os.fsync(file.fileno())
    temporary.replace(path)


def state():
    return json.loads((BG / 'state.json').read_text())


def save(value):
    atomic_json(BG / 'state.json', value)
    current = BASE / 'current.next'
    current.unlink(missing_ok=True)
    current.symlink_to(value['slots'][value['active']]['release'])
    current.replace(BASE / 'current')


def caddyfile(slot, record):
    return f'''{{
    admin localhost:2019
    auto_https off
}}
:8080 {{
    header X-Portfolio-Slot {slot}
    header X-Portfolio-Release {record['sha']}
    handle /health {{
        reverse_proxy {record['containers']['api']}:8000
    }}
    handle_path /api/* {{
        reverse_proxy {record['containers']['api']}:8000
    }}
    handle {{
        reverse_proxy {record['containers']['portfolio']}:8080
    }}
}}
'''


def reload_proxy(slot, record):
    """One Caddy /load transaction; never restart the public listener."""
    proxy = Path(json.loads((BG / 'proxy.json').read_text())['directory'])
    staged = proxy / 'candidate.caddy'
    staged.write_text(caddyfile(slot, record))
    run('/usr/bin/docker', 'exec', 'applied-ai-caddy', '/usr/local/bin/caddy-nocap',
        'validate', '--config', '/config/caddy/candidate.caddy', '--adapter', 'caddyfile', safety=False)
    run('/usr/bin/docker', 'exec', 'applied-ai-caddy', '/usr/local/bin/caddy-nocap',
        'reload', '--config', '/config/caddy/candidate.caddy', '--adapter', 'caddyfile', safety=False)
    staged.replace(proxy / 'active.caddy')


def internal_health(record, attempts=30, safety=True):
    """Read exact runtime SHA and content through private container addresses."""
    wanted = (Path(record['release']) / 'portfolio/site/index.html').read_bytes()
    for _ in range(attempts):
        try:
            objects = json.loads(run('/usr/bin/docker', 'inspect', *record['containers'].values(), safety=False))
            if not all(c['State']['Health']['Status'] == 'healthy' and not c['State']['OOMKilled'] for c in objects):
                raise RuntimeError('container not healthy')
            ips = {c['Name'].lstrip('/'): c['NetworkSettings']['Networks']['applied-ai-private']['IPAddress'] for c in objects}
            health = json.loads(fetch('http://' + ips[record['containers']['api']] + ':8000/health'))
            page = fetch('http://' + ips[record['containers']['portfolio']] + ':8080/')
            if health.get('release') != record['sha'] or health.get('status') != 'ok':
                raise RuntimeError('candidate SHA mismatch')
            if page != wanted or b'Applied AI Systems' not in page:
                raise RuntimeError('candidate content invalid')
            return
        except Exception:
            if RESOURCES and safety:
                RESOURCES.check()
            time.sleep(1)
    raise RuntimeError('candidate health/SHA/content validation failed')


def public_health(slot, record):
    with urllib.request.urlopen('http://127.0.0.1/health', timeout=5) as response:
        value = json.load(response)
        if response.headers.get('X-Portfolio-Slot') != slot:
            raise RuntimeError('proxy slot mismatch')
    if value.get('release') != record['sha'] or value.get('status') != 'ok':
        raise RuntimeError('public release mismatch')
    if fetch('http://127.0.0.1/') != (Path(record['release']) / 'portfolio/site/index.html').read_bytes():
        raise RuntimeError('public content mismatch')


class TrafficSwitchError(RuntimeError):
    pass


def switch(value, target, safety=True):
    record = value['slots'][target]
    internal_health(record, safety=safety)
    original = json.loads(json.dumps(value))
    atomic_json(BG / 'transaction.json', original)
    try:
        reload_proxy(target, record)
        public_health(target, record)
        value['previous'] = original['active']
        value['active'] = target
        save(value)
        (BG / 'transaction.json').unlink()
    except BaseException as error:
        old = original['active']
        reload_proxy(old, original['slots'][old])
        public_health(old, original['slots'][old])
        save(original)
        (BG / 'transaction.json').unlink(missing_ok=True)
        raise TrafficSwitchError('traffic switch failed; previous slot restored') from error


def recover_transaction():
    journal = BG / 'transaction.json'
    if journal.exists():
        original = json.loads(journal.read_text())
        old = original['active']
        internal_health(original['slots'][old], safety=False)
        reload_proxy(old, original['slots'][old])
        public_health(old, original['slots'][old])
        save(original)
        journal.unlink()


def remove(record):
    if not record:
        return
    for name in record['containers'].values():
        # Names originate exclusively in root-owned slot state, never input strings.
        exists = subprocess.run(['/usr/bin/docker', 'inspect', name], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL).returncode == 0
        if exists:
            run('/usr/bin/docker', 'rm', '-f', name, safety=False)


def start(record, unhealthy=False, safety=True):
    for service in SERVICES:
        port = '8080' if service == 'portfolio' else '8000'
        path = '/' if service == 'portfolio' else '/health'
        health = f'python -c "import urllib.request; urllib.request.urlopen(\'http://127.0.0.1:{port}{path}\',timeout=2)"'
        if unhealthy and service == 'portfolio':
            health = 'python -c "raise SystemExit(1)"'
        command = ['/usr/bin/docker', 'run', '-d', '--name', record['containers'][service],
                   '--network', 'applied-ai-private', '--restart', 'unless-stopped',
                   '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                   '--user', '10001:10001', '--memory', '96m' if service == 'portfolio' else '128m',
                   '--memory-swap', '96m' if service == 'portfolio' else '128m',
                   '--cpus', '0.25' if service == 'portfolio' else '0.50', '--pids-limit', '64',
                   '--tmpfs', '/tmp:size=16m,noexec,nosuid,nodev',
                   '--label', 'portfolio.slot=' + record['slot'], '--label', 'portfolio.sha=' + record['sha'],
                   '--health-cmd', health, '--health-interval', '2s', '--health-timeout', '3s',
                   '--health-retries', '3', '--health-start-period', '2s']
        if service == 'api':
            command += ['--env', 'RELEASE_ID=' + record['sha']]
        command += [record['images'][service]]
        run(*command, safety=safety)


def prepare(sha, slot, unhealthy):
    identity = sha + '-' + str(time.time_ns())
    release = BG / 'releases' / identity
    shutil.copytree(BASE / 'template', release)
    extract_site(fetch(f'https://codeload.github.com/{REPO}/tar.gz/{sha}'), release / 'portfolio/site')
    (release / '.env').write_text('RELEASE_ID=' + sha + '\n')
    record = {'sha': sha, 'slot': slot, 'release': str(release),
              'containers': {service: 'portfolio-' + slot + '-' + service for service in SERVICES},
              'images': {service: 'portfolio-bg-' + service + ':' + sha for service in SERVICES}}
    for service in SERVICES:
        run('/usr/bin/docker', 'build', '--tag', record['images'][service], str(release / service), timeout=240)
    atomic_json(release / 'candidate.json', {**record, 'injected_health_failure': unhealthy})
    return record


def report(sha, **updates):
    path = BG / 'reports' / (sha + '.json')
    value = json.loads(path.read_text()) if path.exists() and updates.get('final_status') != 'RUNNING' else {'candidate_sha': sha}
    value.update(updates)
    current = state()
    value['active_slot'] = current['active']
    value['active_sha'] = current['slots'][current['active']]['sha']
    if RESOURCES:
        value['minimum_available_mib'] = round(min(value.get('minimum_available_mib', RESOURCES.minimum), RESOURCES.minimum), 1)
        value['peak_host_used_mib'] = round(max(value.get('peak_host_used_mib', 0), RESOURCES.peak_used), 1)
    atomic_json(path, value)
    print('REPORT ' + json.dumps(value), flush=True)
    return value


def deploy(sha, unhealthy=False):
    verify_ci(sha)
    value = state()
    active = value['active']
    target = 'green' if active == 'blue' else 'blue'
    old = value['slots'].get(target)
    if unhealthy and (value['slots'][active]['sha'] != sha or old is None):
        raise ValueError('health exercise requires current main active and a retained previous slot')
    internal_health(value['slots'][active])
    report(sha, candidate_slot=target, candidate_health='PENDING', traffic_switch='NOT_SWITCHED',
           external_validation='NOT_RUN', rollback='NOT_REQUIRED', final_status='RUNNING')
    candidate = None
    removed = False
    try:
        candidate = prepare(sha, target, unhealthy)
        # Gate again before replacing only the inactive slot.
        verify_ci(sha)
        if RESOURCES:
            RESOURCES.check()
        removed = True
        remove(old)
        start(candidate, unhealthy=unhealthy)
        internal_health(candidate, attempts=12 if unhealthy else 30)
        if RESOURCES:
            RESOURCES.check()
        report(sha, candidate_health='PASS')
        verify_ci(sha)
        value['slots'][target] = candidate
        switch(value, target)
        report(sha, traffic_switch='PASS', external_validation='PENDING', final_status='AWAITING_EXTERNAL')
    except BaseException as error:
        live = state()
        switched = live['active'] == target
        if switched:
            switch(live, active, safety=False)
        if removed:
            if candidate:
                remove(candidate)
            if old:
                start(old, safety=False)
                internal_health(old, safety=False)
        restored = state()
        if old:
            restored['slots'][target] = old
        else:
            restored['slots'].pop(target, None)
        save(restored)
        current_report = json.loads((BG / 'reports' / (sha + '.json')).read_text())
        rolled_back = switched or isinstance(error, TrafficSwitchError)
        report(sha, candidate_health='FAIL' if current_report['candidate_health'] != 'PASS' else 'PASS',
               traffic_switch='ROLLED_BACK' if rolled_back else 'NOT_SWITCHED',
               rollback='PASS' if rolled_back else 'NOT_REQUIRED', final_status='FAILED')
        public_health(active, restored['slots'][active])
        raise


def rollback(sha):
    value = state()
    if value['slots'][value['active']]['sha'] != sha:
        raise ValueError('rollback rejected: stale SHA')
    previous = value.get('previous')
    if not previous or previous == value['active']:
        raise ValueError('no previous slot')
    switch(value, previous, safety=False)
    report(sha, external_validation='FAIL', rollback='PASS', final_status='FAILED')


def confirm(sha):
    value = state()
    if value['slots'][value['active']]['sha'] != sha:
        raise ValueError('confirmation rejected: stale SHA')
    public_health(value['active'], value['slots'][value['active']])
    report(sha, external_validation='PASS', final_status='SUCCESS')


def interrupted(signum, frame):
    raise RuntimeError('deployment interrupted')


def main():
    global RESOURCES
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGHUP, interrupted)
    os.umask(0o022)
    match = re.fullmatch(r'(deploy|rollback|confirm|status|probe) ([0-9a-f]{40})', sys.argv[1] if len(sys.argv) == 2 else '')
    if not match:
        raise SystemExit('Only restricted release commands with a full SHA are permitted')
    with (BASE / 'deploy.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        recover_transaction()
        command, sha = match.groups()
        RESOURCES = Resources()
        RESOURCES.sample()
        RESOURCES.thread.start()
        try:
            if command == 'deploy': deploy(sha)
            elif command == 'probe': deploy(sha, unhealthy=True)
            elif command == 'rollback': rollback(sha)
            elif command == 'confirm': confirm(sha)
            else:
                value = json.loads((BG / 'reports' / (sha + '.json')).read_text())
                print('REPORT ' + json.dumps(value), flush=True)
        finally:
            RESOURCES.stop.set()
            if command in ('deploy', 'probe', 'rollback', 'confirm'):
                path = BG / 'reports' / (sha + '.json')
                if path.exists():
                    shutil.copyfile(path, BG / 'reports' / f'{sha}-{command}-{time.time_ns()}.json')


if __name__ == '__main__':
    main()
