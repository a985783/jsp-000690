import Mathlib

open scoped Finset

syntax "answer(" term ")" : term
macro_rules
  | `(answer($t)) => `($t)

/-!
### Ported definitions from FormalConjecturesForMathlib/Combinatorics/Hypergraph/Finite.lean
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

namespace Finset

variable {V : Type*} [DecidableEq V]

/-- Every edge has exactly `r` vertices. -/
def IsUniform (H : Finset (Finset V)) (r : ℕ) : Prop := ∀ e ∈ H, e.card = r

instance (H : Finset (Finset V)) (r : ℕ) : Decidable (H.IsUniform r) :=
  decidableDforallFinset

/-- A weak proper coloring has no monochromatic edge. -/
def IsProperHypergraphColoring (H : Finset (Finset V)) {C : Type*} (c : V → C) : Prop :=
  ∀ e ∈ H, ∃ x ∈ e, ∃ y ∈ e, c x ≠ c y

instance (H : Finset (Finset V)) {C : Type*} [DecidableEq C] (c : V → C) :
    Decidable (H.IsProperHypergraphColoring c) :=
  decidableDforallFinset

/-- The edge family admits a weak proper coloring with `k` colors. -/
def HypergraphColorable (H : Finset (Finset V)) (k : ℕ) : Prop :=
  ∃ c : V → Fin k, H.IsProperHypergraphColoring c

instance [Fintype V] (H : Finset (Finset V)) (k : ℕ) :
    Decidable (H.HypergraphColorable k) :=
  Fintype.decidableExistsFintype

instance [Fintype V] (H : Finset (Finset V)) :
    DecidablePred (fun j => ¬ H.HypergraphColorable j) :=
  fun _ => inferInstance

/-- The weak chromatic number is exactly `k`. -/
def HasHypergraphChromaticNumber (H : Finset (Finset V)) (k : ℕ) : Prop :=
  H.HypergraphColorable k ∧ ∀ j < k, ¬ H.HypergraphColorable j

/-- The number of hyperedges containing a vertex. -/
def hypergraphDegree (H : Finset (Finset V)) (v : V) : ℕ := #{e ∈ H | v ∈ e}

end Finset

namespace Erdos834

open Filter Asymptotics

/--
The 22-edge 3-uniform hypergraph on 9 vertices from [Li25], display (5).
Vertices are indexed 0..8 (corresponding to 1..9 in the paper).
-/
def H : Finset (Finset (Fin 9)) :=
  { {0, 1, 2}, {0, 1, 8}, {0, 2, 7}, {0, 3, 5}, {0, 3, 7}, {0, 3, 8},
    {0, 4, 6}, {0, 4, 7}, {0, 4, 8}, {0, 5, 6},
    {1, 2, 5}, {1, 2, 6}, {1, 3, 8}, {1, 4, 8}, {1, 5, 6},
    {2, 3, 7}, {2, 4, 7}, {2, 5, 6},
    {3, 5, 7}, {3, 5, 8},
    {4, 6, 7}, {4, 6, 8} }

/-- Proper 3-coloring of H witnessing HypergraphColorable 3. -/
def c3 : Fin 9 → Fin 3
  | 0 => 0
  | 1 => 0
  | 3 => 0
  | 4 => 0
  | 2 => 1
  | 5 => 1
  | 7 => 1
  | 8 => 1
  | 6 => 2

set_option maxRecDepth 200000
set_option maxHeartbeats 4000000

theorem H_uniform : H.IsUniform 3 := by
  decide

theorem H_degrees : ∀ v : Fin 9, 7 ≤ H.hypergraphDegree v := by
  decide

theorem H_colorable_3 : H.HypergraphColorable 3 :=
  ⟨c3, by decide⟩

theorem H_not_colorable_lt_3 : ∀ j < 3, ¬ H.HypergraphColorable j := by
  decide

theorem H_chromatic : H.HasHypergraphChromaticNumber 3 :=
  ⟨H_colorable_3, H_not_colorable_lt_3⟩

theorem H_crit_edges : ∀ e ∈ H, (H.erase e).HypergraphColorable 2 := by
  decide

theorem H_crit_verts : ∀ v : Fin 9, (H.filter (fun e ↦ v ∉ e)).HypergraphColorable 2 := by
  decide

/--
Does there exist a $3$-critical $3$-uniform hypergraph with minimum degree at least $7$,
where criticality means that deleting any edge or vertex reduces chromatic number $3$ to $2$?

In the second formulation, the chromatic notion of criticality, Li [Li25] provides an
explicit $3$-critical $3$-uniform hypergraph on $9$ vertices with minimum degree $7$.
-/
theorem erdos_834.parts.ii :
    answer(True) ↔ ∃ (n : ℕ) (H : Finset (Finset (Fin n))),
    H.IsUniform 3 ∧ H.HasHypergraphChromaticNumber 3 ∧
      (∀ e ∈ H, (H.erase e).HypergraphColorable 2) ∧
      (∀ v : Fin n, (H.filter (fun e ↦ v ∉ e)).HypergraphColorable 2) ∧
      ∀ v : Fin n, 7 ≤ H.hypergraphDegree v := by
  constructor
  · intro _
    exact ⟨9, H, H_uniform, H_chromatic, H_crit_edges, H_crit_verts, H_degrees⟩
  · intro _
    trivial

end Erdos834
