# Phase 19A baseline — 2026-09-24 UTC

Implementation began approximately 15:38 UTC. Target 6–10 active hours; hard maximum two days. No further engineering programme follows this capstone.

| Check | Observed result |
|---|---|
| Public main / local clean main / live release | `4562ca3fa0a6f582ca8b29262d2b5bac55fab935` |
| Main workflows | quality, documentation, security, container-config, deploy-aws: success |
| HTTP / and /health | 200 using public address from host; not an independent external probe |
| Docker | Five production/rollback containers healthy |
| Management | SSH, Tailscale, Docker active; no Docker TCP API listener |
| RAM | 1,998,614,528 total; 1,228,664,832 available bytes |
| Swap | 2,147,479,552 total; 72,769,536 used bytes |
| Disk | 50,875,670,528 available bytes |
| Load | 1.31 / 1.09 / 0.96; 2 vCPU according to previous baseline |
| Region | eu-north-1, verified through metadata without retaining identity document |
| Recurring architecture | One existing Lightsail host; Caddy and two healthy blue/green portfolio/API slots |
| Existing monthly cost | ESTIMATED USD 12, user-reported bundle; billing unverified |
| Account-wide unrelated resources | UNKNOWN: current host has no authorized control-plane credentials |

No production settings, firewall rules, static IP, deployment behavior or management access changed. No AWS application resource created. A separate Git worktree/branch holds the bootstrap; main stays unchanged.

Kubernetes decision deferred to Phase 19G resource precheck. Existing swap use and limited RAM require caution; no cluster or tool installed in this phase.

## Authentication and continuation

No static access keys requested or created. A non-root AWS Console identity runs the reviewed CloudShell bootstrap once. Normal automation then uses exact-repository, main-only GitHub OIDC. AWS caller account identifiers are derived privately; not embedded in source or returned to chat.

CloudShell inventory will report service/region counts only. Missing permissions are UNKNOWN. Counts alone cannot prove that no unrelated resources exist or establish ownership. AWS account-wide verification remains pending at this checkpoint.

## Acceptance status

PHASE19A_LOCAL_BASELINE = PASS
OIDC_CONFIGURATION = PREPARED, NOT APPLIED
AWS_ACCOUNT_INVENTORY = PENDING_CLOUDSHELL
CAPSTONE_COST_LIMIT = USD 5
AWS_AI_PLATFORM_CAPSTONE_PROVEN = NOT_CLAIMED
