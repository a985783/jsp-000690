# JSP-000690 — Formalization of "A 3-Uniform 3-Chromatic-Critical Hypergraph with Minimum Degree ≥ 7"

Lean 4 formalization prepared for **Justin Sun Prize problem JSP-000690**.

* **Problem (JSP catalogue):**
  *Is there a three-uniform, three-chromatic-critical hypergraph with minimum degree at least seven?*
* **Answer formalized:** **Yes** — established by exhibiting an explicit witness
  and having the Lean kernel verify every required property.
* **Target declaration:** `Erdos834.erdos_834.parts.ii`
* **Source file:** `Erdos834.lean` (single file, no dependencies beyond Mathlib)
* **Licence:** Apache-2.0 (see [LICENSE](LICENSE), [NOTICE](NOTICE), and [ATTRIBUTION.md](ATTRIBUTION.md))

---

## 1. What is Proved

The formalized theorem (`Erdos834.erdos_834.parts.ii`) corresponds directly in
type and declaration signature to the target specified upstream in
`google-deepmind/formal-conjectures` at
`FormalConjectures/ErdosProblems/834.lean` (vendored with pinned SHA256 in
`challenge/Erdos834.lean`):

```lean
theorem erdos_834.parts.ii :
    answer(True) ↔ ∃ (n : ℕ) (H : Finset (Finset (Fin n))),
    H.IsUniform 3 ∧ H.HasHypergraphChromaticNumber 3 ∧
      (∀ e ∈ H, (H.erase e).HypergraphColorable 2) ∧
      (∀ v : Fin n, (H.filter (fun e ↦ v ∉ e)).HypergraphColorable 2) ∧
      ∀ v : Fin n, 7 ≤ H.hypergraphDegree v
```

Anchored on the witness `H` exported by `Erdos834.H`, the file also proves the
seven component lemmas:

| Lemma | Content |
|---|---|
| `H_uniform` | All 22 edges have exactly 3 vertices |
| `H_degrees` | Every one of the 9 vertices has degree ≥ 7 (degree sequence `10,7,7,7,7,7,7,7,7`) |
| `H_colorable_3` | `H` admits a proper 3-colouring (explicit witness `Erdos834.c3`) |
| `H_not_colorable_lt_3` | `H` is not $j$-colourable for any $j < 3$ (all 2/1/0-colourings are exhausted) |
| `H_chromatic` | Chromatic number of `H` is exactly 3 |
| `H_crit_edges` | Deleting any edge makes `H` 2-colourable |
| `H_crit_verts` | Deleting any vertex makes `H` 2-colourable |

The witness is the 9-vertex, 22-edge 3-uniform hypergraph given in
**Ruiliang Li [Li25]**, *On an Erdős–Lovász problem: 3-critical 3-graphs of minimum
degree 7*, arXiv:2512.24850 [cs.DM] (December 2025), Theorem 4.1, display (5).

Every property is discharged by kernel-checked finite evaluation (`decide`).
**`native_decide` is not used anywhere** — see Section 5.

---

## 2. Provenance, Attribution, and AI Disclosure

