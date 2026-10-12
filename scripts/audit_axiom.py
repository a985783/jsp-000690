#!/usr/bin/env python3
"""Fail-closed axiom audit for a Lean theorem.

Enforced rules (Justin Sun Prize PR template / docs/verification.md):
  * the target must elaborate in a clean environment;
  * `#print axioms` output must be inspected transitively;
  * `sorryAx`, `admit`, `native_decide`, `Lean.trustCompiler`,
    `debug.skipKernelTC`, `implemented_by`/`extern` are disqualifying;
  * only `propext`, `Classical.choice`, `Quot.sound` are standard foundations.

TARGET-BOUND & FAIL-CLOSED:
  * output regex binds specifically to the target theorem identifier
    (e.g. `'Erdos834.erdos_834.parts.ii'` in single quotes);
  * an axiom list for a mismatched or wrong declaration is NEVER accepted;
  * any parse failure, compiler warning about sorry, custom axiom, or forbidden
    axiom exits non-zero.

Exit codes:
  0: accepted (clean proof with empty or standard-only axioms)
  1: rejected (forbidden axiom, custom axiom, or elaboration failure)
  2: could-not-determine / indeterminate parse failure
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN_EXACT = {"sorryAx", "Lean.trustCompiler", "Lean.ofReduceBool"}
FORBIDDEN_HINT = re.compile(
    r"sorry|admit|trustCompiler|skipKernelTC|implemented_by|extern|native_decide"
)


def get_target_candidates(module: str, theorem: str) -> list[str]:
    """Require the exact fully qualified declaration passed to #print axioms."""
    return [theorem]


def run(module: str, theorem: str) -> tuple[int, str]:
    code = f"import {module}\n#print axioms {theorem}\n"
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
        return res.returncode, res.stdout + res.stderr
    finally:
        tmp.unlink(missing_ok=True)


def classify(theorem: str, rc: int, output: str, module: str = "") -> tuple[str, int, dict]:
    flat = " ".join(output.split())
    info: dict = {"theorem": theorem, "axioms": [], "raw": flat}

    if rc != 0:
        info["error"] = flat
        return "ELABORATION_FAILED", 1, info

    if re.search(r"\bdeclaration uses 'sorry'\b", flat) or "declaration uses 'sorry'" in flat:
        info["axioms"] = ["sorryAx(implied by compiler warning)"]
        return "REJECTED_FORBIDDEN_AXIOM", 1, info

    if re.search(r"\berror:\b", flat):
        info["error"] = flat
        return "ELABORATION_FAILED", 1, info

    # Build target-bound patterns
    cands = get_target_candidates(module, theorem)
    escaped_names = "|".join(re.escape(c) for c in cands)
    target_re = rf"'(?:{escaped_names})'"

    no_axiom_pat = re.compile(rf"{target_re}\s+does not depend on any axioms")
    axiom_list_pat = re.compile(rf"{target_re}\s+depends on axioms:\s*\[(.*?)\]", re.S)

    if no_axiom_pat.search(flat):
        # Even if reported as no axioms, verify no forbidden hints in raw output
        forbidden_in_raw = [a for a in FORBIDDEN_EXACT if a in flat]
        if forbidden_in_raw:
            info["forbidden"] = forbidden_in_raw
            return "REJECTED_FORBIDDEN_AXIOM", 1, info
        return "ACCEPTED_PURE_PROOF", 0, info

    m = axiom_list_pat.search(flat)
    if not m:
        info["error"] = f"unparseable or target-mismatched #print axioms output for target '{theorem}'; refusing to accept"
        return "INDETERMINATE", 2, info

    raw_axioms = m.group(1).strip()
    axioms = [a.strip() for a in raw_axioms.split(",") if a.strip()]
    info["axioms"] = axioms

    forbidden = [a for a in axioms if a in FORBIDDEN_EXACT or FORBIDDEN_HINT.search(a)]
    custom = [a for a in axioms if a not in ALLOWED and a not in forbidden]

    if forbidden:
        info["forbidden"] = forbidden
        return "REJECTED_FORBIDDEN_AXIOM", 1, info
    if custom:
        info["custom"] = custom
        return "REJECTED_CUSTOM_AXIOM", 1, info

    return ("ACCEPTED_PURE_PROOF" if not axioms else "ACCEPTED_STANDARD_AXIOMS"), 0, info


