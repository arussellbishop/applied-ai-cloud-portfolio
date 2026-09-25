# Capstone cost inventory — Phase 19A

CAPSTONE_COST_LIMIT = USD 5. Target under USD 1. Current incremental deployment usage: none; no AWS capstone resources applied. No exact billing observation claimed.

| Item | Plan / estimate basis | Current status |
|---|---|---|
| Existing Lightsail | USD 12/month user-reported, excluded from incremental capstone | ESTIMATED; billing unverified |
| OIDC provider / IAM role / boundary | No recurring resource charge | PREPARED |
| Bedrock | At most 12 attempts, input capped at 1,024 tokens, output at 128; select available Amazon low-cost model after discovery and pricing check | NOT_STARTED |
| Lambda | One 128–256 MiB function, timeout at most 30 seconds; bounded test workload | NOT_STARTED |
| SQS / DLQ | Two queues, two test messages initially, redrive after two failed receives; no continuous producer | NOT_STARTED |
| CloudWatch logs | One group, one-day retention, no prompt logging | NOT_STARTED |
| CloudWatch alarm | One DLQ alarm during short evidence window, removed same day | NOT_STARTED |
| Dashboard | Reference code by default; deploy only after cost check | NOT_STARTED |
| S3 / EventBridge | Not required; avoid resources for demonstration alone | NOT_PLANNED |
| Kubernetes | Temporary host resource use only if safe; no EKS or new VM | NOT_STARTED |

BILLING_PENDING applies after usage, not to an invented exact bill. Capture usage counters and pricing at model selection; compare delayed billing if available without paid query loops. Stop before any action reasonably capable of exceeding USD 5. Budget alerts are advisory and delayed, not a hard cap. IAM cannot enforce aggregate spend or input/output token limits; code, reviewed workflow, invocation caps and cleanup enforce operational bounds.

## Free budget alert preparation

AWS states that monitoring and budget notifications are free: https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/ . Do not configure paid budget actions, anomaly services or Cost Explorer API polling.

Optional Console-only setup during the same CloudShell checkpoint: Billing → Budgets → create a cost budget named `ai-capstone-5usd`, monthly USD 5; actual USD 1 and USD 4 email alerts to your own address. Filter to Amazon Bedrock, AWS Lambda, Amazon Simple Queue Service and AmazonCloudWatch where available. This intentionally includes unrelated usage in those services: conservative, but not exact capstone attribution. Do not use an unactivated cost-allocation tag as if it guarantees coverage. No email address is written to source. If the account denies access, record BUDGET_ALERT=UNAVAILABLE and proceed with bounded workload controls. No budget actions. Bootstrap itself remains IAM-only.

## Cost decisions and cleanup

Reject EKS, RDS, managed load balancers, NAT gateways, OpenSearch, provisioned Bedrock throughput and SageMaker training. They add cost or operational scope without necessary evidence. No always-on paid resource is authorized.

Normal platform Terraform apply, bounded validation and destroy should run in a single manually dispatched, concurrency-protected OIDC job. Preserve private state for failure recovery; run destroy in a finally/always stage and explicitly verify inventory. Job cancellation can interrupt cleanup, so retain recoverable state and provide a destroy mode. Never upload account-bearing state or plans as public artifacts. No paid state backend needed for one serialized ephemeral exercise.

Intended final NEW_LONG_TERM_RECURRING_CAPSTONE_COST = USD 0; not yet a validated result. OIDC/bootstrap IAM may remain only for future automation; no application resources retained.
