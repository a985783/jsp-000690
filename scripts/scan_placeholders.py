#!/usr/bin/env python3
"""macOS-compatible, comment-stripping placeholder scanner for Lean 4 source files.

Strips:
  - Single line comments: `-- ...`
  - Nested block comments / docstrings: `/- ... -/` (with arbitrary nesting depth)
Respects string literals (`"..."`) so string content is not treated as comments.
Preserves line numbers for precise diagnostics.

Forbidden tokens scanned in stripped code:
  - `sorry`, `admit`, `native_decide`, `sorryAx`
  - `axiom <ident>`
  - `opaque <ident>`
  - `Lean.trustCompiler`, `debug.skipKernelTC`, `implemented_by`, `extern`

Exit codes:
  0: all inspected files are completely clean
  1: forbidden placeholder / construct detected
  2: syntax / IO error
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("sorry", re.compile(r"\bsorry\b")),
    ("admit", re.compile(r"\badmit\b")),
    ("native_decide", re.compile(r"\bnative_decide\b")),
    ("sorryAx", re.compile(r"\bsorryAx\b")),
    ("custom axiom declaration", re.compile(r"\baxiom\s+[A-Za-z_]")),
    ("opaque declaration", re.compile(r"\bopaque\s+[A-Za-z_]")),
    ("trustCompiler", re.compile(r"\bLean\.trustCompiler\b")),
    ("skipKernelTC", re.compile(r"\bdebug\.skipKernelTC\b")),
    ("implemented_by", re.compile(r"\bimplemented_by\b")),
    ("extern", re.compile(r"\bextern\b")),
]


def strip_lean_comments(text: str) -> str:
    """Strips line and block comments from Lean 4 source while preserving line breaks."""
    result: list[str] = []
    i = 0
    n = len(text)
    depth = 0
    in_string = False

    while i < n:
        if depth > 0:
            if i + 1 < n and text[i : i + 2] == "/-":
                depth += 1
                i += 2
            elif i + 1 < n and text[i : i + 2] == "-/":
                depth -= 1
                i += 2
                if depth == 0:
                    result.append(" ")
            elif text[i] == "\n":
                result.append("\n")
                i += 1
            else:
                i += 1
        elif in_string:
            ch = text[i]
            if ch == "\\":
                result.append(" ")
                if i + 1 < n:
                    result.append("\n" if text[i + 1] == "\n" else " ")
                    i += 2
                else:
                    i += 1
            elif ch == '"':
                in_string = False
                result.append('"')
                i += 1
            elif ch == "\n":
                result.append("\n")
                i += 1
            else:
                result.append(" ")
                i += 1
        else:
            if text[i] == '"':
                in_string = True
                result.append('"')
                i += 1
            elif i + 1 < n and text[i : i + 2] == "--":
                i += 2
                while i < n and text[i] != "\n":
                    i += 1
            elif i + 1 < n and text[i : i + 2] == "/-":
                depth = 1
                i += 2
            else:
                result.append(text[i])
                i += 1

    return "".join(result)


def scan_source(source: str, filename: str = "<source>") -> list[str]:
    """Scans Lean source after stripping comments. Returns a list of error descriptions."""
    stripped = strip_lean_comments(source)
    orig_lines = source.splitlines()
    stripped_lines = stripped.splitlines()

    errors: list[str] = []
    for line_idx, stripped_line in enumerate(stripped_lines):
        line_num = line_idx + 1
        for label, pat in FORBIDDEN_PATTERNS:
            m = pat.search(stripped_line)
            if m:
                raw_line = orig_lines[line_idx] if line_idx < len(orig_lines) else stripped_line
                errors.append(
                    f"{filename}:{line_num}: forbidden construct detected ({label}): '{raw_line.strip()}'"
                )
    return errors


def run_controls() -> bool:
    """Runs bidirectional self-test controls."""
    cases: list[tuple[str, str, bool]] = [
        ("clean code", "def x : ℕ := 1\n", True),
        ("line comment with sorry", "-- theorem foo : False := by sorry\ndef x : ℕ := 1\n", True),
        ("docstring with sorry mention", "/-- This solves upstream problem which had sorry. -/\ndef x : ℕ := 1\n", True),
        ("nested block comment with sorry", "/- outer /- inner sorry -/ still outer -/\ndef x : ℕ := 1\n", True),
        ("string containing sorry word", 'def msg : String := "this is sorry in string"\n', True),
        ("actual sorry", "theorem foo : False := by sorry\n", False),
        ("actual admit", "theorem foo : False := by admit\n", False),
        ("actual native_decide", "theorem foo : True := by native_decide\n", False),
        ("actual sorryAx", "theorem foo : False := sorryAx\n", False),
        ("actual axiom", "axiom my_bad_ax : False\n", False),
        ("actual opaque", "opaque mysterious_const : ℕ\n", False),
        ("actual trustCompiler", "attribute [Lean.trustCompiler] foo\n", False),
    ]

    all_ok = True
    print("=== RUNNING SCAN_PLACEHOLDERS CONTROLS ===")
    for name, src, expected_clean in cases:
        errs = scan_source(src, filename=name)
        is_clean = len(errs) == 0
        if is_clean == expected_clean:
            status = "PASS"
        else:
            status = "FAIL"
            all_ok = False
        print(f"[{status}] {name:36s} expected clean={expected_clean}, got clean={is_clean}")
        if not is_clean and expected_clean:
            for e in errs:
                print(f"       unexpected error: {e}")
    return all_ok


def main() -> None:
    ap = argparse.ArgumentParser(description="Scan Lean source for forbidden placeholders (comment-stripped)")
    ap.add_argument("files", nargs="*", help="Lean source files to scan")
    ap.add_argument("--run-controls", action="store_true", help="Run self-test control suite")
    args = ap.parse_args()

    if args.run_controls:
        ok = run_controls()
        sys.exit(0 if ok else 1)

    if not args.files:
        ap.error("at least one file or --run-controls must be specified")

    total_errors = 0
    for f in args.files:
        path = Path(f)
        if not path.is_file():
            print(f"[ERROR] file not found: {path}", file=sys.stderr)
            total_errors += 1
            continue
        source = path.read_text(encoding="utf-8")
        errs = scan_source(source, filename=str(path))
        if errs:
            for e in errs:
                print(f"[FAIL] {e}", file=sys.stderr)
            total_errors += len(errs)
        else:
            print(f"[OK] {path}: clean ({len(source.splitlines())} lines scanned, comments stripped)")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
