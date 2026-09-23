# Terraform platform references

Status: AWS platform implemented/proven; Terraform AWS model is reference-only and does not own that live platform. Azure and GCP are REFERENCE_ONLY_NOT_DEPLOYED. No apply, import, refresh, remote backend or authenticated cloud plan is used.

## Structure and reuse

`terraform/modules/aws_lightsail`, `azure_host` and `gcp_host` each compose cloud-native networking, ingress policy, compute and public-IP resources. Splitting these small stacks into one-resource modules would add interfaces without useful reuse. The shared `container_host` module produces an identical host contract and cloud-init document. The contract describes the Docker, private backend, CI, credential, blue/green and free monitoring boundaries.

The bootstrap intentionally writes only that contract. It does not install Docker, create deployment users, distribute secrets or pretend Azure/GCP deployments have been exercised. The existing operator-reviewed host bootstrap/deployment tooling is a separate lifecycle. A future implementation must adapt and validate it for the selected OS/cloud. This separation keeps Terraform state free of deployment private keys and avoids executing privileged scripts from changing repository content.

Terraform CLI is pinned in CI to 1.14.7; configuration accepts >=1.14.7,<1.15.0. Exact provider pins: AWS 6.66.0, AzureRM 5.6.0, Google 8.4.0. Per-environment committed lockfiles pin package checksums. Provider binaries are not committed. Version selections were checked against official release/registry endpoints and locally validated; upgrades require review and fresh validation. VM image family/latest references are conceptual and must be resolved to a tested immutable image before any deployment.

## Safe reproduction

From the repository root, use `terraform fmt -check -recursive terraform`. In each `terraform/environments/aws`, `azure` and `gcp` directory use `terraform init -backend=false -input=false -lockfile=readonly`, then `terraform validate` and `terraform test`. Every test run explicitly uses `command = plan` and a mock provider; it does not authenticate or contact a cloud. The mock fixtures are synthetic and cannot authenticate.

Normal PR CI has contents-read permission, no cloud credentials, no OIDC write permission and no apply command. IaC jobs run through the existing quality workflow; the existing required quality job depends on all three, so neither the established PR gate nor the exact-SHA production CI gate can report success before IaC completes. Other existing gates remain unchanged. tfsec reports remain visible with dated, scoped design reviews; unexpected findings fail CI.

Never point these roots at production state. `.terraform`, state, variable-value files and plans are ignored. Sensitive output flags reduce console exposure but would not encrypt state; any future real state needs separately approved encrypted storage, access control and locking. This phase creates no state backend.

Sources: [Terraform validation](https://developer.hashicorp.com/terraform/cli/commands/validate), [mock providers](https://developer.hashicorp.com/terraform/language/tests/mocking), [Terraform releases](https://releases.hashicorp.com/terraform/1.14.7/).
