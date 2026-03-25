# Security Policy

## Scope

This repository contains the Polaris protocol specification. Security
considerations apply to the specification itself — its cryptographic
commitments, signing requirements, and verification procedures.

## Core Security Constraint

If verification fails, verification fails.
There is no fallback path for invalid execution.

These are not operational guidelines. They are structural properties of the
Polaris enforcement boundary. No compliant implementation MAY weaken, defer,
or conditionally bypass verification failure.

## Cryptographic Model

Polaris uses **Ed25519** as the normative signing algorithm for
`authority_signature`. All compliant implementations MUST support Ed25519
signature verification.

Canonical encoding uses **SHA-256** for `event_id` derivation. The hash
format is `{algorithm}:{hex}` — algorithm agility is reserved for future
versions via `canonical_encoding_version`.

Requirements for compliant implementations:

- Signature verification MUST use strict mode — reject non-canonical S values
  and small-order points.
- There is no algorithm fallback. If declared `signature_scheme` verification
  fails, verification fails.
- `event_id` MUST be derived from canonical bytes excluding
  `authority_signature.signature`. Implementations MUST NOT include the
  signature in the hashed content.

## Structural Security Properties

The Polaris specification preserves the following properties across all
compliant implementations:

- **Tamper evidence** — modification of any committed event invalidates all
  downstream `canonical_pointer_ref` values.
- **Non-repudiation** — `authority_signature` binds every event to a
  declared signer and signing algorithm.
- **Causal binding** — execution cannot occur without a matching
  `canonical_pointer_ref`.
- **Replay determinism** — independent implementations produce identical
  verification outcomes for identical canonical inputs.
- **No fallback** — failed verification MUST NOT be recoverable through
  alternate paths, weaker algorithms, or configuration overrides.

## Specification Boundary

The specification does not guarantee:

- Key management security — how signing keys are generated, stored, or
  rotated is outside this specification.
- Signer identity — `authority_signature.signer` is an identifier; binding
  it to a real-world entity is outside this specification.
- Availability — denial-of-service conditions are outside this specification.

## Reporting a Vulnerability

If you discover a security vulnerability in this specification — including
ambiguities in normative text that could enable non-compliant implementations
to bypass invariants — report it privately before opening a public issue.

**Contact:** security@polaris-protocol.org

Include:

- Which document and section is affected
- The nature of the ambiguity or vulnerability
- The class of implementation behavior it could enable

We will respond within 72 hours.
