# Final portfolio handover

## Architecture and public state

Public repository: [https://github.com/arussellbishop/applied-ai-cloud-portfolio](https://github.com/arussellbishop/applied-ai-cloud-portfolio). The public portfolio serves HTTP through its existing static IPv4; the address is intentionally omitted. Caddy is the only published application listener. Private Docker BLUE/GREEN slots each hold the static site and health API. GitHub CI, restricted SSH commands, host identity pinning and versioned release records control publication. This is a single-host platform, not multi-region high availability. [Diagrams](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/architecture/diagrams/README.md)

## Project statuses

- Cloud platform: implemented on existing AWS Lightsail, with scoped deployment/recovery evidence.
- AIVouch: AIVOUCH_AWS_VALIDATION_PROVEN in private SQLite/demo mode; public production disabled and disposable runtime removed.
- AI OS: proven remote workspace; historical local orchestration only partially evidenced.
- Air Marshal: historical perception/following prototype and offline/live records; not navigation-grade SLAM or complete autonomy.
- Quantitative Intelligence: historical methods/negative results; no returns claim and incomplete source-only reproducibility.
- Azure/GCP: validated Terraform reference architectures, not deployed. AWS Terraform is also a reference and does not own the live host.

## Deployment and rollback model

The workflow deploys only current main after all exact-SHA CI workflows pass. Candidate health, release SHA and content are checked before an atomic Caddy reload. The previous healthy slot is retained. Pre-switch failure leaves active traffic untouched; post-switch validation failure invokes recovery and the run stays failed. Concurrency and host locks serialize operations.

Historical evidence separately proves automatic rollback in the older replacement pipeline and current blue/green isolation/manual immediate rollback. Do not assume every external failure mode was live-tested. Retain reports and known-good releases; never globally prune Docker during recovery.

## How to update the portfolio

1. Branch from clean main; edit only reviewed public-safe source. Case studies and recruiter documents have repository and site copies; keep each pair identical.
2. Run public-safety and link validation, Mermaid parsing and relevant checks. Terraform changes require format, backend-disabled init, validate, mocked plans and static security. Never run Terraform apply/import against production.
3. Open a PR. Required quality depends explicitly on all IaC jobs and cannot silently skip a failed dependency. Keep all protection rules unchanged; obtain independent review or a specifically authorized one-time administrator merge.
4. After merge, observe all main CI and `deploy-aws`. Confirm the public landing page, changed routes and `/health` report the intended main SHA. A merge alone is not evidence of a healthy deployment.
5. Preserve public evidence summaries and private operational records without leaking endpoints or credentials. Root-owned receiver/bootstrap changes require a separate operator review/install; ordinary content releases do not install privileged repository code.

## How to recover a failed deployment

1. Inspect the GitHub deployment summary: candidate/active SHA, slots, candidate health, traffic switch, external validation, rollback and final status. Check active public health before any manual action.
2. If failure occurred before switching, active traffic should remain on the previous release. Fix the candidate through a reviewed PR; do not bypass CI or force failed traffic live.
3. If automatic recovery has restored the previous release, verify its exact SHA and page/health responses. A recovered service does not turn the failed workflow into success.
4. If authorized manual recovery is needed, use the existing restricted receiver's rollback action with the **currently active full SHA** and a verified retained healthy slot. Stale SHAs are rejected. Preserve host-key pinning and the credential boundary; do not replace them with an interactive deployment shell. Obtain current private connection details through the established operator channel, not this document.
5. Recheck page/health, active SHA and container health. Preserve evidence; repair source through a normal PR and clean CI-gated deployment. If no healthy target or management access exists, stop automatic attempts and use the operator recovery procedure; do not improvise destructive cleanup.

## CI and maintenance

Required workflows cover documentation links, publication safety, Compose, deployment unit tests and security. The quality workflow additionally gates Terraform AWS/Azure/GCP validation and mocked plans plus Mermaid parsing/tool audits. Terraform is pinned to 1.14.7 with exact provider constraints/checksums. These tests do not deploy cloud resources or require provider credentials.

Check GitHub summaries, Docker health, public `/health`, disk, available memory and service state. No paid monitoring or guaranteed notification delivery is claimed. Review dependencies and pinned actions deliberately; regenerate locks and validate through PRs. The dated GCP security review expires on **2026-12-23** and CI will require a fresh review; do not simply suppress findings. Keep the HIGH public-IP and LOW logging/encryption trade-offs visible. Base-image/OS vulnerability review remains a separate maintenance need.

The deployed HTML retains the validated “Applied AI Systems” marker used by release checks. Coordinate any intentional marker change with the receiver's reviewed validation contract. Content-only editing must not accidentally break deployment health assertions.

## Cost and security boundaries

Existing lightweight Lightsail recurring host only; no new cloud resources or recurring cost in the final packaging phase. Heavy compute remains local. Actual bills, taxes/egress and local equipment costs are not inferred. No Terraform state ownership of production, Azure/GCP deployment, public AIVouch authentication, new firewall port, domain or HTTPS work is included.

Credentials remain outside source; Terraform sensitive outputs do not encrypt state. No private repository URLs, proprietary research datasets, personal/customer records or private addresses belong in this handover. The Docker bridge is unpublished for backends but permits egress. Current targeted security checks are not certification or a complete penetration test.

## Deliberately unfinished and future options

AIVouch production secrets/integrations/database, AI-quality evaluation, HTTPS and product/privacy review remain unfinished. Azure/GCP runtime/IAM/region testing remains unperformed. AI OS retry/recovery reliability, Air Marshal navigation/safety capability and quantitative point-in-time/source-only reproduction are not implied complete. Independent failure-domain recovery, alert delivery and capacity testing are potential future enhancements only if separately justified and authorized. Programme completion does not mean every research project became a production product.

## Final records

The [claim audit](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_PORTFOLIO_AUDIT.md), [role matrix](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_ROLE_EVIDENCE_MATRIX.md), [CV bullets](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_CV_BULLETS.md) and [interview pack](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_INTERVIEW_PACK.md) provide recruiter material. GitHub main/deployment history identifies the final public commit. The operator's programme status/validation records hold final acceptance results without credentials. No further development phase is started by this handover.
