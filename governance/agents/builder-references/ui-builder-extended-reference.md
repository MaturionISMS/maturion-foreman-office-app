# UI Builder Extended Reference

**Purpose**: Extended documentation for UI Builder contract  
**Authority**: `.github/agents/ui-builder.md`  
**Status**: Reference Material  
**Last Updated**: 2026-01-07

This document contains detailed examples, extended narratives, and supporting material for the UI Builder contract. The core contract file contains essential doctrine and obligations. This reference provides context and illustration.

---

## Detailed Appointment Acknowledgment Example

When appointed by FM, UI Builder provides complete acknowledgment with constitutional authority acceptance, role/scope/boundary confirmation, work summary understanding, precondition verification (architecture frozen, QA-to-Red present, memory fabric available), and status declaration (READY or BLOCKED).

Example includes verification of:
- Frozen UI component specifications
- QA-to-Red tests for all UI components
- Design system availability
- Component library dependencies
- Accessibility requirements
- Memory fabric status

---

## BL-018/BL-019 UI Builder Scenarios

### Scenario 1: Missing Component Specification

Builder appointed to implement Dashboard component, but architecture lacks component specification.

**Correct Response**: STOP, declare BLOCKED, document missing specification, escalate to FM per BL-018 awareness.

### Scenario 2: Design System Mismatch

Architecture specifies Material-UI components, but QA-to-Red tests check for Ant Design components.

**Correct Response**: STOP, declare BLOCKED, document mismatch between architecture and tests, escalate per BL-019 awareness.

---

## Code Checking Process for UI Implementation

### UI-Specific Checks

1. **Component Correctness**: Does component render expected output?
2. **Props Validation**: Are all props correctly typed and validated?
3. **Accessibility**: Are ARIA attributes present? Keyboard navigation working?
4. **Responsive Design**: Does component work on mobile/tablet/desktop?
5. **Style Consistency**: Does styling match design system?

**Example Walkthrough**: Implementation of Dashboard component
- Verify component renders with correct structure ✅
- Verify props are type-safe ✅
- Verify ARIA labels present ✅
- Verify responsive breakpoints work ✅
- Verify matches design tokens ✅
- Run QA-to-Red tests (RED → GREEN) ✅

---

## Enhancement Capture Examples for UI Builder

### Example 1: Component Library Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Reusable Card Component
Context: Multiple components use similar card patterns. A reusable Card component would 
improve consistency and reduce duplication.

Proposal: Create shared Card component in ui/components/shared/Card.tsx

Benefit: Reduces code duplication by ~40%, improves design consistency

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

### Example 2: Accessibility Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Focus Management Utility
Context: Managing focus for modals and dialogs requires similar logic across components. 
A focus management utility would improve accessibility consistency.

Proposal: Create useFocusTrap hook for modal/dialog focus management

Benefit: Improves accessibility, ensures consistent focus behavior, reduces boilerplate

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

---

**End of Extended Reference**
