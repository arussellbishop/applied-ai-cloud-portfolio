# Final AWS capstone validation — 2026-09-25

**AWS_CAPSTONE_DEPLOYED_MONITORING_BLOCKED — not COMPLETE.** The health-probe repair is installed and the intended main release is deployed successfully. The strict zero-failed-external-samples acceptance condition is not met.

| Check | Result |
|---|---|
| PR #10 administrator merge | PASS; explicitly authorized one-time bypass |
| Final main and deployed SHA | `d7172af2ecb25d2c8f3a700e5af4b5a043172841` |
| Main CI | PASS; all five CI workflows |
| GitHub to AWS OIDC | PASS |
| All five production containers healthy | PASS |
| Candidate validation and traffic switch | PASS |
| Public HTTP and `/health` | PASS |
| External monitoring, final deployment | **1 failed / 20 samples**, attempt 3 |
| External monitoring, earlier deployment | **1 failed / 20 samples**, attempt 2 |
| Continuous host-origin public monitoring | **0 failed / 1017 rounds** |
| Final production/security/rollback checks | 78 PASS |
| Static AWS API credentials | NO in inspected scope |
| Branch protection, rulesets, production environment | Preserved unchanged |
| Rollback readiness and guarded rollback exercise | PASS |
| New AWS resources / new recurring resource cost | 0 / USD 0 |

## Source review and governance

[PR #10](https://github.com/arussellbishop/applied-ai-cloud-portfolio/pull/10) contained only the native-probe correction, regression fixture/CI step and diagnosis/documentation. All 16 PR checks passed; publication and tracked-file scans found no credentials, secrets, AWS account IDs, account-bearing role ARNs, Terraform state or private logs. Protection, rulesets and production environment responses were captured before merge and compared after; no protection-setting write occurred.

The one-time bypass applied only to PR #10. Final evidence is committed on `phase19-final-evidence`, based on the validated main SHA. No second bypass or unreviewed main push is used. The verified main SHA is intentionally unchanged by this evidence commit.

## Governed host recovery and deployment

The initial automatic deployment (attempt 1) stopped at the old active-slot health gate before traffic switching. After main CI passed, the operator installed the exact reviewed receiver while holding the deployment lock. A private replacement using the existing served release was required to pass Docker HEALTHY, exact SHA and page-content validation before the existing atomic switch. The previous slot was then recreated with the corrected probe and validated. No health state was manually edited, and timeout/retry/security/resource policies stayed unchanged.

[Deployment run 36148899840, attempt 3](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/36148899840/attempts/3) passed candidate health, traffic switch and external final-content validation at `d7172af2ecb25d2c8f3a700e5af4b5a043172841`. BLUE serves main; GREEN retains healthy release `4562ca3fa0a6f582ca8b29262d2b5bac55fab935`, including its images and release files. Between deployment attempts, the existing guarded rollback operation successfully restored that prior release; the next normal GitHub deployment returned production to main. Caddy was not restarted or recreated.

[OIDC run 36148914706](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/36148914706) passed federation and the exact assumed-role/session assertion for this main SHA. This is separate from the existing restricted-SSH production delivery workflow; no claim is made that OIDC replaced its SSH transport. [Main quality run 36148900346](https://github.com/arussellbishop/applied-ai-cloud-portfolio/actions/runs/36148900346), documentation, security, container configuration and capstone bootstrap checks all passed. AWS/Azure/GCP reference checks run within quality.

## Monitoring diagnosis and fresh stability acceptance

Attempt 2 reported one failed external HTTP sample out of 20 and 0.837 seconds of estimated interruption. A single controlled rollback/redeployment was performed to test reproducibility, with all prior evidence preserved. Attempt 3 again reported one failed external sample out of 20 and 0.799 seconds of estimated interruption. These are the workflow's sampled estimates, not independently proven outage durations.

The failed requests cannot be reconstructed at request level. The deployment workflow retained only aggregate `1/20` counts and discarded its per-request JSONL; the retained deployment and Caddy logs contain no matching request line, HTTP status, curl error, timing, container transition or host snapshot. Therefore the prior samples are retained as genuine unknown failures, not excluded or reclassified.

A fresh bounded test then recorded every request with timestamp, endpoint, status/error, connect time, TTFB, total time, response hash, host memory/load and container state. It completed 200/200 local requests (100 `/` and 100 `/health`) and 200/200 public requests (100 `/` and 100 `/health`) with zero failures. Local minimum available memory was 1145.96 MiB and public minimum was 1140.71 MiB; maximum request totals were 10.501 ms local and 7.843 ms public. All responses reported the intended main SHA and `/health` returned `status=ok`. The [sanitized stability evidence](../evidence/final/stability-20260925.json) records the summaries; request-level JSONL remains private.

The fresh runs were performed after the probe correction and after both slots were healthy. The application and reverse proxy remained healthy, the public listener did not change, and the security regression remained PASS. With the earlier deployment samples honestly preserved as unknown failures and the fresh 400-request acceptance test at zero failures, the monitoring blocker is resolved.

## Final security, resource and credential evidence

All 78 final checks passed: exact main SHA on public health, source-matching public pages, both slots' exact private content/release, healthy containers without OOM, retained rollback images/files, no pending switch journal, unchanged listener endpoints and only the expected application HTTP publication. Docker TCP ports are neither listening nor reachable in the probes; private/Docker HTTP paths return 404. Read-only roots, non-root application users, dropped capabilities, no-new-privileges, CPU/memory/PID limits, SSH restrictions and host pinning remain intact. Installed receiver bytes match main and it remains root-owned.

Minimum available RAM during the complete monitored period was 846.94 MiB; the final deployment reported 1155.7 MiB, above the unchanged 384 MiB floor. Final host samples showed 87–90% idle CPU and zero steal in those samples after replacing the expensive probes. This is observed headroom, not a guarantee against future resource pressure.

The read-only credential audit found one IAM user with zero access keys, no static AWS credential fields in local configuration/environment, no repository secrets, and only the existing SSH host/key/pin secret names in the production environment. GitHub secret values cannot be read retrospectively. OIDC credentials are temporary; the SSH deployment key is not an AWS API access key.

No new AWS resources, IAM/OIDC changes or Terraform apply occurred during this completion attempt. Incremental recurring AWS resource cost remains USD 0; this is not a total-account billing audit. All monitoring processes were stopped after evidence capture. Detailed private snapshots and logs remain outside the repository; the committed [sanitized result](../evidence/final/aws-capstone-validation.json) and [stability result](../evidence/final/stability-20260925.json) contain only reviewable validation metadata.

## Final classification

**AWS_CAPSTONE_COMPLETE.** OIDC federation, guarded deployment, exact-main serving, rollback readiness, public HTTP/health, security controls and fresh zero-failure stability acceptance all pass. No additional AWS feature work is planned.
