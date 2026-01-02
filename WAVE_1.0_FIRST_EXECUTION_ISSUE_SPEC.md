# Wave 1.0 — First Execution Issue Specification

**Date:** 2026-01-02  
**Authority:** FM Agent Contract v3.0.0, FM Execution Mandate (T0-013)  
**Status:** READY FOR CS2 EXECUTION  
**Context:** Bootstrap Mode — CS2 performs GitHub actions, FM provides instructions

---

## Executive Summary

FM has reviewed the Wave 1.0 execution plan and determined the optimal first execution issue.

**Decision:** Start with **schema-builder** (QA-001 to QA-018)

**Rationale:**
- Provides data foundation required by other builders
- Smallest QA scope (18 components) — lowest risk for first execution
- Clear, bounded responsibility (database schemas and models)
- No blocking dependencies (can start immediately)
- Validates full execution loop before scaling

**Next Issues (After First Issue Validation):**
- qa-builder can start in parallel (test infrastructure)
- ui-builder, api-builder, integration-builder follow after schema foundation

---

## First Execution Issue — schema-builder

### Issue Title

```
Wave 1.0.1 — Schema Foundation (schema-builder: QA-001 to QA-018)
```

### Issue Body

```markdown
# Wave 1.0.1 — Schema Foundation

**Wave:** 1.0  
**Phase:** Foundation  
**Builder:** schema-builder  
**QA Range:** QA-001 to QA-018 (18 QA components)  
**Gate:** GATE-SCHEMA-BUILDER-WAVE-1.0  
**Status:** ASSIGNED — Ready for Build-to-Green

---

## Objective

Implement the **database schema and data persistence layer** for the Conversational Interface subsystem to establish the data foundation for Foreman Office.

**Build Mode:** Build-to-Green (make all assigned QA GREEN exactly once)

---

## Scope

### QA Components (QA-001 to QA-018)

**CONV-01: Conversation Manager Data (QA-001 to QA-005)**
- QA-001: Create conversation (database write, audit log, initial state)
- QA-002: Retrieve conversation (data persistence, message loading, state consistency)
- QA-003: Archive conversation (state transition, reason captured, archive timestamp)
- QA-004: Resume conversation (state transition, audit trail)
- QA-005: Conversation Manager failure modes (database write failure, state conflict handling)

**CONV-02: Message Handler Data (QA-006 to QA-010)**
- QA-006: Send message (validation, persistence, delivery event)
- QA-007: Deliver message (routing, timestamp)
- QA-008: Mark message read (state update, audit log)
- QA-009: Message validation (empty content rejection, invalid conversation ID handling)
- QA-010: Message Handler failure modes (persistence failure retry/escalation)

**CONV-03: FM Conversation Initiator Data (QA-011 to QA-013)**
- QA-011: FM initiates conversation (conversation creation, context attachment)
- QA-012: Attach context to FM-initiated conversation (escalation context, build context, evidence linking)
- QA-013: FM urgent conversation (priority flag, notification)

**CONV-04: Clarification Engine Data (QA-014 to QA-018)**
- QA-014: Detect ambiguity (pattern detection, confidence scoring)
- QA-015: Generate clarifying questions (question quality, context inclusion)
- QA-016: Resolve clarification (sufficient information check, intent transition)
- QA-017: Clarification loop limits (iteration count, escalation after N loops)
- QA-018: Clarification Engine failure modes (ambiguity detection failure, question generation timeout)

### Architectural Reference

**Primary:** `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md`  
**Sections:**
- Conversational Interface Subsystem
- CONV-01: Conversation Manager (data layer)
- CONV-02: Message Handler (data layer)
- CONV-03: FM Conversation Initiator (data layer)
- CONV-04: Clarification Engine (data layer)

**QA-to-Architecture Mapping:** See `QA_TRACEABILITY_MATRIX.md`

---

## Deliverables

### 1. Database Schema

**Entities Required:**
- `Conversation` (id, organisation_id, state, created_at, archived_at, archived_reason, ...)
- `Message` (id, conversation_id, sender, content, timestamp, read_at, ...)
- `ConversationContext` (id, conversation_id, context_type, context_data, ...)
- `ClarificationSession` (id, conversation_id, ambiguity_score, iteration_count, resolved_at, ...)

**Schema Requirements:**
- Strict tenant isolation (organisation_id on all tables)
- Audit timestamps (created_at, updated_at)
- State transition tracking
- Foreign key constraints
- Indexes for performance

### 2. Data Models

**ORM Models Required:**
- All entities with relationships
- Validation rules
- State transition logic
- Query methods

### 3. Database Migrations

**Migration Scripts:**
- Initial schema creation
- Indexes and constraints
- Seed data (if applicable)
- Rollback scripts

### 4. Data Layer Tests

**Test Coverage (100% Required):**
- CRUD operations for all entities
- State transition validations
- Constraint enforcement (foreign keys, unique constraints)
- Tenant isolation verification
- Audit log validation
- Failure mode handling (database write failures, state conflicts)

---

## Success Criteria

**Build-to-Green Success:**
- ✅ All 18 QA components GREEN (QA-001 to QA-018)
- ✅ 100% test coverage for assigned QA
- ✅ Zero test debt (no skipped, commented, or incomplete tests)
- ✅ All database migrations execute successfully
- ✅ All schema constraints enforced
- ✅ Evidence artifacts generated for all QA components

**Gate Status:**
- ✅ GATE-SCHEMA-BUILDER-WAVE-1.0 = PASS

---

## Architecture Compliance

**Frozen Architecture:**
- Architecture V2 is FROZEN (2025-12-31)
- Implement exactly as specified in architecture
- No additions, no interpretations, no deviations

**One-Time Build Law:**
- Build-to-green exactly once
- No iteration or fix-forward
- If not green on first attempt, build is INVALID

**Zero Regression:**
- All QA must remain GREEN after passing
- GREEN → RED = regression = build STOP

**Zero Test Debt:**
- No skipped tests
- No commented tests
- No incomplete tests
- No placeholder tests

---

## Dependencies

**Blockers:** NONE (schema-builder can start immediately)

**Dependent Builders (After schema-builder completion):**
- ui-builder: Requires schema for Conversation UI data
- api-builder: Requires schema for Intent Processing persistence
- integration-builder: Requires schema for event persistence

**Parallel Work (Can start concurrently):**
- qa-builder: Test infrastructure (QA-132 to QA-210) — no dependency on schema

---

## Escalation Paths

**Blocking Issues:**
- Architecture ambiguity → Escalate to FM with specific question
- Missing architectural detail → Escalate to FM with gap description
- Conflicting requirements → Escalate to FM with conflict analysis

**Merge Gate Failures:**
- **STOP all work immediately**
- Report failure to FM with full details
- **DO NOT iterate independently**
- Wait for FM correction and updated instructions

**Build Failures:**
- If QA does not reach GREEN → Escalate to FM
- If regressions occur (GREEN → RED) → Escalate to FM immediately
- If test debt detected → Escalate to FM immediately

---

## Evidence Requirements

**For Each QA Component:**
- Test execution result (PASS/FAIL)
- Test output logs
- Coverage report (100% for assigned QA)
- Evidence artifact (JSON format)

**Gate Evidence:**
- Summary: All 18 QA GREEN
- Coverage: 100%
- Test Debt: Zero
- Regression Count: Zero

**Evidence Location:**
- Evidence artifacts stored in: `/evidence/wave-1.0/schema-builder/`
- Evidence format: See `QA_TO_RED_SUITE_SPEC.md`

---

## Governance Binding

**Constitutional Rules:**
- ✅ 100% QA Passing = PASS; <100% = TOTAL FAILURE
- ✅ Zero Test Debt (no skipped, commented, incomplete tests)
- ✅ Architecture Conformance (implement exactly as specified)
- ✅ Design Freeze (no modifications during execution)
- ✅ Build-to-Green (GREEN means 100% pass, zero failures, zero debt)

**Merge Gate Ownership:**
- FM owns merge gate readiness
- schema-builder STOPS on merge gate failure
- schema-builder escalates to FM (no independent iteration)
- FM investigates root cause and corrects coordination gaps

---

## Bootstrap Execution Model

**CS2 Actions (After Issue Creation):**
1. Create this issue in GitHub (verbatim)
2. Assign `@schema-builder` to the issue
3. Confirm assignment and notify FM

**schema-builder Actions:**
1. Review architecture specification (CONV-01 to CONV-04)
2. Implement database schema, models, migrations
3. Implement tests for QA-001 to QA-018
4. Execute tests and generate evidence
5. Report completion when all 18 QA GREEN

**FM Actions (During Execution):**
1. Monitor schema-builder progress
2. Respond to escalations immediately
3. Validate evidence artifacts
4. Declare GATE-SCHEMA-BUILDER-WAVE-1.0 status
5. Authorize next issue(s) after validation

---

## Next Steps (After schema-builder Completion)

**Immediate Next Issues (After Validation):**
1. **qa-builder** (QA-132 to QA-210) — Test infrastructure (can start in parallel)
2. **ui-builder** (QA-019 to QA-057) — UI components (depends on schema)
3. **api-builder** (QA-058 to QA-092) — Backend logic (depends on schema)

**Wave 1.0 Completion:**
- After all 5 builders complete their QA ranges
- All 210 QA components GREEN
- FM produces Wave 1.0 Readiness Certification

---

## References

**Architecture:**
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md`
- `QA_CATALOG.md`
- `QA_TO_RED_SUITE_SPEC.md`
- `QA_TRACEABILITY_MATRIX.md`

