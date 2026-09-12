# gdoc Server — Sub-component Inventory & Glossary (Phase 0)

> **Deliverable of:** Phase 0 (grounding) of the gdoc Server design-documentation effort.
> **Position:** `docs/architecture/gdocServer/subcomponents/README.md`
> **Status:** Draft for user review (Phase 0 — not yet approved).
> **Companion files (created in later phases):**
> `language-server.md` · `object-database.md` · `object-datastore.md` · `object-builders.md` (Phase 3);
> `../contracts/frontend-odb-api.md` (Phase 1b); `../contracts/task-job-management.md` (Phase 1a).

> **Derived From:**
> `../requirements/requirements.md` (FR-1.1…4.1, NFR-1.1…3.1) ·
> `../adr/001-protocol-agnostic-core.md` … `../adr/009-configuration-lifecycle.md` ·
> `../adr/README.md` (risk register, R-00x-y) ·
> `../architecture.md` (Structure / Key Abstractions / Behaviour) ·
> `.agents/checklists/Architecture Design Checklist.md` (role & boundary clarity; Golden Rules)

---

## 1. Purpose & Position

This file is the **grounding document** for the whole sub-component design. It fixes, once and
only once, two things that every later phase (1a, 1b, 2, 3, 4) must agree with:

1. **Who owns what** — an inventory of the components and a **single-owner** responsibility matrix,
   so no later phase can silently assign one responsibility to two places (or to none).
2. **What the terms mean** — a single, unambiguous definition for each core term
   (Request / Task / Subtask / Job / Document / Package / Project / dedup key / priority).

It intentionally defines **no behaviour and no API shape**. It is the shared vocabulary and the
"single owner" rule that Phase 3 uses when it assigns component requirements
(`LSP-nnn / ODB-nnn / DS-nnn / BLD-nnn`) and that Phase 4 uses to check that nothing is orphaned
or double-owned.

> **ID note:** Component *requirement* IDs (`LSP-nnn / ODB-nnn / DS-nnn / BLD-nnn`) are **not**
> assigned here — they are assigned in Phase 3. This file fixes the *component set* and the *terms*
> those requirements will reference. The matrix rows carry Phase-0 inventory anchors `INV-01…INV-29`
> (deliberately distinct from the risk IDs `R-NNN-M`).

## 2. Scope (v1)

Fixed by the Decisions Log in `../README.md` §7:

- **D-005 — v1 functional scope:** `didOpen/didChange/didClose` (sync), `didChangeWatchedFiles` +
  save (config), **Hover** (depth 0), **Go-to-Definition** (depth 1), **Find References**
  (unbounded), **Diagnostics** (server→client). Completion / Rename / Document Symbols / Semantic
  Tokens are **v2 (provisional)**.
- **D-006 — Object Server is excluded from v1** (future second frontend; see §5.4).

The component *set* below is therefore stable across v1/v2; only the *feature scope* differs.

## 3. Component Inventory

Four v1 components plus one future frontend. The public API exists **only** on the
Frontend↔ODB boundary (D-002).

| # | Component | Type | Position in the core | Public API? | Derived From |
| --- | ----------- | ------ | ---------------------- | ------------- | -------------- |
| C1 | **gdoc Language Server** (LSP Frontend) | Protocol frontend | Swappable frontend over the shared core | **Yes** (the LSP side) | FR-1.1/1.2/1.3, NFR-1.1; ADR-001, ADR-008, ADR-003 |
| C2 | **gdoc Object Database** (ODB) | Core orchestrator / single coordinator | Center: maps Requests→Tasks, schedules, dedups, hosts Builders | **Yes** (the ODB side of the *only* public API) | FR-3.1/3.2, NFR-1.2/2.1/2.2/2.3/3.1; ADR-002/003/004/006/007/008/009 |
| C3 | **gdoc Object Datastore** | Internal data substrate | **Inside** the ODB (encapsulated) | **No** (internal only) | ADR-004, NFR-1.3; R-004-1 |
| C4 | **gdoc Object Builder(s)** | Plugin (one per content type) | **Downstream** of the ODB; executes Jobs | **No** (invoked by ODB only) | FR-2.1/4.1; ADR-005/006/008; R-005-1/2 |
| C5 | **gdoc Object Server** | *Future* second frontend | Replaces C1 as a frontend over the same core | (future) | FR-2.3; ADR-001; **D-006 (excluded from v1)** |

