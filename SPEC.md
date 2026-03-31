Polaris Protocol Specification
Causal Integrity and Trust Attestation for Agent Systems
Version: 1.0
Status: Release Candidate
License (Specification): Creative Commons Attribution 4.0 International (CC-BY-4.0)
License (Reference Implementations): Apache License, Version 2.0
Repository: polaris-specs/polaris-protocol
Conformance: Section K

CHANGELOG
v1.0.0 (current)
Initial release.
Self-declared conformance available (Level 1).
PCIS-1 specified, not yet implemented.
KNOWN-GAPS.md documents 7 acknowledged limitations deferred to v1.1.
v1.1 (planned)
PCIS-1 implemented and published as open source.
Suite-verified conformance available (Level 2).
6-month grace period for existing Level 1 implementations.
Resolution of KNOWN-GAPS items.
v2.0 (future)
Full conformance test suite (PCIS-2).
Complete section coverage.
Algorithm rotation mechanism.
Based on implementation feedback from v1 and v1.1.

Preamble
P.1 — The One Invariant
No side effect may occur unless it is the result of a committed, validated transition — and that
fact must be independently verifiable.
The Polaris invariant. Everything else in this specification follows from it.
Everything in this specification is a consequence of this invariant. If you understand it, you
understand Polaris. If an implementation satisfies it — precisely, verifiably, without exception —

it is Polaris. If it does not, it is not.

P.2 — What Polaris Is
Polaris is a protocol for commit-gated execution.
It defines how proposed state changes are validated, committed to a single canonical
progression, and only then permitted to produce side effects — with a cryptographically
verifiable record of the entire sequence.
Polaris does not define what an agent should do. It defines the constraints under which any agent
action is permitted to occur. The distinction matters: Polaris is not a framework, a runtime, or an
orchestration system. It is the layer that sits between intent and consequence and says: this
action was authorized, in this order, by this authority, and that claim is verifiable by anyone with
access to the record.
Trust is not a feeling. It is a system. Polaris is that system.

P.3 — Why This Exists
AI agent systems are executing consequential actions at scale. They are moving money,
submitting orders, making decisions that affect real systems. The infrastructure for verifying
that those actions were authorized — before they occurred, not after — does not yet exist as a
protocol standard.
The absence of this infrastructure creates a specific class of risk: not that agents will act
incorrectly, but that no one can prove they acted correctly. An agent system without causal
integrity is a system where the logs can be altered, where the order of decisions can be disputed,
where the boundary between "what the agent was authorized to do" and "what the agent did"
cannot be independently established.
Polaris closes this gap. It does not make agents smarter or safer in the sense of better decisions. It
makes the record of what agents did tamper-evident, causally ordered, and independently
verifiable. That is a different problem, and it is the problem Polaris is designed to solve.

P.4 — Design Principles
Restrictive by intent. The constraints in this specification are governance boundaries, not
engineering preferences. An implementation that satisfies all normative requirements can use
this protocol as an unambiguous reference point when external pressure seeks to relax those
boundaries. "The protocol requires this" is a complete answer.
Precise over flexible. Where a choice exists between a flexible formulation and a precise one,
this specification chooses precision. Flexibility at the protocol level produces ambiguity at the

implementation level. Ambiguity produces non-interoperable implementations. Noninteroperable implementations produce a label, not a protocol.
Fail closed always. Every failure mode in this specification resolves to one of two outcomes:
reject the transition, or suspend the domain. There is no third outcome. There is no best-effort
mode. There is no partial success. A system that proceeds under uncertainty is not Polaris.
Verifiable by anyone. The guarantees of this protocol are not assertions by the implementing
party. They are claims that any external verifier — a regulator, an auditor, a counterparty, a court
— can verify independently, without trusting the party that produced the record. If it cannot be
verified independently, it is not a guarantee.

P.5 — Who This Document Is For
Protocol implementers Developers building Polaris-conformant systems. Start with Section A
for orientation, then Section G for the transition object, then the section relevant to the
component you are building.
System integrators Teams adding Polaris to an existing system. Start with Section A.7 (profiles)
and Section A.7.3 (graduation path) to understand what production conformance requires.
Auditors and verifiers Parties verifying that an implementation is conformant. Start with
Section K for the conformance checklist and PCIS-1 test specification.
Evaluators and researchers Parties assessing Polaris for adoption or comparison. Start with
Section J (threat model) for what Polaris guarantees and Section L for how it relates to other
patterns.

P.6 — Document Structure
Section

Title

Status

A

Overview and Scope

Normative — entry point, core invariants, roles, profiles

B

State Domain

Normative — canonical state, partitioning, suspended state

C

Validator

Normative — deterministic validation, purity boundary, verdict

D

Commit Mechanism

Normative — linearization, commit record, conflict handling

E

Canonical Serialization

Normative — deterministic JSON encoding for interoperability

F

Cryptographic Integrity

Normative — SHA-256, Ed25519, chain integrity

G

Transition Object

Normative — schema, lifecycle, causal chain

Section

Title

Status

H

Genesis State

Normative — initialization, genesis hash, chain anchor

I

Execution Gate

Normative — gate checks, execution record, agent authorization

J

Threat Model

Normative — guarantees, boundaries, trust assumptions

K

Conformance

Normative — checklist, PCIS-1 specification, claim format

L

Polaris vs Other Patterns

Informative — positioning against related approaches

All sections B through K are normative. Section L is informative.

P.7 — Normative Language
The key words MUST, MUST NOT, and MAY are used in their RFC 2119 sense throughout this
specification. A requirement using MUST is not a recommendation. It is a condition for
conformance. A system that does not satisfy a MUST is not Polaris-conformant, regardless of
what else it does correctly.
MUST
— required for conformance. No exceptions.
MUST NOT — prohibited. Presence constitutes non-conformance.
MAY
— permitted but not required.
SHOULD — not used in this specification.

The absence of SHOULD is deliberate. A requirement that an implementation "should" do
something is a requirement with an exit. Polaris does not offer exits on its core requirements.
Where a requirement is genuinely optional it is marked MAY. Where it is required, it is MUST.
P.7.1 Terminology Capitalization

The three logical roles are capitalized when referring to the role as a defined protocol concept,
and lowercase when used in a general or descriptive sense:
Capitalized (role as concept): "The Validator returns a PASS or FAIL verdict." "The Commit
Authority advances canonical state." "The Execution Gate blocks execution."
Lowercase (general reference): "the validator in your implementation", "a commit authority may
be co-located with...", "the execution gate checks three conditions."

P.8 — Versioning
v1.0 — this document.
Self-declared conformance (Level 1).

PCIS-1 specified but not yet implemented.
v1.1 — PCIS-1 implemented and published.
Suite-verified conformance (Level 2) available.
6-month grace period for existing Level 1 implementations.
v2.0 — full conformance test suite (PCIS-2).
Complete section coverage.
Algorithm rotation mechanism defined.
Based on implementation feedback from v1 and v1.1.

Breaking changes require a major version increment. A v1 implementation is not required to be
v2-conformant. A v2 implementation must document explicitly which v1 requirements it
preserves and which it supersedes.
P.8.1 Questions and Issues

Questions regarding interpretation of this specification, suspected errors, or proposed changes
should be directed to:
GitHub Issues: https://github.com/polaris-specs/polaris-protocol/issues
Conformance questions: open an issue tagged [conformance].
Errata: open an issue tagged [errata]. Confirmed errata will be published in the repository and
incorporated in the next minor version.
P.8.2 PCIS-1 Timeline

PCIS-1 is under active development. Publication timeline will be announced in the repository
when a release candidate is available. Progress is tracked at: github.com/polaris-specs/polarisprotocol/milestones

P.9 — Legal Notice
Copyright 2026 Daniel Lindberg and the Polaris Protocol contributors.
The Polaris Protocol Specification is licensed under Creative Commons Attribution 4.0
International (CC-BY-4.0). https://creativecommons.org/licenses/by/4.0/
Reference implementations are licensed under the Apache License, Version 2.0.
https://www.apache.org/licenses/LICENSE-2.0
DISCLAIMER OF WARRANTY AND LIABILITY

This specification is provided for informational and implementation guidance purposes. The
authors and contributors make no representations or warranties of any kind, express or implied,
regarding the completeness, accuracy, or fitness for a particular purpose of this specification.

Implementations of this specification are solely responsible for ensuring that their systems
comply with applicable laws and regulations. Nothing in this specification constitutes legal,
financial, or regulatory advice.
PATENT NOTICE

Certain aspects of this specification may be the subject of patent applications. Implementers
should be aware that compliance with this specification does not guarantee freedom from thirdparty patent claims.

Section A — Overview and Scope
Status: Normative (v1.0)

A.1 Overview
Polaris is a protocol for commit-gated execution.
It defines how proposed transitions are validated, committed to a single canonical state
progression, and only then permitted to produce side effects.
Polaris enforces a causal invariant:
No side effect may occur unless it is the result of a committed, validated transition.
Polaris does not define business logic. It defines the constraints under which execution is
permitted.

A.2 Core Concepts (Informative Index)
The protocol is defined by the following sections:
B — State Domain: canonical state, partitioning, and domain boundaries
C — Validator: deterministic evaluation of proposed transitions
D — Commit Mechanism: canonical progression and linearization
E — Canonical Serialization: deterministic encoding for hashing
F — Cryptographic Integrity: tamper evidence and independent verification
G — Transition Object: the fundamental unit of the protocol
H — Genesis State: domain initialization and canonical chain anchor
I — Execution Gate: the third logical role — permits or blocks execution
J — Threat Model: what Polaris guarantees and what it does not
K — Conformance: conformance requirements and test suite

L — Polaris vs Other Patterns: positioning against related approaches

All sections B through K are normative. Section L is informative.

A.3 Roles (Logical Separation)
Polaris defines three logical roles:
Validator (Section C) Evaluates whether a proposed transition is admissible for commit. Returns
PASS or FAIL. Does not execute. Does not commit.
Commit Authority (Section D) Determines canonical progression. Atomically advances
canonical state at a single linearization point. Does not evaluate proposals. Does not execute
transitions.
Execution Gate (Section I) Permits or blocks side effects based on the existence of a committed
transition. Does not validate. Does not advance canonical state.

These roles are logically distinct and MUST remain independently inspectable, even when colocated in a single implementation. They may be co-located in implementation, but MUST
remain logically separable and independently inspectable.
Each role MUST be independently testable in isolation:
The Validator can be tested without running commit or execution.
The Commit Authority can be tested without triggering execution.
The Execution Gate can be tested without running the validator or commit pipeline.
A PASS validation verdict is necessary but not sufficient for execution. Execution requires a
committed transition. The Validator determines eligibility. The Commit Authority determines
progression.
See Section C.15 for role separation requirements.

A.4 Invariants
The following invariants MUST hold for any conformant implementation:
1. Commit-Gated Execution Execution MUST NOT occur without a committed transition.
2. Single Canonical Progression (per domain) At most one successor MAY advance a given
canonical state.
3. Deterministic Validation Identical inputs MUST yield identical validation verdicts.
4. Canonical Serialization State and commit payloads MUST be encoded deterministically.
5. Causal Binding Every side effect MUST reference a committed transition.

6. Progression Integrity The canonical progression MUST be verifiably contiguous. Gaps in
sequence_number or breaks in the prev_state_hash chain MUST be detectable by any verifier
with access to the canonical progression.

A.5 Scope
Polaris defines:
canonical state progression per domain
deterministic validation requirements
commit semantics and linearization
execution gating based on commit
canonical serialization for interoperability
cryptographic integrity for verifiability
Polaris does NOT define:
application-specific business logic
cross-domain atomic coordination
key management procedures (beyond verifiability requirements)
infrastructure topology or deployment architecture
agent orchestration or governance models

A.6 Domains and Partitioning
Polaris operates per state domain.
A domain has:
a single canonical state
a single active commit authority
an independent progression history
Partitioning is permitted by defining multiple independent domains.
Polaris does not guarantee atomicity across domains.

A.7 Profiles
Polaris supports distinct implementation profiles.

A.7.1 Development Profile

A development profile MAY:
simplify validation logic
disable cryptographic integrity
A development profile MUST:
remain deterministic within its constraints
be explicitly configured and identified
A development profile is NOT production-conformant Polaris.
A.7.2 Production-Conformant Profile

A production-conformant implementation MUST:
enforce commit-gated execution
implement deterministic validation
maintain a single canonical progression per domain
use canonical serialization
apply cryptographic integrity (hash + signature + authority identity)
support independent verification of committed artifacts
fail closed on indeterminate conditions
A.7.3 Development-to-Production Graduation (Non-Normative)

An implementation that begins as a development profile and intends to become productionconformant MUST complete the following before claiming production conformance:
Step 1 — Cryptographic integrity Enable cryptographic integrity per Section F. SHA-256 state
hashing active. Ed25519 signing active on all commit records. Authority identity bound to
independently retrievable verification key per F.7. Development profile flag removed from
configuration.
Step 2 — Suspended state enforcement Verify that the domain enters suspended state on
infrastructure failure. Test by making the commit authority unreachable and confirming no
transitions are committed or executed during the outage.
Step 3 — Execution gate hardening Verify that no bypass path exists. Confirm that gate check 1
(commit exists) is never skipped. The gate MUST NOT be bypassed even when the calling code
"knows" the transition is committed.
Step 4 — Trust assumption documentation Produce a deployment-specific document that
states which trust assumptions from J.2 the deployment satisfies, by what mechanism each is
satisfied, and which are NOT satisfied with mitigations.

Step 5 — Conformance self-declaration Complete the self-declaration checklists in A.8. Retain
documentation of completed checklists.

A deployment that has completed all five steps may claim production-conformant Polaris status
under v1 interim conformance. A deployment that has completed steps 1–4 but not step 5 is
production-ready but not yet conformant and MUST NOT claim Polaris conformance until step 5
is complete.

