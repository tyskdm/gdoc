# Design Change Record — 2026-09-27 — De-specification & boundary correction (NC-05 guarantee + ODB-internal invariant rails)

> - **Position:** `docs/architecture/gdocServer/process/changes/change-2026-09-27-despec-boundary-correction.md`
> - **Status:** **[O] Open — approved, applied, verified; pending the §7 single commit.** Re-scoped from the **CANCELLED** 2026-09-26 record (see its banner). Items **(a) purpose**, **(b) 3-tier boundary**, **(c) `task-job-management.md` → ②-level** confirmed in the 2026-09-27 session; **Q-A / Q-B / Q-C (§4) resolved** — **Q-A (a)**, **Q-B (a)–(f)** (no-state-mixing **dropped**), **Q-C B**. The design set is **applied** (§5) and **§6 verification is complete — V1–V7 all PASS** (§6.1). **D-024** is **logged** in `../../README.md` §7. Remaining step: **single commit** (§7).
> - **Date:** 2026-09-27 · **Author:** assistant; framing per user session 2026-09-27 (a/b/c confirmed).
> - **Supersedes:** `change-2026-09-26-system-task-package-unit.md` — **CANCELLED 2026-09-27** (retained for traceability; do not apply; do not log D-024 from it).
> - **Scope (smaller than the cancelled record):** `../../README.md` §7 · `../../contracts/task-job-management.md` (core) · `../../contracts/frontend-odb-api.md` (minor) · `../../adr/007-priority-scheduling.md` (note) · `../../architecture.md` · `../../subcomponents/README.md` · `../../usecases/UC-001…003` (high-level).
> - **Decision to be logged:** **D-024** in `../../README.md` §7 — *reframes **D-014** from a **mechanism** (System Task) to a **guarantee (NC-05) + ODB-internal invariant rails (②)**; the **mechanism (③) is delegated to ODB-internal** and no longer fixed by the design documents. **Logged** in `../../README.md` §7 (D-024 row, 2026-09-27, ✅ user-approved).
> - **⚠️ ID note:** D-022/D-023 already exist (`../../README.md` §7, 2026-09-26); the next free ID is **D-024** — the **same ID** the cancelled record intended, now **re-scoped** (de-spec, not redesign).

*Status legend (shared with `../reviews/README.md`):* [O] Open · [F] Fixed · [C] Confirmed · [D] Deferred · [R] Resolved · [P] Pending fix · [?] Needs user decision.

## 1. Background & Purpose (re-framed)

The **2026-09-26** record proposed **redefining the System Task** — from a *per-file* (State 2) unit to a **per-package** resident waiter — and fixed that *form* in the design documents. In the 2026-09-27 session the framing was corrected:

- **Separation principle.** The C1–C2 contract (C1 = Frontend, C2 = ODB) fixes **guarantees** and **mechanism-agnostic invariant rails**. It does **not** fix the *form* of the ODB's background work — task shape, count, granularity, priority numerics, standing-waiter, attach/detach are **ODB-internal (③)**.
- **NC-05 is a guarantee, not a mechanism.** "A **built state is available**" (for the states the Frontend may rely on) is a **guarantee**. *How* the ODB holds it (a System Task, a package Task, a client Task, …) is **not** part of the guarantee. The 2026-09-26 record treated the mechanism (System Task shape) as if it were contract; it is not.
- **The unit of change is the boundary, not the task.** D-024 therefore **removes over-specification and corrects the boundary** — it does **not** commit to per-file *or* per-package, and does **not** fix priority numerics.

> **Deliberately NOT changed:** ADR-007's State 1/2/3 *definitions* (scope) and its priority **ordering** principle; the ODB's ownership of package membership (**INV-06**) and of Job mechanics (dedup **TJ-005** / dispatch **TJ-012** / commit **TJ-008**); the C1–C2 state notifications. This is a **boundary re-scope** (a D-014 refinement), **not** an ADR change and **not** a new task model.

## 2. The 3-tier boundary (core of this record)

