# ADR-009: Save-triggered, isolated configuration handling

- **ID:** ADR-009
- **Status:** Proposed
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
