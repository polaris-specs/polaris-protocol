# Architectural Invariants

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/invariants.md`

---

## Purpose

Polaris is defined by invariants that MUST remain true across all compliant
implementations.

These invariants define the structural conditions under which canonical state
MAY advance, side effects MAY occur, and canonical history MAY be replayed
and verified.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Invariant Set

Polaris preserves the following core invariant set:

1. Canonical Progression Uniqueness
2. Mandatory Validation Precondition
3. Exclusive Commit Authority
4. No Authoritative Mutation Outside Commit
5. Execution Causality Binding
6. Canonical Pointer Authority
7. Deterministic Replay Reproducibility
8. Non-Bypassable Enforcement Boundary

These invariants are mutually reinforcing. No subset is sufficient.

---

## 1. Canonical Progression Uniqueness

For any canonical state referenced by `canonical_pointer_ref`, at most one
committed successor state MAY become authoritative.

If multiple proposed state transition objects reference the same
`canonical_pointer_ref` value, only the first transition satisfying
validation and commit conditions MAY advance the canonical state pointer.
Any subsequent transition referencing the same `canonical_pointer_ref`
MUST be deterministically rejected.

**Prevents:**

- Parallel authoritative successor states
- Canonical fork formation
- Ambiguous next-state selection

**Compliance requirement:** No more than one committed successor state is
derivable from any canonical predecessor state.

---

## 2. Mandatory Validation Precondition

Canonical state advancement is permitted only when a validation-pass result
has been deterministically produced under the applicable gate profile.

No subsystem, execution context, runtime override, configuration flag,
operator action, or recovery path MAY advance canonical state without
satisfaction of the required validation gates.

**Prevents:**

- Canonical state advancement without validated transitions
- Configuration-based bypass of validation
- Recovery paths that circumvent validation semantics

**Compliance requirement:** Canonical state advancement MUST NOT occur in the
absence of a successful validation-pass result under the applicable gate
profile.

---

## 3. Exclusive Commit Authority

Canonical state pointer advancement is controlled exclusively by commit
authority.

A Polaris system MAY implement commit authority as a single subsystem,
quorum service, threshold mechanism, consensus-bound commit group, or other
compliant authority structure. Regardless of implementation form, canonical
state advancement MUST remain exclusively controlled by commit authority
and MUST NOT be distributed across uncontrolled mutation paths.

**Prevents:**

- Canonical state advancement from implicit state mutation
- Multiple uncoordinated commit paths

**Compliance requirement:** Exactly one authoritative commit path MUST exist
for canonical state advancement, even where commit authority is internally
distributed.

---

## 4. No Authoritative Mutation Outside Commit

No subsystem, interface, code path, or execution context MAY produce an
authoritative state change without passing through validation, commit
authority, and canonical state pointer advancement.

Non-authoritative intermediate state, simulation state, cached projections,
speculative outputs, and local subsystem views do not constitute canonical
state and MUST NOT be treated as authoritative.

**Prevents:**

- Hidden mutation channels
- Side-channel canonical state substitution
- Authoritative mutation through local caches or projections
- Direct store mutation without canonical commit semantics

**Compliance requirement:** Any operation capable of producing authoritative
state change MUST be structurally routed through the validated commit pathway.

---

## 5. Execution Causality Binding

Side effects cannot occur except as a consequence of committed canonical state.

An execution request is permitted only when the request references a
`canonical_pointer_ref` value equal to the canonical state pointer at the
time of evaluation.

**Prevents:**

- Side effects from uncommitted state
- Execution authorized from stale or superseded state
- Side effects outside the validated commit pathway

**Compliance requirement:** Any execution request whose `canonical_pointer_ref`
does not equal the canonical state pointer at evaluation time MUST be rejected.

---

## 6. Canonical Pointer Authority

At any given time, exactly one canonical state pointer value determines the
currently authoritative committed state for the applicable Polaris domain.

The canonical pointer MAY be embodied as a direct state hash,
Merkle-root-derived reference, monotonic index cryptographically bound to
prior canonical state, or coordinated pointer set yielding one authoritative
interpretation. Regardless of form, only one authoritative canonical state
MUST be deterministically derivable at any time.

**Prevents:**

- Divergent authoritative state references across subsystems
- Alternative pointer forms producing alternative authoritative states

**Compliance requirement:** A uniquely authoritative canonical state reference
MUST exist for all operations that depend on canonical state interpretation.

---

## 7. Deterministic Replay Reproducibility

For any given canonical state history and set of referenced artifacts,
independent compliant implementations MUST reproduce the same canonical state
identifiers, validation outcomes, and replay-visible enforcement results.

Replay is verification, not re-execution of authority. Replay MUST NOT
mutate canonical state, advance the canonical pointer, trigger side effects,
or introduce new authoritative transitions.

**Prevents:**

- Non-deterministic canonical history
- Cross-implementation divergence
- Replay-visible outcomes that differ for identical canonical inputs

**Compliance requirement:** Sufficient determinism in canonical encoding,
validation binding, commit record derivation, and replay-visible artifact
structure MUST be preserved to allow independent recomputation of canonical
progression.

---

## 8. Non-Bypassable Enforcement Boundary

No subsystem, interface, execution path, or external integration MAY produce
authoritative state advancement or side-effect authorization except through
the validated commit pathway and execution gate.

Where implementations expose external interfaces, those interfaces MUST
remain subordinate to the same invariant-preserving control structure.

**Prevents:**

- Alternate execution channels around the execution gate
- External integrations bypassing canonical state checks
- Hidden authority escalation through integration layers

**Compliance requirement:** All authoritative state mutation and all protected
execution MUST remain inside invariant-preserving enforcement boundaries.

---

## Derived Invariant Relationships

The Polaris invariant set forms a dependency structure:

- **Canonical Progression Uniqueness** depends on Exclusive Commit Authority
  and Canonical Pointer Authority.
- **Mandatory Validation Precondition** constrains Exclusive Commit Authority.
- **No Authoritative Mutation Outside Commit** depends on Mandatory Validation
  Precondition and Exclusive Commit Authority.
- **Execution Causality Binding** depends on Canonical Pointer Authority.
- **Deterministic Replay Reproducibility** depends on canonical encoding,
  validation binding, and canonical record derivation.
- **Non-Bypassable Enforcement Boundary** preserves the entire invariant set
  against alternate channels.

No invariant MUST be interpreted in isolation where doing so would weaken
the combined constraint set.

---

## Implementation Flexibility

A compliant implementation MAY vary internally in:

- Deployment model
- Process model
- Node topology
- Cryptographic primitives
- Storage substrate
- Hardware trust anchors
- Execution environment

Such variation is compliant only if the implementation preserves the full
invariant set. Implementation flexibility does not authorize invariant
relaxation.

---

## Violation Semantics

A violation occurs when a system permits behavior inconsistent with one or
more Polaris invariants, including but not limited to:

- More than one authoritative successor state derivable from a single
  `canonical_pointer_ref` value
- Canonical state advancement without a validation-pass result
- Canonical state advancement outside commit authority
- Side effects authorized from uncommitted or stale state
- Multiple conflicting authoritative canonical pointer interpretations
- Replay-visible outcomes that differ across compliant implementations for
  identical canonical inputs
- Alternate execution channels that bypass the execution gate

A system exhibiting such behavior MUST NOT be described as Polaris-compliant.

---

## Minimal Compliance Statement

A system is Polaris-compliant with respect to architectural invariants only
if it:

1. Preserves a single authoritative canonical state progression.
2. Requires a deterministic validation-pass result before canonical state
   advancement.
3. Restricts authoritative mutation to commit authority.
4. Binds side effects to `canonical_pointer_ref` equality at evaluation time.
5. Supports deterministic replay of canonical history across independent
   compliant implementations.

Partial compliance is not compliance.