A.8 Conformance
An implementation is Polaris-conformant only if all normative requirements in Sections B
through K are satisfied.
MUST NOT: Partial implementations MUST NOT be represented as Polaris-conformant.
MUST NOT: An implementation MUST NOT claim conformance beyond the boundaries defined
in Section J (Threat Model). Claims that exceed J's stated guarantees are non-conformant
regardless of implementation correctness.
Implementations MAY provide additional features, provided they do not violate the core
invariants defined in A.4.
Conformance is self-declared against the following:
B.8 — State Domain conformance checklist
C.13 — Validator conformance checklist
D.11 — Commit Mechanism conformance checklist
G.9 — Transition Object conformance checklist
H.9 — Genesis State conformance checklist
I.10 — Execution Gate conformance checklist
J — Two normative requirements: J.2 (trust assumptions documented) and J.7 (no out-ofscope claims)
Section K: self-declaration completed [date]
All of the above must be satisfied for a conformant claim. Section K defines the complete
conformance process.

A.9 Failure Model
Polaris follows a fail-closed model.
If required conditions for validation, commit, or integrity cannot be deterministically
established:

MUST: If failure is transition-local, the transition MUST be rejected. The domain continues
normally. Other proposals are not affected.
MUST: If failure is infrastructure-level — validation, commit, or cryptographic integrity
infrastructure is unavailable or produces an indeterminate result — the domain MUST enter
suspended state. No transitions may be committed until the condition is resolved.
No best-effort execution is permitted under either condition.

A.10 Terminology (Minimal)
Transition A proposed change from one canonical state to another. The fundamental unit of the
Polaris protocol. See Section G.
Canonical State The single authoritative state for a domain at a given point in time. Immutable
after commit. See Section B.
Commit The atomic advancement of canonical state at a single linearization point. The only
mechanism by which canonical state may advance. See Section D.
Execution The production of side effects. Permitted only after a committed transition exists and
is verified by the Execution Gate. See Section I.
Validator The component that evaluates whether a proposed transition is admissible for commit.
Returns PASS or FAIL. See Section C.
Commit Authority The component that atomically advances canonical state. Logically
independent per domain. See Section D.
Execution Gate The component that permits or blocks side effects based on the existence of a
committed transition. The third logical role. Execution is blocked unless a committed transition
exists and is referenced by the execution attempt. See Section I.
State Domain A bounded context with a single canonical state, a single commit authority, and an
independent progression history. See Section B.
Genesis State The initial canonical state of a domain. Establishes the anchor of the hash chain.
Precedes sequence_number 1. See Section H.
Canonical Progression The ordered, append-only sequence of committed transitions within a
domain from genesis to present. See Section B and Section H.
Append-Only A data structure or log to which records may only be added, never modified or
deleted. An append-only structure preserves all historical entries permanently. Polaris canonical
progressions, commit records, and observability logs are all append-only.
Side Effect Any action taken by a component that produces an observable change outside the
Polaris protocol itself. Side effects include but are not limited to: writes to external databases or
storage systems, API calls to external services, messages sent to queues or event buses, financial

operations (order submissions, payments, transfers), network requests that mutate state in
external systems, notifications sent to external parties.
Side effects do NOT include: reads from external systems (no mutation), append-only
observability events within the Polaris pipeline that satisfy the purity boundary in Section C.10,
internal Polaris state changes (canonical state advancement).
The distinction is mutation. If the action changes state in a system outside Polaris, it is a side
effect and requires a committed transition as authorization per Section I.

Section B — State Domain
Status: Normative (v1.0) — Revision v1.0.2

B.1 Purpose
This section defines the concept of a state domain, the requirements for canonical state within a
domain, and the boundaries of Polaris guarantees in partitioned systems.
A Polaris system MUST have at least one state domain. The behavior of canonical state, commit
authority, and causal progression is defined per domain.

B.2 Definitions
State Domain A bounded context within which a single canonical state exists, progresses, and is
governed by a logically independent commit authority. All Polaris invariants apply
independently within each domain.
Canonical State The single authoritative state of a domain at any point in time. It is the state
from which all valid proposals are derived and against which all commits are verified.
Commit Authority The logical entity responsible for atomically committing validated
transitions within a state domain. Commit authority is a logical property, not necessarily a
physical one. A single service or node may act as commit authority for multiple domains,
provided each domain's authority is logically isolated.
Canonical Progression The ordered, append-only sequence of committed transitions within a
domain. Each committed transition extends the canonical progression by exactly one step.
Suspended State A domain condition in which forward progression is blocked due to inability to
verify or reach commit authority. A suspended domain retains its committed canonical
progression but permits no new commits or executions.

B.3 Core Requirements
MUST
A single canonical state MUST exist per state domain at all times.
MUST
Canonical state MUST be immutable after commit.
MUST
All proposals within a domain MUST reference the current canonical state
as prev_state.
MUST
A commit MUST atomically update canonical state or reject the transition.
MUST NOT Canonical state MUST NOT be modified outside of the commit function.
MUST NOT Two distinct canonical states MUST NOT exist within the same domain
simultaneously.

B.4 Partitioned State
A Polaris system MAY partition state across multiple domains. Partitioning is permitted when
different parts of the system have independent causal progressions that do not require
coordination at the protocol level.
MAY
State MAY be partitioned across multiple state domains.
MUST
Each partition MUST constitute an independent state domain with its own
canonical
state and its own logically independent commit authority.
MUST NOT Partitions MUST NOT share a canonical state.
MUST NOT Partitions MUST NOT share commit authority logic.

The choice between a single domain and multiple partitioned domains is an architectural
decision. Polaris does not prescribe which is correct. It requires that boundaries are explicit and
that each domain satisfies all Polaris invariants independently.

B.5 Commit Authority and Suspended State
The commit authority is the single point of serialization for state transitions within a domain.

MUST
Each state domain MUST have exactly one logically independent commit
authority
active at any point in time.
MUST
Commit authority MUST be logically independent per domain. A single
physical
process or service MAY serve as commit authority for multiple domains,
provided
each domain's commit logic is fully isolated.
MUST
The commit authority MUST re-validate a transition if canonical state has
changed
since the transition was proposed.
MUST NOT The commit authority MUST NOT commit a transition whose prev_state does
not match
the current canonical state.
MUST
A domain MUST enter suspended state if commit authority cannot be
verified or reached.
MUST NOT A domain in suspended state MUST NOT permit new transitions to be
committed.
MUST NOT A domain in suspended state MUST NOT permit execution of new transitions.
MUST
Suspension MUST NOT invalidate or modify the existing canonical
progression.
Committed state is preserved.
MUST
A suspended domain MUST be externally observable. Silent suspension is
not permitted.

B.5.1 Pending Proposals During Suspension

When a domain enters suspended state, the following rules apply to transitions in flight:
PROPOSED transitions: Remain in PROPOSED phase. MUST NOT be committed during
suspension. MAY be re-proposed after domain resumes, but MUST be treated as new proposals
— prev_state_hash MUST be recomputed against the canonical state at resume time.
VALIDATED transitions (holding a PASS verdict): The PASS verdict is invalidated by
suspension. On domain resume, the transition MUST be re-validated against the current
canonical state before commit is permitted. The original PASS verdict MUST NOT be carried
forward.
COMMITTED transitions: Unaffected by suspension. Committed state is preserved.

EXECUTED transitions: Unaffected by suspension. Execution records are preserved.

The commit authority is responsible for invalidating stale PASS verdicts on domain resume and
for notifying proposers that their transitions require re-validation.

B.6 Cross-Domain Actions
Polaris defines correctness within a single canonical domain. Cross-domain coordination is not
defined in the core protocol.
Out of Scope — Cross-Domain Coordination:

Atomic commits spanning two or more state domains
Distributed transactions across domains
Saga coordination between domains
Shared canonical state across domain boundaries
MUST NOT Polaris does NOT guarantee atomicity across domains.
An action that requires state changes across multiple domains has no
Polaris-level
atomicity guarantee for the cross-domain interval. Each domain commit is
independently Polaris-conformant. The cross-domain composite is not.

When a business action requires state changes across multiple domains, the implementation
MUST choose one of the following approaches and document it explicitly:
Option 1: Coordinated multi-commit. Each domain commits independently. The coordinator
accepts eventual consistency between domains. No Polaris guarantee applies to the crossdomain interval. Failure handling is the responsibility of the coordinator.
Option 2: Orchestrated sequencing. An orchestrator issues proposals to each domain in
sequence. Each commit is independently Polaris-conformant within its domain. The
orchestrator is responsible for compensating transitions on failure. Compensation MUST follow
the compensating transition pattern (see B.7).

Implementation Guidance (non-normative): In many cases, the need for cross-domain
coordination indicates that domain boundaries are incorrectly defined. If two domains require
atomic coordination, merging them into a single domain may simplify correctness and eliminate
coordination complexity entirely.

B.7 Canonical Progression and Replay
The canonical progression of a domain is the complete, ordered record of all committed

transitions from genesis.
MUST
The canonical progression MUST be append-only.
MUST
Each committed transition MUST reference the hash of the preceding
committed state,
forming a verifiable chain.
MUST
A conformant implementation MUST be fully replayable from its canonical
progression.
MUST NOT Committed transitions MUST NOT be deleted, modified, or reordered.
MUST NOT Rollback MUST NOT modify the canonical progression.
MUST
Reversal MUST be implemented as a compensating transition.

B.8 Conformance Requirements
B-1 A single canonical state exists per domain at all times and cannot be in two states
simultaneously.
B-2 Canonical state is immutable after commit. No path exists for modifying committed
state outside the commit function.
B-3 Commit authority is logically independent per domain. The implementation can
demonstrate logical isolation even if a single physical node serves multiple domains.
B-4 A domain enters suspended state when commit authority cannot be verified or
reached. Suspended state is externally observable. No commits or executions occur in
suspended state.
B-5 A transition whose prev_state does not match canonical state at commit time is
rejected.
B-6 The full canonical progression can be replayed to derive current canonical state. Replay
result is identical to live canonical state.
B-7 Cross-domain actions, if present, are documented with the chosen coordination
strategy. No cross-domain atomicity is claimed.
B-8 Reversal is implemented as a compensating transition. No committed transition is
deleted or modified.

B.9 Relationship to Other Sections
Section A defines: the core invariant — no execution without commit.
Section B defines: where canonical state lives, who controls it, and what happens
when
control is lost.

Section C
Section D
Section E
Section G
Section H
Section I
authority

defines: what validation must satisfy before commit is permitted.
defines: the commit mechanism and conflict handling.
defines: how state is serialized for hashing and verification.
defines: the transition object that targets B's canonical state.
defines: the genesis that establishes B's canonical chain anchor.
defines: the execution gate that enforces B's canonical state as the

boundary for execution.
Section J defines: the trust assumptions B's guarantees depend on.

Section B does not define the commit mechanism itself. The atomic update of canonical state and
the handling of commit conflicts are specified in Section D.

B.10 Checkpoints (Non-Normative Guidance)
A checkpoint is a verified snapshot of canonical state at a specific sequence_number, enabling
replay from that point rather than from genesis.
A conformant checkpoint MUST contain: domain_id, sequence_number, canonical_state_hash
(matching resulting_state_hash of the transition at that sequence_number), canonical_state (full
state object), checkpoint_created_at (ISO 8601 UTC millisecond precision), authority_identity.
Full replay from genesis MUST remain possible regardless of whether checkpoints exist.
Checkpoints are an operational convenience, not a replacement for the canonical progression.

Section C — Validator
Status: Normative (v1.0) — Revision v1.0.1

C.1 Purpose
The validator determines whether a proposed transition is eligible to advance toward commit.
Its role is not to execute, mutate, or authorize by itself. Its role is to evaluate a proposal against the
current canonical state and the applicable constraint set and return a fully inspectable verdict.
A validator produces a verdict. It does not produce side effects.

C.2 Core Requirement
A proposed transition MUST pass validation before it may be committed.

MUST
A proposed transition MUST pass validation before it may be committed.
MUST NOT If validation fails, the transition MUST NOT be committed.
MUST NOT If validation fails, the transition MUST NOT be executed.

A PASS verdict is necessary but not sufficient for execution. Execution requires a committed
transition. The Validator determines eligibility. The Commit Authority determines progression.
Failure handling is conditional on the nature of the failure:
MUST
If a specific transition fails validation, that transition MUST be
rejected.
The domain continues normally. Other proposals are not affected.
MUST

If validation infrastructure is unavailable or cannot complete reliably,
the domain MUST enter suspended state (see Section B.5).
No transitions may be committed until validation is restored.

The distinction matters: a failed transition is a local rejection. An unavailable validator is a
domain-level failure. They are handled at different levels.

C.3 Validator Inputs
The validator evaluates a bounded, declared set of inputs. Nothing outside this set may influence
the verdict.
MUST

The validator MUST evaluate only the following classes of input:
— the proposed transition
— the current canonical state for the relevant domain
— the applicable constraint set / gate profile
— explicitly declared deterministic reference data

MUST NOT The validator MUST NOT depend on hidden mutable state.
MUST NOT The validator MUST NOT read undeclared external state.

C.4 Determinism
Validation MUST be deterministic. A validator that produces different verdicts for identical
inputs under replay is not Polaris-conformant.

MUST
set,

Given identical inputs — proposed transition, canonical state, constraint
and reference data — an implementation MUST produce the same validation

verdict.
MUST

A validator MUST produce stable results under replay.
Unstable replay behaviour is non-conformant regardless of cause.

C.5 Side Effects Prohibited
Validation is evaluative, not operative. The validator MUST NOT produce side effects.
MUST NOT A validator MUST NOT:
— mutate canonical state
— trigger external actions
— call execution endpoints
— write to systems whose outputs affect transition validity
— emit irreversible effects of any kind

The purity boundary and the specific permitted exception for observability events are defined in
Section C.10.

C.6 External Dependencies
A validator MAY read external reference data only under strict conditions.
MAY
A validator MAY read external reference data only if ALL of the following
are true:
1. the dependency is explicitly declared
2. the data is versioned or pinned to a deterministic snapshot
3. replay against the same snapshot produces the same verdict
4. the data is treated as validator input, not as live ambient context

Unpinned live reads are not permitted. The following are explicitly disallowed as validator
inputs:
current wall-clock time, unless passed as normalized input under protocol rules
live market price fetched during validation without snapshot binding
mutable cache state not included in replayable inputs
random number generation
any value that may differ between the original validation and a replay

