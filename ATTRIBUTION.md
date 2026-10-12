# Attribution and Provenance

This document records the mathematical origins, upstream software dependencies,
authorship, and AI tooling disclosure for the Lean 4 formalization of
**JSP-000690** (Erdős Problem 834, chromatic formulation).

---

## 1. Mathematical Problem and Origin

* **Problem Identification:** Erdős Problem 834 ([erdosproblems.com/834](https://www.erdosproblems.com/834)),
  catalogued in the Justin Sun Prize problem database as **JSP-000690**.
* **Original Formulation & Chronology:**
  - Posed by Paul Erdős and László Lovász.
  - The Justin Sun Prize catalogue records the date proposed as "No later than 1974 (bibliographic evidence)" / "About 52 years (since 1974)".
  - The problem page cites `[Er74d, p. 282]`. Its
    [bibliography entry](https://www.erdosproblems.com/bibs/Er74d) identifies
    P. Erdős, *Unsolved Problems* (1974), pp. 278–297.
    The original printed page itself was not independently inspected.
* **Dual Readings of "3-Critical":**
  The original formulation left the definition of "3-critical" open, resulting in two non-equivalent readings in the literature:
  1. *Transversal Criticality:* Criticality with respect to the transversal number ($\tau(H)=3$ and $\tau(H-e)=2$ for all $e \in H$). Li (arXiv:2512.24850) shows that any such 3-uniform hypergraph has $\delta(H) \le 6$, answering negatively.
  2. *Chromatic Criticality:* Criticality with respect to weak vertex-colouring ($\chi(H)=3$ and deleting any edge or any vertex yields a 2-colourable hypergraph).
  The Justin Sun Prize problem JSP-000690 adopts this chromatic reading, which Ruiliang Li (2025) resolved affirmatively via the explicit 9-vertex witness formalized here.

---

## 2. Mathematical Solver Attribution

* **Solver:** **Ruiliang Li** (李睿良)
* **Affiliation:** Department of Mathematical Sciences, Tsinghua University, Beijing 100084, China
* **Reference:**
  > Ruiliang Li, *On an Erdős–Lovász problem: 3-critical 3-graphs of minimum degree 7*,
  > arXiv:2512.24850 [cs.DM] (December 2025).
* **Specific Witness:** Theorem 4.1, display (5) of Li (2025) provides an
  explicit 9-vertex, 22-edge 3-uniform hypergraph $H$ with minimum degree
  $\delta(H) = 7$ that is 3-chromatic-critical.
* **Attribution Boundary:** All credit for solving the mathematical problem
  belongs to Ruiliang Li. This repository claims **no mathematical originality**
  and exclusively claims the **Lean 4 formalization contributor role**.

---

## 3. Upstream Specification and Definitions

Portions of this codebase adapt specifications and definitions from the
`google-deepmind/formal-conjectures` repository:

* **Upstream Project:** [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
* **License:** Apache License, Version 2.0 (Copyright 2026 The Formal Conjectures Authors)
* **Upstream Commit SHA:** `2067d8bb82058f40ccbd20a14fb94502434ea9eb`
* **Reference Challenge Statement:**
  - File: `FormalConjectures/ErdosProblems/834.lean`
  - Local vendored copy: `challenge/Erdos834.lean`
  - SHA256: `626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f`
  - The theorem statement in `Erdos834.lean` corresponds to declaration
    `erdos_834.parts.ii` in that specification.
* **Ported Hypergraph Definitions:**
  - Source file: `FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean`
    (SHA256: `0823fba654c8fd849c821338e6624aefac6935a92836523dde9eb6524874949a`)
  - Ported symbols: `Finset.IsUniform`, `Finset.IsProperHypergraphColoring`,
    `Finset.HypergraphColorable`, `Finset.HasHypergraphChromaticNumber`,
    and `Finset.hypergraphDegree`.
  - Modification Notice: In `Erdos834.lean`, computable `Decidable` instances
    were added to support exhaustive finite evaluation by the Lean kernel
    via `decide`.

---

## 4. Formalization Authorship and AI Disclosure

* **Formalization Submitter:** GitHub account [`@a985783`](https://github.com/a985783), selected by the account holder.
  Real name is unconfirmed by the account holder and is deliberately omitted to
  avoid fabrication.
* **AI Assistance Disclosure:**
  In accordance with transparent disclosure standards:
  - Lean 4 proof automation, structuring of decidability instances for kernel
    reduction (`decide`), and the assembly of the finite certificate were
    developed with the assistance of Oh My Pi (OMP) AI coding tools.
  - The transitive axiom audit harness (`scripts/audit_axiom.py`) and statement
    correspondence harness (`scripts/check_statement_match.py`) were developed
    with OMP AI assistance.
  - All mathematical statements and proofs are independently checked and verified
    by the official Lean 4.33.1 kernel without `native_decide` or unverified axioms.

---

## 5. Scope, Priority, and Non-Endorsement Disclaimers

* **Intended Submission Role:** Formalization contributor only, not mathematical
  solver. This is a local preparation, not a submitted award claim.
* **Publication Status:** The account holder authorized the public proof repository
  [`a985783/jsp-000690`](https://github.com/a985783/jsp-000690) and a catalog-reference
  PR. No award claim, identity-verification email, or payment details are submitted.
* **Priority Due Diligence vs. Official Acceptance:** Any internal review or
  audit of existing pull requests on `TheJustinSunPrize/awards` represents
  independent due diligence to understand existing public submissions.
  Neither pull request counts nor submission dates constitute a guarantee of
  priority, eligibility, or acceptance. Final determination of priority and award
  eligibility rests exclusively with the Justin Sun Prize Evaluation Committee.
