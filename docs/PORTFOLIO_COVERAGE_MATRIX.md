# Portfolio coverage matrix

Audit basis: the public repository and its committed evidence on the publication branch. `IMPLEMENTED` means working source or operated delivery is evidenced; `VALIDATED` means bounded tests or static/mocked validation; `ARCHITECTED` means a documented design or reference implementation; `DOCUMENTED` means the capability is described but not independently demonstrated; `MISSING` means evidence was not found. These labels describe evidence maturity, not seniority.

| Area | Capability | Evidence status | Evidence / boundary |
|---|---|---:|---|
| AI / ML | Python ML and evaluation | VALIDATED | Historical research and current validation scripts; no public end-to-end training service. |
| AI / ML | Time-series ML | VALIDATED | Historical weekly market-state work; source inputs were not republished. |
| AI / ML | Hidden Markov Models | VALIDATED | Interpretable HMM evidence over 857 weekly observations; no outperformance claim. |
| AI / ML | Feature engineering | VALIDATED | Train-only transforms and trend, momentum and volatility signals are documented. |
| AI / ML | Walk-forward / no-lookahead methodology | DOCUMENTED | Temporal controls are documented; a fully reproducible walk-forward replay is missing. |
| AI / ML | Model evaluation | VALIDATED | Reconciliation, rejection registers and holdout discipline; not a production model registry. |
| AI / ML | Interpretability | VALIDATED | Interpretable market-state framing and explicit research controls. |
| AI / ML | Computer vision | VALIDATED | Historical OpenCV ORB, latest-frame bus and target-loss tests. |
| AI / ML | Object tracking | VALIDATED | Historical bounded follow experiment with two recorded reacquisitions. |
| AI / ML | Edge AI / robotics | ARCHITECTED | Ubuntu/Tello perception architecture; no fresh flight or navigation-grade autonomy claim. |
| AI / ML | LLM / agentic AI | DOCUMENTED | AIVouch answer-engine visibility and governed tool-assisted workflow; no production LLM quality claim. |
| AI / ML | API-based AI systems | VALIDATED | AIVouch FastAPI prototype, private API checks and bounded runtime evidence. |
| Software | Python application engineering | IMPLEMENTED | Deployment, validation and recovery automation are public. |
| Software | FastAPI / REST APIs | VALIDATED | AIVouch case study records tests and private runtime checks. |
| Software | Testing | IMPLEMENTED | Unit, publication, link, Compose, Terraform and security checks run in CI. |
| Software | Dependency management | VALIDATED | Provider locks, pinned tool versions and dependency checks are committed. |
| Software | Git / documentation / reproducibility | IMPLEMENTED | PR history, evidence records, runbooks and exact-SHA workflows. |
| Cloud | AWS | IMPLEMENTED | Existing Lightsail platform, GitHub delivery and Phase 19 evidence. |
| Cloud | Azure | ARCHITECTED | Terraform VNet/NSG/VM reference with schema and mocked-plan validation; not deployed. |
| Cloud | GCP | ARCHITECTED | Terraform VPC/VM/firewall reference with visible design findings; not deployed. |
| Cloud | Terraform / IaC | VALIDATED | Pinned providers, modules, locks and three credential-free mocked plans. |
| Cloud | Docker / OCI workloads | IMPLEMENTED | Compose, bounded containers and private BLUE/GREEN slots. |
| Cloud | CI/CD / GitHub Actions | IMPLEMENTED | Required CI, exact-SHA gates, OIDC validation and guarded delivery. |
| Cloud | Workload identity / OIDC | IMPLEMENTED | Main-only GitHub-to-AWS federation is recorded in final Phase 19 evidence. |
| Cloud | Least privilege | VALIDATED | Scoped deployment policy, constrained trust and no static AWS deployment keys. |
| Cloud | Blue/green deployment | IMPLEMENTED | Candidate health, content and SHA checks precede atomic Caddy switching. |
| Cloud | Rollback / recovery | VALIDATED | Retained healthy slot, guarded rollback exercise and recovery runbooks. |
| Cloud | Health checks / observability | IMPLEMENTED | Container health, `/health`, public probes and GitHub summaries. |
| Cloud | Event-driven architecture | ARCHITECTED | AWS capstone policy/runbook scopes Lambda/SQS/CloudWatch concepts; no retained workload is claimed. |
| MLOps | Model/service deployment | VALIDATED | Service/container delivery is proven; model registry/training lifecycle is missing. |
| MLOps | Automated validation / CI gates | IMPLEMENTED | Publication safety, IaC, test, security and exact-SHA gates. |
| MLOps | Monitoring | VALIDATED | Bounded health and stability evidence; no enterprise alerting SLA. |
| MLOps | Governance / security | IMPLEMENTED | Evidence boundaries, secret scanning, trust restrictions and runtime controls. |
| MLOps | Artifact / evidence traceability | IMPLEMENTED | Sanitized JSON evidence, run IDs, SHA records and recovery documents. |
| MLOps | Exact-SHA deployment | IMPLEMENTED | Main SHA is checked before delivery and reported by health/deployment records. |
| Architecture | Multi-cloud design | ARCHITECTED | Shared host contract mapped to AWS/Azure/GCP with explicit limits. |
| Architecture | Workload portability | VALIDATED | Provider-specific Terraform references and portable container contract. |
| Architecture | Security architecture | VALIDATED | Private backends, pinned host identity, forced commands and container hardening. |
| Architecture | Cost architecture / FinOps | IMPLEMENTED | Existing host reused, heavy compute kept local, capstone incremental cost USD 0. |
| Architecture | Resilience | VALIDATED | Single-host BLUE/GREEN and rollback evidence; not multi-region HA. |
| Architecture | Edge/cloud split | DOCUMENTED | Local heavy compute and lightweight cloud control/application plane are explicit. |
| Architecture | Integration architecture | DOCUMENTED | CI, GitHub, host receiver, Caddy and evidence boundaries are diagrammed. |
| Architecture | Trade-off decisions | IMPLEMENTED | Cost, security, portability and evidence limits are recorded. |
| Education | MSc Artificial Intelligence and Machine Learning | MISSING | Formal award evidence was not found in this repository. Supply verified award details before publication. |
| Education | MSc dissertation | VALIDATED | Historical HMM methodology is evidenced; dissertation manuscript, supervisor and formal submission record are missing. |
| Education | MSc modules / projects | MISSING | No authoritative module list or assessed project artefacts were found. |
| Education | Virtualisation and Cloud work | MISSING | No standalone assessed module evidence was found in this repository. |
| Professional development | Awarded certifications | MISSING | No certificate evidence was found in the repository. |
| Professional development | Completed training | MISSING | No course-completion evidence was found in the repository. |
| Professional development | Current / planned training | MISSING | No authoritative current-training list was found. |

## Six core projects surfaced

1. AI Operating System: governed persistent engineering workspace.
2. AIVouch: private FastAPI and AI-visibility validation.
3. Air Marshal: computer vision and supervised drone research.
4. Quantitative Intelligence / Finance Lab: interpretable market-state research.
5. Multi-Cloud Platform: portable Terraform and delivery architecture.
6. AWS AI/Cloud Capstone: OIDC, least privilege, CI and cost-guarded validation.

The project pages preserve the difference between implemented, historical, reference-only and missing evidence.
