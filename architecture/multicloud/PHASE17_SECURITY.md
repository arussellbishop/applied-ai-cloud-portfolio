# Security design and static analysis

The IaC reference exposes HTTP public content and explicit-source SSH only. It defines no public Docker API, database or application backend ports. No provider credential, private SSH key, real account identifier, secret variable file, state or deployment endpoint is committed. Public keys are inputs, not generated credentials. Terraform sensitive outputs are redaction only; state must still be protected before any future authorized deployment. Existing GitHub secret and restricted-receiver boundaries are unchanged.

Public HTTP is an intentional existing architecture limitation: no authentication/user data is served there. Domain/HTTPS is not implemented in this phase. SSH source allowlists are a reference requirement and not a claim about dynamic hosted-runner reachability on the existing platform. Cloud control-plane identities and OS identities differ; portability does not erase IAM design.

## Findings, not a clean-scan claim

The pinned lightweight tfsec 1.28.14 scan reports zero findings for AWS and Azure and three for GCP: one HIGH (public IP) and two LOW (VPC flow logs disabled, no customer-managed encryption key). The public IP enables the explicitly intended single-host HTTP endpoint without a load balancer; provider-managed encryption still protects disks at rest; flow logging/retention is deferred to avoid unapproved paid monitoring. These are accepted reference-design risks, not assurances suitable for sensitive production workloads.

All raw findings are retained. `terraform/security-review.json` scopes the reasons to exact cloud, rule, severity and source file and expires on 2026-12-23. CI rejects unreviewed findings and expired review. No tfsec ignore annotations or excluded checks are used. A project-key finding during development exposed tfsec's handling of string metadata; boolean HCL values, converted by the provider to metadata strings, make the intended prohibition explicit and pass that rule. The final finding set remains visible in job summaries/artifacts.

tfsec is a mature scanner whose development focus moved to Trivy. Its rules have uneven provider coverage, particularly Lightsail, and a zero finding count is not comprehensive proof. Repository-specific checks additionally forbid provisioners, imports, backends, secret-producing resources and cloud-secret workflow inputs; they check /32 validation. They complement rather than replace HCL/schema analysis and human review.

NSG wildcard source ports are required for arbitrary client ephemeral ports; deny-all wildcard rules are intentional denial. GCP service-account scopes grant no IAM access by themselves. Default outbound networking is not represented as locked down. No cloud IAM wildcard permission is created. No live security controls were modified.

Sources: [tfsec transition notice](https://github.com/aquasecurity/tfsec/discussions/1994), [GCP public-IP rule](https://aquasecurity.github.io/tfsec/v1.28.14/checks/google/compute/no-public-ip/), [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).
