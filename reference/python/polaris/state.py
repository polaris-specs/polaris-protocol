"""
polaris.state
-------------
Canonical state and history.

A state is canonical if and only if it is an element of H.
Proposed states are not canonical until committed.
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def canonical_serialize(obj: Any) -> bytes:
    """
    Canonical JSON serialization per Polaris spec Section E:
    - UTF-8 encoding
    - No insignificant whitespace
    - Lexicographic key ordering (recursive)
    - No floats, NaN, Infinity
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """SHA-256 hash encoded as lowercase hex per Section E.12."""
    return hashlib.sha256(data).hexdigest()


def state_hash(state: dict) -> str:
    """Compute canonical state hash."""
    return sha256_hex(canonical_serialize(state))


@dataclass
class CanonicalHistory:
    """
    H = (S_0, S_1, S_2, ...)

    The append-only sequence of canonical states.
    n is the pointer to the current canonical state.
    Only the commit authority may advance n.
    """
    _states: list = field(default_factory=list)
    _hashes: list = field(default_factory=list)

    @property
    def n(self) -> int:
        """Current pointer value."""
        return len(self._states) - 1

    @property
    def current_state(self) -> dict:
        """S_n — the current canonical state."""
        return self._states[self.n]

    @property
    def current_hash(self) -> str:
        """Hash of S_n."""
        return self._hashes[self.n]

    def get_state(self, i: int) -> dict:
        return self._states[i]

    def get_hash(self, i: int) -> str:
        return self._hashes[i]

    def _append(self, state: dict, h: str) -> None:
        """Append-only. Called exclusively by commit authority."""
        self._states.append(state)
        self._hashes.append(h)

    def __len__(self):
        return len(self._states)
