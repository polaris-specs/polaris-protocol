# Canonical Encoding

**Status:** Normative
**Version:** 1.0.0
**Spec:** `spec/canonical_encoding.md`

---

## Version

This document specifies canonical encoding version `1.0.0`.

All events produced under these rules MUST carry:

```
"canonical_encoding_version": "1.0.0"
```

A future revision of canonical encoding rules MUST increment this version.
Events carrying an unknown `canonical_encoding_version` MUST be rejected.

---

## Purpose

Polaris uses deterministic canonical encoding to ensure that semantically
equivalent state transition objects produce identical encoded representations,
hashes, validation outcomes, and replay results across compliant implementations.

Canonical encoding is not an optional serialization preference. It is a
structural requirement of the Polaris architecture. A proposed state transition
object is eligible for validation only if it can be normalized into canonical
form and hashed under the rules defined in this document.

---

## Conformance Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as
described in RFC 2119.

---

## Architectural Role

Canonical encoding serves five functions within the Polaris enforcement boundary:

1. It prevents representation ambiguity.
2. It ensures deterministic hash derivation.
3. It binds validation artifacts to a stable transition representation.
4. It enables independent replay and verification across implementations.
5. It prevents semantically identical transition objects from producing
   divergent canonical state outcomes.

Canonical encoding is upstream of validation and upstream of commit. If
canonical encoding fails, validation MUST fail. If validation fails, commit
MUST NOT occur. If commit does not occur, no canonical pointer advancement and
no execution enablement are possible.

---

## Scope

Canonical encoding applies to:

- Proposed State Transition Objects (PSTOs)
- Validation artifacts where deterministic replay is required
- Commit records
- Execution requests
- Execution receipts

This document focuses primarily on PSTO canonical encoding because it defines
the root transition object from which validation, commitment, and execution
eligibility are derived. All other event types derive their canonical encoding
requirements by extension of the same rules.

---

## Core Requirements

A compliant canonical encoding implementation MUST satisfy the following:

- Identical semantic inputs MUST produce identical byte sequences.
- Identical byte sequences MUST produce identical hashes.
- Field ordering MUST be fixed and deterministic.
- Variable-length fields MUST use unambiguous length-prefixed encodings.
- List fields MUST be deterministically ordered.
- Optional fields MUST use deterministic empty encodings rather than silent
  omission, unless the enclosing structure explicitly defines omission semantics.
- Numeric fields MUST use fixed-width encodings where specified.
- Byte order MUST be unambiguous and uniform across implementations.
- Canonicalization MUST complete before validation and hash derivation.

A non-canonical representation MUST be rejected for any operation capable of
influencing validation, commit eligibility, replay verification, or execution
authorization.

---

## Canonicalization Pipeline

The canonicalization pipeline for a proposed state transition MUST proceed
in the following order:

1. Parse the transition object.
2. Normalize all fields into canonical representation.
3. Order all deterministic collections.
4. Encode fields in the fixed canonical order defined in this document.
5. Produce the canonical byte sequence.
6. Derive `event_id` from the canonical byte sequence, excluding
   `authority_signature.signature`.
7. Verify `authority_signature` against the derived hash.

If any step fails, the transition object MUST be rejected.

---

## Canonical Field Order

PSTO fields MUST be encoded in the following order:

1. `canonical_encoding_version`
2. `canonical_pointer_ref`
3. `event_type`
4. `context.timestamp`
5. `context.agent_id`
6. `context.sequence`
7. `context.contextual_tags` (deterministic empty encoding if absent)
8. `candidate_payload`
9. `action_payload` (deterministic empty encoding if absent)
10. `validation_proof` (deterministic empty encoding if absent)
11. `authority_signature.signer`
12. `authority_signature.signature_scheme`

The field `authority_signature.signature` MUST be excluded from canonical
byte derivation. All other listed fields MUST be present in canonical bytes
regardless of whether they carry content.

No implementation MAY reorder these fields when producing canonical bytes.

---

## Primitive Encoding Rules

In the reference embodiment, the following primitive types are used:

