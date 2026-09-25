# Portfolio recovery manifest

The canonical source is GitHub. A large offline recovery copy should be held in Google Drive plus a local Ubuntu copy. AWS is not the canonical archive and must not be treated as the only copy.

| Material | Classification | Recovery action |
|---|---|---|
| Git repository, branches and tags | SOURCE-CONTROLLED | Clone and retain a periodic mirror. |
| Markdown documentation and evidence | SOURCE-CONTROLLED | Retain the repository and an offline export. |
| Architecture diagrams and sources | SOURCE-CONTROLLED | Retain Mermaid sources and rendered exports if needed. |
| Terraform modules and locks | SOURCE-CONTROLLED | Retain source and lockfiles; never state or credentials. |
| Dockerfiles and Compose | SOURCE-CONTROLLED | Rebuild from source and verify image digests where available. |
| GitHub workflows and scripts | SOURCE-CONTROLLED | Retain with commit history and CI evidence. |
| Dependency lockfiles | SOURCE-CONTROLLED | Retain exact versions and checksums. |
| MSc source, dissertation and module work | MUST ARCHIVE | Archive only the versions and datasets permitted for sharing. |
| Project source from private repositories | MUST ARCHIVE | Export privately where ownership and licence permit; do not publish by default. |
| Licensed or sensitive datasets | MUST ARCHIVE | Preserve only where licence and retention rules allow; otherwise preserve lineage and acquisition instructions. |
| CV source files and application materials | MUST ARCHIVE | Store in the private recovery archive, not the public site unless intentionally published. |
| Certification evidence | MUST ARCHIVE | Store verification records privately; publish only approved summary claims. |
| Built static site | REGENERATABLE | Rebuild from `site/` and the Pages workflow. |
| Docker images and containers | REGENERATABLE | Rebuild from source; do not treat running containers as the archive. |
| Terraform plans and validation reports | REGENERATABLE | Recreate from source; keep only sanitized evidence in public Git. |
| AWS OIDC provider, IAM roles and deployment secrets | SECRET — DO NOT ARCHIVE | Recreate through reviewed IaC/control-plane procedure. |
| AWS access keys, browser sessions and tokens | SECRET — DO NOT ARCHIVE | Never export or commit. |
| SSH private keys, known-host private material and environment secrets | SECRET — DO NOT ARCHIVE | Recreate through protected operator/GitHub controls. |
| Terraform state containing account/resource data | SECRET — DO NOT ARCHIVE | Keep private under a reviewed state-recovery process. |

## Archive checks

1. Run the repository publication and secret scans before exporting.
2. Exclude `.env*`, private keys, tokens, Terraform state/plans, provider binaries, logs, caches and generated credentials.
3. Record archive date, source commit and checksum in a private manifest.
4. Test restoring a clean clone and rebuilding the Pages site.
5. Keep at least one local Ubuntu copy and one separate Google Drive copy.
