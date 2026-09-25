#!/usr/bin/env bash
set -euo pipefail
umask 077
export AWS_PAGER="" AWS_REGION=eu-north-1 AWS_DEFAULT_REGION=eu-north-1
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="$HOME/ai-capstone-bootstrap-private"
export TF_VAR_existing_oidc_arn="$(cat "$RUN/existing-oidc-arn")"
"$RUN/terraform" -chdir="$RUN" plan -input=false -detailed-exitcode > "$RUN/verify-plan.txt" 2>&1 || { echo 'BOOTSTRAP_VERIFY_FAILED: drift or denied read; inspect private verify-plan.txt'; exit 1; }
aws iam get-role --role-name ai-capstone-github > "$RUN/role.json"
aws iam list-attached-role-policies --role-name ai-capstone-github > "$RUN/attached.json"
aws iam list-role-policies --role-name ai-capstone-github > "$RUN/inline.json"
python3 - "$RUN" <<'VERIFY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]);r=json.loads((p/'role.json').read_text())['Role']
s=r['AssumeRolePolicyDocument']['Statement']
assert len(s)==1
assert s[0]['Effect']=='Allow'
expected=r['Arn'].rsplit(':role/',1)[0]+':oidc-provider/token.actions.githubusercontent.com'
assert s[0]['Principal']=={'Federated':expected}
assert s[0]['Action']=='sts:AssumeRoleWithWebIdentity'
assert s[0]['Condition']=={'StringEquals':{'token.actions.githubusercontent.com:aud':'sts.amazonaws.com','token.actions.githubusercontent.com:sub':'repo:arussellbishop@160221505/applied-ai-cloud-portfolio@1383937218:ref:refs/heads/main'}}
assert not json.loads((p/'attached.json').read_text())['AttachedPolicies']
assert json.loads((p/'inline.json').read_text())['PolicyNames']==['ai-capstone-deployment']
print('BOOTSTRAP_SUCCESS: main-only OIDC trust; scoped policy; no managed policy attachments; Terraform drift zero')
VERIFY
python3 "$ROOT/cloudshell/inventory.py"
printf '%s\n' 'CLOUDSHELL_SUMMARY: BOOTSTRAP=PASS; OIDC_LIVE=NOT_YET_TESTED; INVENTORY=COUNTS_ONLY; CAPSTONE_APPLICATION_RESOURCES=NOT_CREATED'
printf '%s\n' 'Do not return private plans, state, account IDs, addresses, or credentials.'