| Tier | What it is | Concrete examples | Status in the design documents |
| --- | ---------- | ----------------- | ------------------------------ |
| **① C1–C2 guarantee** | What the ODB **guarantees to the Frontend**; the *contract* level | **NC-05** — a needed State 2 (open + its references, ADR-007) / State 3 (package members) background build is **not dropped / available** to the Frontend; State 1 = the client-requested operation (carried by the client Task). ADR-007 **State 1/2/3 definitions** (scope). ⚠ **Exact scope is the open item (Q-A):** the *confirmed* NC-05 text (review-2026-09-14) is a **waiter/cancellation** guarantee (a needed build is **not immediately cancelled for an empty waiter set**); the broader "available / fresh / held" reading is a **redefinition** that Q-A must sign off (with freshness / failure / in-progress defined). | **STAYS as a guarantee** — exact scope **pending Q-A**. |
| **② ODB-internal invariant rails** | **Mechanism-agnostic** properties the ODB **must uphold** to realize ① (a "shall" the implementation cannot violate) | (a) a required **in-flight Job (Queued/Running) is kept alive by ≥1 waiter** — its lifetime is set by its waiter set, **not** by any built state it later produces (**TJ-007**); (b) a Job with **0 waiters is cancelled** (ref-count, centralized in the ODB, **TJ-007**); (c) **dedup** of identical work (**TJ-005**); (d) **atomic commit of a Job result on success only** — nothing committed on cancel (**TJ-008**); (e) **priority ordering** monotonic with state (highest state = highest priority, ADR-007); (f) the **ODB-owned background work is not Frontend-targetable** — the Frontend cancels **only its own Task** (TJ-007 / D-012); this scope is limited to ODB-owned background work, not a client's own Task (D-014). *(Dropped: a proposed "no state-mixing within one unit of work (ADR-007)" — **no such invariant exists in the confirmed set** and ADR-007 is priority-only; re-raised in **Q-B** only if reinstated with a real source decision.)* | **STAYS** — as *rails* (guidance), not as a specific mechanism. |
| **③ ODB-internal mechanism** | The **concrete form** of the background work — an ODB design/implementation choice | task **shape** (System Task vs client Task vs package Task), **count**, **granularity** (per-file vs per-package vs …), **standing-waiter**, **attach/detach**, **priority numerics** (weights/tiers in the queue). | **RETRACTED** — no longer fixed by the design documents; delegated to ODB-internal design. |

**Consequences (what changes vs the 2026-09-26 record):**

- **TJ-021** stops being "System Task lifecycle" (③) and becomes the **② rail** — "the ODB maintains background work so the needed build is **not dropped** (NC-05, scope per Q-A); the **in-flight Job is kept alive by its waiter set** and **cancelled at 0 waiters**; **atomic commit on success only**" — with the **mechanism (shape, granularity, priority numerics, worker identity, lifecycle triggers) explicitly delegated to ③**. The proposed "no state-mixing" rail is **dropped** (no source decision) and re-raised in Q-B.
- **Per-file vs per-package** is **③** — *not* a boundary decision. The design documents no longer pick one.
- **Priority numerics** are **③**; ADR-007's **ordering** principle stays **①/②**.
- **Q7** (attach/detach) and **Q8** (State-2 defer) from the cancelled record are **③** — not boundary decisions.

## 3. Goal — what the design documents will now say (re-scoped target)

After this change, the design set states, at the boundary level, only:

> *"The ODB maintains background work so that a needed State 2/3 build is **not dropped** (available to the Frontend — **NC-05**, exact scope per **Q-A**). It upholds ODB-internal invariant rails — a required **in-flight Job is kept alive by its waiter set** and **cancelled at 0 waiters** (TJ-007); **dedup** (TJ-005); **atomic commit on success only** (TJ-008); **priority ordering** by state (ADR-007); the ODB-owned background work is **not Frontend-targetable** (the Frontend cancels only its own Task — TJ-007/D-012). The **mechanism** (task shape, granularity, priority **numerics**, worker identity, lifecycle triggers) is **ODB-internal** and is **not** fixed by the design documents."*

That sentence is the **target invariant** for every file in §5. No file may commit to per-file *or* per-package, a task count, a `s-*` shape, or priority numerics.

## 4. Findings & Confirmation Items (re-scoped)

The cancelled record's **Q1…Q12** were framed around the *mechanism*; they are **superseded** by the three boundary questions below. (a/b/c are the *framing* already confirmed; Q-A/Q-B/Q-C are the *details* to sign off before application.)

