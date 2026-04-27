# Polaris Reference Harness

Executable conformance harness for the [Polaris Protocol](https://github.com/polaris-specs/polaris-protocol).

This is not a production implementation. It is a testable truth: every invariant in the protocol either passes or fails deterministically.

---

## What this proves

Each test proves exactly one invariant:

| Test | Invariant |
|---|---|
| `test_execution_gate_rejects_stale_state_ref` | **I3** — stale state reference is blocked |
| `test_execution_gate_permits_current_state_ref` | **I3** — current state reference is permitted |
| `test_execution_gate_blocks_without_commit` | **I3** — no execution without commit |
| `test_execution_gate_blocks_after_second_commit` | **I3** — pointer advance invalidates prior refs |
| `test_i1_concurrent_fork_rejected` | **I1** — at most one successor per canonical state |
| `test_i2_validation_failure_blocks_commit` | **I2** — no commit without validation pass |
| `test_tampered_state_detected` | **I1+I2** — hash chain break detected |
| `test_missing_transition_detected` | **I1** — sequence gap detected |
| `test_valid_proof_verifies` | **CausalChainProof** — valid proof verifies |
| `test_tampered_proof_fails_verification` | **CausalChainProof** — tampered proof rejected |

---

## Causal Chain Proof

Every permitted effect can emit a compact proof binding it to:
- the committed transition that authorized it,
- the canonical state it descended from,
- the commit authority signature.

If the proof cannot be verified, the effect is excluded.

```python
from polaris.proof import build_proof, verify_causal_chain_proof

proof = build_proof("effect-001", psto.transition_id, authority)
verified = verify_causal_chain_proof(proof, authority, public_key)
```

---

## Run

```bash
pip install cryptography pytest
python -m pytest tests/ -v
```

---

## Structure

```
polaris/
  state.py      # Canonical state and history
  psto.py       # Proposed State Transition Object
  crypto.py     # Ed25519 signing and verification
  commit.py     # Commit authority
  gate.py       # Execution gate (I3)
  proof.py      # CausalChainProof
  replay.py     # Deterministic replay verification
tests/
  test_execution_gate.py    # I3
  test_invariants.py        # I1, I2
  test_replay.py            # Tamper detection
  test_causal_chain_proof.py
```

---

## Specification

- Normative spec: [SPEC.md](https://github.com/polaris-specs/polaris-protocol)
- Minimal conformance: [QUICKSTART.md](https://github.com/polaris-specs/polaris-protocol/blob/main/QUICKSTART.md)
- Technical report: [POLARIS-TR-2026-001 v0.5](https://zenodo.org/records/19669105)
