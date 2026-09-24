# CloudShell bootstrap review

Scope: establish a zero-recurring-cost GitHub OIDC control plane only. No Lambda, queue, VM, network, storage, Bedrock inference or production change occurs here. Execute from a non-root Console identity already authorized for IAM; never provide access keys.

## Exact managed resources

- GitHub OIDC provider only if absent. Existing shared provider is reused without alteration and is not put under capstone ownership.
- `ai-capstone-github` role, one-hour maximum session, exact repository `arussellbishop/applied-ai-cloud-portfolio`, exact main ref, audience `sts.amazonaws.com`.
- One inline deployment policy on that role.
- `ai-capstone-runtime-boundary` managed IAM policy. This is an essential bootstrap boundary, not a grant to a running service.

No AdministratorAccess, PowerUserAccess, managed Bedrock full-access policy, IAM user, access key or root use. No change to existing deployment credentials, environments or branch protections.

## Bootstrap versus normal permissions

The human bootstrap identity needs read/create/update for these exact named IAM resources plus optional provider creation and policy tagging; a pre-existing resource collision is not imported or overwritten automatically. Terraform creation fails on a name collision. Reruns with the private state are idempotent; losing state requires recovery/import after review, never deletion/recreation by guesswork.

The deployment role can manage only one named Lambda, two named queues, one log group and one alarm in eu-north-1. It can create only `ai-capstone-runtime` with the pre-existing boundary attached, edit its inline permission policy, pass it only to Lambda, and delete it during cleanup. It cannot edit its own permissions/trust, change the boundary, attach managed policies, create users/keys, remove the runtime boundary, or create the prohibited services. The runtime trust policy will be Lambda-only in platform Terraform. The model runtime policy must narrow to the actual selected model and profile before evidence capture.

Runtime boundary maximum: only Nova Micro v1 or Nova Lite v1 model ARNs in eu-north-1, eu-west-1, eu-west-3 and eu-central-1, plus their exact EU inference profiles from eu-north-1; writes to the single Lambda log stream namespace and consumption of the request queue. This is a candidate allowlist, NOT a claim of model availability. Query actual account availability and profile destinations before selection. No global/US profile, customization or provisioned throughput. Ordinary deployment cannot invoke Bedrock directly; it invokes the bounded Lambda.

## Wildcard review

No action wildcard is granted. `Resource: *` is used only for list/discovery APIs without resource-level authorization (Bedrock lists, Lambda mapping list, Logs group list), CloudWatch GetMetricStatistics, and Lambda CreateEventSourceMapping. Mapping creation/change is constrained by `lambda:FunctionArn` to the exact function. Mapping UUID permissions use the region/account mapping ARN namespace because identifiers are generated and also require the exact function ARN. Mapping list is an account-level metadata read. Event-source mappings must use an untagged provider alias: this role intentionally has no permission to tag arbitrary mapping UUIDs; other resources carry standard project tags. Log stream suffix is dynamic under the exact group. No wildcard model identifiers or repository/ref trust.

Terraform provider reads can require further documented API permissions; do not solve an AccessDenied with broad managed policies. Use AWS service authorization reference and narrow amendments if necessary. Platform plan must reject additional named resources and enforce resource count, timeout, memory and concurrency caps; IAM alone is not a dollar ceiling.

## State, delivery and review

`BOOTSTRAP.sh` downloads Terraform 1.14.7 from HashiCorp HTTPS and verifies the release SHA-256 from the same official origin. Provider version is exact and dependency hashes are checked using the committed lockfile. Script prints only resource names and change types, retains full plans/state privately in CloudShell home, refuses replacements/deletions and applies only four reviewed IAM resource addresses. Inspect `main.tf.json`, both scripts and inventory.py before execution. CloudShell output/state must not be pasted into chat or committed.

`VERIFY.sh` checks zero drift, exact trust, inline policy inventory and absence of managed policy attachments. It then runs read-only service inventory across enabled regions with sanitized counts. Unknown/denied API results remain UNKNOWN; no inventory deletes anything. This inventory is intentionally bounded and not an exhaustive bill audit.

Main protection remains enabled. The trusted workflow must land through existing repository controls; no automatic admin bypass is authorized. GitHub `AWS_ROLE_ARN` may be an Actions variable (not an access key), set through the GitHub web UI during this same checkpoint. Account identifiers must stay out of published logs; AWS credentials action should mask the account ID. No second AWS authentication checkpoint is intended.

## Verification limits

Local syntax/schema validation can prove configuration shape, not AWS authorization or account availability. CloudShell apply/verify and a later actual OIDC job are required. Bootstrap success does not prove inference or the full capstone. No deployment/cleanup success is claimed in Phase 19A.

## Primary references

- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html
- https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/
