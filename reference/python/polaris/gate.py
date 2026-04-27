"""
polaris.gate
------------
Execution Gate per Polaris spec Section I.

Invariant I3:
  execute(E, S_r) => S_r = S_n

The gate performs three checks in order:
  1. Commit exists for this transition_id
  2. transition_id matches the commit record
  3. state_ref equals the current canonical state hash

PERMIT requires all three. A single failure blocks execution.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from polaris.commit import CommitAuthority, CommitRecord
from polaris.state import CanonicalHistory


class GateDecision(Enum):
    PERMIT = "PERMIT"
    BLOCK = "BLOCK"


class BlockReason(Enum):
    EXECUTION_WITHOUT_COMMIT = "EXECUTION_WITHOUT_COMMIT"
    TRANSITION_MISMATCH = "TRANSITION_MISMATCH"
    DOMAIN_NOT_ACTIVE = "DOMAIN_NOT_ACTIVE"
    STALE_STATE_REFERENCE = "STALE_STATE_REFERENCE"


@dataclass
class GateResult:
    decision: GateDecision
    transition_id: str
    state_ref: str
    block_reason: Optional[BlockReason] = None
    evaluated_at: str = ""

    def __post_init__(self):
        if not self.evaluated_at:
            now = datetime.now(timezone.utc)
            self.evaluated_at = now.strftime("%Y-%m-%dT%H:%M:%S.") + \
                                 f"{now.microsecond // 1000:03d}Z"

    @property
    def permitted(self) -> bool:
        return self.decision == GateDecision.PERMIT


class ExecutionGate:
    """
    Enforces I3: execution is permitted only when the execution
    request references the current canonical state pointer.

    The gate is the authoritative enforcement point.
    It does not validate. It does not advance canonical state.
    """

    def __init__(self, history: CanonicalHistory,
                 commit_authority: CommitAuthority):
        self._history = history
        self._authority = commit_authority
        self._log: list = []

    def request_execution(self, transition_id: str,
                          state_ref: str) -> GateResult:
        """
        Request execution for a committed transition.

        transition_id: the committed transition authorizing this execution
        state_ref: the canonical state hash the caller believes is current

        Returns GateResult with PERMIT or BLOCK.
        """

        # Check 1: commit exists
        record: Optional[CommitRecord] = \
            self._authority.get_commit_record(transition_id)
        if record is None:
            result = GateResult(
                decision=GateDecision.BLOCK,
                transition_id=transition_id,
                state_ref=state_ref,
                block_reason=BlockReason.EXECUTION_WITHOUT_COMMIT,
            )
            self._log.append(result)
            return result

        # Check 2: transition_id matches commit record
        if record.transition_id != transition_id:
            result = GateResult(
                decision=GateDecision.BLOCK,
                transition_id=transition_id,
                state_ref=state_ref,
                block_reason=BlockReason.TRANSITION_MISMATCH,
            )
            self._log.append(result)
            return result

        # Check 3: state_ref must equal CURRENT canonical state hash
        # This is I3 — the gate enforcement point
        current_hash = self._history.current_hash
        if state_ref != current_hash:
            result = GateResult(
                decision=GateDecision.BLOCK,
                transition_id=transition_id,
                state_ref=state_ref,
                block_reason=BlockReason.STALE_STATE_REFERENCE,
            )
            self._log.append(result)
            return result

        # All checks passed — PERMIT
        result = GateResult(
            decision=GateDecision.PERMIT,
            transition_id=transition_id,
            state_ref=state_ref,
        )
        self._log.append(result)
        return result

    @property
    def log(self) -> list:
        """Append-only gate evaluation log."""
        return list(self._log)
