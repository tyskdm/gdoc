# Design Change Record — 2026-09-26 — System Task → package-unit resident waiter (State 3)

> ## ⛔ CANCELLED — superseded (2026-09-27)
>
> **This change record is CANCELLED and must NOT be applied.** It was recorded 2026-09-26 and left **Open** awaiting Q1…Q12; it was **never applied** (no design document was changed; **D-024 was not logged** from it). It is retained for traceability and is **superseded by** → `change-2026-09-27-despec-boundary-correction.md`.
>
> **Why it was cancelled (session discussion, 2026-09-27):**
>
> 1. **Wrong unit of change.** The record framed D-024 as a **task redesign** — redefining the System Task from *per-file (State 2)* to a **per-package** resident waiter. The discussion showed that committing to *per-package* (or *per-file*) is a **mechanism choice**, not a C1–C2 boundary decision: the design documents should **not** fix the granularity, count, shape, or priority *numerics* of the ODB's background work.
> 2. **Boundary misplaced.** **NC-05** is a **guarantee** — "a **built state is available**" — not a **mechanism** — "a System Task of a specific shape exists." The record treated the mechanism (System Task shape, per-file vs per-package, priority numerics, standing-waiter) as if it were part of the C1–C2 contract. It is not.
> 3. **Correct scope (agreed 2026-09-27 — items a / b / c).** D-024 = **de-specification + boundary correction**, **not** a redesign:
>    - **(a)** purpose = *remove over-specification and correct the boundary*;
>    - **(b)** the **3-tier boundary** — **①** C1–C2 guarantees (NC-05 scope; ADR-007 State 1/2/3 *definitions*) · **②** ODB-internal **invariant rails** (priority *ordering* monotonicity, ref-count cancel, dedup, atomic commit, no state-mixing) · **③** ODB-internal **mechanism** (task shape, count, granularity, priority *numerics*, standing-waiter, attach/detach) → **③ is retracted from the design documents**;
>    - **(c)** restructure `contracts/task-job-management.md` to **②-level**, retracting **TJ-021**'s concrete mechanism to **③**.
> 4. **Q1…Q12 superseded.** The 12 items in §4 were framed around the *mechanism*. **Q7** (attach/detach) and **Q8** (State-2 defer) are **③ (ODB-internal)** — no longer boundary decisions requiring C1–C2 contract changes. All 12 are superseded by the re-scoped checklist (**Q-A / Q-B / Q-C**) in the successor record.
>
> **Do not apply this record** and **do not log D-024 from this file.** Continue with the successor: `change-2026-09-27-despec-boundary-correction.md`.
>
> **Position:** `docs/architecture/gdocServer/process/changes/change-2026-09-26-system-task-package-unit.md`
> **Status:** ⛔ **CANCELLED — superseded 2026-09-27** — see the banner above. Recorded 2026-09-26 and left **Open** awaiting Q1…Q12; **never applied** (no design document was changed; D-024 was **not** logged from it). Retained for traceability; **superseded by `change-2026-09-27-despec-boundary-correction.md`**. **Do not apply; do not log D-024 from this file.**
> **Date:** 2026-09-26 · **Author:** assistant; model per user handover (2026-09-26).
> **Scope:** the gdocServer design set — `../../README.md` §7 · `../../contracts/task-job-management.md` · `../../contracts/frontend-odb-api.md` · `../../subcomponents/README.md` · `../../usecases/UC-001…003` · `../../architecture.md`.
> **Decision to be logged:** **D-024** in `../../README.md` §7 — *refines (and supersedes the State-2 trigger of) D-014*. **Not yet logged** (logged at application, on approval).
> **⚠️ ID note:** the handover proposed "add D-022"; **D-022 and D-023 already exist** (`../../README.md` §7, 2026-09-26). The next free ID is **D-024** (DC-01 below).

*Status legend (shared with `../reviews/README.md`):* [O] Open · [F] Fixed · [C] Confirmed · [D] Deferred · [R] Resolved · [P] Pending fix · [?] Needs user decision.

## 1. Background & Purpose

`D-014` (2026-09-14) introduced a **System Task** created **per document** whenever it enters **State 2** (open in the editor + its references, ADR-007) or **State 3** (package member). That design has three problems:

