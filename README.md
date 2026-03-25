# Polaris

Polaris enforces a single invariant:

Side effects cannot occur except as a consequence of a validated, committed canonical state transition.

Execution authority is structurally bound to canonical state — enforced by construction, not policy.


## Problem

Distributed systems execute actions based on system state, yet few architectures guarantee that those actions originate from validated causal history.

Execution may occur from speculative or superseded state. State may advance through multiple control paths. Logs may appear correct while the causal chain between state, decision, and execution is not enforced.

Most systems cannot prove that execution originates from canonical state.


## Model

Polaris introduces commit-gated causality.

Execution is permitted only from canonical state established through validated commit progression.

Execution rights are granted by canonical state identity, not by policy or recording.


## Execution Flow

Every action follows a deterministic progression:

Proposed Transition (PSTO)
↓
Validation Pipeline
↓
Commit Authority
↓
Canonical State Pointer
↓
Execution Gate
↓
Side Effects

If any step fails, execution does not occur.


## What Polaris Is

Polaris is a constraint system over execution.

It enforces:

- deterministic state progression
- canonical state authority
- validation before commitment
- execution bound to canonical state
- deterministic replay and verification

Correctness is derived from structure, not from trusted execution.


## Non-Goals

Polaris is intentionally narrow in scope.

Not a blockchain
Does not implement consensus, tokens, or a decentralized ledger.

Not a logging system
Logs record events. Polaris constrains whether events can occur.

Not a workflow engine
Does not orchestrate business logic or process flows.

Not a policy engine
Does not evaluate arbitrary runtime policy.

Not a runtime framework
This repository defines the specification, not an implementation.


## Specification

The protocol is defined normatively in `spec/`.

```
spec/
├── invariants.md
├── canonical_encoding.md
├── execution_graph.md
├── verification_model.md
└── schemas/
    └── event.schema.json
```

Implementations must preserve the invariants and encoding rules defined in these documents.


## Status

Version: 1.0.0
Status: Initial normative release

The specification is the reference.

Implementations are invited.


## Where to Start

- `spec/invariants.md`
- `spec/canonical_encoding.md`
- `spec/execution_graph.md`
- `spec/verification_model.md`
- `spec/schemas/event.schema.json`


## Security

Security issues or specification ambiguities should be reported according to `SECURITY.md`.


## License

MIT — see `LICENSE`.


Pat.: https://polaris-protocol.org/patents
