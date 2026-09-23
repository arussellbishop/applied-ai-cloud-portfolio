# Air Marshal — perception and supervised robotics research

**Status: PARTIALLY_PROVEN historical implementation/experiment evidence. No new flight or source replay was performed in this audit.**

## Problem and implemented prototype

Explore target perception and loss handling on a small drone without treating an experimental vision pipeline as a certified navigation system. The [existing public dossier](https://github.com/arussellbishop/ai-ml-aws-portfolio/blob/a2f1e34b1b06650640d895c36d993b973b41c169/site/robotics.html) reports inspected E012 code with one frame receiver/decoder, a latest-only shared-frame bus, OpenCV ORB monocular visual odometry and a non-commanding search advisor. The odometry module has no drone-command interface. The recorded offline review passed 13 concurrency, bounded-storage and target-loss-policy tests.

A historical E013 depth-scheduled following report records acknowledged takeoff/landing, 4.74 FPS effective tracking/control and two confirmed reacquisitions. These are saved experiment results, not newly reproduced measurements or a general reliability rate. The report retains an earlier run-ID prefix, so provenance is described explicitly instead of silently relabeling it.

## Architecture and safety boundary

Tello video/telemetry → Ubuntu latest-frame bus → perception/experimental odometry → supervised follow/loss policy → timestamped records. Passive advice is separated from motion authority. [Diagram](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/architecture/diagrams/README.md#air-marshal)

## What is not established

Navigation-grade SLAM, a metric obstacle map, safe autonomous confined-space navigation and multi-drone operation are not proven. Historical passive SLAM/reacquisition integration was marked partial. Identity repair, every seek/find/lock/follow transition and obstacle/depth classification accuracy are not independently supported by the accessible evidence; depth-scheduled following is not validated obstacle avoidance. Home-lab/live-drone records must not be described as a completed confined-environment navigation system. A separate synthetic sensor-fusion demonstration is not flight evidence.

A defensible next experiment would use recorded video and injected message delay/loss with predeclared metrics before authorizing more live hardware work. No new experiment, RF interference or flight was performed here.

[Historical provenance](https://github.com/arussellbishop/applied-ai-cloud-portfolio/blob/main/evidence/final/historical-projects.md) · [All projects](https://github.com/arussellbishop/applied-ai-cloud-portfolio#flagship-projects)
