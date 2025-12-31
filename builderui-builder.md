# Builder Contract: ui-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** ui-builder  
**Builder Type:** Specialized Builder (UI & Frontend)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED

**Capabilities:**
- ui (UI component implementation)
- frontend (React components and state management)
- components (reusable UI components)
- styling (CSS, visual design, accessibility)

**Responsibilities:**
- UI components
- Layouts
- Wizards

**Forbidden Actions:**
- ❌ Backend logic
- ❌ Cross-module logic

---

## QA Range Assignment (Bounded Scope)

**Assigned QA Range:** **QA-019 to QA-057**

**Total QA Components:** 39

**Subsystem Coverage:**
- Conversational Interface UI (CONV-05): QA-019 to QA-022 (4 QA)
- Dashboard Subsystem (DASH-01 to DASH-04): QA-023 to QA-042 (20 QA)
- Parking Station UI (PARK-04): QA-054 to QA-057 (4 QA)
- Additional UI components: QA-043 to QA-053 (11 QA - Parking Station data layer UI interaction)

**Authoritative Reference:** `QA_CATALOG.md` (QA-019 to QA-057)

---

## Gate Definition

**Gate ID:** `GATE-UI-BUILDER-WAVE-1.0`

**Gate Configuration:**
```yaml
gate:
  id: "GATE-UI-BUILDER-WAVE-1.0"
  type: "builder"
  builder: "ui-builder"
  required_green:
    - QA-019 to QA-057
  allowed_red:
    - ALL EXCEPT QA-019 to QA-057
  enforcement: "BLOCKING"
```

**Success Criteria:**
- ✅ All 39 QA components GREEN
- ✅ UI components render correctly
- ✅ Accessibility standards met (WCAG 2.1 AA)
- ✅ Responsive design functional
- ✅ Real-time updates operational
- ✅ Evidence for all 39 QA

---

## Evidence Obligations

**Per-QA Evidence Format:**
```json
{
  "qa_id": "QA-XXX",
  "status": "GREEN",
  "test_framework": "jest/react-testing-library",
  "evidence_artifacts": [
    {
      "type": "screenshot",
      "location": "foreman/evidence/qa/UI/QA-XXX/screenshot.png"
    },
    {
      "type": "accessibility_report",
      "location": "foreman/evidence/qa/UI/QA-XXX/a11y_report.json"
    }
  ]
}
```

**Aggregate Evidence:**
- Visual regression test results
- Accessibility audit (WCAG 2.1 AA compliance)
- Responsiveness tests (mobile, tablet, desktop)
- Builder completion report

---

## Escalation Rules

**Escalation Format (5 Elements):**
```
Builder: ui-builder
What: [Specific blocker]
Why: [Root cause]
Blocked: [Which QA cannot proceed]
Decision Required: [What FM should decide]
Consequence: [Impact if no decision]
```

**Escalation Destination:** ESC-02 Escalation Manager → FM

---

## Dependencies

**ui-builder depends on:**
- ⚠️ **schema-builder** for data model contracts
- ⚠️ **api-builder** for API endpoint contracts

**No builders depend on ui-builder** (leaf builder in dependency graph)

---

## Contract Terms

### Builder Obligations

ui-builder MUST:
1. Make all 39 assigned QA GREEN (QA-019 to QA-057)
2. Generate complete evidence for each QA
3. Meet accessibility standards (WCAG 2.1 AA minimum)
4. Implement responsive design (mobile, tablet, desktop)
5. Escalate blockers immediately
6. Work only within assigned QA range

### Builder Restrictions

ui-builder MUST NOT:
1. Implement backend logic
2. Implement database schemas
3. Work on QA outside QA-019 to QA-057
4. Bypass accessibility standards

---

## FM Certification

**Certified By:** Foreman (FM)  
**Date:** 2025-12-31  
**Contract Status:** ACTIVE

---

## References

- `QA_CATALOG.md` (QA-019 to QA-057)
- `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Sections 3, 4, 5
- `PHASE_4.5_BUILDER_TASK_SPECIFICATIONS.md`
- `foreman/builder/ui-builder-spec.md`

---

**END OF BUILDER CONTRACT: ui-builder**
