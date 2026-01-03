# FM Builder Appointment Instruction Template

**Version**: 1.0.0  
**Status**: Canonical Reference  
**Authority**: `governance/ROLE_APPOINTMENT_PROTOCOL.md`  
**Addresses**: BL-0007 (Irresponsible Appointment of Officials Will Collapse the Model)  
**Last Updated**: 2026-01-03

---

## I. Purpose

This document provides the **canonical template** for Maturion Foreman (FM) to use when appointing builders to Build-to-Green tasks.

**Authority**: This template derives from `governance/ROLE_APPOINTMENT_PROTOCOL.md` Section II (Phase 2: Appointment Issuance) and enforces constitutional appointment requirements.

**Status**: **MANDATORY** — FM MUST use this template format for all builder appointments. No free-form or abbreviated appointments permitted.

---

## II. Template Structure

### A. Complete Appointment Instruction

```markdown
APPOINTMENT: [BUILDER-NAME]

Role: [UI-Builder | API-Builder | Schema-Builder | Integration-Builder | QA-Builder]
Task ID: [TASK-ID]
Build Wave: [WAVE-ID] (if applicable)

BUILD TO GREEN

Architecture Reference: [ABSOLUTE-PATH-TO-FROZEN-ARCHITECTURE]
QA Suite Location: [ABSOLUTE-PATH-TO-QA-SUITE]
QA Current Status: RED ([COUNT] tests failing)
Acceptance Criteria: All tests must pass (100%)

Scope Boundaries:
What IS in scope:
- [EXPLICIT-SCOPE-ITEM-1]
- [EXPLICIT-SCOPE-ITEM-2]
- [EXPLICIT-SCOPE-ITEM-3]

What IS NOT in scope:
- [EXPLICIT-OUT-OF-SCOPE-ITEM-1]
- [EXPLICIT-OUT-OF-SCOPE-ITEM-2]
- [EXPLICIT-OUT-OF-SCOPE-ITEM-3]

Governance Constraints:
- Design Freeze: ACTIVE (architecture and QA frozen)
- Zero Test Debt: MANDATORY
- 100% QA Pass: REQUIRED
- Gate Compliance: MANDATORY
- Escalation Path: → Foreman → Johan

Success Criteria:
- All tests GREEN (100%)
- Zero test debt
- Zero warnings
- Evidence trail complete
- Foreman validation passed

Ripple Intelligence Alignment Confirmation:

Governance Canon Version: [VERSION-OR-COMMIT-REF]
Last Canonical Sync: [ISO-8601-DATE]
Ripple Status: [STABLE | IN_PROGRESS | CONFLICT]
Builder Contract Version: [VERSION]
Canonical Authorities Current: [YES | NO]

Confirmation Statement:
- [x] Builder agent contract reflects current Ripple Intelligence obligations
- [x] Builder context is current with latest governance canon
- [x] No ripple ambiguity exists
- [x] Appointment may proceed with governance-current context

FM declares: Ripple Intelligence Alignment = CONFIRMED
```

---

## III. Template Components (Detailed)

### A. Header Section

```
APPOINTMENT: [BUILDER-NAME]

Role: [Builder Role]
Task ID: [Task ID]
Build Wave: [Wave ID]
```

**Requirements**:
- `BUILDER-NAME` MUST be one of: `UI-BUILDER`, `API-BUILDER`, `SCHEMA-BUILDER`, `INTEGRATION-BUILDER`, `QA-BUILDER`
- `Role` MUST match the builder name
- `Task ID` MUST be unique and traceable
- `Build Wave` is optional but recommended for multi-wave builds

**Purpose**: Clearly identifies which builder is being appointed and for what task.

---

### B. BUILD TO GREEN Declaration

```
BUILD TO GREEN
```

**Requirements**:
- MUST be present exactly as shown
- MUST be on its own line
- No variation permitted

**Purpose**: Explicit declaration that this is a Build-to-Green instruction, not a design or planning task.

---

### C. Architecture and QA References

```
Architecture Reference: [ABSOLUTE-PATH-TO-FROZEN-ARCHITECTURE]
QA Suite Location: [ABSOLUTE-PATH-TO-QA-SUITE]
QA Current Status: RED ([COUNT] tests failing)
Acceptance Criteria: All tests must pass (100%)
```

