"""
polaris.replay
--------------
Deterministic replay verification per Polaris spec Section H.7.

Given the committed sequence H = (S_0, S_1, ..., S_n),
any conformant verifier applying the same validation function V
from the same genesis state S_0 reconstructs identical canonical state.

Replay verification:
  Step 1: Verify genesis_hash
  Step 2: For each transition in order:
    - sequence_number is contiguous
    - prev_state_hash matches prior resulting_state_hash
    - resulting_state_hash matches SHA-256 of proposed_state
  Step 3: Final state matches live canonical state

A tampered record breaks the hash chain and fails verification.
"""

import hashlib
from dataclasses import dataclass
from typing import List, Optional

from polaris.state import canonical_serialize, state_hash


@dataclass
class ReplayRecord:
    """Minimal record needed for replay verification."""
    sequence_number: int
    transition_id: str
    prev_state_hash: str
    resulting_state_hash: str
    proposed_state: dict


@dataclass
class ReplayResult:
    valid: bool
    verified_transitions: int
    failure_reason: Optional[str] = None
    failure_at_sequence: Optional[int] = None


def verify_replay(genesis_state: dict,
                  genesis_hash: str,
                  records: List[ReplayRecord],
                  live_canonical_hash: str) -> ReplayResult:
    """
    Replay the canonical history from genesis and verify integrity.

    Detects:
    - Tampered proposed_state (hash chain break)
    - Missing transitions (sequence gap)
    - Final state mismatch
    """
    # Step 1: Verify genesis hash
    computed_genesis = state_hash(genesis_state)
    if computed_genesis != genesis_hash:
        return ReplayResult(
            valid=False,
            verified_transitions=0,
            failure_reason="Genesis hash mismatch",
            failure_at_sequence=0,
        )

    if not records:
        # No transitions — final hash must equal genesis hash
        if genesis_hash != live_canonical_hash:
            return ReplayResult(
                valid=False,
                verified_transitions=0,
                failure_reason="No transitions but live hash differs "
                               "from genesis",
            )
        return ReplayResult(valid=True, verified_transitions=0)

    # Step 2: Walk the chain
    expected_sequence = 1
    current_hash = genesis_hash

    for record in records:
        # Sequence must be contiguous
        if record.sequence_number != expected_sequence:
            return ReplayResult(
                valid=False,
                verified_transitions=expected_sequence - 1,
                failure_reason=f"Sequence gap: expected "
                               f"{expected_sequence}, "
                               f"got {record.sequence_number}",
                failure_at_sequence=record.sequence_number,
            )

        # prev_state_hash must match prior resulting_state_hash
        if record.prev_state_hash != current_hash:
            return ReplayResult(
                valid=False,
                verified_transitions=expected_sequence - 1,
                failure_reason=f"Hash chain break at sequence "
                               f"{record.sequence_number}: "
                               f"prev_state_hash mismatch",
                failure_at_sequence=record.sequence_number,
            )

        # resulting_state_hash must match SHA-256 of proposed_state
        computed = state_hash(record.proposed_state)
        if computed != record.resulting_state_hash:
            return ReplayResult(
                valid=False,
                verified_transitions=expected_sequence - 1,
                failure_reason=f"Tampered state at sequence "
                               f"{record.sequence_number}: "
                               f"resulting_state_hash mismatch",
                failure_at_sequence=record.sequence_number,
            )

        current_hash = record.resulting_state_hash
        expected_sequence += 1

    # Step 3: Final hash must match live canonical state
    if current_hash != live_canonical_hash:
        return ReplayResult(
            valid=False,
            verified_transitions=expected_sequence - 1,
            failure_reason="Final replay hash does not match "
                           "live canonical state",
        )

    return ReplayResult(
        valid=True,
        verified_transitions=len(records),
    )