C.7 Validation Scope
MAY

Validation MAY include:
— structural checks
— schema checks
— canonical-state consistency checks
— transition legality checks
— policy and gate checks
— bounded risk, quota, and permission checks

MUST NOT Validation MUST NOT be used to execute the transition itself.
MUST NOT Validation MUST NOT produce state changes as a consequence of running.

C.8 Validation Verdict
Field

Description

Status

transition_id

Identifier of the transition being evaluated

REQUIRED

validator_version

Version of the validator. Format: {implementation_id}:
{semver}. Example: "polaris-reference-validator:1.0.0"

REQUIRED

input_state_reference

Hash of the canonical state against which the proposal was
validated

REQUIRED

verdict

PASS or FAIL — no other values permitted

REQUIRED

failed_checks

Enumeration of checks that failed, if verdict is FAIL

REQUIRED if
FAIL

reference_data_identifiers

Identifiers of all external reference data used, if any

REQUIRED if
used

diagnostics

Human-readable description. Does not replace normative
verdict fields.

OPTIONAL

MUST
verdict MUST be either PASS or FAIL. No other values are permitted.
MUST
All required fields MUST be present and non-null.
MUST
The verdict MUST be sufficient to reconstruct the validation event during
replay.

C.9 Re-Validation Requirement
A PASS verdict does not grant permanent authority. It binds a proposal to a specific input state at
a specific point in time. If canonical state changes before commit, that binding is no longer valid.
MUST

If canonical state changes after a PASS verdict and before commit,
the transition MUST be re-validated against the new canonical state.

MUST

Re-validation is the responsibility of the Commit Authority.
The Commit Authority MUST detect the state change and trigger revalidation
before proceeding with commit.
MUST NOT A PASS verdict against a superseded canonical state MUST NOT be carried
forward
as valid authorization for commit.

C.10 Validator Purity Boundary
Observability events are permitted within the validator under narrow conditions. This is the only
permitted exception to the prohibition on side effects.
MAY

A validator MAY record observability events, provided those events are:
— append-only
— non-authoritative
— not read back as validator input
— not themselves side effects relevant to transition correctness

If an observability event influences any downstream validator input — directly or indirectly — it
is a side effect and is not permitted.

C.11 Failure Handling
MUST

restored

If validation infrastructure fails or produces an indeterminate result,
the system MUST fail closed:
— no commit may proceed
— no execution may proceed
— the domain MUST enter suspended state if validation cannot be

MUST NOT Best-effort validation is non-conformant. A system that proceeds to
commit on
incomplete or uncertain validation is not Polaris-conformant.

C.12 Profiles
Development Profile: MAY use simplified validators, provided side effects remain prohibited,
deterministic replay remains possible, and the deployment is explicitly marked developmentonly.
Production-Conformant Profile: MUST be deterministic, replayable, declare all reference
inputs, prohibit unpinned live dependencies, and fail closed on uncertainty.

C.13 Conformance Requirements
C-1 The validator is deterministic. Identical inputs produce identical verdicts under replay.
C-2 The validator produces no correctness-relevant side effects. Observability events
satisfy C.10 purity boundary.
C-3 All external reference data is explicitly declared. No undeclared or unpinned live reads
occur.
C-4 The validator re-validates on canonical-state change. The Commit Authority triggers
re-validation when state has changed since the original PASS.
C-5 The validator emits a fully inspectable verdict containing all required fields.
C-6 The validator fails closed on infrastructure failure. No commit or execution proceeds on
indeterminate validation.
C-7 A PASS verdict is not presented as sufficient for execution. The implementation
demonstrates that commit is required between PASS and execution.

C.14 Non-Normative Guidance
Most validator failures come from four mistakes:
1. Reading live external state without snapshot binding — the validator calls a live API. The
result may differ at replay time.
2. Smuggling execution into validation — the validator triggers an action as a consequence of
evaluating a proposal, before commit.
3. Using wall-clock time or randomness implicitly without passing as declared inputs.
4. Treating logs or caches as hidden validator input.

If replay does not reproduce the verdict, the validator is impure.

C.15 Relationship to Other Sections
Section A defines: the core invariant — no execution without commit.
Section B defines: canonical state and commit authority.
Section C defines: what validation must satisfy before commit is permitted.
Section D defines: the commit mechanism, conflict handling, and re-validation
trigger.
Section E defines: serialization for hashing and verification.
Section G defines: the transition object whose validation field C populates.
Section I defines: the gate that enforces that a PASS verdict alone is not
sufficient
for execution. C determines eligibility. I enforces it.
Section J defines: the boundaries of C's correctness guarantees — including that
a
compromised validator is outside Polaris scope.

The three roles — Validator (C), Commit Authority (D), and Execution Gate (I) — are logically
distinct and MUST NOT be collapsed. They may be co-located in implementation, but MUST
remain logically separable and independently inspectable.

Section D — Commit Mechanism
Status: Normative (v1.0) — Revision v1.0.0

D.1 Purpose
The commit mechanism is the single point at which canonical state advances. It is the gate
between a validated proposal and a state change that may authorize execution.
The commit mechanism does not evaluate proposals. It does not execute transitions. Its sole
responsibility is to advance canonical state atomically, at a single linearization point, on the basis
of a valid PASS verdict from the validator.
1. A transition MUST be validated before it may be committed.
2. A commit is the only mechanism by which canonical state may advance.
3. At most one transition may succeed for a given canonical predecessor.
4. Commit MUST occur at a single atomic linearization point.
5. A committed transition MUST produce a verifiable commit record.

6. Execution is permitted only after commit and MUST reference the committed transition.

D.2 Commit as Sole Progression Mechanism
MUST
A commit is the only mechanism by which canonical state may advance.
MUST NOT Canonical state MUST NOT be modified by any mechanism other than a
successful
commit of a validated transition.
MUST NOT Side-channel state updates are not permitted.
MUST NOT Helper writes that advance canonical state are not permitted.
MUST NOT Temporary mutations that are later reconciled are not permitted.

D.3 Linearization Point
Every commit must occur at a single, identifiable linearization point — the moment at which the
canonical state pointer is atomically updated.
MUST
state

Commit MUST occur at a single linearization point where the canonical
pointer is atomically updated.

MUST
The linearization point MUST be atomic. Partial commits are not
permitted.
Either the canonical state pointer advances fully, or it does not advance
at all.
MUST NOT Only one transition may advance canonical state from a given predecessor.
Two transitions with the same prev_state MUST NOT both commit
successfully.

D.4 Commit Prerequisites
Before the linearization point, the commit authority MUST verify:
1. The transition holds a valid PASS verdict from the validator.
2. The prev_state in the transition matches the current canonical state.
3. Exactly one commit authority is active for the domain.
4. The transition has not already been committed (idempotency check).

MUST NOT A transition MUST NOT be committed if any prerequisite fails.
MUST NOT The commit authority MUST NOT rely on external mutable state that is not
part
of the validated input.

D.5 Commit Record
Field

Description

Status

transition_id

Identifier of the committed transition

REQUIRED

prev_state_hash

SHA-256 hash of canonical state before commit, lowercase
hex, per Section E

REQUIRED

resulting_state_hash

SHA-256 hash of canonical state after commit, lowercase
hex

REQUIRED

validation_reference

Reference to validator verdict. Must include
validator_version and input_state_reference.

REQUIRED

committed_at

Timestamp per Section E.13 (millisecond precision, UTC)

REQUIRED

authority_identity

Identity of the commit authority. Bound to verification key
per F.7.

REQUIRED

sequence_number

Monotonically increasing integer within domain, starting
at 1

REQUIRED

signature

Ed25519 signature over canonical digest of commit
payload. Required in production.

REQUIRED
(production)

diagnostics

Human-readable notes. Non-normative.

OPTIONAL

MUST
JSON

prev_state_hash and resulting_state_hash MUST be computed using canonical
serialization as defined in Section E and encoded as lowercase hex per

E.12.
MUST
gaps.

sequence_number MUST be monotonically increasing within a domain with no
A gap in sequence_number indicates a missing or corrupted commit record

and
MUST be treated as a conformance failure.

D.6 Conflict Handling and Retry
MUST
the

A failed commit due to state conflict MUST trigger re-validation against
current canonical state before retry.

MUST NOT A conflicting transition MUST NOT be retried using a PASS verdict that
was
issued against a superseded canonical state.
MUST NOT Blind retry — retrying without re-validation — is not permitted.

D.7 Idempotency
MUST

The commit function MUST be idempotent with respect to transition_id.

MUST
the

If a transition has already been committed, a subsequent commit call for
same transition_id MUST return the existing commit record without

modifying
canonical state.
MUST NOT A duplicate commit MUST NOT advance canonical state a second time.
MUST NOT A duplicate commit MUST NOT produce a second commit record.

D.8 Commit Authority Scope
MUST
At any given time, exactly one commit authority MUST be active per
domain.
MUST
enter

If commit authority cannot be determined or reached, the domain MUST
suspended state. No transitions may be committed during suspension.

MUST NOT Commit authority MUST NOT be shared across domains.
Each domain's commit authority MUST be logically independent.

D.9 Commit Does Not Execute
MUST NOT The commit function MUST NOT execute the transition as a side effect of
committing.
MUST NOT Execution MUST NOT occur as part of the commit linearization point.
MUST
Execution is permitted only after a committed transition exists and MUST
reference
the committed transition's transition_id.
MUST NOT The roles of commit authority and execution gate MUST NOT be collapsed
such that
commit and execution are indistinguishable.

D.10 Failure Handling
MUST
If the commit cannot complete atomically, the canonical state MUST remain
unchanged.
MUST NOT A partially executed commit MUST NOT be treated as a successful commit.
MUST
If the commit infrastructure is unavailable, the domain MUST enter
suspended state.
MUST NOT The system MUST NOT proceed to execution on a commit of uncertain status.

D.11 Conformance Requirements
D-1 Canonical state advances only through the commit function. No other write path exists.
D-2 Commit occurs at a single atomic linearization point. Partial commits are not possible.
D-3 At most one transition commits successfully for a given prev_state. Linearization
violations cannot occur.
D-4 Every committed transition produces a verifiable commit record containing all
required fields.
D-5 Commit conflicts trigger re-validation before retry. Blind retry does not occur.
D-6 The commit function is idempotent. Duplicate commit calls do not advance canonical
state a second time.
D-7 Exactly one commit authority is active per domain. The domain enters suspended state
if authority is lost.
D-8 Commit and execution are logically separable. A committed transition exists as a
distinct record before execution.
D-9 The commit mechanism fails closed. Uncertain or partial commits do not result in
execution.

D.12 Relationship to Other Sections
Section A defines: the core invariant — no execution without commit.
Section B defines: canonical state, state domains, and commit authority scope.
Section C defines: validation prerequisites that must be satisfied before commit.
Section D defines: the commit mechanism, linearization, conflict handling, and
commit record.
Section E defines: canonical serialization used in commit record hashes.
Section F defines: cryptographic integrity of the commit record.
Section G defines: the transition object whose commit_record D populates.
Section H defines: the genesis that precedes sequence_number 1.
Section I defines: the execution gate — logically subsequent to D's commit.
Section J defines: the trust assumptions D's guarantees depend on.

Section E — Canonical Serialization
Status: Normative (v1.0)

E.1 Purpose
Canonical serialization defines how state is transformed into a deterministic byte representation
for hashing and verification.
Two independent implementations MUST produce identical serialized output for the same
logical state.
If serialization is not identical, hashes will diverge and the system is not interoperable.

E.2 Normative Encoding (v1)
State MUST be serialized using Canonical JSON with UTF-8 encoding and deterministic object
key ordering. No alternative encoding is permitted in v1 for interoperable systems.

E.3 General Rules
E.3.1 Encoding

Serialized output MUST be UTF-8 encoded.

No BOM (Byte Order Mark).
E.3.2 Whitespace

No insignificant whitespace is permitted.
Output MUST NOT include spaces, tabs, or line breaks outside string values.
Valid: {"a":1,"b":2} Invalid: { "a": 1, "b": 2 }

E.4 Object Key Ordering
All object keys MUST be sorted lexicographically based on UTF-8 byte ordering. Nested objects
MUST follow the same rule recursively.
Input: {"b":2,"a":1} Serialized: {"a":1,"b":2}

E.5 Data Types
E.5.1 Allowed Types

Object, Array, String, Number, Boolean, Null. No additional types are permitted.

E.6 Numbers (Critical Section)
E.6.1 General Rules

No leading zeros
No trailing zeros after decimal point
No "+" sign
Use lowercase exponential notation if needed
Valid: 1 , 1.5 , 0.01 , 1e3 Invalid: 01 , 1.500 , +1 , 1E3
E.6.2 Floating Point

Floating point values are NOT permitted in v1.
E.6.3 Disallowed Values

The following values MUST NOT appear in canonical state:
Floating point numbers
NaN

Infinity
-Infinity
If a domain model requires decimal precision, values MUST be represented as integers (scaled)
or strings with explicit semantics. Example: price of 10.50 → 1050 (integer, unit = cents) or
"10.50" (string with declared semantics).
E.6.4 String representations for large values

If a domain requires values outside the safe integer range, they MUST be represented as strings
with explicit semantics declared in the domain schema.
E.6.5 Integer Range Constraint

To ensure cross-language numeric precision, integers in canonical state objects MUST be within
the following range:
Minimum: -(2^53 - 1) = -9007199254740991
Maximum: (2^53 - 1) = 9007199254740991

This range corresponds to the safe integer range in IEEE 754 double-precision floating point,
ensuring that implementations in JavaScript and other languages using float64 for numeric
representation can parse and serialize these values without precision loss.
MUST NOT: Integer values outside this range MUST NOT appear in canonical state objects in v1.
If domain logic requires values outside this range, they MUST be represented as strings.

E.7 Strings
MUST be UTF-8
MUST follow JSON escaping rules
No normalization or transformation beyond standard JSON encoding

E.8 Arrays
Order MUST be preserved
Arrays MUST NOT be sorted
[3,1,2] ≠ [1,2,3] and MUST remain [3,1,2]

