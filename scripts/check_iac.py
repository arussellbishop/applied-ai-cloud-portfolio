"""Small repository-specific guardrails; complements tfsec, not a general HCL analyzer."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
files = list((ROOT / "terraform").rglob("*.tf"))
assert files, "No Terraform source"
for path in files:
    if ".terraform" in path.parts:
        continue
    text = path.read_text()
    assert not re.search(r'(?m)^\s*(?:provisioner|import|backend)\s*["{]', text), f"Unexpected execution/state boundary: {path}"
    assert not re.search(r'(?m)^\s*resource\s+"(?:tls_private_key|random_password|azurerm_key_vault_secret|google_secret_manager_secret_version)"', text), f"Secret-producing resource: {path}"
    assert not re.search(r'(?m)^\s*(?:admin_password|private_key|access_key|secret_key)\s*=', text), f"Credential material: {path}"
    assert 'remote-exec' not in text and 'local-exec' not in text
for workflow in [ROOT / '.github/workflows/terraform.yml']:
    text = workflow.read_text()
    assert not re.search(r'\bterraform\s+(?:apply|destroy|import|refresh)\b', text)
    assert 'secrets.' not in text and ('id-' + 'token' + ': write') not in text
    assert '-backend=false' in text and '-lockfile=readonly' in text
# Management sources must be explicitly supplied; each module enforces /32 validation.
for name in ('aws_lightsail', 'azure_host', 'gcp_host'):
    text = (ROOT / 'terraform/modules' / name / 'variables.tf').read_text()
    assert 'endswith(cidr, "/32")' in text and 'length(var.ssh_source_cidrs) > 0' in text
print('IaC repository guardrails passed; no apply/import/provisioner or cloud-secret workflow.')
