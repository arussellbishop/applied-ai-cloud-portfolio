"""Read-only count inventory. No identifiers, credentials or addresses in output."""
import json
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
os.environ["AWS_MAX_ATTEMPTS"] = "1"

def call(service, operation, key, region=None, extra=()):
    cmd = ['aws', service, operation, '--output', 'json', *extra]
    if region:
        cmd += ['--region', region]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode:
        return None
    return json.loads(p.stdout).get(key, [])

regions = call('ec2', 'describe-regions', 'Regions')
if regions is None:
    print('ACCOUNT_INVENTORY=PARTIAL: enabled-region discovery denied')
    regions = [{'RegionName': 'eu-north-1'}]
checks = [
    ('lightsail', 'get-instances', 'instances'),
    ('lightsail', 'get-static-ips', 'staticIps'),
    ('lightsail', 'get-instance-snapshots', 'instanceSnapshots'),
    ('lightsail', 'get-disks', 'disks'),
    ('lightsail', 'get-disk-snapshots', 'diskSnapshots'),
    ('lightsail', 'get-load-balancers', 'loadBalancers'),
    ('lightsail', 'get-relational-databases', 'relationalDatabases'),
    ('lightsail', 'get-container-services', 'containerServices'),
    ('lightsail', 'get-buckets', 'buckets'),
    ('lightsail', 'get-distributions', 'distributions'),
    ('lambda', 'list-functions', 'Functions'),
    ('sqs', 'list-queues', 'QueueUrls'),
    ('eks', 'list-clusters', 'clusters'),
    ('rds', 'describe-db-instances', 'DBInstances'),
    ('elbv2', 'describe-load-balancers', 'LoadBalancers'),
    ('ec2', 'describe-nat-gateways', 'NatGateways'),
    ('ec2', 'describe-instances', 'Reservations'),
    ('opensearch', 'list-domain-names', 'DomainNames'),
    ('bedrock', 'list-provisioned-model-throughputs', 'provisionedModelSummaries'),
]
def inspect(region, service, operation, key):
    rows = call(service, operation, key, region)
    count = 'UNKNOWN' if rows is None else len(rows)
    if key == 'Reservations' and rows is not None:
        count = sum(len(x.get('Instances', [])) for x in rows)
    return {'region': region, 'service': service, 'kind': key, 'count': count}

results = []
with ThreadPoolExecutor(max_workers=6) as pool:
    tasks = [pool.submit(inspect, item['RegionName'], *check) for item in regions for check in checks]
    for task in as_completed(tasks):
        results.append(task.result())
for row in sorted(results, key=lambda r: (r['region'], r['service'], r['kind'])):
    if isinstance(row['count'], int) and row['count']:
        print(f"INVENTORY {row['region']} {row['service']}/{row['kind']}={row['count']}")
private = Path.home() / 'ai-capstone-bootstrap-private'
private.mkdir(exist_ok=True, mode=0o700)
(private / 'inventory-counts.json').write_text(json.dumps(results, indent=2))
print(f"INVENTORY_CHECKS={len(results)}; UNKNOWN={sum(r['count'] == 'UNKNOWN' for r in results)}")
for service, operation, key in [('s3', 'list-buckets', 'Buckets'), ('cloudfront', 'list-distributions', 'DistributionList')]:
    rows = call(service, operation, key)
    count = 'UNKNOWN' if rows is None else rows.get('Quantity', 0) if isinstance(rows, dict) else len(rows)
    print(f'INVENTORY global {service}/{key}={count}')
print('INVENTORY_SCOPE=selected services, enabled regions; counts do not establish ownership or complete billing coverage')
print('UNRELATED_RESOURCES=REVIEW_REQUIRED; do not delete from counts alone')
