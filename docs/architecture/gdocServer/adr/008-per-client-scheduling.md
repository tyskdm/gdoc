# ADR-008: Per-client scheduling with a common / client-specific class split

- **ID:** ADR-008
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

There is one LSP client, but there may be **multiple object-server clients**
(see ADR-001), and each client has a different notion of "what the user is
focused on" (open buffers, active requests). At the same time, much of the
scheduling logic (how priority is computed, how cancellation propagates) is
common to all clients. The architecture states that "task management is divided
into parts that differ by client type and parts that are common to all clients.
The common part is priority management," implemented as "an abstract class
implementing only this common part and concrete classes implementing the parts
that differ by client type."

## Decision

- Task scheduling is managed **per client**: each client's view of open
  documents, active requests, and focus is tracked independently.
- The **common part** (priority management: how priorities are computed,
  inherited, and rescheduled) is factored into an **abstract base class**.
- The **client-specific parts** (how a client reports open/closed documents,
  what constitutes a request, how cancellation is signaled) are implemented in
  **concrete subclasses** — one per client type (LSP client, object-server
  client).
- This is a **template-method** style split: the Object Database drives the
  common algorithm; each client subclass supplies the client-specific hooks.

## Alternatives Considered

- A **single global scheduler** that flattens all clients into one priority
  space (loses per-client focus semantics).
- **Fully independent schedulers** per client with no shared priority logic
  (duplicates the priority algorithm and lets clients disagree about ordering).
- A per-client scheduler with the **priority algorithm duplicated** in each
  client module (drifts over time).

## Consequences

### Pros

- **Correct per-client focus**: an object-server client's "active request" does
  not accidentally raise the priority of the LSP client's documents, and vice
  versa.
- One place (the abstract base) defines priority semantics, so all clients
  behave consistently and are easy to audit.
- Adding a new client type (ADR-001) only requires a **new concrete class**,
  not a scheduler rewrite.

### Cons / Trade-off

- A **shared job** (ADR-006) is still a global resource, so per-client
  priorities must be reconciled when multiple clients' tasks compete for the
  same job — the "highest priority wins" rule must be well defined across
  clients.
- The **common vs. client-specific boundary** can be ambiguous (e.g., is "a
  document is open" a client concern or a global concern?), requiring a clear
  contract.
- Template-method designs can become hard to follow when a concrete class
  overrides many hooks; the set of hooks must be kept minimal and well
  documented.
