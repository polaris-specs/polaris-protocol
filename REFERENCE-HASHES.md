# Polaris Protocol — Reference Hash Values

These hash values are the canonical reference for implementers verifying that their
canonical JSON serialization and SHA-256 implementation match the specification.

If your implementation produces different values, your serialization is non-conformant.
Check: key ordering, whitespace, encoding, timestamp format, integer representation.

---

## Genesis Hash — instrument.BTCUSD

Input object (before serialization):
```json
{
  "authority_identity": "commit-authority.instrument.node-1",
  "domain_id": "instrument.BTCUSD",
  "initial_state": {"last_price": 0, "position": 0, "version": 0},
  "initialized_at": "2026-03-30T10:00:00.000Z",
  "polaris_version": "1.0",
  "sequence_number": 0
}
```

Canonical JSON (genesis_hash field excluded, keys lexicographically ordered):
```
{"authority_identity":"commit-authority.instrument.node-1","domain_id":"instrument.BTCUSD","initial_state":{"last_price":0,"position":0,"version":0},"initialized_at":"2026-03-30T10:00:00.000Z","polaris_version":"1.0","sequence_number":0}
```

SHA-256 genesis_hash:
```
1253f3325d5143a343403bd0380d8b7cd98c23f2bf74e02cee5652cae8aa61d8
```

---

## Genesis Hash — account.user_1

Input object:
```json
{
  "authority_identity": "commit-authority.instrument.node-1",
  "domain_id": "account.user_1",
  "initial_state": {"balance": 0, "version": 0},
  "initialized_at": "2026-03-30T10:00:00.000Z",
  "polaris_version": "1.0",
  "sequence_number": 0
}
```

Canonical JSON:
```
{"authority_identity":"commit-authority.instrument.node-1","domain_id":"account.user_1","initial_state":{"balance":0,"version":0},"initialized_at":"2026-03-30T10:00:00.000Z","polaris_version":"1.0","sequence_number":0}
```

SHA-256 genesis_hash:
```
30904edacf88d7d5e1c34e1168b4c47733dc9da076c1a6ce2a6fc063916f496c
```

---

## Chain Verification Reference — instrument.BTCUSD

T1 state hash: `0840f70d795e45eb91acbefd1e3dce62e22e54ce6f217f3ee6e81688271a29c8`
T2 state hash: `d1043f90223e037d9c521511043548e4aa39768e3f21174ebadedc6dffcde172`
T3 state hash: `64a5731d43cc15219e653aa9b34beba70d1c43b2b0a5691e0e4a596627e83a2b`

---

## Computation Method

All hashes computed as:
```
hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',',':')).encode('utf-8')).hexdigest()
```

Python reference:
```python
import json, hashlib

def canonical_hash(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()
```