| # | Question | Options / recommendation | Status |
| - | -------- | ------------------------ | ------ |
| **Q-A (gate — NC-05 scope)** | **NC-05 guarantee scope (①):** the *confirmed* NC-05 (review-2026-09-14) is a **waiter/cancellation** guarantee — a needed State 2/3 background build is **not immediately cancelled for an empty waiter set**. The draft had *extended* it to "a built state is **available / held / fresh**". **Choose:** **(a)** keep NC-05 at its **original** waiter/cancel scope (the ② rails TJ-007/008 already carry cancel + commit); **or** **(b)** adopt a **new** "state-availability" guarantee — then define its **freshness** (TJ-018 generation scope), **failure** (what the Frontend sees if the build fails/cancels), and **in-progress** semantics (what "available" means before commit). | **Default: (a)** (the confirmed text). If the user wants **(b)** (the stronger availability guarantee), the three semantics above must be **defined first** — until then it is **not** treated as confirmed | ✅ **Resolved — (a)** chosen (original waiter/cancel scope; ② rails TJ-007/008 carry cancel + commit). Reflected in TJ-021. |
| **Q-B (gate — ② rails)** | **Invariant rail list (②):** confirm the **corrected** mechanism-agnostic rails — (a) a required **in-flight Job is kept alive by ≥1 waiter**; (b) **0 waiters ⇒ cancel** (TJ-007); (c) **dedup** (TJ-005); (d) **atomic commit on success only** (**TJ-008**); (e) **priority ordering** by state (ADR-007); (f) the **ODB-owned background work is not Frontend-targetable** (Frontend cancels only its own Task — TJ-007/D-012). **And decide the dropped rail:** reinstate "**no state-mixing**" **only** with a real source decision + a defined "unit of work" (it is **not** in ADR-007 today); otherwise leave it **dropped**. | yes to (a)–(f) as corrected; **no-state-mixing: dropped by default** unless the user provides a basis | ✅ **Resolved — (a)–(f)** confirmed; **no-state-mixing dropped**. Reflected in TJ-021. |
| **Q-C (low-stakes — ③ wording)** | **How much of ③ to leave in the docs:** **A** — omit ③ references entirely (docs say only "mechanism is ODB-internal, not fixed here"); **B** — keep a one-line *"may exist"* note ("the ODB *may* realize this via an internal background mechanism; the concrete form is not fixed"). This is a **description-policy** choice, **not** a substantive design decision — resolve **after** Q-A/Q-B. | **B (recommended)** — a single neutral line, no shape/granularity/numerics | ✅ **Resolved — B** (one-line “may exist” note). Reflected in TJ-021. |

**Disposition of the superseded Q1…Q12 (cancelled record §4):** Q1 (ID = D-024) → **kept** (same ID, re-scoped). Q2 (rel. to D-014) → **reframed** ("reframes D-014: mechanism → guarantee + rails"). Q3/Q4/Q5/Q6 (record-location & trade-off placement) → **relocated** into Q-B/Q-C. **Q7 (attach/detach) & Q8 (State-2 defer) → ③ (ODB-internal)**, no longer boundary decisions. Q9/Q10/Q11/Q12 (NC-06 producers, shutdown, dispatch-skip, UC-004…011) → **③ or already covered by ② rail (b)**; no design-doc change required beyond the ②/③ boundary.

## 5. Per-file plan — *applied on approval (2026-09-27)* (results in §6.1)

