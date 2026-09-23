"""Run pinned tfsec, preserve every finding, and reject risks without current review."""
import argparse
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--cloud', choices=['aws', 'azure', 'gcp'], required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--tfsec', type=Path)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
review = json.loads((ROOT / 'terraform/security-review.json').read_text())
assert datetime.date.today() <= datetime.date.fromisoformat(review['review_by']), 'Security design review expired'
with tempfile.TemporaryDirectory(prefix='portfolio-tfsec-') as folder:
    binary = args.tfsec
    if binary is None:
        url = 'https://github.com/aquasecurity/tfsec/releases/download/v1.28.14/tfsec_1.28.14_linux_amd64.tar.gz'
        data = urllib.request.urlopen(url, timeout=60).read()
        assert hashlib.sha256(data).hexdigest() == '329ae7f67f2f1813ebe08de498719ea7003c75d3ca24bb0b038369062508008e', 'Scanner checksum mismatch'
        binary = Path(folder) / 'tfsec'
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            binary.write_bytes(archive.extractfile('tfsec').read())
        binary.chmod(0o700)
    report = args.output / f'{args.cloud}-tfsec.json'
    command = [str(binary.resolve()), str(ROOT / 'terraform/environments' / args.cloud), '--format', 'json', '--out', str(report.resolve()), '--no-module-downloads', '--no-colour']
    result = subprocess.run(command, env={**os.environ, 'GOMAXPROCS': '2'}, capture_output=True, text=True)
    assert result.returncode in (0, 1) and report.exists(), 'Scanner execution failed: ' + result.stderr
    document = json.loads(report.read_text())
    findings = document.get('results') or []
    unexpected = []
    for finding in findings:
        relative = Path(finding['location']['filename']).resolve().relative_to(ROOT).as_posix()
        finding['location']['filename'] = relative
        matches = [item for item in review['findings'] if item['cloud'] == args.cloud and item['rule'] == finding['long_id'] and item['severity'] == finding['severity'] and item['file'] == relative]
        finding['review'] = matches[0]['reason'] if len(matches) == 1 else 'UNREVIEWED'
        if len(matches) != 1:
            unexpected.append(finding['long_id'])
    report.write_text(json.dumps(document, indent=2) + '\n')
    lines = [f'### {args.cloud.upper()} IaC security', f'tfsec 1.28.14: {len(findings)} findings; {len(unexpected)} unreviewed.']
    lines += [f"- {f['severity']} `{f['long_id']}`: {f['review']}" for f in findings]
    summary = '\n'.join(lines) + '\n'
    print(summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as output:
            output.write(summary)
    assert not unexpected, 'Unreviewed security findings: ' + ', '.join(unexpected)
