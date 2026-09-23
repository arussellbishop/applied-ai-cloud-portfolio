# GCP validated reference

REFERENCE_ONLY_NOT_DEPLOYED. The module takes an existing project identifier and declares a custom VPC, regional subnet, target-tagged HTTP and restricted-SSH ingress, regional Standard-tier external IPv4 and one e2-small Compute Engine VM. Shared CPU is not equivalent sustained capacity to Lightsail. No project, billing account, API enablement or credentials are created.

OS Login is enabled; project-wide SSH keys and serial-console access are disabled. A dedicated service account has no project IAM grants; limited logging/monitoring OAuth scopes are ceilings, not permission grants. Human OS Login IAM assignment would remain a separately reviewed pre-deployment responsibility. No broad cloud-platform scope or wildcard IAM role is added. Shielded VM secure boot, vTPM and integrity monitoring are enabled. Backends would remain private Docker endpoints after a separately tested host bootstrap.

The intentional external IP, disabled VPC flow logs and provider-managed rather than customer-managed disk encryption remain visible scanner findings. Their cost/security tradeoffs are documented in the security review, not suppressed. Public IP does not imply public Docker, database or backend access: ingress rules allow HTTP and source-restricted SSH only. Default egress is retained for updates/provider access; no claim of egress filtering is made. Sensitive workloads need a different review.

No VPC, VM, address, service account or firewall rule has been deployed. Schema and mocked plans do not test OS Login access, image/zone availability, billing prerequisites or runtime bootstrap. No NAT, load balancer, managed database or paid monitoring deployment is included.

Source: [Google Compute instance](https://registry.terraform.io/providers/hashicorp/google/8.4.0/docs/resources/compute_instance).
