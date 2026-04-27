"""
polaris.psto
------------
Proposed State Transition Object (PSTO).

A PSTO carries:
- a reference to the state it acts upon (prev_state_hash)
- the proposed next state
- a payload for validation

Phase lifecycle: PROPOSED → VALIDATED → COMMITTED → EXECUTED
                                      → REJECTED
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class Phase(Enum):
    PROPOSED = "PROPOSED"
    VALIDATED = "VALIDATED"
    COMMITTED = "COMMITTED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"


class RejectionReason(Enum):
    SCHEMA_INVALID = "SCHEMA_INVALID"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    COMMIT_CONFLICT = "COMMIT_CONFLICT"
    REVALIDATION_FAILED = "REVALIDATION_FAILED"
    DOMAIN_SUSPENDED = "DOMAIN_SUSPENDED"
    INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"
    DUPLICATE_TRANSITION_ID = "DUPLICATE_TRANSITION_ID"


@dataclass
class PSTO:
    """
    Proposed State Transition Object.

    prev_state_hash must reference the current canonical state hash
    at proposal time. If canonical state changes before commit,
    the PSTO must be re-validated.
    """
    proposed_state: dict
    payload: dict
    prev_state_hash: str
    transition_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.") +
        f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    )
    phase: Phase = Phase.PROPOSED
    validation_verdict: Optional[dict] = None
    commit_record: Optional[dict] = None
    execution_record: Optional[dict] = None
    rejection_reason: Optional[RejectionReason] = None

    def reject(self, reason: RejectionReason) -> None:
        self.phase = Phase.REJECTED
        self.rejection_reason = reason
