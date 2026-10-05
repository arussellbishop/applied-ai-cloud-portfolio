from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def main():
    df=pd.read_csv(ROOT/"data/processed/student_intervention_baseline.csv")
    checks={"rows":len(df),"duplicate_student_ids":int(df.student_id.duplicated().sum()),"missing_cells":int(df.isna().sum().sum()),"attendance_out_of_range":int(((df.attendance<0)|(df.attendance>100)).sum()),"outcome_invalid":int((~df.outcome.isin([0,1])).sum())}
    checks["status"]="PASS" if not any(checks[k] for k in ["duplicate_student_ids","missing_cells","attendance_out_of_range","outcome_invalid"]) else "FAIL"
    (ROOT/"technical-assurance/data-quality-results.json").write_text(json.dumps(checks,indent=2)+"\n")
    (ROOT/"data-governance/data-quality-method.md").write_text("""# Data-quality method\n\nThe demonstrator checks completeness, uniqueness, range validity and label validity before evaluation. Production use would add provenance, lawful basis, retention, access, lineage, representativeness and data-subject correction controls. A failed check blocks promotion until disposition is approved and evidenced.\n""")
    print(json.dumps(checks,indent=2))
if __name__=="__main__": main()
