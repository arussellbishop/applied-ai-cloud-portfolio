# Applied AI & Cloud Engineering Portfolio

Hands-on application validation, cloud delivery and research work, with measured evidence and explicit limits. The strongest current implementation is the AWS delivery platform and private AIVouch validation; robotics and quantitative work are presented as bounded historical research evidence.

[![CI](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/workflows/quality.yml/badge.svg)](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/workflows/quality.yml)

## What this portfolio demonstrates

- Python/FastAPI application validation and Docker/Linux runtime security.
- GitHub Actions CI/CD, restricted deployment credentials, blue/green switching and tested recovery.
- Terraform modules and cloud architecture: **AWS implemented; Azure/GCP validated references, not deployed**.
- Agent-assisted operations, computer vision/autonomous-systems prototypes and quantitative ML research, with evidence maturity stated separately.
- Cost-aware placement: a small cloud application/control plane and local heavy compute.

## Flagship Projects

| Project / problem | Implementation and architecture | Strongest evidence | Status / limits |
|---|---|---|---|
| [AI Operating System](case-studies/ai-operating-system.md): persistent, governed engineering work | Android/Termux, private access, SSH/tmux, Linux, Codex/Git; historical local scheduling | Working remote operating model; dated local dashboard/timer records | Proven access model; orchestration/retries only partially evidenced |
| [AIVouch](case-studies/aivouch.md): inspect AI answer-engine visibility | FastAPI/mobile/web; private Docker + SQLite demo validation | 36 tests and 18 API checks; AWS runtime controls; 88 MiB idle | Private cloud validation proven; public production disabled |
| [Air Marshal](case-studies/air-marshal.md): perception and target-loss handling | Tello/Ubuntu, OpenCV ORB, latest-frame bus, supervised policy | Historical 13-test review and bounded live-follow report | Prototype evidence; no navigation-grade SLAM or new flight validation |
| [Quantitative Intelligence](case-studies/quantitative-intelligence.md): defensible regime research | HMM, temporal controls, evaluation/rejection registries | Historical train-only/prefix-inference records and negative results | No returns claim; incomplete source-only reproduction |
| [Cloud / Multi-Cloud Platform](case-studies/aws-cloud-architecture.md): verifiable, recoverable releases | Lightsail, Docker, Caddy, GitHub CI and Terraform references | Measured zero observed interruption; isolated unhealthy candidate; rollback evidence | Single host; HTTP only; Azure/GCP undeployed |

## Inspect the evidence

[Claim audit](recruiter/FINAL_PORTFOLIO_AUDIT.md) · [Role → evidence matrix](recruiter/FINAL_ROLE_EVIDENCE_MATRIX.md) · [Recruiter summary](recruiter/FINAL_RECRUITER_SUMMARY.md) · [CV bullets](recruiter/FINAL_CV_BULLETS.md) · [Interview pack](recruiter/FINAL_INTERVIEW_PACK.md) · [Handover](recruiter/FINAL_HANDOVER.md)

[Seven architecture diagrams](architecture/diagrams/README.md) · [Terraform source](terraform/README.md) · [Sanitized validation records](evidence/final/README.md) · [Multi-cloud distinctions](case-studies/multi-cloud-platform-engineering.md)

## Validation and boundaries

Required CI covers public-safety, links, deployment unit tests, Compose, all three Terraform environments, mocked plans and Mermaid parsing. Terraform CI never applies resources and uses no cloud credentials. The [deployment workflow](deploy/automation/README.md) waits for exact-main-SHA CI and uses pinned host identity and a restricted command boundary. A zero-observed-interruption measurement is not a universal zero-downtime SLA.

This portfolio does not assert enterprise-scale operation, team leadership, sole unaided authorship, years of experience or a senior title. Tool-assisted implementation was reviewed through tests, explicit control boundaries and recorded decisions. Public summaries do not release private application source or proprietary research data.