> **Why this cut:** C1 and C5 are *swappable frontends* over the *same* core (ADR-001), so the
> core = C2 + C3 + C4. C3 is deliberately **not** a peer service — it is the ODB's internal store
> (ADR-004) — and C4 is a **plugin** the ODB hosts (ADR-005). The rest of the design assumes this
> cut; please confirm it in §9.

---

## 4. Responsibility Ownership (single owner)

**Rule (ADR-008):** *every decision — every priority / ordering / cancellation / build decision —
has exactly one owner.* The matrix therefore assigns **exactly one** component per
responsibility. A responsibility owned by two components is a defect; one owned by nobody is a
defect.

### 4.1 Single-owner matrix

| ID | Responsibility (what is decided / done) | **Single owner** | Basis (ADR / FR / R) |
| ---- | ------------------------------------------ | ------------------ | ---------------------- |
| INV-01 | LSP protocol handling & session lifecycle (init/shutdown) | **C1 Frontend** | FR-1.1; ADR-001 |
| INV-02 | Translate LSP messages ↔ Requests; results ↔ LSP notifications | **C1 Frontend** | ADR-001, ADR-008 |
| INV-03 | Apply **client-type-specific** request priority, ordering, cancellation | **C1 Frontend** | ADR-008 |
| INV-04 | Track its own open documents & focus | **C1 Frontend** | ADR-008 |
| INV-05 | Document sync (`didOpen/didChange/didClose`) → background work | **C1 Frontend** | FR-1.3 |
| INV-06 | Project & package scoping (watch workspace root / config) | **C1 Frontend** | architecture.md |
| INV-07 | Dispatch diagnostics/tokens/errors to the client as notifications | **C1 Frontend** | FR-1.2; architecture.md |
| INV-08 | Register completion callback; hand events onto its own loop | **C1 Frontend** | ADR-003 (R-003-1/2) |
| INV-09 | Map a Request 1:1 to a Task | **C2 ODB** | ADR-002, ADR-008 |
| INV-10 | Task lifecycle / priority / cancellation (protocol-agnostic) | **C2 ODB** | ADR-007, ADR-008 |
| INV-11 | Decompose a Task into Subtasks and/or Jobs | **C2 ODB** | ADR-002, ADR-008 |
| INV-12 | Job dedup registration & single-in-flight invariant | **C2 ODB** | ADR-006, ADR-008 (R-006-3) |
| INV-13 | Priority-inheritance bookkeeping (Job takes max of its waiters) | **C2 ODB** | ADR-006 (R-006-4) |
| INV-14 | Reference-counted cancellation (active while ≥1 waiter) | **C2 ODB** | ADR-006 (R-006-3) |
| INV-15 | State-based scheduling (states 1/2/3 + reference-depth) | **C2 ODB** | ADR-007 |
| INV-16 | Dependency-graph management across Packages | **C2 ODB** | FR-2.1, NFR-2.1; architecture.md |
| INV-17 | Config save = rebuild event (re-scope / invalidation) | **C2 ODB** | ADR-009 (R-009-1) |
| INV-18 | Exclusive coordination / single-writer over the Datastore | **C2 ODB** | ADR-004 (R-004-1) |
| INV-19 | Public synchronous, non-blocking facade to frontends | **C2 ODB** | ADR-003, ADR-004 |
| INV-20 | Push completion callback (on the ODB worker thread) | **C2 ODB** | ADR-003 |
| INV-21 | Host Builder plugins (lifecycle) & dispatch Jobs to them | **C2 ODB** | ADR-005, ADR-008 |
| INV-22 | **Execute** a Job (Parse/Link/Compile) | **C4 Builder** | FR-2.1; ADR-005 |
| INV-23 | **Derive** the Job dedup key (per content type, via SDK) | **C4 Builder** | R-006-2, R-005-2 |
| INV-24 | **Cooperative** cancellation inside a running Job | **C4 Builder** | R-005-1; ADR-005 |
| INV-25 | **Atomic commit** of results (on success only) | **C4 Builder** | R-006-1 |
| INV-26 | Produce diagnostics / tokens / symbols for a document | **C4 Builder** | FR-1.2/FR-2.1; architecture.md |
| INV-27 | Store gdoc objects & relationships (in-memory) | **C3 Datastore** | ADR-004; NFR-1.3 |
| INV-28 | Fast state retrieval / lookup for the ODB | **C3 Datastore** | NFR-1.3 |
| INV-29 | Maintain physical link/relationship integrity | **C3 Datastore** | NFR-2.1; architecture.md |

