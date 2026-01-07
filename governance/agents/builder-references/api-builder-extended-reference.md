# API Builder Extended Reference

**Purpose**: Extended documentation for API Builder contract  
**Authority**: `.github/agents/api-builder.md`  
**Status**: Reference Material  
**Last Updated**: 2026-01-07

This document contains detailed examples, extended narratives, and supporting material for the API Builder contract. The core contract file contains essential doctrine and obligations. This reference provides context and illustration.

---

## Detailed Appointment Acknowledgment Example

When appointed by FM, the API Builder provides a complete acknowledgment including:

- Constitutional authority acceptance (AGENT_CONSTITUTION.md, BUILD_PHILOSOPHY.md, GOVERNANCE_AUTHORITY_MATRIX.md)
- Design Freeze acknowledgment
- Zero Test Debt commitment
- 100% QA Pass requirement
- OPOJD (One-Prompt One-Job Done) execution discipline

**Example Structure**:
```
ACKNOWLEDGED: API BUILDER APPOINTMENT

I acknowledge and accept:
- AGENT_CONSTITUTION.md as supreme authority
- BUILD_PHILOSOPHY.md as supreme building authority
- GOVERNANCE_AUTHORITY_MATRIX.md as authority reference
- Design Freeze is ACTIVE
- Zero Test Debt is MANDATORY
- 100% QA Pass is REQUIRED
- OPOJD (One-Prompt One-Job Done) execution discipline

I confirm understanding of:
- My role: API Builder
- My scope: Backend API endpoints for Foreman Office module
- My boundaries: No UI, no schema changes, no governance modifications
- My escalation path: → Foreman → Johan

I confirm understanding of:
- Work to be performed: Implement API endpoints per frozen architecture
- Success criteria: 100% QA pass, zero debt, zero warnings
- Artifacts required: Builder QA Report, implementation complete, tests passing
- Frozen specs location: architecture/frozen/foreman-office/
- QA-to-Red suite location: tests/qa-to-red/foreman-office/

Precondition verification:
✅ Architecture specifications are frozen and available
✅ QA-to-Red test suite is present and failing as expected
✅ API route specifications defined in architecture
✅ Business logic requirements clear and unambiguous
✅ Memory fabric is available
✅ No blocking governance conditions detected

STATUS: READY TO PROCEED
```

---

## BL-018/BL-019 API Builder Scenarios

### Scenario 1: Missing API Route Definition

**Situation**: Builder is appointed to implement API endpoints for "User Management", but architecture has no user management routes defined.

**Correct Builder Response**:
```
APPOINTMENT PRECONDITION FAILURE DETECTED

Issue: Architecture missing API route definitions
Module: User Management
Expected: API route specifications in architecture/frozen/foreman-office/api/user-management.md
Actual: File not found or incomplete

This is a BL-018 precondition failure (architecture incompleteness).

ESCALATION TO FM:
"I cannot proceed with implementing User Management API because the architecture does not 
define the required API routes. Per BL-018 awareness, FM is obligated to ensure architecture 
completeness before builder appointment. Please freeze complete architecture specifications 
before reassigning this task."

BUILDER STATUS: BLOCKED (awaiting FM resolution)
```

### Scenario 2: QA-to-Red Test Misalignment

**Situation**: Architecture specifies POST /api/users endpoint, but QA-to-Red test checks GET /api/user (singular).

**Correct Builder Response**:
```
ARCHITECTURE-TEST MISALIGNMENT DETECTED

Architecture Spec: POST /api/users (plural)
QA-to-Red Test: GET /api/user (singular)

This is a BL-019 precondition failure (specification-test misalignment).

ESCALATION TO FM:
"There is a mismatch between the architecture specification and QA-to-Red test for user 
endpoints. Architecture defines POST /api/users but test expects GET /api/user. Per BL-019 
awareness, FM must resolve this through TARP before I can proceed."

BUILDER STATUS: BLOCKED (awaiting FM resolution)
```

---

## Code Checking Process for API Implementation

### Step-by-Step API Code Checking

**Scenario**: Builder has implemented POST /api/dashboards endpoint

#### Step 1: Logical Correctness Review
```
Builder reviews API implementation:
- Does endpoint handle request correctly?
- Are request validations in place?
- Are error responses appropriate?
- Is business logic sound?

✅ Verified: Endpoint validates input, handles errors, returns correct responses
```

#### Step 2: Architecture Alignment Review
```
Builder compares implementation to frozen architecture:
- Architecture specifies: POST /api/dashboards with JSON body
- Implementation: Matches specification exactly

✅ Verified: Implementation aligns with frozen architecture
```

#### Step 3: QA-to-Red Validation
```
Builder runs QA-to-Red tests:
- Expected: Tests transition from RED to GREEN
- Actual: All dashboard API tests now passing

✅ Verified: Implementation makes RED tests GREEN correctly
```

#### Step 4: Obvious Defects Detection
```
Builder checks for:
- SQL injection vulnerabilities ✅ None (using parameterized queries)
- Missing error handling ✅ All error paths handled
- Hardcoded values ✅ None found (using configuration)
- Missing input validation ✅ All inputs validated
- Broken imports ✅ All imports valid

✅ Verified: No obvious defects detected
```

