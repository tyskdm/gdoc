# Design Review — 2026-09-27 (identifier-dependency audit round)

> **Reviewer:** Cline-led cross-document audit (user-requested) — exhaustive grep enumeration of every ID family in the design set (`NC-*`, `OM-*`, `FU-*`, `P2-*`, `D-*`, `Q-*`, `INV-*`, `TJ-*`, `SCR-*`, tier symbols ①②③), each hit classified as **proper provenance** vs **normative dependency**; derivation chains read per rule and compared against `README.md` §4.2.
> **Scope:** all design-set documents (`README.md`, `requirements/`, `adr/`, `architecture.md`, `usecases/`, `usecase_analysis/`, `subcomponents/`, `contracts/`) checked against `process/` artifacts for (a) identifier cross-reference consistency, (b) derivation-chain integrity, (c) prefix ↔ document-type assignments, (d) improper process → design dependencies.
> **Method:** `Design Review Procedure.md` §2.3 mechanical checks — per-family enumeration, per-hit classification (proper vs normative), derivation-chain verification (TJ-001…TJ-021), prefix registry cross-check against `README.md` §4.1.
> **Supporting artifact (read-only; no action required):** `process/identifier-dependency-audit.md` — per-citation evidence tables, prefix registry, derivation analysis, Mermaid diagrams, grep-verified appendix (2026-09-27).
> **Excluded (by design, recorded for auditability):** UC-004…011 (undrafted) · D-020/D-021/D-022/D-023 scope · `process/` records as mutable history (they are the *sources* being audited, not review targets) · `usecase_analysis/` C-01…C-09 (self-contained draft namespace, no collision) · `traceability.md` mechanical checks (Phase 4 — file does not yet exist).

## 1. Purpose, concern & review perspective

**Why this round exists.** The design set maintains a strict derivation discipline (`README.md` §4.2: Rank 1 requirements → … → Rank 6 use cases), and `process/` (reviews, change records, phase plans) is **governance history, not a normative source** of the set. The concern that motivated this round: over the course of the review rounds, **process-artifact IDs (NC-*, P2-*) began to appear inside normative design text** — so that a `shall` clause now depends for its meaning on a mutable review record, and a reader of the design set alone can no longer resolve every term. If left unmanaged, the set's self-containment silently degrades, and a later review round that supersedes parts of that history could retroactively change the meaning of normative text.

**What was reviewed, in order of emphasis:**

1. **In-set resolvability (primary concern):** for every ID cited in a design document, can the design set alone resolve it? Each citation was classified as **proper provenance** (a decision-log row recording what it resolved; a traceability note) vs **normative dependency** (design text whose meaning requires a process record) — the latter is the violation class.
2. **Derivation-chain integrity:** do rules / contracts / use cases derive from the in-set ranks above them, and does every chain ultimately reach Rank 1 (FR/NFR)? In particular: are there **proxy anchors** that "reach" Rank 1 without naming the actual guarantee?
3. **Namespace hygiene:** does every ID prefix have exactly one owning document type in the `README.md` §4.1 registry? Any unregistered families (orphan IDs) or collisions between look-alike prefixes (e.g. `C1…C5` vs `C-01…C-09`)?
4. **Out of scope (by design):** the quality of individual decisions, UC behaviors, API details — those were the object of the earlier rounds (NC/RV/CA/GL/GE/DV). This round audits only the **identifier and dependency structure** between documents.

## 2. Findings (shared status legend: `README.md` in this folder)

