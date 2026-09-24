#!/usr/bin/env bash
set -euo pipefail
umask 077
STEP=preflight
trap 'printf "BOOTSTRAP_FAILED: %s; details retained privately\n" "$STEP"' ERR
export AWS_PAGER=""
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export AWS_REGION=eu-north-1 AWS_DEFAULT_REGION=eu-north-1
command -v aws >/dev/null
command -v python3 >/dev/null
# Never print caller identity. Refuse root even if the Console permits CloudShell.
CALLER_ARN="$(aws sts get-caller-identity --query Arn --output text)"
[[ "$CALLER_ARN" != *:root ]] || { echo 'BOOTSTRAP_FAILED: use a non-root Console identity'; exit 1; }
ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
OIDC="arn:aws:iam::${ACCOUNT}:oidc-provider/token.actions.githubusercontent.com"
RUN="$HOME/ai-capstone-bootstrap-private"
mkdir -p "$RUN"
chmod 700 "$RUN"
# Keep state and account-bearing plans outside the Git checkout.
cp "$ROOT/terraform/bootstrap/main.tf.json" "$RUN/main.tf.json"
cp "$ROOT/terraform/bootstrap/.terraform.lock.hcl" "$RUN/.terraform.lock.hcl"
if aws iam get-open-id-connect-provider --open-id-connect-provider-arn "$OIDC" > "$RUN/provider.json" 2> "$RUN/provider.err"; then
  python3 - "$RUN/provider.json" <<'CHECK'
import json,sys
p=json.load(open(sys.argv[1]))
assert p['Url'] in ['token.actions.githubusercontent.com','https://token.actions.githubusercontent.com']
assert 'sts.amazonaws.com' in p['ClientIDList'], 'Existing shared provider lacks audience; stop without modifying it'
CHECK
  # A provider created by this same state must remain managed on rerun.
  export TF_VAR_existing_oidc_arn="$OIDC"
else
  grep -q NoSuchEntity "$RUN/provider.err" || { echo 'BOOTSTRAP_FAILED: provider lookup denied; inspect private provider.err'; exit 1; }
  export TF_VAR_existing_oidc_arn=''
fi
TF_VERSION=1.14.7
if [[ ! -x "$RUN/terraform" ]]; then
  [[ "$(uname -m)" == x86_64 ]] || { echo 'BOOTSTRAP_FAILED: use x86_64 CloudShell'; exit 1; }
  curl --fail --silent --show-error --location "https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip" -o "$RUN/terraform.zip"
  curl --fail --silent --show-error --location "https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_SHA256SUMS" -o "$RUN/SHA256SUMS"
  (cd "$RUN"; grep " terraform_${TF_VERSION}_linux_amd64.zip$" SHA256SUMS | sed 's/terraform_[0-9.]*_linux_amd64.zip/terraform.zip/' | sha256sum --check --status)
  python3 - "$RUN" <<'UNZIP'
import sys,zipfile,pathlib
p=pathlib.Path(sys.argv[1])
with zipfile.ZipFile(p/'terraform.zip') as z:(p/'terraform').write_bytes(z.read('terraform'))
(p/'terraform').chmod(0o700)
UNZIP
fi
TF="$RUN/terraform"
"$TF" -chdir="$RUN" version -json | python3 -c 'import sys,json; assert json.load(sys.stdin)["terraform_version"] == "1.14.7"'
if [[ -f "$RUN/terraform.tfstate" ]] && "$TF" -chdir="$RUN" state list | grep -q 'aws_iam_openid_connect_provider.github'; then
  export TF_VAR_existing_oidc_arn=''
fi
# Persist only a non-secret ARN privately so VERIFY can resolve the same configuration.
printf '%s' "$TF_VAR_existing_oidc_arn" > "$RUN/existing-oidc-arn"
STEP=terraform_init
"$TF" -chdir="$RUN" init -input=false -lockfile=readonly > "$RUN/init.txt" 2>&1
"$TF" -chdir="$RUN" validate -no-color > "$RUN/validate.txt" 2>&1
STEP=terraform_plan
"$TF" -chdir="$RUN" plan -input=false -out=bootstrap.plan > "$RUN/plan.txt" 2>&1
"$TF" -chdir="$RUN" show -json bootstrap.plan > "$RUN/plan.json"
python3 - "$RUN/plan.json" <<'GUARD'
import json,sys
p=json.load(open(sys.argv[1]))
allowed={'aws_iam_openid_connect_provider.github[0]','aws_iam_policy.runtime_boundary','aws_iam_role.github','aws_iam_role_policy.deployment'}
for r in p.get('resource_changes',[]):
 if r['mode']=='data':continue
 assert r['address'] in allowed, 'Unexpected bootstrap resource'
 assert 'delete' not in r['change']['actions'], 'Refusing replacement or deletion'
 print(r['address']+': '+','.join(r['change']['actions']))
GUARD
# Running this reviewed script authorizes only the allowlisted IAM-only plan.
STEP=terraform_apply
"$TF" -chdir="$RUN" apply -input=false bootstrap.plan > "$RUN/apply.txt" 2>&1
STEP=verification
bash "$ROOT/cloudshell/VERIFY.sh"