**Requirements**:
- `Architecture Reference` MUST be an absolute path to frozen architecture document
- `QA Suite Location` MUST be an absolute path to QA test suite
- `QA Current Status` MUST explicitly state RED and include test count
- `Acceptance Criteria` MUST explicitly state 100% pass requirement

**Purpose**: Provides builder with exact references to frozen specifications and clear success criteria.

**Validation**:
- FM MUST verify architecture exists and is frozen before issuing appointment
- FM MUST verify QA suite exists and is RED before issuing appointment
- FM MUST verify test count is accurate

---

### D. Scope Boundaries

```
Scope Boundaries:
What IS in scope:
- [EXPLICIT-SCOPE-ITEM-1]
- [EXPLICIT-SCOPE-ITEM-2]
- [EXPLICIT-SCOPE-ITEM-3]

What IS NOT in scope:
- [EXPLICIT-OUT-OF-SCOPE-ITEM-1]
- [EXPLICIT-OUT-OF-SCOPE-ITEM-2]
- [EXPLICIT-OUT-OF-SCOPE-ITEM-3]
```

**Requirements**:
- MUST include both "What IS in scope" and "What IS NOT in scope"
- MUST be explicit (no "etc.", no "similar items")
- MUST be complete (all relevant scope items listed)
- MUST prevent scope ambiguity

**Purpose**: Prevents scope creep and ensures builder knows exactly what to implement and what to avoid.

**Examples**:

**Good Scope Definition**:
```
What IS in scope:
- Implement Dashboard component per architecture section 3.2
- Implement Navigation component per architecture section 3.3
- Make all 12 failing dashboard tests pass
- Follow design specifications exactly

What IS NOT in scope:
- API integration (Integration Builder scope)
- Authentication logic (API Builder scope)
- Database queries (Schema Builder scope)
- Creating additional tests (QA Builder scope)
- Modifying architecture or QA
```

**Bad Scope Definition**:
```
What IS in scope:
- Build the dashboard
- Make tests pass

What IS NOT in scope:
- Backend stuff
```

---

### E. Governance Constraints

```
Governance Constraints:
- Design Freeze: ACTIVE (architecture and QA frozen)
- Zero Test Debt: MANDATORY
- 100% QA Pass: REQUIRED
- Gate Compliance: MANDATORY
- Escalation Path: → Foreman → Johan
```

**Requirements**:
- MUST include Design Freeze status
- MUST include Zero Test Debt requirement
- MUST include 100% QA Pass requirement
- MUST include Gate Compliance requirement
- MUST include Escalation Path

**Purpose**: Reminds builder of constitutional constraints that apply to all execution.

**Notes**:
- These constraints are **non-negotiable**
- Builder MUST acknowledge these constraints explicitly
- Violation of these constraints triggers FM intervention

---

### F. Success Criteria

```
Success Criteria:
- All tests GREEN (100%)
- Zero test debt
- Zero warnings
- Evidence trail complete
- Foreman validation passed
```

**Requirements**:
- MUST be explicit and measurable
- MUST include 100% test pass requirement
- MUST include zero test debt requirement
- MUST include zero warnings requirement
- MUST include evidence trail requirement
- MUST include FM validation requirement

**Purpose**: Defines exactly what "complete" means for this appointment.

---

### G. Ripple Intelligence Alignment Confirmation

```
Ripple Intelligence Alignment Confirmation:

Governance Canon Version: [VERSION-OR-COMMIT-REF]
Last Canonical Sync: [ISO-8601-DATE]
Ripple Status: [STABLE | IN_PROGRESS | CONFLICT]
Builder Contract Version: [VERSION]
Canonical Authorities Current: [YES | NO]

Confirmation Statement:
- [x] Builder agent contract reflects current Ripple Intelligence obligations
- [x] Builder context is current with latest governance canon
- [x] No ripple ambiguity exists
- [x] Appointment may proceed with governance-current context

FM declares: Ripple Intelligence Alignment = CONFIRMED
```

**Requirements** (from `governance/ROLE_APPOINTMENT_PROTOCOL.md` Section IV-A):
- FM MUST verify builder contract currency
- FM MUST verify governance canon version
- FM MUST verify ripple status (STABLE / IN_PROGRESS / CONFLICT)
- FM MUST confirm all checkboxes before declaring CONFIRMED
- FM MUST NOT appoint if ripple status is IN_PROGRESS or CONFLICT

