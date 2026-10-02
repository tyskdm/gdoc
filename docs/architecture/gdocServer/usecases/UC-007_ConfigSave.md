# UC-007: Config Save

> **Tailored template for:** gdocServer Phase 2
> **Use at:** `usecases/UC-007_ConfigSave.md`
> **ID rule:** `<TYPE>-<UC-ID 00x>-<NNN>` — unique within the use case, sequential.
> **Terminology:** per `../../subcomponents/README.md` §6 (C1 = Language Server · C2 = Object Database · C3 = Object Datastore · C4 = Object Builder) and `../../README.md` §4.

---

## Use Case

### ID

UC-007

### Name

Config Save

### Purpose

When the workspace **configuration** file (e.g. `gdoc.project.json`) is **saved** — either from the IDE (`textDocument/didSave`) or changed on disk externally (`workspace/didChangeWatchedFiles`, `type:"changed"`) — the saved configuration becomes the **sole definition of project structure** (ADR-009). The change is a **first-class rebuild/invalidation event** on a distinct, higher-stability track from live document edits (TJ-016, TJ-017):

a. **C1** stays **protocol-only** (D-019): it does **not** read/parse the configuration and does **not** pre-derive Packages/Documents/content-types. On `didSave` for the configuration file it sends `submit(CONFIG_SAVE{workspace root, config location?})` (API-001; the workspace root is **required** — D-019 refining D-017); for external changes it forwards the raw `WATCHED_FILES{events}` and lets C2 classify (UC-005 Alt D routing).

b. **C2** (ODB) is the **single reader, parser, and owner** of the configuration (D-019, INV-06, ADR-009): it reads the **saved** content from disk (never an editor buffer — TJ-017), **(re)defines** the **Project** scope — Packages, their member documents, content types, dependencies — diffs it against the current scope and **applies the re-scope**: releases State 3 for documents that left a package (ADR-007); **invalidates/re-schedules in-flight work** affected by the re-scope (TJ-016, R-009-1); **invalidates/removes** Datastore entries for removed scopes (ADR-004); updates the dependency graph (NFR-2.1); dispatches **rebuild Jobs** for affected scopes (TJ-005/009/011/012); pushes `DiagnosticsEvent` for affected documents (D-015); and acks with `SyncPayload` (post-save rebuild/invalidation notice) (TJ-016/017, §5.1).

c. **C3** (Datastore) is passive: invalidation and new-result commits happen via the ODB only (ADR-004 single writer).

d. **C4** (Builder) executes the rebuild Jobs and cooperatively cancels affected in-flight Jobs (INV-24/TJ-019); its results are committed by C2 only (TJ-008).

e. In **v1**, `CONFIG_SAVE` is an **expected ticketed** operation — honest progress `begin…end` (NFR-1.4) — because a re-scope rebuild can be long-running or unbounded.

f. **Contrast with siblings:** UC-005 handles non-open disk changes for **regular** documents (per-document result staleness by mtime); a configuration change is a **project-structure redefinition**, not a single-document staleness. UC-006 handles **deletion** (of a member file, or of the configuration file itself): Datastore removal + graph invalidation.

### Actors

