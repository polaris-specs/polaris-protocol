# Polaris

**Polaris is a protocol that ensures system actions can only occur as consequences of validated canonical state transitions.**

Polaris introduces a deterministic control layer for computing systems where actions cannot occur unless they are derived from validated, committed canonical state. Instead of relying on logs, audits, or after-the-fact policy evaluation, Polaris enforces causal integrity structurally.

In a Polaris system, execution is not trusted because it was recorded. Execution is trusted because it can only occur as a consequence of canonical state progression.

---

## The Problem

AI agents act. They call APIs, modify infrastructure, move funds, trigger workflows, and interact with real-world systems.

Today there is no structural guarantee that those actions emerged from validated, authorized system state. Actions may occur from speculative or superseded state. Logs can be rewritten. State can be mutated outside controlled pathways. Execution may occur before correctness is established.

There is no widely adopted protocol that ensures otherwise.

---

## Core Principle

Polaris enforces a single invariant:

```
No side effect may occur except as a consequence of a validated, committed canonical state transition.
```

Every action in a Polaris system must follow this progression:

```
Proposed Transition (PSTO)
        |
        v
Validation Pipeline
        |
        v
Commit Authority
        |
        v
Canonical State Pointer
        |
        v
Execution Gate
        |
        v
Side Effects
```

A transition must pass validation before it can be committed. A commit must advance the canonical state pointer. Execution requests must reference the canonical pointer at evaluation time. If any step fails, the action is rejected before execution occurs.

---

## What Polaris Is

Polaris functions as a deterministic control plane for state mutation and execution.

It enforces:

- Deterministic state progression
- Canonical state authority
- Validation before mutation
- Execution bound to canonical state
- Deterministic replay and verification

These properties allow system behavior to be verified from canonical state history rather than inferred from logs.

---

## Non-Goals

Polaris is intentionally narrow in scope.

**Not a blockchain.** Polaris does not implement a decentralized ledger, token system, or consensus network. It maintains canonical state progression to enforce execution causality, not global consensus.

**Not a logging system.** Logs record events after they occur. Polaris ensures events cannot occur unless they originate from validated canonical state.

**Not a workflow engine.** Polaris does not orchestrate business workflows. It enforces the conditions under which authoritative state transitions and execution may occur.

**Not a policy engine.** Polaris does not evaluate arbitrary runtime policy. It enforces deterministic validation gates bound to canonical state transitions.

**Not a runtime framework.** This repository defines the protocol specification, not a runtime implementation. Implementations may vary in language or architecture provided they preserve the normative invariants.

---

## Repository Structure

```
spec/
├── canonical_encoding.md
├── invariants.md
├── execution_graph.md
├── verification_model.md
└── schemas/
    └── event.schema.json
```

| File | Purpose |
|---|---|
| `canonical_encoding.md` | Deterministic encoding rules for transitions |
| `invariants.md` | Architectural invariants all implementations must preserve |
| `execution_graph.md` | Authoritative state progression and execution gating |
| `verification_model.md` | Deterministic replay and independent verification |
| `event.schema.json` | Machine-readable schema for protocol events |

---

## Protocol Status

**Version:** 1.0.0
**Status:** Initial normative release

The documents in `spec/` are normative. Field names, encoding rules, invariant definitions, and verification procedures defined in these files form the canonical Polaris protocol specification.

Changes to normative behavior require a version increment.

---

## Where to Start

1. `spec/invariants.md`
2. `spec/canonical_encoding.md`
3. `spec/execution_graph.md`
4. `spec/verification_model.md`
5. `spec/schemas/event.schema.json`

---

## Security

Security vulnerabilities or specification ambiguities should be reported according to `SECURITY.md`.

---

## License

MIT — see `LICENSE`.