### 4.2 The one near-duplication, resolved

`architecture.md` lists *Job Deduplication / Priority Inheritance / Reference-based Cancellation*
under the **Builder's** characteristics. The ADRs are higher authority here (see the source-of-
truth order) and split the concern cleanly; we adopt that split:

- **Management / bookkeeping** — *which* unit is shared, reference counting, priority inheritance,
  the cancel **decision** → **C2 ODB** (INV-12 / INV-13 / INV-14). Basis: ADR-006 ("Reference
  counting is centralized in the ODB; frontends only cancel their own tasks"), ADR-008 (the ODB
  "deduplicates shared processing … into shared Jobs").
- **Mechanism** — Job **identity** (dedup key), **execution**, cooperative cancel, atomic commit →
  **C4 Builder** (INV-22 / INV-23 / INV-24 / INV-25). Basis: ADR-005 (Builders are the only
  component that converts source into objects), R-006-2 (key-derivation helper from the builder
  SDK), R-006-1 (results committed atomically on success only).

So there is no double owner: the ODB *decides* the sharing; the Builder *performs* it.
*(Flagged for explicit user confirmation in §9.)*

### 4.3 Non-responsibilities (what each does NOT do)

Preventing "two places own it" requires stating the negative side as clearly as the positive.

- **C1 Frontend:** never schedules Jobs directly; never owns the Task lifecycle or the
  cancellation of work it did not submit; never touches the Datastore; never branches on core
  semantics. (ADR-002, ADR-004, ADR-008)
- **C2 ODB:** never branches on client type; never parses content (delegates to a Builder);
  never exposes the Datastore; never holds protocol-specific state. (R-008-2, ADR-005, ADR-004,
  ADR-001)
- **C3 Datastore:** **no public API**; no internal locking / thread-safety; no persistence; no
  direct frontend or external access. (ADR-004, R-004-1)
- **C4 Builder:** no scheduling (the ODB schedules); no direct Datastore access (it commits
  through the ODB); no frontend interaction; no cross-content-type assumptions. (ADR-005, ADR-008)

---

## 5. Boundaries (the contracts)

The boundaries are the load-bearing walls. Later phases must not move them without a Decisions-Log
entry.

### 5.1 Frontend ↔ ODB = the **only** public API

The **sole** public API in the system is the Frontend↔ODB contract (D-002). It is synchronous,
lightweight, and non-blocking: a heavy request returns a **request id** and its completion is
**pushed back** via a pre-registered callback; **polling is forbidden**. The exact operation set
and Request model are specified in **Phase 1b** (`../contracts/frontend-odb-api.md`).
(ADR-003, ADR-004, ADR-008)

### 5.2 Datastore is **internal** to the ODB

The Datastore has **no public API** and **no internal locking**; it is reached **only** through
the ODB, which is the single writer/coordinator. This is what keeps the Datastore "dumb" and safe.
(ADR-004, R-004-1)

### 5.3 Builder is **downstream** of the ODB

The ODB hosts Builders as plugins and dispatches atomic Jobs to them; a Builder may run as a
**subprocess** (one launch = one Job). A Builder commits its results **back through the ODB** and
never touches the Datastore directly. (ADR-005, ADR-008)

### 5.4 Object Server (future) — a second frontend, not a writer

The Object Server (C5) is realized by adding a **second frontend** over the **same** core, not by
rebuilding the core. Until delivered it is **excluded from v1** (D-006); when delivered it is
**read-only initially**, or its writes are **routed through the same mutation API** so the ODB
remains the single writer. (ADR-001, R-001-1)

---

## 6. Glossary — single definitions

Each term is defined **once** here. Later documents *reference* these definitions; they must not
redefine them. "Single Source" names the authoritative text; "Derived From" is the chain.