| Actor | Description |
| ----- | ----------- |
| IDE Client (User) | Edits and **saves** the configuration file in the IDE (`textDocument/didSave`), or modifies it externally (VCS checkout, manual edit — detected by the IDE's file watcher). |
| C1 — Language Server (Frontend) | Translates `didSave` (config file) into `submit(CONFIG_SAVE{workspace root, config location?})` (API-001); forwards `WATCHED_FILES{changed}` raw; does **not** read/parse the configuration (D-019). Maps `DiagnosticsEvent` → `publishDiagnostics` (D-015). |
| C2 — Object Database (ODB) | Single reader/parser/owner of the configuration (D-019, INV-06). Reads + parses the saved content, diffs and applies the re-scope (TJ-016/017), invalidates/re-schedules in-flight work (R-009-1), invalidates Datastore entries (ADR-004), dispatches rebuilds, pushes diagnostics (D-015). |
| C3 — Object Datastore | Passive: entries for removed scopes invalidated/removed; new results committed — ODB only (ADR-004). |
| C4 — Object Builder | Executes rebuild Jobs (Parse/Link/Compile); cooperatively cancels on re-scope cancellation (INV-24/TJ-019); never writes to the Datastore (ADR-004; TJ-008). |

### Derived From

FR-1.1 (LSP — `didSave`; the config family of v1, D-005) · **FR-2.2** (hierarchical organization — Project/Package redefinition) · FR-3.3 (State-3 background build not dropped) · NFR-1.4 (WDP for ticketed `CONFIG_SAVE`) · NFR-2.1 (data consistency — dependency-graph update) · NFR-2.3 (robust scheduling — priority per ADR-007) · **ADR-009** (save-triggered, isolated configuration handling → **R-009-1** re-scope vs in-flight · **R-009-2** override rules) · **TJ-016** (config save = first-class rebuild/invalidation event) · **TJ-017** (config override rules) · **D-019** (ODB configuration ownership; INV-06; `CONFIG_SAVE` payload = workspace root **required**) · **TJ-005/007/008/009/011/012** (Job model) · **TJ-021 / D-014 → D-024** (background-build guarantee + invariant rails) · **D-015** (diagnostics push) · **D-018** (terminal `reason`) · **D-011** (result retention) · **D-020** (per-document `version_id` semantics — unchanged by re-scope) · **D-002** (no Datastore public API) · **ADR-004** (single writer) · **ADR-007** (State 3) · **ADR-001** (protocol-agnostic core) · `contracts/frontend-odb-api.md` (API-001…004 · §4.1 `CONFIG_SAVE` · §5.1 `SyncPayload` · §5.2 events · §6 facade · §5 `ErrorCode`) · `usecase_analysis/2. Edit Workspace Configuration File.md` (raw draft — sequence + notes; absorbed per D-003) · `UC-001` (initial `CONFIG_SAVE`; degraded mode) · `UC-005` Alt D (watched config → `CONFIG_SAVE` path)

### Scope Decisions Applied

- **D-005** (v1 scope: sync + **config** + query + diagnostics — configuration save is v1)
- **D-019** (configuration ownership = ODB: C1 stays protocol-only; `CONFIG_SAVE` payload = **workspace root required** + config location if known; ODB absorbs INV-06 as its Workspace/Project Manager sub-concern)
- **D-016** (boundary: `WATCHED_FILES{deleted}` for a member file — or the config file itself — is UC-006's path; config **re-scope** is this UC's path)
- **D-015** (diagnostics push for affected documents after `CONFIG_SAVE` processing — a listed trigger)
- **D-018** (`TerminalEvent.reason` — `system_cancelled` for ODB-initiated re-scope cancellations; `user_canceled` if the Frontend cancels its own ticketed Task)
- **D-014 → D-024** (background work for added/removed State-3 membership — NC-05 guarantee + ② invariant rails; ③ mechanism ODB-internal)
- **D-020** (re-scope changes **scope/priority/dedup-key inputs**, not per-document `version_id` — open documents keep their `open_revision` generations)
- **D-008** (shared-Job management = ODB; mechanism = Builder)
- **P2-002 lineage** (Config Save is an independent UC — `plan.md` §1 inventory; raw draft `usecase_analysis/2` absorbed per D-003)

### Preconditions

- Workspace is initialized (UC-001 complete).
- The ODB has read the workspace configuration at least once during UC-001 (or is in **degraded mode** — configuration not found — in which case this save may be the remediation: Alt D / EH-007-003).
- The configuration file **may** be open in the editor with **unsaved** edits — those edits have **no** effect until saved (TJ-017).
- Documents **may** be in **State 3** (package members) under the **current** scope (ADR-007).
- In-flight work **may** exist: live client Tasks, queued/running Jobs, ODB-internal State 2/3 background work (D-014/D-024).

### Postconditions

- **C1:** `Submission` (inline `Result` or `request_id` ticket) handled; if ticketed, the progress stream + terminal are consumed and the terminal `Result` fetched (API-002); `DiagnosticsEvent`s mapped to `publishDiagnostics` (D-015).
- **C2:** Project scope **matches the saved configuration exactly** (Packages, members, content types, dependencies); in-flight work affected by the re-scope cancelled (terminal `Cancelled` + `reason`, D-018) or re-scheduled; Datastore entries for removed scopes invalidated/removed; dependency graph updated (NFR-2.1); rebuilds for affected scopes dispatched and committed (TJ-008); **no partial re-scope observable** (atomicity).
- **C3:** invalidation + commit by ODB only (ADR-004); Datastore passive (NFR-1.3).
- **C4:** rebuild Jobs executed; affected in-flight Jobs cooperatively cancelled (INV-24/TJ-019) or completed (results committed/discarded by C2 — TJ-008).
- **Global:** structural facts (membership, dependencies, content types) are defined **solely by the saved configuration**; unsaved buffer content was **not** applied (TJ-017); subsequent per-document behavior (priority, diagnostics, background builds) reflects the new scope (ADR-007, D-015, FR-3.3).

## Analysis Focus

- **Configuration ownership (D-019):** `CONFIG_SAVE` is the **only** v1 operation where the ODB itself reads workspace content. C1 forwards the workspace root (and the config location, if it knows it) — **URI-level only, no parsing**. A change to the configuration format never forces a Frontend change (ADR-001).
- **Save-only application (TJ-017, ADR-009):** unsaved buffer edits of the configuration have **no** effect. The save is a **bounded, discrete event** — easy to schedule, cancel, and rebuild (ADR-009 Pros).
- **Re-scope vs in-flight (R-009-1, TJ-016):** a document that leaves a package loses State 3 and its background work; a newly added member gains them (FR-3.3/D-014/D-024); in-flight Tasks affected by the re-scope are **invalidated/re-scheduled** so final membership, priority states, and objects match the saved configuration.
- **Override rules (R-009-2, TJ-017):** the saved configuration **wins** on structural facts; open-text edits never override it and never invalidate config-derived state.
- **Ticketing + progress (NFR-1.4):** `CONFIG_SAVE` is **expected ticketed** in v1 (rebuilds may be unbounded) → `begin…report…end` with **honest** progress (no fabricated percentage).
- **Two entry points, one C2 pipeline:** `didSave` (C1 classifies) and `WATCHED_FILES{changed}` (C2 classifies — UC-005 Alt D) both converge on the **same** `CONFIG_SAVE` pipeline in C2.
- **Idempotency:** a save with **no change** is a no-op re-scope (EH-007-001).
- **Degraded-mode boundary:** a save that **creates** the first configuration triggers the initial build (UC-001); a save where the configuration is **absent** re-scopes to degraded mode (EH-007-003); the `deleted` event itself is UC-006's (D-016).
- **No per-document staleness:** unlike UC-005 (mtime staleness), a configuration change is a **structural** event — per-document `version_id` is **unchanged** (D-020); what changes is **scope, priority, and dedup-key inputs** (content types, dependency state, build options — TJ-005).

---

## Main Scenario

1. The user edits the configuration file in the IDE and **saves**. The IDE sends `textDocument/didSave` for document D.
2. C1 recognizes D as the workspace configuration (URI match against the known config location / workspace-root convention — **no content parsing**, D-019) and submits `CONFIG_SAVE{workspace root, config location?}` (API-001; D-019).
3. C2 maps it to a Task (TJ-001) and returns a **ticket** `Submission{request_id}` (expected in v1 — NFR-1.4).
4. C2 pushes `ProgressEvent{begin}` (NFR-1.4).
5. C2 **reads and parses** the **saved** configuration from disk (D-019, INV-06) — **not** from the editor buffer (TJ-017).
6. C2 **diffs** the parsed scope (Packages, members, content types, dependencies) against the current scope.
7. No change → **Alt B** (no-op `Result{Success}`).
8. Change → C2 applies the re-scope:
   - **(a) State 3:** documents that left a package are **released** from State 3 (and their ODB background work dropped — D-014/D-024); newly added members **enter** State 3 (background build — FR-3.3/D-014/D-024) (ADR-007; ST-007-001).
   - **(b) In-flight:** live client Tasks and queued/running Jobs affected by the re-scope are **invalidated/re-scheduled** (TJ-016; R-009-1); cancelled client Tasks get `TerminalEvent{status:Cancelled, reason:"system_cancelled"}` (D-018); Jobs cancelled when their last waiter leaves (TJ-007).
   - **(c) Datastore:** entries for removed scopes are **invalidated/removed** by C2 (ADR-004; DR-007-001).
   - **(d) Graph:** dependency edges (inter-package, external references) re-defined per the saved configuration (NFR-2.1; DR-007-002).
   - **(e) Rebuilds:** Jobs for affected documents dispatched to C4 — deduplicated (TJ-005), state-priority (ADR-007; TJ-011/012), priority inheritance (TJ-009).
9. C4 executes (Parse/Link/Compile) and returns results; C2 **commits atomically** (TJ-008) — C4 never writes (ADR-004).
10. C2 pushes `DiagnosticsEvent{document, diagnostics}` for each affected document whose diagnostics changed (D-015; `request_id` optional — D-025).
11. C2 emits `ProgressEvent{end}` + `TerminalEvent{status:Success}`; C1 fetches `Result{Success, SyncPayload{affected documents}}` (API-002) and maps the diagnostics to `publishDiagnostics`.

## Alternative Scenarios

### A — External change (file watched)

**Condition:** the configuration file is modified **outside** the IDE (VCS checkout, manual edit, build tool).

1. The IDE's file watcher sends `workspace/didChangeWatchedFiles { changes:[{uri:D, type:"changed"}] }`.
2. C1 forwards the **raw** event: `submit(WATCHED_FILES{events:[{uri:D, type:"changed"}]})` (API-001) — C1 does **not** classify (protocol-only, D-019).
3. C2 — which **owns** the config location (D-019) — classifies D as the workspace configuration and routes it into the **same** `CONFIG_SAVE` pipeline (UC-005 Alt D).
4. Main Scenario resumes from step 5 (read + parse).

### B — No-op save (unchanged)

**Condition:** the parsed configuration is **identical** to the current scope.

1. C2 applies **no** re-scope: no State-3 change, no cancellation, no rebuild (EH-007-001).
2. C2 returns `Result{Success}` (inline, or terminal if ticketed; no progress obligation for inline — §4 progress note). Bounded, discrete, idempotent (ADR-009).

### C — Malformed / unparseable configuration

**Condition:** the save produced **invalid** content (syntax error, schema violation).

1. C2 **rejects** the re-scope: the **current** scope remains in effect — **no partial re-scope** (atomicity discipline, TJ-008) (EH-007-002).
2. C2 returns `Result{Error{code:E_INVALID_REQUEST, message, retryable}}` (inline, or as a ticketed terminal — §5 `ErrorCode`).
3. C1 maps the error to its own protocol (diagnostic/log) — its choice (R-008-1/2).

### D — Configuration file no longer present

**Condition:** `CONFIG_SAVE` arrives but the configuration file is **absent** (e.g., it was deleted; the `deleted` event itself is UC-006's path — D-016).

1. C2 re-scopes to **degraded mode** — **no Packages** (UC-001 Alt "No Project Configuration Found") (EH-007-003).
2. All documents are released from State 3; affected in-flight work is cancelled (TJ-016; D-014/D-024); package-scoped Datastore entries invalidated (ADR-004).
3. C2 returns `Result{Success}`. A later save **re-creating** the configuration re-triggers the initial build (UC-001 step 10 onward).

### E — Rebuild in flight (cooperative cancel)

**Condition:** C2 must cancel an in-flight Job during the re-scope (its document left the project scope).

1. C2 signals C4 to cancel the Job; C4 cancels **cooperatively** within the run bound (INV-24/TJ-019) — or completes within the bound.
2. If it completes within the bound, C2 **discards** the result (TJ-008; the document is out of scope). No commit for a document no longer in the saved scope (EH-007-004).

### F — Race with open-text edits

**Condition:** a concurrent `didChange` (UC-003) on an open document during the re-scope.

1. The **saved configuration wins** on structural facts (TJ-017; ST-007-003): membership, priority, and dedup-key inputs follow the saved configuration.
2. The open-text edit does **not** invalidate config-derived state; the document's buffer `version_id` (`open_revision`) is unchanged (D-020) — only scope/priority/inputs changed.

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant IDE as IDE Client
    participant C1 as Language Server
    participant C2 as Object Database
    participant C3 as Object Datastore
    participant C4 as Object Builder

    IDE -) C1: textDocument/didSave (config) — or — didChangeWatchedFiles{changed}
    alt didSave (C1 classifies, URI-level only — D-019)
        C1->>C2: submit(CONFIG_SAVE{workspace root, config location?}) (API-001)
    else watched (C1 forwards raw; C2 classifies — UC-005 Alt D)
        C1->>C2: submit(WATCHED_FILES{events:[{uri, type:changed}]}) (API-001)
    end
    C2-->>C1: Submission{request_id} (ticket — expected v1, NFR-1.4)
    C2-)C1: ProgressEvent{begin} (NFR-1.4)
    Note over C2: read + parse SAVED config (D-019, INV-06)<br/>diff scope: Packages · members · content types · dependencies
    alt scope changed (TJ-016)
        Note over C2: State 3: release leavers / add joiners (ADR-007)<br/>in-flight Tasks/Jobs invalidated-re-scheduled (R-009-1)
        opt affected in-flight Job
            C2->>C4: cancel (INV-24/TJ-019)
            C4-->>C2: stopped, or completed within bound
            Note over C2: out-of-scope result discarded (TJ-008)
        end
        C2-)C1: TerminalEvent{Cancelled, reason:system_cancelled} (D-018) — affected client Tasks
        C2->>C3: invalidate-remove removed-scope entries (ADR-004)
        C2->>C4: rebuild Jobs for affected scopes (TJ-005/009/011/012)
        C4-->>C2: results
        C2->>C3: commit results atomically (TJ-008)
        C2-)C1: DiagnosticsEvent{document, diagnostics} (D-015, D-025)
    else unchanged
        Note over C2: no-op (EH-007-001)
    end
    C2-)C1: ProgressEvent{end} + TerminalEvent{Success}
    C1->>C2: get_result(request_id) (API-002)
    C2-->>C1: Result{Success, SyncPayload{affected documents}}
    C1 -) IDE: publishDiagnostics (D-015)
