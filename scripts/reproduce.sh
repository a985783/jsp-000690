#!/usr/bin/env sh
# Full reproduction for the JSP-000690 formalization.
# Requires: elan/lake on PATH, python3, network access for the first run.
set -eu

cd "$(dirname "$0")/.."

echo "== versions =="
cat lean-toolchain
lake --version

echo
echo "== 1/4 fetch prebuilt Mathlib oleans for the pinned revision =="
lake exe cache get

echo
echo "== 2/4 clean build =="
lake build

echo
echo "== 2b/4 no placeholders in the proof source =="
if grep -nE '\b(sorry|admit|native_decide)\b|\baxiom +[A-Za-z_]|\bopaque +[A-Za-z_]' Erdos834.lean; then
  echo "FAIL: forbidden placeholder found"; exit 1
fi
echo "OK: no sorry / admit / native_decide / axiom / opaque in Erdos834.lean"

echo
echo "== 3/4 transitive axiom audit of the target theorem =="
python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii

echo
echo "== 4/4 statement correspondence against the pinned challenge file =="
python3 scripts/check_statement_match.py

echo
echo "ALL CHECKS PASSED"
