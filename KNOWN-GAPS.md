# Polaris Protocol Specification v1.0 — Known Gaps

This document lists acknowledged limitations of Polaris v1.0 that are deferred to v1.1.
These items do not affect interoperability of conformant implementations but represent areas
where the specification is incomplete or where further work is needed.
Contributors are invited to propose resolutions via: https://github.com/polaris-specs/polaris-protocol/issues

## GAP-01 — Intentional Authority Transfer

**Category:** Protocol design
**Affects:** Section D, Section F
**Status:** Deferred to v1.1

The specification covers authority loss (→ suspended state) but not intentional authority
transfer. When commit authority is deliberately transferred from node-1 to node-2, there is
no "authority transfer record" defined in the spec. From the chain's perspective, this is
indistinguishable from a node disappearing and a new node appearing. An external verifier
cannot distinguish a legitimate transfer from an attack.
v1.1 target: Define an authority transfer record with signing requirements that make transfers
independently verifiable and distinguishable from unexpected authority loss.

## GAP-02 — "Deployment Context" and "Independent" Undefined

**Category:** Terminology
**Affects:** Section F.7, Section J.2
**Status:** Deferred to v1.1

Both terms are used normatively without formal definitions. "Independently accessible to
any verifier within the deployment context" — what avgrenses deployment context? What does
"independently" mean precisely?
v1.1 target: Add formal definitions with worked examples.

## GAP-03 — No Worked Example with Actual Hash Values

**Category:** Pedagogical
**Affects:** All sections
**Status:** Partially closed — reference hash values published in REFERENCE-HASHES.md.
Full end-to-end worked example with narrative deferred to v1.1.

There is no complete end-to-end walkthrough from genesis initialization through T1 → T2 →
execution with all actual SHA-256 hash values computed and published. Such an example would
allow implementers to verify their implementation against known-good values.
v1.1 target: Produce a reference example in Python or Rust with all hash values computed and
published in the repository. Requires a working reference implementation.

## GAP-04 — Domain Re-activation and Stale Proposal Notification

**Category:** Operational
**Affects:** Section B.5.1
**Status:** Partially addressed (B.5.1 defines suspension semantics; re-activation not fully specified)

Section B.5.1 defines what happens to pending proposals during suspension. It does not
fully specify: who is responsible for notifying proposers that their transitions require
re-validation after domain resume, and whether there is a time limit on re-validation
after resume.
v1.1 target: Add normative requirements for re-activation notification and re-validation time
window.

## GAP-06 — No Retry Limit for FAILED Executions

**Category:** Operational
**Affects:** Section I.5
**Status:** Deferred to v1.1

Section I.5 permits retry of FAILED executions without defining a maximum retry count,
backoff requirements, or escalation criteria. In production systems, unbounded retry is
an operational risk.
v1.1 target: Add normative requirement that retry policy MUST be documented and MAY
include maximum retry count and backoff strategy. Consider whether an
EXECUTION_ABANDONED terminal state is needed.

## GAP-07 — Archival and Cold Storage Not Addressed

**Category:** Operational
**Affects:** Section B.7, Section H.7
**Status:** Deferred to v1.1

The spec requires append-only canonical progression and full replayability from genesis.
It does not address what it means to archive older records to cold storage, whether
compression is conformant, or what "available for verification" means for archived records.
v1.1 target: Define conformant archival: what conditions a cold storage solution must satisfy to
remain conformant (e.g., retrievable on-demand within defined SLA, verifiable hash chain
maintained, public key for retired authorities remains accessible).

## Summary

| Gap | Category | Severity | Target |
|---|---|---|---|
| GAP-01 Intentional authority transfer | Protocol design | High | v1.1 |
| GAP-02 "Deployment context" undefined | Terminology | Medium | v1.1 |
| GAP-03 No worked example (partially closed) | Pedagogical | Low | Partially closed |
| GAP-04 Domain re-activation notification | Operational | Medium | v1.1 |
| GAP-06 No retry limit for FAILED executions | Operational | Low | v1.1 |
| GAP-07 Archival and cold storage | Operational | Medium | v1.1 |

This document is maintained alongside the specification. When a gap is resolved, it is removed
from this document and the resolution is noted in the CHANGELOG.
