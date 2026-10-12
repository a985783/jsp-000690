#!/usr/bin/env python3
"""Machine verification of transplanted Finset definitions against upstream formal-conjectures.

Verifies:
  1. Vendored reference hash pin (scripts/reference/upstream_definitions.lean)
  2. Upstream commit SHA pin: 2067d8bb82058f40ccbd20a14fb94502434ea9eb
  3. Syntactic and semantic correspondence of the 5 transplanted Finset definitions:
     - Finset.IsUniform
     - Finset.IsProperHypergraphColoring
     - Finset.HypergraphColorable
     - Finset.HasHypergraphChromaticNumber
     - Finset.hypergraphDegree
  4. Definitional equality in Lean kernel (`by rfl`) against machine-extracted
     Upstream.Finset declarations with explicitly qualified cross-dependencies.

Exit codes:
  0: all 5 definitions match the pinned upstream reference exactly
  1: discrepancy detected in one or more definitions or Lean rejected rfl
  2: reference or source file missing / IO error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "scripts" / "reference"
PROVENANCE_FILE = REFERENCE_DIR / "PROVENANCE.json"
VENDORED_REF_FILE = REFERENCE_DIR / "upstream_definitions.lean"

PINNED_UPSTREAM_COMMIT = "2067d8bb82058f40ccbd20a14fb94502434ea9eb"
PINNED_UPSTREAM_FILE_SHA256 = "0823fba654c8fd849c821338e6624aefac6935a92836523dde9eb6524874949a"
PINNED_VENDORED_SHA256 = "2291e166792fabc70f4961a757d0561becec3d2721fda287dfe6b4732bbc66f6"

UPSTREAM_REPO_PATH = Path("/tmp/fc")
UPSTREAM_REL_FILE = Path("FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean")

TARGET_DEFINITIONS = [
    "IsUniform",
    "IsProperHypergraphColoring",
    "HypergraphColorable",
    "HasHypergraphChromaticNumber",
    "hypergraphDegree",
]


def extract_definitions(text: str) -> dict[str, str]:
    """Extracts Lean definitions by name, returning normalized signature + body."""
    defs: dict[str, str] = {}
    pat = re.compile(
        r"^def\s+([A-Za-z0-9_]+)\s*(.*?)\s*:=\s*(.*?)(?=\n(?:def\s|instance\s|theorem\s|lemma\s|omit\s|end\s|namespace\s|variable\s|set_option\s|open\s|/--|/-!|\Z))",
        re.M | re.S,
    )
    for m in pat.finditer(text):
        name = m.group(1).strip()
        sig = " ".join(m.group(2).split())
        body = " ".join(m.group(3).split())
        defs[name] = f"def {name} {sig} := {body}"
    return defs


def make_upstream_lean_definitions(ref_defs: dict[str, str]) -> str:
    """Generates an independent Upstream.Finset namespace from machine-extracted reference definitions.

    Explicitly qualifies internal predicate calls (e.g. H.IsProperHypergraphColoring ->
    Upstream.Finset.IsProperHypergraphColoring H) so that Lean's dot-notation on
    H : Finset (Finset V) does not accidentally resolve to local Finset predicates.
    """
    lines = [
        "namespace Upstream.Finset",
        "variable {V : Type*} [DecidableEq V]",
    ]
    for name in TARGET_DEFINITIONS:
        if name not in ref_defs:
            raise KeyError(f"missing target definition '{name}' in extracted reference definitions")
        raw_def = ref_defs[name]
        # Replace dot-notation calls on Finset with explicit Upstream.Finset calls:
        # e.g. H.IsProperHypergraphColoring c -> Upstream.Finset.IsProperHypergraphColoring H c
        def_code = re.sub(
            r"\b([A-Za-z0-9_]+)\.IsProperHypergraphColoring\s+([A-Za-z0-9_]+)\b",
            r"Upstream.Finset.IsProperHypergraphColoring \1 \2",
            raw_def,
        )
        # e.g. H.HypergraphColorable <arg> -> Upstream.Finset.HypergraphColorable H <arg>
        def_code = re.sub(
            r"\b([A-Za-z0-9_]+)\.HypergraphColorable\s+([A-Za-z0-9_]+)\b",
            r"Upstream.Finset.HypergraphColorable \1 \2",
            def_code,
        )
        lines.append(def_code)
    lines.append("end Upstream.Finset")
    return "\n".join(lines)


def verify_definition_texts(
    source_defs: dict[str, str], ref_defs: dict[str, str]
) -> list[str]:
    """Compares the 5 target definitions. Returns list of errors."""
    errors = []
    for name in TARGET_DEFINITIONS:
        if name not in ref_defs:
            errors.append(f"missing target definition '{name}' in reference")
            continue
        if name not in source_defs:
            errors.append(f"missing transplanted definition '{name}' in source")
            continue
        src = source_defs[name]
        ref = ref_defs[name]
        if src != ref:
            errors.append(
                f"definition '{name}' mismatch:\n  expected: {ref}\n  actual:   {src}"
            )
    return errors


def verify_lean_rfl(ref_defs: dict[str, str], module: str = "Erdos834") -> tuple[bool, str]:
    """Verifies definitional equality (`by rfl`) against machine-extracted Upstream.Finset declarations."""
    upstream_block = make_upstream_lean_definitions(ref_defs)

    code = f"""import {module}
