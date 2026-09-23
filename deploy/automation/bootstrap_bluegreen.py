#!/usr/bin/python3 -I
"""One-time operator installation; never invoked by the deployment credential."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

if os.geteuid() != 0:
    raise SystemExit('Run as the authorized host operator')
source = Path(__file__).with_name('deploy.py')
spec = importlib.util.spec_from_file_location('receiver', source)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
if r.BG.exists():
    raise SystemExit('Blue/green state already exists; inspect it instead of reinitializing')
release = (r.BASE / 'current').resolve(strict=True)
sha = (release / '.env').read_text().strip().split('=', 1)[1]
if not r.re.fullmatch('[0-9a-f]{40}', sha):
    raise SystemExit('Active release must have an exact Git SHA')
objects = json.loads(r.run('/usr/bin/docker', 'inspect', 'applied-ai-caddy', 'applied-ai-portfolio', 'applied-ai-api'))
if any(c['State']['Health']['Status'] != 'healthy' for c in objects):
    raise SystemExit('Healthy baseline required')
caddy = objects[0]
config_volume = next(m['Source'] for m in caddy['Mounts'] if m['Destination'] == '/config')
startup_file = Path(next(m['Source'] for m in caddy['Mounts'] if m['Destination'] == '/etc/caddy/Caddyfile'))
r.BG.mkdir(mode=0o755)
(r.BG / 'releases').mkdir()
(r.BG / 'reports').mkdir()
shutil.copyfile(startup_file, r.BG / 'original-Caddyfile')
record = {'sha':sha, 'slot':'blue', 'release':str(release),
          'containers':{'portfolio':'applied-ai-portfolio','api':'applied-ai-api'},
          'images':{name:objects[index]['Config']['Image'] for name,index in [('portfolio',1),('api',2)]}}
value = {'active':'blue','previous':None,'slots':{'blue':record}}
r.atomic_json(r.BG / 'proxy.json', {'directory':str(Path(config_volume) / 'caddy'), 'startup_file':str(startup_file)})
r.atomic_json(r.BG / 'state.json', value)
proxy = Path(config_volume) / 'caddy'
(proxy / 'active.caddy').write_text(r.caddyfile('blue', record))
r.run('/usr/bin/docker','exec','applied-ai-caddy','/usr/local/bin/caddy-nocap','validate','--config','/config/caddy/active.caddy','--adapter','caddyfile')
# Keep this existing bind-mounted inode: all later startup config changes are atomic
# replacements inside the directory-mounted volume, not container recreations.
with startup_file.open('w') as file:
    file.write('import /config/caddy/active.caddy\n');file.flush();os.fsync(file.fileno())
r.reload_proxy('blue', record)
r.public_health('blue', record)
r.run('/usr/bin/docker','update','--memory','128m','--memory-swap','128m','--pids-limit','64','applied-ai-api')
r.run('/usr/bin/docker','update','--pids-limit','64','applied-ai-portfolio')
shutil.copyfile(source, '/usr/local/libexec/portfolio-deploy')
Path('/usr/local/libexec/portfolio-deploy').chmod(0o755)
print('Blue slot adopted; Caddy process retained; private reload installed; receiver ready')
