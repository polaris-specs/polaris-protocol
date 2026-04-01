# Polaris Protocol

Polaris enforces a single invariant:

> No side effect may occur unless it is the result of a committed,
> validated transition — and that fact must be independently verifiable.

Execution authority is structurally bound to canonical state.
Enforced by construction, not policy.

---

## Problem

Distributed systems execute actions based on system state, yet no
widely deployed architecture structurally guarantees that those actions
originate from validated causal history.

Execution may occur from speculative or superseded state. State may
advance through multiple control paths. Logs may appear correct while
the causal chain between state, decision, and execution is not enforced.

Most systems cannot prove that execution originates from canonical state.

---

## Model

Polaris introduces commit-gated causality.

Every action follows a deterministic progression:

```
Proposed Transition
        ↓
Validator
        ↓
Commit Authority
        ↓
Canonical State
        ↓
Execution Gate
        ↓
Side Effects
```

If any step fails, execution does not occur.
No bypass path exists in a conformant implementation.

---

## What Polaris Is Not

**Not a blockchain.**
Does not implement consensus among mutually distrusting parties.
Assumes a designated commit authority.

**Not an audit log.**
Logs record what happened. Polaris structurally prevents unauthorized
execution before it occurs.

**Not a workflow engine.**
Does not orchestrate business logic or process flows.

**Not a policy engine.**
Does not evaluate arbitrary runtime policy.

**Not a runtime framework.**
This repository defines the specification, not an implementation.

---

## Specification

| Document | Purpose |
|---|---|
| `SPEC.md` | Complete normative specification v1.0 |
| `KNOWN-GAPS.md` | Acknowledged limitations deferred to v1.1 |
| `REFERENCE-HASHES.md` | Canonical reference hash values for implementers |

---

## Where to Start

**Implementing Polaris:**
Read `SPEC.md` Section A (Overview), then Section G (Transition Object),
then the section relevant to the component you are building.

**Verifying conformance:**
Read `SPEC.md` Section K for the self-declaration checklist
and PCIS-1 test specification.

**Understanding what Polaris guarantees:**
Read `SPEC.md` Section J (Threat Model).

**Checking your serialization:**
See `REFERENCE-HASHES.md` for canonical reference hash values.

---

## Status

```
Version:    1.0
License:    Specification — CC-BY-4.0
            Reference implementations — Apache 2.0
Conformance: Self-declared (Level 1). PCIS-1 suite in development.
```

Implementations are invited.
Questions and errata: open an issue tagged [conformance] or [errata].
