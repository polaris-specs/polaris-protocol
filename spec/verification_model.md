# Verification Model

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/verification_model.md`

---

## Purpose

The verification model defines how a compliant implementation proves the
integrity, authenticity, and causal validity of events, transitions, and
canonical state progressions.

No transition MAY become authoritative without satisfying the verification
conditions defined in this document.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Verification Levels

Verification operates at three levels, each of which MUST be satisfied
independently and in order:

1. **Canonical Integrity** — the event is well-formed and its `event_id`
   is correct.
2. **Signature Authenticity** — the `authority_signature` is valid against
   the canonical encoding.
3. **Causal Validity** — the event's `canonical_pointer_ref` is consistent
   with canonical state progression.

A failure at any level MUST cause verification to fail. A passing result at
one level does not compensate for failure at another.

---

## Level 1: Canonical Integrity

### 1.1 Constraint

An event MUST be canonically encodable and its `event_id` MUST match the
hash derived from that encoding.

### 1.2 Procedure

A compliant implementation MUST perform the following steps:

1. Parse the event object.
2. Apply canonical encoding rules as defined in `spec/canonical_encoding.md`.
3. Exclude `authority_signature.signature` from the canonical byte sequence.
   Include all other fields in canonical field order.
4. Compute `SHA-256` of the canonical byte sequence.
5. Hex-encode the result, lowercase, 64 characters.
6. Compare the result to the event's `event_id` field.

If the computed value does not match `event_id`, verification MUST fail with
a canonical integrity error.

### 1.3 Rejection Conditions

Canonical integrity verification MUST fail if:

- The event cannot be parsed into a valid structure.
- Any required field is absent.
- Any field violates the encoding constraints defined in
  `spec/canonical_encoding.md`.
- The recomputed hash does not match `event_id`.
- `canonical_encoding_version` does not reference a known version.

---

## Level 2: Signature Authenticity

### 2.1 Constraint

`authority_signature` MUST be a valid attestation over the canonical encoding
by the declared signer.

### 2.2 Procedure

A compliant implementation MUST perform the following steps, and MUST NOT
proceed to this level unless Level 1 has passed:

1. Extract `authority_signature.signer`, `authority_signature.signature_scheme`,
   and `authority_signature.signature`.
2. Reconstruct the canonical byte sequence as computed in Level 1 (excluding
   `authority_signature.signature`).
3. Verify `authority_signature.signature` against the canonical byte sequence
   using `authority_signature.signer` as the verification key and
   `authority_signature.signature_scheme` as the algorithm.

If signature verification fails, verification MUST fail with a signature
authenticity error.

### 2.3 Multi-Authority Attestation

Where `signatures` array entries are present, each entry MAY be verified
independently using the same procedure. A failure of an entry in `signatures`
MUST NOT by itself cause overall verification to fail unless the applicable
gate profile requires it.

`authority_signature` MUST always be verified. It is not substitutable by
entries in `signatures`.

### 2.4 Rejection Conditions

Signature authenticity verification MUST fail if:

- `authority_signature` is absent.
- `authority_signature.signature_scheme` is not a recognized algorithm.
- `authority_signature.signature` is not a valid base64-encoded value.
- The signature does not verify against the canonical byte sequence.
- `authority_signature.signer` cannot be resolved to a verification key.

There is no algorithm fallback. Implementations MUST NOT fall back to a
weaker algorithm if the declared `signature_scheme` fails.

---

## Level 3: Causal Validity

### 3.1 Constraint

The event's position in canonical state progression MUST be consistent with
the Canonical Progression Uniqueness and Canonical Pointer Authority
invariants defined in `spec/invariants.md`.

### 3.2 Procedure

A compliant implementation MUST perform the following steps, and MUST NOT
proceed to this level unless Levels 1 and 2 have passed:

1. Retrieve the current canonical state pointer for the applicable domain.
2. Compare `canonical_pointer_ref` to the canonical state pointer.

For a **PSTO** (`event_type: "psto"`):
- `canonical_pointer_ref` MUST equal the current canonical state pointer.
- If `canonical_pointer_ref` is `null`, the event MUST be a genesis event
  and no prior canonical state MUST exist for this domain.

For a **validation_artifact** (`event_type: "validation_artifact"`):
- `canonical_pointer_ref` MUST reference the `event_id` of the PSTO being
  validated.

For a **commit_record** (`event_type: "commit_record"`):
- `canonical_pointer_ref` MUST reference the `event_id` of the
  `validation_artifact` authorizing this commit.
- The commit record MUST carry a `validation_proof` confirming
  `VALIDATE_PASS`.

For an **execution_request** (`event_type: "execution_request"`):
- `canonical_pointer_ref` MUST equal the canonical state pointer at the
  time of evaluation.
- If the canonical state pointer has advanced since the request was
  formed, the request MUST be rejected.

For an **execution_receipt** (`event_type: "execution_receipt"`):
- `canonical_pointer_ref` MUST reference the `event_id` of the
  `execution_request` it receipts.

### 3.3 Sequence Verification

`context.sequence` MUST be exactly one greater than the `context.sequence`
of the preceding event for the same `context.agent_id`. For genesis events,
`context.sequence` MUST be `0`.

A compliant implementation MUST reject any event whose `context.sequence`
is non-monotonic with respect to prior events from the same agent.

### 3.4 Rejection Conditions

Causal validity verification MUST fail if:

- `canonical_pointer_ref` does not match the required value for the given
  `event_type`.
- `canonical_pointer_ref` is `null` for a non-genesis event.
- `context.sequence` is non-monotonic.
- A `commit_record` does not carry a `VALIDATE_PASS` result in
  `validation_proof`.
- An `execution_request` references a superseded canonical state pointer.

---

## Unified Verification Result

A compliant implementation SHOULD produce a structured verification result
containing:

```
VerificationResult {
    valid:                    bool
    level_reached:            1 | 2 | 3
    canonical_integrity:      pass | fail
    signature_authenticity:   pass | fail
    causal_validity:          pass | fail
    failure_reason:           string | null
    event_id:                 string
    event_type:               string
}
```

`valid` MUST be `true` if and only if all three levels pass. A partial pass
MUST NOT be reported as `valid`.

---

## Replay Verification

During replay, a verifier MUST apply all three verification levels to each
event in `context.sequence` order for a given `context.agent_id`.

Replay verification MUST be idempotent. Repeated replay of the same canonical
history MUST produce identical results.

Replay MUST NOT:

- Mutate canonical state.
- Advance the canonical state pointer.
- Trigger side effects.
- Introduce new authoritative transitions.

If any event in the replay sequence fails verification, all subsequent events
in that sequence MUST be treated as unverified. A verifier MUST NOT skip
failed events and continue verifying downstream events as if they were valid.

---

## Enforcement Boundary

Verification is part of the enforcement boundary as defined in
`spec/invariants.md` (Invariant 8: Non-Bypassable Enforcement Boundary).

A Polaris implementation MUST NOT:

- Advance canonical state for an event that has not passed all three
  verification levels.
- Authorize execution for a request that has not passed Level 3.
- Accept a commit record that references a PSTO which has not passed
  Levels 1 and 2.

Verification results produced outside the enforcement boundary — including
results produced by external systems, cached results, or results carried
in non-verified metadata — MUST NOT substitute for independent verification.

---

## Minimal Compliance Statement

A Polaris implementation is compliant with the verification model only if:

1. It applies canonical integrity, signature authenticity, and causal validity
   verification independently and in order.
2. It rejects any event that fails at any verification level.
3. It produces identical verification outcomes for identical canonical inputs
   across independent compliant implementations.
4. It does not advance canonical state or authorize execution without a
   complete verification pass.
5. It does not substitute external, cached, or unverified results for
   independent verification.
