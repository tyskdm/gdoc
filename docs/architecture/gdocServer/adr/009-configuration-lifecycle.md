# ADR-009: Save-triggered, isolated configuration handling

- **ID:** ADR-009
- **Status:** Accepted
- **Date:** 2026-09-08

## Context / Background

The project/package structure (which folders are packages, their dependencies,
external references) is defined by configuration (e.g., `gdoc.project.json`).
This structure determines document state-3 membership (ADR-007) and the
dependency graph. The architecture notes that "changes to the package settings
in the workspace (project) root configuration file can alter this state" and
that "changes to configuration files are **not affected by changes to open text
documents** and are **only reflected upon saving**."

## Decision

- Changes to project/package **configuration** are applied **only on save**, not
  on every keystroke, and are treated as a distinct, higher-stability track
  from live document edits.
- A configuration change is a **first-class event** that (re)defines which
  documents belong to packages and their dependency relationships; it is
  scheduled independently of, and is **not invalidated by**, changes to open
  text documents.
- The resulting re-scoping (added/removed packages, changed dependencies)
  triggers the appropriate rebuild/invalidation in the Object Database.

## Alternatives Considered

- **Live configuration** (apply on every keystroke), treating the config file
  like an open buffer — risks constant re-scoping and wasted work.
- Configuration applied **only on an explicit "reload workspace" command** —
  simpler, but config edits silently take no effect until the user remembers to
  reload.
- Configuration as part of the **same document-edit pipeline** (a `didChange`
  on the config file) — couples stable structure to volatile edits.

## Consequences

### Pros

- **Stable structure**: package membership and the dependency graph do not
  churn during casual editing of the config file.
- **Clear semantics**: "what you are typing in the editor is not the project
  structure; saving is what defines it," matching editor expectations.
- Config changes are a **bounded, discrete event** → easier to schedule,
  cancel, and rebuild correctly than a continuous stream of edits.

### Cons / Trade-off

- A config edit has **no effect until saved**, which can surprise users who
  expect live behavior.
- The server must **reconcile a saved-config re-scope against in-flight tasks**
  (a document that was in a package may no longer be), requiring careful
  invalidation and re-scheduling.
- Because config changes are "not affected by open text documents," a save must
  correctly override any stale open-buffer assumptions, and the reverse (open-
  buffer changes must not override config) must be enforced.

### Risks

> A **risk** (in contrast to the trade-offs above) is a constraint that, if
> violated in detailed design or implementation, breaks *correctness* (silent
> corruption, stale results, lost work) or *availability* (deadlock,
> starvation, unbounded resource use). Each entry states its failure mode, the
> mitigation the Decision already provides, and the verification it requires.
> All risks are collected in the [risk register](./README.md#risk-register).

- **R-009-1 (correctness — re-scope vs. in-flight tasks).** A saved
  configuration triggers a re-scope while tasks are in flight.
  - *Failure mode:* A document that leaves a package keeps its state-3
    priority or stale objects; newly added dependencies are not picked up —
    inconsistent dependency graph and scheduling state.
  - *Mitigation:* The config save is a first-class invalidation event handled
    by the single coordinator (ADR-004); detailed design must define how
    in-flight tasks affected by the re-scope are invalidated/re-scheduled.
  - *Verify:* test a config save during in-flight builds; assert final package
    membership, priority states, and objects match the saved configuration.
- **R-009-2 (correctness — override rules).** Config must override stale
  open-buffer assumptions; open-text changes must not override config.
  - *Failure mode:* The server applies unsaved buffer edits as the project
    structure, or lets buffer edits invalidate a saved configuration — wrong
    document states (ADR-007) and wrong scheduling.
  - *Mitigation:* Configuration is applied only from saved content (Decision);
    buffer edits never touch config-derived state.
  - *Verify:* test: edit config unsaved → no effect; save → effect; an
    open-text edit racing a config save → the saved configuration wins for
    structural facts.

The "no effect until saved" UX surprise is an accepted, deliberate trade-off.
