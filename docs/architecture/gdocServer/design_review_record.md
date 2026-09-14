# Design Review Record

> **Scope:** Cross-document consistency and completeness review of Phase 0 - Phase 1b documents.
> **Date:** 2026-09-14
> **Status legend:** [F] = Fixed, [C] = Confirmed, [D] = Deferred to later phase

---

## 1. Inconsistencies

| ID | Finding | Affected File(s) | Status | Notes |
| --- | --- | --- | --- | --- |
| NC-01 | README.md Phase 3 step 4 attributed in-memory/thread-safe/single-writer to NFR-3.1. Correct: NFR-1.3 + NFR-2.2. | README.md L354 | [F] Fixed | Changed to (NFR-1.3/2.2). |
| NC-02 | TJ-008: Builder commits to Datastore contradicts ADR-004 (ODB is sole writer). | task-job-management.md | [F] Fixed | Reworded to ODB commits Builder candidate. |
| NC-03 | frontend-odb-api.md s4.3: Builder as C3; correct is C4. | frontend-odb-api.md L188/190 | [F] Fixed | C3 to C4. |
| NC-04 | TJ-018 fresh-iff ignores dependency changes; TJ-005 covers via dedup key. | task-job-management.md | [F] Fixed | Added dependency note. |
| NC-05 | Background builds (State 2/3): no Request, no Task, empty waiter, immediate cancel. | TJ-001/004/007 | [C] Confirmed | **D-014 = A (System Task).** |

---

## 2. Omissions / Underspecified

| ID | Finding | Status | Notes |
| --- | --- | --- | --- |
| OM-01 | Diagnostics delivery path undefined (LSP publishDiagnostics push). | [C] Confirmed | **D-015 = B (event push).** |
| OM-02 | didClose (State 2 release) has no explicit API payload action. | [C] Confirmed | **D-016 = action/type in payload.** |
| OM-03 | File deletion: no payload in WATCHED_FILES; Datastore cleanup undefined. | [C] Confirmed | Covered by D-016 (type:deleted). |
| OM-04 | No CONFIG_LOAD / INITIALIZE for workspace startup. | [D] Deferred | Phase 2 UC. |
| OM-05 | OperationPayload schema per operation undefined. | [C] Confirmed | **D-017 = alongside Phase 2.** |
| OM-06 | ErrorCode lacks policy-based cancel distinction (TJ-014). | [C] Confirmed | **D-018 = TerminalEvent.reason.** |
| OM-07 | E_NOT_BUILT trigger and recovery unexplained. | [D] Deferred | Phase 3. |

---

## 3. Edge Cases and Operational Concerns

| ID | Finding | Status | Notes |
| --- | --- | --- | --- |
| ED-01 | Cancelled tasks get TTL + ExpiryEvent noise. | [D] Deferred | Phase 3/4. |
| ED-02 | open_revision resets to 0 on didClose breaks monotonic ordering. | [D] Deferred | Phase 2 UC. |
| ED-03 | DefinitionPayload single position; LSP supports Location[]. | [F] Fixed | Now list format. |

---

## 4. Minor Issues (Typos / Notation)

| # | Finding | Status |
| --- | --- | --- |
| 1 | architecture.md L52: isuse to uses, to parses to to parse | [F] Fixed |
| 2 | README.md s4.1 ID table missing F prefix | [F] Fixed |
| 3 | task-job-management.md s4: TJ-005/006 missing NFR-3.1 in Derived From | [F] Fixed |

---

## 5. Decisions Requiring User Confirmation

> These are the **design decisions** that must be settled before Phase 2 (use-case analysis) begins.
> Each has a **recommended option** with rationale. Please confirm or propose alternatives.

### D-014: Background Build Task Model (NC-05)

**Problem:** State 2 (references of open files) and State 3 (package members) trigger background builds with **no client Request**. Per TJ-001 (1:1:N) and TJ-007 (waiter set), no Task = empty waiter set = Job immediately cancelled.

**Options:**

| Option | Description | Pros | Cons |
| -------- | ------------- | ------ | ------ |
| **A (recommended)** | **System Task.** ODB generates internal Task on State 2/3 entry. In waiter set. Cancelled when doc leaves state. | Preserves 1:1:N. Unified cancel. | Extends TJ-001 trigger. Needs s-* ID namespace. |
| B | State = implicit waiter. | No extra objects. | Breaks TJ-001/007 definitions. |
| C | Background Job exception class. | No model change. | Two Job lifecycles. |

