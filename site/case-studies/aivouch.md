# AIVouch — private AWS application validation

**AIVOUCH_AWS_VALIDATION_PROVEN. Private development/demo validation; not a public production launch.**

## Problem, implementation and architecture

AIVouch helps inspect how AI answer engines describe a business, retain scan evidence and organize reviewed follow-up actions. The working prototype uses a Python/FastAPI backend, mobile client, web interface and database-backed API. Cloud validation preserved the frozen prototype and used its existing SQLite/demo configuration, synthetic users and an internal Docker network on the existing Lightsail host.

Frozen tag `aivouch-android-cloud-beta-v11-working` and commit `02cba14c0e37adf6379b6ed20d15a45de3a504aa` remain unchanged. AWS-specific container configuration and narrowly tested dependency fixes were isolated on derived commit `cb920e94407f5c348698230754ff848ff3648ec2`. Private source was not published.

## Verified evidence

- Original baseline: 30 backend/API tests plus 5 mobile policy tests passed. Derived candidate: those 35 plus one targeted dependency-compatibility test passed; zero failures or skips within those suites. TypeScript, config, dependency consistency and smoke checks also passed.
- 18 private API checks passed: startup/readiness, registration/login boundaries, invalid requests, synthetic business create/read/update, demo-only scan evidence, ownership rejection and persisted read after restart.
- Actual AWS runtime: non-root UID, no-new-privileges, all capabilities dropped, read-only root, default seccomp and enforcing AppArmor. Limits: 256 MiB memory, 0.5 CPU, 64 PIDs, bounded writable storage; no public port or Docker socket.
- Working-set memory: 88.00 MiB idle median and 103.41 MiB small-request peak. Charged cgroup peak was 121.90 MiB. Host minimum available RAM was 799.62 MiB over monitored work; swap peaked at 33.62 MiB. No load test or production capacity claim is made.
- Clean shutdown completed in 1.11 seconds with exit 0. Disposable containers/network, generated credentials and synthetic data were removed; portfolio health remained good.

**COEXISTENCE_SAFE_FOR_LIGHTWEIGHT_DEMO** applies to that bounded test only. [Sanitized validation record](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/evidence/final/aivouch-validation.json) · [Validation diagram](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/architecture/diagrams/README.md#aivouch-validation)

## Readiness boundary

Public production exposure remains disabled pending production credentials, integrations, HTTPS/security review and final product-readiness work. Real AI-provider behavior, production database/billing and a new signed-device run were not validated. Demo scan success is not AI answer-quality evaluation. Application dependency audits found no known vulnerabilities on the validation date; base-image/OS CVEs were not independently audited. The public record is a sanitized operator validation summary, not a public release of the private test suite.

[All projects](https://github.com/arussellbishop/applied-ai-cloud-portfolio#flagship-projects) · [Cloud platform](aws-cloud-architecture.md)
