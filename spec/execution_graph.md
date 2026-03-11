# Execution Graph

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/execution_graph.md`

---

## Purpose

The Polaris execution graph describes how proposed state transitions move
through validation, commitment, canonical state advancement, and execution
authorization.

Unlike conventional workflow graphs that represent task ordering, the Polaris
execution graph represents the authoritative progression of system state and
the conditions under which side effects MAY occur. It captures the causal
structure of the Polaris architecture.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Architectural Role

The execution graph connects the following core Polaris mechanisms:

- Proposed State Transition Objects (PSTOs)
- Validation pipeline evaluation
- Commit authority
- Canonical state pointer advancement
- Execution gate enforcement

Together these form a deterministic progression pipeline. No stage MAY be
bypassed. No side effect MAY occur outside this pipeline.

---

## Graph Model

The Polaris execution model is represented as a directed acyclic graph:

```
Nodes = canonical system states
Edges = validated, committed transitions
```

Each edge represents a candidate transition produced by a PSTO. A node is
reachable only if the transition producing it passed validation and was
committed by commit authority.

Polaris enforces that only a single validated transition MAY advance canonical
state from any predecessor node. This produces a single canonical execution
path.

---

## Canonical Progression

Let:

```
S_n   = canonical state at step n
T_n   = validated transition at step n
```

Canonical progression MUST follow:

```
S_0 -> S_1 -> S_2 -> ... -> S_n

where S_{n+1} = commit(S_n, T_n)
```

Each `S_n` is identified by its `canonical_pointer_ref` value. Each transition
`T_n` is identified by its `event_id`, derived from canonical encoding as
defined in `spec/canonical_encoding.md`.

Only transitions that satisfy the following MAY produce the next canonical
state:

1. Canonical encoding succeeds.
2. Validation-pass result is produced under the applicable gate profile.
3. `canonical_pointer_ref` equals the current canonical state pointer.
4. Commit authority accepts the transition.

---

## Candidate Transition Graph

At any point, multiple candidate transitions MAY reference the same
predecessor state:

```
        T_a
S_n ----------> S_a   (candidate)

        T_b
S_n ----------> S_b   (candidate)

        T_c
S_n ----------> S_c   (candidate)
```

Polaris MUST allow only one of these transitions to become authoritative.
Commit authority enforces this by:

1. Accepting the first transition satisfying validation and pointer equality.
2. Rejecting all subsequent transitions referencing the same
   `canonical_pointer_ref`.

Rejected candidate transitions MUST NOT produce side effects and MUST NOT
enter canonical history.

---

## Linearization Point

The execution graph contains exactly one linearization point for authoritative
state progression. This point occurs at commit authority when the canonical
state pointer advances.

```
Before commit:   transitions are candidates only
After commit:    the committed transition is authoritative
```

The linearization point MUST be singular. Implementations that distribute
commit authority MUST preserve a single authoritative commit decision, as
required by the Exclusive Commit Authority invariant defined in
`spec/invariants.md`.

---

## Pipeline Structure

The authoritative progression pipeline MUST be traversed in the following
order for every state transition:

```
PSTO (event_type: "psto")
        |
        v
Validation (event_type: "validation_artifact")
        |
        v
Commit Authority (event_type: "commit_record")
        |
        v
Canonical State Pointer advancement
        |
        v
Execution Gate (event_type: "execution_request")
        |
        v
Side Effects (event_type: "execution_receipt")
```

Each stage represents an enforcement boundary. A transition MUST NOT advance
to the next stage if the current stage fails.

The event types at each stage correspond directly to the `event_type` enum
values defined in `spec/schemas/event.schema.json`.

---

## Execution Authorization

Side effects MUST NOT be triggered by candidate transitions.

Execution is permitted only when an execution request satisfies:

```
execution_request.canonical_pointer_ref == current canonical state pointer
```

A Polaris implementation MUST reject any execution request whose
`canonical_pointer_ref` does not equal the canonical state pointer at
evaluation time. This is the Execution Causality Binding invariant.

---

## Graph Constraints

The Polaris execution graph enforces the following constraints. Each
corresponds to an invariant defined in `spec/invariants.md`:

| Constraint | Corresponding Invariant |
|---|---|
| State nodes form a single authoritative chain | Canonical Progression Uniqueness |
| Transitions MUST pass validation before commit | Mandatory Validation Precondition |
| Only commit authority MAY advance canonical state | Exclusive Commit Authority |
| Execution requires `canonical_pointer_ref` equality | Execution Causality Binding |
| Rejected transitions MUST NOT produce side effects | Non-Bypassable Enforcement Boundary |

---

## Replay and Graph Reconstruction

The canonical state store records committed transitions as an append-only
sequence of `commit_record` events.

During replay, an observer MUST reconstruct the execution graph by
sequentially applying committed transitions in `context.sequence` order.
Replay MUST NOT:

- Mutate canonical state
- Advance the canonical pointer
- Trigger side effects
- Introduce new authoritative transitions

Because `event_id` values are hash-derived from canonical encoding and each
transition references its predecessor via `canonical_pointer_ref`, modification
of any prior node invalidates the entire downstream graph. Replay therefore
verifies both graph structure and state progression simultaneously.

---

## Multi-System Coordination

In deployments where multiple subsystems evaluate execution eligibility, the
canonical state pointer MUST act as the shared coordination primitive.

Independent subsystems MAY evaluate execution eligibility against the same
canonical state pointer value. However, each subsystem MUST independently
verify `canonical_pointer_ref` equality before authorizing execution. No
subsystem MAY delegate this check to another.

This allows Polaris to coordinate execution across distributed components
while preserving deterministic state authority and the Non-Bypassable
Enforcement Boundary invariant.

---

## Security Properties

The execution graph model prevents the following failure classes:

- **Race-condition state mutation** — serialized by the linearization point
- **Unauthorized state progression** — prevented by commit authority exclusivity
- **Side effects from uncommitted state** — prevented by execution causality binding
- **Forked authoritative histories** — prevented by canonical progression uniqueness
- **Replay-visible divergence** — prevented by deterministic canonical encoding

---

## Minimal Compliance Statement

A Polaris implementation is compliant with the execution graph model only if:

1. All authoritative state transitions traverse the full pipeline in order.
2. Only one candidate transition MAY become authoritative per canonical
   predecessor state.
3. Execution MUST NOT occur unless `canonical_pointer_ref` equals the
   current canonical state pointer.
4. Replay of committed transitions MUST reproduce identical canonical state
   identifiers across independent compliant implementations.
5. No stage in the pipeline MAY be bypassed by any subsystem, interface,
   or external integration.
