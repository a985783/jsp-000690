# PRIORITY-AUDIT — JSP-000690 (Erdős #834)

**Local, pre-submission audit. No external action was taken: nothing was pushed,
posted, commented on, or e-mailed. This file and `SUBMISSION.md` are the only
files created.**

* Audit date: 2026-10-12 (UTC).
* Auditor: local worker agent preparing a submission for GitHub account `qingsongcui`.
* Evidence tooling: `gh api` (authenticated as `qingsongcui`), `git`, `curl`.
* Machine snapshots of every artefact quoted below are cached under
  `delivery-jsp-000690/.audit/` (not part of the submission).

---

## 1. Verdict (short)

> **Current recommendation: DO NOT SUBMIT JSP-000690 as a priority
> contribution — high risk, and not supported by official review.**

This is a recommendation under uncertainty, not a settled fact. It rests on the
following **static** findings:

1. An **earlier, same-question, publicly hosted complete Lean source** exists
   (`plby/lean-proofs`, file present by commit dated 2026-08-17), and by
   September a JSP PR already cited it with a **fixed 40-character SHA**
   (`8822f7ddef30…`, PRs #1383/#4071).
2. Our own work is dated 2026-10-12 and formalizes the *same published witness*
   (Li25 display (5)) already covered by that earlier source, so any priority
   position rests entirely on a maintainer's discretionary interpretation.
3. **No source has been accepted or recorded**: at the pinned awards `main`,
   JSP-000690 still reads `Lean proof | No`, and it is absent from the candidate
   and award registers. There is therefore no official adjudication either way.

| item | value | how established |
|---|---|---|
| Earlier public source | `plby/lean-proofs`, file `src/latest/ErdosProblems/Erdos834.lean` | static inspection of the blob via `git show` |
| Commit carrying that file | `da153ecd8a4f3bee42edca0c596e313bb834fb34`, **committer date 2026-08-17T18:05:20Z** | `gh api …/commits?path=…` |
| Content at that commit | complete-looking, **0 occurrences of `sorry`**, addresses **both** readings (chromatic + transversal) | `grep -c sorry` on the extracted blob |
| Latest commit of the same file | `0054e9e8108f574d2c17b1859c2a2f57256491f9` (2026-08-31T19:34:02Z) | commit history |
| First JSP submission for this problem | PR #21 / issue #15, **2026-09-16T09:32–09:57Z** | `gh api` search |
| Our proof | `delivery-jsp-000690` commit `57b1685…`, **2026-10-12** | local `git log` |
| Official priority rule | priority = **earliest selected commit in an accepted original repository**; PR-open time is explicitly *not* decisive | pinned `docs/award-process.md` |

**What is *not* claimed here.** The earlier proof was **not** built and no
`#print axioms` audit was run on it in this audit; therefore it is **not**
described as "formally verified" or "accepted". Its committer timestamp is
**evidence that the source existed by 2026-08-17**, not proof of when it was
independently published or completed — and the pinned rules themselves state
that *"commit timestamps alone are insufficient evidence of when a proof was
completed"*. Consequently this file **does not** assert that `plby/lean-proofs`
*would* be the accepted source, nor that a submission *cannot* establish priority;
those are maintainer determinations. What it does assert is that a **plausible,
rules-relevant, earlier public source** exists, that it is cited by open PRs, that
the rules bar us from registering someone else's proof, and that submitting
therefore carries **high risk of a duplicate/non-priority outcome** — which is why
submission is not recommended unless the user overrides.

The complete submission draft requested by the assignment is nevertheless
provided at `SUBMISSION.md`, ready to send **only if** the user overrides this
recommendation. It contains no claim of originality or priority.

### 1.1 Static review vs. measured verification (what was actually done)

Nothing in this audit was **built, compiled, or axiom-audited** except our own
repository's own artefacts (and even those only by reading their scripts, not by
re-running `lake build`). Concretely:

| claim in this file | evidence class | what was **not** done |
|---|---|---|
| "an earlier same-question source exists, containing 0 `sorry`" | **static**: `git show` of the blob at a named commit + `grep -c sorry` + target-list read | **not built**; **no** `#print axioms` on it; **not** verified to compile |
| "committer date 2026-08-17" | **static metadata**: `gh api …/commits` field `.commit.committer.date` | **not** corroborated by independent public history; rules say timestamps alone are insufficient |
| "first JSP submission 2026-09-16" | **API metadata** from `search/issues` + per-item `created_at` | — |
| "no source recorded / no candidate / no award" | **static**: raw file reads at pinned SHA | — |
| "our proof passes audit at `[propext, Classical.choice, Quot.sound]`" | **README/reproduce-script recorded output only**; not re-run in this audit | **not re-run** here (assignment says main agent runs checks) |
| "our witness == Li25 display (5)" | **measured** (pure computation, no Lean): set comparison + degree count | — |

Where a statement depends on the earlier proof *compiling*, it is marked as an
open item (§9.6) rather than asserted.

---

## 2. Official-rules baseline (pinned to current `main`)

TheJustinSunPrize/awards `main` HEAD at audit time:

```
16877004910734cecca83cc5af0fec2f5a4125b3   (2026-10-08T10:25:49Z,
  "docs: record OpenAI complete results for 19 catalog problems (#4869)")
```

Every rule document below was fetched **at that SHA** from
`https://raw.githubusercontent.com/TheJustinSunPrize/awards/16877004910734cecca83cc5af0fec2f5a4125b3/<path>`:

| path | git blob SHA | sha256 (first 16) | key content used here |
|---|---|---|---|
| `CONTRIBUTING.md` | `9ce07d57dd690d91f6817fdc711f7225e0feddb2` | `4b8c5c7092ba99ed` | external solver/Lean submission rules; "do not register someone else's proof" |
| `.github/PULL_REQUEST_TEMPLATE.md` | `e2c02f71b7e0d0254217c3bf67605c30f8e56a56` | `2729a10a4485fa02` | required PR fields (the template used by `SUBMISSION.md`) |
| `docs/award-process.md` | `533399eea3c0d9a0b713c410363e5be24bdb5d7e` | `8e2cf839a809ac1d` | §"Lean formalization or both roles" — **priority definition**, 14-day review, challenge rules |
| `docs/attribution.md` | `4a36d6a4b557c064b397270bb0572c3a6dc19514` | `685540326df51110` | authorship/identity rules, "repository ownership alone does not establish authorship" |
| `docs/verification.md` | `e084805019f442f56fd74334cbfb1a13333023e2` | `a0d7294fedd10337` | optional `lean-verify` self-check guidance |
| `problems/catalog-0601-0700.md` | (at main SHA above) | — | current JSP-000690 record: `Lean proof | No` |

**Rule text quoted verbatim** (from `docs/award-process.md`, §"Lean formalization
or both roles", lines 88–105 of the pinned file):

> "After the mathematical solution has passed review, maintainers verify the Lean
> proof before comparing priority. Solver registration is not a prerequisite. If
> no formalization source is already recorded, the accepted submission becomes
> the earliest recorded source. If multiple submissions pass verification in the
> same review period, the earliest selected commit in the accepted original proof
> repositories takes priority. If a source is already recorded, a new submission
> replaces it on priority grounds only after verification establishes that the
> selected complete proof is earlier. … **PR opening time does not determine
> priority.** Maintainers check the selected commit's time and supporting public
> history when reviewing a priority claim. Commit timestamps alone are
> insufficient evidence of when a proof was completed … Supply independently
> checkable public history tying the selected proof version to the claimed date."

And from `CONTRIBUTING.md`, §"External solver and Lean submissions":

> "…Do not register someone else's proof, a mirror or a copy on their behalf."
> "**Only complete solutions to the original problem are accepted, whether
> mathematical or in Lean.** Special cases, intermediate lemmas, weaker results
> and conditional arguments relying on additional unproved assumptions do not
> qualify."
> "**A Lean submission without the mathematical solution and its supporting
> evidence is invalid and will not be accepted.**"

## 3. What the original problem is (exact source)

* Erdős Problem #834, https://www.erdosproblems.com/834 (page last edited
  2026-01-01; accessed 2026-10-12). Citation string recommended by the site:
  `T. F. Bloom, Erdős Problem #834, https://www.erdosproblems.com/834, accessed 2026-10-12`.
