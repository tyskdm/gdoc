# Phase 2 — Work Plan: Use Case Analysis

> **Purpose:** Unify behavioral evidence (use cases) for v1 scope, reverse-check Phase 1 contracts,
> and establish the requirement decomposition per component that Phase 3 will verify.
> **Position:** `docs/architecture/gdocServer/process/phase2/plan.md`
> **Status:** 🟡 In Progress — Step 1 (UC-001 ✅, UC-002 ✅, UC-003 ✅, UC-004…007 ⬜)

> **Related:** `../../README.md` §8 (Phase 2 definition · **authoritative procedure**)
> · `../../contracts/task-job-management.md` (TJ-*)
> · `../../contracts/frontend-odb-api.md` (API-*) · `../../subcomponents/README.md` (glossary + ownership)
>
> **Skill & Template (local):** `./skill.md` (analysis procedure) · `./template.md` (UC output structure)
> These are **project-specific** tailoring of `.agents/skills/usecase-analysis/` and `.agents/templates/`.
> **Use these local files, not the `.agents/` originals.**
>
> **This file is a work tracker.** The authoritative procedure lives in `../../README.md` §8.
> Do not duplicate procedure text here.

---

## 1. UC Inventory (v1 scope per D-005)

| UC-ID | Name | Category | Trigger (LSP event) | FR/NFR | Status |
| ----- | ---- | -------- | ------------------- | ------- | ------ |
| UC-001 | Open Workspace | Lifecycle | `initialize` / `initialized` | FR-1.1, NFR-1.1 | ✅ |
| UC-002 | Open Text | Sync | `textDocument/didOpen` | FR-1.3, NFR-2.3 | ✅ (2026-09-15; NC-06 resolved → P2-003 applied 2026-09-15) |
| UC-003 | Edit Text | Sync | `textDocument/didChange` | FR-1.3, NFR-2.3 | ✅ (2026-09-25; D-020 applied; findings → TJ-012 note + `frontend-odb-api.md` §4.1, user-approved) |
| UC-004 | Close Text | Sync | `textDocument/didClose` | FR-1.3, D-016 | ⬜ |
| UC-005 | Watched File Change | Sync | `workspace/didChangeWatchedFiles` (changed) | FR-1.3, ADR-007 | ⬜ |
| UC-006 | File Deletion | Sync | `workspace/didChangeWatchedFiles` (deleted) | D-016, FR-2.1 | ⬜ |
| UC-007 | Config Save | Config | `textDocument/didSave` (config) / watched | ADR-009, FR-2.2 | ⬜ |
| UC-008 | Hover | Query | `textDocument/hover` | FR-1.2 | ⬜ |
| UC-009 | Go to Definition | Query | `textDocument/definition` | FR-1.2 | ⬜ |
| UC-010 | Find References | Query | `textDocument/references` | FR-1.2, NFR-1.4 | ⬜ |
| UC-011 | Diagnostics | Push | (server→client push, D-015) | FR-1.2, D-015 | ⬜ |

> **Scope note:** Semantic Tokens, Completion, Rename, Document Symbols are **v2 (D-005 provisional)** —
> excluded from Phase 2.
>
> **Diagnostics (UC-011)** is a **server-initiated push** (D-015 `DiagnosticsEvent`), not a
> client-initiated request. It coexists with a `DIAGNOSTICS` pull operation.

---

## 2. Step Status

| Step | Description | Status |
| ---- | ----------- | ------ |
| 1 | Sync + Lifecycle UCs (UC-001…007) | 🟡 3/7 (UC-001, UC-002, UC-003 ✅) |
| 2 | Query UCs (UC-008…011) | ⬜ |
| 3 | Reverse-check + Gap Analysis | ⬜ |
| 4 | Archive + Final Status Update | ⬜ |

> Authoritative DoD: `../../README.md` §8 Phase 2.

### Step 1 checklist

- [ ] UC-001…007 exist in `usecases/`, follow `./template.md`
- [ ] All 7 have complete SCR-C1/C2/C3/C4 requirements (none empty)
- [ ] UC-004 (Close) shows cancellation (TJ-016) + Datastore cleanup
- [ ] UC-005/006 (Watch/Deletion) show DOCUMENT_SYNC discriminator per D-016
- [ ] UC-007 (Config Save) shows ADR-009 config reload behavior
- [ ] All 7 have Reverse-check tables populated (zero ❌ at step end)

### Step 2 checklist

- [ ] UC-008…011 exist in `usecases/`, follow `./template.md`
- [ ] All 4 have complete SCR-C1/C2/C3/C4 requirements
- [ ] UC-008/009 show ticket → get_result → TerminalEvent flow (D-014)
- [ ] UC-010 shows progress events (begin/report/end) per NFR-1.4
- [ ] UC-011 shows `DiagnosticsEvent` push (D-015) + Frontend maps to `publishDiagnostics`
- [ ] All 4 have Reverse-check tables populated

### Step 3 checklist

