# QA-to-Red Specification

**Version:** 1.0  
**Status:** Phase 4.4 Deliverable  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Authority:** Derived from FRS (Phase 4.2) and Architecture Spec (Phase 4.3)  
**Canonical Location:** `/QA_TO_RED_SPEC.md`

---

## Governance Statement

This QA-to-Red Specification is the **binding contract** for:
- Builder task assignment (Phase 4.5)
- Build-to-Green execution (Wave 1.0+)
- QA validation and gating
- Progress measurement and failure localization

All QA units in this specification are **derived exclusively** from:
- **`FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md`** (Version 1.0, Phase 4.2)
- **`FM_ARCHITECTURE_SPEC.md`** (Version 1.0, Phase 4.3)
- **`ARCHITECTURE_TRACEABILITY_MATRIX.md`** (Version 1.0, Phase 4.3)

No QA implementation or execution may proceed without explicit reference to and alignment with this QA-to-Red Specification.

---

## Constitutional Hierarchy

```
Governance Repository (Constitutional Authority)
    ↓
BUILD_PHILOSOPHY.md (Supreme Build Authority)
    ↓
docs/governance/FM_APP_DESCRIPTION.md (Authoritative Product Intent - Phase 4.1)
    ↓
FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md (Functional Contract - Phase 4.2)
    ↓
FM_ARCHITECTURE_SPEC.md (Architecture Contract - Phase 4.3)
    ↓
QA_TO_RED_SPEC.md (THIS DOCUMENT - Phase 4.4)
    ↓
QA_TRACEABILITY_MATRIX.md (QA Inventory - Phase 4.4)
    ↓
Builder Task Assignment (Phase 4.5 - BLOCKED until QA-to-Red accepted)
    ↓
Build-to-Green Execution (Wave 1.0+ - BLOCKED)
```

**Rules:**
- All QA units MUST trace to FRS requirements
- All QA units MUST trace to architecture components
- QA IDs are immutable once assigned
- QA must be RED before implementation starts
- QA must be 100% GREEN before completion
- Zero test debt permitted

---

## 1. QA Suite Purpose and Enforcement Role

### 1.1 Purpose

The QA-to-Red suite serves as:

1. **Deterministic Acceptance Contract**: Defines objective, machine-verifiable criteria for Build-to-Green completion
2. **Non-Coder Orchestration Interface**: Enables builder task assignment and progress tracking without code review
3. **Failure Localization System**: Allows precise identification of build failures by QA ID
4. **Progressive Build Gateway**: Enables partial Build-to-Green by QA range with mandatory gate enforcement
5. **Governance Enforcement Mechanism**: Prevents scope creep and ensures requirements traceability

### 1.2 Enforcement Role

The QA-to-Red suite operates under the following enforcement model:

**Pre-Implementation Phase (QA-to-Red):**
- All QA units MUST be defined before any implementation code is written
- All QA units MUST be in RED state (failing) before Build-to-Green starts
- QA RED state proves that functionality does not yet exist
- If QA is GREEN before build starts, there is NOTHING TO BUILD (governance violation)

**Implementation Phase (Build-to-Green):**
- Builders receive QA ranges (e.g., QA-CONV-001 to QA-CONV-010)
- Builders implement code ONLY to make assigned QA units pass
- Builders iterate until 100% of assigned QA units are GREEN
- Builders report completion only when assigned QA is 100% GREEN

**Completion Phase (Validation):**
- 100% QA GREEN is MANDATORY for build completion
- 99% passing = TOTAL FAILURE
- ANY test failure = BUILD BLOCKED
- Zero test debt permitted
- No skipped tests (.skip(), .todo())
- No partial passes accepted

### 1.3 Operational Characteristics

**Indexability:**
- Every QA unit has a unique, immutable identifier
- QA IDs enable precise task assignment and progress tracking
- QA IDs enable failure localization without code inspection

**Sequenceability:**
- QA units have defined ordering within domains
- Dependencies between QA units are explicit
- Builders can be assigned sequential QA ranges

