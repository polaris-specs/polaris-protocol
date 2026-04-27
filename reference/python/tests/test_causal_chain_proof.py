"""
Tests for CausalChainProof.

Every permitted effect can emit a compact proof binding it to
the committed transition that authorized it.

If the proof cannot be verified, the effect is excluded.
"""

import pytest
from polaris.commit import CommitAuthority
from polaris.crypto import generate_keypair
from polaris.proof import build_proof, verify_causal_chain_proof
from polaris.psto import PSTO
from polaris.state import CanonicalHistory, state_hash


def make_committed_system():
    genesis = {"balance": 100, "version": 0}
    history = CanonicalHistory()
    genesis_h = state_hash(genesis)
    history._append(genesis, genesis_h)

    private_key, public_key = generate_keypair()
    authority = CommitAuthority(history, private_key, public_key)

    psto = PSTO(
        proposed_state={"balance": 90, "version": 1},
        payload={"action": "debit", "amount": 10},
        prev_state_hash=genesis_h,
    )
    authority.commit(psto)

    return authority, public_key, psto


def test_valid_proof_verifies():
    """A proof built from a committed transition verifies correctly."""
    authority, public_key, psto = make_committed_system()

    proof = build_proof("effect-001", psto.transition_id, authority)

    assert proof is not None
    assert verify_causal_chain_proof(proof, authority, public_key) is True


def test_proof_fails_for_uncommitted_transition():
    """No proof can be built for an uncommitted transition."""
    authority, public_key, psto = make_committed_system()

    proof = build_proof("effect-001", "nonexistent-transition-id",
                        authority)

    assert proof is None


def test_tampered_proof_fails_verification():
    """A proof with a tampered state_ref fails verification."""
    from dataclasses import replace
    authority, public_key, psto = make_committed_system()

    proof = build_proof("effect-001", psto.transition_id, authority)
    assert proof is not None

    # Tamper with state_ref
    tampered = CausalChainProof_replace(proof, state_ref="a" * 64)

    assert verify_causal_chain_proof(tampered, authority, public_key) \
           is False


def CausalChainProof_replace(proof, **kwargs):
    """Helper to create modified proof (frozen dataclass)."""
    from polaris.proof import CausalChainProof
    d = {
        "effect_id": proof.effect_id,
        "transition_id": proof.transition_id,
        "state_ref": proof.state_ref,
        "prev_state_hash": proof.prev_state_hash,
        "commit_record_hash": proof.commit_record_hash,
        "authority_identity": proof.authority_identity,
        "signature": proof.signature,
    }
    d.update(kwargs)
    return CausalChainProof(**d)
