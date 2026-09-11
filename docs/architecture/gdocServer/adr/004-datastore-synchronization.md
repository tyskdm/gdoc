# ADR-004: Centralized synchronization over a dumb, synchronous in-memory datastore

- **ID:** ADR-004
- **Status:** Accepted
- **Date:** 2026-09-08

## Context / Background

The Object Datastore holds all generated gdoc objects and their cross-document
relationships for a Project. It is written to by many concurrent Jobs (through
the Object Database) and read by frontends for fast lookups. The architecture
explicitly describes the Datastore as a "Synchronous Implementation,"
"In-Memory Storage," with "No Internal Concurrency Control … exclusive access
and synchronization are managed externally by the Object Database," and as an
"Encapsulated Component … completely hidden from Frontends … accessible only
via the Object Database."

## Decision

- The Datastore is implemented as a set of **plain, synchronous, in-memory data
  structures** with **no internal locking or thread-safety**.
- **All** concurrency control and exclusive access is **centralized in the
  Object Database** (the single coordinator on its worker thread / event loop).
- The Object Database's **public synchronous methods are lightweight and
  non-blocking**: they submit work (returning a task ticket) or return current
  state and promptly return to the caller; they do **not** block waiting for
  analysis to finish. **Heavy processing (Parse / Link / Compile) is deferred
  to, and executed on, the ODB's dedicated worker thread** (see ADR-003). The
  Datastore therefore only ever sees fast, in-memory operations.
- The Datastore is **fully encapsulated**: no frontend or external component
  may access it directly; every read and write goes through the Object Database.

## Alternatives Considered

- A fine-grained-locked (or lock-free) datastore that is thread-safe on its
  own, letting multiple frontends read concurrently without the ODB.
- A dedicated embedded database engine (e.g., SQLite) providing its own
  concurrency and persistence.
- An actor model in which the datastore is an actor owning all mutations.

## Consequences

### Pros

- A single coordinator gives one **total order of mutations** → simple,
  deterministic consistency; no distributed-lock reasoning.
- The datastore stays simple, low-latency, and easy to reason about (plain
  structures), matching the "fast lookup" requirement.
- Because heavy analysis runs on the ODB worker thread and the public API is
  non-blocking (see ADR-003), the Datastore is never a long-running blocking
  resource; its synchronous, in-memory operations stay low-latency even while
  CPU-intensive Jobs run elsewhere.
- Encapsulation prevents frontends from building ad-hoc assumptions over
  internal structures, keeping the core's data model a single source of truth.

### Cons / Trade-off

- Every read is serialized through the ODB, so read-heavy frontends compete
  with background analysis for the single coordinator; this can become a
  throughput bottleneck under many object-server clients.
- **In-memory only** means no built-in persistence/recovery; project state is
  rebuilt on restart (acceptable for a language server, but a deliberate
  limitation).
- All correctness depends on the ODB being a strict single writer; any future
  path that mutates outside the ODB silently breaks the "no internal locking"
  guarantee. This is reinforced today by a single write-*origin* as well (the LSP
  frontend is the only writer, ADR-001); if that origin constraint is ever
  lifted in favor of multi-client editing, all frontends funnel through this
  one coordinator — which is what this guarantee exists to preserve.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-004-1 (correctness — silent data corruption).** The Datastore has no
  internal locking; all correctness depends on strict single-coordinator
  access.
  - *Failure mode:* Any access path outside the ODB (direct reference, a
    mutation from another thread via a callback) causes data races and silent
    corruption — the hardest failure class to detect. Related: R-001-1
    (invariant by convention).
  - *Mitigation:* Encapsulation: only the ODB touches the Datastore; all
    mutations go through the single coordinator on the worker thread
    (ADR-003).
  - *Verify:* architectural test forbidding Datastore references outside the
    ODB; concurrency regression test that fails if a second thread mutates
    concurrently.
- **R-004-2 (availability — head-of-line blocking).** Public synchronous
  methods must be lightweight and non-blocking.
  - *Failure mode:* A public method that waits for analysis to complete blocks
    the worker thread and stalls every other task; combined with R-003-1 this
    can become a cross-thread deadlock.
  - *Mitigation:* The non-blocking submit/ticket contract in the Decision
    (heavy work is deferred to the worker thread).
  - *Verify:* test that a heavy request returns its ticket without blocking a
    subsequent light request on the same facade.
- **R-004-3 (performance — throughput bottleneck).** All reads are serialized
  through the single coordinator.
  - *Failure mode:* Read-heavy Object Server clients compete with background
    analysis for the coordinator and starve interactive work (R-007-1).
  - *Mitigation:* Reads stay fast in-memory operations; revisit (read cache /
    batching) when the Object Server ships — out of scope today.
  - *Verify:* load test with several concurrent frontends reading during a
    background build.

The in-memory-only (no persistence) limitation is an accepted, deliberate
trade-off.
