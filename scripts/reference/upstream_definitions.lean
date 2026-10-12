/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

/-!
# Upstream Reference Definitions for Erdős Problem 834

Provenance:
- Repository: https://github.com/google-deepmind/formal-conjectures
- Commit: 2067d8bb82058f40ccbd20a14fb94502434ea9eb
- Source File: FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean
- Source File SHA256: 0823fba654c8fd849c821338e6624aefac6935a92836523dde9eb6524874949a

This file records the exact upstream definitions transplanted into `Erdos834.lean`.
-/

namespace Finset

variable {V : Type*} [DecidableEq V]

/-- Every edge has exactly `r` vertices. -/
def IsUniform (H : Finset (Finset V)) (r : ℕ) : Prop := ∀ e ∈ H, e.card = r

/-- A weak proper coloring has no monochromatic edge. -/
def IsProperHypergraphColoring (H : Finset (Finset V)) {C : Type*} (c : V → C) : Prop :=
  ∀ e ∈ H, ∃ x ∈ e, ∃ y ∈ e, c x ≠ c y

/-- The edge family admits a weak proper coloring with `k` colors. -/
def HypergraphColorable (H : Finset (Finset V)) (k : ℕ) : Prop :=
  ∃ c : V → Fin k, H.IsProperHypergraphColoring c

/-- The weak chromatic number is exactly `k`. -/
def HasHypergraphChromaticNumber (H : Finset (Finset V)) (k : ℕ) : Prop :=
  H.HypergraphColorable k ∧ ∀ j < k, ¬ H.HypergraphColorable j

/-- The number of hyperedges containing a vertex. -/
def hypergraphDegree (H : Finset (Finset V)) (v : V) : ℕ := #{e ∈ H | v ∈ e}

end Finset
