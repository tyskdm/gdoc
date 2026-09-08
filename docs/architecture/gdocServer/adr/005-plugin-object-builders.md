# ADR-005: Plugin-based Object Builders per content type

- **ID:** ADR-005
- **Status:** Proposed
- **Date:** 2026-09-08

## Context / Background

gdoc supports multiple content types that differ in syntax and object model
(e.g., `gdoc` markup, `doxml` source). Parsing, linking, and compiling these
require domain-specific logic. The Object Database must orchestrate this work
without depending on any one content type. The architecture states that
"Different Builders are provided as plugins for each type of target package,"
that the Object Database is a "Plugin Host," and that builders provide a
"Plugin-Based Architecture" for specific content types (e.g., `gdoc`, `doxml`).

## Decision

- Content-specific build logic is encapsulated in **Object Builders**, one (or
  more) per content type, integrated as **plugins** whose lifecycle is managed
  by the Object Database (the plugin host).
- Builders are the **only** component that converts raw source into gdoc
  objects, semantic tokens, symbols, and diagnostics.
- The core (Object Database, Datastore, frontends) is **agnostic to which
  builders are present**; adding a new content type means adding a new builder,
  not modifying the core.

## Alternatives Considered

- Hard-coding content-type `if/else` dispatch inside the Object Database.
- A single generic builder with a large set of runtime-configured,
  format-specific strategies.
- External parser processes (separate binaries) invoked per content type.

## Consequences

### Pros

- **Open/closed**: new content types are added without touching scheduling,
  storage, or frontends.
- Domain logic is isolated and independently testable per builder.
- A uniform builder contract (job in → objects/diagnostics out) is what enables
  job deduplication and priority inheritance (ADR-006) to be expressed
  uniformly.

### Cons / Trade-off

- The plugin contract must be rich enough to cover the differences between
  builders (cancellation, incremental parsing, error reporting) without leaking
  content-type details.
- Builders that are long-running or CPU-bound still need to run under the ODB's
  concurrency model (ADR-003), so the plugin API must expose cooperative
  cancellation or run in an executor.
- A richer set of builders means more surface area for inconsistency; a shared
  "builder SDK"/base class is needed to keep the contract uniform.