| Symbol | Definition |
|---|---|
| `U8` | Unsigned 8-bit integer |
| `U16` | Unsigned 16-bit integer, big-endian |
| `U32` | Unsigned 32-bit integer, big-endian |
| `U64` | Unsigned 64-bit integer, big-endian |
| `BYTES[N]` | Exactly N bytes |
| `VARBYTES` | U32 length prefix followed by length bytes |
| `HASH32` | BYTES[32] — SHA-256 digest |

Alternative primitive layouts MAY be used only if they preserve deterministic
equivalence and unambiguous replay semantics across all compliant
implementations.

Byte order MUST be network order (big-endian) for all fixed-width numeric
fields.

---

## Variable-Length Fields

All variable-length fields MUST be length-prefixed.

A compliant implementation MUST reject:

- Inconsistent stated lengths.
- Trailing undecoded bytes after the declared length boundary.
- Multiple equivalent representations of the same field value.
- Ambiguous concatenation boundaries.

---

## Optional Fields

Optional fields (`context.contextual_tags`, `action_payload`,
`validation_proof`) MUST use deterministic empty encodings when absent.

Silent omission is NOT canonical unless the enclosing structure explicitly
defines a canonical absence rule. Where two implementations would produce
different byte sequences for the same absent optional field, the encoding is
non-compliant.

---

## Deterministic List Ordering

Any list or collection contributing to canonical bytes MUST be
deterministically ordered.

This applies to:

- Presence vector entries
- Constraint references
- Artifact references
- Proof artifact identifiers

Where not otherwise specified by the applicable transition class, entries MUST
be ordered lexicographically by the canonical byte representation of their
primary identifier field.

---

## Hash Derivation

The canonical `event_id` is derived as:

```
event_id = SHA-256(canonical_bytes_without_authority_signature)
```

Where:

- `canonical_bytes_without_authority_signature` includes all fields in
  canonical order except `authority_signature.signature`.
- `authority_signature.signer` and `authority_signature.signature_scheme`
  ARE included.
- The result is hex-encoded, lowercase, 64 characters.

A compliant implementation MUST derive identical `event_id` values for
semantically equivalent transition objects.

---

## Signature Verification

After canonical byte derivation and `event_id` computation,
`authority_signature.signature` MUST be verified against `event_id` using
`authority_signature.signer` and `authority_signature.signature_scheme`.

If signature verification fails, validation MUST fail. Signature verification
MUST NOT repair or reinterpret a non-canonical transition representation.

---

## Cross-Implementation Determinism

Cross-implementation determinism is a first-class Polaris requirement.

An implementation is not compliant merely because it is internally consistent.
It MUST be externally reproducible by other compliant implementations operating
on the same canonical inputs.

This requirement applies to:

- PSTO canonicalization
- `event_id` derivation
- Replay-visible validation artifacts
- Commit record derivation
- Execution request binding

---

## Rejection Conditions

A proposed transition MUST be rejected as non-canonical if any of the
following occur:

- A required field is missing.
- A fixed-width field has incorrect width.
- A variable-length field has inconsistent length metadata.
- A deterministic collection is not ordered as required.
- An optional field uses a non-canonical absence form.
- Canonical byte derivation depends on implementation-local ordering, locale,
  whitespace, formatting, or undefined serialization behavior.
- The recomputed `event_id` differs from the claimed value.
- Signature verification fails against the recomputed canonical hash.
- `canonical_encoding_version` is absent or does not match a known version.

---

## Non-Goals

Canonical encoding does not:

- Determine whether a transition should pass semantic or domain-specific gates.
- Replace gate profile evaluation.
- Replace commit authority semantics.
- Replace execution gate enforcement.

It provides the stable representational substrate on which those mechanisms
depend.

---

## Minimal Compliance Statement

A Polaris implementation is canonically compliant only if semantically
equivalent proposed state transition objects normalize to identical canonical
byte representations, producing identical `event_id` values, identical
validation behavior, and identical replay-visible outcomes across all
compliant implementations.
