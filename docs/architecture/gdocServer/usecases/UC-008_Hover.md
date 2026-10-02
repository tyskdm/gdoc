# UC-008: Hover

> **Tailored template for:** gdocServer Phase 2
> **Use at:** `usecases/UC-008_Hover.md`
> **ID rule:** `<TYPE>-<UC-ID 00x>-<NNN>` — unique within the use case, sequential.
> **Terminology:** per `../../subcomponents/README.md` §6 (C1 = Language Server · C2 = Object Database · C3 = Object Datastore · C4 = Object Builder) and `../../README.md` §4.

---

## Use Case

### ID

UC-008

### Name

Hover

### Purpose

When the user hovers the cursor over a symbol at position **P** in a document **D**, the IDE sends `textDocument/hover` (FR-1.2) and expects a **Hover** (contents + range) or **null**. Hover is the **fastest, most local** of the v1 query operations (D-005): a single-symbol lookup over already-committed Datastore objects — a **read**, not a re-analysis.

a. **C1** (Language Server) stays **protocol-only** (ADR-001; INV-02): it translates `textDocument/hover` into `submit(HOVER{documents:[D + raw sync fact], payload:{position:P}})` (API-001; §4.1/D-017: the minimum field for `HOVER` is `position`), and maps the answer back — `HoverPayload` → LSP `Hover`, empty payload → LSP `null`, `Error` → protocol error, `Cancelled` → client cancellation semantics (R-008-1). C1 does **not** read content, resolve symbols, or render anything: the payload is **data** (declaration signature + documentation), and the "popup" is the IDE's job (D-013 note; §4.1 note).

b. **C2** (ODB) is the **sole answerer**: it maps the Request to exactly one Task (TJ-001), schedules D at **State 1** priority for the Task's lifetime (ADR-007; TJ-011/012 — State 1 is *precisely* "a document referenced by an active client request", hover being the canonical case), resolves D's **current `version_id`** from its state (TJ-018/D-020), and answers from a **fresh committed result** (fast path — §8 S1: inline `Submission{inline, Result{Success, HoverPayload}}`, no Job). If no fresh committed result exists (e.g., first hover right after a UC-003 edit), the request-driven Task **may run an in-Task build** (TJ-001 extension: "a state-1 hover whose referenced objects are not yet built") — **bounded** to the objects needed to answer (D-013: HOVER = immediate reference depth; **not** the unbounded closure of TJ-014/UC-010) — in which case the flow is ticketed (API-001), with an honest `ProgressEvent{begin…end}` (NFR-1.4) and a `TerminalEvent` (§5.2), and C1 fetches via `get_result` (API-002; no polling — F6.2).

c. **C3** (Datastore) is passive: hover reads are in-memory low-latency lookups served via C2 (NFR-1.3; ADR-004; D-002 — no public Datastore API); if a build was triggered, the new result is committed **by C2 only, atomically, on success only** (TJ-008).

d. **C4** (Builder) is involved **only on the build path**: it executes the in-Task build Job (Parse/Link/Compile) from the supplied context (buffer content if open, disk if non-open — D-020/§4.3), returns candidate objects including the declaration's signature + documentation that `HoverPayload` needs (§5.1), and cancels **cooperatively** within the execution bound (TJ-019). C4 does not write to the Datastore (ADR-004; TJ-008).

e. **Cancellation** is own-only (D-012): C1 cancels its own hover Task only (`cancel(request_id)`, API-003); C2 applies reference-counted cancellation (TJ-007) — a shared Job stays alive while ODB-internal background waiters (D-014/D-024) or other Frontends' Tasks remain.

f. **Contrast with siblings:** UC-002/UC-003 *trigger* background builds (State 2) and push diagnostics (D-015); Hover **consumes** committed results and may *request* a bounded in-Task build — `HOVER` is **not** among D-015's listed diagnostic-push triggers. UC-009 (Go to Definition) is the same single-symbol family (immediate depth — D-013); UC-010 (Find References) is the **unbounded** query (TJ-014; ticketed with honest progress — NFR-1.4).

### Actors

| Actor | Description |
| ----- | ----------- |
| IDE Client (User) | Hovers the cursor over a symbol at position P in document D (`textDocument/hover`); may cancel via the client's cancellation mechanism. |
| C1 — Language Server | Translates `textDocument/hover` → `submit(HOVER{documents, payload:{position}})` (API-001; D-017); handles **both** inline and ticketed `Submission` (API-001); when ticketed, consumes progress + terminal and fetches via `get_result` (API-002; F6.2); maps `HoverPayload` → LSP `Hover`, empty → `null`, `Error` → protocol error, `Cancelled` → client cancellation semantics (R-008-1); cancels **its own** Task only (D-012). Does **not** read content or resolve symbols (ADR-001; INV-02). |
| C2 — Object Database (ODB) | Sole answerer: Task 1:1 (TJ-001); State 1 scheduling while live (TJ-011/012); `version_id` resolution (TJ-018/D-020); freshness check (TJ-005/018); in-Task build when missing/stale (TJ-001 extension; bounded — D-013); Job dedup/join (TJ-005/006); atomic commit on success only (TJ-008); composes `HoverPayload` (§5.1); inline vs ticket (API-001) + honest progress (NFR-1.4); own-only reference-counted cancel (TJ-007; D-012). |
| C3 — Object Datastore | Passive: in-memory low-latency reads (NFR-1.3); writes/commits only via C2 (ADR-004; D-002). |
| C4 — Object Builder | (Build path only) Executes the in-Task build Job (Parse/Link/Compile) from the supplied context (D-020); returns candidate objects including the declaration's signature + documentation (§5.1); cooperative cancel (TJ-019); never writes to the Datastore (ADR-004; TJ-008). |

