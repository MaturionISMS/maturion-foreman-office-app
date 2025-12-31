# Phase 4.5 — Builder Task Specification: schema-builder

**Builder:** schema-builder  
**Version:** 1.0  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Phase:** 4.5 — Builder Task Assignment (QA-Bounded, Design-Only)  
**Status:** TASK_DEFINED  
**Authority:** Derived from Phase 4.5 Builder Assignment Plan

---

## Builder Identity

**Builder Name:** schema-builder  
**Recruitment Date:** 2025-12-30  
**Recruitment Status:** ✅ RECRUITED (Wave 0.1)  
**Specification:** `foreman/builder/schema-builder-spec.md`

**Builder Capabilities:**
- ✅ schema (database schema design)
- ✅ models (entity models and relationships)
- ✅ migrations (schema versioning and evolution)

**Builder Responsibilities:**
- Database schemas
- Models

**Builder Forbidden Actions:**
- ❌ UI
- ❌ Integration routing

---

## Wave 1.0 Assignment

### QA Range (Bounded Scope)

**Assigned QA Range:** **QA-001 to QA-018**

**Total QA Components:** 18

**QA Listing:**
- QA-001: Create conversation (verify database write, verify audit log, verify initial state)
- QA-002: Retrieve conversation (verify data persistence, verify message loading, verify state consistency)
- QA-003: Archive conversation (verify state transition, verify reason captured, verify archive timestamp)
- QA-004: Resume conversation (verify state transition, verify audit trail, verify UI update)
- QA-005: Conversation Manager failure modes (database write failure retry/escalation, state conflict handling)
- QA-006: Send message (verify validation, verify persistence, verify delivery event)
- QA-007: Deliver message (verify routing, verify UI update, verify timestamp)
- QA-008: Mark message read (verify state update, verify audit log)
- QA-009: Message validation (empty content rejection, invalid conversation ID handling)
- QA-010: Message Handler failure modes (persistence failure retry/escalation, intent processing failure handling)
- QA-011: FM initiates conversation (verify conversation creation, verify Johan notification, verify context attachment)
- QA-012: Attach context to FM-initiated conversation (verify escalation context, verify build context, verify evidence linking)
- QA-013: FM urgent conversation (verify priority flag, verify immediate notification, verify inbox placement)
- QA-014: Detect ambiguity (verify pattern detection, verify confidence scoring, verify clarification trigger)
- QA-015: Generate clarifying questions (verify question quality, verify context inclusion, verify option presentation)
- QA-016: Resolve clarification (verify sufficient information check, verify intent transition, verify resolution criteria)
- QA-017: Clarification loop limits (verify iteration count, verify escalation after N loops, verify structured capture)
- QA-018: Clarification Engine failure modes (ambiguity detection failure safe default, question generation timeout)

### Architectural Coverage

**Subsystems:**
- Conversational Interface Subsystem (data layer)

**Components:**
- CONV-01: Conversation Manager
- CONV-02: Message Handler
- CONV-03: FM Conversation Initiator
- CONV-04: Clarification Engine

**Data Entities (schema-builder responsibility):**
- **Conversation** — conversationId, userId, state, createdAt, archivedAt, resumedAt, lastMessageAt, messageCount
- **Message** — messageId, conversationId, senderId, content, type, state, createdAt, deliveredAt, readAt
- **ConversationContext** — conversationId, contextType, contextData, createdAt
- **Clarification** — clarificationId, messageId, questions, responses, state, resolvedAt

**Architectural Traceability:**
- See `QA_TRACEABILITY_MATRIX.md` for complete mapping
- See `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Section 3 for component contracts

---

## Builder Success Criteria

### Deterministic Gate

**Gate ID:** `GATE-SCHEMA-BUILDER-WAVE-1.0`

**Gate Type:** Builder Gate

**Required GREEN:** QA-001 to QA-018 (18 QA components)

**Allowed RED:** All QA except QA-001 to QA-018

**Enforcement:** BLOCKING (schema-builder cannot complete until all assigned QA are GREEN)

**Gate Evaluation Logic:**
```
IF QA-001 through QA-018 are all GREEN:
    THEN Gate = PASS
    AND schema-builder task COMPLETE
ELSE:
    Gate = FAIL
    AND List which QA are RED (blockers)
    AND schema-builder task INCOMPLETE
