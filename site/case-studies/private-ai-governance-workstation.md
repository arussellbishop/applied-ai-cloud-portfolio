# Project 2: Private AI Governance and Assurance Workstation

**Status: IMPLEMENTED LOCAL PROTOTYPE / READY FOR CONTROLLED SYNTHETIC EVALUATION**

## Purpose

A portable, local-first AI governance and assurance workstation for offline research, evidence management, RAG evaluation and professional assessment preparation.

The design keeps the working corpus, models and evidence local. Public portfolio material contains only sanitised descriptions, synthetic examples and reproducible design information.

## Architecture

The workstation is built around a bootable removable Linux installation with:

- local Ollama inference;
- CPU fallback for portability;
- a local embedding model;
- SQLite and FTS5 lexical retrieval;
- dense embedding retrieval and hybrid ranking;
- source/version metadata;
- governance entities for risks, obligations, controls, evidence, tests and findings;
- professional assurance and client-evidence schemas;
- explicit human review and abstention when evidence is insufficient.

The current test device is a 64 GB removable USB. The larger original device failed during sustained writes and was not used for the final build.

## Corpus and retrieval baseline

The controlled corpus currently contains 11 source records and 305 indexed chunks with 305 local embeddings. Sources cover UK government AI guidance, ICO AI/data-protection material, UK legislation metadata, NIST, NCSC, OWASP, education guidance and EU AI material.

The system distinguishes:

- law and regulation;
- regulatory guidance;
- government guidance;
- voluntary frameworks and standards;
- internal policy;
- analyst recommendations.

This distinction is essential: guidance and frameworks must not be presented as legislation, and analyst recommendations must not be presented as authority.

## Evaluation evidence

The original lexical RAG produced unsupported or poorly classified answers on broad questions. A hybrid FTS5 plus embedding pipeline was therefore added. It uses validated source identifiers and fails closed when structured model output is invalid.

The hybrid pipeline has successfully returned exact source identifiers for retrieved passages and has demonstrated improved retrieval on prompt-injection questions. Remaining evaluation work includes deterministic authority classification, stronger claim-entailment checks, citation completeness, temporal correctness and a larger regression suite.

## Governance controls demonstrated

- local-only inference by default;
- external LLM and embedding calls disabled by design;
- source manifests and hashes;
- current/superseded/under-review source status;
- hybrid retrieval rather than embeddings alone;
- exact retrieved-source identifiers;
- explicit gaps and confidence fields;
- prompt-injection treatment of retrieved documents as untrusted data;
- human approval as the final authority;
- structured risk, control, evidence and assurance records;
- client-evidence storage separated from public portfolio material.

## Current limitations

- Encryption is a mandatory remaining gate before real client data is added.
- No real client data is included or claimed.
- The USB has not yet passed the cross-computer boot and offline acceptance test.
- The current corpus is a controlled baseline, not a complete legal library.
- The local model can still produce invalid or over-broad classifications; retrieval validation reduces but does not eliminate this risk.
- This is not a certification, legal advice service or substitute for qualified human review.

## Professional-use boundary

The workstation is suitable for controlled research, synthetic assessments, evidence preparation and examination/portfolio demonstration after the stated tests pass. Client deployment requires encryption, access control, retention rules, documented engagement scope, source-freshness checks and human sign-off.

## Evidence model

The private system records the relationship:

```text
AI SYSTEM -> RISK -> OBLIGATION -> CONTROL -> EVIDENCE -> TEST -> FINDING -> RECOMMENDATION
```

This public case study intentionally excludes private databases, raw source files, model weights, licensed standards and client material.
