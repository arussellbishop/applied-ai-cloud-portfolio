# MULTI-CLOUD PLATFORM ENGINEERING

A small cloud platform demonstrates repeatable delivery and architectural judgment without paying for three idle environments.

**AWS: implemented/proven. Azure and GCP: Terraform-validated reference architectures, not deployed infrastructure.** The Terraform AWS reference also remains separate from ownership of the live Lightsail host.

The live AWS platform uses GitHub CI, restricted SSH deployment, a single bounded Lightsail host, private Docker BLUE/GREEN slots and Caddy traffic switching. Candidate health and exact Git SHA are checked before traffic changes; the previous healthy slot is retained for rollback. Public HTTP serves portfolio content only.

Reusable Terraform modules map that operational contract onto Lightsail, Azure VNet/NSG/Linux VM and GCP VPC/firewall/Compute Engine patterns. A shared host contract describes the runtime bootstrap boundary. Provider versions/checksums are pinned, PR CI validates all three references without cloud credentials, and offline mocked plans exercise module outputs without creating resources.

Static security evidence retains three GCP findings: one HIGH for the intentional public IP and two LOW for flow logging and customer-managed disk keys. The HIGH is an accepted reference-design trade-off, not a false positive or proof that the design is suitable for sensitive production workloads. Static security evidence includes visible GCP design tradeoffs: a deliberate public IP, provider-managed encryption and deferred flow logging. These are not presented as a clean security scan. The public/backend boundary and source-restricted management model are explicit; real deployment keys, account identifiers and endpoints are absent from public artifacts.

FinOps keeps a low-cost always-on application/control plane in AWS and heavy ML/research compute local. Azure/GCP cost components are documented without inventing live bills. No new recurring cloud infrastructure was created for this evidence.

Limits: provider/schema and mocked-plan validation do not prove regional SKU availability, a working Azure/GCP host, cloud IAM access or production readiness. Bootstrap, HTTPS, sensitive-data use and live cloud integrations would need separately authorized work.

[Terraform, architecture diagrams and evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/tree/main/architecture/multicloud)

[Terraform source](https://github.com/arussellbishop/applied-ai-cloud-portfolio/tree/main/terraform)
