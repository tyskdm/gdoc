# gdoc Server — Design Document Set

> This folder is the **design-documentation set** for the gdoc Server: its requirements, the
> architectural decisions and risks, the contracts, the use-case analysis, the per-component
> requirements, and the traceability that closes them.
>
> **This `README.md` is the single index for the set.** It defines (1) what documents exist and their
> roles, (2) how they **derive from one another**, (3) the **conventions** they all share, (4) the
> current **status**, and (5) — most importantly — **how to change them safely**, including *after*
> the design is complete.
>
> **Read this file first in every session.** If a decision here conflicts with the chat history,
> **this file wins** — it is the resumable source of record.

## 1. Document Map

The set is organized by **role in the derivation chain** (see §3). Current state:

| Role | File(s) | What it holds | Status |
| --- | --- | --- | --- |
| Top-level requirements | `requirements/requirements.md` | FR-*/NFR-* — the "what"; **origin of all IDs** | existing |
| Strategic decisions | `adr/001…009-*.md` | ADR-* — how the requirements are satisfied | existing |
| Risk register | `adr/README.md` | R-NNN-* — risks to turn into rules + tests | existing |
| Architecture | `architecture.md` | Structure, behavior, abstractions (Workspace/Project/Package) | existing |
| Contract: Task/Job rules | `contracts/task-job-management.md` | TJ-* — the shared-execution model | ✅ approved (Phase 1a, 2026-09-11) |
| Contract: public API | `contracts/frontend-odb-api.md` | API-* operations + Request/Result model | ✅ approved (Phase 1b, 2026-09-13) |
| Use-case analysis | `usecases/UC_*.md` | Behavioral evidence; IF/ST/DR/EH/SCR derived per component | 🟡 in progress (Phase 2; UC-001…003 ✅, UC-004…011 ⬜) |
| Use-case drafts | `usecase_analysis/*.md` | Raw analysis; **to be merged into `usecases/`** (D-003) | in-flight |
| Responsibility inventory + glossary | `subcomponents/README.md` | Component/responsibility inventory, single-owner matrix, glossary | **done** (Phase 0) |
| Component requirements | `subcomponents/{language-server,object-database,object-datastore,object-builders}.md` | LSP-*/ODB-*/DS-*/BLD-* — per-component requirement sets | **planned** (Phase 3) |
| Traceability + closure | `traceability.md` | Full bidirectional trace matrix + risk closure | **planned** (Phase 4) |
| **Phase process** | `process/phase2/{plan,skill,template}.md` | Phase 2 work tracker + tailored skill + template | **active** (Phase 2) |
| **Design review record** | `process/design_review_record.md` | Cross-document consistency/completeness review of Phase 0–1b (NC-*/OM-* findings) | **active** (findings ongoing) |

**Two related folders, one rule.** `usecases/` (formal, `UC_*`) and `usecase_analysis/` (raw drafts)
currently coexist. Per **D-003** the plan is **option A**: `usecases/` is canonical and
`usecase_analysis/` is absorbed (its LSP links / sequence diagrams / the `6. Update Document` Task
Queue note) into `UC_*`, then removed or archived. Settle this before Phase 2 so traceability does
not double-count.

**Final shape (target):**

```
docs/architecture/gdocServer/
├─ README.md                         # THIS FILE — index + governance
├─ requirements/requirements.md      # top-level requirements (ID origin)
├─ architecture.md                   # structure / behavior / abstractions
├─ adr/                              # 001…009 + README.md (risk register)
├─ contracts/
│  ├─ task-job-management.md         # Phase 1a — TJ-* rules
│  └─ frontend-odb-api.md            # Phase 1b — API-* operations
├─ usecases/                         # UC_*.md (formal; absorbs usecase_analysis/)
├─ usecase_analysis/                 # raw drafts (absorbed → removed/archived per D-003)
├─ subcomponents/
│  ├─ README.md                      # Phase 0 — inventory + glossary (done)
│  ├─ language-server.md             # Phase 3 — LSP-*
│  ├─ object-database.md             # Phase 3 — ODB-*
│  ├─ object-datastore.md            # Phase 3 — DS-*
│  └─ object-builders.md             # Phase 3 — BLD-*
├─ process/                          # per-phase work tools + review records
│  ├─ design_review_record.md        # cross-document review of Phase 0–1b (NC-*/OM-*)
│  └─ phase2/
│     ├─ plan.md                     # Phase 2 work tracker (status + decision log)
│     ├─ skill.md                    # Phase 2 analysis method (tailored)
│     └─ template.md                 # Phase 2 output format (tailored)
└─ traceability.md                   # Phase 4 — bidirectional matrix + risk closure
```

## 2. Sources of Truth (priority order)

When two documents disagree, the **higher-ranked** one wins. A change to a source of truth must
follow §6 (Change Guideline) and be recorded in §7.

| Rank | Document | Role |
| --- | --- | --- |
| 1 | `requirements/requirements.md` | Top-level requirements (FR-*/NFR-*). **Origin of all requirement IDs.** |
| 2 | `adr/*.md` (001–009) + `adr/README.md` | Strategic decisions (ADR-*) + risks (R-NNN-*). **Basis of the contracts.** ADRs are strategic decisions — do not change them without user confirmation. |
| 3 | `architecture.md` | Structure, behavior, abstractions (Workspace/Project/Package). |
| 4 | `usecases/UC_*.md` | Behavioral analysis (template-based; IF/ST/DR/EH/SCR IDs). |
| 5 | `contracts/`, `subcomponents/*.md`, `traceability.md` | Executable specifications **derived** from ranks 1–4. |