E.9 Null and Boolean
null MUST be encoded as "null"
true MUST be encoded as "true"
false MUST be encoded as "false"

E.10 Hashing Input
The exact serialized byte output is the input to the hashing function. No transformation is
allowed between serialization and hashing.

E.11 Compliance Requirement
An implementation is compliant only if:
It produces identical serialized output for identical logical state
It rejects unsupported or non-normalizable values

E.12 Hash Output Encoding
All SHA-256 hash outputs used in this protocol — including prev_state_hash,
resulting_state_hash, and genesis_hash — MUST be encoded as lowercase hexadecimal strings.
Valid: "a3f2e1d4c5b6..."
Invalid: "A3F2E1D4C5B6..." (uppercase)
Invalid: base64 encoding

MUST NOT: use uppercase, base64, or any other encoding. This applies to all hash fields
throughout the specification.

E.13 Timestamp Format
All timestamps in canonical objects — including proposed_at, committed_at, executed_at, and
initialized_at — MUST use the following format:
YYYY-MM-DDTHH:MM:SS.sssZ

Where .sss is exactly three decimal places (millisecond precision) and Z indicates UTC. No
other timezone offset is permitted.
Valid: "2025-03-28T14:32:01.087Z"
Invalid: "2025-03-28T14:32:01Z"
(missing milliseconds)
Invalid: "2025-03-28T14:32:01.000000Z" (microseconds not permitted)
Invalid: "2025-03-28T14:32:01+00:00"
(offset notation not permitted)

E.14 Relationship to Other Sections
Section B defines: canonical state — the object E serializes for hashing in
prev_state_hash
and resulting_state_hash.
Section D defines: commit record — E's canonical serialization is used to produce
the
commit payload digest that F signs.
Section F defines: cryptographic integrity — F uses E's canonical JSON
serialization as
input to SHA-256 for both state hashing and payload hashing.
Section G defines: transition object — G's proposed_state and payload fields MUST
conform
to E's rules. G's prev_state_hash is computed using E.
Section H defines: genesis state — H's initial_state and genesis hash computation
use E.
Section K defines: E-1 through E-8 conformance checklist items.
Section E is the serialization contract that makes cross-implementation hash
interoperability
possible. If two implementations disagree on E, their hashes will not match and
their
canonical progressions will be incompatible.

Section F — Cryptographic Integrity
Status: Normative (v1.0)

F.1 Purpose
Cryptographic integrity provides tamper evidence, authenticity, and independent verifiability
for committed Polaris artifacts.

Cryptography does not determine whether a transition is valid. Validation determines eligibility.
Commit authority determines canonical progression. Cryptographic integrity makes committed
artifacts independently verifiable.

F.2 Core Requirement
A production-conformant Polaris implementation MUST apply cryptographic integrity controls
to committed artifacts.
At minimum, this MUST include:
a cryptographic hash over the canonical serialized commit payload
a digital signature over the commit artifact or its canonical digest
explicit identification of the signing authority
explicit declaration of the algorithms used
A system operating without these guarantees is NOT production-conformant Polaris.

F.3 What Is Signed
The signed object MUST correspond to a canonical serialized commit payload.
Implementations MUST NOT sign ambiguous, non-canonical, or presentation-level
representations.
MUST
the

Implementations MUST sign the canonical digest of the commit payload, not
raw payload bytes directly.

MUST

The canonical digest MUST be computed as:
SHA-256( canonical_JSON_serialize( commit_payload ) )
per Section E serialization rules.

MUST

The digest bytes — 32 bytes, raw, not hex-encoded — are the input to the
Ed25519 signing function.

MUST NOT The hex-encoded string representation of the digest MUST NOT be used as
signing
input. Sign the raw bytes.

The signed payload MUST be sufficient to verify: which transition was committed, which
canonical predecessor it references, which resulting state it produced, which authority
committed it, which validation result it depended on.

F.4 Commit Payload Requirements
A production-conformant commit payload MUST include, directly or by stable reference:
transition_id
sequence_number
prev_state_hash
resulting_state_hash
validation_reference
commit_timestamp
authority_identity
algorithm_identifiers
Optional fields MAY be included, provided they are part of the canonical serialized form and do
not introduce ambiguity.

F.5 Hashing
The hash MUST be computed over the canonical serialized payload defined by the protocol. No
transformation is permitted between canonical serialization and hashing. The hash algorithm
MUST be explicitly declared.
F.5.1 Default Profile

The default hashing profile for Polaris v1 is SHA-256.
F.5.2 Two Distinct Hashing Roles

Two distinct uses of SHA-256 exist in Polaris. Implementations MUST NOT conflate them.
State hashing:

Input: canonical JSON serialization of canonical state object.
Output: prev_state_hash and resulting_state_hash.
Used in: transition object (Section G.3) and commit record (Section D.5).
Payload hashing:

Input: canonical JSON serialization of commit payload object.
Output: canonical digest used as input to Ed25519 signing (Section F.6).
Used in: commit record signature only.

Both operations use SHA-256. Both operations use canonical JSON serialization per Section E.
They operate on different objects and produce values with different semantics. Mixing them is a
conformance failure.

F.6 Signatures
The commit artifact MUST be digitally signed by the active commit authority for the relevant
domain. The signature algorithm MUST be explicitly declared.
F.6.1 Default Signature Profile

The default signature algorithm for Polaris v1 is Ed25519 as defined in RFC 8032, using the
standard (non-prehashed) variant.
MUST
—

The message input to Ed25519 signing MUST be the raw SHA-256 digest bytes
exactly 32 bytes, not hex-encoded.
Pseudocode:
digest = SHA256(canonical_JSON_serialize(commit_payload))
signature = Ed25519_sign(private_key, digest)

MUST

Implementations MUST use the standard Ed25519 variant (not Ed25519ph,
Ed25519ctx, or any prehashed variant).

The message input to the Ed25519 signing function is the raw 32-byte SHA-256 digest. Standard
Ed25519 per RFC 8032 uses SHA-512 internally as part of the signing algorithm itself — for
nonce generation and key expansion. This is transparent to the caller and is not an additional
hash of the message. It does not change what the caller passes in.
Result: sign(private_key, sha256_digest_bytes) produces an interoperable Ed25519
signature across all standard implementations regardless of their internal SHA-512 use.
Interoperability note: Implementations in Python (cryptography library), Go (crypto/ed25519),
Rust (ed25519-dalek), and Node.js (noble-ed25519) all implement standard Ed25519. Passing the
32-byte SHA-256 digest as the message parameter will produce interoperable signatures across
all of these.

F.7 Authority Identity
Every production-conformant signed commit MUST identify the authority that produced it.

MUST
Authority identity MUST be bound to a verification key that is
independently
accessible to any verifier within the deployment context.
MUST
A verifier MUST be able to retrieve the verification material — the
public key
or equivalent — without requiring access to the commit authority itself.
MUST NOT A commit artifact is non-conformant if a verifier cannot independently
retrieve
the verification material needed to check the signature without
assistance from
the signing party.

F.7.1 Verification Key Format

The verification key (public key) MUST be published and accessible in the following format:
Primary format (MUST be supported): Raw Ed25519 public key bytes encoded as lowercase
hex. Length: exactly 64 hex characters (32 bytes).
Alternative format (MAY be supported): JSON Web Key (JWK) as defined in RFC 7517, with
"kty": "OKP" , "crv": "Ed25519" , "x" (base64url-encoded public key bytes).
MUST
The primary format (lowercase hex) MUST always be available.
MUST
The verification key MUST be accessible at a stable, publicly documented
location
without authentication.
MUST NOT The verification key MUST NOT require contacting the commit authority to
retrieve.

F.8 Verification Requirement
A production-conformant implementation MUST support independent verification of
committed artifacts.
Independent verification MUST be able to determine:
1. Whether the payload hash matches the canonical serialized artifact.
2. Whether the signature is valid against the declared algorithm and authority verification
key.
3. Whether the authority identity matches the verification material independently retrieved
per F.7.

4. Whether the commit links correctly to the referenced predecessor — prev_state_hash
matches the canonical state that preceded this commit.
5. Whether sequence_number is contiguous with no gaps from the preceding committed
artifact.
6. Whether the prev_state_hash in this artifact matches the resulting_state_hash of the
preceding committed artifact in the canonical progression (chain integrity).
7. Whether the domain_id in the commit record matches the domain being verified. A commit
record produced by domain A MUST NOT be accepted as valid for domain B, even if the
signature is cryptographically valid. Cross-domain replay is a conformance failure.
If any check fails, the artifact MUST be treated as invalid. A chain in which any artifact fails any
check is non-conformant.

F.9 Relationship to Correctness
Cryptographic integrity does not replace validation. A valid signature does not imply that a
transition was admissible. A valid hash chain does not imply that validation was correct.
Cryptographic integrity proves that the committed artifact has not been altered and that it was
produced by the declared authority under the declared scheme.

F.10 Development Profile
Cryptographic integrity MAY be disabled only under an explicitly configured development
profile.
A development profile without cryptographic integrity:
MAY be used for learning, testing, or local reference implementations
MUST NOT be presented as production-conformant Polaris
MUST NOT claim cryptographic tamper evidence
MUST remain explicit in configuration and documentation
Cryptographic integrity MUST NOT be silently disabled.

F.11 Failure Handling
MUST NOT If production cryptographic integrity cannot be reliably applied at
commit time,
the commit MUST NOT succeed.

MUST
domain

If verification material is unavailable, invalid, or indeterminate, the

MUST enter suspended state. No transitions may be committed until
cryptographic
integrity can be reliably established.

Best-effort signing is non-conformant. Unsigned production commits are non-conformant.
Silent continuation without cryptographic integrity is non-conformant.

F.12 Key Management Boundary
This specification requires verifiable authority identity and valid signatures, but does not fully
standardize operational key management.
Out of scope for core Polaris v1:
key generation ceremony details
HSM requirements
rotation procedure design
certificate lifecycle policy
organizational trust governance
F.12.1 Key Rotation and Historical Verifiability

When commit authority rotates signing keys:

MUST
Active signing capability and passive verification accessibility are
distinct:
Active signing: The retiring key MUST NOT be used to sign new commits
after
rotation is complete.
Passive verification: The retiring key's public key MUST remain
independently
accessible for the lifetime of any canonical progression it has signed,
or until
verified checkpoints signed by the new authority exist for all
transitions signed
by the retiring key.
MUST
A retiring key MAY be revoked from operational signing use. Its public
key MUST
remain accessible for verification purposes after revocation.
MUST NOT The public key of a retired signing authority MUST NOT be deleted or made
inaccessible while any unarchived committed transitions reference it.

F.13 Non-Repudiation and Auditability
Production-conformant cryptographic integrity strengthens auditability and origin verification,
but deployment-specific legal non-repudiation claims depend on external trust and governance
frameworks.
The core protocol therefore guarantees cryptographic verifiability of committed artifacts, not
universal legal non-repudiation.

F.14 Compliance Requirement
A production-conformant Polaris cryptographic integrity implementation is conformant only if:
it hashes the canonical serialized commit payload
it signs the canonical digest (raw bytes) of the commit artifact
it declares the algorithms used
it identifies the signing authority with independently accessible verification key
it supports independent verification including chain integrity (F.8 check 6)
it fails closed when integrity cannot be established

F.15 Relationship to Other Sections
Section B defines: commit authority — the entity whose key signs commit records
per F.6.
Section D defines: commit record — the object F signs.
Section E defines: canonical JSON serialization — F uses E's rules for both state
hashing
and commit payload hashing. F depends on E for all byte-level
operations.
Section G defines: transition object — G's commit_record field contains the
signed artifact
F produces.
Section H defines: genesis state — H's genesis_hash uses the same SHA-256 +
canonical JSON
approach as F's state hashing.
Section J defines: F's scope boundaries. J.7 explicitly lists key management, HSM
requirements, and rotation ceremonies as out of scope. F.12
defines the
verifiability constraint that key management must satisfy.
Section K defines: F-1 through F-7 conformance checklist items.

Section F is the integrity layer. Without F, the canonical progression is a structured record. With
F, it is a tamper-evident, independently verifiable chain.

Section G — Transition Object
Status: Normative (v1.0)

G.1 Purpose
The transition object is the fundamental unit of the Polaris protocol. Every operation in a Polaris
system is represented as a transition — a proposed change from one canonical state to another,
subject to validation and commit before execution is permitted.
A transition is not a command. It is not a request. It is a structured record of intent that must pass
through the full Polaris lifecycle before it produces any side effect.
MUST

Every proposed state change in a Polaris system MUST be represented as a
transition object conformant with this section.
MUST NOT State changes MUST NOT occur outside of the transition lifecycle.

G.2 Lifecycle
A transition passes through four mandatory phases. No phase may be skipped. No phase may
occur out of order.
PROPOSED ──► VALIDATED ──► COMMITTED ──► EXECUTED
│
│
▼
▼
REJECTED
REJECTED
(validation)
(commit conflict
or re-validation)

PROPOSED: The transition exists as a structured object referencing the current canonical state.
No validation has occurred. No commit has occurred. No execution is permitted.
VALIDATED: The validator has evaluated the transition and returned a PASS verdict.
VALIDATED is necessary but not sufficient for commit. If canonical state changes before
commit, the transition must be re-validated.
COMMITTED: The commit authority has atomically advanced canonical state. A commit record
exists. Execution is now permitted. The transition is permanently part of the canonical
progression.
EXECUTED: Side effects have been produced. All side effects reference the transition_id of this
committed transition.
REJECTED: The transition has been permanently rejected. It does not advance canonical state
and does not permit execution.
MUST
→

A transition MUST pass through phases in the order: PROPOSED → VALIDATED

COMMITTED → EXECUTED
MUST NOT A transition MUST NOT advance to COMMITTED without a current PASS
verdict.
MUST NOT A transition MUST NOT advance to EXECUTED without reaching COMMITTED.
MUST NOT Phase order MUST NOT be reversed or skipped for any reason.

G.3 Normative Schema
Field

Type

Description

Status

transition_id

string
(UUID
v4)

Globally unique identifier. Immutable once
assigned.

REQUIRED

Field

