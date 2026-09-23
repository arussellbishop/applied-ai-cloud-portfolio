# AI Operating System

## Evidence-backed result

The working architecture is Android / Termux → private mesh networking → AWS Lightsail → SSH → tmux → Codex. It gives a mobile operator a persistent terminal workspace without moving hardware-dependent work or heavy local datasets to the host.

## Design choices

- tmux preserves active terminal work across client disconnects.
- Git and documentation remain first-class delivery artifacts.
- Lightweight services are bounded; heavy ML, hardware integrations, and large datasets remain outside this host.
- The deployment is validated privately before any public exposure.

## Boundary

This case study describes a proven access and operating model. It does not claim a production AI platform, a migrated data estate, or a replacement for local hardware workloads.