| ID | Sev | Finding | Location (file + §; lines auxiliary) | Recommendation | Status | Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| ID-01 | med | **NC-05** is defined only in `process/reviews/review-2026-09-14.md` §1, yet cited in **normative** design text — including the **TJ-021 `shall`-clause anchor** ("…not dropped (NC-05)") — so an in-set reader must open a review record to resolve a term in normative text; `process/reviews/` is mutable history (later rounds already supersede parts of it) | `contracts/task-job-management.md` TJ-021 (L223) + §6 D-024 row (L340, proper) · `architecture.md` Task definition (L73) + background-build paragraph (L266) · `subcomponents/README.md` Task glossary row (L200) · `usecases/UC-001_OpenWorkspace.md` (L269, L410) · `usecases/UC-002_OpenText.md` (L97, L166) | demote to provenance — drop the bare ID from normative prose where the D-024 decision row already records the resolution; keep the ID in the decision log (`README.md` §7 — proper) | [F] | Approved 2026-09-27. Bare **NC-05** removed from all 8 normative/narrative sites; the guarantee is now anchored in-set by **FR-3.3** (`requirements/requirements.md` §3, added with ID-05 Option A) plus D-024. NC-05 survives only in proper provenance: `README.md` §7 (D-014, D-024 rows) and `contracts/task-job-management.md` §6 (D-024 traceability row). Verify: `grep -rn 'NC-05' README.md architecture.md subcomponents/ contracts/ usecases/ adr/ requirements/` → only those 3 decision/traceability rows. |
| ID-02 | med | **NC-06 / P2-003** are defined only in `process/reviews/review-2026-09-14.md` §1 + `process/phase2/plan.md`, yet annotate a **wire-format exception** in the contract (`request_id` optional for `DiagnosticsEvent`/`ExpiryEvent`) and UC-002/UC-003 narrative — the normative rule itself is self-contained, but the IDs are resolution markers with **no in-set anchor** | `contracts/frontend-odb-api.md` (L105, L264, L287, L297) · `usecases/UC-002_OpenText.md` (L371, L380, L388) · `usecases/UC-003_EditText.md` (L53, L395, L404) | issue **D-025** (in-set anchor for the NC-06/P2-003 resolution — see §3) and re-point normative citations to D-025; keep the historical IDs in decision-log rows | [F] | Approved 2026-09-27, **Option A**. **D-025** issued in `README.md` §7 (origin NC-06/P2-003 recorded there as provenance); all 11 citations re-pointed to D-025 — `contracts/frontend-odb-api.md` (API-004 event-stream exception, §5.2 schema comment, RESOLVED note, DiagnosticsEvent bullet), `usecases/UC-002_OpenText.md` (IF-002-002, SCR-C1-002-002, Resolved note), `usecases/UC-003_EditText.md` (D-015 bullet, IF-003-002, SCR-C1-003-002). Verify: `grep -rln 'NC-06\|P2-003' README.md architecture.md subcomponents/ contracts/ usecases/ adr/ requirements/` → only `README.md` (D-024/D-025 decision-log rows — proper). |
| ID-03 | low–med | the **①/②/③ tier taxonomy** (① guarantee · ② invariant rails · ③ mechanism) is used as a classification axis in 4 design docs, but its canonical naming lives only in the change record `process/changes/change-2026-09-27-despec-boundary-correction.md` §4–§5; the README D-024 row enumerates only (1)/(2)/(3) | `contracts/task-job-management.md` (TJ-021 ×4) · `contracts/frontend-odb-api.md` (×2) · `subcomponents/README.md` (×1) · `adr/007-priority-scheduling.md` (scope note ×1) | add a glossary entry naming ①/②/③ to `contracts/task-job-management.md` §2 (or `architecture.md` §1 vocabulary) so the taxonomy resolves in-set | [F] | Approved 2026-09-27. Tier-symbol line added to `contracts/task-job-management.md` §2 "Reading the rules": **① = guarantee** (FR-3.3; D-024 scope (1)) · **② = invariant rails** (D-024 scope (2)) · **③ = mechanism** — ODB-internal, not fixed (D-024 scope (3)). The taxonomy now resolves in-set; citing docs (frontend-odb-api, subcomponents, ADR-007) unchanged. Verify: `grep -n 'Tier symbols' contracts/task-job-management.md` → 1 hit (§2). |
| ID-04 | low | **INV-01…INV-30** (defined in-set, `subcomponents/README.md` §7), component IDs **C1–C5** (`subcomponents/README.md` §3), and the **D-nn** decision log (`README.md` §7) are **absent from the §4.1 ID-scheme registry** | `README.md` §4.1 (missing rows) · cited from `usecases/UC-001_OpenWorkspace.md` (INV-06 ×3) · `contracts/frontend-odb-api.md` (L166) · README D-017/D-019 rows | add §4.1 rows: `INV-01…INV-30` · `C1…C5` · `D-nn` (prefix · Home · scope) | [F] | Approved 2026-09-27. Three rows added to `README.md` §4.1: Component ID `C<n>` (Home `subcomponents/README.md` §3) · Phase-0 invariant `INV-NN` (Home `subcomponents/README.md` §4.1 single-owner matrix) · Decision log `D-nn` (Home `README.md` §7). Verify: `grep -n 'Component ID\|Phase-0 invariant\|Decision log' README.md` → 3 rows in §4.1. |
| ID-05 | low | **TJ-021** chain `FR-3.1/3.2 → ADR-002 → ADR-007 → D-014 → D-024` reaches Rank 1, **but** no FR/NFR states the guarantee itself ("a needed State 2/3 background build is not dropped; the ODB supplies its own waiters") — FR-3.1/3.2 (tiered abstraction / robust scheduling) act as **proxy anchors**; the true origin is review finding NC-05 | `contracts/task-job-management.md` TJ-021 · `requirements/requirements.md` (no guarantee statement) | **[?] needs user decision** — see §3 (Option A: explicit requirement; Option B: accept proxy + record in Phase 4) | [C] | User chose **Option A** (2026-09-27). **FR-3.3 "Background-build continuity"** added to `requirements/requirements.md` §3 (self-contained, Rank-1 clean — no process-ID references); **FR-3.3** prepended to TJ-021's Derived-From (rule body, §4 rule index, §6 TJ→upstream table) and to the Task glossary row's Derived-From in `subcomponents/README.md`. The guarantee is now explicitly stated at Rank 1 and TJ-021's chain reaches it directly. |

