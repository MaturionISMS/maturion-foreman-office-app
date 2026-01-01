# Builder Contract: schema-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** schema-builder  
**Builder Type:** Specialized Builder (Data & Persistence)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED

**Capabilities:**
- schema (database schema design)
- models (entity models and relationships)
- migrations (schema versioning and evolution)

**Responsibilities:**
- Database schemas
- Models

**Forbidden Actions:**
- ❌ UI implementation
- ❌ Integration routing

---

## QA Range Assignment (Bounded Scope)

**Assigned QA Range:** **QA-001 to QA-018**

**Total QA Components:** 18

**QA Listing:**
- QA-001: Create conversation (database write, audit log, initial state)
- QA-002: Retrieve conversation (data persistence, message loading, state consistency)
- QA-003: Archive conversation (state transition, reason capture, timestamp)
- QA-004: Resume conversation (state transition, audit trail, UI update)
- QA-005: Conversation Manager failure modes (retry/escalation, conflict handling)
- QA-006: Send message (validation, persistence, delivery event)
- QA-007: Deliver message (routing, UI update, timestamp)
- QA-008: Mark message read (state update, audit log)
- QA-009: Message validation (rejection, invalid ID handling)
- QA-010: Message Handler failure modes (retry/escalation, intent processing failure)
- QA-011: FM initiates conversation (creation, notification, context attachment)
- QA-012: Attach context to FM conversation (escalation/build context, evidence linking)
- QA-013: FM urgent conversation (priority flag, immediate notification, inbox placement)
- QA-014: Detect ambiguity (pattern detection, confidence scoring, trigger)
- QA-015: Generate clarifying questions (quality, context, option presentation)
- QA-016: Resolve clarification (sufficiency check, intent transition, criteria)
- QA-017: Clarification loop limits (iteration count, escalation after N, structured capture)
- QA-018: Clarification Engine failure modes (safe default, timeout handling)

**Authoritative Reference:** `QA_CATALOG.md` (QA-001 to QA-018)

---

## Architectural Coverage

**Subsystems:**
- Conversational Interface Subsystem (data layer)

**Components:**
- CONV-01: Conversation Manager
- CONV-02: Message Handler
- CONV-03: FM Conversation Initiator
- CONV-04: Clarification Engine

**Data Entities (schema-builder owns):**
- **Conversation** — conversationId, userId, state, createdAt, archivedAt, resumedAt, lastMessageAt, messageCount
- **Message** — messageId, conversationId, senderId, content, type, state, createdAt, deliveredAt, readAt
- **ConversationContext** — conversationId, contextType, contextData, createdAt
- **Clarification** — clarificationId, messageId, questions, responses, state, resolvedAt

**Architectural Traceability:**
- Architecture: `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Section 3
- Traceability: `QA_TRACEABILITY_MATRIX.md`

---

## Gate Definition

**Gate ID:** `GATE-SCHEMA-BUILDER-WAVE-1.0`

**Gate Type:** Builder Gate

**Gate Configuration:**
```yaml
gate:
  id: "GATE-SCHEMA-BUILDER-WAVE-1.0"
  type: "builder"
  builder: "schema-builder"
  required_green:
    - QA-001 to QA-018
  allowed_red:
    - ALL EXCEPT QA-001 to QA-018
  enforcement: "BLOCKING"
  description: "schema-builder must make all assigned QA GREEN"
