from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
text_files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
joined = '\n'.join(p.read_text(errors='ignore') for p in text_files if p.suffix.lower() in {'.md', '.html', '.yml', '.yaml', '.py', '.txt'})
patterns = {
    'private-key': r'BEGIN (?:RSA|OPENSSH|EC|PRIVATE) KEY',
    'aws-key': r'AKIA[0-9A-Z]{12,}',
    'ipv4': r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])',
    'private-mesh': r'(?i)tail' + r'scale(?:0|s+ip|s+status)',
    'secret-assignment': r'(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*[^\s<>{}]+',
}
errors = []
for name, pattern in patterns.items():
    for match in re.finditer(pattern, joined):
        value = match.group(0)
        if name == 'ipv4' and value in {'0.0.0.0', '127.0.0.1'}:
            continue
        errors.append(f'{name}: {value[:40]}')
for p in root.rglob('*'):
    if p.is_file() and p.name not in {'.gitignore'} and p.suffix in {'.env', '.key', '.pem', '.crt'}:
        errors.append(f'forbidden file: {p.relative_to(root)}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'publication scan passed ({len(text_files)} files inspected)')
