# Usecase Analysis Skill (gdocServer Tailored)

> **Tailored from:** `.agents/skills/usecase-analysis/SKILL.md`
> **Project:** gdocServer design-documentation set
> **Applies to:** Phase 2 use-case analysis (`usecases/UC-*.md`)

If an error occurs, terminate the process and return the error information.

## Arguments

/skill:usecase-analysis (input, output, references={references}) --> result

1. input: Filepath - (requires) Markdown file describing the target usecase
2. output: Filepath - (requires) Markdown file for saving analysis results
3. references: Filepath(s) - (optional) Markdown file(s) to refer to for analysis

Reject missing or unknown arguments.

**Required references for gdocServer Phase 2:**

- `../../contracts/task-job-management.md` (TJ-001…TJ-021)
- `../../contracts/frontend-odb-api.md` (API-001…004, Request/Result/Event models)
- `../../subcomponents/README.md` §4 (ownership matrix) + §6 (glossary)
- `../../requirements/requirements.md` (FR/NFR origin)
- `../../README.md` §7 (decisions D-001…D-018)

### gdocServer Phase 2 — How to invoke

In this project the **input** is not a standalone "usecase description file" —
it is the **UC row from `plan.md` §1** (UC-ID, Name, Trigger, FR/NFR)
plus the **relevant LSP event** and **Phase 2 Procedure step** from `../../README.md` §8.

Concrete invocation (example — UC-001 Open Workspace):

```
input:     UC-001 row from plan.md (Trigger: initialize/initialized; FR-1.1, NFR-1.1)
           + LSP 3.17 `initialize` request/response contract
output:    usecases/UC-001_OpenWorkspace.md
references: ../../contracts/task-job-management.md
            ../../contracts/frontend-odb-api.md
            ../../subcomponents/README.md
            ../../requirements/requirements.md
            ../../README.md §7
            usecase_analysis/1. Open Workspace.md  (protocol-level reference)
```

**Rules for output:**
- Write to `../../usecases/UC-NNN_<Name>.md` (flat filename, no subfolders).
- Structure: follow `./template.md` exactly.
- Every UC must produce ≥1 requirement per component (C1/C2/C3/C4).
- If no requirement is derivable for a component, write a one-line justification
  in that component's SCR section (e.g., "C3: No direct impact — read-only query, no Datastore write").

## Steps

- Read all documents specified in {references}.
- Focus on the usecase specified in {input}.
- Perform the following analysis and document the results, including the process, in {output}.
  1. Identify the relevant actors (from `../../subcomponents/README.md` §3: C1–C4)
  2. Create a sequence diagram showing the interactions between actors that implement the use case
  3. List the requirements for messages and activations based on the sequence diagram
  4. List those requirements for **all 4 components** (C1/C2/C3/C4); for C3 (Datastore) express as **internal data-model / single-writer invariants** (ADR-004), not actor-facing behavior
  5. **Cross-reference** each requirement against Phase 1 contracts (TJ-*/API-*) and fill the **Reverse-check table**
  6. **Verify** that no component is left without at least one derived requirement
  7. Ensure all decisions **D-014…D-018** are reflected where applicable
  8. Ensure terminology matches the glossary (`../../subcomponents/README.md` §6)
- Use the template in `./template.md` as the output structure.
- Return "OK" as {result}.