* Original print source given by the page: **`[Er74d, p.282]`**.
  The [site's bibliography endpoint](https://www.erdosproblems.com/bibs/Er74d)
  identifies **P. Erdős, *Unsolved Problems* (1974), pp. 278–297**.
  The specific location p. 282 comes from the problem page. The printed page
  itself was not independently inspected. An earlier draft incorrectly mixed
  this reference with a different 1975 paper; that citation has been removed.
* Page wording (verbatim):
  > "Does there exist a $3$-critical $3$-uniform hypergraph in which every vertex
  > has degree $\geq 7$? … A problem of Erdős and Lovász. They do not specify what
  > is meant by $3$-critical. One definition …: a hypergraph is $3$-critical if
  > there is a set of $3$ vertices which intersects every edge, but no such set of
  > size $2$, and yet for any edge $e$ there is a pair of vertices which intersects
  > every edge except $e$. … An alternative definition is that a hypergraph is
  > $3$-critical if it has chromatic number $3$, but its chromatic number becomes
  > $2$ after deleting any edge or vertex. In either case, this has been resolved
  > by Li [Li25]. In the first formulation, the transversal notion of criticality,
  > Li proves that a $3$-critical $3$-uniform hypergraph must have a vertex of
  > degree $\leq 6$. On the other hand, in the second formulation, the chromatic
  > notion of criticality, Li provides an explicit $3$-critical $3$-uniform
  > hypergraph on $9$ vertices with minimum degree $7$."

* **JSP-000690 catalog record** (`problems/catalog-0601-0700.md`, lines 1531–1547
  at the pinned main SHA) chooses the **second (chromatic)** formulation:

  | field | value |
  |---|---|
  | Problem description | *Is there a three-uniform, three-chromatic-critical hypergraph with minimum degree at least seven?* |
  | Current status | Solved |
  | Lean proof | **No** |
  | Eligible to claim | No |
  | Publication details | `[Li25] On an Erdős--Lovász problem: 3-critical 3-graphs of minimum degree 7 — arXiv:2512.24850 (2025)` |

* The catalog's own **frozen Lean statement** is vendored in this repository as
  `challenge/Erdos834.lean`.
  sha256 = `626258ec807262bd2a43bb6e6a923273fbdc85443e170fa703d5b33efc55583f`
  — **verified byte-identical** to upstream
  `google-deepmind/formal-conjectures` `FormalConjectures/ErdosProblems/834.lean`
  at that repo's `main` HEAD `86daeae6fa80d23eb32bb610aa499ce88180c5a5` (checked
  2026-10-12 by `curl` + `diff`, whole-file identical).
  The frozen file declares **both** readings: `erdos_834.parts.i` (transversal,
  `answer(False)`) and `erdos_834.parts.ii` (chromatic, `answer(True)`); both
  bodies are `sorry` upstream. Our submission targets **only `parts.ii`**.

### 3.1 Chromatic vs transversal — kept strictly separate

