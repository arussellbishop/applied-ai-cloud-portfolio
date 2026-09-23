# AWS and cloud architecture

## Control-host model

A small existing Lightsail host provides a low-cost control and development surface for documentation, Git, lightweight services, and portfolio work. The design preserves SSH and private-network access, uses Docker security controls, and keeps public exposure behind one reverse proxy.

## Delivery model

Releases are versioned, the active release is switchable, health checks run before promotion, and rollback preserves the previous release. Public HTTP activation was performed separately from private validation; HTTPS remains a separate domain and DNS decision.

## Cost boundary

No new AWS resources, managed databases, load balancers, Kubernetes clusters, snapshots, or paid monitoring were introduced for this work. Account-wide billing is not claimed as verified.
