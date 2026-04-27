"""
polaris.crypto
--------------
Cryptographic integrity per Polaris spec Section F.

Signing:
  digest = SHA-256(canonical_JSON_serialize(commit_payload))
  signature = Ed25519_sign(private_key, digest_bytes)

Verification:
  Ed25519_verify(public_key, digest_bytes, signature)

Key format: raw bytes (32 bytes public, 32 bytes private seed).
"""

import hashlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)

from polaris.state import canonical_serialize


def generate_keypair():
    """Generate Ed25519 keypair. Returns (private_key, public_key)."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def public_key_hex(public_key: Ed25519PublicKey) -> str:
    """Encode public key as lowercase hex per Section F.7.1."""
    raw = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
    return raw.hex()


def sign_commit_payload(private_key: Ed25519PrivateKey,
                        commit_payload: dict) -> str:
    """
    Sign commit payload per Section F.6.1:
    1. Canonical JSON serialize the payload
    2. SHA-256 digest (raw 32 bytes)
    3. Ed25519 sign the digest bytes
    Returns hex-encoded signature.
    """
    serialized = canonical_serialize(commit_payload)
    digest = hashlib.sha256(serialized).digest()  # raw bytes, not hex
    signature_bytes = private_key.sign(digest)
    return signature_bytes.hex()


def verify_commit_signature(public_key: Ed25519PublicKey,
                             commit_payload: dict,
                             signature_hex: str) -> bool:
    """
    Verify Ed25519 signature over commit payload.
    Returns True if valid, False otherwise.
    """
    try:
        serialized = canonical_serialize(commit_payload)
        digest = hashlib.sha256(serialized).digest()
        signature_bytes = bytes.fromhex(signature_hex)
        public_key.verify(signature_bytes, digest)
        return True
    except Exception:
        return False
