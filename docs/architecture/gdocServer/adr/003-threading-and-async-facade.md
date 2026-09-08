# ADR-003: Frontend asyncio + background worker thread + synchronous facade

- **ID:** ADR-003
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

The LSP frontend must remain responsive: the guidelines state that client
messages "must be handled with the highest priority" and that it should "avoid
implementing complex processing to keep execution time to a minimum." Yet the
analysis work (parse/link/compile) is CPU-intensive and potentially long-running.
Python is GIL-bound; doing heavy analysis in the same event loop that serves
client I/O would stall responsiveness.

## Decision

- The **LSP frontend** runs on Python `asyncio` and keeps its per-message
  handling light, **deferring heavy work** to the backend.
- The **Object Database** runs on a **dedicated background worker thread** and
  owns an **internal `asyncio` event loop** for concurrent Task/Job
  orchestration.
- The Object Database exposes **thread-safe synchronous methods** to frontends,
  abstracting the internal threading/async complexity. Frontends call
  synchronous methods rather than managing threads/queues themselves.
- **Completion is pushed to the frontend, not polled.** When a Task/Job
  completes, the ODB **invokes a completion callback that the frontend
  registered in advance**, calling it **on the ODB's own worker thread** and
  with **no knowledge of the frontend's threading/async model**. The (async)
  frontend's callback does nothing heavy: it only **hands the event onto its
  own event loop** (e.g. `asyncio` `loop.call_soon_threadsafe`). This removes
  polling and keeps the ODB and the frontend decoupled from each other's
  concurrency mechanisms.

> **Python implementation.** Fully supported in the standard library. The ODB
> stores plain callables and, on its worker thread, simply calls
> `callback(ticket)`. The async frontend registers a callback that calls
> `loop.call_soon_threadsafe(handler, ticket)` (or, for a coroutine,
> `asyncio.run_coroutine_threadsafe(handler(ticket), loop)`). Both
> `*_threadsafe` APIs are designed to be invoked from a **foreign thread** and
> atomically schedule work on the target loop — so the ODB never needs to know
> the loop exists, and no polling is required.

## Alternatives Considered

- Run all analysis inside the frontend's `asyncio` event loop (single-threaded
  async), using `run_in_executor` for CPU-bound work.
- A thread pool owned by the frontend, with the frontend dispatching and
  merging results.
- A fully multi-process design (a separate analysis process) with IPC.
- **Frontend polling for completion:** the frontend repeatedly queries the ODB's
  ticket status. Rejected: wastes CPU, adds latency, and couples the frontend to
  the ODB's ticket API and to its own poll interval.

## Consequences

### Pros

- The frontend I/O loop is **never blocked by CPU-bound analysis**, sustaining
  the stated responsiveness non-functional requirement.
- A single background thread + one internal event loop gives a **single,
  well-defined place** for scheduling, cancellation, and state, simplifying
  correctness.
- A synchronous facade keeps the frontend simple and hides the core's internal
  concurrency, so the frontend can stay `async` without leaking threads.

### Cons / Trade-off

- A single worker thread caps parallel analysis to what the internal event loop
  can schedule concurrently; CPU-bound Jobs may need `run_in_executor` inside
  the ODB to use multiple cores, adding complexity.
- Registered **completion callbacks must be lightweight**: the ODB invokes them
  on its own worker thread, so a callback that does heavy work would block the
  ODB. The (async) frontend therefore only posts to its loop
  (`loop.call_soon_threadsafe`) and defers the real work to the loop.
- Cross-thread hand-off must use asyncio's **thread-safe** APIs
  (`loop.call_soon_threadsafe` / `asyncio.run_coroutine_threadsafe`); a plain
  `loop.call_soon` from the ODB worker thread is **not** safe.
