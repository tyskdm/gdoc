# Architecture Decision Records (ADR) — gdoc Server

This folder records the **strategic architectural decisions** underlying
[`../architecture.md`](../architecture.md) (gdoc Server Architecture). A decision
that is not directly derived from an upstream requirement — but whose rationale,
alternatives, and trade-offs are worth preserving — is captured here, **one ADR
per decision**.

These records are **drafts reconstructed from the current architecture document**:
the decisions are already reflected in the design, and the ADRs formalize the
context, the decision, the alternatives considered, and the consequences.

## Conventions

- `NNN` in the file name is a zero-padded sequence number used for stable ordering.
- The **ID** (`ADR-NNN`) is the stable identifier referenced elsewhere.
- **Status** values follow the project ADR convention:
  `Proposed` (under discussion) · `Accepted` (the current design) ·
  `Superseded` (replaced by a newer ADR) · `Deprecated` (no longer in use).

## Index

| ID | Title | Status |
|----|-------|--------|
| [ADR-001](./001-protocol-agnostic-core.md) | Swappable protocol frontend over a shared, protocol-agnostic core | Proposed |
| [ADR-002](./002-request-task-job-model.md) | Three-tier Request / Task / Job execution model | Proposed |
| [ADR-003](./003-threading-and-async-facade.md) | Frontend asyncio + background worker thread + synchronous facade | Proposed |
| [ADR-004](./004-datastore-synchronization.md) | Centralized synchronization over a dumb, synchronous in-memory datastore | Proposed |
| [ADR-005](./005-plugin-object-builders.md) | Plugin-based Object Builders per content type | Proposed |
| [ADR-006](./006-job-sharing-semantics.md) | Job deduplication, priority inheritance, reference-based cancellation | Proposed |
| [ADR-007](./007-priority-scheduling.md) | State-based document priority scheduling | Proposed |
| [ADR-008](./008-per-client-scheduling.md) | Per-client scheduling with a common / client-specific class split | Proposed |
| [ADR-009](./009-configuration-lifecycle.md) | Save-triggered, isolated configuration handling | Proposed |
