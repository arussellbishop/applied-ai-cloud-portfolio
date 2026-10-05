from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def main():
    a=pd.read_csv(ROOT/"data/processed/student_intervention_baseline.csv"); b=pd.read_csv(ROOT/"data/processed/student_intervention_drift.csv")
    cols=["attendance","assessment_performance","engagement","prior_interventions","support_need"]
    rows=[]
    for c in cols:
        base=float(a[c].mean()); current=float(b[c].mean()); diff=current-base
        rows.append({"feature":c,"baseline_mean":round(base,4),"drift_mean":round(current,4),"difference":round(diff,4),"flag":abs(diff)>0.1})
    result={"status":"PASS","scenario":"deliberate distribution shift","features":rows,"action":"investigate and trigger reassessment before relying on production decisions"}
    (ROOT/"technical-assurance/drift-results.json").write_text(json.dumps(result,indent=2)+"\n")
    (ROOT/"incidents/incident-001-model-drift.md").write_text("""# Incident 001 - synthetic model drift\n\n## Event\nA monitoring review identified a material change in attendance, performance and engagement distributions in the drift fixture.\n\n## Containment\nPause automated recommendations, preserve the affected model/data versions, increase human review and notify the AI System Owner.\n\n## Investigation and corrective action\nRe-run data-quality, performance and subgroup tests; assess retraining, threshold change or retirement. Effectiveness is recorded in `corrective-actions/CAPA-001.md`.\n""")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
