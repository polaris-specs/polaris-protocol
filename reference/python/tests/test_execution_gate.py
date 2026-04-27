"""
Tests for Invariant I3: Execution Causality Binding

execute(E, S_r) => S_r = S_n

The execution gate permits side effects only when the request
references the current canonical state. Stale references are
structurally rejected.
"""

import pytest
from polaris.commit import CommitAuthority
from polaris.crypto import generate_keypair
from polaris.gate import ExecutionGate, GateDecision, BlockReason
from polaris.psto import PSTO, Phase
from polaris.state import CanonicalHistory, state_hash


def make_system(validator_fn=None):
    """Helper: create a minimal Polaris system."""
    genesis = {"balance": 100, "version": 0}
    history = CanonicalHistory()
    genesis_h = state_hash(genesis)
    history._append(genesis, genesis_h)

    private_key, public_key = generate_keypair()
    authority = CommitAuthority(history, private_key, public_key,
                                 validator_fn)
    gate = ExecutionGate(history, authority)

    return history, authority, gate, genesis_h


# ─────────────────────────────────────────────
# I3 Core: stale state reference is rejected
# ─────────────────────────────────────────────

def test_execution_gate_rejects_stale_state_ref():
    """
    I3: A request referencing a prior state hash is rejected.

    This is the primary I3 test. After a commit advances the pointer,
    the old state hash is no longer current. Any execution attempt
    referencing the old hash must be blocked.
    """
    history, authority, gate, genesis_h = make_system()

    # Commit a transition — pointer advances from 0 to 1
    psto = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=genesis_h,
    )
    success, record = authority.commit(psto)
    assert success

    new_hash = history.current_hash
    assert new_hash != genesis_h

    # Execution request referencing the OLD (genesis) hash — must BLOCK
    result = gate.request_execution(psto.transition_id, genesis_h)

    assert result.decision == GateDecision.BLOCK
    assert result.block_reason == BlockReason.STALE_STATE_REFERENCE


def test_execution_gate_permits_current_state_ref():
    """
    I3: A request referencing the current canonical state is permitted.
    """
    history, authority, gate, genesis_h = make_system()

    psto = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=genesis_h,
    )
    success, record = authority.commit(psto)
    assert success

    current_hash = history.current_hash

    # Execution request referencing CURRENT hash — must PERMIT
    result = gate.request_execution(psto.transition_id, current_hash)

    assert result.decision == GateDecision.PERMIT
    assert result.block_reason is None


def test_execution_gate_blocks_without_commit():
    """
    I3: Execution without a committed transition is blocked.
    A PSTO that was never committed cannot authorize execution.
    """
    history, authority, gate, genesis_h = make_system()

    # Never committed — fabricated transition_id
    fake_transition_id = "00000000-0000-0000-0000-000000000000"

    result = gate.request_execution(fake_transition_id, genesis_h)

    assert result.decision == GateDecision.BLOCK
    assert result.block_reason == BlockReason.EXECUTION_WITHOUT_COMMIT


def test_execution_gate_blocks_after_second_commit():
    """
    I3: After a second commit, the first commit's state_ref
    is no longer current. Execution referencing it must be blocked.

    This tests that I3 is re-enforced after every pointer advance.
    """
    history, authority, gate, genesis_h = make_system()

    # First commit
    psto1 = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=genesis_h,
    )
    success1, _ = authority.commit(psto1)
    assert success1
    hash_after_first = history.current_hash

    # Second commit
    psto2 = PSTO(
        proposed_state={"balance": 80, "version": 2},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=hash_after_first,
    )
    success2, _ = authority.commit(psto2)
    assert success2

    # psto1's resulting state is now stale — must BLOCK
    result = gate.request_execution(psto1.transition_id, hash_after_first)
    assert result.decision == GateDecision.BLOCK
    assert result.block_reason == BlockReason.STALE_STATE_REFERENCE

    # psto2's resulting state is current — must PERMIT
    current_hash = history.current_hash
    result2 = gate.request_execution(psto2.transition_id, current_hash)
    assert result2.decision == GateDecision.PERMIT


def test_execution_gate_log_is_append_only():
    """Gate log records every evaluation and cannot be modified."""
    history, authority, gate, genesis_h = make_system()

    gate.request_execution("fake-id", genesis_h)
    gate.request_execution("fake-id-2", genesis_h)

    log = gate.log
    assert len(log) == 2

    # Modifying the returned log does not affect internal log
    log.clear()
    assert len(gate.log) == 2
