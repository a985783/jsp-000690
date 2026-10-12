#!/usr/bin/env python3
"""Statement-correspondence check for this submission.

Proves that our Lean proof typechecks at the EXACT statement written in the
upstream challenge file, which is vendored here as `challenge/Erdos834.lean`
and hash-pinned. The statement text is machine-extracted from that file (never
retyped by hand), then Lean itself decides whether our proof inhabits it.

Exit 0 iff the frozen file matches its pin, the statement is extractable, and
Lean accepts our proof at that statement.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHALLENGE_FILE = ROOT / "challenge" / "Erdos834.lean"
CHALLENGE_SHA256 = "626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f"
CHALLENGE_THEOREM = "erdos_834.parts.ii"
OURS = "Erdos834.erdos_834.parts.ii"
IMPORTS = ["Erdos834"]

STMT_PAT = r"^theorem\s+{n}\s*:\s*(.*?)\s*:= by\s*$"


def extract_statement(text: str, name: str) -> str:
    m = re.search(STMT_PAT.format(n=re.escape(name)), text, re.S | re.M)
    if not m:
        raise SystemExit(f"could not extract statement for `{name}`")
    stmt = " ".join(m.group(1).split())
    if not stmt:
        raise SystemExit(f"empty statement for `{name}`")
    return stmt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--challenge-file", default=str(CHALLENGE_FILE))
    ap.add_argument("--challenge-sha", default=CHALLENGE_SHA256)
    ap.add_argument("--challenge", default=CHALLENGE_THEOREM)
    ap.add_argument("--ours", default=OURS)
    args = ap.parse_args()

    cf = Path(args.challenge_file)
    if not cf.exists():
        raise SystemExit(f"challenge file not found: {cf}")
    actual = hashlib.sha256(cf.read_bytes()).hexdigest()
    if args.challenge_sha and actual != args.challenge_sha:
        raise SystemExit(
            f"CHALLENGE FILE HASH MISMATCH\n  expected {args.challenge_sha}\n"
            f"  actual   {actual}\nRefusing to certify against a possibly-edited file."
        )

    stmt = extract_statement(cf.read_text(), args.challenge)
    src = ("".join(f"import {m}\n" for m in IMPORTS) + "\n"
           + "-- statement text machine-extracted from the pinned challenge file\n"
           + f"example : {stmt} := @{args.ours}\n")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as fh:
        fh.write(src)
        tmp = Path(fh.name)
    try:
        res = subprocess.run(["lake", "env", "lean", str(tmp)],
                             cwd=ROOT, capture_output=True, text=True, timeout=3600)
        out = (res.stdout + res.stderr).strip()
    finally:
        tmp.unlink(missing_ok=True)

    print(f"challenge file : {cf.name}  sha256={actual}")
    print(f"challenge stmt : {stmt}")
    print(f"our proof      : @{args.ours}")
    if res.returncode == 0 and not out:
        print("\nRESULT: MATCH — our proof typechecks at the frozen challenge statement.")
        sys.exit(0)
    print(f"\nRESULT: MISMATCH — Lean rejected it:\n{out[:2000]}")
    sys.exit(1)


if __name__ == "__main__":
    main()