**Traceability:**
- Every QA unit traces to specific FRS requirements
- Every QA unit traces to specific architecture components
- Bidirectional traceability ensures completeness

**Evidence-Based:**
- Every QA unit defines expected evidence when GREEN
- Evidence is machine-readable and auditable
- Evidence proves build completion objectively

---

## 2. QA ID Scheme

### 2.1 QA ID Format

**Format:**
```
QA-<DOMAIN>-<SEQUENCE>
```

**Components:**

1. **Prefix:** `QA-` (immutable, universal)
2. **Domain Code:** 2-10 character identifier for subsystem (e.g., `CONV`, `DASH`, `PARK`)
3. **Sequence Number:** 3-digit zero-padded sequence within domain (e.g., `001`, `002`, `015`)

**Examples:**
- `QA-CONV-001` — First QA unit in Conversational Interface domain
- `QA-DASH-015` — Fifteenth QA unit in Dashboard domain
- `QA-GOV-003` — Third QA unit in Governance Enforcement domain

### 2.2 Domain Codes

Domain codes map directly to architecture subsystems:

| Domain Code | Subsystem | Description |
|-------------|-----------|-------------|
| `CONV` | Conversational Interface | Persistent conversations, messaging, clarification |
| `DASH` | Dashboard | Status model, drill-down, executive view |
| `PARK` | Parking Station | Idea intake, discussion, conversion flow |
| `INTENT` | Intent Processing | Intent intake, clarification loop, requirement spec, approval |
| `EXEC` | Execution Orchestration | Build orchestration, state management, visibility |
| `ESC` | Escalation & Supervision | Ping system, escalation, silence detection, inbox |
| `GOV` | Governance Enforcement | Governance loading, validation, supremacy enforcement |
| `ANALYTICS` | Analytics | Metrics dashboard, metrics engine, cost tracking |
| `CROSS` | Cross-Cutting | Memory, authority, notification, evidence, audit, watchdog |
| `E2E` | End-to-End | Full workflow integration tests |

### 2.3 Sequence Numbering Rules

1. **Sequential Assignment:** QA IDs within a domain are assigned sequentially starting from 001
2. **No Gaps:** Sequence numbers must be contiguous (no gaps in numbering)
3. **Immutability:** Once assigned, a QA ID NEVER changes
4. **Deprecation:** Deprecated QA units retain their ID and are marked as DEPRECATED (not renumbered)
5. **Ordering:** Sequence numbers imply logical ordering within domain

### 2.4 Immutability Rules

**Immutable Properties:**
- QA ID (never changes)
- Domain code (never changes)
- Sequence number (never changes)

**Mutable Properties:**
- Name (can be clarified)
- Description (can be refined)
- Requirements mapping (can be updated if requirements change)
- Architecture mapping (can be updated if architecture changes)
- Expected evidence format (can be refined)

**Deprecated QA Units:**
- When a QA unit is no longer needed, it is marked as DEPRECATED
- Deprecated QA IDs are NOT reused
- Deprecated QA IDs are NOT renumbered
- Deprecated QA units remain in the inventory for audit trail

### 2.5 QA ID Parsing and Validation

**Valid QA ID Pattern:**
```regex
^QA-[A-Z0-9]{2,10}-[0-9]{3}$
```

**Validation Rules:**
- Must start with "QA-"
- Domain code must be 2-10 uppercase alphanumeric characters
- Sequence must be exactly 3 digits
- Domain code must be registered in domain code table
- Sequence must be unique within domain

---

## 3. QA Domains and Architecture Mapping

### 3.1 Domain-Subsystem Mapping

Each QA domain corresponds to an architecture subsystem defined in `FM_ARCHITECTURE_SPEC.md`:

**CONV Domain → Conversational Interface Subsystem (Section 2.1)**
- Components: CONV-01 through CONV-05
- Covers: Persistent conversations, message handling, FM-initiated conversations, clarification, UI rendering

**DASH Domain → Dashboard Subsystem (Section 2.2)**
- Components: DASH-01 through DASH-04
- Covers: RAG status model, drill-down navigation, executive view, dashboard rendering