```

### Success Definition

**schema-builder succeeds when:**
- ✅ All 18 assigned QA components are GREEN
- ✅ Database schemas created for Conversation, Message, ConversationContext, Clarification
- ✅ Data persistence layer functional
- ✅ CRUD operations validated
- ✅ Data integrity tests pass
- ✅ Migration scripts functional
- ✅ Evidence artifacts generated for all 18 QA

**schema-builder scope = ONLY QA-001 to QA-018**

**Other QA (QA-019 to QA-400+) remaining RED does NOT block schema-builder.**

---

## Evidence Requirements

### Per-QA Evidence

For each QA component (QA-001 to QA-018), schema-builder must generate:

**Evidence Artifact Format (JSON):**
```json
{
  "qa_id": "QA-XXX",
  "qa_name": "<QA name from catalog>",
  "status": "GREEN",
  "execution_timestamp": "2025-12-31T12:00:00Z",
  "execution_time_ms": 250,
  "test_framework": "pytest",
  "test_file": "tests/schema/test_<entity>.py",
  "test_function": "test_<specific_qa>",
  "assertions_passed": 5,
  "assertions_total": 5,
  "coverage_percentage": 100.0,
  "evidence_artifacts": [
    {
      "type": "database_schema",
      "location": "foreman/evidence/qa/CONV/QA-XXX/schema.sql",
      "description": "Database schema definition"
    },
    {
      "type": "migration_script",
      "location": "foreman/evidence/qa/CONV/QA-XXX/migration.sql",
      "description": "Migration script"
    },
    {
      "type": "test_execution_log",
      "location": "foreman/evidence/qa/CONV/QA-XXX/execution.log",
      "description": "Test execution output"
    }
  ],
  "requirements_covered": ["FR-CONV-1"],
  "components_covered": ["CONV-01"]
}
```

**Evidence Location:**
```
foreman/evidence/qa/CONV/<QA_ID>/
  ├─ result.json         # QA execution result
  ├─ artifacts/          # Supporting evidence
  │   ├─ schema.sql      # Database schema
  │   ├─ migration.sql   # Migration script
  │   └─ ...
  └─ logs/               # Execution logs
      └─ execution.log