```

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

**Success Criteria:**
- ✅ All 18 QA components GREEN
- ✅ Database schemas created and functional
- ✅ Migration scripts operational
- ✅ CRUD operations validated
- ✅ Evidence artifacts generated for all 18 QA

**Builder scope = ONLY QA-001 to QA-018**

Other QA (QA-019 to QA-400+) remaining RED does NOT block schema-builder.

---

## Evidence Obligations

### Per-QA Evidence Requirements

For each QA component (QA-001 to QA-018), schema-builder MUST generate:

**Evidence Artifact Format (JSON):**
```json
{
  "qa_id": "QA-XXX",
  "qa_name": "<QA name from catalog>",
  "status": "GREEN",
  "execution_timestamp": "ISO-8601 timestamp",
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

**Evidence Location Structure:**
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

### Aggregate Evidence Requirements

**schema-builder MUST provide:**
1. Schema documentation (ERD, versioning, migration strategy)
2. Test coverage report (100% for QA-001 to QA-018)
3. Builder completion report (all 18 QA summary, evidence inventory)

**Evidence Standards:**
- ✅ Complete and well-formed
- ✅ Immutable (timestamped, version-controlled)
- ✅ Traceable (QA ID → test → schema → architecture)
- ✅ Auditable (reproducible tests)

---

## Escalation Rules

### When to Escalate

schema-builder MUST escalate immediately when:
- Blocked by missing dependency (e.g., database credentials unavailable)
- Cannot make assigned QA GREEN due to architectural issue
- Discovered ambiguity or gap in requirements/architecture
- Persistent technical failure (3+ retry attempts)

### Escalation Format (5 Elements Required)

```
Builder: schema-builder
What: [Specific blocker/issue]
Why: [Root cause]
Blocked: [Which QA cannot proceed]
Decision Required: [What FM should decide]
Consequence: [Impact if no decision]
```

### Escalation Destination

**All escalations route to:** ESC-02 Escalation Manager → FM

**Example Escalation:**
```
Builder: schema-builder
What: Cannot set up test database
Why: Database credentials not available
Blocked: QA-001 (Create conversation test)
Decision Required: Should schema-builder use local SQLite, or wait for production DB?
Consequence: If no decision, 18 QA components cannot start (critical blocker)
```

### Escalation Response Time

- CRITICAL escalations (all 18 QA blocked): Immediate (within 1 hour)
- HIGH escalations (5+ QA blocked): Within 4 hours
- NORMAL escalations (1-4 QA blocked): Within 24 hours

---

## Dependencies

### Dependencies on Other Builders

**schema-builder depends on:**
- ⚠️ **qa-builder** for test infrastructure (test framework, test harness)
  - Resolution: qa-builder provides infrastructure early, or schema-builder sets up own environment

### Other Builders Depend on schema-builder

**Downstream dependencies:**
- ⚠️ **ui-builder** needs data models to render UI
- ⚠️ **api-builder** needs data models for API endpoints
- ⚠️ **integration-builder** needs data contracts for event routing

**Impact:** schema-builder is **foundational** — other builders cannot proceed without schema-builder's work.

**Priority:** schema-builder should be **prioritized** and start immediately.

---

## Collaboration Protocol

### Cross-Builder Communication

**schema-builder may coordinate with:**
- qa-builder (test infrastructure)
- api-builder (data model contracts, CRUD signatures)
- ui-builder (data structure for UI rendering)

**Communication Rules:**
- All cross-builder communication MUST go through FM
- No direct builder-to-builder commands
- Use escalation mechanism for blockers
- Document all interfaces/contracts in shared specifications

### Interface Contracts to Provide

schema-builder MUST provide early interface contracts:

**Conversation Entity Contract:**
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

**Message Entity Contract:**
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

(Similar for ConversationContext and Clarification)

---

## Quality Standards

### Code Quality

- ✅ Schema follows normalization principles
- ✅ Indices defined for performance
- ✅ Foreign key constraints enforced
- ✅ Data types appropriate and validated
- ✅ Migration scripts reversible
- ✅ No data loss during migrations

### Test Quality

- ✅ All 18 QA tests deterministic (same input = same output)
- ✅ Tests independent (can run in any order)
- ✅ Tests clean up after themselves (no side effects)
- ✅ Tests cover happy path + failure modes
- ✅ 100% coverage of assigned QA range (QA-001 to QA-018)

### Evidence Quality

- ✅ Evidence artifacts complete and well-formed
- ✅ Evidence immutable (timestamped, version-controlled)
- ✅ Evidence traceable (QA ID → test → schema → architecture)
- ✅ Evidence auditable (reproducible tests)

---

## Contract Terms

### Builder Obligations

schema-builder MUST:
1. Make all 18 assigned QA components GREEN
2. Generate complete evidence for each QA
3. Provide interface contracts to downstream builders
4. Escalate blockers immediately using 5-element format
5. Adhere to quality standards (code, test, evidence)
6. Work only within assigned QA range (QA-001 to QA-018)
7. Respect forbidden actions (no UI, no integration routing)

### Builder Rights

schema-builder MAY:
1. Request clarification from FM on ambiguous requirements
2. Propose alternative technical approaches (with FM approval)
3. Coordinate with other builders (via FM)
4. Request additional time if blocked by dependency
5. Access all authoritative input documents (QA Catalog, Architecture, etc.)

### Builder Restrictions

schema-builder MUST NOT:
1. Work on QA outside assigned range (QA-019 to QA-400+)
2. Implement UI components (ui-builder's responsibility)
3. Implement API endpoints (api-builder's responsibility)
4. Modify governance or architecture documents
5. Bypass QA validation (all 18 QA must be GREEN)
6. Communicate directly with CS2 (all communication via FM)

---

## Contract Acceptance

### FM Certification

I, Foreman (FM), certify that this builder contract:
- Binds schema-builder to QA-001 to QA-018 (18 QA components)
- Defines deterministic gate (GATE-SCHEMA-BUILDER-WAVE-1.0)
- Specifies complete evidence obligations
- Establishes clear escalation rules
- Identifies dependencies and collaboration protocols
- Sets quality standards and acceptance criteria
- Is ready for Wave 1.0 execution (Phase 5.0)

**Certified By:** Foreman (FM)  
**Date:** 2025-12-31  
**Phase:** 4.5 → 5.0 Transition  
**Contract Status:** ACTIVE

### Builder Acknowledgment

By accepting this contract, schema-builder acknowledges:
- Understanding of assigned QA range (QA-001 to QA-018)
- Commitment to make all 18 QA GREEN
- Obligation to generate complete evidence
- Responsibility to escalate blockers immediately
- Agreement to work within bounded scope
- Acceptance of quality standards

**Contract Effective Date:** Upon Phase 5.0 authorization by CS2

---

## References

### Authoritative Documents
- `QA_CATALOG.md` — QA component definitions (QA-001 to QA-018)
- `QA_TO_RED_SUITE_SPEC.md` — RED/GREEN semantics
- `QA_TRACEABILITY_MATRIX.md` — Architecture ↔ QA mapping
- `BUILDER_GREEN_SCOPE_RULES.md` — Bounded assignment rules
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` — Architecture specification
- `PHASE_4.5_BUILDER_ASSIGNMENT_PLAN.md` — Assignment strategy
- `PHASE_4.5_BUILDER_TASK_SCHEMA_BUILDER.md` — Detailed task specification

### Builder Governance
- `foreman/builder/schema-builder-spec.md` — Builder specification
- `foreman/builder-manifest.json` — Builder registry
- `foreman/builder/builder-capability-map.json` — Capability definitions
- `foreman/builder/builder-permission-policy.json` — Permission boundaries

---

**END OF BUILDER CONTRACT: schema-builder**
