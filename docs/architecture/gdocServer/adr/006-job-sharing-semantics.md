# ADR-006: Job deduplication, priority inheritance, reference-based cancellation

- **ID:** ADR-006
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

Multiple tasks — from the same or from different frontends — frequently need
the same atomic work (e.g., "parse file X"), especially when one request
transitively references a document that another request also needs. Recomputing
it per task wastes CPU and, more importantly, risks inconsistent snapshots if two
parses of the same file interleave. The architecture states that the Builder
manages this as "a single unit of work shared by those Tasks," inherits "the
highest priority among all the Tasks currently requesting it," and is canceled
only "when all associated Tasks have been canceled or removed."

## Decision

- The Builder **deduplicates** concurrent requests for the same job into **one
  shared unit of work**; all requesting tasks await the same result.
- A shared job **inherits the highest priority** of any task currently waiting
  on it (priority inheritance).
- A shared job is **reference-counted for cancellation**: it stays active while
  ≥1 requesting task is alive, and is canceled only when **all** requesting
  tasks have been canceled/removed.

## Alternatives Considered

- **Per-task jobs (no dedup):** simplest, but duplicated CPU and inconsistent
  snapshots under concurrency.
- **Global memoization** keyed on (file, version) with no task ownership: fast,
  but cancellation and priority become hard to attribute.
- A **lock per file:** correct serialization, but blocks lower-priority work
  behind a long low-priority parse.

## Consequences

### Pros

- Eliminates redundant parsing/linking across frontends and tasks → major CPU
  savings and faster cold/hot paths.
- A single in-flight parse per (file, version) guarantees a **consistent object
  snapshot** regardless of how many clients are waiting.
- Priority inheritance prevents a low-priority task from monopolizing a job
  that a high-priority (e.g., client-visible) task also depends on.
- Reference-counted cancellation gives correct lifetime semantics without a
  global scheduler having to track every waiter.

### Cons / Trade-off

- Builders must expose **cooperative cancellation** and be safe to abandon,
  since a job may be canceled mid-run when its last referencing task is removed.
- Priority inheritance can cause **priority inversion** in the reverse
  direction (a low-priority task holds a job that a high-priority task later
  needs); the ODB's re-scheduling (ADR-007) mitigates but does not eliminate
  this.
- Deduplication is only correct if the job key (file + version + relevant
  inputs) precisely captures all inputs; an under-specified key yields stale
  shared results.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-006-1 (correctness — partial state on cancellation).** A shared Job is
  reference-counted and may be canceled mid-run when its last requesting task
  disappears.
  - *Failure mode:* A Builder that has already written partial results leaves
    an inconsistent snapshot in the Datastore.
  - *Mitigation:* Builders are "safe to abandon": results are committed
    atomically on success only — the commit semantics (single swap vs.
    transactional batch) must be fixed in detailed design.
  - *Verify:* test that a mid-run canceled Job leaves the Datastore in its
    pre-Job state; test that a successful Job's results become visible
    atomically.
- **R-006-2 (correctness — dedup-key under-specification).** Deduplication is
  only as correct as the Job key.
  - *Failure mode:* A key that omits an input (file + version + relevant
    inputs) returns *stale* shared results to a different task — a subtle
    correctness bug that is hard to reproduce.
  - *Mitigation:* One key-derivation helper per content type, provided by the
    builder SDK (R-005-2).
  - *Verify:* exhaustive test that differing relevant inputs on the same file
    (content type, dependency state, options) are *not* deduplicated into one
    shared Job.
- **R-006-3 (correctness — reference-count errors).** Job lifetime is
  reference-counted over the requesting tasks.
  - *Failure mode:* Miscounts cancel a Job while waiters remain (lost work) or
    never cancel it (leak); interacts with R-002-1 and ADR-008's cancellation
    translation (R-008-1).
  - *Mitigation:* Reference counting is centralized in the ODB; frontends only
    cancel *their own* tasks.
  - *Verify:* concurrent add/remove of waiters; assert the Job lifecycle
    invariant (active while ≥1 waiter, canceled on the last departure).
- **R-006-4 (availability — priority inversion / starvation).** A low-priority
  task may hold a Job that a high-priority task later needs.
  - *Failure mode:* A client-visible (high-priority) request starves
    indefinitely behind a long low-priority Job.
  - *Mitigation:* ADR-007 re-scheduling mitigates but does not eliminate;
    detailed design must bound it (e.g., cancel-and-re-run at the inherited
    priority, or a timeout).
  - *Verify:* scenario test: a high-priority request for a Job already held by
    a low-priority one completes within a bounded time.
