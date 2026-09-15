# UC-NNN: <Name>

> **Tailored template for:** gdocServer Phase 2
> **Usage:** Copy this into `../../usecases/UC-NNN_<Name>.md`
> **ID rule:** IF/ST/DR/EH/SCR IDs are **globally unique** across all UC files (no reuse)
> **Terminology:** Use glossary terms from `../../subcomponents/README.md` §6 exclusively

## Use Case

### ID

UC-NNN

### Name

<display name>

### Purpose

<one paragraph: what the user/system does and why>

### Actors

| Actor | Role |
| ----- | ---- |
| IDE Client | LSP protocol peer (user-initiated) |
| C1 Language Server | LSP frontend; translates protocol to ODB API |
| C2 Object Database | Orchestrates Tasks/Jobs; owns scheduling, dedup, cancellation |
| C3 Object Datastore | Internal storage; single-writer (ODB only) |
| C4 Object Builder | Plugin; executes Jobs (Parse/Link/Compile) |

### Derived From

<FR/NFR → ADR → D-NNN chain (one line)>

### Scope Decisions Applied

- D-005 (v1 scope)
- <other D-NNN decisions that affect this UC>

### Preconditions

- <state the system must be in before this UC starts (e.g., "Workspace initialized (UC-001 complete)"; "text document open and tracked (UC-002 complete)")>
- <protocol state: which LSP notifications/requests have already been exchanged>

### Postconditions

- <guaranteed state after this UC completes (e.g., "No pending Jobs for this document"; "Datastore entry deleted; graph references invalidated")>
- <what other components observe (e.g., "C2: Task closed, state=completed")>

---

## Analysis Focus

- <aspect 1>
- <aspect 2>

---

## Main Scenario

<numbered steps; each names the actor and the action>

1. <Actor> does <action>.
2. ...

---

## Alternative Scenarios

### <Alternative Name>

**Condition:** <when this path is taken>

1. <step deviation from main>
2. ...

### <Alternative Name 2>

...

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant IDE as IDE Client
    participant C1 as Language Server
    participant C2 as Object Database
    participant C3 as Object Datastore
    participant C4 as Object Builder

    <interactions>
```

---

## Derived Requirements

### Interface (IF-)

#### IF-NNN

<requirement statement>

**Owner:** C1 | C2 | C4
**Derived From:** UC-NNN step X, <scenario>

### State (ST-)

#### ST-NNN

<state requirement>

**Owner:** C2
**Derived From:** ...

### Data (DR-)

#### DR-NNN

<data requirement>

**Owner:** C3 (internal invariant) | C2 | C4
**Derived From:** ...

### Error Handling (EH-)

#### EH-NNN

<error requirement>

**Owner:** ...
**Derived From:** ...

### Component (SCR-)

#### SCR-C1-NNN (Language Server)

<requirement for C1>

**Derived From:** ...

#### SCR-C2-NNN (Object Database)

<requirement for C2>

**Derived From:** ...

#### SCR-C3-NNN (Object Datastore)

<requirement for C3 — internal invariant, not actor-facing>

**Derived From:** ...

#### SCR-C4-NNN (Object Builder)

<requirement for C4>

**Derived From:** ...

---

## Reverse-check (Contract Cross-Reference)

| UC Requirement | Contract Rule | Status | Note |
| -------------- | ------------- | ------ | ---- |
| IF-NNN | API-NNN / TJ-NNN | ✅ | |
| ST-NNN | TJ-NNN | ✅ | |
| SCR-C2-NNN | TJ-NNN, API-NNN | ✅ | |
| ... | ... | ⚠️ | <gap description> |

> **Status:** ✅ = satisfied · ⚠️ = partial / needs contract extension · ❌ = contract gap

---

## Traceability Matrix

| ID | Type | Description | Scenario Step | Owner |
| -- | ---- | ----------- | ------------- | ----- |
| IF-NNN | Interface | ... | Main #N | C1 |
| ... | | | | |