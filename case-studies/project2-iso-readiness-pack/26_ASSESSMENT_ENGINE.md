# Assessment Engine Operating Model

The structured register, not the language model, is the assessment engine.

## Input

1. An exact requirement from the licensed standard or authoritative legal source.
2. The applicability decision.
3. Mapped control IDs.
4. Evidence requests and received artifacts.
5. Test and review results.
6. Human decision and approval.

## Processing

The assessor updates `22_STANDARD_REQUIREMENTS_CROSSWALK.csv` and the SQLite tables. The RAG can locate passages and suggest relevant control IDs, but every mapping is reviewed by a human.

## Output

The system produces an evidence-linked conclusion showing each requirement as open, implemented, effective, nonconforming or not applicable. It lists missing evidence and corrective actions.

## Client lifecycle

Before client evidence exists, the registers contain requirements, controls and evidence requests. When evidence arrives, it is added with an owner, date, integrity information and reviewer. If evidence is missing or inadequate, the status remains open or becomes a finding and a corrective action is created.

## RAG boundary

The RAG must never convert a plausible answer into a compliance decision. It provides retrieval, source classification, gap prompts and draft wording. Human assessors approve applicability, evidence sufficiency, legal interpretation, risk acceptance and final conclusions.