Type

Description

Status

domain_id

string

Domain identifier. Format: {domain_type}.
{domain_identifier}.

REQUIRED

prev_state_hash

string
(hex)

SHA-256 hash of canonical state at proposal
time, lowercase hex per E.12.

REQUIRED

proposed_state

object

Full intended canonical state after
transition. Section E rules apply. Floats not
permitted.

REQUIRED

payload

object

Domain-specific input data. Read by
validator. Does not directly become
canonical state.

REQUIRED

phase

enum

Current lifecycle phase: PROPOSED,
VALIDATED, COMMITTED, EXECUTED,
REJECTED.

REQUIRED

proposed_at

string
(ISO
8601)

Timestamp of creation per E.13. Immutable.

REQUIRED

validation

object

Validation verdict per Section C.8. Null until
validation completes.

REQUIRED when
VALIDATED

commit_record

object

Commit record per Section D.5. Null until
committed.

REQUIRED when
COMMITTED

execution_record

object

Execution record. Null until executed.

REQUIRED when
EXECUTED

agent_id

string

Identifier of proposing agent or component.
Optional.

OPTIONAL

parent_transition_id

string
(UUID
v4)

transition_id of causally preceding
committed transition. See G.6.

CONDITIONAL

metadata

object

Non-normative implementation-specific
data. Must not affect semantics.

OPTIONAL

sequence_number

integer

Set exclusively by the Commit Authority at commit time, per Section D.5.
NOT present in transition proposals. Proposers MUST NOT include
sequence_number in proposals. Presence of sequence_number in a proposal
is SCHEMA_INVALID.

COMMIT-AUTHORITY ONLY — not a proposal field

MUST
All REQUIRED fields MUST be present and non-null.
MUST
phase MUST accurately reflect the current lifecycle state at all times.
MUST NOT transition_id MUST NOT be reused across transitions, domains, or systems.
MUST NOT proposed_at MUST NOT be modified after the transition is created.
MUST NOT metadata MUST NOT be used as validator input.
MUST NOT metadata MUST NOT affect commit or execution semantics.

G.4 Field Constraints
transition_id
MUST be a UUID v4. Assigned at proposal time. Immutable. Globally unique.
domain_id
Format: {domain_type}.{domain_identifier}
MUST: domain_type MUST be lowercase alphanumeric. Underscore permitted.
MUST: domain_identifier MUST be non-empty. Unique within deployment for
domain_type.
MUST NOT: A domain_id not conforming to this format is SCHEMA_INVALID.
Valid: instrument.BTCUSD, account.user_42, portfolio.fund_alpha
Invalid: BTCUSD (missing type), Instrument.BTCUSD (uppercase), instrument/BTCUSD
(slash)
prev_state_hash
MUST be SHA-256 of canonical JSON of canonical state at proposal time, lowercase
hex per E.12.
MUST match current canonical state hash at commit time.
If not: reject, re-validate.
proposed_state
MUST be valid canonical JSON per Section E.
MUST NOT contain floating point values.
     Floating point values are prohibited by Section E.6.2. Detection occurs
     at the transition schema layer (Section G), not the serialization layer
     (Section E). Section E defines the prohibition. Section G enforces it.
     The rejection reason is SCHEMA_INVALID.
MUST NOT contain NaN, Infinity, or -Infinity.
phase
MUST be one of: PROPOSED | VALIDATED | COMMITTED | EXECUTED | REJECTED
MUST advance only in the permitted direction.
sequence_number
MUST NOT be included in transition proposals.
Set exclusively by the Commit Authority at commit time.
A proposal containing sequence_number is SCHEMA_INVALID.
The Commit Authority sets sequence_number atomically at the linearization
point per Section D.5. It is not a hint, not an input, not a negotiation.

G.5 Canonical Serialization of the Transition Object
When a transition object is serialized for hashing, signing, or storage, it MUST follow canonical
JSON rules per Section E.

MUST
prev_state_hash MUST be computed from the canonical serialization of the
canonical
state object, not from the transition object itself.
MUST NOT The transition object MUST NOT be hashed using non-canonical
representations.

G.6 Agent-to-Agent Causal Chain
MUST
parent_transition_id MUST be declared if the transition was causally
preceded by
another committed transition in the system.
MAY

parent_transition_id MAY be omitted only for:
— genesis transitions (no committed predecessor exists)
— transitions that are genuinely causally independent of all prior
committed
transitions in the system
MUST NOT parent_transition_id MUST NOT be omitted when a causal predecessor
exists.
An implementation that omits parent_transition_id when a predecessor
exists is
non-conformant.
MUST

If parent_transition_id is declared, the referenced transition MUST be in
COMMITTED phase at the time of proposal.

MUST NOT parent_transition_id MUST NOT reference a PROPOSED, VALIDATED, REJECTED,
or
EXECUTED transition.

G.7 Immutability Rules
Immutable from proposal (MUST NOT change after creation): transition_id, domain_id,
prev_state_hash, proposed_state, payload, proposed_at
Populated on phase transition (null until relevant phase): validation, commit_record,
execution_record
Mutable during lifecycle: phase — advances forward only, never regresses

MUST NOT Immutable fields MUST NOT be modified after the transition object is
created.
MUST NOT phase MUST NOT regress to an earlier value.
MUST NOT A populated validation, commit_record, or execution_record MUST NOT be
modified
or replaced once set.

G.8 Rejection Semantics
Rejection reasons MUST be one of:
SCHEMA_INVALID — transition object is malformed or missing required fields. Detected
before the validation pipeline runs. The validator is not invoked for SCHEMA_INVALID.
VALIDATION_FAILED — validator returned FAIL verdict. The transition object was structurally
valid but did not pass the constraint set.
COMMIT_CONFLICT — prev_state_hash did not match canonical state at commit time.
Another transition committed in the interval.
REVALIDATION_FAILED — re-validation after a commit conflict returned FAIL. The transition
cannot proceed against the updated canonical state.
DOMAIN_SUSPENDED — the domain is in suspended state. No transitions may be committed
until the domain is ACTIVE. This is a domain-level condition, not a transition-level failure.
INFRASTRUCTURE_FAILURE — validation or commit infrastructure is unavailable or
produced an indeterminate result. Domain enters suspended state per A.9 and B.5.
DUPLICATE_TRANSITION_ID — a transition with this transition_id has already been
committed or is currently in the commit pipeline. Detected at the Commit Authority
before validation runs. The existing committed transition is unaffected. The duplicate
is discarded entirely.

No other rejection reasons are valid in a conformant implementation.
The complete enumeration is: SCHEMA_INVALID, VALIDATION_FAILED, COMMIT_CONFLICT,
REVALIDATION_FAILED, DOMAIN_SUSPENDED, INFRASTRUCTURE_FAILURE,
DUPLICATE_TRANSITION_ID.
Implementations MUST NOT use free-text rejection reasons in place of these enumerated values.
MUST NOT A REJECTED transition MUST NOT be committed.
MUST NOT A REJECTED transition MUST NOT be executed.
MUST NOT A REJECTED transition MUST NOT be modified and re-submitted as the same
transition_id.
MAY
A new transition MAY be proposed with a new transition_id based on the
same intent.

G.9 Conformance Requirements
G-1 Every proposed state change is represented as a transition object with all required
fields present and non-null.

G-2 The phase field accurately reflects the current lifecycle state at all times. No regression.
No skipping.
G-3 Immutable fields are not modified after creation.
G-4 proposed_state and payload conform to Section E serialization rules. Floats are absent.
G-5 A transition does not advance to COMMITTED without a current PASS verdict against
the current canonical state.
G-6 A transition does not advance to EXECUTED without reaching COMMITTED.
G-7 REJECTED transitions are not committed, executed, or reused under the same
transition_id.
G-8 parent_transition_id is declared when a causal predecessor exists. Not omitted when
known.
G-9 If parent_transition_id is declared, the referenced transition is in COMMITTED phase.
G-10 domain_id conforms to {domain_type}.{domain_identifier} format.
G-11 Only the seven defined rejection reasons are used. No free-text bypass.

G.10 Relationship to Other Sections
Section A
Section B
Section C
Section D
Section E
Section F
Section H
for the

defines: the core invariant the gate enforces.
defines: the canonical state G's prev_state_hash references.
defines: the validation verdict embedded in G's validation field.
defines: the commit record embedded in G's commit_record field.
defines: serialization rules for proposed_state, payload, and hashing.
defines: cryptographic integrity of the commit_record.
defines: genesis state — H's genesis_hash becomes G's prev_state_hash
first transition. Without H, G's prev_state_hash has no

verified origin.
Section I defines: execution gate — the component that reads G's commit_record to
authorize
execution. G's execution_record is populated only after I
permits.
Section J defines: the trust assumptions under which G's causal chain guarantees
hold.

Section G is logically prior to all other sections. It defines the unit that the protocol operates on.

Section H — Genesis State
Status: Normative (v1.0)

H.1 Purpose
Every state domain must have a well-defined starting point. The genesis state is that starting
point — the initial canonical state from which all transitions are derived and against which the
first transition's prev_state_hash is computed.
MUST
Every state domain MUST have exactly one genesis state.
MUST
The genesis state MUST be established before any transition is proposed.
MUST NOT A transition MUST NOT be proposed against a domain that has not been
initialized
with a genesis state.

H.2 Genesis State Object
Field

Type

Description

Status

polaris_version

string

Protocol version. MUST be "1.0" for this
specification. No prefix or suffix.

REQUIRED

domain_id

string

Domain identifier per G.4 format rules.

REQUIRED

initialized_at

string (ISO
8601)

Timestamp per E.13. Immutable. Used in
genesis hash computation.

REQUIRED

authority_identity

string

Identity of commit authority that initialized
this domain.

REQUIRED

initial_state

object

The canonical state of the domain at
initialization. Conforms to Section E.

REQUIRED

sequence_number

integer

Always 0 for genesis.

REQUIRED —
always 0

genesis_hash

SHA-256
lowercase hex

SHA-256 of canonical serialization
excluding genesis_hash field itself.

REQUIRED

MUST
initial_state MUST conform to Section E serialization rules.
MUST
initial_state MUST NOT contain floating point values.
MUST
sequence_number MUST be 0 for all genesis state objects.
MUST
genesis_hash MUST be computed as specified in H.3.
MUST NOT The genesis state object MUST NOT be modified after initialization.
MUST
polaris_version MUST be set to the numeric version string without prefix
or suffix.
Valid for this specification: "1.0"
MUST NOT be "v1.0", "1", "v1", "1.0.0", or any other variant.

H.3 Genesis Hash Computation
The genesis hash is the cryptographic anchor of the entire canonical progression.
Genesis hash computation procedure:
1. Construct the genesis state object with all required fields populated,
EXCLUDING the genesis_hash field itself.
2. Serialize using canonical JSON per Section E:
— UTF-8 encoding, no BOM
— No insignificant whitespace
— Lexicographic key ordering
— No floating point values
3. Compute SHA-256 over the canonical serialized bytes.
4. Encode the result as lowercase hex per E.12.
5. Set genesis_hash to this value.

Critical: The genesis_hash field MUST be excluded from the serialization before hashing.
Including it would create a circular dependency — you cannot hash a field whose value depends
on the hash of the object containing it. The procedure is: serialize without genesis_hash → hash →
set genesis_hash.

The genesis hash is the prev_state_hash for the first transition proposed in this domain.

H.4 First Transition Semantics
MUST
The first transition in a domain MUST set prev_state_hash equal to the
domain's

genesis_hash.
MUST
The first committed transition MUST have sequence_number 1.
MUST NOT The first transition MUST NOT have a parent_transition_id.
MUST
The commit authority MUST verify that prev_state_hash equals genesis_hash
when
committing the first transition, exactly as it would verify against any
other
canonical state hash.

H.5 Domain Initialization Procedure
1. Commit authority constructs the genesis state object with all required fields.
2. Commit authority computes genesis_hash per H.3.
3. Commit authority stores the genesis state object as the canonical record for
sequence_number 0.
4. Domain status transitions to ACTIVE.
5. Commit authority is now ready to accept transition proposals.
MUST
Initialization MUST be performed by the commit authority designated for
the domain.
MUST
The genesis state object MUST be stored and available for independent
verification.
MUST NOT A domain MUST NOT accept transition proposals before initialization is
complete.
MUST NOT A domain MUST NOT have more than one genesis state object.

H.5.1 Re-initialization Rejection

An attempt to initialize a domain that already has a genesis state is an initialization failure — not
a transition rejection. It MUST be handled at the initialization layer, before any transition
pipeline is invoked.
Initialization rejection reason: DOMAIN_ALREADY_INITIALIZED
DOMAIN_ALREADY_INITIALIZED — an initialization was attempted for a domain that already
has a genesis state. The existing genesis state is preserved unchanged. The attempted
initialization is discarded entirely.

MUST NOT A DOMAIN_ALREADY_INITIALIZED event MUST NOT modify the existing genesis
state.
MUST NOT DOMAIN_ALREADY_INITIALIZED MUST NOT be returned from the transition
validation or
commit pipeline. It is an initialization-layer rejection only.
MUST
The rejection MUST be logged with: attempted domain_id, existing
genesis_hash,
rejection reason, timestamp.

H.6 Domain Re-initialization
A domain is initialized exactly once. Re-initialization is not permitted within the same domain
identity.
MUST NOT An existing domain MUST NOT be re-initialized.
MUST NOT The genesis state of an existing domain MUST NOT be replaced or modified.
MUST NOT genesis_hash MUST NOT be recomputed or altered after initialization.
MAY
If a fresh start is required, a new domain_id MUST be used. The old
domain's
canonical progression remains intact and independently verifiable.

H.7 Replay from Genesis
MUST
Full replay MUST begin from the genesis state object.
MUST
Replay MUST verify that the genesis_hash of the stored genesis state
object matches
the prev_state_hash of the transition with sequence_number 1.
MUST
Replay MUST verify that resulting_state_hash of transition N matches
prev_state_hash
of transition N+1 for all N ≥ 1.
MUST
Replay MUST verify that sequence_numbers are contiguous with no gaps from
0 through
the highest committed sequence_number.
MUST
The canonical state produced by replay MUST be identical to the live
canonical state.

