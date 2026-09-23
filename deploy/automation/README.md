# Blue/green portfolio deployment

`deploy-aws` accepts main pushes and main-only manual dispatch. All four existing CI workflows must succeed for the exact current main SHA; the receiver repeats this gate before starting and before switching. Branch protection, production environment, secrets, strict SSH host pinning, forced-command account, and deployment concurrency remain in place.

The root-owned receiver maintains BLUE and GREEN records under `/opt/portfolio-deploy/bluegreen`. It starts a candidate only in the inactive slot and verifies container health, exact API SHA, exact page bytes, and the expected page marker on the private Docker network. No backend port is published. Each slot has a 96 MiB portfolio container and 128 MiB API container, no swap allowance, CPU/PID limits, read-only filesystem, dropped capabilities, and no-new-privileges. Candidate work stops below 384 MiB available host memory.

A successful candidate becomes eligible for a single Caddy reload transaction. The existing public Caddy container is never recreated by deployment. Both API and page upstreams change in one configuration load. The prior healthy slot continues running. The startup config resides in the existing Caddy volume and is atomically replaced; a journal restores the previous healthy routing if a switch is interrupted. Caddy's admin endpoint stays on its container loopback and is reached using operator-controlled Docker exec, not a public port. See the [Caddy API transaction documentation](https://caddyserver.com/docs/api#post-load).

A pre-switch failure leaves active routing unchanged and restores the prior inactive slot after removing the failed candidate. A post-switch validation failure switches back to the previous healthy slot and fails the run. Versioned candidate files and reports remain as evidence. No global image pruning runs.

## Operator installation

Review this source and run `bootstrap_bluegreen.py` once as the host operator. It adopts the existing portfolio/API as BLUE, preserves the running Caddy container, prepares restart-safe imported configuration, and installs the restricted receiver. Routine GitHub deployments cannot install privileged source. A receiver update requires separate operator installation.

The existing SSH wrapper and sudo authorization are unchanged. The receiver accepts only a fixed release command plus a full lowercase SHA: deploy, rollback, confirm, status, or probe. Deploy and probe require successful CI for current main. Rollback and confirm reject stale active SHAs. Status exposes only deployment metadata. No interactive shell or arbitrary command is accepted.

## Live diagnostics and reporting

A manual main dispatch with `unhealthy_candidate=true` runs the normal inactive-slot preparation with a deliberately failing portfolio health command. It must fail before the traffic switch, restore the previous inactive slot, and leave active public service healthy. The mode cannot select arbitrary application code or an unapproved branch.

GitHub's step summary reports candidate/active SHA, active/candidate slot, health, switch, external validation, rollback, final status, available memory, and sampled external HTTP interruption. A background runner probe measures public HTTP during the operation. A failed diagnostic remains a failed workflow, even when isolation behaves correctly. Summaries are native GitHub reporting; notification delivery depends on repository/account preferences and is not claimed as separately configured alert delivery.

Run local validation with:

```sh
python3 scripts/validate_publication.py
python3 -m unittest discover -s deploy/automation -p 'test_*.py'
```
