"""Polaris Reference Harness — structural rejection demo.

Three independent failures, each on a fresh system:
  1. Tampered record at sequence 2 — replay fails at that index.
  2. Stale state_ref at the gate — execution blocked.
  3. Unknown transition_id at the gate — execution blocked.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polaris.commit import CommitAuthority
from polaris.crypto import generate_keypair
from polaris.gate import BlockReason, ExecutionGate, GateDecision
from polaris.psto import PSTO
from polaris.replay import ReplayRecord, verify_replay
from polaris.state import CanonicalHistory, state_hash


def make_system():
    genesis = {"balance": 1000, "version": 0}
    history = CanonicalHistory()
    genesis_h = state_hash(genesis)
    history._append(genesis, genesis_h)
    private_key, public_key = generate_keypair()
    authority = CommitAuthority(history, private_key, public_key)
    gate = ExecutionGate(history, authority)
    return history, authority, gate, genesis, genesis_h


def commit_chain(history, authority, genesis_h, states):
    records = []
    prev_hash = genesis_h
    for state in states:
        psto = PSTO(proposed_state=state, payload={}, prev_state_hash=prev_hash)
        ok, record = authority.commit(psto)
        if not ok:
            return None
        records.append(ReplayRecord(
            sequence_number=record.sequence_number,
            transition_id=record.transition_id,
            prev_state_hash=record.prev_state_hash,
            resulting_state_hash=record.resulting_state_hash,
            proposed_state=state,
        ))
        prev_hash = record.resulting_state_hash
    return records


def main() -> int:
    states = [
        {"balance": 900, "version": 1},
        {"balance": 800, "version": 2},
        {"balance": 700, "version": 3},
    ]

    # 1. Tampered record at sequence 2.
    history, authority, _, genesis, genesis_h = make_system()
    records = commit_chain(history, authority, genesis_h, states)
    if records is None:
        return 1
    original = records[1]
    tampered = dict(original.proposed_state)
    tampered["balance"] = 9999
    records[1] = ReplayRecord(
        sequence_number=original.sequence_number,
        transition_id=original.transition_id,
        prev_state_hash=original.prev_state_hash,
        resulting_state_hash=original.resulting_state_hash,
        proposed_state=tampered,
    )
    replay = verify_replay(genesis, genesis_h, records, history.current_hash)
    if replay.valid or replay.failure_at_sequence != 2:
        return 1
    print(f"[FAIL]   tampered record detected at sequence {replay.failure_at_sequence}")

    # 2. Stale state_ref at the gate.
    history, authority, gate, _, genesis_h = make_system()
    psto1 = PSTO(proposed_state=states[0], payload={}, prev_state_hash=genesis_h)
    ok1, _ = authority.commit(psto1)
    if not ok1:
        return 1
    stale_hash = history.current_hash
    psto2 = PSTO(proposed_state=states[1], payload={}, prev_state_hash=stale_hash)
    ok2, _ = authority.commit(psto2)
    if not ok2:
        return 1
    result = gate.request_execution(psto1.transition_id, stale_hash)
    if (result.decision != GateDecision.BLOCK
            or result.block_reason != BlockReason.STALE_STATE_REFERENCE):
        return 1
    print("[REJECT] execution from stale state_ref")

    # 3. Unknown transition_id at the gate.
    _, _, gate, _, genesis_h = make_system()
    result = gate.request_execution("fabricated-transition-id", genesis_h)
    if (result.decision != GateDecision.BLOCK
            or result.block_reason != BlockReason.EXECUTION_WITHOUT_COMMIT):
        return 1
    print("[REJECT] execution without commit")

    return 0


if __name__ == "__main__":
    sys.exit(main())