def run_controls() -> bool:
    """Runs bidirectional self-test control suite without invoking Lean."""
    cases = [
        # (name, rc, output, expected_verdict, expected_code)
        (
            "pure proof with no axioms",
            0,
            "'Erdos834.erdos_834.parts.ii' does not depend on any axioms",
            "ACCEPTED_PURE_PROOF",
            0,
        ),
        (
            "standard axioms (propext, Quot.sound)",
            0,
            "'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, Quot.sound]",
            "ACCEPTED_STANDARD_AXIOMS",
            0,
        ),
        (
            "multiline standard axioms with whitespace",
            0,
            "'Erdos834.erdos_834.parts.ii' depends on axioms: [\n  propext,\n  Classical.choice\n]",
            "ACCEPTED_STANDARD_AXIOMS",
            0,
        ),
        (
            "target mismatch (other theorem without axioms)",
            0,
            "'OtherTheorem' does not depend on any axioms",
            "INDETERMINATE",
            2,
        ),
        (
            "target mismatch (other theorem with axioms)",
            0,
            "'OtherTheorem' depends on axioms: [propext]",
            "INDETERMINATE",
            2,
        ),
        (
            "compiler warning uses sorry",
            0,
            "warning: declaration uses 'sorry'\n'Erdos834.erdos_834.parts.ii' depends on axioms: [sorryAx]",
            "REJECTED_FORBIDDEN_AXIOM",
            1,
        ),
        (
            "forbidden axiom sorryAx",
            0,
            "'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, sorryAx]",
            "REJECTED_FORBIDDEN_AXIOM",
            1,
        ),
        (
            "forbidden axiom trustCompiler",
            0,
            "'Erdos834.erdos_834.parts.ii' depends on axioms: [Lean.trustCompiler]",
            "REJECTED_FORBIDDEN_AXIOM",
            1,
        ),
        (
            "custom axiom rejected",
            0,
            "'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, MySecretAxiom]",
            "REJECTED_CUSTOM_AXIOM",
            1,
        ),
        (
            "elaboration failure (rc=1)",
            1,
            "error: unknown identifier 'Erdos834.erdos_834.parts.ii'",
            "ELABORATION_FAILED",
            1,
        ),
        (
            "empty unparseable output",
            0,
            "random text without declaration name",
            "INDETERMINATE",
            2,
        ),
    ]

    all_ok = True
    print("=== RUNNING AUDIT_AXIOM CONTROLS ===")
    for label, rc, out, exp_verdict, exp_code in cases:
        verdict, code, _ = classify("Erdos834.erdos_834.parts.ii", rc, out, module="Erdos834")
        passed = (verdict == exp_verdict and code == exp_code)
        if not passed:
            all_ok = False
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {label:45s} -> {verdict} (exit {code}, expected {exp_verdict}/{exp_code})")
    return all_ok


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit Lean theorem axioms (fail-closed, target-bound)")
    ap.add_argument("--module", default="Erdos834")
    ap.add_argument("--theorem", default="Erdos834.erdos_834.parts.ii")
    ap.add_argument("--run-controls", action="store_true", help="Run self-test control suite")
    args = ap.parse_args()

    if args.run_controls:
        ok = run_controls()
        sys.exit(0 if ok else 1)

    rc, output = run(args.module, args.theorem)
    verdict, code, info = classify(args.theorem, rc, output, module=args.module)

    print(f"[raw] {info['raw'][:600]}")
    print("=== AUDIT RESULT ===")
    print(f"target   : {info['theorem']}")
    print(f"verdict  : {verdict}")
    print(f"axioms   : {info.get('axioms')}")
    if info.get("forbidden"):
        print(f"forbidden: {info['forbidden']}")
    if info.get("custom"):
        print(f"custom   : {info['custom']}")
    if info.get("error"):
        print(f"error    : {info['error']}")
    sys.exit(code)


if __name__ == "__main__":
    main()