**Purpose**: Ensures builder is appointed with current governance context, preventing stale assumptions and governance drift.

**Validation Procedure**:
1. Check governance canon status: `cat governance/alignment/canonical_sync_status.json | grep sync_status`
2. Verify builder contract currency: `grep "canonical_authorities:" .github/agents/[builder]-builder.md`
3. Evaluate ripple status: STABLE / IN_PROGRESS / CONFLICT
4. Document confirmation in appointment record

**Reference**: `governance/ROLE_APPOINTMENT_PROTOCOL.md` Section IV-A

---

## IV. Invalid Appointment Examples

### A. Missing QA-to-Red (INVALID)

```
APPOINTMENT: API-BUILDER

Role: API Builder
Task ID: BUILD-FM-WAVE1-API-001

Scope: Implement user authentication API

Architecture Reference: /architecture/builds/wave-1-1/frozen-architecture.md
Success Criteria: Authentication works
```

**Why Invalid**:
- Missing "BUILD TO GREEN" declaration
- Missing QA Suite Location
- Missing QA Current Status (must be RED)
- Missing Scope Boundaries (what IS and IS NOT in scope)
- Missing Governance Constraints
- Missing Ripple Intelligence Alignment Confirmation
- Vague success criteria ("authentication works" is not testable)

**Builder Response**:
```
INVALID APPOINTMENT: BuildPhilosophyViolation

Missing Required Components:
1. "BUILD TO GREEN" declaration
2. QA Suite Location not provided
3. QA Current Status not provided (must be RED)
4. Scope boundaries not explicit
5. Governance constraints not listed
6. Ripple Intelligence Alignment not confirmed
7. Success criteria vague ("authentication works" is not 100% QA pass)

Cannot proceed. Builders accept ONLY "Build to Green" instructions with complete appointment package.

Requesting corrected appointment.
```

---

### B. Ambiguous Scope (INVALID)

```
APPOINTMENT: UI-BUILDER

Role: UI Builder
Task ID: BUILD-FM-WAVE1-UI-001

BUILD TO GREEN

Architecture Reference: /architecture/builds/wave-1-1/frozen-architecture.md
QA Suite Location: /tests/ui/dashboard-tests.spec.ts
QA Current Status: RED (12 tests failing)
Acceptance Criteria: All tests must pass (100%)

Scope: Build the dashboard and related components

Governance Constraints:
- Design Freeze: ACTIVE
- Zero Test Debt: MANDATORY
- 100% QA Pass: REQUIRED

Success Criteria:
- All tests GREEN (100%)
- Zero test debt
```

**Why Invalid**:
- Scope is ambiguous ("related components" — which ones?)
- Missing "What IS in scope" and "What IS NOT in scope" explicit lists
- Missing Ripple Intelligence Alignment Confirmation

**Builder Response**:
```
INVALID APPOINTMENT: Scope Ambiguity

Scope boundaries not explicit:
- "related components" is ambiguous — which components?
- No explicit "What IS in scope" list
- No explicit "What IS NOT in scope" list

Ripple Intelligence Alignment not confirmed.

Cannot proceed with ambiguous scope.

Requesting clarification: Which specific components are in scope? Which are out of scope?
```

---

## V. Valid Appointment Example

```
APPOINTMENT: UI-BUILDER

Role: UI Builder
Task ID: BUILD-FM-WAVE1-UI-001
Build Wave: Wave 1.1

BUILD TO GREEN

Architecture Reference: /home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app/architecture/builds/wave-1-1/frozen-architecture.md
QA Suite Location: /home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app/tests/ui/dashboard-tests.spec.ts
QA Current Status: RED (12 tests failing)
Acceptance Criteria: All tests must pass (100%)

Scope Boundaries:
What IS in scope:
- Implement Dashboard component per architecture section 3.2
- Implement Navigation component per architecture section 3.3
- Make all 12 failing dashboard tests pass (test IDs: QA-UI-001 through QA-UI-012)
- Follow design specifications in architecture sections 3.2 and 3.3 exactly
- Implement accessibility per WCAG 2.1 AA requirements in architecture

What IS NOT in scope:
- API integration (Integration Builder scope)
- Authentication logic (API Builder scope)
- Database queries (Schema Builder scope)
- Creating additional tests (QA Builder scope)
- Modifying frozen architecture or QA suite
- Admin dashboard components (different task)
- Settings page components (different task)

Governance Constraints:
- Design Freeze: ACTIVE (architecture and QA frozen)
- Zero Test Debt: MANDATORY
- 100% QA Pass: REQUIRED
- Gate Compliance: MANDATORY
- Escalation Path: → Foreman → Johan

Success Criteria:
- All 12 tests GREEN (100%)
- Zero test debt in UI suite
- Zero TypeScript errors
- Zero lint warnings/errors
- Zero console errors in test runs
- Evidence trail complete (implementation notes, decisions)
- Foreman validation passed

Ripple Intelligence Alignment Confirmation:

Governance Canon Version: commit-abc123def456
Last Canonical Sync: 2026-01-03T10:00:00Z
Ripple Status: STABLE
Builder Contract Version: 2.0.0
Canonical Authorities Current: YES

Confirmation Statement:
- [x] Builder agent contract reflects current Ripple Intelligence obligations
- [x] Builder context is current with latest governance canon
- [x] No ripple ambiguity exists
- [x] Appointment may proceed with governance-current context

FM declares: Ripple Intelligence Alignment = CONFIRMED
```

**Why Valid**:
- ✅ Complete header section
- ✅ "BUILD TO GREEN" declaration present
- ✅ Architecture reference (absolute path)
- ✅ QA suite location (absolute path)
- ✅ QA current status (RED with count)
- ✅ Explicit scope boundaries (IS and IS NOT in scope)
- ✅ Complete governance constraints
- ✅ Measurable success criteria
- ✅ Ripple Intelligence Alignment confirmed

**Builder Response**:
```
ACKNOWLEDGED: UI-BUILDER APPOINTMENT

I acknowledge and accept:
- AGENT_CONSTITUTION.md as supreme authority
- BUILD_PHILOSOPHY.md as supreme building authority
- GOVERNANCE_AUTHORITY_MATRIX.md as authority reference
- Design Freeze is ACTIVE
- Zero Test Debt is MANDATORY
- 100% QA Pass is REQUIRED
- OPOJD (One-Prompt One-Job Done) execution discipline

I confirm understanding of:
- My role: UI Builder
- My scope: Implement Dashboard and Navigation components only (architecture sections 3.2-3.3)
- My boundaries: No API, no DB, no auth, no test creation, no other dashboards
- My escalation path: → Foreman → Johan

I confirm understanding of:
- Work to be performed: Make 12 failing dashboard tests pass (QA-UI-001 through QA-UI-012)
- Success criteria: 100% pass, zero debt, zero warnings, zero errors
- Artifacts provided: Frozen architecture (sections 3.2-3.3), RED QA suite (12 tests)
- Constraints: Design Freeze, no scope expansion, exact architecture conformance

I declare:
- Architecture reviewed and understood (sections 3.2-3.3)
- QA-to-Red reviewed and understood (12 tests failing as expected)
- No blocking questions
- Ready to execute BUILD TO GREEN
```

---

## VI. Template Usage Requirements

### A. When FM MUST Use This Template

FM MUST use this template for:
- ✅ All builder appointments (UI, API, Schema, Integration, QA)
- ✅ All Build-to-Green task assignments
- ✅ All builder re-appointments (if builder revoked and re-assigned)

FM MUST NOT:
- ❌ Create custom or abbreviated appointment formats
- ❌ Skip required template sections
- ❌ Use informal appointment instructions
- ❌ Assume builder understands implicit scope

### B. Template Validation Checklist

Before issuing appointment, FM MUST verify:
- [ ] All template sections present
- [ ] "BUILD TO GREEN" declaration present
- [ ] Architecture reference is absolute path and file exists
- [ ] Architecture is frozen (Design Freeze ACTIVE)
- [ ] QA suite location is absolute path and file exists
- [ ] QA current status is RED (verified via test run)
- [ ] Test count is accurate
- [ ] Scope boundaries are explicit (IS and IS NOT lists complete)
- [ ] Governance constraints are complete
- [ ] Success criteria are measurable
- [ ] Ripple Intelligence Alignment is CONFIRMED
- [ ] All ripple alignment checkboxes are checked

**If ANY checkbox is unchecked → Appointment is INVALID → FM MUST NOT issue**

### C. Template Customization Rules

FM MAY customize:
- ✅ Task-specific scope items
- ✅ Task-specific success criteria (beyond mandatory items)
- ✅ Task-specific governance constraints (beyond mandatory items)

FM MUST NOT customize:
- ❌ Template structure
- ❌ "BUILD TO GREEN" declaration
- ❌ Mandatory governance constraints
- ❌ Mandatory success criteria (100% pass, zero debt, zero warnings)
- ❌ Ripple Intelligence Alignment section

---

## VII. Builder Acknowledgment Requirements

### A. Mandatory Acknowledgment Format

Upon receiving appointment, builder MUST respond with acknowledgment using the format defined in `governance/ROLE_APPOINTMENT_PROTOCOL.md` Section III (Phase 3: Acknowledgement).

**Required Components**:
1. Constitutional Acceptance
2. Scope Confirmation
3. Mandate Confirmation
4. Readiness Declaration OR Blocking Questions

### B. Invalid Appointment Detection

Builder MUST REJECT appointment if:
- Any required template section is missing
- Scope boundaries are ambiguous
- Architecture or QA references are invalid
- QA current status is not RED
- Ripple Intelligence Alignment is not CONFIRMED

**Builder Response**: Use "INVALID APPOINTMENT" response format (see Section IV).

---

## VIII. Terminal-State Execution Discipline (OPOJD)

### A. OPOJD Enforcement via Appointment

This template enforces **OPOJD (One-Prompt One-Job Done)** by:
- Providing complete instructions (no need for clarification mid-execution)
- Defining explicit scope boundaries (no scope ambiguity)
- Stating clear success criteria (no interpretation needed)
- Declaring Design Freeze (no architecture changes during execution)

### B. Permitted Builder States

After appointment acknowledgment, builder MAY transition to:
- `EXECUTING`: Active Build-to-Green implementation
- `BLOCKED`: Legitimate STOP condition encountered
- `COMPLETE`: 100% QA green achieved

Builder MUST NOT:
- Pause for non-STOP clarification
- Request approval between steps
- Fragment execution into approval-gated steps

**Reference**: BUILD_PHILOSOPHY.md Section IX (OPOJD)

---

## IX. Integration with State Model

### A. Appointment Record Storage

When FM issues appointment using this template, FM MUST create appointment record:

**Storage**: `memory/governance/appointments/<task-id>.json`

**Initial State**:
```json
{
  "appointment_status": "APPOINTMENT_INCOMPLETE",
  "execution_status": null,
  "intervention_status": "NONE",
  "appointment_instruction": { ... }
}
```

### B. State Transitions

**After Template Issuance**:
1. FM issues appointment → `appointment_status: APPOINTMENT_INCOMPLETE`
2. Builder acknowledges → `appointment_status: APPOINTMENT_COMPLETE`
3. FM authorizes execution → `execution_status: EXECUTING`

**Reference**: `governance/specs/BUILDER_APPOINTMENT_EXECUTION_STATE_MODEL.md`

---

## X. Success Criteria

This template is successful when:

1. ✅ FM cannot issue non-conforming appointments
2. ✅ Builders receive complete, unambiguous instructions
3. ✅ No free-form or abbreviated appointment paths exist
4. ✅ Ripple Intelligence Alignment is verified before appointment
5. ✅ OPOJD discipline is enforced via complete instructions
6. ✅ Scope boundaries prevent scope creep
7. ✅ Invalid appointments are rejected by builders
8. ✅ Appointment instructions are auditable and traceable

---

## XI. References

**Authoritative Governance**:
- `governance/ROLE_APPOINTMENT_PROTOCOL.md` — Complete appointment protocol
- `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md` — BL-0007, BL-016
- `BUILD_PHILOSOPHY.md` Section IX — OPOJD
- `governance/specs/BUILDER_APPOINTMENT_EXECUTION_STATE_MODEL.md` — State tracking

**Agent Contracts**:
- `.github/agents/ForemanApp-agent.md` Section XII-A — FM appointment authority
- `.github/agents/*-builder.md` — Builder appointment compliance sections

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Canonical Reference (MANDATORY)  
**Authority**: Constitutional (from ROLE_APPOINTMENT_PROTOCOL.md)  
**Last Updated**: 2026-01-03  
**Owner**: Maturion Foreman (FM)  
**Enforcer**: FM + Builders (builders MUST reject non-conforming appointments)

---

*END OF FM BUILDER APPOINTMENT INSTRUCTION TEMPLATE*
