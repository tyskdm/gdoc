# ADR-007: State-based document priority scheduling

- **ID:** ADR-007
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

A workspace can contain many documents, but the user only interacts with a few
at a time. The server must decide what to build first so the document the user
is looking at is correct as soon as possible, while background work (other
documents, transitive references) proceeds without starving interactive work.
The architecture defines three dependency states per document — (1) required by
an active client request, (2) open in the editor, (3) part of a package — and a
reference-depth ordering from the open files.

## Decision

- Every document in the workspace carries **state variables** for the three
  states; a document's effective build priority is derived from the **highest
  state** it is in:
  1. Referenced by an active (non-canceled) client request.
  2. Open in the editor (and the documents it references).
  3. Part of a package (over documents that are in the workspace but belong to
     no package).
- Beyond these, references are built in **reference-depth order from the open
  text**: (a) references of open files, (b) references of those, (c) by
  increasing reference level, and (d) documents that are neither open nor
  referenced are built last.
- Priority is **recomputed on every client interaction** (every time the user
  interacts with the IDE); when a document leaves state 1, its task is
  rescheduled by its state 2/3 priority.
- If multiple requests need a document, it **stays in state 1 until all such
  requests are canceled**.
- Package membership (state 3) is set by configuration and is applied on
  **save**, independent of open-text changes (see ADR-009).

## Alternatives Considered

- A **flat priority queue** keyed only on recency of access (no explicit
  document states).
- Strict **LIFO/FIFO** by request arrival order.
- A **dependency-first topological build** (build all referenced documents to
  completion before responding to anything).

## Consequences

### Pros

- Interactive, user-visible work (state 1) is always prioritized, keeping
  responsiveness even during large background builds.
- Reference-depth ordering means the user's immediate navigation targets are
  correct before the long tail.
- Per-document state is a clean, local way to express priority, making
  re-scheduling on every interaction cheap and predictable.
- Package membership (state 3) gives a deterministic baseline so unrelated
  workspace files never compete with in-package work.

### Cons / Trade-off

- Transitive references are only known **after** building the first-level
  reference, so the "reference-depth order" is inherently incremental — the
  scheduler must support re-ordering as new dependencies appear.
- A document in state 1 for *many* requests is pinned at top priority until all
  are gone, which can delay lower-priority work if a long-lived request is left
  open.
- "All references of an object" requests require completing state-2 builds — a
  large, hard-to-bound amount of work — so the server must decide when to defer
  or cancel these.
- Priority is decided in **two places** (ADR-008): the frontend orders *its*
  requests, and the ODB orders the shared work (these document states). The
  boundary between them — "frontend picks which requests matter, in what order;
  ODB picks which shared work runs first" — is easy to cross by mistake.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-007-1 (availability — starvation).** A document stays in state 1 while
  any non-canceled request references it.
  - *Failure mode:* A long-lived or forgotten request pins a document (and its
    transitive references) at top priority, starving lower-priority work of
    other clients.
  - *Mitigation:* Priority is recomputed on every client interaction; detailed
    design should define a pin bound (age-based demotion or a maximum state-1
    duration).
  - *Verify:* test that a long-lived state-1 request does not block
    lower-priority work beyond the defined bound.
- **R-007-2 (availability — unbounded work).** "All references of an object"
  requests require completing state-2/3 builds — hard-to-bound work.
  - *Failure mode:* CPU/memory exhaustion if the server does not defer or
    cancel such work.
  - *Mitigation:* The server must define a defer/cancel policy for unbounded
    requests (detailed-design input).
  - *Verify:* test that an unbounded request over a large workspace can be
    deferred/canceled and that state remains consistent afterwards.
- **R-007-3 (correctness — two priority domains).** Priority is decided in two
  places: frontends order *their* requests; the ODB orders shared work.
  - *Failure mode:* A crossed boundary (frontend assumes the ODB will
    re-prioritize, or vice versa) silently breaks the responsiveness
    guarantee. See ADR-008.
  - *Mitigation:* The boundary is an explicit contract: the frontend picks
    which requests matter and in what order; the ODB picks which shared work
    runs first.
  - *Verify:* contract tests for representative interactions (open file,
    request, cancel, background build) on both sides of the boundary.

The incremental reference discovery (re-ordering as builds proceed) is an
accepted property, handled under R-002-2.
