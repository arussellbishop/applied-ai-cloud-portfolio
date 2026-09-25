# Cloud decommission checklist

**Preparation only. No deletion is authorized by this document.** The intended long-term public portfolio target is GitHub Pages, with GitHub as canonical source/evidence and Google Drive plus Ubuntu as recovery archives.

## Preconditions before any future AWS action

- [ ] Portfolio Pages URL is live and independent of Lightsail.
- [ ] Main branch, repository archive and offline recovery copies are verified.
- [ ] `REBUILD_FROM_ZERO.md` has been tested from a clean clone.
- [ ] Recovery manifest excludes secrets and contains all required private source/archive references.
- [ ] CV/contact links and evidence links have a verified public destination.
- [ ] A final production export and rollback record are retained privately.
- [ ] Cost owner approves deletion timing and confirms no unrelated workload uses the resources.
- [ ] A dated change window and rollback decision are recorded.

## Inventory and dependency review

- [ ] Enumerate AWS resources read-only by region and service.
- [ ] Identify the existing Lightsail instance, static IP, firewall entries, deployment receiver and protected GitHub environment dependencies.
- [ ] Confirm AIVouch remains private and is not part of public Pages migration.
- [ ] Confirm no GitHub workflow still depends on the host before stopping it.
- [ ] Verify no logs, datasets, state or secrets exist only in AWS.
- [ ] Capture final cost/billing evidence without enabling paid monitoring or recurring services.

## Ordered decommission plan

1. Publish and verify GitHub Pages.
2. Freeze source and evidence at a recorded main SHA.
3. Disable future production deployment triggers only through a reviewed PR, if needed.
4. Preserve private recovery material and operator runbooks.
5. Stop traffic only after Pages is independently verified.
6. Remove host-level application and deployment resources through the reviewed owner/runbook.
7. Remove the existing Lightsail instance and static IP only after confirming no dependency.
8. Remove unused IAM/OIDC resources only after confirming no other repository or workload trusts them.
9. Re-run read-only inventory and cost checks.
10. Record deletion evidence and expected recurring cost of USD 0.

## Azure and GCP boundary

No Azure or GCP recurring portfolio infrastructure is present in this repository's validated scope. Their reference Terraform must remain undeployed unless separately authorized and cost-reviewed.
