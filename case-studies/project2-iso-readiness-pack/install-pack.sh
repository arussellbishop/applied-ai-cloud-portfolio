#!/usr/bin/env bash
set -euo pipefail

SRC=/home/arb1/project2-iso-readiness-pack
USB=/mnt/ai-gov/data/opt/ai-governance/AI_GOVERNANCE
test -d "$SRC"
test -d "$USB"
install -d -m 0750 "$USB/00_ADMIN/ISO_READINESS_PACK"
install -d -m 0750 "$USB/05_TEMPLATES/ISO_READINESS_PACK"
install -d -m 0750 "$USB/15_DATABASE/ISO_READINESS_PACK"
cp -a "$SRC/." "$USB/00_ADMIN/ISO_READINESS_PACK/"
cp -a "$SRC/." "$USB/05_TEMPLATES/ISO_READINESS_PACK/"
cp -a "$SRC/." "$USB/15_DATABASE/ISO_READINESS_PACK/"
sqlite3 "$USB/15_DATABASE/governance.sqlite" < "$SRC/25_CROSSWALK_IMPORT.sql"
printf '%s\n' 'ISO and AI governance readiness pack installed.'
printf '%s\n' 'Classification: WORKING TEMPLATES / SYNTHETIC FIXTURES / NOT CLIENT DATA'
