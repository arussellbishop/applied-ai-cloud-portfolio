# Applied AI Systems

A recruiter-facing portfolio about building useful AI systems with clear operational boundaries. The site focuses on architecture, validation, documentation, lightweight services, and repeatable delivery.

## Featured work

- [AI Operating System](case-studies/ai-operating-system.md) — Android / private networking / SSH / tmux / Codex working architecture.
- [AIVouch](case-studies/aivouch.md) — application validation and container-security profile prepared for later implementation.
- [Air Marshal](case-studies/air-marshal.md) — reserved case-study area; claims remain limited until public source evidence is added.
- [Quantitative Intelligence](case-studies/quantitative-intelligence.md) — reserved case-study area; claims remain limited until public source evidence is added.
- [AWS and cloud architecture](case-studies/aws-cloud-architecture.md) — low-cost control-host design, private validation, rollback, and public activation boundaries.

## Local validation

The repository is designed for GitHub-hosted CI. It uses simple static HTML and small Python validation scripts. CI checks documentation links, public-safe content, Python syntax, dependency metadata, and Compose configuration. The [AWS deployment workflow](deploy/automation/README.md) deploys static portfolio content after all four CI workflows pass on main.

Production activation remains a human-approved operation outside this repository's CI.
