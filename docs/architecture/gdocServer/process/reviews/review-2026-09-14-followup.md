# Design Review — 2026-09-14 (Round 2: follow-up — propagation of D-014…D-018)

> **Provenance:** Migrated verbatim (2026-09-26) from `process/design_review_record.md` (original §8; internal `§8.x` numbering retained).
> **Companion:** `review-2026-09-14.md` (Round 1 — the decisions settled in its §5).
> **Status legend:** [F] = Fixed · [P] = Pending fix · [?] = Needs user decision (shared legend: `README.md` in this folder)

---

## 8. Follow-up Review (2026-09-14) — Propagation of D-014…D-018 into the supporting docs

> **Scope:** A second pass that checks whether the **already-confirmed** decisions (D-014…D-018) and the
> Phase 1a/1b contracts are consistently reflected in the **supporting** documents — `architecture.md`,
> the Phase 0 Glossary (`subcomponents/README.md` §6), and the Phase 2 procedure (`README.md`).
> The decisions themselves are settled in §5; this section tracks their **propagation** into the
> overview / glossary / phase-procedure documents.
> **Verdict key:** ✅ = valid finding · ⚠️ = partially valid · **Status:** [F] fixed · [P] pending fix · [?] needs decision.

### 8.1 `architecture.md` vs D-014…D-018

| ID | Finding | Location | Verdict | Status | Recommendation |
| --- | --- | --- | --- | --- | --- |
| FU-01 | **System Task (D-014) not reflected** — Task is described only as the 1:1 target of a client Request. | architecture.md L72–74, L262, L265 | ✅ valid | [F] | State that the ODB may **also** generate a **System Task** when a document enters State 2/3 (D-014 / TJ-021); it is distinct from a client Request and **not** frontend-cancellable. |
| FU-02 | **Scheduling boundary (ADR-008 / TJ-010):** L223 "Priority adjustment is performed while processing item 1" reads as if the Frontend adjusts Task/Job priority. | architecture.md L223 | ⚠️ partial | [F] | L225 already states the correct two-domain boundary (ADR-007/008). Tighten L223 so item-1 processing = **Frontend Request ordering only**; ODB re-derives shared-work priority itself. |
| FU-03 | **Terminology:** "task ticket" / "job ticket"; a ticket is a request/Task handle, not a Job attribute (API = `Submission{kind:ticket}`). | architecture.md L51–52 | ✅ valid (minor) | [F] | Reword to "a ticket (request handle / `Submission{kind:ticket}`)"; drop "job ticket". |
| FU-04 | **Diagnostics push (D-015) not tied in** — only "notifications" are described. | architecture.md L55, L102 | ✅ valid (minor) | [F] | Note diagnostics reach the client as a server→client **event push** (D-015 `DiagnosticsEvent`), not only client pull. |
| FU-05 | **"File Deletion" absent** from the scenario list; D-016 (Datastore cleanup + Job/System-Task cancel) should be a Phase 2 UC target. | architecture.md L168–194 | ✅ valid | [F] | Add "File Deletion" under *Document Synchronization & Updates*; ensure a Phase 2 UC covers it (D-016). |

### 8.2 Phase 0 Glossary (`subcomponents/README.md`) vs Phase 1b

| ID | Finding | Location | Verdict | Status | Recommendation |
| --- | --- | --- | --- | --- | --- |
| FU-06 | **Task definition** "It is the 1:1 target of a Request" is now incomplete — D-014 / TJ-021 adds System Tasks with no Request. | subcomponents/README.md L188 | ✅ valid | [F] | Update: a Task is created by a client Request (1:1) **or** by an ODB State-2/3 transition (System Task, D-014 / TJ-021). Request def (L187) stays true: each Request → exactly one Task. |
| FU-07 | **State 2 definition drift:** Glossary "open in the editor"; TJ-021 / D-014 "references of an open file"; **ADR-007 (authoritative): "Open in the editor (and the documents it references)."** | subcomponents/README.md L191; TJ-021 L214; D-014; ADR-007 L23 | ✅ valid — **important** | [F] | Unify all to **ADR-007**: State 2 = the open file **and** the documents it references (reference closure, depth-ordered). Fixes the Glossary, TJ-021 / D-014 wording, and pins the System-Task trigger + State-2 UC trigger. |

### 8.3 Phase 2 procedure — "all 4 components" rule vs C3 encapsulation

| ID | Finding | Location | Verdict | Status | Recommendation |
| --- | --- | --- | --- | --- | --- |
| FU-08 | Phase 2 step 3 "drop a requirement on all 4 components per actor (leave none empty)" can be misread to force **C3 (Datastore, internal per ADR-004)** into actor-facing behavior. | README.md L333–334 | ⚠️ partial (mild) | [F] | Add caveat: for C3, express requirements as **internal data-model / single-writer invariants**, not actor-facing behavior (aligns with Phase 3, README L355). |

### 8.4 Decision needed

- **FU-07 (State 2):** confirm the exact meaning so the System-Task trigger (TJ-021) and the State-2 use-case trigger are unambiguous.
  - [x] **A (recommended):** State 2 = the open file **and** the documents it references (ADR-007 wording)
  - [ ] B: State 2 = the open file only
  - [ ] Other: _______

### 8.5 Summary (follow-up review)

| Category | Count | Valid | Partially valid | Needs decision |
| --- | --- | --- | --- | --- |
| `architecture.md` propagation (§8.1) | 5 | 4 | 1 | 0 |
| Glossary consistency (§8.2) | 2 | 2 | 0 | 0 |
| Phase 2 rule (§8.3) | 1 | 0 | 1 | 0 |
| **Total** | **8** | **6** | **2** | **0** |

**Assessment:** the review is **substantively sound** — all 8 points trace to real cross-document gaps introduced by the newly-confirmed D-014…D-018. The one item needing a decision is **FU-07 (State 2)**, the highest-value fix: it removes a genuine semantic ambiguity that directly drives the System-Task trigger (TJ-021) and the Phase 2 State-2 use-case triggers. FU-01/03/05/06/08 are propagation/clarification edits aligned to already-confirmed decisions; FU-02/04 are minor wording tightening.

**Recommended order before Phase 2:** (1) confirm FU-07 → align Glossary + TJ-021 + architecture.md State 2; (2) FU-01 + FU-06 (System Task in architecture.md + Glossary); (3) FU-05 (File Deletion scenario + UC); (4) FU-03 / FU-04 (terminology / diagnostics); (5) FU-02 / FU-08 (wording caveat).

**Resolution (2026-09-14):** all 8 items **fixed** ([F]). FU-07 resolved to **A** (State 2 = the open file **and** the documents it references, per ADR-007) and unified across the glossary (L191), TJ-021, D-014 (README §7), and NC-05. **Gate cleared — Phase 2 (use-case analysis) may begin.**

---
