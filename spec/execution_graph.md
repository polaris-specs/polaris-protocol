# Execution Graph

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/execution_graph.md`

---

## Purpose

The execution graph defines the structural enforcement of canonical state
progression, from proposed transition through validation, commitment,
canonical pointer advancement, and execution authorization.

Side effects cannot occur outside this structure.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Architectural Role

The execution graph connects the following enforcement mechanisms:

- Proposed State Transition Objects (PSTOs)
- Validation pipeline
- Commit authority
- Canonical state pointer advancement
- Execution gate

Together these form a deterministic progression pipeline. No stage MAY be
bypassed. No side effects MAY occur outside this pipeline.

---

## Graph Model

The Polaris execution model is represented as a directed acyclic graph:

```
Nodes = canonical states
Edges = validated, committed transitions
```

A node is reachable only if the transition producing it was validated and
committed by commit authority.

Only a single validated transition MAY advance canonical state from any
predecessor node. This constraint produces a single canonical execution path.

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

A transition MAY produce the next canonical state only if:

1. Canonical encoding succeeds.
2. A validation-pass result is produced under the applicable gate profile.
3. `canonical_pointer_ref` equals the current canonical state pointer.
4. Commit authority accepts the transition.

---

## Candidate Transition Graph

Multiple candidate transitions MAY reference the same predecessor state:

```
        T_a
S_n ----------> S_a   (candidate)

        T_b
S_n ----------> S_b   (candidate)

        T_c
S_n ----------> S_c   (candidate)
```

Only one of these transitions MAY become authoritative. Commit authority
enforces this by:

1. Accepting the first transition satisfying validation and pointer equality.
2. Rejecting all subsequent transitions referencing the same
   `canonical_pointer_ref`.

Rejected candidate transitions MUST NOT produce side effects and MUST NOT
enter canonical history.

---

## Linearization Point

The execution graph contains exactly one linearization point for canonical
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

The progression pipeline MUST be traversed in the following order for every
state transition:

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

Each stage is an enforcement boundary. A transition MUST NOT advance to the
next stage if the current stage fails.

The event types at each stage correspond to the `event_type` enum values
defined in `spec/schemas/event.schema.json`.

---

## Execution Authorization

Side effects MUST NOT be triggered by candidate transitions.

Execution is permitted only if:

```
execution_request.canonical_pointer_ref == current canonical state pointer
```

Any execution request whose `canonical_pointer_ref` does not equal the
canonical state pointer at evaluation time MUST be rejected. This enforces
the Execution Causality Binding invariant defined in `spec/invariants.md`.

---

## Graph Constraints

Each constraint corresponds to an invariant defined in `spec/invariants.md`:

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

During replay, a verifier MUST reconstruct the execution graph by
sequentially applying committed transitions in `context.sequence` order.
Replay MUST NOT:

- Mutate canonical state
- Advance the canonical pointer
- Trigger side effects
- Introduce new authoritative transitions

Because `event_id` values are hash-derived from canonical encoding and each
transition references its predecessor via `canonical_pointer_ref`, modification
of any prior node invalidates the entire downstream graph. Replay verifies
graph structure and state progression as a single operation.

---

## Multi-System Coordination

In deployments where multiple subsystems evaluate execution eligibility, the
canonical state pointer MUST act as the shared coordination primitive.

Each subsystem MUST independently verify `canonical_pointer_ref` equality
before authorizing execution. No subsystem MAY delegate this verification
to another.

---

## Structural Guarantees

The execution graph structurally prevents:

- **Race-condition state mutation** — serialized by the linearization point
- **Unauthorized state progression** — commit authority exclusivity
- **Side effects from uncommitted state** — execution causality binding
- **Forked authoritative histories** — canonical progression uniqueness
- **Replay-visible divergence** — deterministic canonical encoding

---

## Minimal Compliance Statement

A Polaris implementation is compliant with the execution graph only if:

1. All authoritative state transitions traverse the full pipeline in order.
2. Only one candidate transition MAY become authoritative per canonical
   predecessor state.
3. Execution MUST NOT occur unless `canonical_pointer_ref` equals the
   current canonical state pointer.
4. Replay of committed transitions MUST reproduce identical canonical state
   identifiers across independent compliant implementations.
5. No stage in the pipeline MAY be bypassed by any subsystem, interface,
   or external integration.