**Governance:**
- `BUILD_PHILOSOPHY.md` (T0-001)
- `governance/alignment/FM_MERGE_GATE_MANAGEMENT_CANON.md` (T0-014)
- `governance/specs/build-to-green-enforcement-spec.md` (T0-011)
- `governance/contracts/quality-integrity-contract.md` (T0-012)

**Builder Contract:**
- `foreman/builder/schema-builder-spec.md`

---

**Issue Status:** READY FOR CS2 EXECUTION  
**Authorized By:** FM (2026-01-02)  
**Authority:** FM Agent Contract v3.0.0, FM Execution Mandate (T0-013)

---

**END OF ISSUE SPECIFICATION**
```

---

## CS2 Execution Instructions

**For CS2 (Johan) to execute:**

1. **Create GitHub Issue**
   - Title: `Wave 1.0.1 — Schema Foundation (schema-builder: QA-001 to QA-018)`
   - Body: Use issue body above (verbatim)
   - Labels: `wave-1.0`, `schema-builder`, `execution`

2. **Assign Builder**
   - Assign: `@schema-builder`
   - Confirm assignment

3. **Notify FM**
   - Comment on this PR: "Issue created and assigned to schema-builder"
   - Include issue number

**After schema-builder reports completion:**
- FM will validate evidence
- FM will declare gate status
- FM will authorize next issue(s)

---

## Execution Sequencing Decision

**Why schema-builder first?**

| Criterion | Assessment |
|-----------|------------|
| **Risk** | Lowest risk (18 QA, clear scope) |
| **Dependencies** | None (can start immediately) |
| **Blocking Impact** | High (blocks ui-builder, api-builder) |
| **Scope Clarity** | Highest (database schema well-defined) |
| **Validation Value** | High (validates full execution loop) |

**Other builders blocked until schema complete:**
- ui-builder: Needs schema for UI data binding
- api-builder: Needs schema for business logic persistence
- integration-builder: Needs schema for event persistence

**qa-builder can run in parallel:**
- No schema dependency (test infrastructure)
- Can be authorized concurrently if desired

**Recommended Sequencing:**
1. **Phase 1:** schema-builder (this issue)
2. **Phase 2 (Concurrent):** qa-builder + ui-builder + api-builder
3. **Phase 3:** integration-builder (after ui, api complete)

---

## Success Criteria (This Issue)

This first execution issue specification is complete when:

- ✅ Issue specification document created
- ✅ Issue body is clear and actionable
- ✅ CS2 can create GitHub issue without interpretation
- ✅ schema-builder can execute without clarification
- ✅ FM monitoring and escalation paths defined

**Status:** ✅ **COMPLETE — READY FOR CS2 EXECUTION**

---

**Certified By:** Maturion Foreman (FM)  
**Date:** 2026-01-02  
**Authority:** FM Agent Contract v3.0.0, FM Execution Mandate (T0-013)  
**Context:** Wave 1.0 First Execution Issue (Bootstrap Mode)

---

**END OF FIRST EXECUTION ISSUE SPECIFICATION**