* **Problem Origin:** Attributed to Paul Erdős and László Lovász by the
  [Erdős Problem 834 page](https://www.erdosproblems.com/834), which cites
  `[Er74d, p.282]`: P. Erdős, *Unsolved Problems* (1974), pp. 278–297
  ([bibliography](https://www.erdosproblems.com/bibs/Er74d)). The printed page
  itself was not independently inspected. JSP specifies the chromatic reading.
* **Mathematical Discovery:** Resolved by **Ruiliang Li** (李睿良), Department of
  Mathematical Sciences, Tsinghua University (arXiv:2512.24850 [cs.DM], Dec 2025).
  The solver role for the underlying mathematics belongs exclusively to that work;
  this repository claims the **formalization contributor role only**.
* **Upstream Definitions:** Hypergraph predicates (`Finset.IsUniform`,
  `Finset.IsProperHypergraphColoring`, `Finset.HypergraphColorable`,
  `Finset.HasHypergraphChromaticNumber`, `Finset.hypergraphDegree`) are ported
  from `formal-conjectures/FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean`
  (commit `2067d8bb82058f40ccbd20a14fb94502434ea9eb`, Copyright 2026 The Formal
  Conjectures Authors, Apache-2.0). Computable `Decidable` instances were added
  in `Erdos834.lean` to enable finite reduction by `decide`.
* **Challenge Specification:** `challenge/Erdos834.lean` is pinned to commit
  `2067d8bb82058f40ccbd20a14fb94502434ea9eb` (SHA256: `626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f`)
  and used solely for statement correspondence validation.
* **Formalization Submitter:** GitHub account [`@qingsongcui`](https://github.com/qingsongcui).
  Real name is unconfirmed by the account holder and is omitted here to avoid
  fabrication.
* **AI Assistance Disclosure:** Proof search structuring, finite instance
  adaptation for kernel reduction, and verification harnesses were developed
  with the assistance of Oh My Pi (OMP) AI coding tools. All statements and proofs
  are strictly validated by the official Lean 4.33.1 kernel.
* Complete attribution details are documented in [ATTRIBUTION.md](ATTRIBUTION.md)
  and [NOTICE](NOTICE).

---

## 3. Toolchain and Pinned Dependencies

```
lean-toolchain      leanprover/lean4:v4.33.1
mathlib             leanprover-community/mathlib4 @ 0df444a360eaa60ab8c11dca51a86af692955474
```

`lake-manifest.json` pins the complete transitive dependency graph at these
exact revisions.

---

## 4. Reproduction and Verification Instructions

### Manual Execution

```sh
lake exe cache get     # retrieve prebuilt Mathlib oleans for the pinned revision
lake build             # build the `Erdos834` target
python3 scripts/scan_placeholders.py Erdos834.lean
python3 scripts/check_definition_match.py
python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
python3 scripts/check_statement_match.py
```

### Automated Script

```sh
bash scripts/reproduce.sh
bash scripts/reproduce.sh --controls
```

The script runs the full pipeline:
1. Verifies the toolchain versions.
2. Ensures Mathlib prebuilt artifacts are resolved.
3. Cleans and rebuilds only `Erdos834`, preserving dependency artifacts.
4. Scans the proof after stripping comments and strings for forbidden constructs.
5. Verifies all five ported definitions against the pinned reference, including
   kernel-checked definitional equality of machine-extracted declarations.
6. Performs a target-bound, fail-closed transitive axiom audit.
7. Verifies statement correspondence against the pinned challenge file.

*Reproduction evidence (2026-10-12):* All nine dependency repositories were
freshly cloned in `/tmp/jsp690-fresh-20261012` without shared package symlinks.
Prebuilt oleans used existing host cache archives; cold network download of
those archives was not tested. The final `bash scripts/reproduce.sh` completed
every check with exit 0 after cleaning the package build. Auditor controls and
actual Lean clean/sorry examples passed their accept/reject expectations.

---

## 5. Axiom Audit (Transitive, Fail-Closed)

`scripts/audit_axiom.py` inspects the output of `#print axioms` for the target
declaration and enforces fail-closed policies: it accepts only standard Lean
foundations (`propext`, `Classical.choice`, `Quot.sound`) and returns a non-zero
exit code if `sorryAx`, compiler-trust axioms (`Lean.ofReduceBool`), or unparseable
outputs are encountered.

Observed command and output:

```
$ python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
[raw] 'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, Classical.choice, Quot.sound]
=== AUDIT RESULT ===
target   : Erdos834.erdos_834.parts.ii
verdict  : ACCEPTED_STANDARD_AXIOMS
axioms   : ['propext', 'Classical.choice', 'Quot.sound']
$ echo $?
0
```

Because `decide` is evaluated inside the Lean kernel rather than via `native_decide`,
no compiler trust axiom is introduced into the proof.

---

## 6. Statement Correspondence

`scripts/check_statement_match.py` verifies that our theorem typechecks against
the **exact statement string extracted from the pinned challenge file**:

1. Verifies the SHA256 of `challenge/Erdos834.lean`.
2. Machine-extracts the statement signature of `erdos_834.parts.ii`.
3. Invokes Lean to typecheck `@Erdos834.erdos_834.parts.ii` against that extracted statement.

Observed output:

```
$ python3 scripts/check_statement_match.py
challenge file : Erdos834.lean  sha256=626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f
challenge stmt : answer(True) ↔ ∃ (n : ℕ) (H : Finset (Finset (Fin n))), H.IsUniform 3 ∧ …
our proof      : @Erdos834.erdos_834.parts.ii

RESULT: MATCH — our proof typechecks at the frozen challenge statement.
$ echo $?
0
```

---

## 7. Scope, Priority, and Status

* **Intended Contribution:** Formalization only. The mathematical resolution is
  credited to [Li25]. No award application has been submitted.
* **Completeness:** The formalization addresses the exact yes/no question of the
  problem catalogue, establishing a complete formal answer to the problem as
  recorded.
* **Local Preparation Status:** This package is prepared locally for validation.
  No pull request has been opened, no commits have been published to external
  remotes, and no contact with the prize organizers has been made.
* **Priority Audit Disclaimer:** Internal auditing of prior submissions on
  `TheJustinSunPrize/awards` is conducted purely for due-diligence awareness.
  The presence or count of prior PRs does not represent an official assessment
  of priority, validity, or eligibility. Official evaluation and acceptance are
  the sole prerogative of the Justin Sun Prize Academic and Evaluation Committee.
* **Submission Recommendation:** Do not submit this as a first/priority
  formalization claim. Earlier same-target source is linked in official PRs;
  see [PRIORITY-AUDIT.md](PRIORITY-AUDIT.md) for the static evidence and its
  verification limits. [SUBMISSION.md](SUBMISSION.md) is a conditional draft,
  not authorization to publish and not proof of award eligibility.

---

## 8. Verification Summary

Observed locally on Apple Silicon (arm64, macOS, Lean `v4.33.1`):

| Check | Result | Scope / Notes |
|---|---|---|
| Dependency clone | PASS | All 9 dependencies cloned cleanly from git in fresh tree |
| Olean resolution | PASS | Resolved via local Lake cache (cold network download untested) |
| Clean one-command reproduction | PASS | 8707 jobs; final module build 84 seconds; complete script exit 0 |
| Forbidden placeholder scan | PASS | Zero `sorry` / `admit` / `native_decide` / `axiom` / `opaque` |
| Transitive axiom audit | PASS | Target and all seven component lemmas: `[propext, Classical.choice, Quot.sound]` |
| Statement correspondence | PASS | Exact typecheck MATCH against pinned challenge file |
| Definition correspondence | PASS | Five machine-extracted upstream definitions; Lean `rfl` checks |
| Auditor controls | PASS | 31 parser/scanner controls; actual clean proof accepted and `sorryAx` rejected |

The final 40-character local commit SHA is supplied in the delivery report;
it is not embedded in its own commit. Publishing and organizer review remain
separate, unperformed actions.
