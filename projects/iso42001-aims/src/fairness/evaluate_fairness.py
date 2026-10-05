from pathlib import Path
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

ROOT=Path(__file__).resolve().parents[2]
def main():
    df=pd.read_csv(ROOT/"data/processed/student_intervention_baseline.csv")
    score=(-.4+(70-df.attendance)*.045+(55-df.assessment_performance)*.025+(3-df.engagement)*.5+df.prior_interventions*.28+df.support_need*.55)
    df["pred"]=(1/(1+__import__("numpy").exp(-score))>=.5).astype(int)
    rows=[]
    for field in ["gender_group","age_band"]:
        for group,g in df.groupby(field):
            tn,fp,fn,tp=confusion_matrix(g.outcome,g.pred,labels=[0,1]).ravel()
            rows.append({"attribute":field,"group":group,"n":len(g),"selection_rate":round(g.pred.mean(),4),"tpr":round(tp/(tp+fn),4) if tp+fn else None,"fpr":round(fp/(fp+tn),4) if fp+tn else None})
    out=pd.DataFrame(rows); out.to_csv(ROOT/"technical-assurance/fairness-results.csv",index=False)
    (ROOT/"technical-assurance/fairness-method.md").write_text("""# Fairness assessment\n\nThis synthetic assessment reports selection rate, true-positive rate and false-positive rate by synthetic gender and age groups. Differences are signals for investigation, not automatic proof of unlawful discrimination. A competent reviewer must select context-appropriate metrics, examine causal factors, consult affected stakeholders and decide mitigations.\n\nThe test is intentionally limited: no protected characteristic is used as a model feature, but synthetic group labels are retained for post-hoc testing.\n""")
    print(out.to_string(index=False))
if __name__=="__main__": main()
