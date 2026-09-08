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