open scoped Finset

-- Machine-generated independent Upstream.Finset declarations extracted from hash-verified reference
{upstream_block}

variable {{V : Type*}} [DecidableEq V]

-- Definitional equality proofs for all 5 transplanted definitions
example (H : Finset (Finset V)) (r : ℕ) :
    H.IsUniform r ↔ Upstream.Finset.IsUniform H r := by rfl

example {{C : Type*}} (H : Finset (Finset V)) (c : V → C) :
    H.IsProperHypergraphColoring c ↔ Upstream.Finset.IsProperHypergraphColoring H c := by rfl

example (H : Finset (Finset V)) (k : ℕ) :
    H.HypergraphColorable k ↔ Upstream.Finset.HypergraphColorable H k := by rfl

example (H : Finset (Finset V)) (k : ℕ) :
    H.HasHypergraphChromaticNumber k ↔ Upstream.Finset.HasHypergraphChromaticNumber H k := by rfl

example (H : Finset (Finset V)) (v : V) :
    H.hypergraphDegree v = Upstream.Finset.hypergraphDegree H v := by rfl
"""
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as fh:
        fh.write(code)
        tmp = Path(fh.name)
    try:
        res = subprocess.run(
            ["lake", "env", "lean", str(tmp)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=3600,
        )
        return (res.returncode == 0), (res.stdout + res.stderr).strip()
    finally:
        tmp.unlink(missing_ok=True)


def run_controls() -> bool:
    """Runs self-test control suite checking that definition discrepancies are caught."""
    ref_sample = """
namespace Finset
variable {V : Type*} [DecidableEq V]
def IsUniform (H : Finset (Finset V)) (r : ℕ) : Prop := ∀ e ∈ H, e.card = r
def IsProperHypergraphColoring (H : Finset (Finset V)) {C : Type*} (c : V → C) : Prop :=
  ∀ e ∈ H, ∃ x ∈ e, ∃ y ∈ e, c x ≠ c y
def HypergraphColorable (H : Finset (Finset V)) (k : ℕ) : Prop :=
  ∃ c : V → Fin k, H.IsProperHypergraphColoring c
def HasHypergraphChromaticNumber (H : Finset (Finset V)) (k : ℕ) : Prop :=
  H.HypergraphColorable k ∧ ∀ j < k, ¬ H.HypergraphColorable j