| | chromatic reading (`parts.ii`, our target) | transversal reading (`parts.i`) |
|---|---|---|
| criticality | delete any edge **or** vertex ⇒ χ drops 3 → 2 | τ(H)=3, τ(H−e)=2 ∀e |
| answer | **Yes** (existence) | **No** (impossible) |
| Li25 location | §1 Theorem 1.2; §4.1 Theorem 4.1 + display (5); Lemmas 4.2–4.4; Props 4.5–4.6; App. A (edge list), App. B (certificates), App. C (script) | §1 Theorem 1.1: \|E(H)\| ≤ 10 and δ(H) ≤ 6, sharp at K₅⁽³⁾ |
| in our proof | proved | **not** proved (out of scope) |
| in `plby/lean-proofs` | proved | **also** proved (`no_transversalThreeCritical_minDegreeSeven`, `completeThreeGraphFive_*`) |

All JSP submissions reviewed here are on the **chromatic** reading except an
explicit minority noted in §6.

## 4. Priority evidence — the key artefact

### 4.1 `plby/lean-proofs` (earlier public source, statically reviewed)

> **Evidence class: static only.** The findings below come from reading the file
> blob at the named commit (`git show`), its `gh api` commit metadata, and a
> `grep -c sorry`. The project was **not** cloned, built, or axiom-audited, and no
> maintainer/third-party confirmation of its publication date exists. Treat the
> 2026-08-17 date as *the committer timestamp of the commit that introduced the
> file*, which is evidence of existence by that date — **not** a verified proof
> of independent completion/publication time.

* Repo: `https://github.com/plby/lean-proofs` (owner: Boris Alexeev; created
  2025-11-23; `pushed_at` 2026-09-15T20:59:47Z; default branch `main`; no declared
  licence in the GitHub metadata).
* Proof file: `src/latest/ErdosProblems/Erdos834.lean`
  (an HTML-rendered copy lives at `<repo>/ErdosProblems/Erdos834.md`).
