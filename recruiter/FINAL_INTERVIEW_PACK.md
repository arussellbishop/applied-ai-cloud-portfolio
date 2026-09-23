# Interview evidence pack

Use these as evidence-grounded talking points, adjusted to your personal contribution. Historical records are not presented as fresh independent reproductions.

## AI Operating System

### 30-second version

I needed a persistent, reviewable workspace for tool-assisted engineering. I used a mobile-to-Linux access model with private networking, SSH, tmux and a Git-based evidence trail. The decision was to keep consequential publication behind explicit approval and CI rather than equating task completion with safe deployment. The access model is established; older scheduling records provide context, but retries and connector reliability are not fully proven. I would test those boundaries next.

### 2-minute version

**Problem:** Engineering work spans mobile sessions, local hardware and cloud services; context and evidence can be lost between them.

**Decision:** Use a persistent terminal workspace and explicit publication boundaries, keeping orchestration separate from authorization.

**Implementation:** The established path connects Android/Termux through private access to SSH/tmux and the Linux Codex/Git workspace. The current programme records work in branches, tests and PRs, with operator authorization for protected-main administrator merges. Earlier public records describe a local dashboard, central-cycle scheduling, sleep inhibition and backup checks.

**Trade-off:** This is a practical operating model with tool assistance, not a demonstrated general autonomous platform. A tmux session does not make a host failure harmless, and a listed timer does not establish reliable task execution.

**Validation:** The remote working model supports the completed cloud programme. The local orchestration evidence is a dated dashboard/timer and backup summary; I did not rerun that separate system in the final audit. Connector freshness, general retries and independent recovery remain incomplete.

**Result:** There is a defensible working boundary between operator intent, agent-assisted execution and reviewed publication, with evidence rather than status labels supporting claims.

**What I would improve next:** Identify authoritative runnable orchestration source, test failed schedules and idempotent retries, and demonstrate recovery with a declared failure model. I would not claim those future tests already passed.

[Evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/case-studies/ai-operating-system.md)

## AIVouch

### 30-second version

I validated an existing AI-visibility application on the small AWS host without changing its frozen prototype or making it public. I isolated deployment changes, used its SQLite/demo mode and synthetic data, and tested a hardened non-root container. The candidate passed 36 tests and 18 API checks, with roughly 88 MiB idle memory. The result is private cloud-validation evidence, not production AI quality or a completed product launch. Live integrations remain a separate readiness gate.

### 2-minute version

**Problem:** A working AI-visibility prototype needed credible cloud evidence without risking its frozen baseline, exposing authentication over HTTP or adding managed services.

**Decision:** Validate privately on the existing Docker host using the application's supported SQLite/demo configuration, not redesign the database or request unnecessary production credentials.

**Implementation:** A separate validation branch carried hardened container configuration and narrow dependency fixes. The runtime used a dedicated internal network, no published ports, generated temporary credentials, non-root execution, NNP, dropped capabilities, a read-only root and bounded memory/CPU/PIDs.

**Trade-off:** Demo integrations prove routing, state handling and boundaries, not live provider behavior or answer quality. The public evidence is a sanitized summary; private source stays private.

**Validation:** The original 35 tests were reproduced; the derived candidate passed those plus a targeted compatibility check. Eighteen API checks covered health, authentication, invalid input, synthetic writes, demo evidence and restart persistence. Actual kernel controls were inspected. Working-set memory measured about 88 MiB idle and 103 MiB during small requests; no load test was performed.

**Result:** The bounded private AWS validation passed and demonstrated lightweight-demo coexistence. Temporary containers, credentials and synthetic data were removed, and the portfolio remained healthy.

**What I would improve next:** Review production integrations/database, authentication, privacy, HTTPS, base-image vulnerabilities and AI-quality evaluation before any public product exposure. None of those missing checks is hidden behind the validation result.

[Evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/case-studies/aivouch.md)

## Air Marshal

### 30-second version

