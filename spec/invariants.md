# Architectural Invariants

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/invariants.md`

---

## Purpose

Polaris is defined not only by components, but by invariants that MUST
remain true across all compliant implementations.

These invariants describe the structural conditions under which canonical
state MAY advance, side effects MAY occur, and canonical history MAY be
replayed and verified. They are not operational preferences. They are
architectural constraints that preserve the identity of the Polaris
execution model.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Why Invariants Matter

In a conventional system, behavior may emerge from code paths, local policy
checks, and best-effort controls. In Polaris, the execution model is defined
by properties that MUST remain true regardless of deployment model, subsystem
topology, implementation language, or hardware environment.

An implementation that violates these invariants may still function as
software, but it is no longer a compliant Polaris system.

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

These invariants are mutually reinforcing. Together they define Polaris as
a validated, commit-gated, canonical-state execution architecture.

---

## 1. Canonical Progression Uniqueness

For any canonical predecessor state referenced by `canonical_pointer_ref`,
at most one committed successor state MAY become authoritative.

If multiple proposed state transition objects reference the same
`canonical_pointer_ref` value, only the first transition satisfying
validation and commit conditions MAY advance the canonical state pointer.
Any subsequent transition referencing the same `canonical_pointer_ref`
MUST be deterministically rejected for canonical advancement.

**This invariant prevents:**

- Parallel authoritative successor states
- Canonical fork formation
- Dual-authority progression
- Ambiguous next-state selection

**Compliance requirement:** A Polaris implementation MUST ensure that no
more than one authoritative committed successor state is derivable from any
canonical predecessor state.

---

## 2. Mandatory Validation Precondition

Canonical state advancement is permitted only when a validation-pass result
has been deterministically produced under the applicable gate profile.

No subsystem, execution context, runtime override, configuration flag,
operator action, or recovery path MAY advance canonical state without
satisfaction of the required validation gates.

**This invariant ensures:**

- Validation is upstream of commit
- Invalid transitions cannot become authoritative
- Configuration-based bypass cannot grant canonical mutation authority
- Recovery and operational exceptions remain subject to validation semantics

**Compliance requirement:** A Polaris implementation MUST reject any attempt
to produce authoritative canonical state advancement in the absence of a
successful validation-pass result under the applicable gate profile.

---

## 3. Exclusive Commit Authority

Canonical state pointer advancement is controlled exclusively by commit
authority.

A Polaris system MAY implement commit authority as a single subsystem,
quorum service, threshold mechanism, consensus-bound commit group, or other
compliant authority structure. Regardless of implementation form, canonical
state advancement MUST remain exclusively controlled by a commit authority
and MUST NOT be distributed across uncontrolled mutation paths.

**This invariant ensures:**

- Commit remains the single linearization point for authoritative progression
- Canonical advancement cannot emerge from implicit state mutation
- Distributed implementations still preserve a single authoritative commit
  decision

**Compliance requirement:** A Polaris implementation MUST preserve exactly
one authoritative commit path for canonical state advancement, even where
commit authority is internally distributed.

---

## 4. No Authoritative Mutation Outside Commit

No subsystem, interface, code path, or execution context MAY produce an
authoritative system state change without passing through validation, commit
authority, and canonical state pointer advancement.

Non-authoritative intermediate state, simulation state, cached projections,
speculative outputs, and local subsystem views do not constitute canonical
state and MUST NOT be treated as authoritative.

**This invariant prevents:**

- Hidden mutation channels
- Side-channel canonical state substitution
- Authoritative mutation through local caches or projections
- Bypass by direct store mutation without canonical commit semantics

**Compliance requirement:** A Polaris implementation MUST ensure that any
operation capable of producing authoritative state change is structurally
routed through the validated commit pathway.

---

## 5. Execution Causality Binding

Any side-effecting operation MUST be causally bound to committed canonical
state.

An execution request is permitted only when the request references a
`canonical_pointer_ref` value equal to the canonical state pointer at the
time of evaluation. This ensures that external side effects occur only as a
consequence of validated and committed state transitions.

**This invariant ensures:**

- Side effects cannot be triggered from uncommitted state
- Stale or superseded state cannot authorize execution
- Execution is downstream of validation and commit
- Real-world effects are bound to canonical lineage

**Compliance requirement:** A Polaris implementation MUST reject any
side-effecting request whose `canonical_pointer_ref` does not equal the
canonical state pointer at evaluation time.

---

## 6. Canonical Pointer Authority

At any given time, exactly one canonical state pointer value determines the
currently authoritative committed state for the applicable Polaris domain.

The pointer MAY be embodied as a direct state hash, Merkle-root-derived
reference, monotonic index cryptographically bound to prior canonical state,
or coordinated pointer set yielding one authoritative interpretation.
Regardless of form, only one authoritative canonical state MUST be
deterministically derivable at any time.

**This invariant ensures:**

- All compliant subsystems converge on the same authoritative state reference
- Execution and replay reason over the same canonical lineage
- Alternative pointer forms do not create alternative authoritative states

**Compliance requirement:** A Polaris implementation MUST preserve a uniquely
authoritative canonical state reference for all operations that depend on
authoritative state interpretation.

---

## 7. Deterministic Replay Reproducibility

For any given canonical state history and set of referenced artifacts,
independent compliant implementations MUST be able to reproduce the same
canonical state identifiers, validation outcomes, and replay-visible
enforcement results.

Replay is verification, not re-execution of authority. Replay MUST NOT
mutate canonical state, advance the canonical pointer, trigger side effects,
or introduce new authoritative transitions.

**This invariant ensures:**

- Tamper-evident canonical history
- Cross-implementation reproducibility
- Offline verification of enforcement semantics
- Deterministic auditability without runtime trust

**Compliance requirement:** A Polaris implementation MUST preserve sufficient
determinism in canonical encoding, validation binding, commit record
derivation, and replay-visible artifact structure to allow independent
recomputation of canonical progression.

---

## 8. Non-Bypassable Enforcement Boundary

The Polaris architecture establishes a non-bypassable enforcement boundary
such that no subsystem, interface, execution path, or external integration
can produce authoritative state advancement or side-effect authorization
except through the validated commit pathway and execution gate semantics.

Where implementations expose external interfaces, those interfaces MUST
remain subordinate to the same invariant-preserving control structure.

**This invariant prevents:**

- Alternate execution channels around the execution gate
- External integrations bypassing canonical state checks
- Implementation shortcuts that preserve behavior only under normal operation
- Hidden authority escalation through integration layers

**Compliance requirement:** A Polaris implementation MUST ensure that all
authoritative state mutation and all protected side-effect execution remain
inside invariant-preserving enforcement boundaries.

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

No invariant SHOULD be interpreted in isolation where doing so would weaken
the combined architecture.

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

Such variation is compliant only if the implementation continues to preserve
the full invariant set. Implementation flexibility does not authorize
invariant relaxation.

---

## Violation Semantics

A violation occurs when a system permits behavior inconsistent with one or
more Polaris invariants, including but not limited to:

- More than one authoritative successor state derivable from a single
  `canonical_pointer_ref` value
- Canonical advancement without a validation-pass result
- Canonical advancement outside commit authority
- Side effects authorized from uncommitted or stale state
- Multiple conflicting authoritative pointer interpretations
- Replay-visible outcomes that differ across compliant implementations for
  identical canonical evidence
- Alternate execution channels that bypass execution gate checks

A system exhibiting such behavior MUST NOT be described as Polaris-compliant.

---

## Minimal Compliance Statement

A system is Polaris-compliant with respect to architectural invariants only
if it:

1. Preserves a single authoritative canonical state progression.
2. Requires a deterministic validation-pass result before canonical
   advancement.
3. Restricts authoritative mutation to commit authority.
4. Binds side effects to `canonical_pointer_ref` equality at execution time.
5. Supports deterministic replay of canonical history across independent
   compliant implementations.

Partial compliance is not compliance.