## 3. Derivation & Dependency Model

The load-bearing map of the set: **what derives from what**, and **what must be re-checked when
something changes**.

### 3.1 The derivation chain

```
Rank 1   requirements (FR/NFR)                         ── the "what"; origin of IDs
   │
Rank 2   ADRs (decisions) + risk register (R-NNN-*)    ── constraints / "how" at the strategy level
   │        (architecture.md supplies structure & abstractions)
   ▼
 ┌───────────────────────────────┬───────────────────────────────────┐
 ▼                               ▼                                   ▼
contracts: TJ-* rules          contracts: API-* operations          usecases: UC_*
(Task/Job management model)     (Frontend↔ODB surface)              (behavioral evidence;
                                                                       IF/ST/DR/EH/SCR per component)
 └───────────────────────────────┴───────────────────────────────────┘
   ▼
subcomponents: LSP-*/ODB-*/DS-*/BLD-*
   = (contract obligations) ∪ (behavior obligations), each carrying a Derived-From chain
   ▼
traceability.md — full bidirectional matrix + risk closure ("nothing is orphaned")
```

Key properties:

- **Contracts are the "rails."** Phase 1a (TJ-*) and Phase 1b (API-*) formalize the ADRs into
  checkable rules *before* any component is specced, so Phase 3 can *verify against* them.
- **A component requirement is a union.** Every `LSP-*/ODB-*/DS-*/BLD-*` requirement is
  *(contract obligation ∪ behavior obligation)* and must carry a Derived-From chain up to FR/NFR.
- **Single owner.** Every responsibility and every decision has **exactly one** owner (ADR-008);
  see the single-owner matrix in `subcomponents/README.md` §4.

### 3.2 Change propagation (what to re-check when you change what)

| You change… | Re-derive / re-verify… |
| --- | --- |
| A requirement (FR/NFR) | Contracts (TJ-/API-) citing it → UCs covering it → all component reqs citing it → traceability. |
| An ADR or a risk (R-*) | **Confirm with user first** (§6). Then every dependent TJ-/API-/component req and its risk-closure entry. |
| Architecture (structure / abstractions in `architecture.md`) | UCs relying on those abstractions → component reqs citing them → traceability. |
| A contract rule (TJ-*/API-*) | UCs (do they still satisfy it?) → component reqs citing it → traceability. |
| A use case (UC_*) | Component reqs derived from it → traceability. |
| A component req (LSP/ODB/DS/BLD) | Its Derived-From chain (still valid?) → traceability. |
| A glossary term | All documents using the term (`subcomponents/README.md` §6 is the definition home). |

**Invariant:** no ID may ever lose its Derived-From chain, and no requirement may be orphaned from a
FR/NFR. The Phase 4 matrix (§8) is the machine check for this.

### 3.3 Reusable agent assets

- **Phase 2 skill (tailored):** `process/phase2/skill.md` — analysis method for UCs.
- **Phase 2 template (tailored):** `process/phase2/template.md` — UC output structure.
- **Generic skill (base):** `.agents/skills/usecase-analysis/SKILL.md` — the upstream of the tailored skill.
- **Generic template (base):** `.agents/templates/use-case-analysis-template.md` — the upstream of the tailored template.
- **Checklists:** `.agents/checklists/Traceability Check Strategy.md` (Phase 3/4 semantic checks),
  `.agents/checklists/Architecture Design Checklist.md`.

> **Rule:** When a phase has a tailored skill/template under `process/`, **use the tailored version**,
> not the `.agents/` originals. The `.agents/` files are the generic base for tailoring.

## 4. Conventions (apply to every document in this set)

### 4.1 ID scheme

| Kind | Format | Example | Home |
| --- | --- | --- | --- |
| Top-level requirement | `FR-n.m` / `NFR-n.m` | `FR-1.2`, `NFR-2.2` | `requirements/requirements.md` |
| Decision | `ADR-NNN` | `ADR-008` | `adr/` |
| Risk | `R-NNN-M` | `R-006-3` | `adr/README.md` |
| Use case | `UC-nnn` | `UC-002` | `usecases/` |
| Derived requirement | `IF-<UC>-<NNN>` / `ST-<UC>-<NNN>` / `DR-<UC>-<NNN>` / `EH-<UC>-<NNN>` / `SCR-<COMP>-<UC>-<NNN>` (per-UC namespace, e.g. `IF-002-001`, `SCR-C1-002-001`) | `usecases/` |
| Component requirement | `LSP-nnn` / `ODB-nnn` / `DS-nnn` / `BLD-nnn` | `ODB-001` | `subcomponents/` |
| API operation | `API-nnn` | `API-001` | `contracts/frontend-odb-api.md` |
| Task/Job rule | `TJ-nnn` | `TJ-001` | `contracts/task-job-management.md` |
| Facade obligation | `F<n>.<m>` | `F6.1` | `contracts/frontend-odb-api.md` §6 |

### 4.2 "Derived From" format

Every lower-level requirement states its upstream chain on **one line**. Example:

```
[ODB-007] …
  Derived From: FR-3.2 → ADR-006 → R-006-3 → TJ-003 / UC-002
```

### 4.3 Verification policy

- **Mechanical (structural):** every requirement has an ID; no duplicate IDs; no orphans in the
  trace matrix. Keep tables machine-readable so these are checked by grep/aggregation.
- **Semantic (LLM review):** adequacy, semantic containment, consistency, granularity,
  verifiability. Apply `.agents/checklists/Traceability Check Strategy.md` and report in this table:

  | Requirement ID | Status (OK / Partial / NG) | Missing element / reason | Suggested action |
  | --- | --- | --- | --- |

