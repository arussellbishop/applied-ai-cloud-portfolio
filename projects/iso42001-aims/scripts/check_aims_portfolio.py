"""Fail on broken evidence relationships or missing core artifacts."""
from pathlib import Path
import csv, sys
ROOT=Path(__file__).resolve().parents[1]
required=["README.md","DATA_SYNTHETIC_NOTICE.md","aims/aims-scope.md","ai-inventory/ai-system-inventory.csv","risk/ai-risk-register.csv","impact-assessment/student-intervention-impact-assessment.md","audit/internal-audit-report.md","corrective-actions/CAPA-001.md","management-review/management-review-pack.md","certification-readiness/readiness-assessment.md","evidence/evidence-register.csv","07_EVALUATION/iso42001-evaluation-suite.jsonl","case-studies/private-rag-uk-personal-data.md"]
def read_csv(name):
    with (ROOT/name).open(newline="") as f: return list(csv.DictReader(f))
def main():
    errors=[f"missing {f}" for f in required if not (ROOT/f).exists()]
    systems={r["system_id"] for r in read_csv("ai-inventory/ai-system-inventory.csv")}
    risks=read_csv("risk/ai-risk-register.csv")
    for r in risks:
        if r["system_id"] not in systems: errors.append(f"risk {r['risk_id']} references unknown system")
    suite=list((ROOT/"07_EVALUATION/iso42001-evaluation-suite.jsonl").read_text().splitlines()) if (ROOT/"07_EVALUATION/iso42001-evaluation-suite.jsonl").exists() else []
    if len(suite)<50: errors.append(f"evaluation suite has {len(suite)} cases; minimum is 50")
    if errors: print("\n".join(errors)); return 1
    print(f"AIMS portfolio checks PASS ({len(required)} core artifacts, {len(systems)} systems, {len(risks)} risks)")
    return 0
if __name__=="__main__": sys.exit(main())