```

### Aggregate Evidence

**schema-builder must also provide:**

1. **Schema Documentation**
   - Complete entity-relationship diagram
   - Schema versioning documentation
   - Migration strategy documentation

2. **Test Coverage Report**
   - 100% coverage of QA-001 to QA-018
   - Schema validation tests
   - CRUD operation tests
   - Data integrity tests

3. **Builder Completion Report**
   - Summary of all 18 QA components
   - GREEN status confirmation
   - Evidence artifacts inventory
   - Handover readiness declaration

---

## Build-to-Green Instructions

### What schema-builder Must Do

**Step 1: Understand Scope**
- Read this task specification completely
- Review QA_CATALOG.md for QA-001 to QA-018 details
- Review FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section 3 for component contracts
- Review QA_TRACEABILITY_MATRIX.md for architecture mapping

**Step 2: Design Database Schema**
- Design schema for Conversation, Message, ConversationContext, Clarification entities
- Follow architectural contracts exactly (see FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
- Include all required fields per architecture
- Define relationships (foreign keys, indices)
- Plan migration strategy

**Step 3: Implement Schema**
- Create schema definition files (SQL or ORM models)
- Create migration scripts (versioned)
- Implement CRUD operations
- Follow technology stack: (database choice per project standards)

**Step 4: Implement Tests (Make QA GREEN)**
- For each QA (QA-001 to QA-018):
  - Write test code that validates the QA requirement
  - Run test → expect FAIL initially (QA-to-Red baseline)
  - Implement schema/code to make test PASS
  - Verify test is now GREEN
  - Generate evidence artifacts

**Step 5: Validate All QA GREEN**
- Run all 18 QA tests
- Confirm all are GREEN
- No RED allowed in schema-builder's range
- Generate aggregate evidence

**Step 6: Handover**
- Submit evidence to FM
- Declare task COMPLETE
- Gate evaluation: GATE-SCHEMA-BUILDER-WAVE-1.0

### What schema-builder Must NOT Do

**Strictly Forbidden:**
- ❌ Implement UI components (ui-builder's responsibility)
- ❌ Implement API endpoints (api-builder's responsibility)
- ❌ Implement integration routing (integration-builder's responsibility)
- ❌ Work on QA outside of QA-001 to QA-018 range
- ❌ Modify governance or architecture documents
- ❌ Bypass QA validation (all 18 QA must be GREEN)

---

## Dependencies

### Dependencies on Other Builders

**schema-builder has minimal dependencies:**
- ⚠️ Depends on **qa-builder** for test infrastructure (test framework, test harness)
  - Resolution: qa-builder provides test infrastructure early, or schema-builder sets up own test environment

**Other builders depend on schema-builder:**
- ⚠️ **ui-builder** needs data models to render UI
- ⚠️ **api-builder** needs data models for API endpoints
- ⚠️ **integration-builder** needs data contracts for event routing

**Impact:** schema-builder is a **foundational builder** — other builders cannot proceed without schema-builder's work.

**Recommendation:** schema-builder should be **prioritized** and start immediately.

### Dependency Resolution

**If schema-builder is blocked:**
- Escalate immediately via ESC-02 Escalation Manager
- 5-element escalation format:
  - What: Specific blocker
  - Why: Root cause
  - Blocked: Which QA cannot proceed
  - Decision Required: What FM should decide
  - Consequence: Impact if no decision

**Example Escalation:**
```
Builder: schema-builder
What: Cannot set up test database
Why: Database credentials not available
Blocked: QA-001 (Create conversation test)
Decision Required: Should schema-builder use local SQLite, or wait for production DB?
Consequence: If no decision, 18 QA components cannot start (critical blocker)
```

---

## Collaboration Rules

### Cross-Builder Communication

**schema-builder may need to coordinate with:**

1. **qa-builder**
   - For test infrastructure and test execution
   - For evidence artifact generation standards

2. **api-builder**
   - To provide data model contracts early (before full implementation)
   - To align on CRUD operation signatures

3. **ui-builder**
   - To provide data model contracts early
   - To align on data structure for UI rendering

**Communication Protocol:**
- All cross-builder communication must go through FM
- No direct builder-to-builder commands
- Use escalation mechanism for blockers
- Document all interfaces/contracts in shared specifications

### Interface Contracts

**schema-builder must provide interface contracts to downstream builders:**

**Contract: Conversation Entity**
```typescript
interface Conversation {
  conversationId: string;
  userId: string;
  state: 'ACTIVE' | 'PAUSED' | 'ARCHIVED';
  createdAt: Date;
  archivedAt: Date | null;
  resumedAt: Date | null;
  lastMessageAt: Date | null;
  messageCount: number;
}
```

**Contract: Message Entity**
```typescript
interface Message {
  messageId: string;
  conversationId: string;
  senderId: string;
  content: string;
  type: 'user' | 'fm';
  state: 'PENDING' | 'SENT' | 'DELIVERED' | 'READ';
  createdAt: Date;
  deliveredAt: Date | null;
  readAt: Date | null;
}
```

(Similar contracts for ConversationContext and Clarification)

**schema-builder delivers these contracts early** so other builders can proceed in parallel.

---

## Timeline & Milestones

### Recommended Milestones

**Milestone 1: Schema Design Complete (Day 1-2)**
- Database schema designed
- Entity relationships defined
- Migration strategy defined
- Interface contracts published

**Milestone 2: Schema Implementation Complete (Day 3-5)**
- Schema definition files created
- Migration scripts created
- CRUD operations implemented
- Ready for testing

**Milestone 3: QA Implementation (Day 6-10)**
- Tests written for QA-001 to QA-018
- Tests initially RED (QA-to-Red baseline confirmed)
- Schema/code refined to make tests GREEN
- All 18 QA components GREEN

**Milestone 4: Evidence Generation & Handover (Day 11-12)**
- Evidence artifacts generated for all 18 QA
- Aggregate evidence compiled
- Builder completion report generated
- Gate evaluation: PASS

**Estimated Duration:** 10-12 days (depends on schema complexity and test coverage)

---

## Quality Standards

### Code Quality

**schema-builder must ensure:**
- ✅ Schema follows normalization principles
- ✅ Indices defined for performance
- ✅ Foreign key constraints enforced
- ✅ Data types appropriate and validated
- ✅ Migration scripts are reversible
- ✅ No data loss during migrations

### Test Quality

**schema-builder must ensure:**
- ✅ All 18 QA tests are deterministic (same input = same output)
- ✅ Tests are independent (can run in any order)
- ✅ Tests clean up after themselves (no side effects)
- ✅ Tests cover happy path + failure modes
- ✅ 100% coverage of assigned QA range

### Evidence Quality

**schema-builder must ensure:**
- ✅ Evidence artifacts are complete and well-formed
- ✅ Evidence is immutable (timestamped, version-controlled)
- ✅ Evidence is traceable (QA ID → test → schema → architecture)
- ✅ Evidence is auditable (reproducible tests)

---

## Acceptance Criteria (schema-builder Task)

This task is complete when:

- ✅ All 18 QA components (QA-001 to QA-018) are GREEN
- ✅ Database schemas created and validated
- ✅ Migration scripts functional
- ✅ CRUD operations tested and functional
- ✅ Evidence artifacts generated for all 18 QA
- ✅ Interface contracts published for downstream builders
- ✅ Builder completion report submitted
- ✅ Gate GATE-SCHEMA-BUILDER-WAVE-1.0 evaluates to PASS
- ✅ No regressions (all GREEN QA remain GREEN)
- ✅ FM accepts schema-builder's work

**Status after acceptance:** schema-builder task COMPLETE, ready for Wave 1.0 gate evaluation

---

## FM Acceptance (Task Specification)

I, Foreman (FM), confirm that this Builder Task Specification for **schema-builder**:

- Defines explicit QA-bounded scope (QA-001 to QA-018, 18 components)
- Maps QA to architectural components (CONV-01 to CONV-04 data layer)
- Specifies deterministic gate (GATE-SCHEMA-BUILDER-WAVE-1.0)
- Defines evidence requirements (per-QA and aggregate)
- Provides build-to-green instructions
- Identifies dependencies and collaboration needs
- Sets quality standards and acceptance criteria
- Is design-only (no implementation yet)

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Phase:** 4.5 — Builder Task Assignment  
**Status:** TASK_DEFINED — READY FOR WAVE 1.0 EXECUTION (Phase 5.0)

---

**End of schema-builder Task Specification**
