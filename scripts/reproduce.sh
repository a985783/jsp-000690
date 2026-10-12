#!/usr/bin/env bash
# Full reproduction and multi-layer verification for the JSP-000690 formalization.
# Requires: elan/lake on PATH, python3, network access for the first run.
#
# Usage:
#   ./scripts/reproduce.sh             # Run full end-to-end clean build and audits
#   ./scripts/reproduce.sh --controls  # Run self-test control suites for all auditors
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ "${1:-}" == "--controls" ]]; then
  echo "=== RUNNING BIDIRECTIONAL AUDIT CONTROL SUITES ==="
  echo
  python3 scripts/scan_placeholders.py --run-controls
  echo
  python3 scripts/audit_axiom.py --run-controls
  echo
  python3 scripts/check_definition_match.py --run-controls
  echo
  python3 scripts/check_statement_match.py --run-controls
  echo
  echo "ALL AUDIT CONTROLS PASSED"
  exit 0
fi

echo "== versions =="
cat lean-toolchain
lake --version

echo
echo "== 1/5 fetch prebuilt Mathlib oleans for the pinned revision =="
lake exe cache get

echo
echo "== 2/5 clean build of package only (preserving shared Mathlib cache) =="
lake clean jsp000690
rm -rf .lake/build/lib/lean/Erdos834* .lake/build/lib/Erdos834* .lake/build/ir/Erdos834*
lake build

echo
echo "== 3/5 comment-stripped placeholder scan (macOS-compatible) =="
python3 scripts/scan_placeholders.py Erdos834.lean

echo
echo "== 4/5 machine verification of transplanted Finset definitions =="
python3 scripts/check_definition_match.py

echo
echo "== 5/5 transitive axiom audit (target-bound, fail-closed) =="
python3 scripts/audit_axiom.py --module Erdos834 --theorem Erdos834.erdos_834.parts.ii

echo
echo "== 5b/5 statement correspondence against pinned challenge file =="
python3 scripts/check_statement_match.py

echo
echo "ALL REPRODUCTION AND VERIFICATION CHECKS PASSED"