### 4.4 Diagrams

- Use **Mermaid** for all diagrams (sequence, flow, state).
- **Do not include `;` (semicolon) inside Mermaid `note` text** — it causes a parse error.
  Use `·` or line breaks (`<br>`) as separators within notes.

### 4.5 Gate rule

- **Do not proceed to the next step or phase without explicit user approval.**
- After each deliverable, report per §6 (3-point set: DoD / Gaps / Pending).
- Strategic decisions (ADR-level, scope-level) **must** be confirmed with the user before being
  recorded as decided.

## 5. Status

**Current phase:** **Phase 2 🟡 IN PROGRESS** (UC-001/002 ✅ 2026-09-15; UC-003 ✅ 2026-09-25; UC-004…011 ⬜). Phase 0 / 1a CLOSED (2026-09-11); Phase 1b CLOSED (2026-09-13).

| Phase | Purpose | Deliverable | Status |
| --- | --- | --- | --- |
| 0 | Grounding: component/responsibility inventory + glossary | `subcomponents/README.md` | ✅ done (2026-09-11) |
| 1a | Task/Job management rules (goal #3) | `contracts/task-job-management.md` | ✅ approved / closed (2026-09-11) |
| 1b | Frontend↔ODB API (goal #2) | `contracts/frontend-odb-api.md` | ✅ approved / closed (2026-09-13) |
| 2 | Unify use-case analysis (behavioral evidence) | `usecases/UC_*.md` | 🟡 in progress (UC-001/002 ✅ 2026-09-15; UC-003 ✅ 2026-09-25; UC-004…011 ⬜) |
| 3 | Component requirement allocation (goal #1) | `subcomponents/*.md` | ⬜ not started |
| 4 | Final verification: traceability + risk closure | `traceability.md` | ⬜ not started |

**Open-question register** (all answered; a new *open* question must be asked of the user before it
may be assumed):

| ID | Question | Status | Answer |
| --- | --- | --- | --- |
| Q-001 | v1 functional scope | answered | **D-005** (v1 = sync + config + Hover + GoToDefinition + FindReferences + Diagnostics; v2 provisional) |
| Q-002 | Document freshness / identity method | answered | **D-020** (refines D-004) (`version_id` is state-relative: open=buffer `open_revision`, non-open=disk mtime; staleness scoped to the open generation) |
| Q-003 | Is Object Server excluded from v1 | answered | **D-006** (excluded) |
| Q-004 | starvation / unbounded policy | answered | **D-007** (defer to detailed design; fix mechanism classes only) |
| Q-005 | Two-folder merge policy | answered | **D-003** (option A) |

## 6. Change Guideline (how to change this set safely)

Use this **both during** the remaining phases and **after** the design is complete.

1. **Classify the change** (which rank in §2 / which kind in §4.1): requirement · ADR/risk ·
   contract (TJ-/API-) · use case · component requirement · glossary term.
2. **Follow §3.2** to list everything that must be re-derived / re-verified, and update those
   documents **in the same pass**.
3. **Hard rules:**
   - An **ADR** is a strategic decision — **always confirm with the user before changing it** (and
     record the change in §7).
   - Keep **single-source-of-truth**: status and decisions live **only** in this file; do not create
     a second home.
   - Every decision gets an entry in **§7** (append-only).
   - After any change, **re-run the affected traceability** (§4.3: mechanical + semantic checks).
4. **Reporting format** (at the end of each phase / change), the 3-point set:
   1. **DoD met?** (met / unmet + reason).
   2. **Gaps found** (missing / conflicting / at-risk).
   3. **Pending decisions** (questions for the user).

## 7. Change History (Decisions Log)

> **Append-only.** Records user decisions and plan-level commitments — only new entries are added.
> Git records *what* changed; this log records *why*. This is the **single canonical** change
> history for the set.

| ID | Date | Decision | Rationale | Status |
| --- | --- | --- | --- | --- |
| D-001 | 2026-09-11 | Execution order = **goal #3 → goal #2 → (behavior unification) → goal #1** (Phase 1a/1b before goal #1) | Allocation (goal #1) is the thing being verified; it can only be verified once the reference (API + Task/Job) exists. ADRs already fix ~80%, so this is cheap. | ✅ |
| D-002 | 2026-09-11 | Datastore has **no public API** (internal to ODB); the **only** public API is Frontend↔ODB | ADR-004 (single writer, no external access). | ✅ |
| D-003 | 2026-09-11 | Two-folder merge = **option A** (`usecases/` canonical; absorb the good parts of `usecase_analysis/` into `UC_*`, then delete/archive) | Avoids double traceability (resolves Q-005). | ✅ |
| D-004 | 2026-09-11 | Document identity/freshness = **`version_id`**, decided **by the document's state** (**D-020** supersedes D-004's single tuple): while **open**, `version_id` = the LSP `didChange` **`open_revision`** (buffer, monotonic within the open span); while **non-open**, `version_id` = the document's **disk signal** (last-change mtime, observed via `didChangeWatchedFiles`). There is **no single tuple ranking open and non-open versions** — the file and its buffer are distinct data that only share a path. **C1 forwards the raw sync fact it observes** (the `open_revision` for an open document) and **C2 (ODB) owns the state → selection + generation bookkeeping** (TJ-018); content: open → client **buffer**, non-open → builder reads **disk** by path. | Dedup/freshness need a per-change, comparable identity for **both open and non-open** files: LSP `version` covers open buffers (unsaved edits), `didChangeWatchedFiles`+mtime covers disk files. One **state-relative** key unifies them without cross-state ranking (resolves Q-002). The single `(last_save_timestamp, open_revision)` tuple originally specified here is **superseded by D-020**. | ✅ (superseded by D-020) |
| D-005 | 2026-09-11 | **v1 scope** = didOpen/didChange/didClose (sync), didChangeWatchedFiles + save (config), **Hover**, **Go-to-Definition**, **Find References**, **Diagnostics** (server→client). **v2 (provisional)** = Completion / Rename / Document Symbols / Semantic Tokens | Meets "component requirements roughly extractable + not too many" and covers every load-bearing mechanism (request→task→job, dedup, priority, cancel, push-back, config-rebuild, unbounded policy, server→client). v1 user-confirmed; v2 provisional (re-propose if needed at re-verification). | ✅ |
| D-006 | 2026-09-11 | **Object Server excluded from v1** (future: a second frontend over the same core) | User-confirmed (resolves Q-003). | ✅ |
| D-007 | 2026-09-11 | **starvation / unbounded / priority-inversion policy deferred** to detailed design; v1 fixes only the **mechanism classes** (R-007-1 = age-demotion, R-007-2 = size/time-bound; R-006-4 cancel-and-rerun **mechanism later deferred per D-010**); concrete thresholds/timeouts deferred | These are liveness, not correctness, and the ADRs themselves mark them "detailed-design input" (resolves Q-004). | ✅ (deferred-by-design) |
| D-008 | 2026-09-11 | **Shared-Job (dedup / priority inheritance / reference-counted cancellation): *management* = ODB; *mechanism* = Builder.** `architecture.md` §2 (ODB) gains the shared-Job management responsibility; §4 (Builder) is redefined as mechanism-only | Aligns to ADR-002 (ODB owns job dedup/priority/cancellation), ADR-008 (single owner; ODB tracks cancellation centrally), R-006-3. ADR outranks the older `architecture.md` wording (Builder-managed). Resolves G1/G2. User-confirmed (2026-09-11). | ✅ |
| D-009 | 2026-09-11 | Consolidate `execution-plan.md` into this `README.md` as the single index/governance doc for the set; `execution-plan.md` to be removed on approval | The set needs a durable index (document map + derivation model + conventions + status + change guideline + change history) that survives project completion; a pure "plan" expires. Keeps single-source-of-truth (status + decisions have one home). | ✅ |
| D-010 | 2026-09-12 | v1 is **single-executor, non-preemptive**: Job priority affects **dispatch order only** (TJ-011/012), **not runtime resource allocation**; the **R-006-4 cancel-and-re-run mechanism is deferred to detailed design** (not only its threshold). v1 liveness for R-006-4 is closed by priority inheritance (TJ-009) + dispatch order (TJ-012) + bounded execution (TJ-019) + state-1 pin (TJ-013) + unbounded-work defer/cancel (TJ-014). Revisit if use-case analysis / implementation introduces concurrent Job execution or runtime resource priority. (Refines the R-006-4 portion of D-007.) | User: no per-Job runtime priority in v1; cancel-and-re-run incurs wasted-work cost with no liveness benefit in a single-executor model. | ✅ (deferred-by-design) |
| D-011 | 2026-09-13 | **Result retention window** = per-request, in-memory, **fetch-once + TTL**: every terminal `Result` is retained only for a window that **opens at terminal-push delivery** and **closes at the earlier of** a successful `get_result` or a **TTL expiry**. A single code `E_EXPIRED` covers both closing triggers (fetched or TTL-expired); `E_NOT_FOUND` stays reserved for ids never recognized. On TTL expiry the ODB **notifies the owning Frontend** via `ExpiryEvent` (§5.2) carrying `operation` + `DocumentRef` (metadata only, no payload); eviction is unconditional (memory safety), notification best-effort. **TTL threshold deferred** to detailed design (D-007 / R-007-2). | In-memory results (ADR-004, single writer) must be bounded (availability); fetch-once matches the one-shot `get_result` model; the expiry event lets the Frontend build a meaningful diagnostic/log. Reflected in API-002, §5 (`E_EXPIRED`), §5.2 (`ExpiryEvent`), §7. | ✅ |
| D-012 | 2026-09-13 | **Cancel model = 3 forms, all own-only (R-008-1)**: (1) `cancel(request_id)` one Task; (2) `cancel(request_ids)` a **set** (the 1:N case — one Frontend protocol message → 0/1/N ODB Requests); (3) `cancel(all)` all of this Frontend's live Tasks (disconnect / teardown). `owner` is **implicit** = the calling Frontend (its API object); a Frontend can only target **itself**. **`where = DocumentRef` dropped** — the ODB never infers "which ids are moot"; the Frontend supplies exact ids (it owns the protocol→id mapping + intent). | The ODB is protocol-agnostic (R-008-2) and cannot decide which ids are moot; the set form covers the 1:N mapping the Frontend owns (ADR-001 superset); own-only preserves cross-Frontend isolation (ADR-001). Reflected in API-003, §4.4, §7. | ✅ |
| D-013 | 2026-09-13 | **`reference_depth` removed from the Request wire model** — in v1 it was a monotonic function of `operation` (HOVER/DEFINITION immediate, REFERENCES unbounded), so redundant on the wire. The ODB now **derives reference-depth ordering** (TJ-011) and the unbounded defer/cancel (TJ-014) **from the `operation`** (a shared-vocabulary fact). **Boundary discipline (R-008-2):** the ODB is *expected* to understand the operations it receives (shared FE↔ODB API vocabulary) — **normal contract knowledge, not an intrusion** into the Frontend's internal responsibilities; what it must **not** do is interpret the Frontend's *client-type-specific intent* (why it issued the op, IDE focus, per-client rules), which it neither sees nor acts on. A payload (e.g. `HoverPayload`) is **data** (signature + doc), not a UI action — the "popup" is the IDE's job. | Removing a redundant wire field eliminates the "depth = file count / depth = inline-vs-ticket" misreadings and keeps the protocol-agnostic boundary clean while preserving the ODB-internal scheduling (ADR-007); the boundary note fixes the confusion that the ODB knowing an operation ≠ intruding on the FE (the forbidden act is interpreting client-type intent). Reflected in §4, §4.1, §4.2, §5.1. | ✅ |
| D-014 | 2026-09-14 | **System Task model for background builds (NC-05).** The ODB generates an internal **System Task** (ID namespace `s-*`) when a document enters **State 2** (open in the editor and the documents it references, per ADR-007) or **State 3** (package member). System Tasks participate in the Job waiter set like any Task. Cancelled on: `DOCUMENT_SYNC{action:close}`, file deletion (`WATCHED_FILES{type:deleted}`), or config change. System Tasks are **not** cancellable by the Frontend (`E_NOT_FOUND`). TJ-001 extended: Task trigger = client Request **or** ODB state-transition. | Preserves the 1:1:N invariant (TJ-001) and reference-counted cancellation (TJ-007) while accommodating ODB-initiated work. Unified cancel path; no exception class. Reflected in TJ-001 (extended), new TJ-021, §4 index. | ✅ |
| D-015 | 2026-09-14 | **Diagnostics delivery = event push (LSP-idiomatic).** A new `DiagnosticsEvent { document: DocumentRef, diagnostics: Diagnostic[] }` is added to the `RequestEvent` union (§5.2). The ODB **pushes** it via the registered `register_completion` handler after a build produces updated diagnostics (trigger: `DOCUMENT_SYNC` / `WATCHED_FILES` / `CONFIG_SAVE` processing). The Frontend maps it to `textDocument/publishDiagnostics`. The `DIAGNOSTICS` operation (pull) coexists for explicit re-request. | Matches LSP `publishDiagnostics` (server→client unsolicited push). Reuses the existing handler channel. Consistent with `ExpiryEvent` pattern. No N+1 round trips. Reflected in §5.2 (event schema), §5.1 (payload table). | ✅ |
| D-016 | 2026-09-14 | **Document lifecycle via payload discriminators (OM-02, OM-03).** `DOCUMENT_SYNC` payload gains `action: "open" \| "change" \| "close"`. `WATCHED_FILES` payload gains `events: [{uri, type: "created" \| "changed" \| "deleted"}]`. On `close`: ODB releases State 2, cancels the System Task (D-014), demotes priority. On `deleted`: ODB removes Datastore entry, invalidates dependency graph, cancels all related Jobs. The Frontend sends **both** `DOCUMENT_SYNC{action:close}` (state transition) **and** `cancel(request_ids)` (immediate in-flight termination) for the same document. | ODB needs explicit state-transition signals (open/change/close, created/changed/deleted) to manage State 1/2/3 transitions, System Task lifecycle, and Datastore cleanup. A single payload action avoids adding 5+ new operations. Reflected in §4.1, §7 (cancel mapping table). | ✅ |
| D-017 | 2026-09-14 | **Operation payload schema formalized alongside Phase 2 UC analysis (OM-05).** The minimum required fields per v1 operation (HOVER: position; DEFINITION: position; REFERENCES: position+include_declarations; DOCUMENT_SYNC: action+content?; WATCHED_FILES: events[]; DIAGNOSTICS/CONFIG_SAVE: none) will be written into `frontend-odb-api.md` §4 as a normative table during Phase 2 UC analysis. | Not a design decision — formalization of existing intent already present in examples and payload descriptions. Completing it alongside the UC flows ensures consistency with concrete scenarios. | ✅ (deferred-by-design) |
| D-018 | 2026-09-14 | **Policy vs. user cancellation distinguished via `TerminalEvent.reason` (OM-06).** `TerminalEvent` gains an optional field `reason?: "user_canceled" \| "policy_deferred" \| "system_cancelled"`. The ODB sets `reason` on every `Cancelled` terminal. The Frontend: if it did NOT call `cancel()` and received `Cancelled`, the `reason` indicates policy or system. **No new `ErrorCode`** is added; `Cancelled` remains a normal outcome, not an error. | Adding an error code conflates a normal outcome (cancellation) with a failure. A `reason` field on the terminal event is non-invasive, backward-compatible, and sufficient for the Frontend to build meaningful logs/diagnostics. Reflected in §5.2 (event schema). | ✅ |
| D-019 | 2026-09-22 | **Project/package configuration ownership: the ODB (C2) — not the Frontend (C1) — owns reading, parsing, and scoping of the workspace configuration** (e.g., `gdoc.project.json`). The Frontend stays **protocol-only**: it forwards the **workspace root** (and the config location, if it knows it) and issues `CONFIG_SAVE`; it does **not** read/parse the config and does **not** pre-derive **Packages/Documents/content-types** to hand to the ODB. The ODB **absorbs the scoping responsibility (INV-06)** as its **first internal sub-concern — the Workspace/Project Manager** — alongside the existing **Task/Job Manager**; it remains **one component** and the **single writer** (ADR-004): no new component, no second Datastore writer (option **(a)**, user-confirmed). | ADR-001 (protocol-agnostic core — a config-format change must not force a Frontend change), ADR-004 (single ODB writer/coordinator), ADR-009 (config = first-class ODB-owned event), and the already-ODB-owned INV-15/16/17 (state-3 scheduling, dependency graph, config-rebuild) make the Frontend reading the config an **outlier**. Moving INV-06 to C2 closes that inconsistency and keeps one owner per decision (ADR-008). Keeping the ODB a single component with two internal sub-concerns preserves the single-writer invariant. Refines D-017's `CONFIG_SAVE` payload entry (`none` → **workspace root required**). Reflected in: architecture.md §1/§2, subcomponents/README.md §4.1 (INV-06), adr/009 (Decision), contracts/frontend-odb-api.md (CONFIG_SAVE), UC-001. | ✅ |
| D-020 | 2026-09-25 | **`version_id` = state-based identity + generation-scoped staleness (supersedes D-004's single tuple).** A document's identity/freshness `version_id` is **state-relative**: while **open** it is the LSP `didChange` **`open_revision`** (buffer); while **non-open** it is the **disk signal** (last-change mtime, observed via `didChangeWatchedFiles` — the server does **not** poll). There is **no cross-state ranking** and **no single tuple** — the file and its buffer are distinct data that only share a path. **Staleness is scoped to the generation (open episode):** a buffer result is **discarded** once the document is no longer open in that generation (closed at `didClose`, or re-opened as a fresh generation starting `open_revision` at 1 — generations are separated, so revision 1 of a re-open never collides with the prior generation's or the disk's version); a disk result is stale when a newer disk change is observed (`WATCHED_FILES{changed}` ⇒ newer mtime). Monotonicity is **within** a state only (open: `open_revision`↑; non-open: mtime↑) — the two are never compared. C2 (ODB) owns the state → selection + generation bookkeeping; C1 forwards the raw `open_revision` fact + open-buffer content and registers `didChangeWatchedFiles`. Reflected in: `task-job-management.md` TJ-005/TJ-018 (rule), `frontend-odb-api.md` §4/§4.3 (wire model), `subcomponents/README.md` (INV-05/INV-30, glossary Document/dedup key), UC-002/UC-003 (open/change semantics). | User: open and non-open versions cannot be ranked against each other (a file and its buffer are different data). A re-open starts revisions over — that is fine because the close discards the buffer, so generations are separated and no cross-generation comparison is needed. Retires D-004's `(last_save_timestamp, open_revision)` tuple (which implied cross-state ranking) in favor of state-relative identity + generation-scoped staleness. | ✅ (supersedes D-004's tuple) |
| D-021 | 2026-09-25 | **Stale queued-Job dispatch-skip (efficiency) + `DOCUMENT_SYNC` `content` requirement clarified** — from the UC-003 (Edit Text) analysis. (1) `contracts/task-job-management.md`: **note on TJ-012** — a queued Job for a `(file, version, inputs)` whose document `version_id` is no longer current **should not** be dispatched (dispatch permitted; its result can never become the Datastore's "current" entry — TJ-018). **should-level (efficiency), not shall** — correctness already holds via TJ-007/TJ-018; the note avoids wasted Builder work under the single-executor / run-bound regime (TJ-015/TJ-019). (2) `contracts/frontend-odb-api.md` §4.1: `content` **required** for `action:"open"`/`"change"` (open document), **optional** for `action:"close"` — clarifies D-017's `DOCUMENT_SYNC` entry (`action` + `content?`); the full normative D-017 minimum-fields table remains to be written during Phase 2 (deferred-by-design). | UC-003 reverse-check: the Phase 1a contract was silent on dispatch-skip (ST-003-002/SCR-C2-003-002), and a reader could misread D-017's `content?` as optional for `open`/`change`. Both findings recorded as "awaiting user approval" per gate §4.5; applied on user approval (2026-09-25), option **A** (note on TJ-012, no new rule ID). Reflected in: `task-job-management.md` (TJ-012 + §4 index), `frontend-odb-api.md` §4.1, UC-003 (Reverse-check ✅), `process/phase2/plan.md` (P2-005). | ✅ (user-approved 2026-09-25) |

## 8. Derivation Procedure (Roadmap)

Each phase produces a deliverable; a phase with no deliverable is not done.

### Phase 0 — Grounding: component/responsibility inventory + glossary  (✅ done, 2026-09-11)

- **Purpose:** put "who owns what" into words, so later phases cannot produce a "two owners" or "no
  owner" situation.
- **Deliverable:** `subcomponents/README.md` (inventory + single-owner matrix + glossary). **Done.**
- **Depends on:** nothing (first).
- **Procedure:** list components from `architecture.md` (LSP Frontend / ODB / Object Datastore /
  Object Builder(s) / future Object Server); make each component's owned vs non-owned
  responsibilities explicit (ADR-001, ADR-008); fix the boundaries (Datastore inside the ODB —
  ADR-004; Builder downstream of ODB — ADR-005; Object Server a future second frontend writing via
  the same mutate API); fix the invariant glossary in one place (Request / Task / Subtask / Job /
  Document / Package / Project / **dedup key** / **priority**), defining **Subtask (task-local)
  vs Job (shared execution)** once (ADR-002 note).
- **Outcome:** G1/G2 resolved → **D-008**; G3 confirmed (dedup key defined per D-004; priority-policy
  thresholds deferred per D-007).

### Phase 1a — Task/Job management rules (goal #3)  (✅ approved, 2026-09-11)

- **Purpose:** crystallize ADR-002/006/007/009 into an **executable specification (rules)**. These
  are the rails for all component requirements, so this goes **first**.
- **Deliverable:** `contracts/task-job-management.md`.
- **Depends on:** Phase 0.
- **Procedure:**
  1. **Three-tier model** (ADR-002) as a state machine: Task states (Active/Cancelled/Completed…),
     Job states, Subtask relationship — **one state-transition table**.
  2. **Sharing & dedup** (ADR-006): **dedup key = (file, version, inputs)** fixed as a `TJ-` rule
     with inputs listed (content type / dependency state / options) (R-006-2); **single in-flight
     invariant** (R-002-2) — one Job per dedup key at a time; **reference-counted cancellation**
     (R-006-3) — active while waiters ≥ 1, cancel on last departure, cancellation centrally managed
     by the ODB (a frontend cancels "its own task" only); **atomic commit on success** (R-006-1).
  3. **Priority** (ADR-007/006/008): two tiers — **frontend** = which of its requests matter/order
     (ADR-008); **ODB** = which shared work runs first (ADR-007 three states + reference depth);
     **composition rule** at the boundary (R-007-3); **priority inheritance** (ADR-006);
     **starvation** mitigation: state-1 pin bound (R-007-1), unbounded defer/cancel (R-007-2),
     priority-inversion bound (R-006-4).
  4. **Config save = rebuild event** (ADR-009): state-3 (package membership) + dependency-graph
     update timing; which caches are invalidated on config change.
  5. **Document identity / freshness** (Q-002 → **D-020**, refines D-004): `version_id` is **state-relative** (open ⇒ `open_revision` buffer; non-open ⇒ disk mtime) with **generation-scoped staleness** (a buffer result is discarded once the document is no longer open in that generation; a re-open starts revision 1). C2 (ODB) owns the state → selection + generation bookkeeping; reflected in
     the dedup key and the Datastore invariant; resolves the "cannot compare new/old" issue.
- **Self-check:** every ADR-002/006/007/009 *Verify* item maps to a rule (TJ-) + test; risks
  R-002-1/2, R-006-1..4, R-007-1..3 all appear as rules; Subtask-vs-Job boundary consistent (Phase 0);
  "ODB does not branch on client type" (R-008-2) is a rule.
- **User review:** two-tier priority boundary as intended; starvation/unbounded policy accepted;
  Q-002 resolved; Job run bound/timeout accepted (R-005-1 / R-003-3).
- **DoD:** all Verify/risks turned into rules; state-transition table present; dedup key + priority
  rules explicit; Q-002 resolved.

### Phase 1b — Frontend↔ODB API (goal #2)  (✅ approved, 2026-09-13)

- **Purpose:** define the **surface (API)** of the Phase 1a Task/Job rules — the only public API the
  ODB exposes to run its internals.
- **Deliverable:** `contracts/frontend-odb-api.md`.
- **Depends on:** Phase 1a (the API is the surface of the Task/Job rules).
- **Procedure:**
  1. **Operation list** (each `API-nnn`): `submit(request) → { inline result | request id }`
     (ADR-002: 1 request : 1 task); `getResult(id)` / completion via **push-back (pre-registered
     callback)** (ADR-003); `cancel(id | scope)` (ADR-008: own task only); `registerCompletion(callback)`.
  2. **Request model** (protocol-agnostic fields, ADR-002/008): operation / touched documents /
     priority hint / source (frontend identity only, no semantics) / required context
     (reference-depth ordering is ODB-internal, derived from the operation). **R-008-2:**
     it must express **all** context the ODB needs; if not, extend the Request model (the legitimate
     API extension point).
  3. **Result types:** diagnostics / semantic tokens / symbols / completion items / definition /
     references / rename edits, etc. (from FR-1.2).
  4. **Synchronous facade semantics** (ADR-003): callbacks are lightweight; `call_soon_threadsafe` /
     `run_coroutine_threadsafe` required (R-003-2); **no polling**; no heavy work inside a callback
     (R-003-1).
  5. **Error / cancellation model:** API behavior when a task is cancelled (R-008-1 translation).
  6. Trace every API operation to a Phase 1a `TJ-` rule or an ADR.
- **Self-check:** all API ops traceable to TJ-/ADR; Request model expresses all needed context
  (R-008-2); callback constraints explicit (R-003-1/2/3); every FR-1.2 function expressible as a
  result type or API op; cancel translates to "own task only" (R-006-3 / R-008-1).
- **User review:** API granularity (submit/getResult/cancel split) sensible; result-type scope enough
  for v1 (with Q-001); request id means 1:1 with request.
- **DoD:** operations, types, facade, and errors complete, all traceable to ADR/TJ-; every FR-1.2
  function expressible.

### Phase 2 — Unify use-case analysis (behavioral evidence)

- **Purpose:** align the behavioral evidence, and **reverse-check** whether the Phase 1 contracts are
  sufficient for the behaviors.
- **Deliverable:** unified into `usecases/UC_*.md` (`usecase_analysis/` absorbed or explicitly
  re-positioned — decided in the log).
- **Depends on:** Phase 1a / 1b (the reverse-check counterpart).
- **Method:** use `process/phase2/skill.md` (tailored analysis method) +
  `process/phase2/template.md` (output structure).
- **Work tracker:** `process/phase2/plan.md` (step status + decision log).
- **Procedure:**
  1. **Decide the relationship between the two folders** (one choice, recorded in the log — leaving
     them mixed double-counts traceability): Option A = `usecases/` canonical, absorb the good parts
     of `usecase_analysis/` (LSP links, sequence diagrams, the `6. Update Document` Task Queue note)
     into `UC_*`, then delete/archive; Option B = `usecase_analysis/` as "protocol reference" and
     `usecases/` as "formal analysis", relationship stated in this README.
  2. **Cover all FR-1.2 functions + the sync/config families** in UCs; add missing ones (Find
     References / Symbols / Completion / Rename / Diagnostics exposure / Semantic Tokens; sync:
     didOpen/didChange/didClose; config: didChangeWatchedFiles / config save, ADR-009).
  3. Write each UC **template-compliant** (Analysis Focus / Main / Alternative / Sequence Diagram /
     Derived Requirements IF/ST/DR/EH/SCR / Traceability Matrix) and **drop a requirement on all 4
     components per actor** (leave none empty; for **C3 Datastore** — internal, no public API, ADR-004 — express the requirement as an **internal data-model / single-writer invariant**, not actor-facing behavior).
  4. **Reverse-check** each UC against the Phase 1a/1b contracts (satisfies / insufficient); feed gaps
     back to Phase 1a/1b (escape valve).
- **Self-check:** all FR-1.2 + sync + config covered; each UC drops requirements on all 4 components;
  IF/ST/DR/EH/SCR IDs present and traceable; sequence diagrams don't contradict the ADR-008 hand-off
  (inline vs request-id + push); the `3. Open Text` versioning question consistent with Q-002/D-004;
  no duplicate call of the same operation in a sequence.
- **User review:** UC coverage matches v1 intent (e.g. is rename in scope) → Q-001; main/alternative
  scenarios match real client behavior; identify the UCs to implement first.
- **DoD:** all FR-1.2 functions in UCs; requirement decomposition across the 4 components complete;
  consistency with the Phase 1 contracts confirmed.

### Phase 3 — Component requirement allocation (goal #1) — the main verification phase

- **Purpose:** unify the contract obligations (Phase 1) and the behavior obligations (Phase 2) into a
  requirement set per component. This is the **core verification** phase.
- **Deliverable:** `subcomponents/{language-server,object-database,object-datastore,object-builders}.md`.
- **Depends on:** Phase 0 / 1a / 1b / 2.
- **Procedure:**
  1. Each component requirement = **(contract obligations) ∪ (behavior obligations)**.
  2. Give each a stable ID (`LSP-nnn` / `ODB-nnn` / `DS-nnn` / `BLD-nnn`) + a **Derived From**
     (FR/NFR → ADR → UC → API op / TJ- rule).
  3. Describe the Datastore as a **data model + consistency/single-writer invariants** (ADR-004), not
     as a public API.
  4. **Allocate the NFRs** (NFR-1.1..3.1): LSP = asyncio / lightweight message handling / minimal
     runtime (NFR-1.1); ODB = separate thread / internal event loop / dynamic scheduling / share &
     cancel (NFR-2.1/2.2/2.3); Datastore = in-memory / **single-writer, no internal locking,
     single-context & sequential (synchronous, non-async)** (NFR-1.3). *Note:* the **thread-safe**
     obligation is on the **ODB facade** (NFR-2.2 / F6.6), **not** the Datastore — the Datastore is
     "dumb" by design (ADR-004); its safety comes from the sole consumer giving it single-context
     sequential access (see glossary §6, `Object Datastore`; allocate to `DS-001` in this phase).
  5. Confirm **every FR/NFR is covered by ≥1 component requirement** (zero misses).
- **Self-check:** apply the **5** checks from `.agents/checklists/Traceability Check Strategy.md`
  (adequacy, semantic containment, consistency, granularity, verifiability) per component, in a table;
  all FR/NFR covered; all requirements traceable (Derived From not broken); no 0-owner / 2-owner;
  terminology matches Phase 0; each requirement verifiable.
- **User review:** each component's requirements at implementable granularity; NFR allocation sensible;
  the core-to-implement-first is identifiable.
- **DoD:** the 4 component requirement sets complete; all FR/NFR/ADR/UC traceable; adequacy +
  consistency checks pass.

### Phase 4 — Final verification: traceability + risk closure

- **Purpose:** verify the whole can be declared "design complete." **Zero orphans** + **every risk
  reached a rule and a test**, checked mechanically.
- **Deliverable:** `traceability.md` (full bidirectional matrix) + risk-register closure table.
- **Depends on:** Phase 0–3.
- **Procedure:**
  1. Build the **full bidirectional matrix**: `FR/NFR ↔ ADR ↔ UC ↔ (API op / TJ- rule) ↔ component
     requirement`. Verify **no orphans in both directions** (top-down and bottom-up).
  2. **Risk-register closure:** every `R-00x` is "ruled (Phase 1/3)" **and** "reached a test plan
     (Phase 3/4)" — shown in a table.
  3. Close all open questions, or mark them **deferral (to v2)** explicitly.
  4. Final check that terminology is consistent across all documents.
- **Self-check:** zero orphan entries (checked mechanically via the matrix); all `R-00x` reached a
  rule + a test (table below); all open questions closed / deferred; terminology consistent.
- **User review:** the "design complete" verdict; the deferred items accepted; the handoff to
  detailed-design / implementation is sufficient.
- **DoD:** zero orphans; all risks reached a rule + a test; all open questions resolved/deferred;
  user approves "design complete."

**Risk-closure table (template):**

| Risk | Ruled? | Rule ID | Test angle | Reached in | Status |
| --- | --- | --- | --- | --- | --- |
| R-002-1 | to check | | | | |
| R-006-1..4 | to check | | | | |
| R-007-1..3 | to check | | | | |
| R-008-1..3 | to check | | | | |
| R-003-1..3 | to check | | | | |

---

*Maintained as the single index for this document set. Provenance: see §7 (Change History).*
