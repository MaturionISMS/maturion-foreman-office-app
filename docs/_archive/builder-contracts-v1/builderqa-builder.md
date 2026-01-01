# Builder Contract: qa-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** qa-builder  
**Builder Type:** Specialized Builder (QA & Testing)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED

**Capabilities:**
- testing (test implementation and execution)
- coverage (test coverage analysis and reporting)
- qa-of-qa (meta-testing and QA validation)

**Responsibilities:**
- QA tests
- Coverage

**Forbidden Actions:**
- ❌ Architecture modification
- ❌ Governance changes

---

## QA Range Assignment (Bounded Scope)

**Assigned QA Range:** **QA-132 to QA-210**

**Total QA Components:** 79

**Subsystem Coverage:**
- Analytics Subsystem (ANALYTICS-01 to ANALYTICS-03): QA-132 to QA-146 (15 QA)
- Cross-Cutting Components (CROSS-01 to CROSS-06): QA-147 to QA-199 (53 QA)
- Flow-Based QA (partial): QA-200 to QA-210 (11 QA)

**Authoritative Reference:** `QA_CATALOG.md` (QA-132 to QA-210)

---

## Gate Definition

**Gate ID:** `GATE-QA-BUILDER-WAVE-1.0`

**Gate Configuration:**
```yaml
gate:
  id: "GATE-QA-BUILDER-WAVE-1.0"
  type: "builder"
  builder: "qa-builder"
  required_green:
    - QA-132 to QA-210
  allowed_red:
    - ALL EXCEPT QA-132 to QA-210
  enforcement: "BLOCKING"
```

**Success Criteria:**
- ✅ All 79 QA GREEN
- ✅ Test infrastructure functional
- ✅ Cross-cutting concerns validated
- ✅ Analytics operational
- ✅ Evidence for all 79 QA

**Special Note:** qa-builder implements test infrastructure AND validates cross-cutting concerns.

---

## Evidence Obligations

**Per-QA Evidence Format:**
```json
{
  "qa_id": "QA-XXX",
  "status": "GREEN",
  "test_framework": "pytest",
  "evidence_artifacts": [
    {
      "type": "test_execution_result",
      "location": "foreman/evidence/qa/QA/QA-XXX/result.json"
    },
    {
      "type": "coverage_report",
      "location": "foreman/evidence/qa/QA/QA-XXX/coverage.json"
    }
  ]
}
```

**Aggregate Evidence:**
- Test coverage report (100% for QA-132 to QA-210)
- QA-of-QA validation results
- Test infrastructure documentation

---

## Escalation Rules

**Escalation Format (5 Elements):**
```
Builder: qa-builder
What: [Specific blocker]
Why: [Root cause]
Blocked: [Which QA cannot proceed]
Decision Required: [What FM should decide]
Consequence: [Impact if no decision]
```

**Escalation Destination:** ESC-02 Escalation Manager → FM

---

## Dependencies

**qa-builder has minimal dependencies:**
- Can work in parallel with other builders
- Validates work by all other builders

**Other builders may depend on qa-builder:**
- For test infrastructure and frameworks

---

## Contract Terms

### Builder Obligations

qa-builder MUST:
1. Make all 79 assigned QA GREEN (QA-132 to QA-210)
2. Generate complete evidence for each QA
3. Implement test infrastructure
4. Validate cross-cutting concerns
5. Provide test framework to other builders
6. Escalate blockers immediately
7. Work only within assigned QA range

### Builder Restrictions

qa-builder MUST NOT:
1. Modify architecture specifications
2. Change governance rules
3. Work on QA outside QA-132 to QA-210
4. Implement production code (only test code)

---

## FM Certification

**Certified By:** Foreman (FM)  
**Date:** 2025-12-31  
**Contract Status:** ACTIVE

---

## References

- `QA_CATALOG.md` (QA-132 to QA-210)
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Sections 10, 11
- `PHASE_4.5_BUILDER_TASK_SPECIFICATIONS.md`
- `foreman/builder/qa-builder-spec.md`

---

**END OF BUILDER CONTRACT: qa-builder**
