# Validation-only cloud references

**Do not apply these references or import the live host.** No state ownership of production is intended. Azure/GCP remain undeployed; AWS resources here are also a reference, not the source of truth for the existing running host.

See [architecture and validation guide](../architecture/multicloud/README.md). Modules are cloud-specific compositions plus a shared host contract. Required account/key/source variables have no real values committed. Use backend-disabled init, validate, and the mock-provider plan tests only.

The bootstrap writes a contract, not a completed container platform. Provider locks are committed; cache, state, plans and real tfvars are ignored. All findings remain visible in [security review](security-review.json).