Replay verification sequence:

Step 1: Load genesis state object.
Verify: genesis_hash = SHA-256(canonical_serialize(genesis_without_hash))
Set: current_hash = genesis_hash, current_state = initial_state,
expected_sequence = 1
Step 2: For each committed transition T (ordered by sequence_number):
Verify: T.sequence_number = expected_sequence
Verify: T.prev_state_hash = current_hash
Apply: current_state = T.proposed_state
Verify: T.resulting_state_hash = SHA-256(canonical_serialize(current_state))
Set:
current_hash = T.resulting_state_hash, expected_sequence += 1
Step 3: After all transitions:
Verify: current_state = live canonical state
Verify: current_hash = live canonical state hash
If any verification fails → canonical progression is non-conformant.

H.8 Relationship to Suspended State
A domain that has been initialized but whose commit authority is unavailable enters suspended
state per Section B.5. The genesis state is preserved. Replay remains possible. Forward
progression is blocked until commit authority is restored.
A domain that has not yet been initialized is not a suspended domain. It is an uninitialized
domain. These are distinct conditions.
Domain states:
UNINITIALIZED — genesis state does not exist. No transitions may be proposed.
ACTIVE
— genesis state exists, commit authority reachable.
SUSPENDED
— genesis state exists, commit authority unreachable.
MUST NOT An UNINITIALIZED domain MUST NOT be treated as SUSPENDED.
MUST NOT An UNINITIALIZED domain MUST NOT accept transition proposals.

H.9 Conformance Requirements
H-1 Every domain has exactly one genesis state object, stored and available for
independent verification.
H-2 genesis_hash is computed by the defined procedure: canonical serialize without
genesis_hash field → SHA-256 → lowercase hex.

H-3 sequence_number in the genesis state object is 0. The first committed transition has
sequence_number 1.
H-4 The first transition's prev_state_hash equals the domain's genesis_hash.
H-5 Genesis state is immutable after initialization. Never modified or replaced.
H-6 No transitions are accepted before initialization is complete.
H-7 Full replay starting from genesis produces the current canonical state identically.
H-8 UNINITIALIZED and SUSPENDED domain states are distinguishable and handled
differently.
H-9 domain_id in genesis state conforms to {domain_type}.{domain_identifier} format per
Section G.4.
H-10 polaris_version is "1.0" — no prefix, no suffix, no alternative formats.

H.10 Relationship to Other Sections
Section B defines: canonical state and domain boundaries.
Section D defines: commit records starting from sequence_number 1.
Section E defines: canonical JSON serialization used in genesis hash computation.
Section G defines: the transition object — H's genesis_hash becomes G's
prev_state_hash for
the first transition. H is what makes the first G meaningful.
Section I defines: execution gate — H's domain status
(ACTIVE/SUSPENDED/UNINITIALIZED) is
checked in I's gate check 3.
Section J defines: the trust assumptions that protect H. A compromised storage
layer can
delete H. J defines that this is outside Polaris scope.

Genesis is not the first transition. It is what makes the first transition possible.

Section I — Execution Gate
Status: Normative (v1.0)

I.1 Purpose
The Execution Gate is the third and final logical role in the Polaris protocol. It is the enforcement
point of the core invariant: no side effect may occur unless it is the result of a committed,
validated transition.

The Validator determines eligibility. The Commit Authority determines canonical progression.
The Execution Gate determines whether execution is permitted at all.
The Execution Gate does not evaluate the transition. It does not advance canonical state. Its sole
responsibility is to verify that a committed transition exists and to permit or block execution
accordingly.
MUST
Every execution attempt MUST pass through the execution gate.
MUST NOT Execution MUST NOT occur by any path that bypasses the gate.
MUST NOT The execution gate MUST NOT be optional or configurable in productionconformant
deployments.

I.2 The Gate Decision
The execution gate makes a binary decision: PERMIT or BLOCK. There is no third outcome.
There is no partial execution. There is no best-effort mode.
MUST
The gate decision MUST be PERMIT or BLOCK. No other outcome is valid.
MUST
PERMIT requires all gate checks to pass.
MUST
BLOCK on any failed check. A single failed check is sufficient to block
execution.
MUST NOT Partial execution is not permitted under any circumstances.
MUST NOT Best-effort execution is not permitted under any circumstances.

I.3 Gate Checks
The execution gate performs three checks in order. All three must pass for execution to be
permitted.
Check

Condition for PERMIT

Block reason if failed

1. Commit
exists

The transition is in COMMITTED phase. A
commit record exists and is retrievable.

EXECUTION_WITHOUT_COMMIT

2. Transition
identity

The transition_id presented for execution
matches the transition_id in the commit record.

TRANSITION_MISMATCH

3. Domain
active

The domain is in ACTIVE state. Not
SUSPENDED or UNINITIALIZED.

DOMAIN_NOT_ACTIVE

MUST
All three checks MUST pass for execution to be permitted.
MUST
Checks MUST be performed in the order listed.
MUST
The gate MUST record the outcome of every evaluation with transition_id
and reason.
MUST NOT Check 1 MUST NOT be skipped on the assumption that a prior step has
already
verified commit status. The gate is the authoritative enforcement point.

Note: DOMAIN_NOT_ACTIVE is a gate block reason, not a transition rejection reason. It
indicates the gate check failed at the domain state level. DOMAIN_SUSPENDED (Section G.8) is
the corresponding transition-level rejection reason that may be issued when a transition is
formally rejected due to domain suspension.

I.4 Execution Record
MUST
MUST

Every permitted and completed execution MUST produce an execution record.
The execution record MUST be attached to the transition object as
transition.execution_record per Section G.3.
MUST
The execution record MUST contain:
— transition_id (the committed transition that authorized this
execution)
— executed_at (ISO 8601 UTC timestamp per Section E.13, millisecond
precision)
— outcome (COMPLETED or FAILED)
— side_effects (enumeration of side effects produced, if any)
MUST
All side effects produced during execution MUST reference the
transition_id of the
authorizing committed transition.
MUST NOT Side effects MUST NOT be produced without referencing a committed
transition_id.

I.5 Idempotency
MUST
A transition in EXECUTED phase with outcome COMPLETED MUST NOT be
executed again.
MUST
A transition in EXECUTED phase with outcome FAILED MAY be retried,
provided the
committed transition still exists and the domain is ACTIVE.
MUST NOT Re-execution of a COMPLETED transition MUST NOT produce additional side
effects.
MUST
If re-execution of a FAILED transition occurs, the execution record MUST

be updated
or a new execution record appended. Prior records MUST NOT be deleted.

Critical idempotency boundary: The execution gate prevents double-execution at the protocol
level. However, side effects must also be idempotent or explicitly guarded at the implementation
level. Idempotency at the gate and at the side-effect receiver are independent requirements.

I.6 Role Separation
MUST NOT The execution gate MUST NOT perform validation.
MUST NOT The execution gate MUST NOT advance canonical state.
MUST NOT The execution gate MUST NOT be collapsed with the commit function such
that commit
and execution are indistinguishable.
MUST
The gate logic MUST be independently testable in isolation — verifiable
without
running the full validator or commit pipeline.
MUST
These three roles MUST remain logically separable and independently
inspectable
even when co-located: Validator (evaluates admissibility), Commit
Authority
(determines canonical progression), Execution Gate (permits or blocks
side effects).

The most common collapse failure is a function that commits and immediately executes in the
same call with no separable record between them. The test is simple: can you show an external
verifier the committed transition record before execution occurred? If not, the roles are collapsed.

I.7 Gate in Agent Systems
MUST
Every agent action that produces a side effect MUST pass through the
execution gate.
MUST
Each agent's execution MUST reference the transition_id of the committed
transition
that authorized that agent's action.
MUST NOT An agent MUST NOT produce side effects based on a PASS verdict alone.
A committed transition is required.
MUST NOT An upstream agent's committed transition MUST NOT authorize execution for
a
downstream agent. Each agent's execution requires its own committed
transition.

I.8 Failure Handling
MUST
If gate infrastructure is unavailable or produces an indeterminate
result,
the gate MUST block execution.
MUST
If the commit record cannot be retrieved or verified, the gate MUST block
execution.
MUST NOT The gate MUST NOT permit execution on uncertainty. Uncertain = blocked.
MUST NOT A "break glass" or emergency bypass of the execution gate is not
permitted in
production-conformant deployments. If a bypass exists, the deployment is
non-conformant.

There is no emergency override. An execution that cannot be authorized by a committed
transition does not occur.

I.9 Observability
MUST
The gate MUST log every evaluation with: transition_id, gate decision
(PERMIT or
BLOCK), block reason (if BLOCK), evaluated_at timestamp.
MUST
Gate logs MUST be append-only.
MUST NOT Gate logs MUST NOT be used as validator input.
MUST NOT Gate logs MUST NOT affect gate decisions.

I.10 Conformance Requirements
I-1 Every execution attempt passes through the execution gate. No bypass path exists in
production-conformant deployments.
I-2 The gate performs all three checks in order: commit exists, transition identity matches,
domain is active.
I-3 A single failed check blocks execution. Partial execution does not occur.
I-4 Every permitted and completed execution produces an execution record with all
required fields including executed_at per E.13.
I-5 All side effects reference the transition_id of the authorizing committed transition.
I-6 COMPLETED executions are not re-executed. FAILED executions may be retried
against the same committed transition.

I-7 The gate is logically separable from the Validator and Commit Authority. Gate logic is
independently testable.
I-8 In agent systems, each agent's execution is authorized by its own committed transition.
I-9 Gate infrastructure failure results in BLOCK, not PERMIT. Uncertain = blocked.
I-10 Gate evaluations are logged with transition_id, decision, reason, and timestamp.

I.11 Relationship to Other Sections
Section A
Section B
Section C
Section D
Section G
Section H
check 3.
Section J
committed

defines: the core invariant the gate enforces.
defines: domain active/suspended state checked in gate check 3.
defines: the Validator — logically prior to the gate, distinct role.
defines: the commit record verified in gate check 1 and 2.
defines: the transition object and its phase, updated to EXECUTED.
defines: domain state (ACTIVE/SUSPENDED/UNINITIALIZED) checked in gate
defines: I's trust assumptions — I enforces that execution requires a
transition, but cannot detect a commit authority that

committed
fraudulently. J.4 defines this as outside I's scope.
Three audit records form the complete verifiable lifecycle of a transition:
transition.validation.verdict
→ what the Validator decided
transition.commit_record
→ what the Commit Authority committed
transition.execution_record
→ what the Execution Gate permitted
All three MUST exist for a transition in EXECUTED phase.
Any missing record indicates a conformance failure.

Section J — Threat Model
Status: Normative (v1.0)

J.1 Purpose
The threat model defines the security and integrity properties that Polaris provides, the
conditions under which those properties hold, and the boundaries beyond which the protocol
makes no claims.
Polaris is a causal integrity protocol. Its guarantees are about the verifiability of what happened,
in what order, and that the record has not been altered. It is not an access control system. It is not

a Byzantine fault-tolerant consensus protocol. It is not a cryptographic authentication system for
agents or users.
Understanding what Polaris does not protect against is as important as understanding what it
does.

J.2 Trust Assumptions
The Polaris guarantees hold only when the following trust assumptions are satisfied. If any
assumption is violated, the guarantee that depends on it does not hold.
T1 — Commit authority is honest The commit authority commits transitions faithfully
according to the protocol. It does not selectively omit transitions, forge commit records, or
advance canonical state outside the commit function. Polaris cannot protect against a commit
authority that is itself the adversary.
T2 — Validator is deterministic and correct The validator evaluates transitions correctly and
deterministically. A validator that is compromised or incorrectly implemented may issue PASS
verdicts for transitions that should fail. Polaris enforces that a PASS verdict exists before commit
— it does not verify that the verdict is correct.
T3 — Canonical state store is append-only in practice The state store preserves committed
transitions and does not permit modification or deletion outside the protocol. If the underlying
storage is compromised and transitions are deleted, Polaris provides detection via hash chain
verification — but not prevention.
T4 — Cryptographic primitives are not broken SHA-256 and Ed25519 are computationally
secure. A system in which these primitives are broken falls outside the threat model of Polaris v1.
T5 — Reference data used in validation is trustworthy External reference data pinned for use in
validation reflects accurate information at the time of pinning. Polaris guarantees that the same
pinned data produces the same verdict at replay — it does not guarantee that the pinned data
was correct when first used.
MUST
A conformant deployment MUST document which trust assumptions it
satisfies and by
what mechanism.
MUST NOT A deployment MUST NOT claim Polaris guarantees that depend on trust
assumptions
the deployment does not satisfy.

J.3 What Polaris Protects Against
Under the trust assumptions in J.2, Polaris provides the following guarantees:

Post-hoc manipulation of committed transitions. A committed transition cannot be
altered without breaking the hash chain. Any modification is detectable by any verifier.
Deletion of committed transitions. The sequence_number and hash chain together make
gaps detectable. A progression with a missing transition cannot pass replay verification.
Execution without a committed transition. The execution gate enforces this at the
protocol level.
Unauthorized advancement of canonical state. Only the commit function advances
canonical state. Side-channel writes are detectable via hash chain verification.
Ambiguity about causal order. The canonical progression is linear and ordered. The
sequence_number and prev_state_hash chain establish an unambiguous causal order.
Silent failure of validation or commit infrastructure. Polaris fails closed. Infrastructure
failure produces a block or suspended state — never a silent proceed.
Execution based on a stale validation verdict. Re-validation is required when canonical
state changes before commit.
Undetected forgery of the commit record by a non-authority party. Ed25519 signatures
bind the commit record to the commit authority's key. A party without the private key
cannot produce a valid signature. Any forgery attempt is detectable by any verifier with
access to the public key.
Cross-domain replay of commit records. A commit record signed by commit authority of
domain A cannot be accepted as valid for domain B. The domain_id field is part of the
signed payload. A verifier MUST check domain_id matches the domain under verification
before accepting a commit record as valid.

