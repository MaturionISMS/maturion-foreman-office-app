# Builder Contract: api-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** api-builder  
**Builder Type:** Specialized Builder (Backend & API)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED

**Capabilities:**
- api (API endpoint implementation)
- backend (business logic and orchestration)
- logic (decision workflows and state management)
- routes (routing and command handling)

**Responsibilities:**
- API endpoints
- Handlers

**Forbidden Actions:**
- ❌ UI implementation
- ❌ Global state management

---

## QA Range Assignment (Bounded Scope)

**Assigned QA Range:** **QA-058 to QA-092**

**Total QA Components:** 35

**Subsystem Coverage:**
- Intent Processing Subsystem (INTENT-01 to INTENT-04): QA-058 to QA-077 (20 QA)
- Execution Orchestration Subsystem (EXEC-01 to EXEC-03): QA-078 to QA-092 (15 QA)

**Authoritative Reference:** `QA_CATALOG.md` (QA-058 to QA-092)

---

## Gate Definition

**Gate ID:** `GATE-API-BUILDER-WAVE-1.0`

**Gate Configuration:**
```yaml
gate:
  id: "GATE-API-BUILDER-WAVE-1.0"
  type: "builder"
  builder: "api-builder"
  required_green:
    - QA-058 to QA-092
  allowed_red:
    - ALL EXCEPT QA-058 to QA-092
  enforcement: "BLOCKING"
```

**Success Criteria:**
- ✅ All 35 QA GREEN
- ✅ Intent processing pipeline functional
- ✅ Clarification loop operational
- ✅ Build orchestration functional
- ✅ Evidence for all 35 QA

---

## Evidence Obligations

**Per-QA Evidence Format:**
```json
{
  "qa_id": "QA-XXX",
  "status": "GREEN",
  "test_framework": "pytest",
  "test_file": "tests/api/test_<component>.py",
  "evidence_artifacts": [
    {
      "type": "api_test_result",
      "location": "foreman/evidence/qa/API/QA-XXX/result.json"
    },
    {
      "type": "state_transition_log",
      "location": "foreman/evidence/qa/API/QA-XXX/state_log.json"
    }
  ]
}
```

---

## Escalation Rules

**Escalation Format (5 Elements):**
```
Builder: api-builder
What: [Specific blocker]
Why: [Root cause]
Blocked: [Which QA cannot proceed]
Decision Required: [What FM should decide]
Consequence: [Impact if no decision]
```

**Escalation Destination:** ESC-02 Escalation Manager → FM

---

## Dependencies

**api-builder depends on:**
- ⚠️ **schema-builder** for data models (Intent, RequirementSpec, Build entities)

**Other builders depend on api-builder:**
- ⚠️ **ui-builder** needs API contracts
- ⚠️ **integration-builder** needs component contracts

---

## Contract Terms

### Builder Obligations

api-builder MUST:
1. Make all 35 assigned QA GREEN (QA-058 to QA-092)
2. Generate complete evidence for each QA
3. Implement intent processing pipeline
4. Implement build orchestration
5. Escalate blockers immediately
6. Work only within assigned QA range

### Builder Restrictions

api-builder MUST NOT:
1. Implement UI components
2. Implement database schemas
3. Work on QA outside QA-058 to QA-092
4. Bypass state management rules

---

## FM Certification

**Certified By:** Foreman (FM)  
**Date:** 2025-12-31  
**Contract Status:** ACTIVE

---

## References

- `QA_CATALOG.md` (QA-058 to QA-092)
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Sections 6, 7
- `PHASE_4.5_BUILDER_TASK_SPECIFICATIONS.md`
- `foreman/builder/api-builder-spec.md`

---

**END OF BUILDER CONTRACT: api-builder**
