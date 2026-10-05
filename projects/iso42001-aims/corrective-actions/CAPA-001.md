# CAPA-001 - drift monitoring

**Finding:** F-001. **Containment:** pause automated prioritisation and require manual review. **Root cause:** monitoring requirements were documented as periodic review without an operational alert specification.

**Corrective action:** add feature-distribution and subgroup-performance thresholds, alert ownership, evidence retention and escalation SLA; rerun technical tests; update the model card and risk treatment.

**Effectiveness test:** execute `src/drift/evaluate_drift.py`, confirm a flagged result, verify alert routing and management sign-off. Closure is only permitted when the evidence register records the result and an independent reviewer confirms effectiveness.
