# Rebuild from zero

This is a source-first recovery guide. It contains no credentials and intentionally does not perform or authorize cloud deletion.

## 1. Clone and inspect

```bash
git clone https://github.com/arussellbishop/applied-ai-cloud-portfolio
cd applied-ai-cloud-portfolio
git checkout main
```

Review the current evidence, security boundaries and cost documents before changing deployment scope.

## 2. Local prerequisites

- Git, Python 3.12+, Docker Engine and Docker Compose.
- Terraform 1.14.7 for the reference IaC checks.
- Node.js 22.23.2 and npm for diagram checks.
- A GitHub account with repository administration only where explicitly required.
- An AWS CLI supporting browser-based temporary login if AWS validation is resumed.

Do not create long-lived cloud access keys. Use short-lived human login for inspection and GitHub OIDC for automation.

## 3. Validate locally

```bash
python3 scripts/validate_publication.py
python3 scripts/validate_links.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s deploy/automation -p 'test_*.py'
docker compose -f deploy/compose.yaml config --quiet
terraform fmt -check -recursive terraform
```

Terraform environments use backend-disabled init, validation and mocked tests. They are reference checks and must not be treated as ownership of the existing production host.

## 4. GitHub Pages

The static site is under `site/`. The Pages workflow publishes that directory through GitHub Actions. It has no AWS or Lightsail dependency. Enable Pages with the GitHub Actions source if a new repository or fork has not enabled it yet.

## 5. AWS OIDC and deployment prerequisites

Recreate, rather than copy, the following outside source control:

- a main-branch-constrained GitHub OIDC provider and least-privilege deployment role, following the reviewed capstone documents;
- the repository Actions variable containing the role ARN;
- the production environment and its protected deployment secrets, if the existing host is intentionally retained;
- a pinned SSH host identity and dedicated forced-command receiver, if the existing Lightsail delivery path is intentionally retained.

Do not import or apply bootstrap resources from a new empty state without a reviewed state-recovery plan. Never commit role ARNs containing account identifiers, Terraform state, private keys or secret values.

## 6. Container build and deployment

```bash
docker compose -f deploy/compose.yaml build
docker compose -f deploy/compose.yaml up -d
curl --fail http://localhost/health
```

For the existing host, deployment must pass the exact-SHA CI gate, host-key-pinned SSH, inactive-slot health/content/SHA checks, atomic switch and external `/health` validation. The previous healthy slot remains the rollback target. A failed external validation must trigger the reviewed rollback path.

## 7. Verification and rollback

- Verify the served release SHA equals the intended main SHA.
- Verify `/` and `/health` return expected responses.
- Verify only the intended public HTTP listener exists; Docker API and backends remain private.
- Verify both slots, container limits, non-root execution, no-new-privileges, dropped capabilities and read-only controls.
- If validation fails, stop traffic change and restore the previous healthy slot through the guarded receiver.
- Record run IDs, SHA, health result and rollback result in sanitized evidence.

## 8. Secrets and state

Secrets must be injected at runtime through protected GitHub environment controls or a separately reviewed secret manager. Recreate them from authoritative sources; do not archive them in Git, public artifacts, Pages output or Terraform state. Protect any required state privately and never upload account-bearing plans or state as public artifacts.