#### Step 5: Self-Review
```
Builder asks:
- "Would this endpoint handle production traffic correctly?" ✅ Yes
- "Is error handling comprehensive?" ✅ Yes
- "Are security best practices followed?" ✅ Yes
- "Is the code maintainable?" ✅ Yes

✅ Verified: Self-review complete, API quality acceptable
```

---

## Enhancement Capture Examples for API Builder

### Example 1: API Performance Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Caching Layer for Dashboard Data API
Context: During implementation of /api/dashboards endpoint, I noticed that dashboard data 
is relatively static but queried frequently. A caching layer could reduce database load.

Proposal: Introduce Redis caching for dashboard data with 5-minute TTL, invalidated on 
dashboard updates.

Benefit: Reduces database queries by ~80% for dashboard views, improves API response time 
from ~200ms to ~20ms.

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

### Example 2: API Documentation Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: OpenAPI/Swagger Documentation Generation
Context: Current API endpoints lack machine-readable documentation. Adding OpenAPI spec 
generation would improve API discoverability and client library generation.

Proposal: Add @nestjs/swagger decorators to all API endpoints and generate OpenAPI 3.0 spec.

Benefit: Enables automatic client library generation, provides interactive API docs, 
improves developer experience.

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

### Example 3: No Enhancements Identified
```
ENHANCEMENT CAPTURE EVALUATION

Work Unit: User Management API implementation (/api/users endpoints)
Evaluation: No enhancement opportunities identified. Implementation follows established 
patterns, no new utilities needed, no architectural ambiguities encountered.

Statement: No enhancement proposals identified for this work unit.
```

---

## Memory Integration for API Builder

### Memory Loading Protocol

Before starting any API implementation task, API Builder MUST:

1. **Load Global Memories**
   - Scope: `global`
   - Tags: `['api', 'backend', 'architecture', 'security']`
   - Minimum Importance: `medium`

2. **Load Task-Specific Memories**
   - Scope: `wave-1-foreman-office` (or current task scope)
   - Tags: `['api', 'foreman-office', 'backend']`
   - Minimum Importance: `medium`

3. **Verify Memory Availability**
   - If memory fabric is unavailable: **STOP** and escalate to FM
   - If no relevant memories found: Acknowledge and proceed (memories optional but loading is mandatory)

### Memory Usage Example

```python
# API Builder memory loading sequence
memories = memory_fabric.load_memories(
    scopes=['global', 'wave-1-foreman-office'],
    tags=['api', 'backend', 'architecture', 'security', 'foreman-office'],
    min_importance='medium'
)

if memory_fabric.is_unavailable():
    raise BuilderBlockedException(
        "Memory fabric unavailable. Cannot proceed per memory integration requirements."
    )

# Use loaded memories to inform API implementation
for memory in memories:
    if memory.relates_to_api_security():
        apply_security_pattern(memory)
    if memory.relates_to_error_handling():
        apply_error_handling_pattern(memory)
```

---

## Gate Binding – API Builder QA Report Format

When work is complete, API Builder generates `BUILDER_QA_REPORT.md`:

```markdown
# Builder QA Report

**Builder**: API Builder  
**Wave**: 1.0  
**Module**: Foreman Office  
**Date**: 2025-12-30  

## Assignment

**Scope**: Backend API endpoints for Foreman Office module  
**Architecture Spec**: architecture/frozen/foreman-office/api/  
**QA Range**: QA-058 to QA-090 (API-related tests)  

## Completion Summary

**Endpoints Implemented**: 12  
**Tests Passing**: 45 ✅  
**Test Failures**: 0  
**Test Debt**: 0  

## Endpoints Delivered

1. POST /api/dashboards - Create dashboard ✅
2. GET /api/dashboards - List dashboards ✅
3. GET /api/dashboards/:id - Get dashboard details ✅
4. PUT /api/dashboards/:id - Update dashboard ✅
5. DELETE /api/dashboards/:id - Delete dashboard ✅
... (7 more endpoints)

## Code Checking Evidence

Code checking performed on all API implementations:
- Logical correctness verified ✅
- Architecture alignment verified ✅
- QA-to-Red validation successful ✅
- No obvious defects detected ✅
- Security best practices followed ✅
- Self-review complete ✅

Statement: Code checking complete. No obvious defects detected.

## Architecture Alignment

All endpoints align with frozen architecture:
- architecture/frozen/foreman-office/api/dashboard-api.md
- architecture/frozen/foreman-office/api/user-api.md
- architecture/frozen/foreman-office/api/config-api.md

## Security Considerations

- Input validation on all endpoints ✅
- Authentication required on protected routes ✅
- Authorization checks implemented ✅
- SQL injection prevention (parameterized queries) ✅
- XSS prevention (output encoding) ✅
- CSRF protection enabled ✅

## Memory Context

Memories loaded: 8 (scopes: global, wave-1-foreman-office)  
Memory fabric status: Available ✅  
Key patterns applied from memory: Error handling middleware, validation patterns

## Status

**READY** — All requirements met, zero debt, zero failures, security validated
```

---

**End of Extended Reference**