**PARK Domain → Parking Station Subsystem (Section 2.3)**
- Components: PARK-01 through PARK-04
- Covers: Idea intake, parking store, discussion management, parking UI

**INTENT Domain → Intent Processing Subsystem (Section 2.4)**
- Components: INTENT-01 through INTENT-04
- Covers: Intent intake, clarification loop, requirement spec generation, approval management

**EXEC Domain → Execution Orchestration Subsystem (Section 2.5)**
- Components: EXEC-01 through EXEC-03
- Covers: Build orchestration, state management, build visibility

**ESC Domain → Escalation & Supervision Subsystem (Section 2.6)**
- Components: ESC-01 through ESC-04
- Covers: Ping generation, escalation management, silence detection, message inbox

**GOV Domain → Governance Enforcement Subsystem (Section 2.7)**
- Components: GOV-01 through GOV-03
- Covers: Governance loading, validation, supremacy enforcement

**ANALYTICS Domain → Analytics Subsystem (Section 2.8)**
- Components: ANALYTICS-01 through ANALYTICS-03
- Covers: Metrics dashboard, metrics engine, cost tracking

**CROSS Domain → Cross-Cutting Components (Section 2.9)**
- Components: CROSS-01 through CROSS-06
- Covers: Memory manager, authority manager, notification service, evidence store, audit logger, watchdog observer

**E2E Domain → End-to-End Integration**
- No specific components (integrates multiple subsystems)
- Covers: Full workflow tests across subsystem boundaries

### 3.2 QA Coverage Requirements by Domain

Each domain MUST have QA coverage for:

1. **Component Responsibilities**: Every component responsibility from architecture must be tested
2. **Key Behaviors**: Every key behavior defined in architecture must be tested
3. **Decision Points**: Every decision point must have test coverage
4. **State Transitions**: Every state transition must be tested
5. **Error Conditions**: Every error condition must be tested
6. **Integration Points**: Every integration point must be tested

### 3.3 Cross-Domain Dependencies

Some QA units require functionality from multiple domains:

- **INTENT-to-EXEC Flow**: Intent processing depends on execution orchestration
- **ESC-to-CONV Flow**: Escalations trigger FM-initiated conversations
- **GOV-to-ESC Flow**: Governance violations trigger escalations
- **DASH-to-EVIDENCE Flow**: Dashboard drill-down requires evidence store
- **ANALYTICS-to-ALL Flow**: Analytics aggregates data from all domains

Dependencies are documented in `QA_TRACEABILITY_MATRIX.md`.

---

## 4. QA Ordering and Sequencing Rules

### 4.1 Sequencing Principles

**Within-Domain Ordering:**
1. **Foundation First**: Data models and state machines before business logic
2. **Core Before Extensions**: Essential behaviors before optional features
3. **Happy Path Before Error Cases**: Primary flows before edge cases
4. **Unit Before Integration**: Component tests before cross-component tests

**Cross-Domain Ordering:**
1. **Dependencies First**: QA for prerequisite domains before dependent domains
2. **Foundation Layers**: CROSS domain (memory, authority) before application domains
3. **Core Flows**: CONV, INTENT, EXEC before support domains (ESC, ANALYTICS)
4. **End-to-End Last**: E2E domain after all component domains are complete

### 4.2 Recommended Build Wave Sequence

**Wave 1 (Foundation):**
- CROSS domain (QA-CROSS-001 to QA-CROSS-030)
- GOV domain (QA-GOV-001 to QA-GOV-015)

**Wave 2 (Core Interaction):**
- CONV domain (QA-CONV-001 to QA-CONV-025)
- INTENT domain (QA-INTENT-001 to QA-INTENT-020)

**Wave 3 (Execution & Supervision):**
- EXEC domain (QA-EXEC-001 to QA-EXEC-015)
- ESC domain (QA-ESC-001 to QA-ESC-020)

**Wave 4 (Visibility):**
- DASH domain (QA-DASH-001 to QA-DASH-020)
- ANALYTICS domain (QA-ANALYTICS-001 to QA-ANALYTICS-015)

