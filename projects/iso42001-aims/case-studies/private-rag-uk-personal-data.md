# Case Study 2: Private RAG handling UK personal data

**Status: synthetic assurance case study; no client or real personal data.**

## Scenario

A fictional organisation operates a locally hosted retrieval-augmented generation system over approved UK governance and internal policy documents. It processes synthetic personal-data examples and produces evidence-linked research answers for authorised staff. External LLM calls, cloud embeddings and document uploads are disabled by default.

## Assessment scope

The assessment covers UK GDPR/DPA context, ICO regulatory guidance, UK Government guidance, voluntary frameworks, internal policy, prompt injection, retrieval leakage, access control, data minimisation, source currency, human review, logging, retention, supplier risk and incident response.

## Key risks and controls

| Risk | Control | Evidence |
|---|---|---|
| Indirect prompt injection | Retrieved content is untrusted data; instruction-following is constrained and tested | `security/prompt-injection-test.md` |
| Retrieval leakage | User-authorised retrieval, least privilege and private index separation | `privacy/data-flow.md` |
| Unsupported legal claim | Authority classification, source status, citation validation and abstention | `legal/legal-obligations-register.csv` |
| Stale guidance | Version register, retrieval date and deliberate source verification | `references/version-register.csv` |
| Automation bias | Human review and no autonomous consequential decision | `governance/human-oversight-policy.md` |
| Model or corpus change | Change approval, regression tests and rollback | `governance/model-change-procedure.md` |

## Evidence decision

The system is suitable for controlled synthetic research and portfolio demonstration. It is **not approved for real client or special-category personal data** until encryption, access control, retention, DPIA, incident arrangements, source verification and independent human approval are completed for the actual organisation.

## Professional relevance

This case demonstrates the distinction between law, regulatory guidance, government guidance, voluntary frameworks, internal policy and analyst recommendations. It also demonstrates how a technical RAG risk becomes an auditable governance control with evidence and a test.
