# Builder Contract: integration-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** integration-builder  
**Builder Type:** Specialized Builder (Integration & Wiring)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED

**Capabilities:**
- integration (inter-component wiring)
- inter-module (event routing and messaging)
- events (event bus and pub/sub patterns)

**Responsibilities:**
- Module integrations

**Forbidden Actions:**
- ❌ UI implementation
- ❌ Database schemas

---

## QA Range Assignment (Bounded Scope)

**Assigned QA Range:** **QA-093 to QA-131**

**Total QA Components:** 39

**Subsystem Coverage:**
- Escalation & Supervision Subsystem (ESC-01 to ESC-04): QA-093 to QA-116 (24 QA)
- Governance Enforcement Subsystem (GOV-01 to GOV-03): QA-117 to QA-131 (15 QA)

**Authoritative Reference:** `QA_CATALOG.md` (QA-093 to QA-131)

---

## Gate Definition

**Gate ID:** `GATE-INTEGRATION-BUILDER-WAVE-1.0`

**Gate Configuration:**
```yaml
gate:
  id: "GATE-INTEGRATION-BUILDER-WAVE-1.0"
  type: "builder"
  builder: "integration-builder"
  required_green:
    - QA-093 to QA-131
  allowed_red:
    - ALL EXCEPT QA-093 to QA-131
  enforcement: "BLOCKING"
```

**Success Criteria:**
- ✅ All 39 QA GREEN
- ✅ Escalation system functional
- ✅ Governance enforcement operational
- ✅ Event routing validated
- ✅ Evidence for all 39 QA

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
      "type": "integration_test_result",
      "location": "foreman/evidence/qa/INT/QA-XXX/result.json"
    },
    {
      "type": "event_routing_log",
      "location": "foreman/evidence/qa/INT/QA-XXX/routing_log.json"
    }
  ]
}
```

---

## Escalation Rules

**Escalation Format (5 Elements):**
```
Builder: integration-builder
What: [Specific blocker]
Why: [Root cause]
Blocked: [Which QA cannot proceed]
Decision Required: [What FM should decide]
Consequence: [Impact if no decision]
```

**Escalation Destination:** ESC-02 Escalation Manager → FM

---

## Dependencies

**integration-builder depends on:**
- ⚠️ **api-builder** for components to integrate

**No builders depend on integration-builder** (leaf builder)

---

## Contract Terms

### Builder Obligations

integration-builder MUST:
1. Make all 39 assigned QA GREEN (QA-093 to QA-131)
2. Generate complete evidence for each QA
3. Implement ping generation and escalation
4. Implement governance loading and enforcement
5. Escalate blockers immediately
6. Work only within assigned QA range

### Builder Restrictions

integration-builder MUST NOT:
1. Implement UI components
2. Implement database schemas
3. Work on QA outside QA-093 to QA-131
4. Bypass governance rules

---

## FM Certification

**Certified By:** Foreman (FM)  
**Date:** 2025-12-31  
**Contract Status:** ACTIVE

---

## References

- `QA_CATALOG.md` (QA-093 to QA-131)
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Sections 8, 9
- `PHASE_4.5_BUILDER_TASK_SPECIFICATIONS.md`
- `foreman/builder/integration-builder-spec.md`

---

**END OF BUILDER CONTRACT: integration-builder**
