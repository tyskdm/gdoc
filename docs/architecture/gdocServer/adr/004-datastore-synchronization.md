# ADR-004: Centralized synchronization over a dumb, synchronous in-memory datastore

- **ID:** ADR-004
- **Status:** Proposed
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
  guarantee.
