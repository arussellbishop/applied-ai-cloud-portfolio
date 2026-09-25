from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
text_files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '.terraform' not in p.parts and 'node_modules' not in p.parts]
patterns = {
    'private-key': r'BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY',
    'aws-key': r'(?:AKIA|ASIA)[0-9A-Z]{16}',
    'ipv4': r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])',
    'private-mesh': r'(?i)tail' + r'scale(?:0|s+ip|s+status)',
    # GitHub's required OIDC permission is not a credential assignment.
    'secret-assignment': r'(?i)(?<!id-)(password|secret|token|api[_-]?key)\s*[:=]\s*(?!\s|\$\{\{)[^\s<>{}]+',
}
# Additional final-audit categories. Report only locations, never matched values.
patterns.update({
    'provider-token': r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_' + r'pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9]{24,})',
    'aws-account-arn': r'arn:aws[^:]*:[^:]*:[^:]*:[0-9]{12}:',
    'private-home-path': r'(?:/ho' + r'me/|/Us' + r'ers/|[A-Z]:\\Users\\)[A-Za-z0-9_.-]+',
    'aws-account-id': r'(?i)aws[ _-]*account(?:[ _-]*id)?[\s:=\"]+[0-9]{12}',
    'jwt': r'eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{16,}',
    'mesh-ipv6': r'fd7a:' + r'115c:[0-9a-fA-F:]+',
})
errors = []
extensions = {'.md', '.html', '.yml', '.yaml', '.py', '.txt', '.tf', '.hcl', '.json', '.mmd', '.mjs', '.js', '.cjs', '.sh'}
# Only the explicitly chosen fictional CIDRs are allowed, and only in IaC files.
synthetic_cidrs = {'10.' + '42.0.0/16', '10.' + '42.1.0/24', '10.' + '43.1.0/24', '10.' + '42.0.10/32'}
for path in text_files:
    if path.suffix.lower() not in extensions:
        continue
    text = path.read_text(errors='ignore')
    relative = path.relative_to(root)
    for name, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            value = match.group(0)
            if name == 'ipv4' and value in {'0.0.0.0', '127.0.0.1'}:
                continue
            if name == 'ipv4' and relative.parts[0] == 'terraform' and path.suffix in {'.tf', '.hcl'}:
                suffix = re.match(r'/[0-9]{1,2}(?![0-9])', text[match.end():])
                if suffix and value + suffix.group(0) in synthetic_cidrs:
                    continue
            # Report locations/categories, not possible secret values.
            line = text.count('\n', 0, match.start()) + 1
            errors.append(f'{name}: {relative}:{line}')

# Public repository URLs under this owner's account must be approved public sources.
from urllib.parse import urlsplit
for path in text_files:
    if path.suffix.lower() not in extensions:
        continue
    for url in re.findall(r'https://github[.]com/[^\s)<>\[\]`"\']+', path.read_text(errors='ignore')):
        parts = urlsplit(url).path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'arussellbishop' and parts[1] not in {'applied-ai-cloud-portfolio', 'ai-ml-aws-portfolio'}:
            errors.append(f'unapproved-owner-repository-link: {path.relative_to(root)}')
for p in root.rglob('*'):
    if 'node_modules' not in p.parts and '.terraform' not in p.parts and '.git' not in p.parts and p.is_file() and p.name not in {'.gitignore'} and (p.suffix in {'.env', '.key', '.pem', '.crt'} or p.name == '.env' or p.name.startswith('.env.')):
        errors.append(f'forbidden file: {p.relative_to(root)}')
    if 'node_modules' not in p.parts and '.terraform' not in p.parts and '.git' not in p.parts and p.is_file() and ('.tfstate' in p.name or p.name.endswith(('.tfvars', '.tfvars.json', '.tfplan'))):
        errors.append(f'forbidden Terraform artifact: {p.relative_to(root)}')
    if not {'.git', '.terraform', 'node_modules'}.intersection(p.parts) and p.is_file():
        if p.suffix.lower() in {'.csv', '.parquet', '.sqlite', '.db', '.zip', '.tar', '.gz', '.log', '.bak'}:
            errors.append(f'unreviewed-data-or-debug-artifact: {p.relative_to(root)}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'publication scan passed ({len(text_files)} files inspected)')
