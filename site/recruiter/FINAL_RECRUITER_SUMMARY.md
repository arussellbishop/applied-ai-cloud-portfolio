# Applied AI + Cloud/Platform Engineering

This portfolio brings together applied AI application work and hands-on cloud/platform engineering, with a clear distinction between what runs, what was validated privately and what remains research.

Its strongest implementation is a small AWS Lightsail platform delivered through GitHub Actions, restricted deployment credentials and Docker blue/green releases. Candidate health and exact Git SHA are checked before Caddy switches traffic. Recorded exercises demonstrate unhealthy-candidate isolation, rollback capability and zero seconds of observed interruption during one measured deployment—not a universal availability guarantee.

AIVouch provides complementary application evidence: a preserved working prototype, 36 passing candidate tests, 18 private AWS API checks and effective non-root, no-new-privileges, capability, filesystem and resource controls. Public production exposure remains disabled; real integrations and product-readiness work are not presented as complete.

Terraform modules and credential-free CI demonstrate portability and architectural judgement across AWS, Azure and GCP. Only AWS is deployed. The reference designs retain visible security trade-offs and avoid creating idle cloud infrastructure.

Historical AI OS, Air Marshal and quantitative research dossiers add orchestration, computer-vision and evaluation-methodology context, with incomplete navigation, provenance and reproducibility clearly identified. The engineering approach is to preserve evidence, test boundaries, report negative results and keep heavy compute local. The work is tool-assisted and evidence-reviewed; it makes no unsupported claim about seniority, enterprise scale or business impact.

[Project evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio#flagship-projects) · [Role matrix](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/recruiter/FINAL_ROLE_EVIDENCE_MATRIX.md)