**Wave 5 (Continuous Improvement):**
- PARK domain (QA-PARK-001 to QA-PARK-015)

**Wave 6 (Integration):**
- E2E domain (QA-E2E-001 to QA-E2E-010)

### 4.3 Dependency Hints

Dependencies between QA units are documented as follows:

**Notation:**
```
QA-DOMAIN-XXX depends on QA-DOMAIN-YYY
```

**Dependency Types:**

1. **Hard Dependency**: QA-B cannot execute until QA-A is GREEN
2. **Soft Dependency**: QA-B can execute but may have limited coverage without QA-A
3. **Ordering Preference**: QA-A should be completed before QA-B for logical flow

Dependencies are explicitly documented in `QA_TRACEABILITY_MATRIX.md`.

---

## 5. Progressive Gating Model

### 5.1 Gate Definition

A **gate** is a QA-based checkpoint that must be satisfied before proceeding to the next phase of work.

**Gate Components:**
1. **Required Green Set**: Specific QA IDs that MUST be GREEN to pass gate
2. **Allowed Red Set**: QA IDs that are allowed to be RED (not yet implemented)
3. **Gate Name**: Human-readable gate identifier (e.g., "Foundation Gate", "Core Interaction Gate")

### 5.2 Gate Declaration Format

Gates are declared using the following format:

```yaml
gate:
  name: "Foundation Gate"
  id: "GATE-001"
  required_green:
    - QA-CROSS-001
    - QA-CROSS-002
    - QA-CROSS-003
    - QA-GOV-001
    - QA-GOV-002
  allowed_red:
    - QA-CONV-*
    - QA-INTENT-*
    - QA-EXEC-*
    - QA-ESC-*
    - QA-DASH-*
    - QA-ANALYTICS-*
    - QA-PARK-*
    - QA-E2E-*
  enforcement: "BLOCKING"
  escalation_on_failure: true
```

### 5.3 Gate Enforcement Semantics

**BLOCKING Gates:**
- Build execution halts if gate is not satisfied
- No further work assigned until gate passes
- Automatic escalation on gate failure

**NON-BLOCKING Gates:**
- Build execution continues but gate failure is recorded
- Warning issued but work proceeds
- No automatic escalation

**Gate Evaluation:**
- Gates are evaluated before wave transitions
- Gates are evaluated before builder appointment
- Gates are evaluated before completion certification

### 5.4 Allowed Red Set Semantics

The "Allowed Red Set" defines QA units that are explicitly permitted to be RED at a given gate.

**Purpose:**
- Enables progressive build (not all features implemented at once)
- Prevents false gate failures for features not yet assigned
- Makes explicit what IS and IS NOT expected to work

**Wildcard Notation:**
- `QA-CONV-*` means "all QA units in CONV domain"
- `QA-CONV-010:020` means "QA-CONV-010 through QA-CONV-020 inclusive"

**Validation:**
- Any RED QA unit NOT in allowed_red set → Gate FAILURE
- All required_green QA units must be GREEN → Gate PASS
- Empty allowed_red means ALL QA must be GREEN

### 5.5 Default Gates (Wave-Based)

**GATE-FOUNDATION (Wave 1 Exit):**
- Required Green: All CROSS and GOV domain QA
- Allowed Red: All other domains
- Enforcement: BLOCKING

**GATE-CORE-INTERACTION (Wave 2 Exit):**
- Required Green: All CROSS, GOV, CONV, INTENT domain QA
- Allowed Red: EXEC, ESC, DASH, ANALYTICS, PARK, E2E
- Enforcement: BLOCKING

**GATE-EXECUTION (Wave 3 Exit):**
- Required Green: All CROSS, GOV, CONV, INTENT, EXEC, ESC domain QA
- Allowed Red: DASH, ANALYTICS, PARK, E2E
- Enforcement: BLOCKING

**GATE-VISIBILITY (Wave 4 Exit):**
- Required Green: All CROSS, GOV, CONV, INTENT, EXEC, ESC, DASH, ANALYTICS domain QA
- Allowed Red: PARK, E2E
- Enforcement: BLOCKING