J.4 What Polaris Does Not Protect Against
The following threats are outside the scope of Polaris. A deployment that requires protection
against these threats must implement additional controls at the infrastructure or governance
layer.
A compromised commit authority. If the entity holding commit authority is the adversary,
it can commit arbitrary transitions and produce valid signatures. Polaris will record these
faithfully — it will not detect that they are wrong. Trust assumption T1 must hold.
A compromised or incorrectly implemented validator. A validator that issues PASS for
transitions that should fail will cause those transitions to be committed and executed. Trust
assumption T2 must hold.
Byzantine failures across multiple Polaris nodes. Polaris does not define a distributed
consensus mechanism. Polaris is not a BFT protocol.

Incorrect reference data in validation. If a validator uses pinned reference data that was
itself incorrect before pinning, the resulting verdicts will be reproducible but wrong.
Compromise of the private key used for signing. Key management and key security are
outside the scope of Polaris. Trust assumption T4 must hold at the key management level.
Denial of service against commit infrastructure. Polaris defines what must happen in
suspended state — it does not define how to prevent suspension from being induced.
Correctness of business logic in the payload. Polaris validates structural admissibility, not
business intent.
Legal non-repudiation beyond cryptographic verifiability. Polaris provides cryptographic
proof of authority. Whether this constitutes legal non-repudiation depends on external
legal frameworks.

J.5 The Central Guarantee
Given trust assumptions T1–T5 hold, a verifier with access to the genesis state object and the
canonical progression of a domain can independently determine:
1. The exact sequence of transitions that advanced canonical state, in the exact order they
were committed.
2. That no transition in the sequence was modified after commit.
3. That no transition was inserted into the middle of the sequence after the fact.
4. That no transition was deleted from the sequence after the fact.
5. That every execution that occurred was authorized by a committed transition in the
sequence.
6. That the commit authority that produced each commit record held the declared signing key
at the time of commit.
These six properties are what "causal integrity" means in Polaris. Nothing more. Nothing less.

J.6 Attacker Model
Capability

In
Scope

Polaris Response

Modify a committed transition

YES

Hash chain breaks. Detectable at next replay verification.

Delete a transition from
progression

YES

Sequence gap detected. Hash chain breaks.

Capability

In
Scope

Polaris Response

Insert a forged transition

YES

Hash chain breaks unless attacker holds signing key.

Reorder transitions

YES

prev_state_hash chain breaks. Detectable immediately.

Trigger execution without commit

YES

Gate blocks. Non-conformant path does not exist in
spec.

Compromise commit authority

NO

T1 violated. Outside Polaris scope.

Compromise validator logic

NO

T2 violated. Outside Polaris scope.

Steal signing key

NO

T4 violated at key management layer. Outside Polaris
scope.

Feed incorrect reference data

NO

T5 violated. Outside Polaris scope.

Force domain suspension (DoS)

NO

Infrastructure concern. Outside Polaris scope.

J.7 Explicitly Out of Scope
The following security properties are not provided by Polaris and must be addressed by the
deployment at the infrastructure or governance layer:
Access control: who may propose transitions
Authentication: verifying the identity of proposing agents
Authorization policy: whether a proposer is permitted to propose a given transition
Key management: generation, rotation, and revocation of signing keys
Byzantine fault tolerance: consensus across multiple potentially adversarial nodes
Confidentiality: Polaris does not encrypt state or transition data. All canonical state is
readable by any party with access to the canonical progression. Deployments with
confidentiality requirements MUST implement encryption at the storage and transport
layer, outside the Polaris protocol.

Availability guarantees: Polaris defines behavior under unavailability, not prevention
Legal non-repudiation: jurisdiction-specific legal claims beyond cryptographic verifiability
Correctness of validator business logic
Correctness of reference data used in validation

MUST NOT A conformant deployment MUST NOT represent Polaris as providing security
properties
listed in this section as out of scope.
MUST NOT Marketing materials, documentation, or API descriptions for a Polaris
implementation
MUST NOT claim guarantees that exceed the boundaries defined in J.3 and
J.5.

J.7.1 Confidentiality

Polaris canonical state and transition records are not confidential by design. The protocol's
verifiability guarantee requires that commit records be readable by external verifiers.
Common approaches in deployments requiring both Polaris and confidentiality: encrypt
canonical state at rest (provide decryption keys to authorized verifiers under governancedefined conditions); use commitment schemes (commit to hash of encrypted state rather than
plaintext); separate public and private state domains (sensitive data referenced by identifier, not
included in canonical state).
The confidentiality approach is a deployment-level decision. Polaris does not constrain it and
does not define it.

J.8 Relationship to Other Sections
Section A
Section B
Section C
Section D
Section F
Section G
the

defines: the core invariant Polaris enforces.
defines: domain boundaries and canonical state.
defines: Validator requirements — honest Validator is T2.
defines: commit mechanism — honest Commit Authority is T1.
defines: cryptographic integrity — key security is T4.
defines: the transition object — J's protections are specifically about
integrity of G's committed state and the detectability of

tampering.
Section H defines: genesis state — J's guarantee that the canonical progression
is
verifiable starts at H.
Section I defines: execution gate — J's guarantee that execution cannot occur
without
commit is enforced by I.
Section K defines: the conformance process that operationalises J.2's requirement
to
document trust assumptions.

Every guarantee in Sections B through F is conditional on the trust assumptions in J.2. Section J
is not an addendum. It is the frame within which the entire protocol operates.

Section K — Conformance
Status: Normative (v1.0)

K.1 Purpose
This section defines what it means to be Polaris-conformant, how conformance is established in
v1, and what the path to mechanically verified conformance looks like in v1.1.
Conformance is the mechanism that gives "Polaris-conformant" meaning beyond self-assertion.
Without a defined conformance process, the label is marketing. With it, the label is a verifiable
claim.
MUST NOT An implementation MUST NOT claim Polaris conformance without satisfying
the
requirements of this section.
MUST NOT An implementation MUST NOT claim production-conformant status under a
development
profile. See Section A.7.

K.2 Conformance Levels
Level 1 — Self-Declared Conformance (v1 interim) The implementation satisfies all normative
requirements in Sections B through J, as demonstrated by completing the self-declaration
checklist in K.4.

Claim format: "Polaris v1 conformant (self-declared)"
Level 2 — Suite-Verified Conformance (v1.1, forthcoming) The implementation passes the
Polaris Core Invariant Suite (PCIS-1) as specified in K.5, in addition to the self-declaration
checklist.

Claim format: "Polaris v1.1 conformant (PCIS-1 verified, commit: [hash])"

MUST NOT An implementation MUST NOT claim Level 2 conformance before PCIS-1 is
published
and the implementation has passed it.
MUST NOT Level 1 conformance MUST NOT be represented as equivalent to Level 2
conformance.
The distinction MUST be visible in any public conformance claim.

K.3 Self-Declaration Requirements
MUST
MUST

MUST
request.

The self-declaration MUST be a written document, not a verbal claim.
The self-declaration MUST address each checklist item in K.4 with one of:
— SATISFIED: a description of how the requirement is met
— NOT APPLICABLE: a justification for why it does not apply
— NOT SATISFIED: an explanation and a remediation plan
The self-declaration MUST be retained and available for inspection upon

The self-declaration is the document a regulator, auditor, or counterparty will ask to see. Write it
as if a technically competent reviewer who has read this specification will read it. "Yes, we do this"
is not sufficient. "We do this by mechanism X, as evidenced by test Y and configuration Z" is
sufficient.

K.4 Complete Conformance Checklist
Reference convention: each item is identified as {Section letter}-{Item number} . When
citing an item, use format "K.4 B-3" or "K.4 F-5" to avoid ambiguity with section numbers
elsewhere.
A conformant implementation satisfies all 66 items below.
Section B — State Domain
B-1 A single canonical state exists per domain at all times. Cannot be in two states
simultaneously.
B-2 Canonical state is immutable after commit. No path exists to modify committed state
outside the commit function.
B-3 Commit authority is logically independent per domain. Logical isolation demonstrated
even if a single physical node serves multiple domains.
B-4 Domain enters suspended state when commit authority unreachable. Externally
observable. No commits or executions in suspended state.

B-5 Conflict rejection. Transition with non-matching prev_state_hash is rejected at commit
time.
B-6 Full replay from genesis produces current canonical state identically.
B-7 Cross-domain actions documented. No cross-domain atomicity claimed.
B-8 Compensating transitions used for reversal. No committed transition deleted or
modified.
Section C — Validator
C-1 Deterministic validation. Identical inputs produce identical verdicts under replay.
C-2 No correctness-relevant side effects. Observability events satisfy C.10 purity boundary.
C-3 All external reference data declared. No undeclared or unpinned live reads.
C-4 Re-validation on state change. Commit Authority triggers re-validation when state has
changed.
C-5 Inspectable verdict. All required verdict fields present.
C-6 Fail closed. No commit or execution proceeds on indeterminate validation.
C-7 PASS not sufficient for execution. Implementation demonstrates commit required
between PASS and execution.
Section D — Commit Mechanism
D-1 Commit as sole progression mechanism. No other write path to canonical state.
D-2 Single atomic linearization point. Partial commits not possible.
D-3 At most one commit per predecessor. Linearization violation cannot occur.
D-4 Verifiable commit record. Every committed transition produces commit record with all
required fields.
D-5 Re-validation before retry. Commit conflicts trigger re-validation. Blind retry does not
occur.
D-6 Idempotent commit. Duplicate commit calls do not advance canonical state a second
time.
D-7 One commit authority per domain. Domain enters suspended state if authority is lost.
D-8 Commit and execution separable. Committed transition exists as distinct record before
execution.
D-9 Fail closed on commit uncertainty. Uncertain or partial commits do not result in
execution.
Section E — Canonical Serialization
E-1 Identical serialized output for identical state. Two conformant implementations
produce byte-for-byte identical output.

E-2 No floats, NaN, Infinity, -Infinity. Disallowed values absent from all canonical state
objects.
E-3 Deterministic key ordering. UTF-8 lexicographic byte ordering applied recursively.
E-4 No insignificant whitespace. No spaces, tabs, or line breaks outside string values.
E-5 UTF-8 encoding, no BOM.
E-6 Standard JSON string escaping. No normalization beyond standard JSON.
E-7 Array order preserved. Arrays MUST NOT be sorted.
E-8 Booleans and null explicitly encoded. true/false/null as defined.
Section F — Cryptographic Integrity (production only)
F-1 Canonical state hashing active. prev_state_hash and resulting_state_hash computed
via SHA-256 over canonical JSON, lowercase hex.
F-2 Commit payload signing active. Ed25519 standard variant, over SHA-256 digest of
canonical JSON commit payload. Raw bytes signed, not hex-encoded.
F-3 Two SHA-256 uses not conflated. State hashing and payload hashing operate on
distinct objects.
F-4 Authority identity independently verifiable. Verifier can retrieve public key (lowercase
hex) without assistance from signing party.
F-5 Chain integrity verifiable. prev_state_hash in artifact N matches resulting_state_hash
of artifact N-1.
F-6 Cross-domain replay protection. domain_id in commit record verified against domain
under verification.
F-7 Fail closed on crypto failure. Domain enters suspended state if cryptographic integrity
cannot be established.
Section G — Transition Object
G-1 All required fields present. Every transition object contains all required fields, non-null.
G-2 Phase accurate and forward-only. No regression. No skipping.
G-3 Immutable fields not modified after creation.
G-4 proposed_state E-conformant. No floats. Section E rules satisfied.
G-5 A transition does not advance to COMMITTED without a current PASS verdict.
G-6 A transition does not advance to EXECUTED without reaching COMMITTED.
G-7 REJECTED transitions not committed, executed, or reused under same transition_id.
G-8 parent_transition_id declared when causal predecessor exists.
G-9 If parent_transition_id declared, referenced transition is in COMMITTED phase.
G-10 domain_id format conformant: {domain_type}.{domain_identifier}.

G-11 Only the seven defined rejection reasons used. No free-text bypass.
Section H — Genesis State
H-1 Exactly one genesis per domain. Stored and available for independent verification.
H-2 genesis_hash computed correctly. SHA-256 of canonical JSON excluding genesis_hash
field, lowercase hex.
H-3 sequence_number = 0 at genesis. First committed transition has sequence_number 1.
H-4 First transition prev_state_hash = genesis_hash. Chain anchored correctly.
H-5 Genesis immutable. Never modified or replaced after initialization.
H-6 No transitions before initialization. Domain rejects proposals until genesis established.
H-7 Replay from genesis correct. Produces current canonical state identically.
H-8 UNINITIALIZED distinct from SUSPENDED. Handled differently. Not conflated.
H-9 domain_id in genesis state conforms to {domain_type}.{domain_identifier} format per
G.4.
Section I — Execution Gate
I-1 No bypass path. Every execution attempt passes through the gate in production.
I-2 All three gate checks performed in order.
I-3 Single failed check blocks execution. Partial execution not possible.
I-4 Execution record produced with all required fields including executed_at per E.13.
I-5 Side effects reference transition_id of authorizing committed transition.
I-6 COMPLETED not re-executed. FAILED may retry against same committed transition.
I-7 Gate independently testable. Logically separable from Validator and Commit Authority.
I-8 Each agent execution independently authorized. Upstream committed transitions do
not authorize downstream agent execution.
I-9 Infrastructure failure → BLOCK. Gate evaluations logged.
Section J — Threat Model
J-1 Trust assumptions documented. Written record of which trust assumptions from J.2 the
deployment satisfies and by what mechanism.
J-2 No out-of-scope claims. Deployment does not claim security properties listed as out of
scope in J.7.

K.5 Polaris Core Invariant Suite — PCIS-1 (Specification)
PCIS-1 is the mechanical conformance test suite for Polaris v1.1. This section specifies what it will

test. When implemented, passing PCIS-1 constitutes Level 2 conformance.
MUST
MUST
MUST

PCIS-1 MUST be language-neutral. Tests via a defined interface.
PCIS-1 MUST be open source and independently runnable.
PCIS-1 MUST produce a machine-readable result containing:
— implementation identifier
— test suite version
— per-test result: PASS, FAIL, or SKIP with reason
— overall result: CONFORMANT or NON-CONFORMANT
— result hash: SHA-256 of the canonical result document

