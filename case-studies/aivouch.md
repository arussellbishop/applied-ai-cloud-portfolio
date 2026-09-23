# AIVouch

## Validation profile

AIVouch is prepared as a later validation service. The documented runtime profile requires UID/GID 10001, dropped capabilities, `no-new-privileges`, default seccomp, AppArmor compatibility, a read-only root filesystem, bounded writable paths, a 256 MiB memory limit, one CPU, and PID limit 128.

## Current state

The host runtime has passed disposable validation for these controls. The AIVouch application itself is intentionally disabled and is not part of the public deployment.

## Boundary

This is a security and delivery specification, not a claim that the AIVouch application is deployed or externally available.