| File | Re-scoped change (to ①/② only) |
| --- | ------------------------------ |
| **§5.1** `../../README.md` §7 | Add **D-024** (draft row below) *after* D-023. Reframes D-014: mechanism → guarantee (NC-05) + ② rails; **mechanism (③) delegated to ODB-internal**. |
| **§5.2** `../../contracts/task-job-management.md` *(core)* | **TJ-021** → **②-level rail** (drop "System Task lifecycle", `s-*`, one-per-state *mechanism*, and the close/deleted/config triggers); keep the **rails** (in-flight Job kept alive by ≥1 waiter; 0 waiters ⇒ cancel TJ-007; atomic commit TJ-008; ODB-owned / not Frontend-targetable — Frontend cancels own Task) and add one line: *"the concrete mechanism (task shape, granularity, priority numerics, worker identity, lifecycle triggers) is **ODB-internal (③)** — not fixed here."* **TJ-001** extended-trigger note: "the **System Task**" → "ODB-internal background work (mechanism ③)". **§4 index** + **§5.3** rows: D-014 paired with D-024 (de-spec). **Rule count stays 21** (reword, don't add/remove). See **§5.7** for the explicit D-014 element disposition. |
| **§5.3** `../../contracts/frontend-odb-api.md` *(minor)* | **Near-zero.** State notifications unchanged. Where the System Task is cited (NC-06 L287; `system_cancelled` L298), re-scope to "ODB-internal background work (mechanism ③)"; keep NC-06 *semantics* (request-less `DiagnosticsEvent`) as a **guarantee**, not a mechanism. **No API operation changes.** |
| **§5.4** `../../adr/007-priority-scheduling.md` *(note)* | Add a scope note: ADR-007 fixes the priority **ordering** (highest state = highest priority) and the State 1/2/3 **definitions**; the **numeric encoding** (weights/tiers) is **ODB-internal (③)**. (ADR-008 "two priority domains" stays as-is.) |
| **§5.5** `../../architecture.md` + `../../subcomponents/README.md` *(high-level)* | Replace "per-document / State-2 System Task" language with "the ODB maintains background work per **NC-05**; the **mechanism is ODB-internal**." Keep the **Task** glossary / **INV-06** single-owner. |
| **§5.6** `../../usecases/UC-001_OpenWorkspace.md`, `UC-002_OpenText.md`, `UC-003_EditText.md` *(high-level)* | Replace "per-document / State-2 System Task" language with the NC-05 guarantee + ②-rail framing; **UC-002** (NC-06 request-less push) names the **guarantee** (needed build not dropped), not the mechanism. **UC-004…011** — **not yet drafted** (README §5 ⬜); the one-line impact note is recorded **here in §5.8** and applied into each UC file **when it is drafted** (per README §3.2); no rewrite. |

**Not changed:** `adr/README.md` risk register (unless Q-B adds a row — recommended: no), other `contracts/`, Phase 0/1a/1b deliverables not cited above.

### §5.7 — D-014 / TJ-021 element-by-element disposition (explicit, per review)

D-024 **supersedes the mechanism half** of the user-approved **D-014**. Per element, whether it is **maintained** (kept as a ② rail), **replaced** (mechanism → ③), or **retracted**:

| D-014 / TJ-021 element | Current text | D-024 disposition |
| --- | --- | --- |
| (a) distinct `s-*` ID namespace | TJ-021(a) | **Retracted to ③** — worker identity (ID shape/namespace) is not fixed |
| (b) participates in the Job waiter set + priority inheritance | TJ-021(b) | **Maintained** as ② rails (a)/(e) — kept alive by the waiter set; ordered by state |
| (c) cancelled when the document leaves its state (`close`/`deleted`/config change) | TJ-021(c) | **Retracted to ③** — lifecycle / exit triggers not fixed *(the element the original draft left unclassified; now explicit)* |
| (d) **not** Frontend-cancellable (`E_NOT_FOUND`) | TJ-021(d) | **Maintained** as ② rail (f) — ODB-owned, not Frontend-targetable (Frontend cancels only its own Task — TJ-007/D-012) |
| (e) waiter-set decrement on cancellation (ref-count) | TJ-021(e) | **Maintained** as ② rails (a)/(b) — 0-waiters cancel, centralized in the ODB (TJ-007) |
| NC-05 value (needed build not dropped) | review-2026-09-14 | **Maintained** — exact scope confirmed in **Q-A** |

Because this redefines part of a **user-approved** decision (D-014), the **Q-A/Q-B** sign-off is required (README §4.5). The **ADR-007** note (§5.4) is **clarification-only** (no new invariant) per README §2/§3.2.

### §5.8 — UC impact note (README §3.2 dependency re-check; location recorded here)

- **UC-001 / UC-002 / UC-003** (existing): the only user-visible change is that a State-2/3 build is no longer described as a "System Task"; the behavior the UCs rely on (the build runs, the result is committed, the Frontend cannot cancel it directly) is **unchanged**. If any UC file names "System Task", reword to "ODB background build".
- **UC-004…011** (not yet drafted): when drafted, each must state **only the guarantee** (a needed State 2/3 build is available and committed) and must **not** name the worker or its ID/lifecycle (mechanism ③).

> **§5.1 — D-024 draft row (apply on approval; paste verbatim on application):**
>
> `| D-024 | 2026-09-27 | **De-specification / boundary correction (NC-05).** Reframes D-014 from a **mechanism** (per-document **System Task** with an `s-*` namespace) to a **guarantee + invariant rails**: (1) the ODB guarantees a needed State 2 (open + its references, ADR-007) / State 3 (package members) background build is **not dropped / available** — **NC-05** (exact scope per **Q-A**); (2) ODB-internal **invariant rails** the mechanism must uphold — a required **in-flight Job is kept alive by its waiter set** and **cancelled at 0 waiters** (TJ-007); **dedup** (TJ-005); **atomic commit on success only** (**TJ-008**); **priority ordering** by state (ADR-007); the ODB-owned background work is **not Frontend-targetable** (Frontend cancels only its own Task — TJ-007/D-012). (3) The **mechanism** — task shape, count, granularity (per-file vs per-package), standing-waiter, attach/detach, **priority numerics**, **worker identity & lifecycle triggers** — is **ODB-internal** and **no longer fixed by the design documents**. **Supersedes the *mechanism* elements of D-014 (worker identity, lifecycle triggers) while maintaining its guarantee + rails** (element table in §5.7). | The 2026-09-26 attempt (cancelled) fixed the *form* of background work (per-package System Task) in the design set; the form is an ODB-internal choice, not a C1–C2 boundary concern. Removing over-specification keeps the contract (NC-05 guarantee + ② rails) stable and lets the ODB evolve the mechanism without design-doc churn. | ⬜ (user approval) |`

## 6. Verification — *executed 2026-09-27, post-application (results in §6.1)*

*(Commands from `docs/architecture/gdocServer/`.)*

| # | Check | Command / method | Expected |
| - | ----- | ---------------- | -------- |
| V1 | No **③ mechanism** fixed in the design set | `grep -rni 'per-package\|per-file\|one per [Pp]ackage\|s-\*\|priority numerics' usecases contracts architecture.md subcomponents` | 0 *normative* hits (only the explicit "ODB-internal (③), not fixed here" notes) |
| V2 | **NC-05 guarantee (①)** intact | `grep -rn 'NC-05' README.md contracts usecases architecture.md subcomponents` | present, stated as a **guarantee** (built state available), not a mechanism |
| V3 | **② invariant rails** present, mechanism-agnostic; **TJ-008** atomic-commit rail present; **no** "state-mixing" rail | `grep -rn 'waiter set\|0 waiters\|TJ-007\|TJ-008\|priority ordering' contracts/task-job-management.md architecture.md` | rails present (TJ-007/008); **no** "state-mixing"; no task *shape*/granularity fixed |
| V4 | **D-024** = de-spec/boundary (not a mechanism); **D-022/D-023** untouched | read the D-024 row; `grep -c 'D-022\|D-023' README.md` | D-024 = guarantee + rails + ③-delegated; D-022/D-023 count unchanged |
| V5 | **Rule count** unchanged (TJ-001…TJ-021) | `grep -cE '^\| TJ-0' contracts/task-job-management.md` and `grep -cE '^\*\*\[TJ-0' contracts/task-job-management.md` | **42** index rows + **21** inline rules — unchanged (TJ-021 **reworded, not added/removed**) |
| V6 | **INV-06** single owner intact | read the INV-06 row in `subcomponents/README.md` | ODB owns membership; background work references it only |
| V7 | **frontend-odb** state notifications unchanged | diff `contracts/frontend-odb-api.md` | only the re-scope note (NC-06 / `system_cancelled`); no API operation change |

> **V5 pattern note (regression fixed):** the earlier draft's `^ | TJ-0` (space before the pipe) matched **0** lines; the correct anchor is `^\| TJ-0` (pipe at column 0) → **42**. This is the *same* bug the 2026-09-26 record §8 item 8 already corrected (`literal ^| anchor → 42`); it is re-fixed here.

### §6.1 — Verification results (executed 2026-09-27, post-application)

Run from `docs/architecture/gdocServer/` after the §5 application (all in-scope files modified; **D-024** logged in `../../README.md` §7). **All 7 checks PASS.**

| # | Result | Actual evidence (observed) |
| - | ------ | -------------------------- |
| V1 | ✅ PASS | 3 hits, all benign: `contracts/task-job-management.md:223` (TJ-021, explicit “ODB-internal (③), not fixed here”); `usecases/UC-002_OpenText.md:372` (“`s-*` … retracted to ODB-internal by D-024”); `contracts/task-job-management.md:28` (false positive — `ODB-*/LSP-*/DS-*/BLD-*` requirement-ID wildcards + “deferred to detailed design”). **0 normative** per-file / per-package / `s-*`-namespace / priority-numerics fixes. |
| V2 | ✅ PASS | NC-05 present and stated as a **guarantee** (“not dropped”): D-014/D-024 (`README.md:257/267`), TJ-021 (`contracts/task-job-management.md:223/340`), `usecases/UC-001_OpenWorkspace.md:269/410`, `architecture.md:73/266`, `subcomponents/README.md:200`; mechanism delegated to ③. |
| V3 | ✅ PASS | ② rails present — TJ-007 ref-count (`contracts/task-job-management.md:109`), TJ-008 atomic commit (`:115`), waiter-set / 0-waiters⇒cancel (`:92/93`); **no** “state-mixing” rail in contracts/architecture (recorded only as **dropped** in the D-024 log status); no task shape/granularity fixed. |
| V4 | ✅ PASS | D-024 (`README.md:267`) = guarantee + rails + ③-delegated; D-022 (`:265`) & D-023 (`:266`) untouched (grep count = 2). |
| V5 | ✅ PASS | `^\| TJ-0` index rows = **42**; `^\*\*\[TJ-0` inline rules = **21** — unchanged (TJ-021 reworded, not added/removed). |
| V6 | ✅ PASS | INV-06 (`subcomponents/README.md:87`) owner = **C2 ODB** (Project/Packages scoping) — single-owner intact. |
| V7 | ✅ PASS | `contracts/frontend-odb-api.md` diff = **2 lines only**: NC-06 note (L287) and `system_cancelled` note (L298) re-scoped “System Task” → “ODB-internal background … mechanism ③”. The `request_id` Option-A rule and the `reason` token string `“system_cancelled”` are **unchanged**; **no API operation change**. |

**Approval reflection (confirmed by the application):** **Q-A (a)** — NC-05 kept at the original waiter/cancellation-prevention scope (TJ-021: “not immediately cancelled for an empty waiter set — the ODB supplies the waiters itself”). **Q-B (a)–(f)** — rails confirmed; **no-state-mixing dropped**. **Q-C B** — TJ-021 ends with the single “the ODB *may* realize this via internal background tasks … not fixed by this specification” note.

**Minor observation (does not fail V1–V7):** `README.md:259` **D-016** rationale still reads “**System Task** lifecycle”. It is a **decision-log historical row** (2026-09-14, payload-discriminator decision) in `README.md` §7, **outside** the §5.1 scope (which only adds D-024), so it does not affect the normative-contract checks. Optional follow-up (not required): reword to “ODB-internal background-work lifecycle”.

## 7. Status & Commit

- **Commit convention** (mirrors `../reviews/Design Review Procedure.md` §5): **one commit**, made only after Q-A/Q-B/Q-C approval + applied + verified (§6):
  `docs: design change 2026-09-27 (D-024: de-spec / boundary correction — NC-05 guarantee + ② invariant rails; ③ mechanism retracted to ODB-internal)` — this record (finalized §5/§6) + the design-document re-scopes + the D-024 row in `../../README.md` §7 + the CANCELLED banner on the 2026-09-26 record.
- **Trace:** `git log --grep 'D-024'` · `git log --grep 'boundary'`.
- **Status log:** [O] Open (2026-09-27, **revised for the 2026-09-27 review**) — re-scoped from the **CANCELLED** 2026-09-26 record; a/b/c confirmed; **revised** to fold in the review: NC-05 scope split into **Q-A** (confirm the original waiter/cancel text vs. adopt a *defined* availability guarantee); ② rails corrected (**in-flight Job** kept alive by its waiter set; **TJ-008** atomic commit; **"no state-mixing" dropped**; **Frontend-cancel scoped** to ODB-owned work); **D-014 element disposition** made explicit (§5.7); **UC-004…011 impact-note location** set (§5.8); **V3/V5** grep bugs fixed. **Q-A / Q-B / Q-C resolved** (Q-A (a) · Q-B (a)–(f), no-state-mixing dropped · Q-C B); **§5 applied** to all in-scope files; **§6 executed — V1–V7 all PASS (§6.1)**; **D-024 logged** in `../../README.md` §7. [O] Open — remaining step: **§7 single commit** (awaiting user go-ahead).

---

*This is a design **change** record (distinct from a design **review**). Reviews (`../reviews/`) record findings on already-written documents; this records a deliberate design change — its (re-framed) purpose, the 3-tier boundary, the re-scoped confirmation items, the per-file plan, the applied edits, and the verification evidence. It supersedes the CANCELLED `change-2026-09-26-system-task-package-unit.md`.*
