"""
Tests for Invariant I1 and I2.

I1: successor(S_n) is a partial function — at most one successor.
I2: commit(T) => V(T) = PASS — no commit without validation pass.
"""

import pytest
from polaris.commit import CommitAuthority
from polaris.crypto import generate_keypair
from polaris.gate import ExecutionGate
from polaris.psto import PSTO, Phase, RejectionReason
from polaris.state import CanonicalHistory, state_hash


def make_system(validator_fn=None):
    genesis = {"balance": 100, "version": 0}
    history = CanonicalHistory()
    genesis_h = state_hash(genesis)
    history._append(genesis, genesis_h)
    private_key, public_key = generate_keypair()
    authority = CommitAuthority(history, private_key, public_key,
                                 validator_fn)
    return history, authority, genesis_h


def test_i1_concurrent_fork_rejected():
    """
    I1: Two PSTOs with identical prev_state_hash — only one commits.
    The second is rejected with COMMIT_CONFLICT.
    """
    history, authority, genesis_h = make_system()

    psto1 = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=genesis_h,
    )
    psto2 = PSTO(
        proposed_state={"balance": 95, "version": 1},
        payload={"action": "debit", "amount": 5},
        prev_state_hash=genesis_h,
    )

    success1, _ = authority.commit(psto1)
    success2, _ = authority.commit(psto2)

    assert success1 is True
    assert success2 is False
    assert psto2.phase == Phase.REJECTED
    assert psto2.rejection_reason == RejectionReason.COMMIT_CONFLICT


def test_i2_validation_failure_blocks_commit():
    """
    I2: A PSTO that fails validation is not committed.
    """
    def strict_validator(state, psto):
        # Only allow debits of exactly 10
        return psto.payload.get("amount") == 10

    history, authority, genesis_h = make_system(strict_validator)

    psto = PSTO(
        proposed_state={"balance": 95, "version": 1},
        payload={"action": "debit", "amount": 5},  # fails validation
        prev_state_hash=genesis_h,
    )

    success, _ = authority.commit(psto)

    assert success is False
    assert psto.phase == Phase.REJECTED
    assert psto.rejection_reason == RejectionReason.VALIDATION_FAILED
    # Canonical state must not have advanced
    assert history.n == 0
    assert history.current_hash == genesis_h


def test_i2_valid_transition_commits():
    """
    I2: A PSTO that passes validation is committed.
    """
    def strict_validator(state, psto):
        return psto.payload.get("amount") == 10

    history, authority, genesis_h = make_system(strict_validator)

    psto = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},  # passes validation
        prev_state_hash=genesis_h,
    )

    success, record = authority.commit(psto)

    assert success is True
    assert psto.phase == Phase.COMMITTED
    assert history.n == 1
    assert history.current_hash != genesis_h


def test_duplicate_transition_id_rejected():
    """
    Duplicate transition_id is rejected without advancing state.
    """
    history, authority, genesis_h = make_system()

    psto = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={},
        prev_state_hash=genesis_h,
    )
    success1, _ = authority.commit(psto)
    assert success1

    # Same transition_id — must be rejected
    psto_dup = PSTO(
        proposed_state={"balance": 80, "version": 2},
        payload={},
        prev_state_hash=history.current_hash,
    )
    psto_dup.transition_id = psto.transition_id  # force duplicate

    success2, _ = authority.commit(psto_dup)
    assert success2 is False
    assert psto_dup.rejection_reason == RejectionReason.DUPLICATE_TRANSITION_ID
