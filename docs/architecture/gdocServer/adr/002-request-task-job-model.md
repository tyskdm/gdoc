# ADR-002: Three-tier Request / Task / Job execution model

- **ID:** ADR-002
- **Status:** Accepted
- **Date:** 2026-09-08

## Context / Background

A single LSP interaction (a hover, a rename, a completion) may require a
variable, and often large, amount of background work — parsing the current
file, then the files it references, transitively. The amount of work is not
known until the work begins: the architecture notes that "the referenced
documents required by the request become sequentially apparent during request
processing." The server must stay responsive to the client while this work
proceeds, and the same underlying work is shared across frontends and across
repeated requests.

## Decision

- Introduce **three tiers** of execution:
  - **Request** — one external interaction, owned by a frontend. **A single
    request always corresponds to exactly one task.** This 1:1 invariant is
    held at the **Request ↔ Task** boundary.
  - **Task** — a **protocol-agnostic** unit of orchestration, carrying the
    priority, lifecycle, and cancellation that the Object Database assigns and
    manages for it. A Task decomposes into one or more units of processing
    (Parse / Link / Compile).
  - **Job** — an **atomic** unit of execution (Parse, Link, Compile) dispatched
    to an Object Builder.
- **Frontends only create and observe Requests/Tasks**; they never schedule
  Jobs directly.

> **Subtask vs. Job.** The architecture names a Task's internal processing
> units with two terms: *subtasks* ("a single task can contain multiple
> subtasks," used for "compilation and linking") and *Jobs* ("a Task is
> decomposed into one or more Jobs," dispatched to Builders and deduplicated
> across Tasks — see ADR-006). The coherent reading: a **subtask** is the
> *task-local* management unit, and a **Job** is the *(potentially shared)*
> execution unit it requests from a Builder. Because deduplication/sharing
> happens at the **Job** level — *below* the Task level — it does **not** break
> the "one request → one task" invariant: two requests still map to two tasks;
> they may simply await the same underlying Job.

## Alternatives Considered

- A two-tier model where requests are dispatched directly to jobs (no Task
  layer), with per-protocol task management.
- A fully async, single-level model in which every LSP message is its own
  coroutine with no shared scheduling.
- A global queue-based producer/consumer model in which clients push work items
  onto a shared queue.

## Consequences

### Pros

- Clean separation: protocol handling (Request) is decoupled from orchestration
  (Task) and execution (Job) — this is what makes the core protocol-agnostic
  (see ADR-001).
- The Task is the natural place to express **priority, cancellation, and client
  ownership**, which a bare Job or a raw LSP message cannot.
- Decomposing a Task into Jobs lets the Builder layer deduplicate and share
  identical work (see ADR-006) and be prioritized independently.

### Cons / Trade-off

- Three abstractions add conceptual and implementation overhead versus a
  two-tier design.
- The Task → Job decomposition must be done **without knowing the full
  dependency set up front** (references are discovered incrementally), so the
  scheduler must support re-scheduling and dynamic Job creation mid-Task.
- "Subtasks vs. independent Tasks" for internal processing is a design boundary
  that must be kept consistent, or else cancellation and priority tracking will
  double-count work.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-002-1 (correctness — cancellation/priority accounting).** The subtask
  (task-local) vs. shared-Job boundary must stay consistent in every code
  path.
  - *Failure mode:* The same unit of work is tracked twice; reference-counted
    cancellation (ADR-006) misfires — a Job is canceled while waiters remain,
    or never canceled (leak) — and priority inheritance double-counts.
  - *Mitigation:* Ownership is fixed: subtasks are task-local management
    units, Jobs are the shared execution units; deduplication happens at the
    Job level only (ADR-006).
  - *Verify:* two tasks awaiting one shared Job: canceling one keeps the Job
    running; canceling the last cancels the Job; no double-counting of
    priority.
- **R-002-2 (correctness — dynamic Job graph).** Task → Job decomposition is
  incremental because references become apparent during execution.
  - *Failure mode:* Mid-Task Job creation/re-scheduling duplicates already
    in-flight work (breaking the ADR-006 single-in-flight invariant), loses a
    dependency, or admits cycles.
  - *Mitigation:* Dynamically created Jobs are registered through the same
    deduplication key (ADR-006) and reconciled with in-flight work.
  - *Verify:* test that incremental reference discovery yields exactly one
    in-flight Job per (file, version, inputs) and preserves dependency order.

The conceptual/implementation overhead of the three abstractions is an
accepted trade-off, not a risk.