1. **Task churn** — every open/edit creates a per-file System Task and later cancels it.
2. **Priority mixing** — a per-file System Task can hold files of **different states** (a State-3 member riding inside a higher-priority per-file Task), violating **ADR-007** (a Task's priority = the highest state it holds). A single Task must **not** mix states.
3. **Lifetime / leak** — if a System Task is held indefinitely to "guarantee the build", it never releases, so a Job it waits on can never be cancelled — exactly the **R-006-3 leak** (a Job that can never be cancelled).

At the same time, **NC-05** (a reference-counted Job with **0 waiters** is cancelled immediately) must be preserved: the guarantee that a *built state exists* is carried by the **waiter role** in the Job waiter set, not by re-building. The System Task's real job is to **be a waiter**, not to build.

**Purpose:** redefine the System Task from a **per-file (State 2)** unit to a **per-package resident waiter (State 3)** with a **bounded lifetime**, and delegate the `open`/`change` interactions to **client Tasks (State 1)**. This removes the churn and the priority mixing, keeps the waiter role (NC-05), and bounds the lifetime so **TJ-007 cancel can still fire**.

> **Deliberately NOT changed:** ADR-007's State 1/2/3 definitions and the rank-2 ADRs; ADR-009 (package scope); the ODB's ownership of Job mechanics (dedup TJ-005 / dispatch TJ-012 / commit TJ-004) and of package membership (**INV-06**). This is a **C2-internal redefinition** (a D-014 refinement), **not** an ADR change.

## 2. Goal — Decided Model

| file kind | Task(s) | State / priority | lifetime |
| --------- | ------- | ---------------- | -------- |
| **package member** | **package Task** (the single kind of **System Task**) | **State 3 (lowest)** | **resident waiter** — a *re-scoping of the standing-waiter already in TJ-021*, not a new lifecycle; **bounded** — released when **membership becomes empty** (members leave via `DOCUMENT_SYNC{close}`/`WATCHED_FILES{deleted}`, or re-scope `CONFIG_SAVE`/TJ-016, or package deletion). *No "workspace shutdown" API exists in the contract — release = "membership empty ⇒ cancel", the same last-waiter logic as TJ-007 (Q10)* |
| package member **+ active Request** | + **client Task** | **State 1 (highest)** | for the duration of the Request |
| **open, non-package** | **client Task** | State 1 | for the duration of the Request |
| **non-package, non-open** | **none** | — | — (not built in the background) |

**Invariants (conclusion C + INV-06):**

- The package Task is a **waiter**, **not** a passive observer: it exists to sit in the Job waiter set (resolves **NC-05**) so the built state of its Package members is guaranteed without re-building.
- **One package Task per Package** (not per file), holding that Package's member files; it holds **only State-3** files.
- **The ODB owns** the Job mechanics (dedup/dispatch/commit) **and** package membership (**INV-06**). The package Task **references** the membership; it does **not** re-own a second copy.
- **A single Task shall never hold files of different states** (priority-mixing prohibition) — the core rationale for the package/client split.
- A package Task **cannot be cancelled by the Frontend** (carries D-014(d)/TJ-021(d)).
- **Membership-change attach/detach (NEW, Q7)**: when a document *joins/leaves* the package, the ODB attaches/detaches the package Task's Job-waiter-set participation for that member (join ⇒ enter the member's Job waiter set; leave ⇒ leave + decrement, exactly like a client-Task departure, TJ-007). Multi-package membership ⇒ the document is held by the package Task of *each* package. Package deletion ⇒ its package Task is released (membership empty). Config-Save re-scope ⇒ TJ-016 invalidation applies to the *departing* member's Jobs. *The unit of re-scope is now "a document joins/leaves the package", not "a document enters/exits State 2."*
- **State-2 post-completion (NEW, Q8)**: with the State-2 System Task gone, an open **non-package** file has **no resident Task** after its client Task (State 1) completes — its build guarantee is *deferred* to the next operation, with **no continuous rebuild while merely open**. This is an intended consequence and must be reconciled with **ADR-007 (State-2 priority) + TJ-011**: the "State 2" priority row is read as "applies to *client Tasks operating on* open documents", not "a resident State-2 Task exists."

