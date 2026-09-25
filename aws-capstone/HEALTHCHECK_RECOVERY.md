# Existing-container health failure diagnosis — 2026-09-25

Status: **FIX_VALIDATED_ON_HOST; LIVE_MIGRATION_PENDING_REVIEW**.

Main remains `0066a17fa638d505654f145b51179b31bbf32dae`; production serves `4562ca3fa0a6f582ca8b29262d2b5bac55fab935`. This repair does not change OIDC, IAM, branch protection, AWS resources or recurring resource cost.

## Read-only findings

| Container | Initial Docker health | Direct HTTP | Classification |
|---|---|---|---|
| portfolio-blue-portfolio | Unhealthy; probe timeout | 200, 64 ms | E + C |
| portfolio-blue-api | Unhealthy; probe timeout | 200, 233 ms; expected SHA | E + C |
| portfolio-green-portfolio | Unhealthy; probe timeout | 200, 4 ms | E + C |
| portfolio-green-api | Initially healthy, later intermittent failure | 200, 70 ms; expected retained SHA | E + C |
| applied-ai-caddy | Healthy | Public HTTP and health 200 | No detected failure |

E is CPU resource pressure; C is a probe definition whose repeated interpreter/library startup exceeds the total deadline under that pressure. No evidence of A (genuinely failing service), B (wrong command path/URL), D (startup dependency failure) or F (stale health state) explains the observed failures. Current health logs record repeated `Health check exceeded timeout (3s)` with no OOM kills. The containers had been running about 40 hours, so a longer startup grace period would not address this incident. Some application logs contain broken pipes, consistent with clients/probes closing connections; endpoints remain responsive when measured independently.

The actual blue/green runtime definition is in `deploy/automation/deploy.py`, which creates containers directly. The retained Compose file is not the running slot configuration: it lists 20/30-second intervals and five-second timeouts, while Docker inspect and the receiver show a two-second interval and three-second timeout. The URLs are correct: portfolio loopback port 8080 `/`, API loopback port 8000 `/health`. Public `/health` is reverse-proxied to the already-running API process; it does not start a new Python interpreter.

The old probe starts Python and imports `urllib.request` each time. Measured import wall times were 10.50, 7.74, 17.02 and 10.71 seconds for blue portfolio/API and green portfolio/API respectively. All exceed the entire Docker deadline before the request starts. The requests themselves succeeded when allowed to complete. Direct host-to-container HTTP took 4–233 ms. Public `/health` took 12 ms; host localhost `/health` took 23 ms.

Lightsail metrics corroborate CPU exhaustion: recent burst-capacity averages were about 0.0058%, while CPU utilization remained near the 20% baseline. Host samples showed 38–69% CPU steal. This explains the difference between wall time and process CPU time. Repeated Python probes add avoidable CPU demand; these measurements do not attribute all historical burst-credit consumption to the probes. See [AWS CPU burst metrics](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-resource-health-metrics.html) and [Docker probe timeout semantics](https://docs.docker.com/reference/cli/docker/container/run/).

RAM was approximately 979 MiB available at the initial inspection, with 406 MiB swap occupied but no swap-in/out in the sampled intervals. Root disk was 21% used with 46 GiB available; load was approximately 1.2–1.5. This is CPU pressure, not demonstrated RAM/disk exhaustion.

## Minimal correction and validation

Use the existing Alpine `/bin/busybox wget` HTTP client with `exec`, a two-second request timeout, and response consumption to `/dev/null`. No dependency installation is needed. Keep the three-second Docker timeout, two-second interval, three retries and two-second start period unchanged. Keep all CPU/memory/PID/security limits, private exact-SHA/content validation and fail-closed traffic gates unchanged.

Twelve direct native-probe trials across all four production containers succeeded in 0.41–1.93 seconds including Docker exec overhead. Then four temporary application containers were created in two sequential slot pairs using the existing exact images, the corrected receiver's actual start command and unchanged limits. All four became Docker HEALTHY and passed private exact-SHA/page-content checks; each pair remained healthy for at least 30 seconds. No ports were published. The temporary containers were removed.

During this validation, 101 public HTTP/health sampling rounds had zero failures; minimum available RAM was 846.3 MiB, above the receiver's 384 MiB floor. CPU capacity remains constrained, so sustained post-migration observation is still required. The opt-in `check_health_probe.py` integration fixture exercises the actual emitted command and passes success, HTTP 503 rejection, stalled-response timeout and connection-refusal checks. It runs in normal quality CI. All ten existing receiver safety tests pass locally, including unhealthy-candidate rejection and rollback behavior.

After cleanup, 34 security/availability checks pass: only the original five containers remain; their start times and probes are unchanged; listener endpoints match the established baseline; no Docker TCP API is listening or reachable; private/Docker HTTP paths return 404; container hardening and public port bindings are preserved; the installed privileged receiver still matches main. No runtime migration, traffic change, forced deployment or health-state modification occurred.

## Governance and remaining work

Live production still uses the old probe definitions and is not yet fully Docker HEALTHY. The passing temporary candidates do not imply that production has been repaired. A source merge does not automatically install the root-owned receiver or update immutable container health definitions. Follow the operator recovery sequence in the [deployment README](../deploy/automation/README.md#health-probe-under-cpu-pressure) only after review/merge. Preserve current serving containers until a corrected private replacement is healthy and matches the expected release/content. A review gate must not be bypassed without new explicit authorization.

After live repair, require both slots healthy, adequate headroom and security checks before retrying deployment. Then verify all main CI, OIDC, healthy candidate, atomic switch, exact intended main SHA, continuous public HTTP/health and retained healthy rollback. Those post-merge results are pending; this document does not claim them.


## Final validation update — 2026-09-25

The repair is merged and installed; production now serves main `d7172af2ecb25d2c8f3a700e5af4b5a043172841` with all containers healthy. OIDC, deployment, security and rollback pass. Repeated external monitoring failures leave zero-failure acceptance blocked. See [final validation](FINAL_VALIDATION.md); historical pending-review statements above are superseded by that record. The capstone is not marked COMPLETE.
