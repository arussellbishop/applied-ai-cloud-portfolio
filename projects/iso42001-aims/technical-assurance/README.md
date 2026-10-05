# Technical AI assurance

The flagship system is evaluated locally with reproducible synthetic data. Performance, data quality, fairness and drift outputs are evidence inputs to the risk register, impact assessment, audit and management review. These tests demonstrate method and traceability; they are not evidence that a real deployment is safe.

Run from this directory's project root:

```bash
python src/data_generation/generate_synthetic_data.py
python src/models/train_and_evaluate.py
python src/fairness/evaluate_fairness.py
python src/drift/evaluate_drift.py
python src/data_quality/check_data_quality.py
```
