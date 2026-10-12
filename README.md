# JSP-000690 — formalization of "a 3-uniform 3-chromatic-critical hypergraph with minimum degree ≥ 7"

Lean 4 formalization submitted for **Justin Sun Prize problem JSP-000690**.

* **Problem (JSP catalogue):**
  *Is there a three-uniform, three-chromatic-critical hypergraph with minimum degree at least seven?*
* **Answer formalized:** **Yes** — established by exhibiting an explicit witness and
  having the Lean kernel verify every required property.
* **Target declaration:** `Erdos834.erdos_834.parts.ii`
* **Source file:** `Erdos834.lean` (single file, no dependencies beyond Mathlib)

---

## 1. What is proved

The statement formalized is **byte-identical** to the one frozen upstream in
`google-deepmind/formal-conjectures` at
`FormalConjectures/ErdosProblems/834.lean` (a copy is vendored, hash-pinned, in
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

| lemma | content |
|---|---|
| `H_uniform` | all 22 edges have exactly 3 vertices |
| `H_degrees` | every one of the 9 vertices has degree ≥ 7 (degree sequence `10,7,7,7,7,7,7,7,7`) |
| `H_colorable_3` | `H` admits a proper 3-colouring (explicit witness `Erdos834.c3`) |
| `H_not_colorable_lt_3` | `H` is not `j`-colourable for any `j < 3` (all 2/1/0-colourings are exhausted) |
| `H_chromatic` | chromatic number of `H` is exactly 3 |
| `H_crit_edges` | deleting any edge makes `H` 2-colourable |
| `H_crit_verts` | deleting any vertex makes `H` 2-colourable |

The witness is the 9-vertex, 22-edge 3-uniform hypergraph given in
**Li [Li25]**, *On an Erdős–Lovász problem: 3-critical 3-graphs of minimum
degree 7*, arXiv:2512.24850, Theorem 4.1, display (5).

Every property is discharged by kernel-checked finite evaluation (`decide`).
**`native_decide` is not used anywhere** — see section 5.

---

## 2. Provenance and attribution

* The **mathematical result** is due to **Li (2025)** (arXiv:2512.24850). The
  solver role for this problem belongs to that work; the contribution here is
  the **machine-verifiable formalization**.
* The **hypergraph definition, colouring definitions and ported definitions**
  (`Finset.IsUniform`, `Finset.IsProperHypergraphColoring`,
  `Finset.HypergraphColorable`, `Finset.HasHypergraphChromaticNumber`,
  `Finset.hypergraphDegree`) are ported from
  `formal-conjectures/FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean`
  (Copyright 2026 The Formal Conjectures Authors, Apache-2.0). The licence header
  is retained verbatim at the top of `Erdos834.lean`.
* `answer(True)` is expanded by a local one-line macro to `True`, matching the
  semantics of upstream's `answer` term elaborator in
  `FormalConjecturesUtil/Answer.lean` (which elaborates its argument in place).
* No source from any third party is copied into this repository other than the
  Apache-2.0 licensed definitions noted above and the vendored upstream
  *statement* file under `challenge/` (used only for correspondence checking).

---

## 3. Toolchain and pinned dependencies

```
lean-toolchain      leanprover/lean4:v4.33.1
mathlib             leanprover-community/mathlib4 @ 0df444a360eaa60ab8c11dca51a86af692955474
```

`lake-manifest.json` records the full transitive dependency set at those
revisions.

---

## 4. Reproduction

```sh
lake exe cache get     # fetch prebuilt Mathlib oleans for the pinned revision
lake build             # clean build of `Erdos834`
python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
python3 scripts/check_statement_match.py
```

or simply:

```sh
sh scripts/reproduce.sh
```

`scripts/reproduce.sh` also greps the proof source for `sorry` / `admit` /
`native_decide` / `axiom` / `opaque` and fails if any is present.

---

## 5. Axiom audit (transitive, fail-closed)

`scripts/audit_axiom.py` runs `#print axioms` for the target and fails closed:
it accepts only `propext`, `Classical.choice`, `Quot.sound`, and returns a
non-zero exit code on `sorryAx` or on any output it cannot unambiguously parse.

Command and observed output:

```
$ python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
[raw] 'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, Classical.choice, Quot.sound]
=== AUDIT RESULT ===
target   : Erdos834.erdos_834.parts.ii
verdict  : ACCEPTED_PURE_PROOF
axioms   : ['propext', 'Classical.choice', 'Quot.sound']
$ echo $?
0
```

Note on proof techniques: the file uses `decide` (kernel-checked reduction), not
`native_decide`, so no compiler-trust axiom (`Lean.ofReduceBool`) enters the
proof. The audit above confirms this.

---

## 6. Statement correspondence

`scripts/check_statement_match.py` proves that our theorem typechecks at the
**exact statement written in the frozen challenge file**:

* it re-verifies the sha256 of `challenge/Erdos834.lean`,
* machine-extracts the statement text from that file (never retyped by hand),
* and asks Lean to check `@Erdos834.erdos_834.parts.ii` against it.

Observed result:

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

## 7. Scope of this submission

This submission is a **formalization** contribution. The mathematical answer
already exists in the literature ([Li25]) and the JSP catalogue records this
problem as solved; accordingly this repository claims the Lean-formalization
role only.

The formalized statement is the yes/no answer to the catalogue question, so the
submission is a **complete** answer to the problem as recorded — not a partial
result.

---

## 8. Verification status

Observed locally, from a clean checkout of this repository:

| check | result |
|---|---|
| `lake build` | success, 8707 jobs |
| placeholder scan | no `sorry` / `admit` / `native_decide` / `axiom` / `opaque` |
| `#print axioms Erdos834.erdos_834.parts.ii` | `[propext, Classical.choice, Quot.sound]` |
| statement correspondence vs pinned `challenge/Erdos834.lean` | MATCH |

The full 40-character commit SHA of the submitted revision is recorded in the
award claim rather than in this file, so that the README does not have to
predict the hash of the commit that contains it.

Machine: Apple Silicon (arm64), macOS; Lean `v4.33.1`; build of `Erdos834`
takes about 90 seconds once Mathlib oleans are cached.