Air Marshal explores perception and target-loss handling with a small drone. The accessible historical dossier describes an Ubuntu latest-frame pipeline, OpenCV ORB odometry and a non-commanding search advisor. It records 13 offline tests and a later bounded follow-flight report with two reacquisitions. I keep those records distinct from current reproduction: they do not prove obstacle avoidance, complete identity repair or navigation-grade SLAM. The next defensible step would be controlled recorded-video replay before further flight.

### 2-minute version

**Problem:** Target perception and loss handling can fail in ways that matter for motion safety; an experimental vision pipeline must not be treated as complete navigation.

**Decision:** Keep passive visual advice distinct from drone-command authority and describe evidence at the level of individual experiments.

**Implementation:** The historical public dossier reports inspected E012 code with a single frame receiver/decoder, a latest-only shared-frame bus, OpenCV ORB monocular visual odometry and a non-commanding search advisor. It separately describes a later depth-scheduled following experiment.

**Trade-off:** This final audit had the public historical dossiers, not a fresh replay of all original source and hardware. I can explain what those records establish while retaining their partial status and provenance caveats.

**Validation:** The dated review records 13 offline concurrency, storage and target-loss tests. The saved flight report records acknowledged takeoff/landing, about 4.74 FPS and two confirmed reacquisitions. Those figures describe one historical record, not current general reliability. The reported navigation map was not available; passive integration was partial.

**Result:** The evidence supports a supervised perception/following research prototype. It does not support navigation-grade SLAM, complete identity repair, safe confined-space autonomy, validated obstacle classification or multi-drone operation.

**What I would improve next:** Use recorded video, controlled delay/loss injection, predeclared metrics and safety review before new flight. I would preserve negative results and avoid substituting synthetic navigation performance for real hardware evidence.

[Evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/case-studies/air-marshal.md)

## Quantitative Intelligence

### 30-second version

The research question was whether market-regime analysis could be evaluated without misleading temporal or performance claims. Historical HMM records describe train-only transforms and prefix inference; Finance Lab records candidate rejection and an untouched holdout. The important decision was to report negative results and a failed source-only rebuild rather than imply a tradable strategy. Point-in-time and broader walk-forward reproducibility remain incomplete. I would reconstruct licensed frozen inputs and lineage before making any stronger result claim.

### 2-minute version

**Problem:** Financial research is vulnerable to leakage, revised inputs and selecting attractive results after many trials.

**Decision:** Explain the research specification, temporal boundaries, baseline and rejection rules before discussing performance, and retain negative evidence.

**Implementation:** The historical HMM dossier reports 857 weekly observations with train-only preprocessing and prefix-only inference. Finance Lab records experiment/rejection registries, Monte Carlo diagnostics, multiple-testing controls and cost assumptions. Later research-continuous data was kept conceptually separate from frozen dissertation results.

**Trade-off:** These are dated research records, not a newly reproduced licensed dataset and complete executable pipeline in this public repository. Train-only fitting is a useful control but does not establish all point-in-time data availability or every downstream split.

**Validation:** Historical reconciliation reports clean replays, but the source-input-only rebuild report reviewed elsewhere was INVALID because required raw inputs and regeneration code were absent. The candidate matrix records no pre-holdout eligible candidate and an untouched holdout. The available evidence does not establish a fully reproducible walk-forward pipeline or HMM outperformance against gold buy-and-hold.

**Result:** The defensible outcome is research governance: explicit rejected hypotheses, preserved holdout boundaries and acknowledged provenance gaps. No returns, approved live portfolio or autonomous execution are claimed.

**What I would improve next:** Reconstruct permitted frozen inputs, availability timestamps and transformation lineage; predeclare rolling splits and baselines; regenerate report hashes and report failures as well as successes. I would only strengthen claims after that evidence exists.

[Evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/case-studies/quantitative-intelligence.md)

## Cloud / Multi-Cloud Platform

### 30-second version