**If A confirmed, new rules:** (1) TJ-001 trigger = Request OR state-transition. (2) ID: s-* namespace. (3) Cancel on didClose/deletion/config-change. (4) NOT cancellable by Frontend. (5) DOCUMENT_SYNC{close}+cancel = full shutdown.

**User decision:** [x] A (System Task)  [ ] B  [ ] C  [ ] Other: _______

---

### D-015: Diagnostics Delivery Path (OM-01)

**Problem:** v1 core feature (D-005) but no delivery mechanism defined. LSP publishDiagnostics is server-to-client push.

**Options:**

| Option | Description | Pros | Cons |
| -------- | ------------- | ------ | ------ |
| A | Embed in SyncPayload. | 1 round trip. | Not LSP-idiomatic. |
| **B (recommended)** | **Event stream.** Add DiagnosticsEvent to RequestEvent. ODB pushes after build. | LSP-idiomatic. Reuses handler. | Doc-scoped event. |
| C | Frontend pulls via submit(DIAGNOSTICS). | No new API. | N+1 round trips. |

**If B confirmed:** (1) Add DiagnosticsEvent to RequestEvent union. (2) ODB pushes after sync/watched/config. (3) DIAGNOSTICS pull coexists.

**User decision:** [ ] A  [x] B (event push)  [ ] C  [ ] Other: _______

---

### D-016: Document Lifecycle API (OM-02, OM-03)

**Problem:** didClose and file deletion have no explicit payload. ODB cannot distinguish open/change/close or created/changed/deleted.

**Recommended - add action/type discriminators:**

```
DOCUMENT_SYNC: { action: "open"|"change"|"close", content?: string }
WATCHED_FILES: { events: [{uri, type: "created"|"changed"|"deleted"}] }
```

**Behavior:** close releases State 2 + cancels System Task. deleted removes Datastore entry + invalidates graph. Frontend sends BOTH sync and cancel.

**User decision:** [x] OK with action/type in payload  [ ] Prefer separate operations  [ ] Other: _______

---

### D-017: Request Payload Schema (OM-05)

**Problem:** Per-operation required fields not defined.

**Recommendation:** Add table in frontend-odb-api.md s4:

| Operation | Required | Optional |
| ----------- | ---------- | ---------- |
| HOVER | position (line, character) | - |
| DEFINITION | position (line, character) | - |
| REFERENCES | position, include_declarations: bool | - |
| DIAGNOSTICS | - (document ref suffices) | - |
| DOCUMENT_SYNC | action, content? (for open/change) | - |
| WATCHED_FILES | events: [{uri, type}] | - |
| CONFIG_SAVE | - (document ref identifies config) | - |

> Not a design decision - formalization of existing intent. Can be done alongside Phase 2.

**User decision:** [x] OK - formalize alongside Phase 2  [ ] Define now  [ ] Other: _______

---

### D-018: Policy Cancellation Distinction (OM-06)

**Problem:** ODB policy cancel (TJ-014) and user cancel both produce status:Cancelled. Frontend cannot distinguish.

**Recommendation:** No new ErrorCode. Add optional `reason?: string` to TerminalEvent:

- "user_canceled" | "policy_deferred" | "system_cancelled"
- Frontend: did NOT call cancel() + got Cancelled = policy/system.
- Cancelled remains a normal outcome, not an error.

**User decision:** [x] OK - TerminalEvent.reason  [ ] Prefer new ErrorCode  [ ] Other: _______

---

## 6. Items Deferred to Later Phases

| ID | Deferred to | Rationale |
| --- | --- | --- |
| OM-04 | Phase 2 (UC: Open Workspace) | ODB is a library; init outside 4-API surface. |
| OM-07 | Phase 3 (ODB requirements) | Low impact. |
| ED-01 | Phase 3/4 | Operational tuning. |
| ED-02 | Phase 2 (UC: Close Text) | Equality-based freshness limits impact. |

---

## 7. Summary

| Category | Total | Fixed | Confirmed | Deferred |
| ---------- | ------- | ------- | --------- | -------- |
| Inconsistencies | 5 | 4 | 1 | 0 |
| Omissions | 7 | 0 | 5 | 2 |
| Edge Cases | 3 | 1 | 0 | 2 |
| Minor Issues | 3 | 3 | 0 | 0 |
| **Total** | **18** | **8** | **6** | **4** |

**All 6 awaiting items now confirmed (D-014 through D-018).**

---

*Record maintained alongside the design document set. Update status as decisions are confirmed and fixes applied.*