**GATE-COMPLETE (Final):**
- Required Green: ALL QA units
- Allowed Red: NONE
- Enforcement: BLOCKING

---

## 6. QA Evidence Requirements

### 6.1 Evidence Purpose

QA evidence serves to:
1. **Prove Build Completion**: Objective verification that QA is GREEN
2. **Enable Non-Coder Verification**: Johan can verify build success without code review
3. **Support Audit and Traceability**: Permanent record of QA outcomes
4. **Enable Failure Diagnosis**: Evidence helps identify root cause when QA fails

### 6.2 Evidence Artifact Format

Every QA unit, when GREEN, MUST produce evidence in the following format:

```json
{
  "qa_id": "QA-CONV-001",
  "qa_name": "Persistent Conversation State Management",
  "execution_timestamp": "2025-12-31T10:00:00Z",
  "status": "GREEN",
  "execution_time_ms": 150,
  "test_framework": "pytest",
  "test_file": "tests/conversational/test_conversation_manager.py",
  "test_function": "test_conversation_persists_across_sessions",
  "assertions_passed": 5,
  "assertions_total": 5,
  "coverage_lines": 45,
  "coverage_percentage": 100.0,
  "evidence_artifacts": [
    {
      "type": "database_record",
      "location": "evidence/QA-CONV-001/conversation_record.json",
      "description": "Conversation persisted in database"
    },
    {
      "type": "state_snapshot",
      "location": "evidence/QA-CONV-001/state_snapshot.json",
      "description": "Conversation state after restart"
    }
  ],
  "requirements_covered": ["FR-CONV-1"],
  "components_covered": ["CONV-01", "CONV-02"],
  "dependencies_satisfied": []
}
```

### 6.3 Evidence Storage

**Evidence Location:**
```
foreman/evidence/qa/<DOMAIN>/<QA_ID>/
  ├── result.json         # QA execution result (format above)
  ├── artifacts/          # Supporting evidence artifacts
  │   ├── snapshot-1.json
  │   ├── database-dump.json
  │   └── ...
  └── logs/               # Execution logs (if needed)
      └── execution.log
```

**Evidence Retention:**
- Evidence is permanent and immutable
- Evidence is version-controlled
- Evidence is timestamped
- Evidence is auditable

### 6.4 Evidence Types

**Test Execution Evidence:**
- Test framework output (pass/fail status)
- Assertion counts (passed/total)
- Execution time
- Coverage metrics

**Behavioral Evidence:**
- Database state snapshots
- API response examples
- UI state captures (for UI tests)
- Event logs

**Integration Evidence:**
- Cross-component interaction traces
- External API calls (mocked)
- State transitions captured

**Compliance Evidence:**
- Governance rule validation results
- Authority checks
- Privacy guardrail verification

### 6.5 Evidence Validation

Evidence is considered valid when:
1. **Format Compliance**: Matches expected JSON schema
2. **Completeness**: All required fields present
3. **Consistency**: Status matches test output
4. **Traceability**: Requirements and components correctly mapped
5. **Timestamp**: Execution timestamp is recent and reasonable

Invalid evidence → QA status is UNKNOWN → Build BLOCKED

---

## 7. QA-to-Red vs Build-to-Green

### 7.1 Phase Distinction

**QA-to-Red Phase (Phase 4.4 - THIS PHASE):**
- **Activity**: Define QA units, assign IDs, map to requirements/architecture
- **Output**: QA-to-Red specification and traceability matrix
- **Status**: DESIGN ONLY, no implementation, no execution
- **Owner**: Foreman (FM)
- **Deliverable**: QA suite definition (this document)

**Build-to-Green Phase (Wave 1.0+ - FUTURE):**
- **Activity**: Implement production code to make QA units pass
- **Output**: Production code, passing tests, evidence artifacts
- **Status**: IMPLEMENTATION and EXECUTION
- **Owner**: Builder agents (under FM orchestration)
- **Deliverable**: Working system with 100% GREEN QA

### 7.2 QA-to-Red Acceptance Criteria

