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
import urllib.request

BASE = Path('/opt/portfolio-deploy')
REPO = 'arussellbishop/applied-ai-cloud-portfolio'
WORKFLOWS = ('docs.yml', 'quality.yml', 'container.yml', 'security.yml')
SERVICES = ('portfolio', 'api', 'caddy')


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


def compose(release, *args):
    subprocess.run(['/usr/bin/docker', 'compose', '--project-name', 'applied-ai-private',
                    '--project-directory', str(release), '-f', str(release / 'compose.yaml'),
                    '-f', str(release / 'images.yaml'), *args], check=True, timeout=300)


def health(release):
    expected = (release / '.env').read_text().strip().split('=', 1)[1]
    wanted = (release / 'portfolio/site/index.html').read_bytes()
    for _ in range(30):
        try:
            status = json.loads(fetch('http://127.0.0.1/health'))
            page = fetch('http://127.0.0.1/')
            states = subprocess.check_output(['/usr/bin/docker', 'inspect', '--format',
                '{{.State.Health.Status}}', *['applied-ai-' + name for name in SERVICES]], timeout=10).decode().split()
            if status.get('release') == expected and status.get('status') == 'ok' and page == wanted and states == ['healthy'] * 3:
                return
        except Exception:
            pass
        time.sleep(3)
    raise RuntimeError('release health check failed')


def activate(release):
    pending = BASE / 'current.next'
    pending.unlink(missing_ok=True)
    pending.symlink_to(release)
    pending.replace(BASE / 'current')


def deploy(sha):
    verify_ci(sha)
    previous = (BASE / 'current').resolve(strict=True)
    if previous.name == sha:
        health(previous)
        print('Already healthy: ' + sha)
        return
    release = BASE / 'releases' / sha
    if release.exists():
        shutil.rmtree(release)
    shutil.copytree(BASE / 'template', release)
    extract_site(fetch(f'https://codeload.github.com/{REPO}/tar.gz/{sha}'), release / 'portfolio/site')
    (release / '.env').write_text('RELEASE_ID=' + sha + '\n')
    (release / 'images.yaml').write_text('services:\n' + ''.join(
        f'  {name}:\n    image: portfolio-release-{name}:{sha}\n' for name in SERVICES))
    compose(release, 'config', '--quiet')
    compose(release, 'build', *SERVICES)
    verify_ci(sha)  # Reject a superseded commit immediately before changing production.
    try:
        compose(release, 'up', '-d', '--no-build', '--wait', '--wait-timeout', '100', *SERVICES)
        health(release)
        activate(release)
        (BASE / 'previous').unlink(missing_ok=True)
        (BASE / 'previous').symlink_to(previous)
    except BaseException:
        compose(previous, 'up', '-d', '--no-build', '--wait', '--wait-timeout', '100', *SERVICES)
        health(previous)
        activate(previous)
        print('ROLLBACK_OK ' + previous.name, flush=True)
        raise
    print('DEPLOYED ' + sha, flush=True)


def interrupted(signum, frame):
    raise RuntimeError('deployment interrupted')


def main():
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGHUP, interrupted)
    os.umask(0o022)
    command = sys.argv[1] if len(sys.argv) == 2 else ''
    match = re.fullmatch(r'deploy ([0-9a-f]{40})', command)
    if not match:
        raise SystemExit('Only deploy followed by a full commit SHA is permitted')
    with (BASE / 'deploy.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        deploy(match.group(1))


if __name__ == '__main__':
    main()
