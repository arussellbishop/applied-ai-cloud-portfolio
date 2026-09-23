# Multi-cloud platform engineering

AWS is implemented; Azure and GCP are validated, undeployed references.

- [Terraform modules and safe validation](PHASE17_TERRAFORM.md)
- [AWS architecture](PHASE17_AWS_ARCHITECTURE.md)
- [Azure architecture](PHASE17_AZURE_ARCHITECTURE.md)
- [GCP architecture](PHASE17_GCP_ARCHITECTURE.md)
- [Security findings and decisions](PHASE17_SECURITY.md)
- [Cost discipline](PHASE17_FINOPS.md)
- [Validation evidence](PHASE17_VALIDATION.md)

## Current AWS platform

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

## Cloud equivalents

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

## Portability

| Portable contract | Cloud-specific implementation |
|---|---|
| Docker workloads and health endpoints | VM images, burst/CPU capacity and runtime bootstrap |
| Blue/green validation, traffic switch and rollback | Network interface, firewall and public-IP constructs |
| Terraform module interfaces and CI logic | Lightsail versus Azure resource groups/VNet versus GCP projects/VPC |
| Least privilege, secret separation, host verification | Cloud IAM, SSH public-key handling and GCP OS Login |
| Host/application monitoring signals | Native metrics, quotas, retention and billing |

Portability means reusable application and operational contracts with tested adapters, not identical cloud behavior. Only the AWS adapter has live deployment evidence.
