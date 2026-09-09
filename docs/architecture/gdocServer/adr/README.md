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

| ID | Title | Theme | Status |
|----|-------|-------|--------|
| [ADR-001](./001-protocol-agnostic-core.md) | Swappable protocol frontend over a shared, protocol-agnostic core | Foundation | Proposed |
| [ADR-002](./002-request-task-job-model.md) | Three-tier Request / Task / Job execution model | Execution model | Proposed |
| [ADR-003](./003-threading-and-async-facade.md) | Frontend asyncio + background worker thread + synchronous facade | Runtime | Proposed |
| [ADR-004](./004-datastore-synchronization.md) | Centralized synchronization over a dumb, synchronous in-memory datastore | Data store | Proposed |
| [ADR-005](./005-plugin-object-builders.md) | Plugin-based Object Builders per content type | Building | Proposed |
| [ADR-006](./006-job-sharing-semantics.md) | Job deduplication, priority inheritance, reference-based cancellation | Scheduling (sharing) | Proposed |
| [ADR-007](./007-priority-scheduling.md) | State-based document priority scheduling | Scheduling (order) | Proposed |
| [ADR-008](./008-frontend-odb-scheduling-boundary.md) | Responsibility boundary between frontend Requests and ODB Task/Subtask/Job scheduling | Responsibility boundary | Proposed |
| [ADR-009](./009-configuration-lifecycle.md) | Save-triggered, isolated configuration handling | Configuration | Proposed |

## How the ADRs fit together

The ADRs form a connected set, not independent notes. **ADR-001** is the root
decision — a swappable protocol frontend over one shared, protocol-agnostic core
(the Object Database, "ODB") — and every other ADR refines one facet of that
split. A recommended reading order is **001 → 002 → 008 → (003, 004, 005) →
(006, 007) → 009**.

- **ADR-001** — the foundational frontend/core split; the umbrella the rest hang off.
- **ADR-002** — the shared vocabulary: **Request** (frontend) → **Task** (ODB) →
  **Job** (Builder). Every other ADR speaks in these terms.
- **ADR-008** — *who owns what* across the Request/Task boundary: the frontend
  owns client-specific request semantics, the ODB owns protocol-agnostic
  Task/Subtask/Job scheduling. It is the lens that keeps 002, 006, and 007
  consistent with one another.
- **ADR-003** — the runtime mechanism: one ODB worker thread behind a synchronous
  facade (request id / push-back), keeping the 002 tiers observable to frontends
  without leaking threads.
- **ADR-004** — the data substrate: a dumb, synchronous, in-memory datastore with
  all concurrency centralized in the ODB (single writer → total order). This is
  what keeps the shared jobs (006) and document states (007) consistent.
- **ADR-005** — the execution end of a Job: Object Builders as plugins per content
  type (job in → objects/diagnostics out). Its uniform contract is what lets 006
  express deduplication and priority inheritance uniformly.
- **ADR-006** — *which shared work to run, and its lifetime*: Job deduplication,
  priority inheritance, reference-counted cancellation (Job granularity).
- **ADR-007** — *in what order to run it*: state-based document priority +
  reference-depth order, recomputed on each interaction (document granularity).
- **ADR-009** — cross-cutting: save-triggered, isolated configuration; it defines
  ADR-007's state-3 (package membership) and the dependency graph, as a
  first-class rebuild event.

### Key cross-references

- **006 → 002** — sharing happens at the *Job* tier, below the Task tier, so it
  does not break the "one request → one task" invariant.
- **008 → 002 / 006 / 007** — the responsibility boundary that keeps the execution
  model, job sharing, and scheduling mutually consistent; this is also where
  "priority is decided in two places" is pinned.
- **003 ↔ 004** — the worker thread runs the heavy Jobs, so the datastore only
  ever sees fast, synchronous operations.
- **005 → 006** — the uniform builder contract is what makes deduplication and
  priority inheritance expressible across content types.
- **009 → 007** — configuration (applied on save) sets state-3 package membership
  and the dependency graph that scheduling orders over.