This phase (4.4) is complete when:
- ✅ QA-to-Red specification exists (this document)
- ✅ QA traceability matrix exists with all QA units defined
- ✅ Every QA unit has unique immutable ID
- ✅ Every QA unit traces to requirements and architecture
- ✅ Progressive gating model is defined
- ✅ Evidence format is defined
- ✅ NO QA tests have been implemented
- ✅ NO QA tests have been executed
- ✅ NO production code has been written
- ✅ FM explicitly confirms acceptance

### 7.3 Build-to-Green Preconditions

Build-to-Green (Wave 1.0+) CANNOT start until:
- ✅ QA-to-Red specification is accepted by CS2 (Johan)
- ✅ Builder recruitment is complete (already done in Wave 0.1)
- ✅ Platform readiness is GREEN (already confirmed)
- ✅ Architecture is frozen (already done in Phase 4.3)
- ✅ Governance is loaded and validated

---

## 8. QA Suite Structure Summary

### 8.1 Total QA Unit Estimates

Based on architecture complexity and requirements coverage:

| Domain | Estimated QA Units | Rationale |
|--------|-------------------|-----------|
| CONV | 25 | 5 components × 5 test types avg |
| DASH | 20 | 4 components × 5 test types avg |
| PARK | 15 | 4 components × 4 test types avg |
| INTENT | 20 | 4 components × 5 test types avg |
| EXEC | 15 | 3 components × 5 test types avg |
| ESC | 20 | 4 components × 5 test types avg |
| GOV | 15 | 3 components × 5 test types avg |
| ANALYTICS | 15 | 3 components × 5 test types avg |
| CROSS | 30 | 6 components × 5 test types avg |
| E2E | 10 | 10 critical end-to-end workflows |
| **TOTAL** | **185** | **Full system coverage** |

### 8.2 QA Unit Type Distribution

**Unit Tests (60%)**: ~110 QA units
- Component responsibility tests
- State transition tests
- Business rule tests
- Data model tests

**Integration Tests (30%)**: ~55 QA units
- Cross-component interaction tests
- Pipeline tests
- Flow tests
- Integration point tests

**End-to-End Tests (10%)**: ~20 QA units
- Full workflow tests
- User journey tests
- System integration tests

### 8.3 Quality Targets

**Coverage Target**: 100% of architecture components
**Pass Rate Target**: 100% GREEN before completion
**Test Debt Target**: ZERO (no skipped tests, no stubs)
**Execution Time Target**: < 10 minutes for full suite
**Evidence Completeness**: 100% of QA units produce valid evidence

---

## 9. Governance Compliance

### 9.1 BUILD_PHILOSOPHY.md Alignment

This QA-to-Red specification aligns with BUILD_PHILOSOPHY.md:

**One-Time Build Correctness:**
- QA-to-Red defines acceptance criteria before implementation
- Deterministic QA prevents iterative debugging
- Complete specification enables correct-first-time builds

**Zero Regression Guarantee:**
- QA must be 100% GREEN before completion
- No partial passes accepted
- Any test failure blocks build

**Full Architectural Alignment:**
- Every QA unit traces to architecture components
- QA coverage maps to architecture coverage
- No untested architecture components

**Zero Loss of Context:**
- QA IDs are immutable (never lost)
- Evidence is permanent
- Traceability is bidirectional

**Zero Ambiguity Principle:**
- QA IDs are machine-parseable
- Evidence format is explicit
- Gate semantics are deterministic

### 9.2 Memory Fabric Integration

QA outcomes are recorded in Memory Fabric:
- QA execution results → Memory
- Gate pass/fail events → Memory
- Evidence artifacts → Memory (by reference)
- Failure patterns → Memory (for learning)

### 9.3 Compliance with Agent Contract

This specification respects the Agent Contract:
- FM defines QA (not builders)
- Builders implement to make QA pass (not define QA)
- CS2 (Johan) approves via non-coder interface (not code review)
- Evidence-based verification (not subjective review)

---

## 10. QA-to-Red Specification Acceptance

### 10.1 Completeness Checklist

