# Cost discipline and workload placement

NEW_RECURRING_CLOUD_COST = 0

| Cloud | Evidence status | Cost architecture |
|---|---|---|
| AWS | Existing lightweight Lightsail recurring host | Existing bundle, attached static IPv4 and bounded application containers; unchanged |
| Azure | REFERENCE_ONLY_NOT_DEPLOYED | Burstable VM plus separately priced disk, public IP and possible egress; no resources created |
| GCP | REFERENCE_ONLY_NOT_DEPLOYED | Shared-core VM plus disk, external IP and possible egress; no resources created |

These are architecture comparisons, not estimates of an actual bill or claims of a free tier. Pricing varies by region, currency, discounts, runtime and transfer. No exact live bill was obtained or invented. Before any future deployment, price the complete regional shape including idle IPs, disks, backups, logging and egress; agree an owner, expiration and teardown verification. Stopping a VM is not equivalent to eliminating storage/IP charges.

Design goal: low-cost always-on control/application plane + local heavy-compute plane. The small cloud host serves the public portfolio and bounded APIs/control functions; sustained ML training, computer vision, large-model inference and research remain on existing local equipment. This avoids paying for idle GPU/large-memory capacity and acknowledges that two GiB is not a production heavy-compute platform. It does not imply local compute has zero electricity or hardware cost.

No Kubernetes, managed database, load balancer, NAT gateway, Azure/GCP persistent service or new AWS host is created. Schema validation, mocked plans and public-repository GitHub-native CI are used instead of paid infrastructure demonstrations. No paid monitoring service or subscription was added. Reference size validation prevents casual upsizing but cannot enforce a billing cap; organizational budgets and deployment authorization remain separate controls.

Pricing sources checked 2026-09-23: [Lightsail](https://aws.amazon.com/lightsail/pricing/), [Azure Linux VMs](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/), [GCP Compute](https://cloud.google.com/products/compute/pricing).