Note: Not all K.4 checklist items are mechanically testable. PCIS-1 covers the core invariants and
structurally verifiable requirements. Items that require human judgment — particularly J-1 and J2 — are verified through the self-declaration process in K.3, not through the test suite.

Test

Description

Invariant

T01

Execution blocked without commit. Attempt execution of PROPOSED transition.
Gate must block with EXECUTION_WITHOUT_COMMIT.

Invariant 1

T02

Execution blocked with forged commit record. Cryptographic verification must fail.

Invariant 1,
F

T03

Single canonical successor. Submit two transitions with identical prev_state_hash.
Exactly one commits. Second rejected with COMMIT_CONFLICT.

Invariant 2

T04

Deterministic validation. Submit identical transition twice against identical
canonical state. Verdicts must be identical.

Invariant 3

T05

Canonical serialization identity. Serialize identical state twice. Byte-for-byte
identical. SHA-256 hashes match.

Invariant 4

T06

Float rejection. Include float in proposed_state. SCHEMA_INVALID before
validation runs.

E,
Invariant 4

T07

Causal binding. Execute committed transition. Verify execution_record references
transition_id. Attempt side effect without transition_id — must fail.

Invariant 5

T08

Progression integrity — gap detection. Delete transition at sequence N. Run replay.
Gap detected.

Invariant 6

T09

Chain integrity — hash break detection. Modify proposed_state of committed
transition N. Run replay. Hash chain break detected at N.

Invariant 6,
F

T10

Suspended state on authority loss. Make commit authority unreachable. Verify
domain enters suspended state. No commit succeeds. State externally observable.

B.5, A.9

T11

Re-validation on state change. Obtain PASS. Commit different transition first.
Attempt original with stale PASS. Re-validation triggered. Stale PASS not accepted.

C.9, D.6

T12

Genesis hash correctness. Compute genesis_hash independently. Compare to
stored value. Must match exactly.

H

T13

Full replay identity. Replay from genesis. Compare to live canonical state. Byte-forbyte identical.

B, H,
Invariant 6

T14

Cryptographic signature verification. Retrieve commit record. Independently verify
Ed25519 signature using publicly accessible verification key. Must succeed without
assistance from commit authority.

F.6, F.7

T15

Role isolation. Test Validator without commit or execution. Test Execution Gate
without Validator or commit pipeline. Both must be independently testable.

C.15, I.7

K.6 Conformance Claim Format
Level 1 — self-declared:
This implementation claims Polaris v1 conformance (self-declared).
Specification version: Polaris Protocol Specification v1.0
Self-declaration date: [ISO 8601 date]
Self-declaration document: [URL or reference]
Sections B through J: all normative requirements satisfied
Section K: self-declaration completed [date]
Self-declaration covers:
K.4 B-1 through B-8 ✓
K.4 C-1 through C-7 ✓
K.4 D-1 through D-9 ✓
K.4 E-1 through E-8 ✓
K.4 F-1 through F-7 ✓
K.4 G-1 through G-11 ✓
K.4 H-1 through H-9 ✓
K.4 I-1 through I-9 ✓
K.4 J-1 through J-2 ✓
Trust assumptions satisfied: [list from J.2 with mechanisms]
Known gaps: [none | list with remediation plans]
Contact for verification: [contact]

Level 2 — PCIS-1 verified:
This implementation claims Polaris v1.1 conformance (PCIS-1 verified).
Specification version: Polaris Protocol Specification v1.1
PCIS-1 version: 1.0
PCIS-1 result: CONFORMANT
PCIS-1 result hash: [SHA-256 of canonical result document]
PCIS-1 run date: [ISO 8601 date]
Self-declaration document: [URL]
Trust assumptions satisfied: [list from J.2 with mechanisms]
PCIS-1 result document: [URL]

MUST NOT A conformance claim MUST NOT omit the conformance level.
MUST NOT A conformance claim MUST NOT omit the specification version.
MUST NOT A Level 1 claim MUST NOT use the Level 2 claim format or imply mechanical
verification.

K.7 Interim Period Commitment
The interim period is the time between v1 publication and PCIS-1 availability. During this period,
Level 1 self-declared conformance is the only available mechanism.
PCIS-1 is targeted for release within 12 months of the first production-conformant
implementation being publicly announced. Progress is tracked at: github.com/polarisspecs/polaris-protocol/milestones
The Polaris Protocol maintainers commit to:
1. Not revoking Level 1 conformance claims made in good faith during the interim period
when PCIS-1 becomes available, provided the implementation passes PCIS-1 within 6
months of PCIS-1 publication.
Level 1 claims made after PCIS-1 is published are still valid, but MUST be distinguished from
Level 2 claims in all public representations.

K.8 Relationship to Other Sections
Section A defines: A.8 which references K for conformance process.
Section B–J define: normative requirements that K.4 aggregates.
Section K defines: how conformance is established, claimed, and verified.
Section L defines: what Polaris is not — L's positioning is enforced by K as the
mechanism
that prevents Polaris labels on non-conformant
implementations.

Section L — Polaris vs Other Patterns
Status: Informative (v1.0)

This section contains no normative requirements. Its purpose is to position Polaris relative to
known architectural patterns.

L.1 Purpose
Polaris shares vocabulary with several established patterns — event sourcing, saga, distributed
transactions, and audit logging. The similarities are real. The differences are fundamental. This
section draws the line precisely so that a reader familiar with any of these patterns can locate
Polaris accurately without conflating it with something else.

L.2 Polaris vs Event Sourcing
Event sourcing is the most common conflation. Both maintain an append-only history of state
changes. The surface resemblance is strong.
What they share

Where they diverge

Append-only record of
state changes.

Event sourcing records what happened. Polaris enforces that nothing
happens without prior authorization through the commit gate.

Current state
reconstructed by replaying
history.

Event sourcing does not require that events be validated before they are
appended. Polaris mandates validation before commit.

Hash chain or sequence for
ordering and integrity.

Event sourcing does not define an execution gate. Events may trigger side
effects by any mechanism. Polaris requires side effects to be explicitly
gated on committed transitions.

Replayability as a design
goal.

Event sourcing is a storage and reconstruction pattern. Polaris is an
execution control protocol. The record is a consequence of the protocol, not
its purpose.

Relationship: Polaris is not event sourcing. Polaris produces an event-sourced record as a side
effect of enforcing commit-gated execution. You can implement Polaris on top of an event store.
You cannot implement Polaris by adopting event sourcing alone — the execution gate and
commit-before-execution invariant are not part of the event sourcing pattern.

L.3 Polaris vs Saga Pattern
The saga pattern manages long-running business transactions across multiple services using a
sequence of local transactions with compensating actions on failure.
What they share

Where they diverge

Compensating actions for reversal
rather than rollback.

Saga coordinates the sequence of actions. Polaris authorizes
each individual action. They operate at different levels.

Acknowledgment that distributed
atomicity is not available.

Saga does not require that each step be validated before
execution. Polaris mandates it.

Sequential state progression across
steps.

Saga manages orchestration logic. Polaris does not manage
orchestration — it constrains what each step may do.

Relationship: Polaris and saga are complementary, not competing. A multi-agent system may
use a saga-style orchestrator to sequence agent actions, while each agent action is individually
governed by Polaris. The orchestrator handles the flow. Polaris handles the authorization and
integrity of each step.

L.4 Polaris vs Distributed Transaction Coordinator
Distributed transaction coordinators — two-phase commit, XA transactions — provide atomic
commits across multiple participants.
What they share

Where they diverge

The word "commit" and the
concept of an atomic state
change.

Distributed coordinators provide atomicity across multiple
participants. Polaris provides atomicity within a single domain. Crossdomain atomicity is explicitly out of scope for Polaris.

The concept of a
prepare/validate phase before
commit.

Distributed coordinators are infrastructure — they move data. Polaris
is a protocol — it governs execution.

Failure semantics — if commit
fails, state does not change.

Distributed coordinators do not require cryptographic integrity or
execution gating. Polaris requires both.

Relationship: Polaris is not a distributed transaction coordinator. It does not provide crossdomain atomicity. Where a distributed coordinator provides atomicity across participants,
Polaris provides causal integrity within a domain. They solve different problems.

L.5 Polaris vs Audit Logging
Audit logging records what happened for review after the fact. Polaris produces a verifiable
record of what happened.

What they share

Where they diverge

A record of actions taken, in
order, with timestamps.

Audit logs are written after execution. Polaris commits before execution.

Used for compliance, review,
and incident investigation.

Audit logs can be modified, deleted, or forged without built-in detection.
Polaris's hash chain makes modification detectable.

Append-only design intent.

Audit logs record what happened. They do not prevent unauthorized
execution. Polaris prevents unauthorized execution.

Structured records with
fields and identifiers.

Audit logs are self-reported by the system being audited. Polaris's
cryptographic signing creates a record independently verifiable without
trusting the reporting system.

Relationship: Audit logging is reactive. Polaris is preventive. An audit log tells you what
happened. Polaris proves that what happened was authorized before it happened, and that the
record has not been altered since. A system with Polaris produces an audit log as a by-product. A
system with only an audit log does not have Polaris.

L.6 Polaris vs Access Control Systems
Access control systems — RBAC, ABAC, policy engines — determine who is permitted to do
what.
What they share

Where they diverge

A gate that permits or blocks
actions.

Access control determines who may act. Polaris determines whether a
specific proposed action has been validated and committed before
execution.

Policy evaluation before
action.

Access control is stateless with respect to execution history. Polaris is
stateful — every execution is bound to a specific committed transition.

Used in regulated and
compliance-sensitive systems.

Access control does not produce a verifiable causal record. Polaris does.

Relationship: Access control and Polaris are complementary. Access control answers "is this
agent permitted to propose this transition?" Polaris answers "has this transition been validated,
committed, and is execution now authorized?" A complete system needs both. Access control
governs who may enter the Polaris pipeline. Polaris governs what exits it.

L.7 Polaris vs Blockchain and Distributed Ledger Technology
Blockchain and distributed ledger technologies (DLT) are the most common frame applied to
Polaris by technically experienced readers. The surface resemblance is strong: both maintain
append-only records, both use hash chains, both use cryptographic signing.
What they share

Where they diverge

Append-only record of state
changes with cryptographic
integrity.

Blockchain achieves consensus among mutually distrusting parties
without a central authority. Polaris assumes a defined commit authority
and makes no claims about consensus.

Hash chain linking each
record to its predecessor.

Blockchain's chain serves consensus — it allows distrusting nodes to
agree on canonical history. Polaris's chain serves verifiability — it allows
any party to verify that a trusted commit authority produced an unaltered
record.

Tamper-evident history.

Blockchain is designed for adversarial environments where any
participant might be malicious. Polaris assumes a trusted commit
authority (T1).

Independent verifiability.

Blockchain achieves verifiability through distributed replication. Polaris
achieves verifiability through cryptographic signing by a known
authority. Different mechanisms, different threat models.

Relationship: Polaris is not a blockchain. It does not solve the Byzantine generals problem. It
does not provide consensus among mutually distrusting parties. It assumes trust in the commit
authority and uses cryptography to make the authority's actions verifiable.

A blockchain may be used as the storage layer for a Polaris canonical progression. This is valid.
But the blockchain properties — decentralization, permissionless participation, consensus — are
not Polaris properties.
The choice: if you have a designated trusted commit authority, Polaris is appropriate. If you need
consensus among parties who do not trust each other, a blockchain is appropriate.

L.8 Polaris vs OpenTelemetry and Distributed Tracing
OpenTelemetry (OTel) is the most common observability framework engineers will compare to
Polaris. Both produce structured records of system activity.

What they share

Where they diverge

Structured records of system
activity with timestamps and
identifiers.

OTel records what happened — after it happened. Polaris commits
before execution — the record precedes and authorizes the action.

Causal ordering of events.

OTel's trace context propagates correlation IDs. Polaris's
prev_state_hash chain creates cryptographic causal binding. OTel traces
can be dropped. Polaris's chain cannot be broken without detection.

Used for compliance and
audit purposes.

OTel traces are self-reported by the system being observed. Polaris
records are independently verifiable — a verifier does not need to trust
the reporting system.

Spans and traces connecting
distributed operations.

OTel does not block or authorize execution. It observes it. Polaris blocks
execution without a committed transition.

Relationship: OTel and Polaris are complementary. OTel tells you what your system did. Polaris
proves what your system was authorized to do. A Polaris-conformant system can and should
emit OTel traces alongside Polaris commit records. They serve different audiences: OTel serves
developers debugging behavior, Polaris serves auditors verifying authorization.

The test: can an external auditor verify that action X was authorized before it occurred, using
only publicly accessible records, without trusting any party involved? OTel cannot satisfy this
test. Polaris can.

L.9 Summary — One Line Each
Event Sourcing
You have the storage pattern. You are missing the execution gate and the
commit-before-execution invariant.
Saga Pattern
You have the orchestration pattern. Polaris governs individual steps within
the saga, not the saga itself.
Distributed Transaction Coordinator
You have cross-participant atomicity. Polaris provides intra-domain causal
integrity, not cross-domain atomicity.
Audit Logging
You have a reactive record. Polaris is preventive authorization that produces
a verifiable record as a by-product.

Access Control
You have permission checking. Polaris provides execution gating bound to a
committed, verifiable causal record.
Blockchain / DLT
You have consensus among mutually distrusting parties. Polaris assumes a
trusted commit authority and provides causal integrity, not distributed
consensus.
OpenTelemetry / Distributed Tracing
You have observability after execution. Polaris is authorization before
execution.
They are complementary, not competing.

None of these patterns is wrong. None of them is Polaris. Polaris solves one problem precisely:
ensuring that no side effect occurs unless it is the result of a committed, validated transition, and
that this fact is independently verifiable after the fact.

L.10 Relationship to Other Sections
Section A defines: the core invariant that distinguishes Polaris from all seven
patterns above.
Section J defines: the boundaries of Polaris guarantees — knowing what Polaris
does not provide
is the practical version of L's theoretical positioning.
Section K defines: how to verify that an implementation is actually Polaris and
not one of the
seven patterns above with a Polaris label.

