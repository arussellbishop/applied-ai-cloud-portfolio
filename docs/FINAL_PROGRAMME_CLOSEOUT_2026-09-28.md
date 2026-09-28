# Final portfolio programme close-out — 2026-09-28

## Final status

The public portfolio is served independently through GitHub Pages. The AWS capstone implementation and validation were completed, and recovery verification authorizes the planned runtime retirement as a FinOps decision. Final AWS deletion remains pending successful AWS endpoint execution. Historical failures remain preserved in their original evidence documents; the final 400/400 stability acceptance remains the closing validation result.

## Evidence retained

- GitHub-to-AWS OIDC federation passed without static deployment credentials.
- Exact-SHA CI gating, blue/green isolation, health validation and rollback evidence passed.
- Fresh stability acceptance passed 400/400 requests.
- Terraform validates portable AWS, Azure and GCP architecture; only AWS was implemented and operated.
- The recovery archive, restore report and final AWS metadata are retained privately.

## Public delivery

Canonical portfolio: https://arussellbishop.github.io/applied-ai-cloud-portfolio/  
Repository: https://github.com/arussellbishop/applied-ai-cloud-portfolio

GitHub Pages is the public presentation layer. It does not depend on the former Lightsail host, CloudFront distribution or portfolio S3 site bucket.

## Cost and governance

The portfolio runtime is approved for retirement after recovery verification to target USD 0 persistent portfolio AWS runtime cost. The non-billable GitHub OIDC control-plane material may be retained where useful. Unrelated or genuinely unowned AWS resources are not treated as portfolio deletion targets.
