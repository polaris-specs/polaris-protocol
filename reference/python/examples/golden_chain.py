"""Polaris Reference Harness — golden chain demo.

Builds genesis + 3 commits, replays from genesis, and exercises the
execution gate at the current canonical state. Prints exactly one line
on success.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polaris.commit import CommitAuthority
from polaris.crypto import generate_keypair
from polaris.gate import ExecutionGate, GateDecision
from polaris.psto import PSTO
from polaris.replay import ReplayRecord, verify_replay
from polaris.state import CanonicalHistory, state_hash


def main() -> int:
    genesis = {"balance": 1000, "version": 0}
    history = CanonicalHistory()
    genesis_h = state_hash(genesis)
    history._append(genesis, genesis_h)

    private_key, public_key = generate_keypair()
    authority = CommitAuthority(history, private_key, public_key)
    gate = ExecutionGate(history, authority)

    states = [
        {"balance": 900, "version": 1},
        {"balance": 800, "version": 2},
        {"balance": 700, "version": 3},
    ]

    records = []
    last_psto = None
    prev_hash = genesis_h
    for state in states:
        psto = PSTO(proposed_state=state, payload={}, prev_state_hash=prev_hash)
        ok, record = authority.commit(psto)
        if not ok:
            return 1
        records.append(ReplayRecord(
            sequence_number=record.sequence_number,
            transition_id=record.transition_id,
            prev_state_hash=record.prev_state_hash,
            resulting_state_hash=record.resulting_state_hash,
            proposed_state=state,
        ))
        prev_hash = record.resulting_state_hash
        last_psto = psto

    replay = verify_replay(genesis, genesis_h, records, history.current_hash)
    if not replay.valid or replay.verified_transitions != len(states):
        return 1

    result = gate.request_execution(last_psto.transition_id, history.current_hash)
    if result.decision != GateDecision.PERMIT:
        return 1

    print("[PASS] valid chain verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
