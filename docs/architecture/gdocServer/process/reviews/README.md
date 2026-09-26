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

Per-round prefixes, unique across the set: `NC-*` (inconsistencies) · `OM-*` (omissions) · `ED-*` (edge cases) · `FU-*` (decision-propagation follow-up) · `RV-*` (general review rounds, from 2026-09-26).
Locations are cited by **file + §/requirement ID** (line numbers are auxiliary only).

## Review rounds

| File | Date | Scope | Findings | Status |
| ---- | ---- | ----- | -------- | ------ |
| `review-2026-09-14.md` | 2026-09-14 | Round 1 — Phase 0 → 1b cross-document | NC-01…06, OM-01…07, ED-01…03, minor×3 | ✅ closed (D-014…D-018 confirmed) |
| `review-2026-09-14-followup.md` | 2026-09-14 | Round 2 — D-014…018 propagation | FU-01…08 | ✅ closed (all [F]) |
| `record-2026-09-15-post-phase2.md` | 2026-09-15 | Post-Phase-2 decisions (traceability) | P2-003, P2-004 (summary) | ✅ |
| `review-2026-09-26.md` | 2026-09-26 | Phase 0 → UC-003 (Phase 2 in progress) | RV-01…07 | ✅ closed (all [F], 2026-09-26) |

## Change history

- 2026-09-26: review records moved from `process/design_review_record.md` into this folder (per-round files, content migrated verbatim); review procedure documented in `Design Review Procedure.md` (this folder — repo-resident, since the `.agents/` setup is not yet stable). (D-022)

*Record maintained alongside the design document set. Update status as decisions are confirmed and fixes applied.*
