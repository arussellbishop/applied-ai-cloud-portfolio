# ISO/IEC 42001 AI Management System & AI Assurance Demonstrator

**Status: SYNTHETIC, REPRODUCIBLE PORTFOLIO DEMONSTRATOR**

This project demonstrates practical AI management-system implementation, assurance and audit work for a fictional UK education-technology organisation, **EduAssist AI Ltd**.

It is not an ISO certificate, accredited audit, legal opinion or real client engagement. It contains no real personal data, no licensed ISO text and no production service. Exact normative references must be verified against legitimately accessed standards and are marked `VERIFY_AGAINST_LICENSED_STANDARD` where required.

## Navigate the evidence

- [Portfolio guide](PORTFOLIO_GUIDE.md)
- [Synthetic data notice](DATA_SYNTHETIC_NOTICE.md)
- [AIMS scope](aims/aims-scope.md)
- [AI system inventory](ai-inventory/ai-system-inventory.csv)
- [AI governance charter](governance/ai-governance-charter.md)
- [Risk register](risk/ai-risk-register.csv)
- [Impact assessment](impact-assessment/student-intervention-impact-assessment.md)
- [Technical assurance](technical-assurance/README.md)
- [Legal register](legal/legal-obligations-register.csv)
- [Internal audit](audit/internal-audit-report.md)
- [Corrective action](corrective-actions/CAPA-001.md)
- [Management review](management-review/management-review-pack.md)
- [Certification readiness](certification-readiness/readiness-assessment.md)
- [Evidence graph](evidence/evidence-register.csv)
- [Standards register](references/standards-status-register.md)
- [Free online reference library](references/free-reference-library.md)
- [Licensed-standard verification register](references/licensed-standard-verification-register.csv)
- [Internal audit report (HTML)](audit/internal-audit-report.html)
- [Evaluation suite](07_EVALUATION/iso42001-evaluation-suite.jsonl)
- [Private RAG UK personal-data case study](case-studies/private-rag-uk-personal-data.md)
- [Recruiter brief](../../recruiter/ISO42001_RECRUITER_BRIEF.md)

## Management-system story

Context and scope → leadership and policy → planning and risk → support and competence → operation and lifecycle → technical assurance → performance evaluation → internal audit → management review → corrective action and continual improvement.

## Reproduce

```bash
python3 -m pip install -r requirements.txt
python3 src/data_generation/generate_synthetic_data.py
python3 src/models/train_and_evaluate.py
python3 src/evaluation/generate_evaluation_suite.py
python3 scripts/check_aims_portfolio.py
pytest -q
```

The committed reports are generated from deterministic synthetic data. Re-running the commands should produce equivalent metrics within the documented tolerance.

## Evidence chain

`AI system -> impact assessment -> risk -> control -> technical test -> audit finding -> corrective action -> retest -> management review` is represented in the evidence register and supporting artifacts. The synthetic drift scenario is deliberately imperfect so the repository demonstrates assurance and improvement, not a fictional flawless deployment.
