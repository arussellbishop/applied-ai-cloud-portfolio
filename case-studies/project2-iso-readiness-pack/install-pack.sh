#!/usr/bin/env bash
set -euo pipefail

SRC="${PROJECT2_PACK_SOURCE:?Set PROJECT2_PACK_SOURCE to the local pack directory}"
USB="${AI_GOVERNANCE_USB_ROOT:?Set AI_GOVERNANCE_USB_ROOT to the mounted project root}"
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
