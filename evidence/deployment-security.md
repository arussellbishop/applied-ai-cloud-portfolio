# Deployment and security evidence summary

- Docker Engine, Compose, Buildx, containerd, and runc were validated on the existing host.
- Disposable tests passed for no-new-privileges, default seccomp, AppArmor, dropped capabilities, read-only roots, bounded tmpfs, resource limits, and non-root execution.
- Caddy, portfolio, and API were validated privately before HTTP activation.
- The public HTTP release exposes only the reverse proxy; backend ports and the Docker API remain private.
- A previous release remains available for rollback.

This summary intentionally omits host addresses, account identifiers, raw firewall output, credentials, private paths, and private-network details.