| Term | Single definition | Single Source | Derived From |
| ------ | ------------------- | --------------- | -------------- |
| **Request** | One external interaction initiated by a client, expressed protocol-specifically (an LSP command/notification, or a future Object API call). **One request always maps to exactly one Task** (1:1 at the Request↔Task boundary). | ADR-002, ADR-008 | FR-3.1 |
| **Task** | A **protocol-agnostic** unit of internal orchestration, owned and managed by the ODB. Carries the priority, lifecycle, and cancellation the ODB assigns; decomposes into Subtasks and/or requests Jobs. It is the 1:1 target of a Request. | ADR-002, ADR-008 | FR-3.1, NFR-2.3 |
| **Subtask** | The **task-local** management unit inside a Task (a step the Task owns, e.g. "link document X for this Task"). **Not shared** across Tasks and **not deduplicated**; a Task may contain several. | ADR-002 (note) | FR-3.1 |
| **Job** | The **atomic, (potentially shared)** unit of execution (Parse/Link/Compile) dispatched to a Builder. Identified by a **dedup key**; multiple Tasks may await the same Job; dedup, priority inheritance, and reference-counted cancellation happen **at this level** (below the Task). One Builder launch = one Job. | ADR-002, ADR-005, ADR-006, ADR-008 | FR-3.1/3.2, NFR-3.1 |
| **Document** | A single source file within a Project (e.g. a `.gdoc` or `.doxml` file); the unit of parsing/analysis. Carries the ADR-007 priority **states** (1: referenced by an active request; 2: open in the editor; 3: part of a package) and a monotonic **`version`** revision. | architecture.md; ADR-007; D-004 | FR-2.2 |
| **Package** | The fundamental unit of **content and distribution**. A Project holds one or more internal packages and may reference external ones. **Package membership (state 3)** is set by configuration and **applied on save**. | architecture.md; ADR-009 | FR-2.2 |
| **Project** | The **root** organizational unit of gdoc; maps **1:1 to a VSCode Workspace**; the top-level container for configuration and resources; contains Packages. | architecture.md | FR-2.2 |
| **dedup key** | The identity of a Job used for deduplication: it captures the **target document + its version + the relevant inputs** (content type, dependency state, build options) so that identical work shares one Job and differing inputs do **not** collapse. The exact rule is fixed in **Phase 1a** (`../contracts/task-job-management.md`, `TJ-`); this file fixes only the **term**. | ADR-006; R-006-2; D-004 | FR-3.2 |
| **priority** | A **two-domain** scheduling rank. (a) **Frontend:** which of *its* Requests matter and in what order (client-type-specific). (b) **ODB:** which shared work runs first — per-document states 1/2/3 + reference-depth from open text, recomputed on each interaction. In addition, a Job **inherits the highest priority** of the Tasks awaiting it. Exact thresholds/policies (starvation / unbounded / inversion) are **deferred** to detailed design. | ADR-007; ADR-008; ADR-006; D-007 | NFR-2.3 |

### 6.1 Subtask vs Job — the load-bearing distinction (define once, reference forever)

> **Subtask = task-local management unit. Job = shared execution unit.**
>
> A Task contains Subtasks (its own steps). A Task *requests* Jobs (shared work) from Builders.
> Because deduplication / sharing happens **at the Job level, below the Task level**, it does
> **not** break the "one request → one task" invariant: two requests still produce two Tasks;
> they may simply await the **same** Job. (ADR-002 note; ADR-006)
>
> Consequence for every later document: **never** describe dedup / cancellation / priority
> inheritance at the *Subtask* level — that is a Job-level concern (owned by the ODB; see
> INV-12 / INV-13 / INV-14).

---

## 7. Phase 0 Self-Check

Executed against `../README.md` §8 (Phase 0 検証観点) and
`.agents/checklists/Architecture Design Checklist.md` (Golden Rules: unique ID, single
responsibility per file, link integrity; "role & boundary clarity").

| # | Check | Result | Note |
| --- | ------- | -------- | ------ |
| S1 | Every responsibility is owned by **exactly one** component (no 0-owner, no 2-owner) | ✅ | INV-01…INV-29 each have one owner; §4.2 resolves the only near-duplication (dedup mgmt = ODB, mechanism = Builder). |
| S2 | Term definitions do not contradict any ADR | ✅ | Each term's Single Source is an ADR/architecture passage; subtask vs Job matches the ADR-002 note; priority matches ADR-007/008; dedup key matches ADR-006 / R-006-2. |
| S3 | "Only the Frontend↔ODB boundary is a public API" is explicit | ✅ | §3 table + §5.1 + §4.3 (C3/C4 have no public API). |
| S4 | Object Server is marked "future / read-only or via the same mutation API" | ✅ | §3 (C5) + §5.4 (D-006, ADR-001, R-001-1). |
| S5 | Single responsibility per file; unique IDs; links resolvable | ✅ | One topic (inventory + glossary); `C1…C5` component IDs + `INV-01…INV-29` anchors; relative links to ADR/FR/architecture. |

