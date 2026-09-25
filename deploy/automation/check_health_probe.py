#!/usr/bin/env python3
"""Opt-in Docker integration checks for the actual emitted health command.

Use an existing portfolio image; the fixture has no network or published ports.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import uuid
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--sudo', action='store_true')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('receiver', Path(__file__).with_name('deploy.py'))
    receiver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(receiver)
    record = {'slot': 'test', 'sha': 'a' * 40,
              'containers': {'portfolio': 'unused-web', 'api': 'unused-api'},
              'images': {'portfolio': args.image, 'api': args.image}}
    with patch.object(receiver, 'run') as run:
        receiver.start(record)
    command = run.call_args_list[0].args
    probe = command[command.index('--health-cmd') + 1]
    fixture = r'''
import os, subprocess, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
mode = 'ok'
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass
    def do_GET(self):
        current = mode
        if current == 'stall':
            time.sleep(5)
            return
        self.send_response(503 if current == 'error' else 200)
        self.send_header('Content-Length', '2')
        self.end_headers()
        try: self.wfile.write(b'ok')
        except BrokenPipeError: pass
server = ThreadingHTTPServer(('127.0.0.1', 8080), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
for mode, success in [('ok', True), ('error', False), ('stall', False)]:
    started = time.monotonic()
    result = subprocess.run(['/bin/sh', '-c', os.environ['PROBE']], capture_output=True, timeout=8)
    elapsed = time.monotonic() - started
    assert (result.returncode == 0) == success, (mode, result.returncode)
    if mode == 'stall': assert elapsed < 6, elapsed
    print(mode, 'PASS', flush=True)
server.shutdown()
server.server_close()
result = subprocess.run(['/bin/sh', '-c', os.environ['PROBE']], capture_output=True, timeout=8)
assert result.returncode != 0
print('connection refused PASS', flush=True)
'''
    docker = (['sudo', '-n'] if args.sudo else []) + ['docker']
    name = 'health-probe-test-' + uuid.uuid4().hex[:12]
    try:
        subprocess.run(docker + ['run', '--rm', '--name', name, '--network', 'none',
                       '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                       '--user', '10001:10001', '--memory', '96m', '--memory-swap', '96m',
                       '--cpus', '0.25', '--pids-limit', '64', '--env', 'PROBE=' + probe,
                       '--entrypoint', 'python', args.image, '-c', fixture], check=True, timeout=120)
    finally:
        subprocess.run(docker + ['rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
