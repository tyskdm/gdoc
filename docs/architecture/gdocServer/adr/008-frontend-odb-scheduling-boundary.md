# ADR-008: Responsibility boundary between frontend Requests and ODB Task/Subtask/Job scheduling

- **ID:** ADR-008
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

gdoc Server serves one LSP client and (per ADR-001) possibly multiple
object-server clients — and, in the future, other protocol frontends such as an
MCP server. Each client type has a *different* notion of "what the user is
focused on" (open buffers, active requests) and different rules for when a
request should be prioritized or canceled. LSP request semantics are not
object-server semantics, and both are not MCP semantics.

At the same time, the work those requests ultimately cause — parsing, linking,
compiling — is *shared* and *protocol-agnostic*: two different frontends asking
for the same document produce the same underlying work (ADR-006). The execution
engine (the Object Database, "ODB") must therefore run that work under a single,
consistent set of rules.

An earlier draft of this ADR expressed the client-specific vs. common split as a
class hierarchy *inside* the ODB — an abstract base scheduler plus one concrete
subclass per client type. That framing had two problems:

1. It leaked client-type-specific request semantics into the protocol-agnostic
   core, undercutting the clean frontend/core split of ADR-001.
2. It contradicted ADR-002, where a *Task* is a **protocol-agnostic** unit owned
   and scheduled by the ODB — i.e. it should *not* be scheduled per client type.

The client-specific differences really live at the **Request** level, and that
level is owned by the frontend.

## Decision

Responsibility is split along the **Request / Task boundary** (ADR-002) by
**component**, not by class hierarchy:

- **Requests are the frontend's responsibility.** Each protocol frontend (LSP,
  object-server, MCP, …) is a separate component that:
  - translates its protocol messages into Requests and back;
  - tracks *its own* open documents, active requests, and focus; and
  - applies the **client-type-specific** rules for request priority, ordering,
    and cancellation.

  Because these rules differ per client type, the logic lives in the frontend,
  next to the protocol it belongs to.

- **Tasks — and the Subtasks / Jobs they decompose into — are the ODB's
  responsibility.** A Task is protocol-agnostic: the ODB assigns and manages its
  priority, lifecycle, and cancellation, and it is processed with **the same
  rules regardless of which frontend submitted it**. The ODB:
  - maps a Request 1:1 to a Task (ADR-002);
  - deduplicates shared processing into Subtasks (task-local) and shared Jobs
    (ADR-006); a shared unit is traced from the **target object** so a parse
    already started by an earlier request is not re-executed; and
  - dispatches atomic Jobs to Builders, which may run them as **subprocesses**
    (e.g. `pandoc` for Markdown) — one launch = one Job (ADR-005).

  The ODB does **not** branch its Task/Subtask/Job logic on the client type.

- **Hand-off contract.** A light request is answered inline and its result
  returned; a heavy request returns a **request id** (task handle / ticket),
  after which completion is *pushed* back to the frontend (ADR-003). The
  frontend therefore knows "I must wait" without any knowledge of the ODB's
  internal threading or of other clients.

In one line: **client-specific = Requests (frontend); protocol-agnostic =
Task/Subtask/Job (ODB).**

## Alternatives Considered

- **Per-client-type scheduler subclasses inside the ODB** (the earlier draft):
  an abstract base implementing the common priority logic plus one concrete
  subclass per client type. Rejected: leaks client-type request semantics into
  the protocol-agnostic core, contradicts ADR-002's protocol-agnostic Task, and
  weakens ADR-001's frontend/core split.
- **A single global scheduler flattening all clients into one priority space:**
  forces one set of request rules onto frontends that need different ones, and
  loses per-client focus semantics.
- **Fully independent schedulers, one per frontend, with no shared core:**
  duplicates the (protocol-agnostic) Task/Subtask/Job scheduling and Job
  deduplication, and re-introduces the inconsistent-snapshot problem ADR-006
  exists to solve.

## Consequences

### Pros

- **Single owner per decision.** Every request priority/ordering/cancellation
  decision has exactly one owner — the frontend that made it. The ODB never has
  to interpret client-type semantics.
- **Consistent with ADR-001/002/005/006/007.** The split is a component
  boundary (frontend vs. core), so adding a new frontend (Object Server, MCP) is
  *additive* and does not touch the ODB's scheduling code.
- **Uniform task semantics.** Two frontends requesting the same document
  exercise the *same* Task/Subtask/Job path, so deduplication (ADR-006) and
  state-based document priority (ADR-007) apply identically.
- **Frontends stay small.** Each implements one protocol's rules and talks to a
  synchronous ODB facade (ADR-003); it does not manage threads, jobs, or other
  clients.

### Cons / Trade-off

- **Priority is decided in two places.** The frontend orders *its* requests; the
  ODB orders the shared work (document states, ADR-007). The boundary — "frontend
  picks *which requests matter and in what order*; ODB picks *which shared work
  runs first*" — must be stated clearly or it will be crossed.
- **The ODB still needs context to schedule** (which documents a request touches,
  reference depth). That context must be expressible as protocol-agnostic Request
  fields. If a client type needs something the Request model lacks, the Request
  model (ADR-002) is extended — the ODB must not be allowed to special-case the
  client type.
- **Cancellation semantics differ by protocol** (e.g. closing a document in LSP
  cancels its hover tasks; an object-server client has its own rules). Each
  frontend translates *its* cancellation into the ODB's Task/Job cancellation
  API, so the ODB's cancellation stays protocol-agnostic.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-008-1 (correctness — cancellation translation).** Each frontend must
  translate its protocol's cancellation (LSP cancel, document close, client
  disconnect; the Object Server has its own rules) into the ODB's Task/Job
  cancellation API.
  - *Failure mode:* A mistranslation over- or under-decrements Job
    references (R-006-3), leaks tasks, or cancels work other tasks still need.
  - *Mitigation:* The ODB cancellation API stays protocol-agnostic; per-
    frontend translation is a small, unit-testable mapping.
  - *Verify:* per-protocol tests that each cancellation event maps to exactly
    the right Task/Job cancellations and no more.
- **R-008-2 (correctness — boundary discipline).** The ODB must never branch
  on client type.
  - *Failure mode:* Special-casing leaks client semantics into the
    protocol-agnostic core, breaking the ADR-001 split and making
    deduplication/scheduling (ADR-006/007) frontend-dependent.
  - *Mitigation:* The Request model (ADR-002) must express all context the ODB
    needs; the escape valve is extending the model, not branching on the
    client.
  - *Verify:* architectural test that the ODB's scheduling/cancellation
    decision paths never inspect a client-type field.

Extending the Request model when a client type needs something new is an
accepted trade-off (it is additive).