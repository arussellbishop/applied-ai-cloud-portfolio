# Portfolio deployment

`deploy-aws` runs on pushes to `main`. Its `ci-gate` job requires successful push runs of documentation, quality, container-config, and security for that exact commit. Required branch checks are the actual job names: `links`, `quality`, `compose`, and `scan`. The independent pull-request review requirement remains enabled.

The deploy job uses the `production` environment, restricted to the `main` branch. Environment secrets are `AWS_DEPLOY_HOST`, `AWS_DEPLOY_KEY`, and `AWS_KNOWN_HOSTS`. The known-host entry comes directly from the existing host's ED25519 public key over the authenticated management connection. Strict host-key checking is mandatory; the workflow never learns a key from an unauthenticated network scan.

The dedicated ED25519 credential authenticates as `portfolio-deploy`. Its root-owned authorized-key entry uses `restrict` and a forced command. The account has no Docker group access. Its only sudo permission runs the root-owned receiver, which accepts exactly `deploy` and a full lowercase commit SHA. The receiver independently verifies current main and all four CI results through GitHub's public HTTPS API. API errors, rate limits, failed checks, and stale commits fail closed. No GitHub credential is stored on the production host.

## Release boundary

Only regular static files under `site/` are accepted from the exact GitHub commit archive. Traversal, links, unsupported files, and excessive sizes are rejected. Repository Dockerfiles, Python, workflows, and shell scripts are never executed by the receiver. Runtime files come from the root-owned host template at `/opt/portfolio-deploy/template`. Updating the receiver or runtime template requires a separate operator-reviewed installation; committing a new receiver does not install it.

SHA-named directories and distinct image tags retain previous releases. All three existing services keep their established private network and public HTTP configuration. AIVouch remains disabled. No Docker TCP API, new AWS resource, bundle change, domain, or TLS configuration is introduced.

GitHub concurrency serializes production jobs without cancellation. A host filesystem lock rejects overlapping deployment attempts. The receiver checks for a superseding main commit again after building and before activating containers.

## Health and rollback

Compose waits for container health. The receiver checks all three containers, the exact release identifier from `/health`, and byte-for-byte landing-page content. Only then does it atomically change `/opt/portfolio-deploy/current` and record `/opt/portfolio-deploy/previous`. A switch or health failure restores the previous image tags with `--no-build`, verifies their health, and exits unsuccessfully. No automatic pruning removes rollback images or directories.

The workflow additionally checks public HTTP from the GitHub-hosted runner. A failure of this external check marks the run failed and requires investigation; it does not blindly roll back a locally healthy service because an external network outage may be unrelated to the release.

An operator can recover using the previous root-owned release:

```sh
previous=$(readlink -f /opt/portfolio-deploy/previous)
sudo docker compose --project-name applied-ai-private --project-directory "$previous" \
  -f "$previous/compose.yaml" -f "$previous/images.yaml" \
  up -d --no-build --wait --wait-timeout 100 portfolio api caddy
```

After checking `/health` and the page, the operator should update the root-owned `current` symlink to that release. The restricted credential deliberately cannot select an arbitrary old release or obtain a shell.

## Validation

```sh
python3 scripts/validate_publication.py
python3 -m unittest discover -s deploy/automation -p 'test_*.py'
```

Tests cover non-main rejection, failed CI rejection, archive traversal and symlink rejection, and restoration of the previous release after health failure. Production activation is established by a successful `deploy-aws` run and matching public release SHA, not by these unit tests alone.
