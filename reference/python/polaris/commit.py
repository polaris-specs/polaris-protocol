"""
polaris.commit
--------------
Commit Authority per Polaris spec Section D.

The commit authority is the sole component permitted to advance
the canonical pointer. Pointer advancement is atomic (CAS).

commit(T) = SUCCESS if T passes validation against current S_n
            and the pointer advances from n to n+1.
            FAIL otherwise (validation failure or pointer contention).
"""

import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

from polaris.crypto import sign_commit_payload, public_key_hex
from polaris.psto import PSTO, Phase, RejectionReason
from polaris.state import CanonicalHistory, state_hash, canonical_serialize
import hashlib


def _now_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + \
           f"{now.microsecond // 1000:03d}Z"


@dataclass
class CommitRecord:
    transition_id: str
    prev_state_hash: str
    resulting_state_hash: str
    sequence_number: int
    committed_at: str
    authority_identity: str
    signature: str
    validation_reference: dict


class CommitAuthority:
    """
    Single commit authority for one domain.

    Invariant I1: At most one successor per canonical state.
    Invariant I2: No commit without validation PASS.

    Uses a threading.Lock as the CAS linearization point.
    """

    def __init__(self, history: CanonicalHistory,
                 private_key, public_key,
                 validator_fn=None):
        self._history = history
        self._private_key = private_key
        self._public_key = public_key
        self._authority_identity = public_key_hex(public_key)
        self._validator_fn = validator_fn or (lambda state, psto: True)
        self._lock = threading.Lock()
        self._committed: dict = {}  # transition_id -> CommitRecord
        self._sequence = 0

    @property
    def authority_identity(self) -> str:
        return self._authority_identity

    def commit(self, psto: PSTO) -> Tuple[bool, Optional[CommitRecord]]:
        """
        Attempt to commit a PSTO.

        Returns (True, CommitRecord) on success.
        Returns (False, None) on failure — sets psto.phase to REJECTED.

        The lock is the linearization point (CAS equivalent).
        """
        # Duplicate check before lock
        if psto.transition_id in self._committed:
            psto.reject(RejectionReason.DUPLICATE_TRANSITION_ID)
            return False, None

        with self._lock:
            # Re-check duplicate inside lock
            if psto.transition_id in self._committed:
                psto.reject(RejectionReason.DUPLICATE_TRANSITION_ID)
                return False, None

            current_hash = self._history.current_hash
            current_state = self._history.current_state

            # I1: prev_state_hash must match current canonical state
            if psto.prev_state_hash != current_hash:
                psto.reject(RejectionReason.COMMIT_CONFLICT)
                return False, None

            # I2: validate against current canonical state
            valid = self._validator_fn(current_state, psto)
            if not valid:
                psto.reject(RejectionReason.VALIDATION_FAILED)
                return False, None

            # Advance pointer
            self._sequence += 1
            resulting = state_hash(psto.proposed_state)

            # Build commit payload for signing
            commit_payload = {
                "authority_identity": self._authority_identity,
                "committed_at": _now_iso(),
                "prev_state_hash": current_hash,
                "resulting_state_hash": resulting,
                "sequence_number": self._sequence,
                "transition_id": psto.transition_id,
                "validation_reference": {
                    "input_state_reference": current_hash,
                    "verdict": "PASS",
                },
            }

            signature = sign_commit_payload(self._private_key,
                                             commit_payload)

            record = CommitRecord(
                transition_id=psto.transition_id,
                prev_state_hash=current_hash,
                resulting_state_hash=resulting,
                sequence_number=self._sequence,
                committed_at=commit_payload["committed_at"],
                authority_identity=self._authority_identity,
                signature=signature,
                validation_reference=commit_payload["validation_reference"],
            )

            # Append to history (append-only)
            self._history._append(psto.proposed_state, resulting)

            # Update PSTO phase
            psto.phase = Phase.COMMITTED
            psto.commit_record = commit_payload
            psto.validation_verdict = {"verdict": "PASS",
                                        "input_state_reference": current_hash}

            self._committed[psto.transition_id] = record
            return True, record

    def get_commit_record(self, transition_id: str) \
            -> Optional[CommitRecord]:
        return self._committed.get(transition_id)
