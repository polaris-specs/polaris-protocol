# Quickstart — First Implementors Path

**Polaris Protocol v1.0 Release Candidate**

This document defines the smallest valid path into Polaris.

Full conformance is not required to begin. You need to understand the
core invariants and try them in practice. That is enough to contribute
meaningfully to the protocol's development.

---

## Level 0 — Read and Push Back

No implementation required.

**Do this:**

1. Read [SPEC.md](./SPEC.md) — start with the Preamble and Section A
2. Read [KNOWN-GAPS.md](./KNOWN-GAPS.md)
3. Read the technical report: https://polaris-protocol.org/paper/

**What you can say:**

*"I have read the spec. Here is what I think is wrong, unclear, or
missing."*

That is a real contribution. Protocol design improves under critical
reading. If you find a gap, contradiction, or ambiguity — that is
exactly what Level 0 is for.

Open an issue tagged `[feedback]` or email daniel@polaris-protocol.org.

Level 0 takes about 30 minutes.

---

## Level 1 — Minimal Implementation

You have implemented enough to verify that the core invariants hold
and to give grounded feedback on the spec.

Five requirements. Nothing more.

---

### L1.1 — Genesis state with correct genesis hash

Your implementation must produce a genesis state whose hash matches
the reference value in [REFERENCE-HASHES.md](./REFERENCE-HASHES.md).

This is the canonical encoding test. If your genesis hash does not
match, nothing downstream will. Start here.

---

### L1.2 — Transition lifecycle: PROPOSED → VALIDATED → COMMITTED

Your implementation must enforce the three-phase lifecycle in order.
A transition that has not passed PROPOSED and VALIDATED must not reach
COMMITTED. There is no shortcut.

The commit authority is the only component permitted to advance a
transition to COMMITTED.

---

### L1.3 — Hash chain integrity

Each committed transition record must reference the hash of the
preceding committed state via `prev_state_hash`. A transition whose
`prev_state_hash` does not match the current canonical pointer must
be rejected before commit.

This is the append-only chain. Without it, replay verification is
structurally impossible.

---

### L1.4 — Seven rejection reasons

Your implementation must be capable of returning exactly these seven
rejection reasons:

```
SCHEMA_INVALID
VALIDATION_FAILED
COMMIT_CONFLICT
REVALIDATION_FAILED
DOMAIN_SUSPENDED
INFRASTRUCTURE_FAILURE
DUPLICATE_TRANSITION_ID
```

Two invariants that must hold for every rejection, regardless of
reason: no side effect is produced, and the canonical pointer is not
advanced.

---

### L1.5 — Reference hash verification

Run your implementation against the reference inputs in
[REFERENCE-HASHES.md](./REFERENCE-HASHES.md) and confirm that your
output hashes match.

A match means your canonical encoding is spec-compliant across
implementations. A mismatch means something is wrong — either in
your implementation or in the spec. Both findings are useful.

---

### What Level 1 does not require

- Full gate profile implementation
- Ed25519 signing
- PCIS-1 test suite passage
- Distributed commit or consensus
- Performance benchmarking
- Production-grade error handling
- Any specific language or runtime

You may implement in any language, on a single node, in memory.
Stub everything outside the five requirements. A working Level 1
prototype in an evening is the goal, not a production system.

---

### When you are done

Create a short `POLARIS-LEVEL1.md` in your repository and open an
issue tagged `[implementation]`.

Tell us what the spec made easy, what it made hard, and what was
unclear or missing. That feedback shapes what comes next.

---

## What comes next

Full conformance — against SPEC.md Section K.4 and the PCIS-1 test
suite — will be defined after Level 1 feedback has been incorporated.

It will not be defined unilaterally. It will reflect what Level 1
implementors actually found.

---

**Start today.**

Repo: https://github.com/polaris-specs/polaris-protocol
Questions: open an issue or email daniel@polaris-protocol.org