```

## Derived Requirements

### Interface Requirements (IF)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| IF-007-001 | C1 | C1 shall, on `didSave` for a document D it recognizes as the workspace configuration (**URI-level only — no content parsing**, D-019), submit `CONFIG_SAVE` with `payload = { workspace root (required), config location (if known) }` (API-001 §4.1; D-019 refining D-017). C1 shall **not** pre-derive Packages/Documents/content-types (ADR-001, ADR-003). |
| IF-007-002 | C1 · C2 | C1 shall, on `WATCHED_FILES{changed}` for the configuration file, forward the **raw** `events` (API-001) without classification; C2 shall classify D as the workspace configuration (it **owns** the config location — D-019) and route it into the `CONFIG_SAVE` pipeline (UC-005 Alt D). Both entry points converge on one C2 pipeline. |
| IF-007-003 | C2 · C1 | C2 shall acknowledge a `CONFIG_SAVE` with `SyncPayload` (affected documents; post-save rebuild/invalidation notice) (TJ-016/017; §5.1). C2 may ticket it (expected in v1, NFR-1.4), in which case it shall emit honest progress `begin…end` (§5.2; NFR-1.4) and a `TerminalEvent{Success}`; C1 shall fetch the terminal via `get_result` (API-002) and shall not poll to wait (F6.2). |
| IF-007-004 | C2 · C1 | C2 shall push a `DiagnosticsEvent{document, diagnostics}` for each document whose diagnostics changed as a result of the re-scope (D-015), with `request_id` optional (D-025); C1 shall map it to `publishDiagnostics`. |

### State Transition Requirements (ST)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| ST-007-001 | C2 | C2 shall redefine **State 3** membership from the saved configuration: documents that left a package are **released** from State 3 (and their ODB background work dropped — D-014/D-024); newly added members **enter** State 3 (with background build — FR-3.3/D-014/D-024) (ADR-007; TJ-016). |
| ST-007-002 | C2 | C2 shall **invalidate/re-schedule in-flight** Tasks and Jobs affected by the re-scope, so that final membership, priority states, and objects match the saved configuration (TJ-016; R-009-1). Cancelled client Tasks shall carry `TerminalEvent{status:Cancelled, reason:"system_cancelled"}` (D-018); queued/running Jobs are cancelled when their last waiter leaves (TJ-007). |
| ST-007-003 | C2 | **Override rule** (TJ-017; R-009-2): the configuration shall be applied **only** from the saved content — unsaved buffer edits of the configuration have **no** effect; open-text (buffer) edits shall **never** touch config-derived state or override a saved configuration; on a race, the **saved configuration wins** on structural facts. |

### Data Requirements (DR)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| DR-007-001 | C3 (via C2) | C2 shall invalidate/remove Datastore entries for documents that left the project scope (removed packages/members) and commit new build results for re-scoped documents — as the **single writer** (ADR-004); **no partial re-scope shall be observable** (atomic commit discipline, TJ-008). |
| DR-007-002 | C2 (+ C3) | C2 shall update the dependency graph (inter-package edges, external references) to match the saved configuration (NFR-2.1; FR-2.2). |
| DR-007-003 | C3 (invariant) | The Datastore remains passive; **no** component other than the ODB writes or invalidates entries (ADR-004; NFR-1.3; D-002 — no Datastore public API). C4 rebuild results become durable **only** via C2's commit (TJ-008). |

### Error Handling (EH)

| ID | Requirement |
| -- | ----------- |
| EH-007-001 | A save of an **unchanged** configuration shall be a safe **no-op**: no re-scope, no cancellations, no rebuilds; `Result{Success}` (idempotency; ADR-009 — bounded, discrete event). |
| EH-007-002 | An **unparseable** configuration shall be **rejected without partial application**: the current scope remains in effect (atomicity discipline, TJ-008); C2 returns `Result{Error{code:E_INVALID_REQUEST}}` (inline or ticketed terminal; §5 `ErrorCode`); C1 maps the error to its own protocol (R-008-1). |
| EH-007-003 | A `CONFIG_SAVE` where the configuration file is **absent** shall re-scope to **degraded mode** (no Packages — UC-001 Alt "No Project Configuration Found"): all documents released from State 3, affected in-flight work cancelled (TJ-016; D-014/D-024), package-scoped entries invalidated (ADR-004); `Result{Success}`. A later save re-creating the configuration re-triggers the initial build (UC-001). The `deleted` event itself is UC-006's path (D-016). |
| EH-007-004 | Re-scope cancellation of an in-flight Job: C4 shall cancel **cooperatively** within the run bound (INV-24/TJ-019) or complete; C2 shall **discard** results for documents that left the scope (TJ-008) — no commit for out-of-scope documents. |

### Software Component Requirements (SCR)

| ID | Component | Requirement |
| -- | --------- | ----------- |
| SCR-C1-007-001 | C1 | C1 shall, on `didSave` for the configuration file, submit `CONFIG_SAVE{workspace root, config location?}` (IF-007-001); shall, on a watched `changed` event, forward raw `WATCHED_FILES{events}` (IF-007-002); shall handle the `Submission` (inline `Result` or ticket); if ticketed, consume the progress stream + `TerminalEvent` and fetch the `Result` via `get_result` (API-002; F6.2 no-polling); shall map `DiagnosticsEvent` → `publishDiagnostics` (D-015) and `Error` → its own protocol (R-008-1). |
| SCR-C1-007-002 | C1 | C1 shall **not** read/parse `gdoc.project.json` or pre-derive Packages/Documents/content-types (D-019; ADR-001) — its classification is URI-level only. C1 shall treat `CONFIG_SAVE` as a normal task lifecycle: it may cancel its own ticketed Task via `cancel(request_ids)` (D-012) and shall receive `TerminalEvent{Cancelled, reason:"user_canceled"}` (D-018). |
| SCR-C2-007-001 | C2 | C2 shall implement the `CONFIG_SAVE` pipeline: (1) read + parse the **saved** configuration from disk (D-019/INV-06; never the editor buffer — TJ-017); (2) diff the scope (Packages, members, content types, dependencies); (3) if changed, apply the re-scope — State 3 release/entry (ST-007-001), in-flight invalidation/re-schedule (ST-007-002; D-018 reasons), removed-scope Datastore invalidation + graph update (DR-007-001/002); (4) dispatch rebuild Jobs for affected scopes (TJ-005/009/011/012; ADR-007); (5) commit results atomically (TJ-008); (6) push `DiagnosticsEvent`s (D-015; D-025); (7) ack with `SyncPayload` / terminal `Result{Success}` (IF-007-003); (8) handle the error cases EH-007-001…EH-007-004. |
| SCR-C3-007-001 | C3 | The Datastore shall support scope invalidation/removal and new-result commits as **ODB-only** atomic operations (ADR-004; DR-007-001/003); it shall remain passive (NFR-1.3). |
| SCR-C4-007-001 | C4 | C4 shall execute rebuild Jobs (Parse/Link/Compile) for re-scoped documents, building from the context dispatched at run time (dedup-key inputs: content types, dependency state, build options — TJ-005); shall cancel **cooperatively** on re-scope cancellation within the run bound (INV-24/TJ-019); shall **not** write to the Datastore (ADR-004; TJ-008). |

## Reverse-check

| ID | Phase 1a/1b contract rule | Satisfied? | Notes |
| -- | ------------------------- | :--------: | ----- |
| IF-007-001 | §4.1 `CONFIG_SAVE` (payload: workspace root **required** — D-019) · API-001 | ⚠️ | Operation + payload are normative; *how C1 recognizes which saved file is the config* (location discovery: workspace-root convention vs. ODB-reported) is C1's mapping concern (R-008-1) and not pinned in the contract — to be made explicit in Phase 3 LSP-*. |
| IF-007-002 | D-019 · UC-005 Alt D (routing) · API-001 `WATCHED_FILES` | ✅ | raw-forward + ODB-classifies pattern established in UC-005 |
| IF-007-003 | §5.1 `SyncPayload` (TJ-016/017 note) · §4 progress note (`CONFIG_SAVE` expected ticketed in v1) · API-002 · F6.2 | ✅ | |
| IF-007-004 | §5.2 `DiagnosticsEvent` (D-015; `CONFIG_SAVE` a listed trigger) · D-025 (optional `request_id`) | ✅ | |
| ST-007-001 | TJ-016 (State-3 membership redefined) · ADR-007 · D-014/D-024 (TJ-021) | ✅ | |
| ST-007-002 | TJ-016 (in-flight invalidated/re-scheduled) · R-009-1 · D-018 · TJ-007 | ✅ | |
| ST-007-003 | TJ-017 · R-009-2 | ✅ | |
| DR-007-001 | ADR-004 · TJ-008 · TJ-016 (rebuild/invalidation) | ✅ | |
| DR-007-002 | NFR-2.1 · FR-2.2 · TJ-016 | ✅ | |
| DR-007-003 | ADR-004 · NFR-1.3 · D-002 (no Datastore public API) | ✅ | |
| EH-007-001 | ADR-009 (bounded, discrete event) · API-001 | ✅ | |
| EH-007-002 | §5 `ErrorCode` (`E_INVALID_REQUEST`) · TJ-008 (no partial commit) | ✅ | stable code set; mapping to LSP errors is C1's (R-008-1) |
| EH-007-003 | UC-001 Alt (degraded mode) · TJ-016 · D-016 (boundary with UC-006) | ✅ | |
| EH-007-004 | INV-24/TJ-019 · TJ-008 | ✅ | |
| SCR-C1-007-001 | §4.1 · API-001/002 · F6.2/6.3/6.4 · D-015 | ✅ | facade discipline normative |
| SCR-C1-007-002 | D-019 · ADR-001 · D-012 | ✅ | |
| SCR-C2-007-001 | TJ-016/017 · D-019 · ADR-004/007/009 · D-015/D-018 | ✅ | |
| SCR-C3-007-001 | ADR-004 · NFR-1.3 | ✅ | |
| SCR-C4-007-001 | TJ-005 · INV-24/TJ-019 · TJ-008 · ADR-004/005 | ✅ | |

> **Findings (1 ⚠️, zero ❌):** every UC-007 requirement is grounded in the Phase 1a/1b contracts, with a single partial item: the C1-side rule for *"which saved file is the configuration"* (location discovery on `didSave`) is C1's mapping concern (R-008-1) and is not pinned in the contract — recorded here as a reverse-check note (⚠️), **no contract change required**; to be made explicit in the Phase 3 LSP-*.

---

## Traceability Matrix

| Requirement ID | Type | FR | NFR | ADR | TJ | INV | D-xxx | API |
| -------------- | ---- | -- | --- | --- | -- | --- | ----- | --- |
| IF-007-001 | IF | FR-1.1 | — | ADR-001, ADR-003, ADR-009 | — | — | D-005, D-017, D-019 | API-001, §4.1 |
| IF-007-002 | IF | FR-1.1 | — | ADR-009 | — | — | D-016, D-019 | API-001 |
| IF-007-003 | IF | FR-1.1 | NFR-1.4 | ADR-009 | TJ-016, TJ-017 | — | D-011, D-015 | API-001, API-002, §4.1, §5.1 |
| IF-007-004 | IF | FR-4.2 | — | ADR-008 | — | — | D-015, D-025 | §5.2 |
| ST-007-001 | ST | FR-2.2, FR-3.3 | — | ADR-007, ADR-009 | TJ-016, TJ-021 | — | D-014 → D-024 | — |
| ST-007-002 | ST | — | NFR-2.3 | ADR-007, ADR-009 | TJ-007, TJ-016 | — | D-018 | §5.2 |
| ST-007-003 | ST | — | NFR-2.1 | ADR-009 | TJ-017 | — | — | — |
| DR-007-001 | DR | FR-2.2 | NFR-1.3, NFR-2.1 | ADR-004 | TJ-008, TJ-016 | — | D-002 | — |
| DR-007-002 | DR | FR-2.2 | NFR-2.1 | ADR-004 | TJ-016 | — | — | — |
| DR-007-003 | DR | — | NFR-1.3 | ADR-004 | TJ-008 | — | D-002 | — |
| EH-007-001 | EH | — | — | ADR-009 | — | — | D-005 | API-001 |
| EH-007-002 | EH | FR-4.1 | NFR-3.2 | — | TJ-008 | — | — | §5 (`ErrorCode`) |
| EH-007-003 | EH | — | — | ADR-004, ADR-009 | TJ-016 | — | D-014 → D-024, D-016 | — |
| EH-007-004 | EH | — | NFR-3.2 | ADR-004 | TJ-008, TJ-019 | INV-24 | — | §5.2 |
| SCR-C1-007-001 | SCR | FR-1.1 | NFR-1.4, NFR-3.1 | ADR-008, ADR-009 | — | — | D-012, D-015, D-017, D-019 | API-001/002, §4.1, §6, §7 |
| SCR-C1-007-002 | SCR | FR-1.1 | — | ADR-001 | — | — | D-012, D-018, D-019 | §5.2 |
| SCR-C2-007-001 | SCR | FR-2.2, FR-3.3 | NFR-2.1, NFR-2.3, NFR-3.1 | ADR-004, ADR-007, ADR-009 | TJ-005, TJ-008, TJ-009, TJ-011, TJ-012, TJ-016, TJ-017 | — | D-014 → D-024, D-015, D-018, D-019, D-025 | §4.1, §5.1, §5.2 |
| SCR-C3-007-001 | SCR | — | NFR-1.3 | ADR-004 | TJ-008 | — | D-002 | — |
| SCR-C4-007-001 | SCR | — | NFR-2.3, NFR-3.2 | ADR-004, ADR-005 | TJ-005, TJ-019 | INV-24 | — | — |