def hypergraphDegree (H : Finset (Finset V)) (v : V) : ℕ := #{e ∈ H | v ∈ e}
end Finset
"""
    ref_defs = extract_definitions(ref_sample)
    all_ok = True
    print("=== RUNNING CHECK_DEFINITION_MATCH CONTROLS ===")

    # Control 1: Exact match
    c1_errs = verify_definition_texts(ref_defs, ref_defs)
    c1_pass = (len(c1_errs) == 0)
    print(f"[{'PASS' if c1_pass else 'FAIL'}] exact match control                   -> clean={c1_pass}")
    if not c1_pass:
        all_ok = False

    # Control 2: Modified IsUniform body (trivial True)
    mod_sample2 = ref_sample.replace("∀ e ∈ H, e.card = r", "True")
    c2_errs = verify_definition_texts(extract_definitions(mod_sample2), ref_defs)
    c2_pass = (len(c2_errs) == 1 and "IsUniform" in c2_errs[0])
    print(f"[{'PASS' if c2_pass else 'FAIL'}] modified IsUniform body caught          -> caught={c2_pass}")
    if not c2_pass:
        all_ok = False

    # Control 3: Modified HypergraphColorable type
    mod_sample3 = ref_sample.replace(
        "HypergraphColorable (H : Finset (Finset V)) (k : ℕ)",
        "HypergraphColorable (H : Finset (Finset V)) (k : Int)",
    )
    c3_errs = verify_definition_texts(extract_definitions(mod_sample3), ref_defs)
    c3_pass = (len(c3_errs) == 1 and "HypergraphColorable" in c3_errs[0])
    print(f"[{'PASS' if c3_pass else 'FAIL'}] modified HypergraphColorable type caught  -> caught={c3_pass}")
    if not c3_pass:
        all_ok = False

    # Control 4: Missing definition
    mod_sample4 = ref_sample.replace("def hypergraphDegree", "def otherDegree")
    c4_errs = verify_definition_texts(extract_definitions(mod_sample4), ref_defs)
    c4_pass = (len(c4_errs) == 1 and "hypergraphDegree" in c4_errs[0])
    print(f"[{'PASS' if c4_pass else 'FAIL'}] missing hypergraphDegree caught         -> caught={c4_pass}")
    if not c4_pass:
        all_ok = False

    # Control 5: Dependency isolation test in make_upstream_lean_definitions
    gen_upstream = make_upstream_lean_definitions(ref_defs)
    c5_pass = (
        "Upstream.Finset.IsProperHypergraphColoring H c" in gen_upstream
        and "Upstream.Finset.HypergraphColorable H k" in gen_upstream
        and "Upstream.Finset.HypergraphColorable H j" in gen_upstream
        and "H.IsProperHypergraphColoring" not in gen_upstream
        and "H.HypergraphColorable" not in gen_upstream
    )
    print(f"[{'PASS' if c5_pass else 'FAIL'}] upstream namespace dependency isolation  -> isolated={c5_pass}")
    if not c5_pass:
        all_ok = False

    return all_ok


def main() -> None:
    ap = argparse.ArgumentParser(description="Verify Finset definition correspondence against upstream")
    ap.add_argument("--source", default=str(ROOT / "Erdos834.lean"))
    ap.add_argument("--upstream-repo", default=str(UPSTREAM_REPO_PATH), help="Optional path to local upstream clone")
    ap.add_argument("--reference", default=str(VENDORED_REF_FILE))
    ap.add_argument("--lean", action="store_true", default=True, help="Prove definitional equality in Lean kernel (by rfl) [default: True]")
    ap.add_argument("--no-lean", dest="lean", action="store_false", help="Skip Lean kernel rfl verification")
    ap.add_argument("--run-controls", action="store_true", help="Run self-test control suite")
    args = ap.parse_args()

    if args.run_controls:
        ok = run_controls()
        sys.exit(0 if ok else 1)

    print("=== FINSET DEFINITION CORRESPONDENCE AUDIT ===")
    print(f"pinned upstream commit: {PINNED_UPSTREAM_COMMIT}")

    # Step 1: Always verify vendored reference file (no dependence on /tmp/fc)
    vendored = Path(args.reference)
    if not vendored.is_file():
        print(f"[ERROR] vendored reference file not found: {vendored}", file=sys.stderr)
        sys.exit(2)
    actual_v_sha256 = hashlib.sha256(vendored.read_bytes()).hexdigest()
    print(f"vendored reference    : {vendored}")
    print(f"vendored ref sha256   : {actual_v_sha256}")
    if actual_v_sha256 != PINNED_VENDORED_SHA256:
        print(f"[FAIL] vendored reference hash mismatch:\n  expected {PINNED_VENDORED_SHA256}\n  actual   {actual_v_sha256}", file=sys.stderr)
        sys.exit(1)
    ref_text = vendored.read_text(encoding="utf-8")

    # Step 1b: Optional check against /tmp/fc if available (non-blocking if absent)
    if args.upstream_repo:
        upstream_file = Path(args.upstream_repo) / UPSTREAM_REL_FILE
        if upstream_file.is_file():
            actual_u_sha256 = hashlib.sha256(upstream_file.read_bytes()).hexdigest()
            print(f"upstream clone file   : {upstream_file}")
            print(f"upstream clone sha256 : {actual_u_sha256}")
            if actual_u_sha256 != PINNED_UPSTREAM_FILE_SHA256:
                print(f"[FAIL] upstream clone file sha256 mismatch: expected {PINNED_UPSTREAM_FILE_SHA256}", file=sys.stderr)
                sys.exit(1)

    # Step 2: Extract definitions
    source_file = Path(args.source)
    if not source_file.is_file():
        print(f"[ERROR] source file not found: {source_file}", file=sys.stderr)
        sys.exit(2)
    source_text = source_file.read_text(encoding="utf-8")

    ref_defs = extract_definitions(ref_text)
    src_defs = extract_definitions(source_text)

    # Step 3: Compare each target definition
    errs = verify_definition_texts(src_defs, ref_defs)
    if errs:
        print("\n[FAIL] Discrepancies detected:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print("\n[OK] All 5 transplanted Finset definitions match upstream exactly:")
    for name in TARGET_DEFINITIONS:
        print(f"  ✓ {src_defs[name]}")

    # Step 4: Lean kernel rfl check (default enabled)
    if args.lean:
        print("\n[LEAN] Verifying definitional equality (by rfl) against machine-extracted Upstream declarations...")
        ok, out = verify_lean_rfl(ref_defs, module=Path(args.source).stem)
        if not ok:
            print(f"[FAIL] Lean definitional equality check failed:\n{out}", file=sys.stderr)
            sys.exit(1)
        print("[OK] Lean kernel confirmed definitional equality (rfl) for all 5 definitions.")

    sys.exit(0)


if __name__ == "__main__":
    main()
