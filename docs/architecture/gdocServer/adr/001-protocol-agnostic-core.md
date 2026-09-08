# ADR-001: Swappable protocol frontend over a shared, protocol-agnostic core

- **ID:** ADR-001
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

gdoc Server must serve two different kinds of consumers:

1. An IDE (VSCode) through the Language Server Protocol (LSP 3.17.0).
2. A future **Object Server** that exposes gdoc objects through a direct API
   (e.g., as graph data) for programmatic access.

The architecture already defines backend components (Object Database, Object
Datastore, Object Builders) whose concerns are independent of the transport
protocol, and explicitly states that the Object Server "replaces the gdoc
Language Server component, which is the frontend of the language server" while
"the rest of the configuration is the same as the Language Server." It also
states that "in the current version of gdoc Server, changes to objects can only
be made from the language server."

## Decision

- The gdoc Server is structured with a clean split between a **protocol-specific
  frontend** and a **protocol-agnostic core**.
- The frontend's sole responsibility is to translate protocol messages (LSP)
  into internal **Requests** and to translate core results back into protocol
  notifications. All shared state and orchestration live in the core (Object
  Database + Datastore + Builders).
- The **Object Server is to be realized by adding a second frontend** that talks
  to the same core — i.e., the LSP frontend is *swappable*, and the server is
  not rebuilt.
- Until the Object Server is delivered, the **LSP frontend is the only frontend**
  and the **only path through which gdoc objects can be created or mutated**.

## Alternatives Considered

- A single LSP-only server with no protocol abstraction, and a separate,
  independently-built Object Server with its own parsing/storage (duplicated
  backends).
- A monolithic API server that exposes both LSP and a custom API from one code
  path, sharing internal classes directly.
- A REST/gRPC gateway in front of a core, treating both frontends as "clients"
  of an RPC core.

## Consequences

### Pros

- Adding the Object Server is **additive** (a new frontend), not a rewrite; the
  expensive backend (parse/link/analyze, scheduling, storage) is reused.
- Protocol-specific complexity (LSP lifecycle, capability registration, semantic
  tokens) is isolated, so swapping protocols does not disturb the core.
- Multiple concurrent frontends (one LSP client + N object-server clients) can
  share one consistent object state, with work deduplicated across them (see
  ADR-006).

### Cons / Trade-off

- Every core operation must be designed up front to be protocol-agnostic, which
  constrains how the core can optimize for a single protocol.
- The core interface (the Request model) must be a **superset** of the needs of
  all frontends; if it is designed incompletely, rework is likely when the
  Object Server's needs differ.
- "Changes can only be made from the language server" is a **temporary
  asymmetry**: making the mutation path protocol-agnostic is deferred, so the
  Object Server will initially be read-only, or its writes must be routed
  through a common mutation API.