- [x] QA suite purpose and enforcement role defined (Section 1)
- [x] QA ID scheme defined with immutability rules (Section 2)
- [x] QA domains mapped to architecture subsystems (Section 3)
- [x] QA ordering and sequencing rules defined (Section 4)
- [x] Progressive gating model defined with enforcement semantics (Section 5)
- [x] QA evidence requirements defined with format and storage (Section 6)
- [x] QA-to-Red vs Build-to-Green distinction clarified (Section 7)
- [x] QA suite structure estimated (Section 8)
- [x] Governance compliance verified (Section 9)

### 10.2 Traceability Verification

- [x] All requirements from FRS covered by QA domains
- [x] All architecture components covered by QA domains
- [x] All subsystems have corresponding QA domains
- [x] Cross-cutting concerns have QA coverage (CROSS domain)
- [x] End-to-end workflows have QA coverage (E2E domain)

### 10.3 Acceptance Criteria Status

Per Phase 4.4 issue acceptance criteria:

- [x] ✅ QA ID scheme exists and is immutable-by-design (Section 2)
- [x] ✅ QA inventory structure defined (Section 8, detailed in QA_TRACEABILITY_MATRIX.md)
- [x] ✅ QA traceability approach defined (Section 3, 9.2)
- [x] ✅ Progressive gating semantics defined (Section 5)
- [x] ✅ Evidence requirements defined (Section 6)
- [x] ✅ No QA tests implemented (DESIGN ONLY)
- [x] ✅ No QA tests executed (DESIGN ONLY)
- [x] ⏸ No builders recruited (builders already recruited in Wave 0.1 - recruitment complete)
- [x] ⏸ FM explicitly confirms acceptance (Section 11)

### 10.4 Known Limitations

**Estimates Only:**
- QA unit counts are estimates based on architecture complexity
- Actual counts will be determined during QA inventory creation (QA_TRACEABILITY_MATRIX.md)

**Technology-Agnostic:**
- This specification does NOT define test frameworks, languages, or tools
- Technology choices deferred to implementation planning

**No Execution:**
- This is a design specification only
- No tests have been implemented or executed
- Execution is deferred to Build-to-Green phase (Wave 1.0+)

---

## 11. FM Acceptance Declaration

I, Foreman (FM), explicitly confirm acceptance of this QA-to-Red Specification:

**`QA_TO_RED_SPEC.md` (Version 1.0)**

This QA-to-Red Specification:
- Is complete, coherent, and unambiguous
- Derives exclusively from FRS and Architecture Spec
- Defines immutable QA ID scheme with deterministic parsing
- Maps QA domains to all architecture subsystems
- Defines sequencing rules and dependency management
- Defines progressive gating model with enforcement semantics
- Defines evidence format and storage requirements
- Distinguishes QA-to-Red (design) from Build-to-Green (implementation)
- Estimates 185 total QA units across 10 domains
- Aligns with BUILD_PHILOSOPHY.md and Agent Contract
- Enables non-coder orchestration and verification
- Is ready to serve as binding contract for builder task assignment

**Total Estimated QA Units:** 185  
**Total Domains:** 10  
**Total Gates:** 6  
**Requirements Covered:** 28 functional + 8 cross-cutting = 36 total  
**Architecture Components Covered:** 36

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Signature:** This document constitutes formal FM acceptance

---

## 12. Next Phase Gate

**Phase 4.5 (Builder Recruitment & Delegation):** BLOCKED until Phase 4.4 accepted by CS2

**Pending Deliverable:** `QA_TRACEABILITY_MATRIX.md` (detailed QA inventory with all 185 QA units)

---

## 13. Ratchet Statement Compliance

> We do not build what we cannot verify.  
> We do not verify what we cannot index and trace.

**Status:** ✅ COMPLIANT

- QA units are indexable (unique IDs)
- QA units are traceable (to requirements and architecture)
- QA units are verifiable (evidence-based)
- Ready for CS2 acceptance
- No implementation ahead of QA definition
- Build-to-Green (Wave 1.0) remains BLOCKED

---

**End of QA-to-Red Specification**
