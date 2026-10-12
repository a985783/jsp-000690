# SUBMISSION — JSP-000690 (Erdős #834), Lean formalization reference

**Historical draft, not the final PR body.** The account holder subsequently
authorized publication under `a985783` and a catalog-reference PR.
The final submitted body is available in
[PR #5023](https://github.com/TheJustinSunPrize/awards/pull/5023);
its selected proof revision is `2378a9cc1f2c5aa62bcd233288c64036d96bc493`.
The fill-in fields below belong to the historical draft, not the submitted PR.
`PRIORITY-AUDIT.md` §1 and §7: a **plausible earlier same-question public source**
exists — a file was already present in a public repository at a commit whose
committer date is 2026-08-17, and by September two open catalog PRs cited it with
a **fixed 40-character SHA**. Because that earlier source has not been built,
audited, or accepted by the maintainers (it is a *static* finding only), this
draft does **not** assert that it is the accepted source or that our submission
*would* lose priority; it asserts that the situation is high-risk and not
supported by official review. **Submission is therefore not recommended** unless
the user overrides. This draft is provided only so that a compliant PR body exists
in that case, and it contains no claim of originality or priority.

The text below follows the official PR template
`.github/PULL_REQUEST_TEMPLATE.md` at awards `main`
`16877004910734cecca83cc5af0fec2f5a4125b3` (blob `e2c02f71b7e0d0254217c3bf67605c30f8e56a56`),
with the template's own section order and wording. Placeholders that only the
user can supply are marked `[[FILL: …]]` and listed in §F of the fill-in sheet.

---

## Draft PR body (copy the block below into the PR description)

---

## Submission type

- [ ] Mathematical solver information
- [x] Lean proof or formalization author information

## Problem

- Problem ID(s): JSP-000690
- Original problem source and exact location (page, section or problem number):
  Erdős Problem #834, https://www.erdosproblems.com/834 — original print source
  `[Er74d, p.282]`: P. Erdős, *Unsolved Problems* (1974), pp. 278–297,
  specifically p. 282, as identified by the
  [problem page bibliography](https://www.erdosproblems.com/bibs/Er74d).
  The original printed page has not been independently inspected. The problem page gives two
  non-equivalent readings of "3-critical"; the JSP-000690 entry uses the
  **chromatic** reading ("three-chromatic-critical"), and this submission targets
  only that reading.
- Current entry and proposed change: in `problems/catalog-0601-0700.md`
  (JSP-000690, lines 1531–1547 at awards `main`
  `16877004910734cecca83cc5af0fec2f5a4125b3`), the current text is
  `Current status | Solved`, `Lean proof | No`, `Eligible to claim | No`, with
  `[Li25]` in `Publication details`. **Proposed change:** set `Lean proof` to
  `Yes` with the pinned source below, and add an `Attribution basis` row. No other
  field is changed: `Current status`, `Eligible to claim`, `Publication details`,
  `Historical bounty` and `Elapsed years` are left exactly as they stand, and the
  index reconciliation is left to maintainers.
- Related issue, if any: none opened by the submitter. Prior and parallel
  submissions on this problem are listed under "Related PRs", below.
- Related PRs and how this contribution differs, including any issue found in an
  existing submission and supporting evidence:
  * `plby/lean-proofs` — the same catalogue statement (and, in fact, also the
    transversal reading) is also addressed there at
    `src/latest/ErdosProblems/Erdos834.lean`; a file is present at a commit whose
    committer date is **2026-08-17** (`da153ecd8a4f3bee42edca0c596e313bb834fb34`,
    static inspection only; not built or verified by the submitter), and open
    catalog PRs #1383 and #4071 cite that source with a fixed full SHA.
    **This submission makes no claim to be earlier, first, or independent
    priority over it, and it does not displace it.** The submitter's work
    post-dates that commit date.
  * JSP items for the same problem: issues #15, #126, #157, #697, #704, #880,
    #882, #1023, #1066, #1113, #1292, #1610, #1614, #1868, #2044, #2186; PRs
    #21, #35, #39, #427, #717, #737, #747, #794, #823, #842, #845, #879, #1097,
    #1099, #1152, #1383, #1609, #1613, #1895, #1947, #2007, #2108, #2185, #2545,
    #2878, #3828, #4071, #4233, #4564, #4650, #4703. The submitter is not the
    author of any of these and makes no priority claim over them.
  * Difference: this is an **independent re-formalization** of Li's published
    witness, not a migration, mirror, or copy of any of the above; it reuses no
    proof text from any of them. Its only purpose in the record would be as an
    additional independently checkable verification reference. If the submitter
    is told that an earlier or existing source already covers this contribution,
    the submitter accepts that outcome and does not dispute it.
- For solver/publication updates: not applicable — this is not a solver
  submission; the mathematical solution is Li's and is already recorded in the
  catalogue's `Publication details`.

## Formal statement

- Complete mathematical solution (provided earlier or in this PR), public proof or
  publication, relevant theorem/pages, version or date:
  R. Li, *On an Erdős–Lovász problem: 3-critical 3-graphs of minimum degree 7*,
  arXiv:2512.24850v1, first submitted **2025-12-31T13:19:18Z**, updated
  2026-10-12. Relevant locations, verified against the PDF text:
  - **§1, Theorem 1.2** (Chromatic interpretation): *"There exists a 3-uniform
    hypergraph H that is critically 3-chromatic (under weak colourings) and
    satisfies δ(H) ≥ 7. In fact, there is such an H on 9 vertices with δ(H) = 7."*
    (PDF p.2.)
  - **§4.1, Theorem 4.1 and display (5)** (PDF p.7): the explicit 22-edge,
    9-vertex 3-graph on `V(H) = [9]`.
  - **§4.2, Lemma 4.2** (degrees): `d_H(1) = 10` and `d_H(v) = 7` for
    `v ∈ {2,…,9}`, hence `δ(H) = 7`.
  - **§4.3, Lemma 4.3** (`H` is not 2-colourable), **Lemma 4.4** (`H` admits a
    proper 3-colouring, so χ(H) = 3).
  - **Propositions 4.5–4.6** (edge- and vertex-criticality), with certificates in
    **Appendix B**, machine-readable edge list in **Appendix A**, and a
    brute-force checker in **Appendix C**; the proof of Theorem 1.2 is at PDF p.9.
  - The paper's **transversal** result (§1, Theorem 1.1: `|E(H)| ≤ 10`, hence
    `δ(H) ≤ 6`, sharp at the complete 3-graph `K₅⁽³⁾`) is a *different* question
    and is **not** part of this submission.
- Mathematical review reference or current review status: the catalogue already
  records this problem as `Solved` with `[Li25]` in `Publication details`; the
  Erdős-problems page states that under the chromatic reading "Li provides an
  explicit 3-critical 3-uniform hypergraph on 9 vertices with minimum degree 7".
  The submitter asserts **no** independent mathematical review and **no** organizer
  acceptance.
- Formal statement location, pinned to a full commit SHA: the frozen statement is
  vendored, hash-pinned, in this repository at
  `challenge/Erdos834.lean` (sha256
  `626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f`), which is
  **byte-identical** to upstream
  `google-deepmind/formal-conjectures/FormalConjectures/ErdosProblems/834.lean`
  (verified by fetch+`diff` on 2026-10-12; upstream `main` HEAD
  `86daeae6fa80d23eb32bb610aa499ce88180c5a5`).
  [[FILL: public URL of this repository, branch, and full 40-character commit SHA
  — see §F]]
- Fully qualified target theorem name: `Erdos834.erdos_834.parts.ii`
  (frozen statement reproduced verbatim, with its upstream comment):

  ```lean
  @[category research solved, AMS 5]
  theorem erdos_834.parts.ii :
      answer(True) ↔ ∃ (n : ℕ) (H : Finset (Finset (Fin n))),
      H.IsUniform 3 ∧ H.HasHypergraphChromaticNumber 3 ∧
        (∀ e ∈ H, (H.erase e).HypergraphColorable 2) ∧
        (∀ v : Fin n, (H.filter (fun e ↦ v ∉ e)).HypergraphColorable 2) ∧
        ∀ v : Fin n, 7 ≤ H.hypergraphDegree v
  ```

- Statement origin (maintainer-approved reference and version, or proposed
  statement requiring review): the statement is **not** authored here. It is the
  frozen public statement of `formal-conjectures` (linked and hash-pinned above),
  whose own reference is `R. Li, arXiv:2512.24850`. Any statement-to-prose
  correspondence question is for maintainers.
- Correspondence to the original problem: definitions, assumptions, quantifiers,
  conclusion and all required cases; explain any differences from an approved
  statement.
  - Object: `H : Finset (Finset (Fin n))` is a finite simple hypergraph (no
    repeated edges); `H.IsUniform 3` = every edge has exactly 3 vertices.
    Colouring is the **weak** (no-monochromatic-edge) notion:
    `IsProperHypergraphColoring H c := ∀ e ∈ H, ∃ x ∈ e, ∃ y ∈ e, c x ≠ c y`, and
    `HypergraphColorable H k := ∃ c : V → Fin k, IsProperHypergraphColoring H c`.
    `HasHypergraphChromaticNumber H 3` = `HypergraphColorable H 3 ∧ ∀ j < 3,
    ¬ HypergraphColorable H j`. `hypergraphDegree H v` = number of edges
    containing `v`.
  - Witness: `n = 9` and `H = Erdos834.H`, a 22-edge 3-uniform hypergraph.
    Degrees: `(10,7,7,7,7,7,7,7,7)`, i.e. minimum degree exactly 7.
  - Required cases discharged: uniformity (22/22 edges size 3); chromatic number
    exactly 3 (an explicit 3-colouring `Erdos834.c3`, plus exhaustive exclusion of
    all 1/2-colourings); criticality under deletion of **any single edge**
    (22 cases) and of **any single vertex** (9 cases), each 2-colourable.
  - Scope differences: `parts.i`, the **transversal** reading of the same Erdős
    item (`answer(False)`), is deliberately **not** formalized here. Only the
    chromatic reading named in the JSP-000690 entry is claimed. The witness matches
    Li25 display (5) exactly (checked by set comparison after the re-indexing
    `i ↦ i+1`; degree vector identical).

## Proof submission

For Lean contributions only. Use the original repository containing your
contribution, owned by your submitting account or an organization.

```json
[
  {
    "repository": "[[FILL: https://github.com/a985783/jsp-000690]]",
    "branch": "main",
    "commit": "[[FILL: full 40-character commit SHA of the submitted revision]]"
  }
]
```

Local preparation only: no remote is configured and no publication is authorized.
The final local SHA is supplied with the delivery report rather than embedded
in its own commit. If publication is later explicitly approved, fill the public
repository URL and selected SHA; do not send this draft with unfilled fields.

- Proof file at the selected commit and fully qualified theorem name:
  `Erdos834.lean`, theorem `Erdos834.erdos_834.parts.ii`; supporting component
  lemmas `Erdos834.H_uniform`, `H_degrees`, `H_colorable_3`,
  `H_not_colorable_lt_3`, `H_chromatic`, `H_crit_edges`, `H_crit_verts`.
  `Erdos834.lean` sha256 (local) =
  `c92f311b73d80dfd781a70eb90c0e944ebaf1ebdf040380f9f280880335f7204`.
- How the proof establishes the formal statement above, including any separate
  verification entry:
  - `answer(...)` is expanded by a one-line local macro to its argument, matching
    upstream's `answer` term elaborator semantics, so the frozen statement reduces
    to `True ↔ (∃ …)`. The proof's `constructor` branch produces the witness
    (`⟨9, H, H_uniform, H_chromatic, H_crit_edges, H_crit_verts, H_degrees⟩`) and
    the reverse direction is `trivial`.
  - Every finite claim is closed by `decide` (**kernel-checked reduction**);
    `native_decide` is **not** used anywhere, so no compiler-trust axiom
    (`Lean.ofReduceBool`) enters the proof.
  - `scripts/check_statement_match.py` machine-extracts the statement text from the
    hash-pinned `challenge/Erdos834.lean` (it never retypes it) and has Lean
    type-check this proof's declaration against exactly that text. The full
    statement-correspondence output is reproduced under "Reproduction", below.
  - A separate, independent verification entry is **not** supplied; the checks
    below are submitter-run only.

## Reproduction

For Lean contributions only.

- Exact Lean version and `lean-toolchain` path:
  `leanprover/lean4:v4.33.1` (file `lean-toolchain` at the submission root).
- Pinned dependencies (including mathlib, if used) and manifest path:
  `leanprover-community/mathlib4` at
  `0df444a360eaa60ab8c11dca51a86af692955474`, recorded in `lake-manifest.json`
  (and repeated in `lakefile.toml` as the Mathlib `require`).
- Build instructions pinned to the selected commit:
  ```sh
  git clone [[FILL: repository URL]]
  cd [[FILL: repo dir]]
  git checkout [[FILL: full 40-character commit SHA]]
  ```
- Commands for setup, clean build and checking each target theorem; include a
  separate statement-to-proof check if needed:
  ```sh
  lake exe cache get
  lake clean jsp000690
  lake build
  python3 scripts/scan_placeholders.py Erdos834.lean
  python3 scripts/check_definition_match.py
  python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
  python3 scripts/check_statement_match.py
  ```
  Or, in one step:
  ```sh
  bash scripts/reproduce.sh
  ```
  The script strips comments and strings before scanning our proof, checks
  transplanted definitions by kernel equality, and fails on any rejected check.

  Observed statement-correspondence output (local, 2026-10-12):
  ```
  $ python3 scripts/check_statement_match.py
  challenge file : Erdos834.lean  sha256=626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f
  challenge stmt : answer(True) ↔ ∃ (n : ℕ) (H : Finset (Finset (Fin n))), H.IsUniform 3 ∧ …
  our proof      : @Erdos834.erdos_834.parts.ii
  RESULT: MATCH — our proof typechecks at the frozen challenge statement.
  ```

- Axiom audit command and output for each target (for example,
  `#print axioms Fully.Qualified.theoremName`):
  ```sh
  python3 scripts/audit_axiom.py --theorem Erdos834.erdos_834.parts.ii
  ```
  Observed output (local, 2026-10-12):
  ```
  [raw] 'Erdos834.erdos_834.parts.ii' depends on axioms: [propext, Classical.choice, Quot.sound]
  === AUDIT RESULT ===
  target   : Erdos834.erdos_834.parts.ii
  verdict  : ACCEPTED_STANDARD_AXIOMS
  axioms   : ['propext', 'Classical.choice', 'Quot.sound']
  ```
  Dependencies reported are exactly the three standard Lean foundations
  (`propext`, `Classical.choice`, `Quot.sound`). The auditor is **fail-closed**:
  it refuses any output it cannot unambiguously parse, any `sorryAx`, and any
  declaration that does not bind to the requested theorem identifier.
  No other declarations are claimed for audit purposes; if maintainers wish each
  component lemma audited individually, the submitter will provide the outputs.

## Pre-submission Lean verification (optional)

We recommend the `lean-verify` skill; reports and logs are optional here.

- Method/tool and version, if available: the optional `lean-verify` skill was
  **not** run. Verification supplied here is the submitter's own script suite
  (`scripts/reproduce.sh`, `scripts/audit_axiom.py`,
  `scripts/check_statement_match.py`) run locally on macOS/arm64.
- Checked repository and full commit SHA; identify any difference from the
  submitted version: same commit as submitted —
  [[FILL: full 40-character commit SHA]] — no differences.
- Verification date, actual conclusion and limitations: 2026-10-12. Conclusion:
  clean build of `Erdos834`; no `sorry`/`admit`/`native_decide`/`axiom`/`opaque`
  in `Erdos834.lean`; transitive axiom report `[propext, Classical.choice,
  Quot.sound]`; statement correspondence `MATCH` against the hash-pinned challenge
  file. Limitations: this is **submitter-run**, not independent human review; the
  `challenge/Erdos834.lean` file is a vendored copy used only for correspondence
  checking, and the upstream statement is frozen in `formal-conjectures`, not here.
- Summary of statement correspondence, coverage, Lean checks and trust
  dependencies: the formalized statement is the chromatic existence claim of
  JSP-000690 / Erdős #834; coverage is the explicit witness plus all edge/vertex
  deletions; trust dependencies are the three standard axioms above with no
  compiler-trust axiom.
- Report in this PR or external report/log/evidence links, if available:
  [[FILL: optional — link to a CI run for the exact SHA, if one is produced]]

## Attribution

- Mathematical solver(s) and contribution, if applicable: **Ruiliang Li** — sole
  author of arXiv:2512.24850, which resolves the Erdős–Lovász question under both
  readings; the chromatic existence answer and the explicit 9-vertex,
  22-edge construction are Li's (Theorem 1.2; Theorem 4.1 and display (5)).
  The submitter claims **no** mathematical credit.
- Lean formalization contributor account, if applicable: **`a985783`** —
  the submitter's GitHub account — prepared this independent Lean 4 formalization
  of the chromatic reading in the repository named under "Proof submission".
  **AI assistance is disclosed:** this formalization was produced with the help of
  an AI coding agent (OpenAI Codex / large-language-model assistance) under the
  submitter's direction; the submitter does not claim sole manual authorship of
  every proof step. [[FILL: the submitter's real name — see §F; the legal name is
  not stated here and must not be invented]]
- Independent verifier(s), if any: **none claimed**. The checks in this draft are
  submitter-run only; no independent human verification is asserted.
- Public authorship evidence; for an organization repository, link verifiable
  evidence connecting your account to the claimed proof files/theorems (such as
  merged PRs, attributable changes or project authorship records). Explain
  mismatches between authors, accounts and proposed credits:
  the intended repository owner and submitting account is `a985783`.
  Local commits currently use `omp <omp@localhost>`, not the account holder's
  verified identity. No organisation repository is involved. Potential
  mismatches, which are for maintainers to weigh:
  * the underlying mathematical result and witness are Li's, not the submitter's;
  * an **earlier** same-question public source is known to exist
    (`plby/lean-proofs`, file present at a commit whose committer date is
    2026-08-17; statically inspected only), and the submitter makes no priority
    claim over it;
  * this work was produced with AI assistance, so "authorship" here means
    direction and curation by the submitter, not manual line-by-line authorship.

## Submission checklist

- [x] I changed only the relevant catalog's solver attribution, Lean proof
  information or supporting sources and supplied the applicable evidence.
- [x] The submitted result fully solves the original problem. Any submitted Lean
  proof is complete at the specified commit, with no `sorry`, `admit` or added
  unproved assumptions replacing proof steps.
- [x] For Lean: I have linked the complete mathematical solution and its proof or
  publication evidence provided earlier, or supplied them in this PR, and
  identified the mathematical solver and Lean formalization author separately.
- [x] For Lean: I am claiming my own contribution in the original personal or
  organization repository, with verifiable contribution evidence for an
  organization repository; the selected commit is in the named branch, and I
  supplied statement correspondence, reproduction commands and axiom audit
  results.
- [x] This PR contains no Lean source files, archives, binaries, vendored
  dependencies or private identity/contact/payment information.

---

## Fill-in sheet (complete before any submission)

| # | placeholder | where | what is needed |
|---|---|---|---|
| F1 | `[[FILL: repository URL]]` | Proof submission / Reproduction | public GitHub repo under the `a985783` account containing this exact commit |
| F2 | `[[FILL: branch]]` | Proof submission | the branch the commit lives on |
| F3 | `[[FILL: full 40-character commit SHA]]` | several places | final local SHA supplied in the delivery report; publish and select that exact revision only after explicit approval |
| F4 | `[[FILL: the submitter's real name]]` | Attribution | legal name for the Lean formalization credit. **Unknown — must be confirmed by the user. Do not fabricate.** |
| F5 | `[[FILL: optional CI link]]` | Pre-submission verification | optional link to a CI run for the exact SHA |

## Not included, by design

* **No claim of originality, firstness, or priority.** The rules explicitly state
  that "PR opening time does not determine priority" and that the earliest
  *selected commit* in an accepted original repository wins; an earlier
  same-question public source is known to exist (see `PRIORITY-AUDIT.md` §1).
  This draft neither asserts that the earlier source will be accepted nor disputes
  it; it merely makes no competing priority claim.
* **No solver role claimed.** The mathematical solution is Li's.
* **No statement change proposed.** `Current status`, `Eligible to claim`,
  `Publication details`, `Historical bounty`, `Elapsed years` are untouched.
* **No proof source is intended for the awards repository.** Only the catalog rows
  would change; the Lean source stays in the external repository, as the
  maintainers require.
* **No real name is asserted** anywhere in the draft; the one place it is needed
  (Attribution) is left to the user.