## 3. Plan — How to Proceed

**Order** (apply only after the §4 checklist Q1…Q6 is approved):

1. **`../../README.md` §7** — add decision **D-024** (refines/supersedes the State-2 trigger of **D-014**) *after* D-023. Drafted row: §5.1.
2. **`../../contracts/task-job-management.md`** — rewrite **TJ-021** (package-unit, State 3, bounded lifetime, exit = re-scope/shutdown); extend the **TJ-001** "extended trigger (D-014)" note (client Request **or** package-scope transition); align the §4 index row (TJ-021) and the §5.3 D-014 / TJ-021 rows to add **D-024**.
3. **`../../architecture.md`** — the *Task* bullet in §Execution Model + the "Task and Subtask" (L266-area) prose → 2-type model.
4. **`../../subcomponents/README.md`** — glossary **Task** row → 2-type model (+ optional dedicated **System Task (package Task)** row); **INV-06** parenthetical (package Task references, does not re-own).
5. **`../../usecases/UC-001_OpenWorkspace.md`, `UC-002_OpenText.md`, `UC-003_EditText.md`** — replace "per-document / State 2 per-file Task" language with the 2-type model (client Task State 1 + package Task State 3). **UC-002 is the most impactful** (open → reference-closure build; NC-06's request-less push is then carried by the package Task — meaning-preserving rename).
6. **`../../contracts/frontend-odb-api.md`** (DC-03 ripple) — NC-06 resolution (L287) + `TerminalEvent.reason` `system_cancelled` (L298): per-file State-2 System Task → package Task.
7. **Trade-off record** (DC-04) — per the agreed location: record both trade-offs in the **D-024 Rationale** cell (precedent: D-021), or (option B) add two rows to the risk register. **Recommended: D-024 Rationale.**

**Not changed:** `adr/007-priority.md`, `adr/README.md` (unless option B), other `contracts/` files, `usecases/UC-004…011` (in-flight), Phase 0/1a/1b deliverables not cited above.

## 4. Important Findings & Confirmation Items

| ID | Item | Location | Recommendation | Status |
| --- | ---- | -------- | -------------- | ------ |
| DC-01 | **ID conflict:** handover says "add D-022", but **D-022 and D-023 already exist** | `../../README.md` §7 | Use the next free ID **D-024** for the new decision | [C] |
| DC-02 | **UC naming:** handover's "UC-001_OpenText" is actually **UC-002_OpenText** (real: UC-001_OpenWorkspace / UC-002_OpenText / UC-003_EditText) | `../../usecases/` | Edit the three real files; do not target a non-existent UC-001_OpenText | [C] |
| DC-03 | **Ripple not in the handover's 5-item plan:** `frontend-odb-api.md` cites the System Task (NC-06 L287; `system_cancelled` L298) | `../../contracts/frontend-odb-api.md` | Include it: reframe per-file State-2 System Task → package Task (semantic-preserving rename) | [C] |
| DC-04 | **Where to record the two trade-offs** (per-file cancel lost; dual-priority for open members): `adr/README.md` risk register is ADR-scoped (`R-NNN-M`); these are *trade-offs*, not failure-prone risks | `../../adr/README.md` vs `../../README.md` §7 | **[?] A/B** — **A (recommended):** record in the **D-024 Rationale** cell (precedent D-021). **B:** add two rows to the risk register | [?] |
| DC-05 | **refine vs supersede D-014:** removing the State-2 trigger is a partial supersede, not just a refinement | `../../README.md` §7 | Word D-024 as "refines (and supersedes the **State-2 trigger** of) D-014" | [C] |
| DC-06 | **Ownership:** package membership stays with the ODB (**INV-06**); the package Task must only *reference* it | `../../subcomponents/README.md` INV-06 | Keep single owner; add a "references, does not re-own" note; no second owner | [C] |

### Confirmation checklist (final checklist — apply only once all are resolved)

| # | Question | Recommendation | User decision |
| - | -------- | -------------- | ------------- |
| Q1 | **New decision ID = D-024** (D-022/D-023 already used)? | yes — D-024 | ⬜ pending |
| Q2 | **Relationship to D-014** = "refines (and supersedes the State-2 trigger of) D-014"? | yes | ⬜ pending |
| Q3 | **Include the `frontend-odb-api.md` ripple** (L287 NC-06, L298 `system_cancelled`)? | yes (semantic-preserving rename) | ⬜ pending |
| Q4 | **Trade-off record location** = A (D-024 Rationale) or B (risk register rows)? | A | ⬜ pending |
| Q5 | **Glossary**: add a dedicated **System Task (package Task)** row + an **INV-06** parenthetical? | yes | ⬜ pending |
| Q6 | **UC reframe** = "package member ⇒ package Task (State 3) + client Task (State 1); non-member ⇒ client Task (State 1) only" (NC-06 carried by the package Task, meaning-preserving)? | yes | ⬜ pending |

**Tier 0 — foundational behavior (from review 2026-09-26, §8).** These define what Q1–Q6 above would be recorded *about*, so settle them **first**. All must be resolved (⬜→✅) before the approval gate. (Q9 **refines Q6**.)

| # | Question | Recommendation | User decision |
| - | -------- | -------------- | ------------- |
| Q7 | **standing-waiter attach/detach**: on a member joining/leaving the package, how does the package Task enter/leave the affected Job waiter sets (incl. multi-package membership, package deletion, Config-Save vs a running Job)? | define the attach/detach rule (§2 invariant); TJ-016 governs the re-scope trigger; decrement on departure per TJ-007 | ⬜ pending |
| Q8 | **State-2 post-completion**: an open non-package file has no resident Task after its client Task completes. Accept the deferral + reconcile with ADR-007/TJ-011? | yes — deferred to next operation (client Task, State 1); no continuous rebuild; ADR-007 "State 2" row = "applies to client Tasks on open docs" | ⬜ pending |
| Q9 | **NC-06 producers** (refines Q6): the request-less `DiagnosticsEvent` now has *two* producers (client Task = open/operation closure; package Task = package maintenance) — "carried by the package Task" (Q6) is incomplete. Confirm both are named. | yes — name both in UC-002 L386 + `frontend-odb-api.md` §5.2; `request_id` optional for both; §5.2 relaxation stays meaning-preserving | ⬜ pending |
| Q10 | **release mechanism**: no "workspace shutdown" API exists. Confirm release = "membership empty ⇒ cancel" (TJ-007), not a separate call. | yes — grounded in TJ-007/TJ-016; no new API added | ⬜ pending |
| Q11 | **D-024 Rationale scope** (refines Q4): D-021 dispatch-skip is an *efficiency* measure (stale queued Jobs); it does not cover waiter-detach or running-Job cancellation. Confirm the Rationale delineates which rule covers which case. | yes — (a) file-unit cancel lost → D-021 (stale queued) + D-017 (per-doc); (b) waiter-detach → TJ-016; (c) running-Job cancel → recorded as residual cost | ⬜ pending |
| Q12 | **UC-004…011 inheritance**: Phase 2 (not started). Record how the new model is inherited so they are not built on the old assumption. | yes — impact note in §5.7 (no rewrite now) | ⬜ pending |

## 5. Applied Changes — *to be filled on application*

> Filled with the per-file before→after (the diff actually applied) + a pointer to the verification evidence in §6, after Q1…Q6 are approved and the edits are applied. Planned content per file:

- **§5.1 `../../README.md` §7 — D-024 row** *(drafted; apply on approval; paste verbatim here on application)* — D-024: "System Task redefined as a package-unit resident waiter (State 3 only); `open` delegated to client Tasks (State 1) — refines (and supersedes the State-2 trigger of) D-014. One kind of System Task: the **package Task** — one per Package, State 3 (lowest), a resident waiter in the Job waiter set guaranteeing the built state; bounded lifetime (released on package re-scope or workspace shutdown). No per-file / State-2 System Task; open ⇒ client Task (State 1); non-package, non-open ⇒ no Task. A single Task never mixes files of different states. Not Frontend-cancellable (D-014(d))." + Rationale (NC-05 waiter role; churn & priority-mixing removal; R-006-3 avoidance; trade-offs (a) file-unit cancel lost (mitigated D-021 dispatch-skip) and (b) open package-member dual-priority (expected; ADR-007), recorded here per D-021 precedent).
- **§5.2 `../../contracts/task-job-management.md`** — TJ-021 rewrite (package-unit, State 3, bounded lifetime, exit = re-scope/shutdown, s-* one per Package, not Frontend-cancellable, no per-file State-2 Task, no state-mixing) + TJ-001 extended-trigger note + §4 index row (TJ-021) + §5.3 D-014/TJ-021 rows (add D-024).
- **§5.3 `../../architecture.md`** — *Task* bullet (§Execution Model) + "Task and Subtask" (L266-area) prose → 2-type model.
- **§5.4 `../../subcomponents/README.md`** — glossary **Task** row → 2-type model (+ dedicated **System Task (package Task)** row) + **INV-06** parenthetical.
- **§5.5 `../../usecases/UC-001…003`** — 2-type model language (per-UC occurrence map: Purpose / Derived-From / Scope / Pre-Post conditions / main-flow / alternatives / reverse-check / traceability). *Plus (review 2026-09-26):* **UC-002 L386 (NC-06, Q9)** — reframe to name **both** request-less-diagnostic producers (client Task = open/operation reference closure; package Task = package maintenance), not just "the package Task"; **UC-002 State-2 line (Q8)** — an open non-package file is a client Task (State 1) with a *deferred* build guarantee (no resident State-2 Task); **UC-003** — the package-member maintenance Task is the package Task (State 3), not a per-file State-2 Task.
- **§5.6 `../../contracts/frontend-odb-api.md`** — **L287 (NC-06)**: the request-less `DiagnosticsEvent` rationale keeps its meaning, but the subject is named as **both** producers (client Task for open/operation closures; package Task for package maintenance) — `request_id` optional for both; the §5.2 relaxation (P2-003) stays meaning-preserving (**Q9**). **L298 (`system_cancelled`)**: "System Task" → "package Task" (the only System Task kind). *No API operation changes.*
- **§5.7 `../../usecases/UC-004_OpenWorkspace … UC-011_WatchFiles` — impact note, NOT a rewrite** *(review 2026-09-26, Q12)*: per `README.md` §3.2 (a contract change re-confirms dependent UCs), record how Phase 2 inherits the new model so it is not built on the old assumption: (a) the **package Task (State 3)** is the *resident* maintainer for package-member documents (per-package, not per-file); (b) *open* non-package documents are **client Tasks (State 1)** with a deferred build (Q8); (c) **membership change** (attach/detach) is the unit of re-scope, not "State 2 entry/exit" (Q7). *One-line impact note per UC; no text change in this commit.*

## 6. Verification — *to be run after application*

*(Commands run from `docs/architecture/gdocServer/`.)*

| # | Check | Command / method | Expected |
| - | ----- | ---------------- | -------- |
| V1 | No per-file **State-2 System Task** remains | `grep -rn 'State 2.*System Task\|System Task.*State 2' usecases contracts architecture.md subcomponents` | 0 (except the D-024 supersede note) |
| V2 | **D-024** defined; **D-022/D-023** untouched | `grep -c 'D-024' README.md` ; `grep -c 'D-022\|D-023' README.md` | D-024 ≥ 1; D-022/D-023 count unchanged from pre-change |
| V3 | **TJ-021** is package-unit | `grep -n 'package Task\|Package Task' contracts/task-job-management.md` | present in TJ-021, TJ-001 note, §4 index, §5.3 |
| V4 | **Rule count** unchanged | `grep -c '^| TJ-0' contracts/task-job-management.md` | 42 (21 in §4 + 21 in §6) |
| V5 | **D-014 paired with D-024** in every package-Task context | `grep -rn 'D-014' usecases contracts architecture.md subcomponents` | each package-Task claim cites D-014/D-024 |
| V6 | **UC classification** consistent | spot-check UC-001/002/003 Purpose / Postcond / Traceability | 2-type model in all three |
| V7 | **frontend-odb ripple** applied (if Q3=yes) | `grep -n 'system_cancelled\|NC-06' contracts/frontend-odb-api.md` | package Task, not per-file State-2 |
| V8 | **Single owner** (INV-06) intact | read the INV-06 row | ODB owns membership; package Task references only |

## 7. Status & Commit

- **Commit convention** (mirrors `../reviews/Design Review Procedure.md` §5): **one commit**, made only after Q1…Q12 approval (Tier-0 Q7–Q12 first) + applied + verified (§6):
  `docs: design change 2026-09-26 (System Task → package-unit State-3 waiter; D-024)` — this record (finalized §5/§6/§7) + the design document changes + the D-024 row in `../../README.md` §7.
- **Trace:** `git log --grep 'D-024'` · `git log --grep 'package Task'`.
- **Status log:** [O] Open (2026-09-26) — plan + proposal + findings recorded. **Review 2026-09-26 received (§8): 7/8 concerns accepted, 1 (lifecycle framing) rebutted with evidence; Tier-0 Q7–Q12 added.** Now **awaiting Q1…Q12** (Tier-0 first).

## 8. Review response (2026-09-26)

A design review (separate from this change record) evaluated the plan and raised 8 concerns. Dispositions (evidence in this record / the contracts):

| # | Review concern | Disposition | Evidence / basis |
|---| -------------- | ----------- | ---------------- |
| 1 | Task/Job lifecycle conflict (current = finite; new = breaks it) | **Partially rebutted** | The *standing-waiter already exists* in TJ-021(c): the per-file System Task is "cancelled when the document leaves its state", not completed when a Job completes. This is a **re-scoping** (file→package, State 2/3→3), not a new lifecycle. *But* the underlying concern — define **membership attach/detach** — is valid → **Q7**. |
| 2 | State-2 guarantee after client Task completes | **Accepted** | Open non-package files lose their immediate build; deferred to the next operation. → **Q8** + §2 invariant. |
| 3 | NC-06 semantics (two producers, not just the package Task) | **Accepted** | Current basis = "System Task reference-closure build" (`frontend-odb-api.md` L287, UC-002 L386). New model: client Task (State 1) + package Task (State 3). → **Q9** (refines Q6) + §5.5/§5.6. |
| 4 | Membership change / re-scoping (attach/detach, multi-package, deletion, Config-Save) | **Accepted** | Valid gaps. → **Q7** + §2 invariant. |
| 5 | Shutdown notification path (no shutdown API) | **Accepted** (nuance) | Confirmed: no shutdown API in `frontend-odb-api.md`; D-012 `cancel(all)` is own-Tasks only. Release = "membership empty ⇒ cancel" (TJ-007). *Nuance:* this gap also exists in the current model (per-file System Tasks rely on close/delete/config-change). → **Q10**. |
| 6 | Trade-off mitigation precision (D-021 scope) | **Accepted** | Confirmed: TJ-012 (D-021) is a *should-level efficiency note* (stale queued-Job dispatch-skip); it does not cover waiter-detach or running-Job cancellation. → **Q11** (refines Q4). |
| 7 | UC-004…011 inheritance | **Accepted** | Valid (README §3.2). Phase 2 not started. → **Q12** + §5.7. |
| 8 | V4 grep bug | **Accepted (empirically confirmed)** | The original command matched **all 387 lines** (a backslash-pipe in a BRE is alternation, not a literal pipe); the corrected command (a literal `^|` anchor) returns **42**. → **V4 fixed** (§6). |

**Net:** the review's core recommendation — *resolve the foundational behavior (Tier 0) before the record-location questions (Q1–Q6)* — is **adopted**. The one rebuttal (#1) corrects an over-statement: the standing-waiter is not new; only its scoping and the membership attach/detach rule are new.

---

*This is a design **change** record (distinct from a design **review**). Reviews (`../reviews/`) record findings on already-written documents; this records a deliberate design change — its background, the decided model, the per-file plan, the confirmation checklist, the applied edits, and the verification evidence. The change-record procedure (when/how to record, like `../reviews/Design Review Procedure.md`) is **deferred** for a later pass (per user, 2026-09-26); this file is the first record under it.*
