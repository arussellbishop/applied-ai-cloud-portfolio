# OIDC trust recovery — 2026-09-25

GitHub reports immutable subjects enabled for this repository. The capstone role now matches the exact owner/repository IDs and main ref, retaining the STS audience and existing permissions. Before/after trust documents are retained privately on the operator host. No Terraform apply or application-resource change was performed.

Run 36131621754 attempt 2 successfully obtained AWS credentials through OIDC, then failed the workflow's literal wildcard identity comparison. This repair checks the exact expected assumed-role ARN and session, masks the account ID, and fixes SHA summary formatting. Bootstrap Terraform and its assertions now match live trust. Existing CloudShell bootstrap copies must be updated from this source before planning again; zero Terraform drift has not been revalidated.

A successful end-to-end workflow rerun remains pending merge through existing repository controls. No administrator bypass is authorized.

Reference: https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims
