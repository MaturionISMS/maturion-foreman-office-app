# Commissioning Wizard UI Specification

**Version**: 1.0.0  
**Status**: Architecture Specification (F-U1)  
**Module**: Commissioning UI  
**Type**: UI/UX Specification

---

## Purpose

The Commissioning Wizard UI is a **step-by-step, dummy-proof** interface for commissioning the FM application.

**Core Principle**: Enable a non-technical authority to commission the system with absolute clarity and zero ambiguity.

This specification is part of **Batch 2 — Memory & Commissioning Foundations** and adheres to strict constraints:

✅ **DOES**:
- Provide linear, step-by-step commissioning flow
- Show clear "Do this now" instructions
- Display validation status (green/red indicators)
- Lock steps until prerequisites are met
- Show status visibility at all times
- Explain blockers and next actions clearly

❌ **DOES NOT**:
- Auto-activate the system
- Skip validation steps
- Allow free navigation before completion
- Hide critical information
- Make assumptions about user knowledge

---

## UX Principles

### 1. Linear Flow Only

**Rule**: Users must complete steps in order. No jumping ahead.

**Rationale**: Commissioning is a critical process. Skipping steps could leave the system in an invalid state.

**Implementation**:
- Steps are numbered (1, 2, 3, ...)
- Future steps are visually disabled (greyed out)
- Clicking a future step shows a modal: "Please complete Step X first"
- Previous steps can be reviewed but not modified once complete

### 2. Clear Instructions

**Rule**: Every step has explicit, actionable instructions.

**Format**:
```
Step X: [Action Required]

[Clear explanation of what this step validates]

DO THIS NOW:
• [Specific action 1]
• [Specific action 2]
• [Specific action 3]

[Button: Check Status]
```

### 3. Immediate Validation Feedback

**Rule**: After each action, show immediate feedback.

**States**:
- ⏳ **Checking**: "Validating requirements..."
- ✅ **Pass**: "Requirement satisfied. Proceeding to next step."
- ❌ **Fail**: "Requirement not met. See details below."
- ⚠️ **Warning**: "Non-critical issue detected. You may proceed or fix it."

### 4. No Silent Progress

**Rule**: Every state change must be visible and explained.

**Implementation**:
- Progress bar shows current step and overall completion
- Each step shows its status (Not Started / In Progress / Complete / Blocked)
- Failed validations show clear error messages and remediation guidance
- Success transitions show confirmation message

### 5. Forced Redirection

**Rule**: Users cannot access other parts of the app until commissioning is complete.

**Implementation**:
- All routes redirect to commissioning wizard until complete
- Modal appears if user tries to navigate away
- Browser back button redirects to commissioning
- No "Skip" or "Cancel" buttons during critical steps

---

## Step Definitions

### Step 1: Welcome & Readiness Check

**Objective**: Explain commissioning and perform initial system check.

**UI Elements**:
- Welcome message explaining what commissioning is
- List of what will be validated
- Estimated time to complete (5-10 minutes)
- [Button: Begin Commissioning]

**Validation**: None (information only)

**Next**: Automatically proceed to Step 2

---

### Step 2: Memory Fabric Validation

**Objective**: Ensure memory system is initialized and operational.

**Instructions**:
```
DO THIS NOW:
1. Verify memory directory exists: /memory
2. Check memory lifecycle state
3. Confirm no critical failures

If memory is not initialized, run:
  init-memory-fabric.py
```

**Validation**:
- Memory directory structure exists
- Memory lifecycle state is USABLE (not DEGRADED or FAILED)
- No privacy violations detected

**Status Indicators**:
- ✅ Memory Initialized
- ✅ Lifecycle State: USABLE
- ✅ Privacy Check: PASS

**On Failure**:
- Show specific blocker (e.g., "Memory lifecycle is FAILED")
- Show remediation command
- [Button: Re-check After Fix]

**Next**: Step 3 (only if all validations pass)

---

### Step 3: Governance Structure Validation

**Objective**: Ensure governance policies and specifications are in place.

**Instructions**:
```
DO THIS NOW:
1. Verify governance directory exists: /governance
2. Check for required policy files
3. Confirm architecture index is present
```

**Validation**:
- Governance directory structure complete
- Required policy files exist
- Architecture index present and valid

**Status Indicators**:
- ✅ Governance Policies: PRESENT
- ✅ Architecture Index: VALID
- ✅ Privacy Guardrails: CONFIGURED

**On Failure**:
- Show missing files
- Provide links to canonical governance repository
- [Button: Re-check After Fix]

**Next**: Step 4 (only if all validations pass)

---

### Step 4: Security & Privacy Configuration

**Objective**: Validate security and privacy settings.

**Instructions**:
```
DO THIS NOW:
1. Verify privacy guardrails are configured
2. Check environment variables are set
3. Confirm no secrets in memory or code
```

**Validation**:
- Privacy guardrails configured
- Required environment variables set (NODE_ENV, etc.)
- No PII or secrets detected

**Status Indicators**:
- ✅ Privacy Guardrails: CONFIGURED
- ✅ Environment Variables: SET
- ✅ Secret Detection: PASS

**On Failure**:
- Show specific configuration issues
- Provide remediation guidance
- [Button: Re-check After Fix]

**Next**: Step 5 (only if all validations pass)

---

### Step 5: Dependency Validation

**Objective**: Ensure runtime dependencies are installed.

**Instructions**:
```
DO THIS NOW:
1. Verify node_modules directory exists
2. Check that all required packages are installed
3. Confirm no dependency vulnerabilities
```

**Validation**:
- Runtime dependencies installed
- No critical vulnerabilities detected
- Package versions compatible

**Status Indicators**:
- ✅ Dependencies: INSTALLED
- ✅ Vulnerabilities: NONE CRITICAL
- ✅ Compatibility: VERIFIED

**On Failure**:
- Show missing or vulnerable packages
- Provide remediation command: `npm install`
- [Button: Re-check After Fix]

**Next**: Step 6 (only if all validations pass)

---

### Step 6: Final System Check & Activation

**Objective**: Perform comprehensive readiness check and activate the system.

**Instructions**:
```
FINAL CHECKS:
All previous validations will be re-run to ensure
nothing changed during commissioning.

If all checks pass, the system will be marked as COMMISSIONED.
```

**Validation**:
- Re-run all previous validations
- Confirm no regressions
- System is in valid state

**On Success**:
- Show comprehensive readiness report
- Display overall readiness percentage (must be 100%)
- [Button: Commission System]

**On Failure**:
- Show which step failed
- Navigate back to failing step
- Require user to fix and retry

**Next**: Commissioning Complete Screen

---

### Step 7: Commissioning Complete

**Objective**: Confirm commissioning is complete and grant access to the application.

**UI Elements**:
- ✅ Success message: "System Successfully Commissioned"
- Summary of completed validations
- Timestamp of commissioning
- [Button: Enter Application]

**Actions**:
- Update commissioning state to COMMISSIONED
- Enable access to main application
- Log commissioning event to audit trail
- Redirect to main dashboard

---

## UI Components

### Progress Bar

**Location**: Top of screen, always visible

**Display**:
```
Step 2 of 7: Memory Fabric Validation
[███████░░░░░░░░░░░░] 28% Complete
```

**Behavior**:
- Updates automatically as steps complete
- Cannot be clicked to jump ahead
- Clicking completed steps shows review modal (read-only)

---

### Status Card

**Used In**: Each validation step

**Layout**:
```
┌─────────────────────────────────────────┐
│ ⏳ Checking Memory Lifecycle State...   │
└─────────────────────────────────────────┘

or

┌─────────────────────────────────────────┐
│ ✅ Memory Initialized                   │
│ ✅ Lifecycle State: USABLE              │
│ ✅ Privacy Check: PASS                  │
│                                         │
│ [Continue to Next Step]                 │
└─────────────────────────────────────────┘

or

┌─────────────────────────────────────────┐
│ ❌ REQUIREMENT NOT MET                  │
│                                         │
│ Issue: Memory lifecycle is FAILED       │
│                                         │
│ Remediation:                            │
│ 1. Check memory health logs             │
│ 2. Run: init-memory-fabric.py           │
│ 3. Restart commissioning wizard         │
│                                         │
│ [Re-check After Fix]                    │
└─────────────────────────────────────────┘
```

---

### Blocker Modal

**Triggered When**: User tries to skip a step or navigate away

**Layout**:
```
┌─────────────────────────────────────────┐
│  ⚠️ Cannot Skip This Step               │
│                                         │
│  Commissioning requires all steps to be │
│  completed in order. Please complete:   │
│                                         │
│  Step 2: Memory Fabric Validation       │
│                                         │
│  Before proceeding to:                  │
│  Step 3: Governance Structure           │
│                                         │
│  [Back to Current Step]                 │
└─────────────────────────────────────────┘
```

---

### Status Sidebar

**Location**: Right side of screen, always visible

**Display**:
```
COMMISSIONING STATUS

Step 1: Welcome ✅ COMPLETE
Step 2: Memory Fabric ⏳ IN PROGRESS
Step 3: Governance Structure ⬜ NOT STARTED
Step 4: Security & Privacy ⬜ NOT STARTED
Step 5: Dependencies ⬜ NOT STARTED
Step 6: Final Check ⬜ NOT STARTED
Step 7: Complete ⬜ NOT STARTED

Overall Readiness: 28%
```

---

## Navigation Rules

### Allowed Navigation

✅ **Review Previous Steps**: User can click completed steps to review (read-only)
✅ **Current Step**: User can interact with current step
✅ **Help/Documentation**: User can access help without leaving wizard

### Prohibited Navigation

❌ **Skip Ahead**: Future steps are disabled, clicking shows blocker modal
❌ **Exit Wizard**: No exit button, all routes redirect back to wizard
❌ **Browser Back**: Intercepts back button, shows confirmation modal
❌ **Main App Access**: All app routes redirect to wizard until commissioning complete

---

## Error Handling

### Validation Failure

**Response**:
1. Show clear error message
2. Display specific requirement that failed
3. Provide remediation guidance
4. Show [Re-check After Fix] button
5. Do NOT auto-advance

### System Error

**Response**:
1. Show technical error details (for debugging)
2. Provide escalation path (contact support)
3. Log error to audit trail
4. Show [Retry] and [Report Issue] buttons

### Network/API Failure

**Response**:
1. Show "Connection Issue" message
2. Explain impact (cannot validate requirements)
3. Show [Retry] button with loading indicator
4. If repeated failures, show offline guidance

---

## Accessibility

### Keyboard Navigation

- Tab through steps and buttons
- Enter to activate buttons
- Escape to dismiss modals (where appropriate)
- Arrow keys to review previous steps

### Screen Reader Support

- ARIA labels on all interactive elements
- Status announcements on validation complete
- Error messages read immediately
- Progress updates announced

### Visual Accessibility

- High contrast mode support
- Colorblind-safe indicators (not just red/green)
- Text scaling support (up to 200%)
- Focus indicators on all interactive elements

---

## Integration Points

### Data Sources

**RequirementLoader** (`lib/startup/RequirementLoader.ts`):
- Provides validation logic
- Returns `StartupAssessment` with results
- Identifies blockers and warnings

**CommissioningController** (`lib/commissioning/CommissioningController.ts`):
- Provides commissioning state
- Updates state when commissioning complete
- Provides commissioning history

### APIs (Conceptual)

```typescript
// Get current commissioning state
GET /api/commissioning/status
Response: { state: "COMMISSIONING", currentStep: 2 }

// Validate a specific step
POST /api/commissioning/validate/{step}
Response: { passed: true, results: [...] }

// Complete commissioning
POST /api/commissioning/complete
Response: { commissioned: true, timestamp: "..." }
```

---

## State Management

### Wizard State

```typescript
interface CommissioningWizardState {
  currentStep: number;
  completedSteps: number[];
  stepStatus: {
    [step: number]: 'not_started' | 'in_progress' | 'complete' | 'blocked';
  };
  overallReadiness: number;
  blockers: string[];
  warnings: string[];
}
```

### Persistence

- State saved to localStorage (browser)
- State also saved to backend (commissioning state file)
- On page refresh, restore from last saved state
- If step fails, do not mark as complete

---

## Testing Requirements

### Unit Tests

- Test each step component renders correctly
- Test validation logic for each step
- Test navigation rules (skip prevention)
- Test error handling and recovery

### Integration Tests

- Test full wizard flow (all steps)
- Test state persistence and restoration
- Test redirection logic
- Test API integration

### UX Tests

- Test with non-technical users
- Measure time to complete
- Measure error rate (how often users need help)
- Verify clarity of instructions

---

## Batch 2 Compliance

Per Batch 2 requirements, this UI specification:

✅ **DOES**:
- Provide pure visibility and guidance layer
- Show clear next steps and blockers
- Require explicit human action for each step
- Prevent implicit progression
- Surface all validation results clearly

❌ **DOES NOT**:
- Auto-activate the system
- Auto-advance through steps
- Bypass validation checks
- Hide critical information
- Execute builds or external delegation

---

## Future Enhancements

### Phase 2 (Post-Batch 2)

- **Automated Remediation**: One-click fixes for common issues
- **Progress Persistence**: Save progress across sessions
- **Multi-Language Support**: Localize instructions
- **Video Tutorials**: Embedded help videos for each step
- **Diagnostic Tools**: Built-in system health checker

---

## Critical Statement

**This UI does not trigger execution, builds, or external delegation.**

The Commissioning Wizard is a pure visibility and guidance layer. All validation is performed by the `RequirementLoader`, and all state updates are explicit user actions.

---

## Governance

**Authority**: Issue #172 (F-U1)  
**Batch**: Batch 2 — Memory & Commissioning Foundations  
**Architecture**: Pure visibility layer  
**QA**: UI component tests required  
**Compliance**: Zero auto-activation, zero implicit progression

---

## Files (Implementation, Future)

```
app/commissioning/
├── page.tsx                     # Main wizard page
├── layout.tsx                   # Commissioning layout
├── steps/
│   ├── 1-welcome.tsx
│   ├── 2-memory-validation.tsx
│   ├── 3-governance-validation.tsx
│   ├── 4-security-validation.tsx
│   ├── 5-dependency-validation.tsx
│   ├── 6-final-check.tsx
│   └── 7-complete.tsx
├── components/
│   ├── ProgressBar.tsx
│   ├── StatusCard.tsx
│   ├── BlockerModal.tsx
│   └── StatusSidebar.tsx
└── README.md                    # Implementation guide

tests/ui/
└── test_commissioning_wizard_spec.py  # Spec validation tests
```

---

**End of Commissioning Wizard UI Specification**

**STATUS**: Architecture Specification Only — Implementation Pending