* **Commit history of that exact path** (`gh api repos/plby/lean-proofs/commits?path=src/latest/ErdosProblems/Erdos834.lean`):

  | commit | committer date | message |
  |---|---|---|
  | `da153ecd8a4f3bee42edca0c596e313bb834fb34` | **2026-08-17T18:05:20Z** | `Add Erdos834.` |
  | `33a6b9a285cb64ac276ce4d0b3a4111b82c972b6` | 2026-08-23T01:17:44Z | `Add headers.` |
  | `0054e9e8108f574d2c17b1859c2a2f57256491f9` | 2026-08-31T19:34:02Z | `lint: Erdos834` |
  | `8822f7ddef30fadbd92e1c6ab4ed897af356af5e` | 2026-09-15T20:59:44Z | `minor` (pins the file as it stood when PR #1383/#4071 cite it) |

  Verified by direct read of the blob:
  * at `da153ecd…`: 814 lines, **`grep -c sorry` = 0**, same target set;
  * at `8822f7ddef30`: 828 lines, sha256 `9e508b00b70b7ab8e823f3239a881b450a68fcfe18ff21ea46a21f1d3513d423`,
  * blob SHA at pin: `9f1445329ca95554d964c4c04f2ce022004adcc0`.
  * Commit `da153ecd…` was authored **and** committed by `Boris Alexeev
    <boris.alexeev@gmail.com>`; the parent is `85f418da…`. GitHub reports
    `verified: false` for that commit — i.e. commit-signature verification is **not**
    available, which matters because the rules require *independent* public history
    (commit timestamps alone are explicitly insufficient).
* File header (verbatim):
  > `Informal authors: - R. Li`
  > `Formal authors: - Codex - GPT-5.6 Sol`
  > `URLs: - https://github.com/plby/lean-proofs/blob/main/ErdosProblems/Erdos834.md`
* Acceptance-relevant targets inside the file (all `sorry`-free):
  `erdos_834`, `exists_chromaticThreeCritical_minDegreeSeven`,
  `liHypergraph_chromaticThreeCritical`, `liHypergraph_isUniform`,
  `liHypergraph_minDegreeSeven`, `liHypergraph_edgeCritical`,
  `liHypergraph_vertexCritical`, plus the transversal family
  `transversalThreeCritical_exists_degree_le_six`,
  `no_transversalThreeCritical_minDegreeSeven`,
  `completeThreeGraphFive_properties`.
* The `erdos_834` statement formalizes **both** readings as one conjunction, i.e.
  a strict superset of the JSP-000690 chromatic question.
* Caveats that maintainers will have to resolve anyway:
  (a) authorship is credited to AI model names, with `Boris Alexeev` as committer;
  (b) the commit is **unsigned/unverified**; (c) the repo declares no licence
  (COPYING/attribution question). None of these *removes* it from being an
  earlier public proof, but they are the places a challenge would probe.

### 4.2 Our own proof (for the record)

* `delivery-jsp-000690`, single commit `57b16852ac4190a0b18357fa640e579ceb83813e`,
  committer date `2026-10-12T16:07:43+08:00` (= 2026-10-12T08:07:43Z).
* `Erdos834.lean` sha256 `c92f311b73d80dfd781a70eb90c0e944ebaf1ebdf040380f9f280880335f7204`.
* Witness `Erdos834.H` is, after re-indexing `i ↦ i+1`, **exactly** Li25 display
  (5) — verified in this audit by set comparison (`22` edges, symmetric difference
  empty) and degree vector `(10,7,7,7,7,7,7,7,7)`.
* So our contribution *re-formalizes the identical published witness* with an
  identity of subject-matter; it adds no new mathematical content and no earlier
  Lean verification of any part of the problem.

## 5. Timeline (all times UTC)

| time | event | artefact |
|---|---|---|
| 1974 | problem source: *Unsolved Problems*, p. 282; catalogue dates it "no later than 1974" | `[Er74d, p.282]` — see §3 |
| 2025-12-31T13:19:18Z | Li25 v1 posted | arXiv:2512.24850v1 (single author: Ruiliang Li; updated 2026-10-12) |
| **2026-08-17T18:05:20Z** | file `Erdos834.lean` present in a public repo as of this commit's committer date ("Add Erdos834."); 0 `sorry` (static read only) | `plby/lean-proofs@da153ecd…` `src/latest/ErdosProblems/Erdos834.lean` |
| 2026-08-23T01:17:44Z | "Add headers." to the same file | `plby/lean-proofs@33a6b9a2…` |
| 2026-08-31T19:34:02Z | last content change of that file before the JSP wave ("lint: Erdos834") | `plby/lean-proofs@0054e9e8…` |
| 2026-09-15T20:59:44Z | `plby` `main` frozen ("minor") | `8822f7ddef30…` — the commit later cited by #1383/#4071 |
| 2026-09-16T09:32:21Z | first JSP item for this problem (issue) | #15 (milshop) — inline `Proof.lean`, sha256 `b774101a…`, Lean 4.24.0 |
| 2026-09-16T09:57:15Z | first JSP PR for this problem | #21 (paradoxSCH) — closed, superseded by #2108 |
| 2026-09-16T10:55:07Z | 2nd PR | #35 (superpilot69/wofuhuola + "ChatGPT 6 Astra") — closed |
| 2026-09-16T11:40:48Z | catalog-attribution PR | #39 (randyxian08) — closed by maintainer `GordonLtron` (see §6) |
| 2026-09-16T15:42:38Z | parallel chromatic recipient claim | #126 (solivansprvill-droid) |
| **2026-09-17T12:29:57Z** | **focus issue #697** (homelymole95): first such "Correction" proposing `Lean proof = Yes` | cites `homelymole95/jsp-000690-chromatic-lean@4dc3c7eb…`; explicitly disclaims exclusive priority and discloses #126 |
| 2026-09-17T13:46:59Z | #747 (CHENLexiao8848) consolidating #737; first PR to explicitly list `plby` as *prior* submission | cites `plby@8822f7ddef30` |
| 2026-09-17…09-23 | ~30 further same-problem PRs/issues | see §6 |
| **2026-09-18T17:32:59Z** | **focus PR #1383** (xinkuangsi-spec): records the *plby* source, catalog-only, 1 file +1/−1 | no authorship claimed |
| **2026-09-23T04:09:22Z** | **focus PR #4071** (dcdreamy-code): same, richer body, 8 files +96/−0 | maintainer comment says priority is *not* reset by resubmission |
| 2026-10-08T10:25:49Z | awards `main` HEAD used for this audit | `16877004910734cecca83cc5af0fec2f5a4125b3` |
| 2026-10-12T08:07:43Z | our proof committed locally | `delivery-jsp-000690@57b1685…` |
| — | **no merge, no candidate, no award** | JSP-000690 `Lean proof = No` at main; absent from `candidates/README.md` and `awards/README.md` |

## 6. Focused review of #697, #1383, #4071, and the earliest submissions

### #697 — `[Correction] JSP-000690 Lean proof and claim eligibility`
* Type: **issue** (not PR), by `homelymole95`, 2026-09-17T12:29:57Z, **open**.
* Asks to flip `Lean proof → Yes`, cite
  `homelymole95/jsp-000690-chromatic-lean@4dc3c7ebce6bb7fbdff6575c14a77c1e068d18e5`,
  target `Jsp000690.jsp000690 : Jsp000690.JSP000690Statement`, Lean `v4.35.0-rc2`,
  Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`; axiom report
  `[propext, Classical.choice, Quot.sound]`.
* Self-limiting text (important precedent): *"This correction does not assert
  exclusive formalization priority"*, and it discloses the parallel #126.
* Its comment (same author, 12:39:45Z) adds: *"Mathematical discovery credit and
  Lean formalization credit should remain distinct."*

### #1383 — `JSP-000690: record existing Lean formalization (plby/lean-proofs)`
* **PR**, `xinkuangsi-spec`, 2026-09-18T17:32:59Z, **open**, `mergeable_state =
  blocked`, 1 file, `+1/−1`.
* Records `plby/lean-proofs@8822f7ddef30fadbd92e1c6ab4ed897af356af5e`,
  file `src/latest/ErdosProblems/Erdos834.lean`, authors "per file headers".
* Explicitly: *"The undersigned is the catalog editor only, not the proof author
  … no authorship or award eligibility is claimed."*
* ⚠️ Its cited path is `src/latest/ErdosProblems/Erdos834.lean`, which **is**
  correct — but its toolchain description (`lakefile`/`lean-toolchain`) does not
  match `plby`'s actual layout; reviwers must resolve by SHA, not by path prose.

### #4071 — `JSP-000690: register Lean formalization (plby/lean-proofs)`
* **PR**, `dcdreamy-code`, 2026-09-23T04:09:22Z, **open**, blocked, 8 files, +96/−0.
* Same source SHA as #1383; adds a "Pre-submission Lean verification (optional)"
  block with `lean-verify` reference and a 2026-09-24 manual-inspection note;
  states toolchain `v4.33.0`, "authors per file header: Codex, GPT-5.x".
* Maintainer `Federico2014` comment, 2026-09-23T15:26:55Z (verbatim, priority-relevant):
  > "**Please do not submit Lean source code directly to our repository.** … Host
  > your Lean source code in your own public repository and provide its URL,
  > branch, and full commit SHA. … **Resubmitting will not reset your priority for
  > award consideration.** We will assess priority based on the original
  > source-code submission time or the verifiable completion time of the proof in
  > your repository, as applicable—not the date of the replacement PR."

Net effect of the three focus items: they are **catalog-metadata PRs/issues that
all point at the pre-existing `plby` proof**; none of them is itself a proof
contribution, and none has been merged.

### Earliest submissions #15 / #21 / #35 / #39 (all 2026-09-16)
* #15 (milshop, issue): self-contained inline `Proof.lean`, sha256
  `b774101a4cfbf9715a2823fe87fe8208981adbbdc4f2f244ff8428190d8a547e`, Lean
  4.24.0, axioms `[propext, Quot.sound]`; chromatic reading only; explicitly
  *"not a recommendation to add a duplicate problem"*; prepared "with OpenAI Codex
  assistance".
* #21 (paradoxSCH, PR): chromatic; source `paradoxSCH/awards@e47dce2e…`
  `submissions/jsp-000690/Main.lean`, sha256 `c584af6d…`; Lean 4.34.0 + bundled
  Std; axioms `[propext, Quot.sound]` (+`Classical.choice` for one auxiliary).
  Closed 2026-09-20 by maintainer with the "don't submit source here / resubmit
  without resetting priority" message; reopened as #2108
  (`paradoxSCH/jsp-000690-lean@246f0523…`).
* #35 (superpilot69 / X `@wofuhuola` + "ChatGPT 6 Astra", PR): chromatic; Lean
  4.34.0; axioms `[propext, Quot.sound]`; closed; also received the same maintainer
  message.
* #39 (randyxian08, PR): catalog-attribution only; **closed as rejected** by a
  non-maintainer-looking account `GordonLtron` (2026-09-21T04:11:31Z) alleging
  "Identity & Attribution Mismatch", "Invalid Repository Architecture",
  "Acknowledged Non-Priority", and an "outdated toolchain (Lean 4.19.0)". The
  submitter then re-pointed at a dedicated repo `randyxian08/jsp000690-lean@928c0b05…`
  with Lean 4.34.0 and asked where the 4.34.0 minimum is published. ⚠️ **This
  "minimum Lean version 4.34.0" is not stated in any rule document at the pinned
  main SHA**; treat any such requirement asserted in review as unverified (§9).

### Distributed-state conclusion
**46 JSP items are scoped to JSP-000690** (55 raw search hits; 9 of those are
cross-problem PRs such as #40/#41/#133/#144/#458/#498/#1017/#1032 that merely
co-list it). Of the 46, **37 are open and 9 closed; none is merged**. As of the
pinned main SHA no submission has been accepted: the catalog still reads
`Lean proof | No`, and JSP-000690 appears in neither `candidates/README.md` nor
`awards/README.md`. **No source has been recorded yet, and no priority has been
adjudicated.**

## 7. Priority assessment for `qingsongcui` (risk-based, not adjudicated)

Applying the pinned rules to the **static** facts, with all conclusions framed as
risk rather than as a settled determination:

1. **A later date than a plausible earlier source.** A public file containing the
   same question already existed at a commit dated 2026-08-17 (static metadata),
   and by 2026-09-23 two open PRs cited it with a fixed SHA. Our work is dated
   2026-10-12. Under the rules' controlling principle — *"the earliest selected
   commit in the accepted original proof repositories takes priority"* — our
   position is **weak if that earlier source is accepted**; it is **not
   established that it will be** accepted (it has not been, and maintainers have
   to verify it first).
2. **We cannot adopt the earlier source.** `CONTRIBUTING.md`: *"Do not register
   someone else's proof, a mirror or a copy on their behalf."* Registering `plby`
   (or any of the ~20 third-party repos) is explicitly prohibited; and
   `docs/attribution.md` rejects *"a mirror or collection of someone else's proof"*
   and says repository ownership or last-committer status does not establish
   authorship. So we cannot convert the earlier date into our own position.
3. **Our proof adds no new mathematical content**: the witness equals Li25 display
   (5) exactly (measured by set comparison); the mathematics is already credited
   in the catalogue's `Publication details` to Li25.
4. **The problem is already recorded as solved**, by Li25 (2025-12-31). `Eligible
   to claim` is *No*; eligibility would require **both** a recorded mathematical
   solution and a recorded Lean proof, and neither is recorded.
5. **Resubmitting does not reset priority** (maintainer statement in #4071), so
   the many unmerged PRs give no time anchor either.

**Therefore:** on the present evidence a submission would **not build a
defensible priority position** and carries a high risk of a duplicate/non-priority
outcome. **Recommendation: do not submit** unless the user overrides. This is a
risk judgement on static evidence; it is not a ruling, and it does not predict the
maintainers' verification outcome for any source.

## 8. What would change the verdict

Resubmit **only** if the user can supply a *verifiably earlier* complete proof of
the **same chromatic statement** by their own account, with independent public
history (e.g. a signed, dated commit or a CI run predating 2026-08-17). Absent
that, a submission is not justified by the rules as pinned here.

## 9. Open / unresolved items (for the user or maintainers)

1. **Real name.** `qingsongcui` is only a GitHub handle. The award process requires
   an identity-verification e-mail; the draft intentionally leaves the legal name
   blank. *Do not invent one.*
2. **plby authorship.** The file header credits `Codex`/`GPT-5.6 Sol`; the committer
   is a human (`Boris Alexeev`) and the commit is unsigned. How the maintainers
   attribute this is their call — we neither challenge nor rely on it.
3. **plby licence.** GitHub metadata shows no licence for `plby/lean-proofs`;
   third-party reuse of its *text* would be an open question (we reuse none).
4. **"Minimum Lean v4.34.0" claim.** Not found in the pinned rules; we will not
   assert it (our toolchain is `v4.33.1`, matching the frozen challenge file's
   upstream toolchain family).
5. **Toolchain/target drift.** Our `parts.ii` target is the *chromatic* reading
   only; the transversal `parts.i` (`answer(False)`) is **not** proved here. If a
   maintainer reads "3-critical" as including `parts.i`, this submission would be
   incomplete — another reason to avoid submitting.
6. **The earlier source was reviewed statically only** (see §1.1): no `git clone`,
   build, or `#print axioms` was run on `plby/lean-proofs` in this audit. What is
   established is that the file exists at those commits with 0 `sorry` and the
   target list stated above; what is **not** established is that it compiles, that
   its axioms are clean, or that maintainers would accept it. Maintainer-side
   reproduction is a rule requirement before any acceptance.

## 10. How to re-run this audit

```sh
# official rules at the audit SHA
BASE=16877004910734cecca83cc5af0fec2f5a4125b3
for p in CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md \
         docs/award-process.md docs/attribution.md docs/verification.md; do
  curl -sL "https://raw.githubusercontent.com/TheJustinSunPrize/awards/$BASE/$p" -o "$(basename $p)"
done

# focus items
gh api repos/TheJustinSunPrize/awards/issues/697   --jq '{title,state,created_at,body}'
gh api repos/TheJustinSunPrize/awards/pulls/1383   --jq '{title,state,created_at,head:.head.repo.full_name}'
gh api repos/TheJustinSunPrize/awards/pulls/4071   --jq '{title,state,created_at,head:.head.repo.full_name}'
gh api repos/TheJustinSunPrize/awards/issues/4071/comments --jq '.[]|{user:.user.login,created_at,body}'

# the key prior source (static inspection: history + blob content)
gh api "repos/plby/lean-proofs/commits?path=src/latest/ErdosProblems/Erdos834.lean&per_page=100" \
  --jq '.[]|{sha,date:.commit.committer.date,msg:(.commit.message|split("\n")[0])}'
git clone --filter=blob:none --no-checkout https://github.com/plby/lean-proofs
cd lean-proofs && git show da153ecd8a4f3bee42edca0c596e313bb834fb34:src/latest/ErdosProblems/Erdos834.lean | grep -c sorry
# (optionally, to actually verify it: lake exe cache get && lake build)

# our own artefacts
shasum -a 256 challenge/Erdos834.lean Erdos834.lean
```
