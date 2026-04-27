"""
Tests for replay verification and tamper detection.

A valid chain replays identically.
A tampered chain fails deterministically.
"""

import pytest
from polaris.replay import ReplayRecord, verify_replay
from polaris.state import state_hash


def make_chain(n_transitions: int):
    """Build a valid chain of n transitions."""
    genesis = {"balance": 100, "version": 0}
    genesis_h = state_hash(genesis)

    records = []
    current_state = genesis
    current_hash = genesis_h

    for i in range(1, n_transitions + 1):
        next_state = {"balance": 100 - i * 10, "version": i}
        next_hash = state_hash(next_state)
        records.append(ReplayRecord(
            sequence_number=i,
            transition_id=f"tid-{i}",
            prev_state_hash=current_hash,
            resulting_state_hash=next_hash,
            proposed_state=next_state,
        ))
        current_state = next_state
        current_hash = next_hash

    return genesis, genesis_h, records, current_hash


def test_valid_chain_replays():
    """A valid chain passes replay verification."""
    genesis, genesis_h, records, live_hash = make_chain(3)

    result = verify_replay(genesis, genesis_h, records, live_hash)

    assert result.valid is True
    assert result.verified_transitions == 3
    assert result.failure_reason is None


def test_tampered_state_detected():
    """
    A tampered proposed_state breaks the hash chain.
    Replay must detect it deterministically.
    """
    genesis, genesis_h, records, live_hash = make_chain(3)

    # Tamper with record 2
    original = records[1]
    tampered_state = dict(original.proposed_state)
    tampered_state["balance"] = 9999  # tampered
    records[1] = ReplayRecord(
        sequence_number=original.sequence_number,
        transition_id=original.transition_id,
        prev_state_hash=original.prev_state_hash,
        resulting_state_hash=original.resulting_state_hash,  # unchanged
        proposed_state=tampered_state,  # tampered
    )

    result = verify_replay(genesis, genesis_h, records, live_hash)

    assert result.valid is False
    assert result.failure_at_sequence == 2
    assert "Tampered" in result.failure_reason


def test_missing_transition_detected():
    """A gap in sequence_number fails replay."""
    genesis, genesis_h, records, live_hash = make_chain(3)

    # Remove record 2 (sequence 2)
    records_with_gap = [records[0], records[2]]

    result = verify_replay(genesis, genesis_h, records_with_gap, live_hash)

    assert result.valid is False
    assert "gap" in result.failure_reason.lower()


def test_empty_chain_valid():
    """A chain with no transitions is valid if live hash equals genesis."""
    genesis = {"balance": 100, "version": 0}
    genesis_h = state_hash(genesis)

    result = verify_replay(genesis, genesis_h, [], genesis_h)

    assert result.valid is True
    assert result.verified_transitions == 0


def test_genesis_hash_tamper_detected():
    """A tampered genesis hash fails immediately."""
    genesis = {"balance": 100, "version": 0}
    genesis_h = state_hash(genesis)
    wrong_genesis_h = "a" * 64  # wrong hash

    result = verify_replay(genesis, wrong_genesis_h, [], genesis_h)

    assert result.valid is False
    assert "Genesis" in result.failure_reason
