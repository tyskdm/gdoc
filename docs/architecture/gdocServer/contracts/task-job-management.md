# gdoc Server — Task/Job Management Contract

> **Deliverable of:** Phase 1a (Task/Job management rules, goal #3) of the gdoc Server design-documentation effort.
> **Position:** `docs/architecture/gdocServer/contracts/task-job-management.md`
> **Status:** Draft for user review (Phase 1a — **not yet approved**).
> **Companion files:** `./frontend-odb-api.md` (Phase 1b) · `../usecases/UC_*.md` (Phase 2) · `../subcomponents/*.md` (Phase 3) · `../traceability.md` (Phase 4).
> **Role in the set:** a **Rank-5 contract** (an executable specification **derived** from ranks 1–4, per `../README.md` §2/§3). It is the **rails**: every Phase 3 component requirement that touches Task/Job decomposition, deduplication, cancellation, priority, or configuration-rebuild must cite the applicable `TJ-` rule here, so Phase 3 can *verify against* it.

> **Derived From (document-level):**
> `../requirements/requirements.md` (FR-3.1, FR-3.2, NFR-2.3, NFR-2.1, NFR-3.1) ·
> `../adr/002-request-task-job-model.md` · `../adr/006-job-sharing-semantics.md` · `../adr/007-priority-scheduling.md` · `../adr/009-configuration-lifecycle.md` (primary) ·
> `../adr/003-threading-and-async-facade.md` · `../adr/005-plugin-object-builders.md` · `../adr/008-frontend-odb-scheduling-boundary.md` (supporting — the risks they own that these rules close) ·
> `../adr/README.md` (risk register, `R-NNN-M`) · `../architecture.md` (execution model; Task/Subtask; state-based scheduling) ·
> `../subcomponents/README.md` §4 (single-owner matrix, `INV-*`) + §6 (glossary) ·
> `../README.md` §4 (conventions), §7 (D-004, D-005, D-007, D-008, D-010), §8 (Phase 1a procedure).

---

## 1. Purpose & Position

This contract crystallizes the four load-bearing strategic decisions — **ADR-002** (three-tier model), **ADR-006** (job sharing), **ADR-007** (priority scheduling), **ADR-009** (configuration lifecycle) — into **checkable rules** `TJ-001…TJ-020`. Per `../README.md` §3.1, "contracts are the rails": this document is written **first** so Phase 3 can verify component requirements against it rather than inventing them.

Two properties fix how to read it:

- **Binding on the ODB unless marked Frontend.** Most rules are obligations of the **Object Database (C2)**. Rules that state a **frontend (C1)** obligation are the *other side* of the ADR-008 boundary; they are included so the boundary is **explicit and testable** (R-007-3) and are allocated to `LSP-*` in Phase 3.
- **Terms are referenced, not redefined.** Request / Task / Subtask / Job / Document / Package / Project / **dedup key** / **priority** have a single definition in `../subcomponents/README.md` §6. This file uses them with exactly that meaning.

> **Not in scope here:** the exact *operation set / Request model / result types* of the Frontend↔ODB surface (Phase 1b, `./frontend-odb-api.md`); per-component allocation of these rules into `ODB-*/LSP-*/DS-*/BLD-*` requirements (Phase 3); and the **concrete numeric thresholds/timeouts** for the liveness rules — those are **deferred to detailed design** (D-007). Phase 1a fixes only the **mechanism classes** (TJ-013/014/015), never the numbers.

## 2. Reading the rules

Each rule is a **shall** (a testable obligation) and carries:

- an ID `TJ-nnn` (`../README.md` §4.1);
- a **one-line Derived-From** chain (`../README.md` §4.2) up to its FR/NFR origin;
- a **single owner** (one component, per the single-owner matrix `../subcomponents/README.md` §4); and
- the **risk(s)** it rules, so the Phase 4 closure table can verify "every `R-00x` reached a rule and a test".

Owners: **ODB** = C2 · **Frontend** = C1 · **Builder** = C4 · **Datastore** = C3.

---

## 3. Rules

### 3.1 Three-tier model & state machine

**[TJ-001] Three-tier execution model.** Execution is three tiers — **Request → Task → Job** — with **Subtasks** as the task-local step unit. A **Request** corresponds to **exactly one Task** (the 1:1 invariant is held at the Request↔Task boundary). A **Task** decomposes into zero or more **Subtasks** and/or requests one or more **Jobs**. **Jobs are the only tier that is deduplicated / shared**, and that sharing happens *below* the Task tier, so it does not break the 1:1 invariant.

- **Owner:** ODB. **Risk(s):** (foundation for R-002-1).
- Derived From: FR-3.1 → ADR-002 → ADR-008.
- **Test:** two requests that touch the same document produce two Tasks that await the same Job; the 1:1 Request↔Task invariant holds.

**[TJ-002] Subtask vs Job boundary.** A **Subtask** is a **task-local** management unit: it is **not shared** across Tasks and **not deduplicated**. A **Job** is the **(potentially shared)** execution unit. Deduplication, priority inheritance, and reference-counted cancellation occur **only at the Job tier** — never at the Subtask tier.

- **Owner:** ODB. **Risk(s):** R-002-1.
- Derived From: FR-3.1 → ADR-002 (Subtask note) → R-002-1.
- **Test:** the same unit of work is never tracked as both a shared Job and a task-local Subtask; ref-count / priority accounting is not double-counted across the two tiers.

**[TJ-003] Task lifecycle states.** Every Task is in exactly one state: **Pending** (created, not yet scheduled) · **Active** (scheduled; decomposing and/or awaiting Jobs) · **Completed** (all required Jobs done; the result for its Request is ready) · **Cancelled** (its Request's frontend canceled it). `Completed` and `Cancelled` are **terminal**.

- **Owner:** ODB. **Risk(s):** —.
- Derived From: FR-3.1 → ADR-002.
- **Test:** a Task reaches a terminal state exactly once; no transition out of a terminal state.

**[TJ-004] Job lifecycle states.** Every Job is in exactly one state: **Queued** (registered under its dedup key, not yet dispatched) · **Running** (dispatched to a Builder) · **Completed** (Builder succeeded; result **atomically committed**; all waiters completed) · **Cancelled** (cooperatively canceled before or mid-run; nothing committed). `Completed` and `Cancelled` are **terminal**. A Job holds a **waiter set** (the Tasks awaiting it); its lifetime is governed by that set (TJ-007).

- **Owner:** ODB. **Risk(s):** R-006-1 (commit), R-006-3 (lifetime).
- Derived From: FR-3.1/3.2 → ADR-002, ADR-005, ADR-006 → R-006-1/3.
- **Test:** a mid-run-canceled Job reaches `Cancelled` and commits nothing; a successful Job reaches `Completed` and completes all its waiters.

**State-transition tables** (the single tables the Phase 1a procedure requires):

*Task transitions*

| From | To | Trigger (obligation) | Owner |
| --- | --- | --- | --- |
| — | Pending | A Request is accepted; the ODB maps it **1:1** to a Task (TJ-001). | ODB |
| Pending | Active | The ODB schedules the Task. | ODB |
| Active | Completed | All Jobs the Task requires are `Completed`; the Task's result is ready for its Request. | ODB |
| Active | Cancelled | The Task's **own** frontend cancels its Request (TJ-007; Frontend-side in TJ-010). | ODB (on Frontend action) |
| Pending | Cancelled | The Task's **own** frontend cancels its Request before it runs (TJ-007). | ODB (on Frontend action) |

*Job transitions*

| From | To | Trigger (obligation) | Owner |
| --- | --- | --- | --- |
| — | Queued | A Task requests a Job for a **dedup key** (TJ-005); if an identical key is already in flight, the Task **joins its waiter set** instead of creating a new Job (TJ-006/007). | ODB |
| Queued | Running | The ODB dispatches the Job to a Builder in priority order (TJ-009/011/013/014). | ODB |
| Running | Completed | The Builder returns success; the ODB **atomically commits** the result (TJ-008) and completes every waiter. | ODB (Builder commits) |
| Queued | Cancelled | The Job's **waiter set becomes empty** before dispatch (TJ-007). | ODB |
| Running | Cancelled | The Job's **waiter set becomes empty mid-run**; the Builder is **cooperatively canceled** and commits **nothing** (TJ-007/008). | ODB (Builder cancels) |

### 3.2 Sharing & deduplication

**[TJ-005] Dedup key.** A Job's identity for deduplication is its **dedup key = (file, version, inputs)**, where **inputs = {content type, dependency state, build options}**. Two requests are deduplicated into one Job **iff** their dedup keys are identical. The key-derivation logic is per content type and supplied by the Builder SDK (TJ-020). The **version** component is the **`version_id`** tuple `(last_save_timestamp, open_revision)` (TJ-018).

- **Owner:** ODB (key) + Builder (derivation). **Risk(s):** R-006-2.
- Derived From: FR-3.2 → ADR-006 → R-006-2 → D-004.
- **Test:** differing *relevant inputs* on the same file (content type / dependency state / options) are **not** collapsed into one Job; identical inputs are.

**[TJ-006] Single in-flight invariant.** **At most one Job per dedup key is in flight (Queued or Running) at a time.** A Task that requests a Job whose key is already in flight **joins that Job's waiter set** rather than starting a new one. Jobs created **dynamically mid-Task** (incremental reference discovery) are registered through the **same** dedup key and reconciled with in-flight work, so no key ever has two live Jobs.

- **Owner:** ODB. **Risk(s):** R-002-2, R-006-2.
- Derived From: FR-3.2 → ADR-006 → ADR-002 (R-002-2) → R-006-2.
- **Test:** incremental reference discovery yields **exactly one** in-flight Job per (file, version, inputs) and preserves dependency order.

**[TJ-007] Reference-counted cancellation.** A Job is **active while its waiter set has ≥ 1 member**; it is **canceled only when the last waiting Task departs**. The **count and the cancel decision are centralized in the ODB**; a **frontend cancels only its own Task** and never a Job or another frontend's Task directly. Cancellation is a **cooperative** request to a Builder (TJ-004/008).

- **Owner:** ODB (count + decision); Frontend (cancel own Task only). **Risk(s):** R-006-3, R-008-1, R-002-1.
- Derived From: FR-3.2 → ADR-006 → R-006-3 → ADR-008 (R-008-1).
- **Test:** with two Tasks awaiting one shared Job, canceling one **keeps** the Job running; canceling the last **cancels** it; concurrent add/remove of waiters never leaves the Job canceled-with-waiters or running-without-waiters.

**[TJ-008] Atomic commit on success only.** A Builder commits its result to the Datastore **atomically, and only on success**. A Job **canceled mid-run commits nothing** — the Datastore is left in its **pre-Job** state; partial results are **never** exposed. (The exact commit mechanism — single swap vs. transactional batch — is a detailed-design detail, not a threshold.)

- **Owner:** Builder (commit); ODB (no-expose guarantee). **Risk(s):** R-006-1.
- Derived From: FR-3.2 → ADR-006 → R-006-1 → ADR-005 (R-005-2).
- **Test:** a mid-run-canceled Job leaves the Datastore in its pre-Job state; a successful Job's result becomes visible atomically (all-or-nothing).

**[TJ-009] Priority inheritance.** A Job **inherits the highest priority of all Tasks currently awaiting it**. When a high-priority waiter departs, the Job's effective priority **drops to the max of the remaining waiters**. Inheritance is **accounted at the ODB**, per Job, from the waiter set (never per Subtask).

- **Owner:** ODB. **Risk(s):** R-006-4, R-002-1.
- Derived From: FR-3.2 → ADR-006 → R-006-4.
- **Test:** a high-priority waiter on a Job already held by a low-priority one raises the Job's effective priority; removing the high-priority waiter lowers it again, with **no double-counting**.

### 3.3 Priority (two-domain)

**[TJ-010] Two-domain priority boundary.** Priority is decided in **two domains** and the boundary is a **contract**: the **Frontend** orders *which of its own Requests matter and in what order* (client-type-specific); the **ODB** orders *which shared work runs first* using protocol-agnostic document states and reference depth (TJ-011/012). The **ODB shall not branch its Task/Subtask/Job logic on the client type** — if a frontend needs context the Request model lacks, the model is **extended**, never special-cased. *(The Frontend-side obligation — apply its own request priority/order/cancellation — is owned by C1 and allocated to `LSP-*` in Phase 3.)*

- **Owner:** ODB (does-not-branch); Frontend (orders own requests). **Risk(s):** R-007-3, R-008-2.
- Derived From: NFR-2.3 → ADR-008 → R-007-3 → R-008-2.
- **Test:** architectural check that the ODB's scheduling/cancellation decision paths **never inspect a client-type field**; representative open/request/cancel/background interactions behave the same regardless of the submitting frontend.

**[TJ-011] Document states & reference-depth ordering.** Every workspace document carries state variables for the three states; a document's effective build priority is its **highest** state:

1. **State 1** — referenced by an active (non-canceled) client request.
2. **State 2** — open in the editor (and the documents it references).
3. **State 3** — part of a package (over workspace documents in no package).

Within/below these, references are built in **reference-depth order from open text**: (a) references of open files, (b) references of those, (c) by increasing reference level, (d) documents neither open nor referenced are built **last**.

- **Owner:** ODB. **Risk(s):** (basis for R-007-1/2).
- Derived From: NFR-2.3 → ADR-007.
- **Test:** a state-1 document is scheduled before a state-2 one before a state-3 one; reference-depth ordering (a→b→c→d) holds for a representative reference graph.

**[TJ-012] Priority recomputation.** Priority is **recomputed on every client interaction** (every user action). When a document **leaves state 1**, its Task is **rescheduled** by its state 2/3 priority. A document referenced by *multiple* requests **stays in state 1 until all** such requests are canceled.

- **Owner:** ODB. **Risk(s):** R-007-1.
- Derived From: NFR-2.3 → ADR-007 → R-007-1.
- **Test:** a definition-lookup Task drops priority when the user interacts with another file; a document stays state 1 while any non-canceled request references it, and reschedules on the last departure.

**[TJ-013] State-1 pin bound (mechanism).** A document stays in state 1 only while a **non-canceled** request references it, and the ODB **shall apply an age-based demotion** (or maximum state-1 duration) so a long-lived/forgotten state-1 request **cannot starve** lower-priority work beyond a bound. **The bound value is deferred to detailed design (D-007);** this rule fixes the **mechanism** only.

- **Owner:** ODB. **Risk(s):** R-007-1. **Status:** mechanism fixed · threshold **deferred (D-007)**.
- Derived From: NFR-2.3 → ADR-007 → R-007-1 → D-007.
- **Test:** a long-lived state-1 request does **not** block lower-priority work beyond the (eventual) bound; the demotion trigger is age/timeout, not client type.

**[TJ-014] Unbounded-work defer/cancel (mechanism).** Requests that require completing state-2/3 builds over a large workspace (e.g. **Find References** over the whole object) may be **deferred or canceled** by a bounded policy so they cannot exhaust CPU/memory. **The policy thresholds are deferred to detailed design (D-007);** this rule fixes the **mechanism** (the server *has* a defer/cancel policy and it preserves state consistency afterwards).

- **Owner:** ODB. **Risk(s):** R-007-2. **Status:** mechanism fixed · threshold **deferred (D-007)**.
- Derived From: NFR-2.3 → ADR-007 → R-007-2 → D-007.
- **Test:** an unbounded request over a large workspace can be deferred/canceled and the Datastore/scheduling state remains consistent afterwards.

**[TJ-015] Priority-inversion bound — DEFERRED (not a v1 mechanism).** In v1 the ODB executes Jobs **single-executor and non-preemptively**: a running Job runs to completion, and **priority affects only dispatch order** (TJ-011/TJ-012), **not runtime resource allocation**. A high-priority request arriving while a lower-priority Job is running therefore **waits for that Job to finish** — a wait already **bounded** by that Job's execution time (itself capped by the Builder run bound, TJ-019). Because **no runtime resource is allocated by priority** in v1, **cancel-and-re-run at an inherited priority gives no liveness benefit** and only incurs **wasted-work cost**; it is therefore **not a v1 obligation**.

- **v1 liveness closure for R-006-4:** priority inheritance (TJ-009) + dispatch order (TJ-012) + bounded Builder execution (TJ-019) + state-1 pin (TJ-013) + unbounded-work defer/cancel (TJ-014).
- **Re-entry condition:** if use-case analysis / detailed design introduces **concurrent Job execution** or **runtime resource allocation by priority**, a priority-inversion bound (preempt or cancel-and-re-run) shall be introduced with a concrete bound.
- **Owner:** ODB. **Risk(s):** R-006-4 (v1: closed by TJ-012/019/013/014; preemption aspect **deferred**). **Status:** **deferred (D-010)** — no v1 mechanism obligation.
- Derived From: NFR-2.3 → ADR-006/007 → R-006-4 → **D-010** (refines the R-006-4 portion of D-007).
- **Test (v1):** a high-priority request behind a running Job completes within that Job's (bounded) execution time, with **no preemption required**; a non-cooperative Builder is timed out without stalling others (TJ-019).

### 3.4 Configuration save = rebuild event

**[TJ-016] Config save is a first-class, isolated rebuild/invalidation event.** Changes to project/package **configuration** are applied **only on save** (never on every keystroke) and are treated as a **distinct, higher-stability track** from live document edits. A saved configuration is a **first-class event** that (re)defines **state-3 package membership** and the **dependency graph**; it is **not invalidated by** changes to open text. The resulting re-scope (added/removed packages, changed dependencies) **triggers rebuild/invalidation** in the ODB, and **in-flight Tasks affected by the re-scope are invalidated/re-scheduled** so final membership, priority states, and objects match the saved configuration.

- **Owner:** ODB. **Risk(s):** R-009-1.
- Derived From: ADR-009 → R-009-1 → ADR-004 (single-writer coordination).
- **Test:** a config save during in-flight builds yields final package membership, priority states, and objects consistent with the saved config; a document that leaves a package loses its state-3 priority and stale objects.

**[TJ-017] Config override rules.** Configuration is applied **only from saved content**; an **unsaved** buffer edit of the config has **no effect** until saved. **Open-text (buffer) edits never touch config-derived state**, and config changes are **not overridden** by open-text edits: in a race between an open-text edit and a config save, the **saved configuration wins** for structural facts.

- **Owner:** ODB. **Risk(s):** R-009-2.
- Derived From: ADR-009 → R-009-2 → ADR-007 (document states).
- **Test:** edit config unsaved → no effect; save → effect; an open-text edit racing a config save does not override the saved configuration for structural facts.

### 3.5 Document identity & freshness

**[TJ-018] Document identity / freshness key = `version_id`.** A document's identity/freshness key is the **`version_id` = tuple `(last_save_timestamp, open_revision)`** (D-004): `last_save_timestamp` = the file's **last on-disk save time (mtime)**; `open_revision` = the LSP `didChange` `version` for **open** files, **0** for **non-open** files; compare `last_save_timestamp` first, then `open_revision`. This key is used **consistently** as (a) the **version component of the dedup key** (TJ-005) and (b) the **Datastore freshness invariant**: a stored result for a document is **fresh iff its `version_id` equals the document's current `version_id`**. This resolves the "cannot compare new/old" problem (Q-002 → D-004) **for both open and non-open files**. A document's result is **stale** (and must be rebuilt) when its current `version_id` ≠ the stored result's `version_id`.

- **Scope & computation (D-004 · ADR-001 · FR-1.3):** the `version_id` covers **both open and non-open** files. **Content source:** **open** files → the **client buffer** (C1 supplies it; reflects unsaved edits); **non-open** files → the **builder reads the file from disk by path**. **Change detection:** open → `didChange` (LSP `version`); non-open → **`didChangeWatchedFiles`** (the IDE's watcher — the server does **not** poll the disk). **The `version_id` is computed by C1** (open: `didChange` version + last-save mtime; non-open: mtime via `stat`, `open_revision` = 0); C1 is further obligated to **register `workspace/didChangeWatchedFiles`** for non-open project files. *(This C1 obligation is the boundary's other side (ADR-008), allocated to `LSP-*` in Phase 3.)*
- **Owner:** C1 (computes `version_id`) + ODB (key) + Datastore (freshness invariant). **Risk(s):** R-006-2, (NFR-2.1 consistency).
- Derived From: NFR-2.1 → ADR-006 → R-006-2 → D-004 (Q-002).
- **Test:** an **open** file edited (version bump) or a **non-open** file changed on disk (didChangeWatchedFiles ⇒ mtime bump) ⇒ the stale result is invalidated and rebuilt; a concurrent reader never observes a torn new/old mix; two Tasks with different `version_id`s for the same file are **not** deduplicated; the `version_id` is well-defined whether the file is currently open (buffer) or not (disk).

### 3.6 Builder obligations (mechanism side of sharing)

These two are the **Builder-side** halves of the sharing/cancellation mechanics the ODB *decides* (D-008: **management = ODB, mechanism = Builder**); they are stated here so Phase 3 can allocate them to `BLD-*`.

**[TJ-019] Cooperative cancellation & execution bound.** A Builder **shall cooperate with cancellation** (observe a cancel request promptly) and **shall run under the ODB's execution bound**; a hung / non-cooperative Builder **may be canceled / timed out** without stalling other Jobs. A Builder is **safe to abandon**: after cancellation it leaves no partial result (TJ-008).

- **Owner:** Builder. **Risk(s):** R-005-1, R-003-3.
- Derived From: FR-4.1 → ADR-005 → R-005-1 → ADR-003 (R-003-3) → ADR-006 (R-006-1).
- **Test:** a non-cooperative Builder is canceled/timed out without stalling other Jobs; a cooperative Builder observes cancellation promptly; a canceled Builder leaves no partial state.

**[TJ-020] Dedup-key derivation via the Builder SDK.** Each content type's Builder **shall derive its dedup key** (TJ-005) through a **shared Builder SDK / base class**, so that differing **relevant inputs** (content type, dependency state, build options) are **never collapsed** into one Job, and cancellation / incremental parsing / error reporting are handled **uniformly** across Builders.

- **Owner:** Builder. **Risk(s):** R-005-2, R-006-2.
- Derived From: FR-4.1 → ADR-005 → R-005-2 → ADR-006 (R-006-2).
- **Test:** an SDK conformance suite per Builder: key derivation (differing inputs ⇒ different keys), cancellation, incremental parsing, error injection.

---

## 4. Rule index (machine-readable)

One row per rule. This table is the grep/aggregation target for the Phase 1a and Phase 4 mechanical checks (every `TJ-*` has an ID, a Derived-From chain, an owner, and at least one of {rules a risk, is a foundation, is a deferred-mechanism}).

| ID | Rule (short) | Owner | Derived From (chain) | Rules risk(s) | Test angle |
| --- | --- | --- | --- | --- | --- |
| TJ-001 | Three-tier model (Req:Task:Job = 1:1:N) | ODB | FR-3.1 → ADR-002 → ADR-008 | (basis R-002-1) | 2 reqs → 2 tasks → 1 shared Job |
| TJ-002 | Subtask vs Job boundary (Job-only sharing) | ODB | FR-3.1 → ADR-002 note → R-002-1 | R-002-1 | no double-count across tiers |
| TJ-003 | Task lifecycle states | ODB | FR-3.1 → ADR-002 | — | terminal state exactly once |
| TJ-004 | Job lifecycle states + waiter set | ODB | FR-3.1/3.2 → ADR-002/005/006 | R-006-1/3 | cancel→no commit; success→all waiters done |
| TJ-005 | Dedup key = (file, version, inputs) | ODB+Builder | FR-3.2 → ADR-006 → R-006-2 → D-004 | R-006-2 | differing inputs ⇒ not collapsed |
| TJ-006 | Single in-flight invariant per key | ODB | FR-3.2 → ADR-006 → R-002-2 | R-002-2, R-006-2 | exactly one in-flight Job per key |
| TJ-007 | Reference-counted cancellation | ODB (Frontend cancels own Task) | FR-3.2 → ADR-006 → R-006-3 → R-008-1 | R-006-3, R-008-1, R-002-1 | last-departure cancels; no leak/lost work |
| TJ-008 | Atomic commit on success only | Builder+ODB | FR-3.2 → ADR-006 → R-006-1 → R-005-2 | R-006-1 | mid-run cancel ⇒ pre-Job state |
| TJ-009 | Priority inheritance (max of waiters) | ODB | FR-3.2 → ADR-006 → R-006-4 | R-006-4, R-002-1 | inherit/relax with no double-count |
| TJ-010 | Two-domain priority boundary (no client-type branch) | ODB (Frontend orders own) | NFR-2.3 → ADR-008 → R-007-3 → R-008-2 | R-007-3, R-008-2 | ODB paths never read client-type |
| TJ-011 | Document states 1/2/3 + reference-depth | ODB | NFR-2.3 → ADR-007 | (basis R-007-1/2) | state + depth ordering holds |
| TJ-012 | Priority recomputed each interaction | ODB | NFR-2.3 → ADR-007 → R-007-1 | R-007-1 | drop on state-1 departure |
| TJ-013 | State-1 pin bound (mechanism; threshold D-007) | ODB | NFR-2.3 → ADR-007 → R-007-1 → D-007 | R-007-1 | bounded starvation |
| TJ-014 | Unbounded-work defer/cancel (mechanism; D-007) | ODB | NFR-2.3 → ADR-007 → R-007-2 → D-007 | R-007-2 | defer/cancel keeps state consistent |
| TJ-015 | Priority-inversion bound — **deferred (D-010)**; v1 liveness via TJ-009/012/019 | ODB | NFR-2.3 → ADR-006/007 → R-006-4 → **D-010** | R-006-4 (preempt. deferred) | bounded via dispatch order + run bound (no preemption in v1) |
| TJ-016 | Config save = rebuild/invalidation event | ODB | ADR-009 → R-009-1 → ADR-004 | R-009-1 | re-scope matches saved config |
| TJ-017 | Config override rules (saved wins) | ODB | ADR-009 → R-009-2 → ADR-007 | R-009-2 | unsaved=no effect; save wins race |
| TJ-018 | Document identity/freshness = `version_id` (mtime, open_revision) | C1+ODB+Datastore | NFR-2.1 → ADR-006 → R-006-2 → D-004 | R-006-2, NFR-2.1 | open edit (rev↑) or non-open disk change (mtime↑) ⇒ invalidate/rebuild |
| TJ-019 | Builder cooperative cancel + run bound | Builder | FR-4.1 → ADR-005 → R-005-1 → R-003-3 | R-005-1, R-003-3 | non-coop Builder timed out; no stall |
| TJ-020 | Builder SDK dedup-key derivation | Builder | FR-4.1 → ADR-005 → R-005-2 → R-006-2 | R-005-2, R-006-2 | SDK conformance: keys/cancel/parsing |

## 5. Self-check (per `../README.md` §4.3)

### 5.1 Mechanical / structural (checked by grep / aggregation on the rule index)

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| M1 | Every rule has a `TJ-nnn` ID; IDs are unique | ✅ | TJ-001…TJ-020 each appear exactly once as a heading and once in §4 index (no duplicates). |
| M2 | No orphan: every rule's Derived-From chain ends at an FR/NFR (or D-decision grounded on one) | ✅ | §4 index: every chain terminates in FR-3.x / FR-4.1 / NFR-2.x / (D-004/D-007 which resolve Q-002/Q-004 and are themselves FR/ADR-grounded). |
| M3 | Every Phase-1a-required risk is ruled by ≥ 1 rule | ✅ | R-002-1/2, R-006-1..4, R-007-1..3 (all required) + R-005-1/2, R-008-1/2, R-009-1/2 — see §5.3 closure table; none missing. |
| M4 | Tables are machine-readable (stable IDs in leading cells) | ✅ | §3 state tables, §4 index, §5/§6 traceability tables all lead with the ID column. |
| M5 | Terms not redefined (single-source kept in Phase 0) | ✅ | §1 states terms are referenced, not redefined; no new definitions of Request/Task/Subtask/Job/Document/Package/Project/dedup key/priority. |

### 5.2 Semantic (LLM review, per `.agents/checklists/Traceability Check Strategy.md`)

Adequacy · semantic containment · consistency · granularity · verifiability, per the ADR *Verify* items the rules must close:

| Upstream item (ADR Verify / risk) | Status | Covered by | Missing element / reason | Suggested action |
| --- | --- | --- | --- | --- |
| ADR-002 · R-002-1 (cancel/priority accounting; subtask-vs-Job) | OK | TJ-002, TJ-007, TJ-009 | — | — |
| ADR-002 · R-002-2 (dynamic Job graph; single in-flight) | OK | TJ-006 | — | — |
| ADR-006 · R-006-1 (partial state on cancel) | OK | TJ-008 | commit *mechanism* (swap vs batch) is detailed-design — explicitly noted, not a gap | carry to Phase 3 (ODB/BLD) |
| ADR-006 · R-006-2 (dedup-key under-spec) | OK | TJ-005, TJ-006, TJ-020 | "inputs" = {content type, dependency state, options} is the agreed set; a content type needing a 4th input must extend via SDK (TJ-020) | re-check at Phase 2 reverse-check |
| ADR-006 · R-006-3 (ref-count errors) | OK | TJ-007 | — | — |
| ADR-006 · R-006-4 (priority inversion / starvation) | OK | TJ-009 + TJ-012 (dispatch order) + TJ-019 (run bound) + TJ-013/014 | v1 single-executor: liveness via dispatch order + bounded execution; **cancel-and-re-run deferred (D-010)** — no liveness benefit, only wasted-work cost | revisit only if concurrency / runtime resource priority is introduced |
| ADR-007 · R-007-1 (state-1 starvation) | OK | TJ-012, TJ-013 | pin *bound* deferred (D-007) — mechanism fixed | fill threshold in detailed design |
| ADR-007 · R-007-2 (unbounded work) | OK | TJ-014 | defer/cancel *policy* deferred (D-007) — mechanism fixed | fill policy in detailed design |
| ADR-007 · R-007-3 (two priority domains) | OK | TJ-010 | Frontend-side obligation allocated to `LSP-*` in Phase 3 (stated, not owned here) | confirm allocation at Phase 3 |
| ADR-008 · R-008-2 (no client-type branch) | OK | TJ-010 | — | — |
| ADR-009 · R-009-1 (re-scope vs in-flight) | OK | TJ-016 | — | — |
| ADR-009 · R-009-2 (override rules) | OK | TJ-017 | — | — |
| NFR-2.1 (dependency/consistency) | OK | TJ-018 | Datastore freshness invariant is ODB-owned; no Datastore public API (D-002) | — |
| NFR-3.1 (merge overlapping work) | OK | TJ-005, TJ-006 | — | — |

### 5.3 Risk-closure table (feeds `../README.md` §8 Phase 4 template)

Every `R-00x` relevant to Task/Job management is "ruled" here; the **test** column is the angle to carry into Phase 3/4. (Liveness *thresholds* remain **deferred by design** per D-007 — the rule + test angle exist, the number does not yet.)

| Risk | Ruled? | Rule ID | Test angle | Threshold status |
| --- | --- | --- | --- | --- |
| R-002-1 | ✅ | TJ-002 / TJ-007 / TJ-009 | no double-count across Subtask/Job; ref-count correct | n/a (correctness) |
| R-002-2 | ✅ | TJ-006 | exactly one in-flight Job per key; dependency order | n/a (correctness) |
| R-006-1 | ✅ | TJ-008 | mid-run cancel ⇒ pre-Job state; success ⇒ atomic | commit mechanism = detailed design |
| R-006-2 | ✅ | TJ-005 / TJ-006 / TJ-020 | differing inputs ⇒ not collapsed | key inputs = agreed set |
| R-006-3 | ✅ | TJ-007 | last-departure cancels; no leak/lost work | n/a (correctness) |
| R-006-4 | ✅ | TJ-009 / TJ-012 / TJ-019 (+ TJ-013/014) | bounded completion via dispatch order + run bound (no preemption in v1) | **cancel-and-re-run deferred (D-010)** |
| R-007-1 | ✅ | TJ-012 / TJ-013 | bounded starvation from state-1 pin | **pin deferred (D-007)** |
| R-007-2 | ✅ | TJ-014 | unbounded request defer/cancel keeps consistency | **policy deferred (D-007)** |
| R-007-3 | ✅ | TJ-010 | ODB paths never read client-type; both-sides contract | n/a (correctness) |
| R-008-1 | ✅ | TJ-007 | per-protocol cancel maps to exactly its Task | (Phase 1b per-protocol test) |
| R-008-2 | ✅ | TJ-010 | architectural test: no client-type branch | n/a (correctness) |
| R-009-1 | ✅ | TJ-016 | config save during in-flight builds ⇒ consistent | n/a (correctness) |
| R-009-2 | ✅ | TJ-017 | unsaved no effect; saved wins race | n/a (correctness) |
| R-005-1 | ✅ | TJ-019 | non-coop Builder timed out, no stall | **run bound deferred (D-007)** |
| R-003-3 | ✅ | TJ-019 | single-worker not globally stalled | **run bound deferred (D-007)** |
| R-005-2 | ✅ | TJ-008 / TJ-020 | SDK conformance (cancel/parsing/errors/keys) | n/a (correctness) |

## 6. Traceability (this document ↔ upstream)

> The **full bidirectional** matrix across the whole set is Phase 4 (`../traceability.md`). The table below is this document's **own** closure: every upstream item it was asked to rule is followed by ≥ 1 rule, and every rule traces to an upstream item.

**Upstream → TJ (does every assigned input get followed here?)**

| Upstream item | Followed by |
| --- | --- |
| FR-3.1 (tiered abstraction) | TJ-001, TJ-002, TJ-003, TJ-004 |
| FR-3.2 (dedup / priority inheritance / ref-cancellation) | TJ-005, TJ-006, TJ-007, TJ-008, TJ-009 |
| FR-4.1 (plugin builders) | TJ-019, TJ-020 |
| NFR-2.1 (data consistency) | TJ-018 |
| NFR-2.3 (robust/dynamic scheduling) | TJ-010, TJ-011, TJ-012, TJ-013, TJ-014, TJ-015 |
| NFR-3.1 (merge overlapping work) | TJ-005, TJ-006 |
| ADR-002 (three-tier model) | TJ-001…TJ-004 |
| ADR-006 (sharing) | TJ-005…TJ-009, TJ-018 |
| ADR-007 (priority) | TJ-011, TJ-012, TJ-013, TJ-014, TJ-015 |
| ADR-008 (boundary / no client branch) | TJ-007, TJ-010 |
| ADR-009 (config lifecycle) | TJ-016, TJ-017 |
| ADR-005 / ADR-003 (builder mechanism / runtime) | TJ-008, TJ-015, TJ-019, TJ-020 |
| D-004 (version_id = identity) | TJ-005, TJ-018 |
| D-007 (thresholds deferred) | TJ-013, TJ-014, TJ-019 |
| D-010 (R-006-4 cancel-and-re-run deferred) | TJ-015 |
| D-008 (mgmt=ODB / mech=Builder) | TJ-007, TJ-008, TJ-009, TJ-019, TJ-020 |

**TJ → upstream (does every rule trace out? — no orphans)**

| TJ rule | FR/NFR | ADR | Risk(s) | D / Q |
| --- | --- | --- | --- | --- |
| TJ-001 | FR-3.1 | ADR-002, 008 | R-002-1 | — |
| TJ-002 | FR-3.1 | ADR-002 | R-002-1 | — |
| TJ-003 | FR-3.1 | ADR-002 | — | — |
| TJ-004 | FR-3.1/3.2 | ADR-002/005/006 | R-006-1/3 | — |
| TJ-005 | FR-3.2 | ADR-006 | R-006-2 | D-004 |
| TJ-006 | FR-3.2 | ADR-006, 002 | R-002-2, R-006-2 | — |
| TJ-007 | FR-3.2 | ADR-006, 008 | R-006-3, R-008-1, R-002-1 | — |
| TJ-008 | FR-3.2 | ADR-006, 005 | R-006-1, R-005-2 | — |
| TJ-009 | FR-3.2 | ADR-006 | R-006-4, R-002-1 | — |
| TJ-010 | NFR-2.3 | ADR-008 | R-007-3, R-008-2 | — |
| TJ-011 | NFR-2.3 | ADR-007 | R-007-1/2 (basis) | — |
| TJ-012 | NFR-2.3 | ADR-007 | R-007-1 | — |
| TJ-013 | NFR-2.3 | ADR-007 | R-007-1 | D-007 |
| TJ-014 | NFR-2.3 | ADR-007 | R-007-2 | D-007 |
| TJ-015 | NFR-2.3 | ADR-006/007 | R-006-4 (preempt. deferred) | **D-010** (refines D-007) |
| TJ-016 | NFR-2.1 | ADR-009, 004 | R-009-1 | — |
| TJ-017 | NFR-2.1 | ADR-009, 007 | R-009-2 | — |
| TJ-018 | NFR-2.1 | ADR-006 | R-006-2 | D-004 (Q-002) |
| TJ-019 | FR-4.1 | ADR-005, 003, 006 | R-005-1, R-003-3 | — |
| TJ-020 | FR-4.1 | ADR-005, 006 | R-005-2, R-006-2 | — |

---

## 7. Items for user review (Phase 1a DoD gate)

Per `../README.md` §8 (Phase 1a *User review*), please confirm before Phase 1b:

- [x] **Two-tier priority boundary** (TJ-010): Frontend orders *its* requests; ODB orders shared work by states + depth; ODB never branches on client type — as intended? (R-007-3 / R-008-2)
- [x] **Dedup key** (TJ-005): `inputs = {content type, dependency state, build options}` is the sufficient, agreed set — and any 4th input is added via the Builder SDK (TJ-020), not a new key shape? (R-006-2)
- [x] **Starvation / unbounded** (TJ-013/014) and **Builder run bound** (TJ-019): mechanism classes fixed, thresholds **deferred (D-007)** — accepted? (R-007-1/2, R-005-1, R-003-3)
- [x] **Priority-inversion (TJ-015) deferred (D-010):** v1 is **single-executor / non-preemptive**; priority affects dispatch order only; **cancel-and-re-run is not a v1 mechanism** (wasted-work cost, no liveness benefit); liveness closed by TJ-012/019/013/014. Revisit only if concurrency / runtime resource priority is introduced — accepted? (R-006-4)
- [x] **Q-002 resolved** via **D-004** (TJ-018): identity/freshness = **`version_id` = (last-save mtime, open_revision)** — open files use the **buffer** (`didChange` version), non-open files use the **disk** (`didChangeWatchedFiles` + mtime); the tuple is computed by **C1** and used by ODB as the dedup-key version + Datastore freshness invariant. **Both open and non-open files are covered** — no separate labeled-version layer needed in v1?
- [x] **Builder obligations** (TJ-019/020) included in *this* contract (vs. Phase 3 only) so Phase 3 can allocate them to `BLD-*` — agree?
- [x] **Rule count/scope:** 20 rules, TJ-001…TJ-020, all Owner-tagged to a single component — nothing double-owned / unowned?

**DoD status (per `../README.md` §8 Phase 1a):**

- All ADR-002/006/007/009 *Verify* items + risks turned into rules — **met** (§5.2 / §5.3; all `OK`).
- State-transition table present (Task + Job) — **met** (§3.1).
- Dedup key + priority rules explicit — **met** (TJ-005…TJ-009, TJ-010…TJ-015).
- Q-002 resolved — **met** (TJ-018, via D-004).
- **Verdict: DoD met**, pending the §7 confirmations above (esp. the D-007 deferral acceptance).
