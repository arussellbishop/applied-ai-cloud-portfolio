"""Check local Markdown/HTML, public-main source links, anchors and mirror consistency."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/arussellbishop/applied-ai-cloud-portfolio'
SKIP = {'.git', '.terraform', 'node_modules'}
errors = []
count = 0

def headings(path):
    identifiers = set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', path.read_text(), re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        identifiers.add(slug)
    return identifiers

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
    def handle_starttag(self, tag, attrs):
        self.targets.extend(value for key, value in attrs if key in {'href', 'src'} and value)

for path in ROOT.rglob('*'):
    if not path.is_file() or SKIP.intersection(path.parts) or path.suffix not in {'.md', '.html'}:
        continue
    text = path.read_text()
    if path.suffix == '.md':
        targets = re.findall(r'\]\(([^)]+)\)', text)
    else:
        parser = Links(); parser.feed(text); targets = parser.targets
    for raw in targets:
        target = raw.strip().strip('<>')
        parsed = urlsplit(target)
        destination = None
        if parsed.scheme in {'http', 'https'}:
            if parsed.netloc == 'github.com' and parsed.path.startswith(PREFIX):
                tail = parsed.path[len(PREFIX):]
                if tail in {'', '/'}: destination = ROOT / 'README.md'
                elif tail.startswith(('/blob/main/', '/tree/main/')):
                    destination = ROOT / unquote(tail.split('/', 3)[3])
            # Remote endpoint existence is checked separately after publication.
        elif not parsed.scheme and not parsed.netloc:
            if parsed.path == '/health': continue
            destination = (ROOT / 'site' / unquote(parsed.path.lstrip('/'))) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
            if not parsed.path: destination = path
        if destination is None: continue
        count += 1
        if not destination.exists(): errors.append(f'missing target: {path.relative_to(ROOT)} -> {target}')
        elif parsed.fragment and destination.suffix == '.md' and unquote(parsed.fragment) not in headings(destination):
            errors.append(f'missing anchor: {path.relative_to(ROOT)} -> {target}')
for folder in ['case-studies', 'recruiter']:
    for path in (ROOT / folder).glob('*.md'):
        mirror = ROOT / 'site' / folder / path.name
        if not mirror.exists() or mirror.read_bytes() != path.read_bytes(): errors.append(f'site mirror mismatch: {path}')
if errors: raise SystemExit('\n'.join(errors))
print(f'Links PASS: {count} local/public-main targets and anchors; site document mirrors match.')
