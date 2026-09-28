# Design Review Records — Index

> One file per review round: `review-YYYY-MM-DD[-suffix].md`; `record-*.md` for decision / traceability notes.
> **The single source of record for design decisions is `../README.md` §7 (D-*)** — review files record *findings and resolutions*, not decisions.
> **Review procedure (when / how to review, recording & commit conventions):** `Design Review Procedure.md` (this folder — kept in the repo because the `.agents/` setup is not yet stable).

## Status legend (shared by all review files)

| Tag | Meaning |
| --- | ------- |
| [O] | Open — recorded, not yet actioned |
| [F] | Fixed — resolution + verification recorded in the row |
| [C] | Confirmed — finding valid, resolved as a decision |
| [D] | Deferred — to a later phase (reason in row) |
| [R] | Resolved — closed (e.g. by a later contract change) |
| [P] | Pending fix — a follow-up pass owns the fix |
| [?] | Needs user decision (A/B options recorded in the file) |

## Findings ID scheme

Per-round prefixes, unique across the set: `NC-*` (inconsistencies) · `OM-*` (omissions) · `ED-*` (edge cases) · `FU-*` (decision-propagation follow-up) · `RV-*` (general review rounds, from 2026-09-26) · `CA-*` (cross-model consistency audit, 2026-09-26) · `GL-*` (GPT-5.6 Luna review round, 2026-09-26) · `GE-*` (Gemini 3.8 Flash review round, 2026-09-26) · `DV-*` (D-024 de-specification verification round, 2026-09-27) · `ID-*` (identifier-dependency audit round, 2026-09-27).
Locations are cited by **file + §/requirement ID** (line numbers are auxiliary only).

## Review rounds

| File | Date | Scope | Findings | Status |
| ---- | ---- | ----- | -------- | ------ |
| `review-2026-09-14.md` | 2026-09-14 | Round 1 — Phase 0 → 1b cross-document | NC-01…06, OM-01…07, ED-01…03, minor×3 | ✅ closed (D-014…D-018 confirmed) |
| `review-2026-09-14-followup.md` | 2026-09-14 | Round 2 — D-014…018 propagation | FU-01…08 | ✅ closed (all [F]) |
| `record-2026-09-15-post-phase2.md` | 2026-09-15 | Post-Phase-2 decisions (traceability) | P2-003, P2-004 (summary) | ✅ |
| `review-2026-09-26.md` | 2026-09-26 | Phase 0 → UC-003 (Phase 2 in progress) | RV-01…07 | ✅ closed (all [F], 2026-09-26) |
| `review-2026-09-26-Qwen3.8:27b.md` | 2026-09-26 | Phase 0 → UC-003 (independent cross-model audit) | CA-01…07 | ✅ closed (all [F], 2026-09-26) |
| `review-2026-09-26-GPT-5.6 Luna.md` | 2026-09-26 | Phase 0 → UC-003 (evaluation of Findings 1–3) | GL-01…03 | ✅ closed (all [F], 2026-09-26) |
| `review-2026-09-26-gemini-3.8-flash.md` | 2026-09-26 | Phase 0 → UC-003 (contract-anchored consistency check) | GE-01…04 | ✅ closed (all [F], 2026-09-26) |
| `review-2026-09-27-D-024-despec.md` | 2026-09-27 | D-024 de-specification — verification round (V1–V11 independent re-execution) | DV-01…06 | ✅ closed (all [F], 2026-09-27) |
| `review-2026-09-27-identifier-audit.md` | 2026-09-27 | Identifier & dependency-structure audit (process → design ID leakage, derivation chains, namespace hygiene) | ID-01…05 | ✅ closed (ID-01…04 [F], ID-05 [C] Option A; D-025 issued, FR-3.3 added) |

## Change history

- 2026-09-26: review records moved from `process/design_review_record.md` into this folder (per-round files, content migrated verbatim); review procedure documented in `Design Review Procedure.md` (this folder — repo-resident, since the `.agents/` setup is not yet stable). (D-022)
- 2026-09-26: independent cross-model consistency audit recorded as `review-2026-09-26-Qwen3.8:27b.md`; CA-01…CA-07 found and fixed the same day (D-019 propagation into IF-001-004, event status `Success` per contract §5.2, `get_result` fetch step, TerminalEvent Task attribution, §5.2 `request_id` optional phrasing, postconditions main-flow qualifier, UC-002 Alt A example).
- 2026-09-26: review round recorded as `review-2026-09-26-GPT-5.6 Luna.md`; GL-01…GL-03 found and fixed the same day (GL-01 DiagnosticsEvent push suppression on unchanged diagnostics in UC-001/003; GL-02 System Tasks one per State 2 document in reference closure in UC-002/003; GL-03 semantic tokens qualified as v2 provisional per D-005 in architecture.md).
- 2026-09-26: review round recorded as `review-2026-09-26-gemini-3.8-flash.md`; GE-01…GE-04 found and fixed the same day (GE-01 System Task lifecycle alignment in UC-003; GE-02 DR-003-002 scoping/ownership; GE-03 event push order standardization in UC-002/003; GE-04 CONFIG_SAVE degraded-mode TerminalEvent + get_result step in UC-001).
- 2026-09-27: D-024 de-specification verification round recorded as `review-2026-09-27-D-024-despec.md`; DV-01…DV-06 found and fixed the same day after user approval (DV-01 UC-002 unit-count phrasing → NC-05 coverage form; DV-02 change-record status → [R] Resolved with executed commit `e8605db`; DV-03 D-016 row "System Task" → "background build work"; DV-04 D-014 row supersession pointer + status; DV-05 V5 label decomposition 21+21=42; DV-06 record-body NC-05 scope aligned to Q-A(a) + derivation note).
- 2026-09-27: identifier-dependency audit round recorded as `review-2026-09-27-identifier-audit.md` (supporting evidence: `process/identifier-dependency-audit.md`, read-only); ID-01…ID-05 found and fixed the same day after user approval (ID-01 NC-05 demoted from normative text → FR-3.3/D-024 anchors; ID-02 **D-025 issued** in README §7, 11 citations re-pointed — Option A; ID-03 ①/②/③ tier symbols defined in `task-job-management.md` §2; ID-04 `C<n>`/`INV-NN`/`D-nn` rows added to README §4.1; ID-05 **FR-3.3 added** to requirements.md + prepended to TJ-021 Derived-From — Option A).

*Record maintained alongside the design document set. Update status as decisions are confirmed and fixes applied.*