### Derived From

FR-1.2 (LSP Hover) · FR-3.2 (request → Task → Job; in-Task build) · NFR-1.3 (low-latency in-memory Datastore reads) · NFR-1.4 (honest progress when ticketed) · NFR-2.1 (consistency — no stale/partial answers) · NFR-3.1 (dedup/shared work) · **ADR-001** (protocol-agnostic core; C1 stays protocol-only) · **ADR-004** (ODB sole writer; Datastore passive) · **ADR-007** (State 1 = "referenced by an active client request") · **TJ-001** (1:1 mapping; in-Task build) · **TJ-003** (Task terminal) · **TJ-004** (Job lifecycle) · **TJ-005/006** (dedup key; join in-flight Job) · **TJ-007** (reference-counted cancel) · **TJ-008** (atomic commit on success only) · **TJ-009** (priority inheritance) · **TJ-010/011/012/013** (two-tier priority; State 1; release; bounded) · **TJ-018** (state-based identity/freshness) · **TJ-019** (execution bound; cooperative cancel) · **TJ-020** (dedup key derivation, Builder SDK) · **TJ-021/D-014** (background waiters; Job survival) · **D-002** (no public Datastore API) · **D-005** (v1 scope — Hover is v1) · **D-007** (execution bound) · **D-011** (retention; inline not retained) · **D-012** (own-only cancel) · **D-013** (HOVER = immediate reference depth; payload is data, "popup" is the IDE's job) · **D-017** (HOVER minimum field: `position`) · **D-018** (cancel `reason`) · **D-020** (state-relative `version_id`) · **D-021** (stale Job dispatch skip — P2-005 note on TJ-012) · `contracts/frontend-odb-api.md` (API-001…004 · §4.1 `HOVER` · §5.1 `HoverPayload` · §5.2 events · §8 **S1/S2**) · `contracts/task-job-management.md` (TJ rules) · `usecase_analysis/8. Hover Request.md` (raw draft — "Hover Data or Need to compile"; absorbed per D-003) · `UC-001` (initial build enabling the fast path) · `UC-002/003` (open/edit sync — `open_revision`, buffer content; the in-flight rebuilds a hover may join) · `UC-009/010` (query siblings — same family; UC-010 unbounded, TJ-014)

### Scope Decisions Applied

- **D-005** (v1 scope: sync + config + **Hover** + GoToDefinition + FindReferences + Diagnostics)
- **D-013** (reference-depth order derived from the operation — HOVER = **immediate/bounded**; `HoverPayload` is *data* (signature + doc), **not** UI markup — the "popup" is the IDE's job)
- **D-017** (HOVER minimum payload field: `position`)
- **D-018** (`TerminalEvent.reason` = `user_canceled` when C1 cancels its own hover Task)
- **D-012** (cancellation is own-only — C1 cancels its own Task only; ODB-internal work is not Frontend-targetable)
- **D-014 → D-024** (a shared Job may also be awaited by ODB-internal background waiters — cancelling the hover does **not** kill it, TJ-007)
- **D-020** (the answer is anchored to the **current** state-relative `version_id`: open → `open_revision`/buffer; non-open → disk mtime)
- **D-021** (a queued Job for a superseded version is not dispatched / does not become "current" — P2-005 note on TJ-012)
- **D-007** (execution bound for the in-Task build; `E_TIMEOUT` as the error surface)
- **D-002 / ADR-004** (no public Datastore API; hover reads go through C2, commits are C2-only)
- **D-011** (a ticketed hover Result is retained in the fetch-once window; an inline Result is **not** retained)

### Preconditions

- Workspace initialized (UC-001 complete); ODB API object obtained and completion handler registered (API-004/§6).
- D is a document C2 recognizes (workspace member per saved configuration — D-019 — or an open document) — otherwise EH-008-002 (`E_NOT_FOUND`).
- If D is **open**: it is synced — buffer content + `open_revision` known to C2 (UC-002/UC-003). If **non-open**: C2 has D's observed disk signal (mtime) (D-020; UC-005/UC-006 context).
- **No** requirement that D's build is complete: a missing/stale result triggers the in-Task build path (TJ-001 extension; Main #6–8). The **fast path** (Main #9, §8 S1) assumes a fresh committed result — the typical case after UC-001/UC-002/UC-003.
- In-flight work **may** exist: live Tasks, in-flight Jobs on D or its references (joinable — Alt B), ODB-internal background work (D-014/D-024).

### Postconditions

- **C1:** LSP `textDocument/hover` answered — `Hover` (contents + range), `null`, or a protocol error/cancellation (IF-008-002/003/004; EH-008-*).
- **C2:** the hover Task is **terminal** (`Completed`/`Cancelled` — TJ-003); a **failed** hover yields `Result{status:Error, error:ErrorInfo{code, retryable:true}}` (§5 `ErrorInfo`) — failure is a `Result` status, not a Task state (TJ-003); if it ran a build: the Job is terminal, committed **on success only** (TJ-008), and the "current" pointer advanced only for the then-current generation's version (TJ-018); D has left **State 1** (TJ-012) and reverts to State 2/3 scheduling; ODB-internal background work unaffected (D-014/D-024).
- **C3:** (if a build ran) a new committed entry for (D, version, inputs) — by C2 alone (ADR-004); otherwise **unchanged** — hover is read-only against the Datastore (NFR-1.3).
- **C4:** (if dispatched) the Job ran to terminal (completed or cooperatively canceled — TJ-019); **no partial result exposed** (TJ-008).
- **Global:** the answer reflects **only** a committed result of the current version (TJ-018); no stale, partial, or cross-Frontend data (ADR-001; NFR-2.1); no half-created Task (API-001).

## Analysis Focus

- **Query over committed objects, not re-analysis.** The happy path is a **read**: C2 composes `HoverPayload` from committed Datastore objects (NFR-1.3; §8 S1). C4 is not involved; C1 never sees the objects (ADR-001/004; D-002).
- **Fast path vs build path (TJ-001 extension).** A fresh committed result → inline (S1), no Job, no progress. Otherwise the hover Task **may run an in-Task build** (the raw draft's "Need to compile") — **bounded** to the objects needed to answer (D-013: HOVER = immediate depth; **not** TJ-014's unbounded closure) — and the ticketed flow applies (API-001; NFR-1.4 honest progress; §8 S2-style).
- **State 1, shortest-lived.** Hover is the *shortest* State-1 user (ADR-007; TJ-011(a): "hover / definition / references" — the client is waiting for an answer, highest priority) and releases on terminal (TJ-012), bounded (TJ-013; D-007).
- **Version anchoring (TJ-018/D-020).** The answer is composed only from the **current** `version_id`'s result — a superseded `open_revision`'s result is **stale** (not returned); a queued Job for a superseded version is not dispatched / does not become "current" (D-021).
- **Sharing (TJ-005/006/007/009).** Hover joins in-flight Jobs (a UC-003 rebuild; ODB-internal background work — D-014/D-024); while the hover waits, priority inheritance raises the shared Job (TJ-009); cancelling the hover leaves the Job alive while other waiters remain (TJ-007).
- **C1 stays protocol-only (ADR-001; D-013 note).** C1 maps `textDocument/hover` ↔ `HOVER`, `HoverPayload` ↔ LSP `Hover{contents, range}` or `null`, `Error` → LSP error — and does **not** resolve symbols, read content, or render anything (INV-02).
- **Diagnostics is not hover's concern.** `HOVER` is not among D-015's listed `DiagnosticsEvent` triggers (that surface is UC-011's); a hover-triggered build failure surfaces as the hover's `Result{Error}` (EH-008-003).

---

## Main Scenario

1. The user hovers the cursor over a symbol at position **P** in document **D**. The IDE sends `textDocument/hover {uri:D, position:P}`.
2. C1 translates to `HOVER{documents:[{uri:D, open_revision:r}], payload:{position:P}}` and calls `submit` (API-001; §4.1/D-017: `position` required; §4.3: include the **raw** `open_revision` fact + open-buffer content if D is open). C1 does **not** read content or interpret (ADR-001; INV-02).
3. C2 maps it to **exactly one Task** (TJ-001) and schedules D at **State 1** priority for the Task's lifetime (ADR-007; TJ-011(a)/TJ-012 — "a document referenced by an active client request").
4. C2 resolves D's **current `version_id`** from its state (TJ-018/D-020): open → latest `open_revision`; non-open → the observed disk mtime.
5. C2 checks the Datastore for a **fresh committed result** for the dedup key `(D, version, inputs)` (TJ-005; freshness TJ-018; low-latency read — NFR-1.3):
   - **Fresh** → step 9 (inline answer — §8 S1).
   - **Missing/stale** (e.g., first hover after a UC-003 edit) → C2 runs an **in-Task build** (TJ-001 extension — the raw draft's "Need to compile") — step 6.
6. C2 registers a Job for `(D, version, inputs)` — or **joins** an in-flight Job with the same key (TJ-006 — e.g., a UC-003 rebuild, or an ODB-internal background Job, D-014/D-024) — and dispatches in State-priority order (TJ-011/012), with the Job's effective priority inheriting the hover's State 1 (TJ-009). The build is **bounded** for HOVER: immediate reference depth — only the objects needed to answer the declaration (D-013; TJ-014 does **not** apply).
7. C2 returns a **ticket** `Submission{request_id}` (API-001) and pushes `ProgressEvent{begin…end}` — honest, no fabricated percentages (NFR-1.4; §5.2).
8. C4 executes (Parse/Link/Compile) from the supplied context — buffer content if open, disk if non-open (D-020; §4.3) — and returns candidate objects including the declaration's **signature + documentation** (§5.1); on a cancel request it stops **cooperatively** within the execution bound (TJ-019).
9. **Fast path:** C2 composes `HoverPayload` from the committed objects (§5.1) and answers inline: `Submission{inline, Result{Success, HoverPayload}}` (S1).
   **Build path:** C2 commits the candidate **atomically, on success only** (TJ-008) — the "current" pointer advances (TJ-018); the Task is terminal `Completed` (TJ-003); C2 pushes `TerminalEvent{status:Success}` (§5.2); C1 fetches `Result{Success, HoverPayload}` via `get_result` (API-002 — no polling, F6.2).
10. C1 maps the answer: `Success` + `HoverPayload` → LSP `Hover{contents, range}`; **empty `HoverPayload`** (no symbol at P) → LSP `null` (FR-1.2; R-008-1); `Error` → LSP error; `Cancelled` → client cancellation semantics (EH-008-001/002/003/004).
11. The hover Task is **terminal** → D leaves **State 1** and reverts to State 2/3 scheduling (TJ-012); ODB-internal background work continues independently (D-014/D-024).

## Alternative Scenarios

### A — Fast path (fresh committed result)

**Condition:** a fresh committed result for the current `(D, version, inputs)` already exists — the typical case after UC-001/UC-002/UC-003.

1. Steps 1–5 as in the Main Scenario; step 5 resolves **fresh**.
2. C2 composes `HoverPayload` from the committed objects (§5.1) and returns `Submission{inline, Result{Success, HoverPayload}}` — **no** Job, **no** progress events (§8 S1; D-011: an inline Result is **not** retained).
3. C1 maps to LSP `Hover` (or `null` — Alt C) and responds to the IDE.
4. D leaves State 1 on Task terminal (TJ-012).

### B — Sharing with in-flight work (dedup join)

**Condition:** a Job for the same dedup key `(D, version, inputs)` is already in-flight — e.g., a UC-003 rebuild right after an edit, or an ODB-internal State 2/3 background Job (D-014/D-024).

1. The hover Task **joins** the in-flight Job's waiter set instead of starting a new one (TJ-006; NFR-3.1 — one in-flight Job per key).
2. While the hover (State 1) waits, the Job's **effective priority is raised** (TJ-009 — priority inheritance); it falls back when the hover leaves.
3. The single commit (TJ-008) serves both waiters; the hover fetches its answer from it (API-002).
4. If the hover is cancelled, the Job **remains** alive while other waiters remain (TJ-007) and its eventual commit still benefits a later hover (Alt A).

### C — No symbol at position

**Condition:** D is known and answerable (a fresh/committed result exists), but **no symbol** resolves at position P.

1. C2 answers `Result{Success, **empty** HoverPayload}` — inline or ticketed terminal (both forms; IF-008-002) — a **normal** outcome, **not** an error (§5: `Success` with an empty payload; `Cancelled` ≠ Error discipline).
2. C1 maps the empty payload to LSP `null` and responds to the IDE (FR-1.2; R-008-1).
3. State 1 is released (TJ-012); Datastore unchanged (read-only — NFR-1.3).

### D — Unknown document / malformed request

**Condition:** D is **not** a document C2 recognizes, or the Request is malformed (e.g., missing `position`).

1. C2 rejects **inline**: `Result{Error, code: E_NOT_FOUND | E_INVALID_REQUEST}` (API-001 rejection; §5 `ErrorCode`) — and leaves **no half-created Task** (TJ-001; API-001).
2. C1 maps the error to an LSP protocol error and responds to the IDE (R-008-1).
3. No State transition, no Job, no Datastore effect.

### E — Build failure (hover required compile)

**Condition:** the in-Task build fails — Builder error → `E_BUILD_FAILED`, or the execution bound is exceeded → `E_TIMEOUT` (TJ-019; D-007).

1. C4 reports the failure (or is stopped at the bound); C2 **commits nothing** — the Datastore remains as before the Job (TJ-008; §5 atomicity).
2. The hover Task is **terminal** (`Completed` — TJ-003) with `Result{status:Error, error:ErrorInfo{code, retryable:true}}` (§5 `ErrorInfo`); C2 pushes `TerminalEvent{status:Error}` (§5.2) and C1 fetches it (API-002).
3. A committed result of a **previous** version of D remains, but is **stale** under the current `version_id` (TJ-018) — it is **not** returned as the answer (ST-008-003).
4. C1 maps `Error` to an LSP error response (R-008-1). Diagnostics for D are already available via the D-015 push from the sync UC (UC-002/UC-003) — `HOVER` is **not** a D-015 trigger.

### F — Cancellation (client cancels the hover)

**Condition:** the user cancels while the hover is pending (client `$/cancelRequest` or equivalent teardown) — typically the build path (Main #8).

1. C1 calls `cancel(request_id)` for **its own** hover Task (API-003; D-012 own-only; R-008-1).
2. C2 makes the Task terminal `Cancelled{reason:"user_canceled"}` (D-018; §5 — a **normal** outcome, not an error) and pushes `TerminalEvent{status:Cancelled, reason}` (§5.2).
3. The in-flight Job: C4 cancels **cooperatively** within the execution bound (TJ-019) or completes; C2 **commits nothing** for the cancelled hover (TJ-008). The Job **remains** alive while other waiters remain (TJ-007) — including ODB-internal background waiters (D-014/D-024) — and its eventual commit still benefits a later hover (Alt A).
4. C1 treats `Cancelled` as the client's cancellation semantics (LSP `$/cancelRequest` response semantics; R-008-1); State 1 is released (TJ-012).

## Sequence Diagram

```mermaid
sequenceDiagram
    participant IDE as IDE Client
    participant C1 as Language Server
    participant C2 as Object Database
    participant C3 as Object Datastore
    participant C4 as Object Builder

    IDE -) C1: textDocument/hover {uri:D, position:P}
    C1->>C2: submit(HOVER{documents:[{D, open_revision:r}], payload:{position:P}}) (API-001)
    Note over C2: Task 1:1 (TJ-001) · State 1 while live (TJ-011/012)<br/>version_id = current (open → open_revision, non-open → mtime) (TJ-018/D-020)
    alt fresh committed result for (D, version, inputs)
        C2->>C3: read committed objects (NFR-1.3)
        C3-->>C2: objects
        C2-->>C1: Submission{inline, Result{Success, HoverPayload}} (S1)
    else missing or stale (in-Task build — TJ-001 ext.)
        C2-->>C1: Submission{request_id} (ticket, API-001)
        C2-)C1: ProgressEvent{begin…end} (NFR-1.4)
        Note over C2: dedup key (D, version, inputs) —<br/>join in-flight Job if any (TJ-006) · bounded: immediate depth (D-013)
        C2->>C4: Job (Parse/Link/Compile)
        C4-->>C2: candidate objects (signature + doc — §5.1)
        C2->>C3: commit atomically, on success only (TJ-008)
        C2-)C1: TerminalEvent{Success} (§5.2)
        C1->>C2: get_result(request_id) (API-002, no polling — F6.2)
        C2-->>C1: Result{Success, HoverPayload}
    end
    C1 -) IDE: Hover {contents, range} | null (FR-1.2; empty payload → null)
    Note over C2: Task terminal → D leaves State 1 (TJ-012)
```

---

## Derived Requirements

### Interface Requirements (IF)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| IF-008-001 | C1 | C1 shall, on `textDocument/hover` for document D at position P, submit `HOVER` with `documents = [D + its raw sync fact (`open_revision` if open, with open-buffer content — §4.3)]` and `payload = { position: P }` (API-001; §4.1/D-017: the minimum field for `HOVER` is `position`). C1 shall **not** read content, resolve symbols, or pre-derive declarations (ADR-001; INV-02). |
| IF-008-002 | C2 (→C1) | C2 shall answer `HOVER` with `Result{status:Success, payload:HoverPayload}` — the declaration's **signature + documentation** for the symbol at P (§5.1; **data, not UI markup** — D-013/§4.1 note) — or an **empty `HoverPayload`** when no symbol resolves at P (C1 maps it to LSP `null` — FR-1.2; R-008-1). C2 shall **not** embed UI markup or popup actions in the payload (D-013). |
| IF-008-003 | C2 · C1 | The hover answer shall be delivered as an inline `Submission{kind:"inline", result}` (§8 S1) **or** a ticket `Submission{kind:"ticket", request_id}` (API-001) — C1 shall handle **both** forms (API-001). When ticketed, C2 shall emit an honest `ProgressEvent{begin…end}` (NFR-1.4; §5.2) and a `TerminalEvent{status}`; C1 shall fetch the terminal Result via `get_result` (API-002) and shall **not** poll to wait (F6.2). A ticketed terminal Result is retained in the fetch-once window (D-011); an inline Result is **not** retained (D-011). |
| IF-008-004 | C1 | On client cancellation (`$/cancelRequest` or equivalent), C1 shall call `cancel(request_id)` for **its own** hover Task (API-003; D-012 own-only) and shall treat the resulting `TerminalEvent{status:Cancelled, reason:"user_canceled"}` (D-018) as a **normal** outcome, not an error (§5). C2 shall apply reference-counted cancellation (TJ-007) and shall **not** cancel another Frontend's Task or an ODB-internal Job on C1's behalf (R-008-1; D-014/D-024). |

### State Transition Requirements (ST)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| ST-008-001 | C2 | While the hover Task is non-terminal (TJ-003), its document D shall be scheduled at **State 1** priority (referenced by an active client request — ADR-007; TJ-011(a)); on Task terminal, D shall leave State 1 and revert to State 2/3 scheduling (TJ-012). State-1 pinning shall be bounded (TJ-013; D-007). |
| ST-008-002 | C2 | A `HOVER` Request shall map to **exactly one Task** (TJ-001) that reaches a terminal state (TJ-003). Any Job it requests shall follow the Job lifecycle (TJ-004) and be registered under the dedup key `(D, version, inputs)` (TJ-005); if a Job with the same key is already in-flight, the hover Task shall **join** its waiter set instead of starting a new Job (TJ-006); cancellation of the hover Task shall decrement the waiter count without cancelling the Job while other waiters remain (TJ-007); while the hover Task waits, the Job's effective priority shall inherit its State 1 (TJ-009). |
| ST-008-003 | C2 | A hover answer shall be composed **only** from a result committed for D's **current** `version_id` (TJ-018/D-020); a result for a superseded `open_revision` (or an ended generation) shall be **stale** — it shall **not** be returned as the answer, and a queued Job for a superseded version shall not be dispatched and its result shall not become "current" (D-021; TJ-018). |

### Data Requirements (DR)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| DR-008-001 | C3 (via C2) | Hover answer reads shall go through C2 (ADR-004; D-002 — no public Datastore API); C3 shall serve low-latency in-memory lookups of committed objects (NFR-1.3). C1 and C4 shall **not** access the Datastore (ADR-001/004; D-002). |
| DR-008-002 | C2 | When a hover triggers an in-Task build, the new result shall be committed **atomically, on success only** (TJ-008); the "current" pointer shall advance only on commit for the then-current generation's version (TJ-018); a cancelled/failed hover build shall commit **nothing** and expose **no partial result** (TJ-008; §5 atomicity). |
| DR-008-003 | C2 | Dedup: a hover Task and a concurrent sync/background Task sharing the same `(D, version, inputs)` dedup key shall share **one** Job (TJ-005/006; NFR-3.1); the hover Task joins the waiter set (TJ-006) — never two in-flight Jobs per key. |

### Error Handling (EH)

| ID | Requirement |
| -- | ----------- |
| EH-008-001 | **No symbol** at position P (D known and answerable) shall yield `Result{Success, empty HoverPayload}` — a **normal** outcome, **not** an error (FR-1.2; §5; R-008-1); C1 shall map it to LSP `null`. See the IF-008-002 note (the empty-payload shape is stipulated here; the §5.1 clarification candidate is logged in `plan.md` P2-008). |
| EH-008-002 | An **unknown/unrecognized** document, or a **malformed** Request, shall be rejected inline: `Result{Error, code: E_NOT_FOUND | E_INVALID_REQUEST}` (API-001 rejection; §5 `ErrorCode`), with **no half-created Task** (TJ-001; API-001); C1 shall map the error to an LSP protocol error (R-008-1). |
| EH-008-003 | An in-Task build failure (Builder error → `E_BUILD_FAILED`; execution bound exceeded → `E_TIMEOUT` — TJ-019; D-007) shall commit **nothing** (TJ-008); the hover Task is **terminal** (`Completed` — TJ-003) with `Result{status:Error, error:ErrorInfo{code, retryable:true}}` (§5 `ErrorInfo`); a committed result of a **previous** version remains but is **stale** and shall **not** be returned (TJ-018; ST-008-003); C1 shall map `Error` to an LSP error response (R-008-1). |
| EH-008-004 | Cancellation mid-build: C4 shall cancel **cooperatively** within the execution bound (TJ-019) or complete; C2 shall commit **nothing** for the cancelled hover (TJ-008); the Task is terminal `Cancelled{reason:"user_canceled"}` (D-018); the Job shall **remain** alive while other waiters remain (TJ-007) — including ODB-internal background waiters (D-014/D-024) — and its eventual commit shall still benefit a later hover (Alt A). |

### Software Component Requirements (SCR)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| SCR-C1-008-001 | C1 | C1 shall translate `textDocument/hover` → `submit(HOVER{documents, payload:{position}})` (IF-008-001); handle **both** `Submission` forms (API-001; IF-008-003); when ticketed, consume `ProgressEvent{begin…end}` + `TerminalEvent` and fetch the Result via `get_result` (API-002; F6.2 no-poll); map `Success` + `HoverPayload` → LSP `Hover`, empty payload → LSP `null`, `Error` → LSP error, `Cancelled` → client cancellation semantics (IF-008-002/004; EH-008-001…004); cancel **its own** Task on client cancellation (D-012); never block the event loop (NFR-1.1). |
| SCR-C1-008-002 | C1 | C1 shall remain **protocol-only** (ADR-001; R-008-1): no content reading, no symbol resolution, no Datastore access (D-002), and no interpretation of the payload beyond its LSP mapping — the payload is **data**, and the "popup" is the IDE's job (D-013 note; §4.1 note). |
| SCR-C2-008-001 | C2 | C2 shall implement the `HOVER` pipeline: (1) map Request→Task 1:1 (TJ-001); (2) resolve the current `version_id` from state (TJ-018/D-020); (3) hold D at State 1 for the Task's lifetime and release on terminal (TJ-011/012/013); (4) check freshness of the committed result for `(D, version, inputs)` (TJ-005; TJ-018; NFR-1.3 read); (5) if missing/stale, run the in-Task build (TJ-001 extension) — Job registration/dedup (TJ-005/006), priority inheritance (TJ-009), bounded to the objects needed to answer (D-013 immediate depth; TJ-014 does **not** apply); (6) commit atomically on success only (TJ-008); (7) compose `HoverPayload` from committed objects (§5.1); (8) answer inline (S1) or ticket + honest progress + terminal push (API-001/002/004; NFR-1.4); (9) handle EH-008-001…EH-008-004. |
| SCR-C3-008-001 | C3 | The Datastore shall serve hover reads as passive, low-latency in-memory lookups (NFR-1.3); all writes/invalidations shall be C2-only atomic operations (ADR-004; D-002); a hover-triggered commit is C2's atomic operation (TJ-008); C1 and C4 shall **never** touch C3 (ADR-004). |
| SCR-C4-008-001 | C4 | C4 shall execute dispatched in-Task build Jobs (Parse/Link/Compile) from the supplied context — buffer content if open, disk if non-open (D-020; §4.3); produce candidate objects including the declaration's **signature + documentation** that `HoverPayload` requires (§5.1); cancel **cooperatively** within the execution bound (TJ-019); derive its dedup key via the Builder SDK (TJ-020); and **not** write to the Datastore (ADR-004; TJ-008). |

## Reverse-check

| ID | Phase 1a/1b contract rule | Satisfied? | Notes |
| -- | ------------------------- | :--------: | ----- |
| IF-008-001 | §4.1 `HOVER` (`position`) · D-017 · §4.3 (`open_revision` + open-buffer content) · API-001 | ✅ | |
| IF-008-002 | §5.1 (`HoverPayload`: "declaration's signature + documentation… data, not UI markup") · D-013 (payload is data; the "popup" is the IDE's job) · FR-1.2 (LSP `Hover | null`) | ⚠️ | The **empty-payload** case (no symbol at P) is not explicitly fixed in §5.1 — this UC stipulates an **empty `HoverPayload`** under `Success` (not an error), with C1 mapping to LSP `null` (R-008-1). Candidate one-line clarification for §5.1 (logged in `plan.md` P2-008); no other contract change needed. |
| IF-008-003 | API-001 (inline\|ticket; Frontend handles **both**) · §8 S1 (HOVER inline) · API-002 (no poll; F6.2) · §5.2/NFR-1.4 (honest progress) · D-011 (retention; inline not retained) | ✅ | |
| IF-008-004 | API-003 (own-only) · D-012 · D-018 (`reason:"user_canceled"`) · §5 (`Cancelled` ≠ Error) | ✅ | |
| ST-008-001 | ADR-007 (State 1 = active client reference) · TJ-011/012/013 · D-007 | ✅ | |
| ST-008-002 | TJ-001/003/004/005/006/007/009 | ✅ | |
| ST-008-003 | TJ-018 · D-020 · D-021 (P2-005 note on TJ-012) | ✅ | |
| DR-008-001 | ADR-004 · D-002 · NFR-1.3 | ✅ | |
| DR-008-002 | TJ-008 · TJ-018 · §5 (atomicity) | ✅ | |
| DR-008-003 | TJ-005/006 · NFR-3.1 | ✅ | |
| EH-008-001 | FR-1.2 · §5 (payload iff `Success`) · R-008-1 | ✅ | See IF-008-002 (the ⚠️ covers the empty-payload shape) |
| EH-008-002 | API-001 (rejection; no half-created Task) · §5 (`E_NOT_FOUND`/`E_INVALID_REQUEST`) | ✅ | |
| EH-008-003 | §5 (`E_BUILD_FAILED`/`E_TIMEOUT`; `ErrorInfo.retryable`) · TJ-008 · TJ-019 · D-007 | ✅ | |
| EH-008-004 | TJ-019 · TJ-007/021 (D-014) · D-012 · D-018 | ✅ | |
| SCR-C1-008-001 | API-001/002/003/004 · NFR-1.1/1.4 · F6.2 · R-008-1 | ✅ | |
| SCR-C1-008-002 | ADR-001 · D-013 (note) · D-002 · R-008-1 | ✅ | |
| SCR-C2-008-001 | TJ-001…013/018/021 · D-013 · D-020/021 · API-001/004 · §8 S1/S2 · NFR-1.4 | ✅ | |
| SCR-C3-008-001 | ADR-004 · D-002 · NFR-1.3 · TJ-008 | ✅ | |
| SCR-C4-008-001 | TJ-005/019/020 · §5.1 · D-020 · ADR-004 | ✅ | |

> **Findings (1 ⚠️, zero ❌):** every UC-008 requirement is grounded in the Phase 1a/1b contracts. The single partial item — the **soft-empty answer** (no symbol under the cursor) — is stipulated by this UC as an **empty `HoverPayload`** under `Success` (C1 → LSP `null`, R-008-1); §5.1 does not fix that shape explicitly, and a one-line clarification is a candidate (recorded in `plan.md` P2-008, pending user approval per the §4.5 gate). No other contract change.

---

## Traceability Matrix

| ID | Type | Description | Scenario Step | Owner |
| --- | ---- | ----------- | ------------- | ----- |
| IF-008-001 | Interface | `HOVER{documents (D + raw `open_revision`/open-buffer content), payload:{position}}` (D-017; §4.3); C1 does not read content (ADR-001; INV-02) | Main #2 | C1 |
| IF-008-002 | Interface | Answer = `Success` + `HoverPayload` (signature + doc, data not UI — §5.1/D-013) or **empty** payload → LSP `null` (R-008-1) | Main #9–10, Alt C | C2 (→C1) |
| IF-008-003 | Interface | Inline (`S1`) or ticket (API-001) — C1 handles both; ticketed: honest progress (NFR-1.4) + terminal + `get_result` (API-002; F6.2); retention (D-011) | Main #7, #9, Alt A | C2 (→C1) |
| IF-008-004 | Interface | Client cancellation → own-only `cancel(request_id)` (D-012); `Cancelled{reason:"user_canceled"}` is a normal outcome (D-018; §5) | Alt F | C1 (→C2) |
| ST-008-001 | State | D at State 1 while the hover Task is live; leaves on terminal (TJ-011/012; ADR-007); bounded (TJ-013/D-007) | Main #3, #11 | C2 |
| ST-008-002 | State | Task 1:1 (TJ-001); Job dedup key + join (TJ-005/006); reference-counted cancel (TJ-007); priority inheritance (TJ-009) | Main #6, Alt B | C2 |
| ST-008-003 | State | Answer only from the **current** `version_id`'s result; stale versions not returned; superseded Jobs don't become "current" (TJ-018/D-020; D-021) | Main #4–5, #9, Alt E | C2 |
| DR-008-001 | Data | Hover reads via C2 only (ADR-004; D-002); C3 passive, low-latency (NFR-1.3); C1/C4 don't touch C3 | Main #5, Alt A | C3 (via C2) |
| DR-008-002 | Data | In-Task build result committed atomically on success only (TJ-008); "current" advances only for the then-current version (TJ-018); no partial exposure | Main #8–9, Alt E/F | C2 |
| DR-008-003 | Data | One Job per dedup key shared by hover and sync/background Tasks (TJ-005/006; NFR-3.1) | Alt B | C2 |
| EH-008-001 | Error | No symbol at P → `Success` + empty `HoverPayload` → LSP `null` (normal outcome; FR-1.2) | Alt C | C2 (→C1) |
| EH-008-002 | Error | Unknown document / malformed → `E_NOT_FOUND`/`E_INVALID_REQUEST`, no half-created Task (API-001; TJ-001) | Alt D | C2 (→C1) |
| EH-008-003 | Error | Build failure → no commit (TJ-008); `Error{E_BUILD_FAILED|E_TIMEOUT, retryable}` (TJ-019/D-007; §5); stale prior result not returned (TJ-018) | Alt E | C2 (→C1) |
| EH-008-004 | Error | Cancellation → cooperative stop (TJ-019); no commit (TJ-008); Job survives if other waiters (TJ-007; D-014/D-024); `reason:"user_canceled"` (D-018) | Alt F | C2 (+C4) |
| SCR-C1-008-001 | Component | Hover translation + both Submission forms + progress/terminal consumption + LSP mapping + own-only cancel + no event-loop blocking (NFR-1.1) | Main #2, #9–10, Alt F | C1 |
| SCR-C1-008-002 | Component | Protocol-only discipline: no content reading/symbol resolution/Datastore access; payload is data, the "popup" is the IDE's job (ADR-001; D-013; D-002) | Main #1–2 | C1 |
| SCR-C2-008-001 | Component | `HOVER` pipeline: Task (TJ-001) → `version_id` (TJ-018) → State 1 (TJ-011/012) → freshness (TJ-005/018) → bounded in-Task build (TJ-001 ext.; D-013) → commit (TJ-008) → `HoverPayload` (§5.1) → inline/ticket (API-001/004) | Main #3–11, Alts A–F | C2 |
| SCR-C3-008-001 | Component | Passive in-memory reads (NFR-1.3); ODB-only writes (ADR-004; D-002; TJ-008) | Main #5, #9 | C3 |
| SCR-C4-008-001 | Component | In-Task build execution (Parse/Link/Compile) from supplied context (D-020); signature + doc objects (§5.1); cooperative cancel (TJ-019); no Datastore writes (TJ-008) | Main #8, Alt F | C4 |