- [ ] Every TJ-001…TJ-021 exercised by ≥1 UC
- [ ] Every API-001…API-004 exercised by ≥1 UC
- [ ] Every D-014…D-018 reflected in ≥1 UC
- [ ] Gap report written ("no gaps" or "gaps + proposed fixes")
- [ ] If gaps: proposed contract additions logged
- [ ] **User approval to proceed** (gate per README §4.5)

### Step 4 checklist

- [ ] Archive `usecases/` (old) → `archive/usecases-legacy/`
- [ ] Archive `usecase_analysis/` → `archive/usecase-analysis-legacy/`
- [ ] New UCs confirmed in `usecases/` (UC-001…UC-011)
- [ ] README §5 Status → Phase 2 ✅
- [ ] README §7 updated with any new decisions (D-019+)
- [ ] 3-point set report to user (DoD / Gaps / Pending)

---

## 3. Decision Log (Phase 2)

> Append-only. Records decisions made during Phase 2 execution.

| ID | Date | Decision | Rationale | Status |
| -- | ---- | -------- | --------- | ------ |
| P2-001 | 2026-09-15 | Start from scratch; archive existing UCs after rewrite | Existing UCs have ID collisions, outdated terminology, D-014…D-018 gaps; cost of fixing > writing fresh | ✅ |
| P2-002 | 2026-09-15 | File Deletion is an independent UC (UC-006) | `architecture.md` lists it as a separate scenario; D-016 gives it unique behavior (Datastore cleanup + Job cancel + graph invalidation) | ✅ |
| P2-003 | 2026-09-15 | **Finding (from UC-002 reverse-check):** NC-06 open item resolved to the **"YES" branch** — a request-less `DiagnosticsEvent` push **exists** (System-Task reference-closure builds, D-014, produce diagnostics with no triggering client request). Contract relaxation applied: `RequestEvent.request_id` **optional** for `DiagnosticsEvent`/`ExpiryEvent` (document-scoped pushes invoke the handler with no `request_id`); `ProgressEvent`/`TerminalEvent` keep it required; no API operation changes | **Applied 2026-09-15** to `frontend-odb-api.md` §5.2 (envelope + OPEN ITEM note → RESOLVED) and API-004 event-stream note; NC-06 closed in `process/design_review_record.md` | ✅ (user approved 2026-09-15) |
| P2-004 | 2026-09-15 | **ID scheme changed to per-UC namespace:** derived-requirement IDs are now `IF/ST/DR/EH-<UC>-<NNN>` and `SCR-<COMP>-<UC>-<NNN>` (3-digit UC number; e.g. `IF-002-001`, `SCR-C1-002-001`); numbering is **append-only within a UC** — adding a requirement to one UC never touches other files; UC-001/UC-002 IDs renamed (36 IDs); README §4.1, template, and both UC file headers updated | Avoids consulting other UC files for numbering; prevents ID collisions structurally; done before Phase 3 references any UC ID (last low-cost window) | ✅ (user approved 2026-09-15) |
| P2-005 | 2026-09-25 | **UC-003 findings applied (user-approved):** (1) **dispatch-skip of stale queued Jobs** added to `contracts/task-job-management.md` as an **efficiency note on TJ-012** (should-level: "a queued Job for a `(file, version, inputs)` whose document `version_id` is no longer current should not be dispatched; dispatch permitted, but its result must not become the 'current' entry — TJ-018") — from UC-003 ST-003-002/SCR-C2-003-002; (2) **`DOCUMENT_SYNC` `content` requirement clarified** in `contracts/frontend-odb-api.md` §4.1 — required for `action:"open"`/`"change"` (open document), optional for `action:"close"` (clarifies D-017's `action` + `content?` entry; the full normative D-017 table is still to be written during Phase 2) | Both findings were recorded as "awaiting user approval" per gate §4.5; user chose option **A** (note on TJ-012, not a new rule ID) and approved the §4.1 wording clarification | ✅ (user approved 2026-09-25) |

---

## 4. References

| Source | Use |
| ------ | --- |
| `./skill.md` | **Local tailored skill** — procedure for each UC (use this, not `.agents/`) |
| `./template.md` | **Local tailored template** — UC output structure (use this, not `.agents/`) |
| `../../contracts/task-job-management.md` | TJ-001…TJ-021 — rules to cross-reference |
| `../../contracts/frontend-odb-api.md` | API-001…004, Request/Result/Event models |
| `../../subcomponents/README.md` §4/§6 | Ownership matrix + glossary |
| `../../requirements/requirements.md` | FR/NFR origin |
| `../../adr/*.md` | Strategic decisions (context, not re-derived) |
| `../../README.md` §7 | D-001…D-018 decisions |
| `../../usecase_analysis/*.md` | **Reference only** (LSP links, Task Queue, close scenarios) |
| `../../usecases/*.md` (old) | **Reference only** (scenario content for OpenText/EditText/GoToDef) |
| LSP 3.17 spec | Protocol-level details (links in `usecase_analysis/1. Open Workspace.md`) |
