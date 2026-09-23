# Cloud / Multi-Cloud Platform

**Status: AWS IMPLEMENTED / PROVEN. Terraform reference models are validated; Azure and GCP are not deployed.**

## Problem and implementation

Publish inspectable engineering work on a small existing cloud host while making releases verifiable and recoverable. The implementation uses Python validation, GitHub Actions, a restricted deployment credential, AWS Lightsail, Docker and Caddy. The host remains 2 vCPU / 2 GiB; no load balancer or orchestration cluster was added.

GitHub → exact-SHA CI gate → host-key-pinned SSH → root-owned forced-command receiver → inactive BLUE/GREEN Docker slot → internal health/SHA/content checks → atomic Caddy switch → external HTTP validation. The previous healthy slot stays running for rollback. GitHub secrets hold deployment material; it is not stored in source or Terraform. The deployment account accepts fixed commands, not an interactive shell. Workflow concurrency and host locking prevent overlapping deployments. Only Caddy publishes HTTP; Docker API and backend ports are not public.

## Strongest evidence

- [Successful switch run 35918554872](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/35918554872): 30 external paired landing/health samples, zero failed samples, both slot identities observed. **0 seconds observed during the measured validation**, with approximately 0.2-second sampling; not an unconditional availability guarantee.
- [Unhealthy candidate run 35918711359](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/35918711359): failed before traffic switch; 44 external samples observed only the healthy active slot. The workflow correctly failed.
- Immediate blue/green rollback drill: retained healthy slot restored in 0.579 seconds, then original routing restored; no sampled HTTP failures. The measured dual-slot host-used peak was 755.7 MiB; highest reading across operations was 760.3 MiB and minimum available RAM 1145.7 MiB. These historical sampled values are not capacity guarantees.
- [Automatic rollback run 35911003436](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/35911003436): the earlier replacement-based pipeline detected a bad page marker and automatically restored the exact previous SHA. That exercise had about 102 seconds aggregate sampled interruption across candidate/rollback/recovery replacements. It motivated blue/green; its interruption must not be hidden or conflated with the later zero-observed-interruption measurement.
- Current blue/green post-switch rollback has targeted unit coverage and a live immediate rollback drill. An external network outage was **not** injected into the current blue/green path. This is a narrower claim than a full live fault matrix.

[Sanitized switch/rollback records](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/evidence/final/cloud-validation.json) · [Deployment implementation](https://github.com/arussellbishop/applied-ai-cloud-portfolio/tree/main/deploy/automation) · [Architecture diagrams](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/architecture/diagrams/README.md)

## Trade-offs and limitations

A single host is still a single failure domain. HTTP serves public portfolio content only; no AIVouch authentication is exposed. Native GitHub summaries and health/resource checks provide lightweight observability, not a separately verified alert-delivery service. The Docker bridge permits egress; unpublished backends do not imply an egress-isolated network. Runtime non-root, NNP, read-only, capabilities and resource controls reduce risk but do not constitute a comprehensive security certification.

## Portability and cost

[Multi-cloud Terraform case study](multi-cloud-platform-engineering.md): AWS is implemented, Azure/GCP are validated references. Exact provider locks, credential-free CI, mocked plans, network/IAM differences and three visible GCP findings are documented. Heavy ML/research workloads stay local. The existing Lightsail recurring host is unchanged; no new recurring cloud resources were added.

Next improvements would require separate authorization: HTTPS/production readiness, independent failure-domain recovery, tested alert delivery and workload-specific capacity assessment.

[All projects](https://github.com/arussellbishop/applied-ai-cloud-portfolio#flagship-projects) · [Role evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_ROLE_EVIDENCE_MATRIX.md)
