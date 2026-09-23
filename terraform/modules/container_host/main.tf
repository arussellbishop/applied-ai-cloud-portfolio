terraform {
  required_version = ">= 1.14.7, < 1.15.0"
}
# A shared bootstrap boundary, not an untested Docker installer.
# This creates only a documentation file if ever supplied to a NEW reference VM.
# Host operator must review/install the separately versioned Docker/deployment stack.
locals {
  contract = {
    schema             = 1
    public_ingress     = "Caddy HTTP only; no authentication or personal data"
    private_backends   = "Docker bridge; no published application/database ports"
    deployment         = "Restricted forced-command SSH; pinned host key; CI-gated immutable SHA"
    traffic            = "Inactive candidate health/SHA validation; atomic switch; retained rollback slot"
    container_controls = ["non-root", "no-new-privileges", "cap-drop ALL", "read-only root", "bounded memory/CPU/PIDs"]
    credentials        = "Provision outside cloud-init/Terraform; never place secrets in state"
    monitoring         = ["GitHub job summary", "Docker health", "/health", "public HTTP", "disk", "MemAvailable", "service state"]

  }
}
output "cloud_init" {
  description = "Writes the reviewed contract only; does not install Docker or configure SSH."
  value       = "#cloud-config\n${yamlencode({ write_files = [{ path = "/etc/portfolio-host-contract.json", permissions = "0644", owner = "root:root", content = jsonencode(local.contract) }] })}"
}
output "contract" {
  value = local.contract
}
