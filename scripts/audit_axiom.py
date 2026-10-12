#!/usr/bin/env python3
"""Fail-closed axiom audit for a Lean theorem.

Enforced rules (Justin Sun Prize PR template / docs/verification.md):
  * the target must elaborate in a clean environment;
  * `#print axioms` output must be inspected transitively;
  * `sorryAx`, `admit`, `native_decide`, `Lean.trustCompiler`,
    `debug.skipKernelTC`, `implemented_by`/`extern` are disqualifying;
  * only `propext`, `Classical.choice`, `Quot.sound` are standard foundations.

FAIL-CLOSED: any outcome that is not an unambiguous clean parse exits non-zero.
A parse failure must never be reported as an accepted proof.

Exit codes: 0 accepted, 1 rejected, 2 could-not-determine.
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

NO_AXIOM_PAT = re.compile(r"does not depend on any axioms")
AXIOM_LIST_PAT = re.compile(r"depends on axioms:\s*\[(.*?)\]", re.S)


def run(module: str, theorem: str) -> tuple[int, str]:
    code = f"import {module}\n#print axioms {theorem}\n"
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as fh:
        fh.write(code)
        tmp = Path(fh.name)
    try:
        res = subprocess.run(["lake", "env", "lean", str(tmp)],
                             cwd=ROOT, capture_output=True, text=True, timeout=3600)
        return res.returncode, res.stdout + res.stderr
    finally:
        tmp.unlink(missing_ok=True)


def classify(theorem: str, rc: int, output: str) -> tuple[str, int, dict]:
    flat = " ".join(output.split())
    info: dict = {"theorem": theorem, "axioms": [], "raw": flat}

    if rc != 0:
        info["error"] = flat
        return "ELABORATION_FAILED", 1, info
    if re.search(r"declaration uses 'sorry'", flat):
        info["axioms"] = ["sorryAx(implied by compiler warning)"]
        return "REJECTED_FORBIDDEN_AXIOM", 1, info
    if NO_AXIOM_PAT.search(flat):
        return "ACCEPTED_PURE_PROOF", 0, info

    m = AXIOM_LIST_PAT.search(flat)
    if not m:
        info["error"] = "unparseable #print axioms output; refusing to accept"
        return "INDETERMINATE", 2, info

    axioms = [a.strip() for a in m.group(1).split(",") if a.strip()]
    info["axioms"] = axioms
    forbidden = [a for a in axioms if a in FORBIDDEN_EXACT or FORBIDDEN_HINT.search(a)]
    custom = [a for a in axioms if a not in ALLOWED and a not in forbidden]
    if forbidden:
        info["forbidden"] = forbidden
        return "REJECTED_FORBIDDEN_AXIOM", 1, info
    if custom:
        info["custom"] = custom
        return "REJECTED_CUSTOM_AXIOM", 1, info
    return "ACCEPTED_PURE_PROOF", 0, info


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit Lean theorem axioms (fail-closed)")
    ap.add_argument("--module", default="Erdos834")
    ap.add_argument("--theorem", required=True)
    args = ap.parse_args()

    rc, output = run(args.module, args.theorem)
    verdict, code, info = classify(args.theorem, rc, output)

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
