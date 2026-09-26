# Design Review Procedure (cross-document)

> **When to run:** at each phase gate — after a phase closes and before the next phase begins — and after any batch of new decisions (D-*) that must propagate into existing documents.
> **Applies to:** the gdocServer design set (`docs/architecture/gdocServer/`); adaptable to other document sets with the same derivation discipline.

## 1. Scope & exclusions

- Review the **completed** documents in the current phase scope; in-flight deliverables are checked for internal consistency only.
- **Do not flag** deferred-by-design items (D-* with a deferral status) or work tracked by the phase plan. List them in the review file's **Excluded** note for auditability — an exclusion is a recorded decision, not an oversight.

## 2. Method (in order)

1. **Decision propagation:** for every D-* confirmed *after* a document was written, verify the decision is reflected in *all* documents that state the affected behavior — body text, scenarios, tables, self-checks, and checklist rows.
2. **`.agents/checklists/Traceability Check Strategy.md`** — the 5 checks (adequacy, semantic coverage, consistency, granularity, verifiability) per document.
3. **Mechanical checks (grep),** at minimum:
   - ID counts in self-checks/charts match reality (e.g. "TJ-001…TJ-021" vs. actual rows; "INV-01…INV-30" vs. the matrix);
   - superseded decisions no longer cited as current (search each superseded D-* in tables);
   - stale "provisional / to be logged / pending" markers for items already settled;
   - orphan IDs — IDs cited in tables/checks without a body definition (search each ID, count hits ≥ 2 and confirm a definition exists).
4. **Record each finding:** stable ID · severity (high/med/low) · location (**file + §/requirement ID** — line numbers are auxiliary only, they rot) · recommendation · status.

## 3. Recording

- **One file per round** in `docs/architecture/gdocServer/process/reviews/`: `review-YYYY-MM-DD.md` (suffix `-followup` for a same-day second pass; `record-YYYY-MM-DD-*.md` for decision/traceability notes).
- **Format:** header (date · scope · method · exclusions) → findings table (`ID | Sev | Finding | Location | Recommendation | Status | Resolution`) → verdict → (if any) decisions needed with A/B options (see `review-2026-09-14.md` §5 for the pattern).
- **Status legend (shared):** [O] Open · [F] Fixed · [C] Confirmed · [D] Deferred · [R] Resolved · [P] Pending fix · [?] Needs user decision. Defined in `process/reviews/README.md`.
- **Register** the new file in `process/reviews/README.md` (rounds table + change history).
- **Decisions are not recorded here.** A finding that escalates into a design decision is logged as `D-NNN` in the set `README.md` §7; the review file references it.

## 4. Fix & verify

- Fix in priority order (high → low); keep the fix minimal and limited to already-confirmed decisions.
- For each fixed finding update its row: **Status [F] + Resolution** (what changed + verification evidence, e.g. the grep command and its result).
- Re-run the mechanical checks of step 2.3 after the fixes; record the evidence in the Resolution cells.

## 5. Commits (two, in order)

1. `docs: record design review YYYY-MM-DD (<PREFIX>-01…NN)` — the review file (+ index / procedure changes); all findings [O].
2. `docs: apply design review YYYY-MM-DD (<PREFIX>-01…NN)` — the document fixes + status/Resolution updates in the review file.

Rationale: the pre-fix state is committed as a fact first; `git log --grep '<PREFIX>-'` then traces each finding from record → fix. Findings IDs in commit messages keep the history greppable.

## 6. Escalation

- A finding that implies a **design change** (not mere propagation) → stop, record it as [?] with A/B options + recommendation in the review file, and log the user's outcome as D-NNN in `README.md` §7 before applying.
