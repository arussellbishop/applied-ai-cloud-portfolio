# Architecture evidence gallery

Seven required views, with implementation and evidence boundaries shown explicitly. All source diagrams and embedded Mermaid blocks are syntax-checked in CI; parsing is not a substitute for architecture review.

## Portfolio platform

Implemented single-host AWS platform; existing private backend bridge permits egress.

```mermaid
flowchart LR
    GH[GitHub main] --> CI[Exact-SHA CI gate]
    CI --> SSH[Restricted deployment SSH]
    SECRETS[GitHub secrets boundary] -.-> SSH
    SSH --> RECEIVER[Root-owned command receiver]
    subgraph HOST[Existing Lightsail - 2 vCPU / 2 GiB]
        RECEIVER --> CANDIDATE[Inactive Docker slot]
        CANDIDATE --> CHECK[Health and SHA validation]
        CHECK --> SWITCH[Atomic Caddy upstream switch]
        SWITCH --> CADDY[Caddy HTTP ingress]
        CADDY --> ACTIVE[Active private Docker slot]
        PREVIOUS[Previous healthy slot] -. rollback .-> SWITCH
        ACTIVE --> HEALTH[Health and external validation]
        HEALTH -. failure .-> PREVIOUS
    end
    INTERNET[Public portfolio visitors] --> IPV4[Existing static IPv4]
    IPV4 --> CADDY
    HEALTH --> SUMMARY[GitHub deployment summary]
```

[Diagram source](../multicloud/current-aws.mmd)

## CI/CD and blue/green deployment

Implemented control flow. Live pre-switch isolation and immediate rollback are proven; current post-switch external-outage injection is not claimed.

```mermaid
flowchart TD
    PR[Reviewed PR] --> MAIN[GitHub main SHA]
    MAIN --> CI[Required CI including Terraform and publication checks]
    CI --> AUTH[Restricted SSH credential and pinned host identity]
    AUTH --> LOCK[Workflow concurrency and host lock]
    LOCK --> INACTIVE[Prepare inactive Docker slot]
    INACTIVE --> VERIFY{Health SHA and content pass?}
    VERIFY -- No --> KEEP[Fail run - active traffic unchanged]
    VERIFY -- Yes --> SWITCH[Atomic Caddy upstream switch]
    SWITCH --> EXTERNAL{External HTTP validation passes?}
    EXTERNAL -- Yes --> RETAIN[Success - retain previous healthy slot]
    EXTERNAL -- No --> RESTORE[Restore previous healthy slot]
    RESTORE --> FAIL[Verify restored health - fail run]
```

[Diagram source](cicd-bluegreen.mmd)

## AIVouch validation

Completed private demo validation; disposable resources have been removed. No live external integration is implied.

```mermaid
flowchart LR
    FROZEN[Private frozen prototype] --> COPY[Isolated validation branch]
    COPY --> TEST[Clean tests and dependency audits]
    TEST --> IMAGE[Hardened bounded container]
    subgraph PRIVATE[Temporary internal Docker network on existing AWS host]
        IMAGE --> API[FastAPI - synthetic requests]
        API --> DB[Disposable SQLite data]
        API --> DEMO[Demo engines only]
        API --> CONTROLS[Health restart and kernel-control checks]
    end
    CONTROLS --> EVIDENCE[Sanitized evidence and resource measurements]
    EVIDENCE --> CLEANUP[Remove containers network credentials and test data]
    PORTFOLIO[Existing public portfolio - untouched by this validation]
    LIMIT[No public AIVouch route or live provider validation]
```

[Diagram source](aivouch-validation.mmd)

## AI Operating System

Working remote model plus clearly separated historical orchestration records. General retries/recovery remain unproven.

