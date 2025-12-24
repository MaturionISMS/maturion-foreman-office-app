# Implementation Strategy — Memory Era + Watchdog Era Alignment

## 0. Metadata
- Date:
- Owner: Johan Ras
- Source Surveys:
  - ARCH-ALIGN-01 (Architecture Readiness Alignment)
  - MEM-AUTH-01 (Memory Authority Boundary Audit)
  - FM-RESP-01 (Foreman Memory Responsibility Gap Analysis)
  - WD-OBS-01 (Watchdog Observability Readiness)

## 1. Objective
Align FM runtime architecture and operational controls with governance canon introduced in G-COG-A2/A3 and commissioning governance (G-C2/C3/C4).

## 2. Executive Summary (Current State)
- Governance canon is strong and non-contradictory.
- Runtime architecture is missing required state machines and integration points.
- Observability is defined in canon but not yet implemented or exposed.

## 3. Blocking Gaps (Must Address Before Build Execution Features)
### 3.1 Memory Lifecycle State Machine (BLOCKING)
Define runtime lifecycle states and transitions; define ownership; define failure transitions.

### 3.2 CHP ↔ Memory Integration Architecture (BLOCKING)
Define when/how CHP reads allowed memory; how proposals are generated; how proposals are routed; audit logging.

### 3.3 Memory State Observability (BLOCKING)
Define telemetry/query surfaces for Foreman and Watchdog; audit trail query semantics; dashboard targets.

## 4. Non-Blocking Improvements (Clarity + Operations)
### 4.1 Foreman Role Canon Clarifications
Explicitly enumerate memory constraint supervision and memory integrity enforcement in Foreman POLC duties.

### 4.2 Watchdog Implementation Readiness
Create required directory structures; define daily/weekly report artifact generation plan; define escalation artifact locations.

## 5. Workstreams and Sequencing
- WS1: Architecture Contracts (state machines, integration points, failure modes)
- WS2: Observability + Audit Query Surfaces
- WS3: Proposal Workflow Runtime (queue, review, decision, notify)
- WS4: Canon Clarifications (Foreman role, cross-references)
- WS5: Build Console Features (after WS1–WS3)

## 6. Acceptance Criteria
- Deterministic memory lifecycle state model exists and is referenced by FM runtime.
- CHP reads are allowlist-only and auditable.
- No canonical memory writes are possible from CHP or builders.
- Foreman and Watchdog can observe memory state and audit trails without introspection.
- Proposal-only path is implemented with human governance review (no auto-promotion).

## 7. Issue Queue
(links)