I built a verifiable release path for the portfolio on an existing small Lightsail host. GitHub CI gates a restricted, host-key-pinned deployment; the candidate starts in the inactive Docker slot and passes health/SHA checks before Caddy switches traffic. A measured deployment had zero observed interruption across 30 external samples, and an unhealthy candidate stayed isolated. Terraform validates Azure/GCP equivalents without deploying them. The trade-off is a single host and HTTP-only public content, not an enterprise availability claim.

### 2-minute version

**Problem:** The portfolio needed credible delivery and recovery evidence without paying for extra cloud hosts or disrupting management access.

**Decision:** Reuse the existing small Lightsail host, preserve security boundaries and make release eligibility explicit before traffic changes.

**Implementation:** GitHub Actions waits for CI on the exact main SHA. Restricted SSH commands, pinned host identity and GitHub secrets authorize a root-owned receiver. It prepares the inactive Docker slot, checks health, SHA and content, then atomically switches Caddy. The previous healthy slot remains available. Terraform models cloud equivalents through reusable modules, with provider locks and credential-free schema/mocked-plan CI.

**Trade-off:** A single host remains a single failure domain. HTTP is for public content only. Azure and GCP are not deployed; the GCP public IP is a visible accepted HIGH reference-design finding, not a false positive.

**Validation:** A successful blue/green run recorded 30 external samples and zero observed interruption. A deliberately unhealthy candidate never became the observed public slot. A live immediate rollback drill took 0.579 seconds. Earlier automatic rollback restored the exact prior SHA but had interruption; current blue/green external-outage injection was not performed. These are different pieces of evidence.

**Result:** The running AWS platform and public IaC/CI artifacts demonstrate bounded, reviewable delivery with explicit cost and security decisions. No new recurring cloud infrastructure was created.

**What I would improve next:** Separately authorize HTTPS/production readiness, alert delivery and failure-domain recovery if the workload justifies them, rather than adding infrastructure merely for presentation.

[Evidence](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/case-studies/aws-cloud-architecture.md)

## Focused questions

**Why Lightsail rather than EC2/EKS?** The existing small host met the public-content/control-plane need. A more complex stack would add operational and recurring-cost obligations without evidence that the workload needed them. This is a fit-for-scope choice, not a claim Lightsail is always better.

**Why blue/green?** Replacement releases caused measured interruption. Preparing and validating an inactive slot keeps active traffic separate from candidate startup and retains an immediate rollback target, at the cost of temporary dual-slot resources.

**How did you secure deployments?** Exact-SHA CI, dedicated restricted commands, strict host-key pinning, secrets outside source, serialized deployment and no public Docker/backend API. Those controls reduce the deployment attack surface; they are not a comprehensive security audit.

**How did you test rollback?** An earlier deliberately invalid page caused automatic restoration of the exact prior SHA and a failed workflow. Later blue/green validation proved pre-switch isolation and a live immediate rollback drill. The current post-switch failure path also has unit coverage; no actual external outage was injected.

**Why keep heavy compute local?** The cloud host has two GiB RAM and serves lightweight application/control functions. Sustained ML, computer vision and research need different capacity. Keeping them on existing local equipment avoids idle cloud capacity, not all electricity/hardware cost.

**How do AWS/Azure/GCP designs differ?** Lightsail packages host/network constructs; Azure uses resource groups, VNet/subnet, NSG, NIC and VM; GCP uses projects, custom VPC/firewall, Compute Engine and OS Login. Containers and operational contracts are portable; IAM, IP pricing, images and API behavior differ. Only AWS has live evidence here.

**How did you prevent research leakage/lookahead?** Historical HMM records describe train-only fitting and prefix-only inference. I would not generalize that to every dataset: availability timestamps, revisions, source-only reproducibility and full walk-forward evaluation have gaps. Those gaps are explicitly reported rather than represented as solved.

**What is production-ready versus prototype?** The public-content AWS platform is operating with tested release controls, but remains single-host and HTTP-only. AIVouch is privately validated and not a production launch. Azure/GCP are undeployed references. AI OS orchestration, robotics and quantitative research retain their stated evidence limits. “Production-style controls” is not the same as broad production certification.
