# Record — 2026-09-15 (Post-Phase-2 decisions, traceability summary)

> **Provenance:** Migrated (2026-09-26) from `process/design_review_record.md` (original §9).

> Authoritative log: `process/phase2/plan.md` §6. Entries below are summarized for traceability.

| ID | Decision | Scope |
| -- | -------- | ----- |
| P2-004 | UC derived-requirement ID scheme changed to **per-UC namespace** (`IF/ST/DR/EH-<UC>-<NNN>`, `SCR-<COMP>-<UC>-<NNN>`, e.g. `IF-002-001`, `SCR-C1-002-001`); append-only numbering within a UC | README §4.1, `process/phase2/template.md`, `usecases/UC-001_OpenWorkspace.md`, `usecases/UC-002_OpenText.md` (36 IDs renamed) |
| P2-003 | NC-06 open item resolved to the "YES" branch (request-less `DiagnosticsEvent` push exists); contract relaxation of `RequestEvent.request_id` (optional for `DiagnosticsEvent`/`ExpiryEvent`) **applied 2026-09-15** | `contracts/frontend-odb-api.md` §5.2 + API-004 (done); NC-06 closed (§2) |


*Record maintained alongside the design document set. Update status as decisions are confirmed and fixes applied.*