```mermaid
flowchart LR
    OP[Operator intent and scope] --> MOBILE[Android and Termux]
    MOBILE --> ACCESS[Private access and SSH]
    ACCESS --> SESSION[Persistent tmux workspace]
    SESSION --> TOOLS[Codex tools and Git]
    TOOLS --> REVIEW[Evidence tests and explicit approval]
    REVIEW --> PUBLICATION[CI-gated publication]
    subgraph HISTORICAL[Historical local records - partially proven]
        DASH[Local dashboard] --> CYCLE[Central cycle and listed timers]
        CYCLE --> RECORDS[Project and source-health records]
        BACKUP[Recorded sample backup restore]
    end
    TOOLS -. separate historical system .-> DASH
    GAP[Retry and full recovery guarantees not established]
```

[Diagram source](ai-operating-system.mmd)

## Air Marshal

Historical prototype and experiment architecture, not newly reproduced flight or completed navigation. E012 and E013 are distinct evidence scopes.

```mermaid
flowchart LR
    subgraph E012[Historical E012 inspected implementation and offline tests]
        TELLO[Tello video and telemetry] --> FRAME[Single receiver and latest-frame bus]
        FRAME --> ORB[OpenCV ORB visual odometry]
        ORB --> ADVICE[Passive search advice - no command interface]
        FRAME --> POLICY[Target-loss policy under offline tests]
        POLICY --> LOG[Bounded timestamped records]
    end
    subgraph E013[Separate historical E013 experiment record]
        FLIGHT[Supervised depth-scheduled following] --> EVENTS[Recorded takeoff landing and reacquisitions]
    end
    UNKNOWN[Not established - metric map or safe autonomous navigation]
```

[Diagram source](air-marshal.mmd)

## Quantitative research

Conceptual synthesis of historical research records, not a currently reproduced end-to-end pipeline. Future work is dashed.

```mermaid
flowchart LR
    subgraph HMM[Historical HMM methodology]
        INPUT[Frozen weekly input record] --> TRAIN[Train-only preprocessing]
        TRAIN --> INFER[Prefix-only inference]
        INFER --> BASELINE[Comparable-window baseline review]
    end
    subgraph LAB[Historical Finance Lab records]
        EXP[Experiment registry] --> TEST[Costs and multiple-testing diagnostics]
        TEST --> REJECT[No eligible candidate - holdout untouched]
        GAP[Source-only rebuild INVALID]
    end
    BASELINE --> REVIEW[Research review with limitations]
    REJECT --> REVIEW
    GAP --> REVIEW
    REVIEW -. future prerequisite .-> FUTURE[Licensed input lineage and reproducible walk-forward replay]
```

[Diagram source](quantitative-research.mmd)

## Multi-cloud Terraform comparison

AWS implemented platform; Terraform AWS ownership remains reference-only. Azure/GCP are validated references, not deployed.

```mermaid
flowchart TB
    CI[Portable CI validation and deployment contract]
    subgraph AWS[AWS - implemented platform / reference IaC]
        AN[Lightsail managed networking] --> AS[Lightsail port policy]
        AS --> AC[Small Lightsail Linux host]
        AI[Static IPv4 / HTTP] --> AS
    end
    subgraph AZURE[Azure - validated reference only]
        ZN[VNet and subnet] --> ZS[NSG HTTP and restricted SSH]
        ZS --> ZC[Burstable Linux VM]
        ZI[Standard public IPv4] --> ZS
    end
    subgraph GCP[GCP - validated reference only]
        GN[Custom VPC and subnet] --> GS[Targeted firewall / OS Login]
        GS --> GC[Small Compute Engine VM]
        GI[Regional external IPv4] --> GS
    end
    CI -. contract .-> AC
    CI -. contract .-> ZC
    CI -. contract .-> GC
    AC --> SHARED[Docker host / Caddy / private slots]
    ZC -. bootstrap not deployed .-> SHARED
    GC -. bootstrap not deployed .-> SHARED
    SHARED --> MONITOR[Health endpoints / host metrics / GitHub summaries]
    LOCAL[Local heavy-compute plane] -. separate workload placement .-> CI
```

[Diagram source](../multicloud/multicloud.mmd)