**Positive observations (no action):** all other ID traffic is **proper** — `D-*` decision citations in design docs (decisions sit legitimately between requirements and contracts); `OM-*`/`FU-*`/`DV-*`/`Q-*`/`DC-*` confined to `process/` records and decision-log rows that *resolved* them; `P2-*` outside the NC-06 context only in README §5/§8 roadmap + its own plan; TJ-001…TJ-020 all start `FR-3.x/4.x` (spot-verified). **No circular references, no dangling in-set IDs, no prefix collisions** (C1…C5 vs C-01…C-09 are distinct namespaces).

## 3. Decisions needed (per `Design Review Procedure.md` §6)

### D-025 (proposed): in-set anchor for the NC-06 / P2-003 resolution — ID-02

**Problem:** the `request_id` optionality rule (`frontend-odb-api.md` §5.2) and the UC-002/UC-003 narrative cite NC-06/P2-003, which exist only under `process/`. An in-set reader cannot resolve them; the rule's canonical origin is currently a review record.

**Options:**

| Option | Description |
| ------ | ----------- |
| **A (recommended)** | Log **D-025** in `README.md` §7: "`request_id` optional for `DiagnosticsEvent`/`ExpiryEvent` (handler may be invoked without one; Frontend routes by `document`); required for `ProgressEvent`/`TerminalEvent` — resolves NC-06 (P2-003)". Re-point the normative citations to D-025; the historical IDs remain in the D-025 row as provenance. |
| B | Leave citations as-is (accept the process → design provenance dependency). |

**User decision:** [x] **A** (2026-09-27) — issued; D-025 logged in `README.md` §7 and all normative citations re-pointed (see ID-02 Resolution).

---

### ID-05: TJ-021 proxy anchor — treatment?

**Problem:** no FR/NFR states the NC-05 guarantee explicitly ("a needed State 2/3 background build is not dropped; the ODB supplies its own waiters"); FR-3.1/3.2 are the nearest (proxy) anchors. The Phase 4 `traceability.md` matrix will show this as a loose link until the requirement layer names the guarantee.

**Options:**

| Option | Description |
| ------ | ----------- |
| A | Add an explicit requirement to `requirements.md` (e.g., under FR-3.x: "a needed State 2/3 background build is not dropped; the ODB supplies its own waiters") and prepend it to TJ-021's Derived-From. |
| **B (recommended for now)** | Accept FR-3.1/3.2 as proxy anchors and record the NC-05/D-024 provenance explicitly in the Phase 4 `traceability.md` (external-provenance column). Cheaper; defensible because TJ-021's normative text is self-contained. |

**User decision:** [x] **A** (2026-09-27) — FR-3.3 added to `requirements/requirements.md` §3 and prepended to TJ-021's Derived-From (see ID-05 Resolution).

## 4. Approval gate & next steps (`Design Review Procedure.md` §4–§5)

- **User approval (2026-09-27):** ID-01…ID-04 approved; ID-02 → **Option A**; ID-05 → **Option A**. All fixes applied and verified (see the Resolution column). Design documents modified: `requirements/requirements.md` (FR-3.3), `README.md` (§4.1 rows + D-025), `contracts/task-job-management.md` (TJ-021, §2, §4, §6), `contracts/frontend-odb-api.md` (D-025 re-points), `architecture.md`, `subcomponents/README.md`, `usecases/UC-001…003`.
- Fixes were applied in priority order (med → low): **ID-01 → ID-02 → ID-03 → ID-04**; each fixed row carries **Status [F] + Resolution** (what changed + verification grep) in this file; ID-05 resolved to [C] with Option A recorded.
- This file will be registered in `process/reviews/README.md` (rounds table + change history + `ID-*` prefix) and committed as one: `docs: design review 2026-09-27 (ID-01…05)`.
- The supporting audit report `process/identifier-dependency-audit.md` remains as a read-only evidence artifact (not indexed as a review round).



