"""
polaris.proof
-------------
CausalChainProof

A compact, verifiable record that a side effect was permitted
only because it descended from a committed, validated transition
in the canonical history.

This is not a receipt for "effect succeeded".
It is a receipt for: effect was structurally authorized to occur.

Verification (v0.1):
  1. commit_record_hash exists in canonical history
  2. signature verifies against commit authority public key
  3. prev_state_hash matches the commit record
  4. state_ref matches resulting_state_hash of commit record
"""

import hashlib
from dataclasses import dataclass
from typing import Optional

from polaris.commit import CommitAuthority, CommitRecord
from polaris.crypto import verify_commit_signature
from polaris.state import canonical_serialize


@dataclass(frozen=True)
class CausalChainProof:
    effect_id: str           # identifier of the side effect
    transition_id: str       # the committed transition that authorized it
    state_ref: str           # resulting_state_hash of the commit record
    prev_state_hash: str     # prev_state_hash of the commit record
    commit_record_hash: str  # SHA-256 of canonical commit payload
    authority_identity: str  # public key hex of commit authority
    signature: str           # Ed25519 signature from commit record


def build_proof(effect_id: str,
                transition_id: str,
                commit_authority: CommitAuthority) \
        -> Optional[CausalChainProof]:
    """
    Build a CausalChainProof for a given effect and transition.
    Returns None if the transition has not been committed.
    """
    record: Optional[CommitRecord] = \
        commit_authority.get_commit_record(transition_id)
    if record is None:
        return None

    # Reconstruct commit payload for hashing
    commit_payload = {
        "authority_identity": record.authority_identity,
        "committed_at": record.committed_at,
        "prev_state_hash": record.prev_state_hash,
        "resulting_state_hash": record.resulting_state_hash,
        "sequence_number": record.sequence_number,
        "transition_id": record.transition_id,
        "validation_reference": record.validation_reference,
    }
    payload_bytes = canonical_serialize(commit_payload)
    commit_record_hash = hashlib.sha256(payload_bytes).hexdigest()

    return CausalChainProof(
        effect_id=effect_id,
        transition_id=transition_id,
        state_ref=record.resulting_state_hash,
        prev_state_hash=record.prev_state_hash,
        commit_record_hash=commit_record_hash,
        authority_identity=record.authority_identity,
        signature=record.signature,
    )


def verify_causal_chain_proof(proof: CausalChainProof,
                               commit_authority: CommitAuthority,
                               public_key) -> bool:
    """
    Verify a CausalChainProof.

    Checks:
      1. commit record exists in authority
      2. signature verifies against public key
      3. prev_state_hash matches commit record
      4. state_ref matches resulting_state_hash
    """
    record: Optional[CommitRecord] = \
        commit_authority.get_commit_record(proof.transition_id)
    if record is None:
        return False

    # Reconstruct commit payload for signature verification
    commit_payload = {
        "authority_identity": record.authority_identity,
        "committed_at": record.committed_at,
        "prev_state_hash": record.prev_state_hash,
        "resulting_state_hash": record.resulting_state_hash,
        "sequence_number": record.sequence_number,
        "transition_id": record.transition_id,
        "validation_reference": record.validation_reference,
    }

    if not verify_commit_signature(public_key, commit_payload,
                                    proof.signature):
        return False

    if proof.prev_state_hash != record.prev_state_hash:
        return False

    if proof.state_ref != record.resulting_state_hash:
        return False

    return True