**Gaps / caveats found (for user review):**

- **G1 (§4.2) — RESOLVED (2026-09-11):** `architecture.md` had attributed job *dedup / priority /
  ref-cancel* to the **Builder**. Reconciled: `architecture.md` §2 (ODB) now owns *management* and
  §4 (Builder) is *mechanism-only*, per ADR-008 / R-006-3 (higher authority than the former wording).
- **G2 — RESOLVED (user confirmed, 2026-09-11):** FR-3.2 lists "Job Deduplication / Priority
  Inheritance / Reference-based Cancellation" as capabilities; their *management* is owned by the ODB
  (INV-12/13/14) and the *mechanism* by the Builder (INV-22…INV-25). Confirmed the ODB (not the
  Builder) is the intended owner of the *management*.
- **G3 — CONFIRMED (2026-09-11, user):** The **dedup key** is *defined* — `(file, version, inputs)`
  (version = the LSP `version`, **D-004**; identity per R-006-2) — to be formalized as a `TJ-` rule in
  **Phase 1a**. The **priority-policy thresholds** (starvation / unbounded / priority-inversion) are
  *deferred* to detailed design (**D-007**), with the mechanism classes fixed (R-007-1 / R-007-2 / R-006-4).
  "Key + classes now, exact rule/thresholds later" split **accepted**.

---

## 8. Traceability (this file → upstream)

| Upstream item | Followed here |
| --------------- | --------------- |
| FR-1.1 / 1.2 / 1.3 | C1 responsibilities INV-01…INV-07; Glossary (Request) |
| FR-2.1 / 2.2 | INV-16, INV-22, INV-26, INV-27…INV-29; Glossary (Document/Package/Project) |
| FR-3.1 / 3.2 | INV-09…INV-26; Glossary (Task/Subtask/Job/dedup key/priority) |
| FR-4.1 | C4 Builder; §5.3 |
| FR-2.3 | C5 Object Server; §5.4 |
| NFR-1.1 / 1.2 / 1.3 | C1 (INV-08), C2 (INV-19/INV-20), C3 (INV-27/INV-28) |
| NFR-2.1 / 2.2 / 2.3 | INV-16, INV-10/INV-19, INV-15 |
| NFR-3.1 | INV-12 (dedup) |
| ADR-001…009 | §3, §4, §5, §6 (cited inline) |
| R-001-1, R-002-1/2, R-003-1/2, R-004-1, R-005-1/2, R-006-1/2/3/4, R-008-2, R-009-1 | §4.1 (inline), §5 |

*(The full two-direction trace matrix is produced in Phase 4 — `../traceability.md`.)*

---

## 9. Items for User Review (Phase 0 DoD gate)

Per the Resume Protocol, I stop here for your review before Phase 1a.

- [x] **Component cut (4 + 1 future):** C1 Frontend / C2 ODB / C3 Datastore / C4 Builder /
  C5 (future Object Server) — as assumed? (Builder treated as an independent component.)
- [x] **Datastore = internal, no public API** (only the ODB touches it) — agreed?
- [x] **v1 scope:** Object Server excluded (D-006) — confirmed?
- [x] **§4.2 resolution:** job dedup / priority / ref-cancel **management = ODB**, **mechanism =
  Builder** — RESOLVED (G1 reconciled in `../architecture.md` §2/§4; G2 confirmed by user, 2026-09-11).
- [x] **Glossary (§6):** the nine single definitions — any term misdefined?

**DoD status:** **Phase 0 CLOSED (2026-09-11).** Deliverable produced (`subcomponents/README.md`);
single-owner matrix + glossary + boundaries complete; all §9 items approved by user; G1/G2 resolved
(architecture.md §2/§4 reconciled per ADR-002 / ADR-008 / R-006-3) and recorded as **D-008** in
`../README.md` §7; G3 confirmed (dedup key defined per D-004; priority-policy thresholds deferred per D-007).
**Proceeding to Phase 1a** — `../contracts/task-job-management.md`.
