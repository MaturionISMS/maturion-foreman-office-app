# Builder Appointment Acknowledgment Format

## Purpose

This document defines the **mandatory appointment acknowledgment format** all builders must use when receiving appointments from FM.

**Authority**: `governance/ROLE_APPOINTMENT_PROTOCOL.md`  
**Addresses**: BL-0007 (Irresponsible Appointment of Officials Will Collapse the Model)  
**Status**: CONSTITUTIONAL — Non-negotiable

**Extracted from builder agent contracts per Issue #447/#448 (prompt size compliance)**

---

## Mandatory Appointment Acknowledgment Format

Upon appointment, builders MUST respond with:

```
ACKNOWLEDGED: [BUILDER-NAME] APPOINTMENT

I acknowledge and accept:
- AGENT_CONSTITUTION.md as supreme authority
- BUILD_PHILOSOPHY.md as supreme building authority
- GOVERNANCE_AUTHORITY_MATRIX.md as authority reference
- Design Freeze is ACTIVE
- Zero Test Debt is MANDATORY
- 100% QA Pass is REQUIRED
- OPOJD (One-Prompt One-Job Done) execution discipline

I confirm understanding of:
- My role: [Builder Role]
- My scope: <explicit list from appointment>
- My boundaries: <explicit list from appointment>
- My escalation path: → Foreman → Johan

I confirm understanding of:
- Work to be performed: <summary from appointment>
- Success criteria: 100% QA pass, zero debt, zero warnings
- Artifacts provided: Frozen architecture, RED QA suite
- Constraints: Design Freeze, no scope expansion

I declare:
- Architecture reviewed and understood
- QA-to-Red reviewed and understood
- No blocking questions
- Ready to execute BUILD TO GREEN

OR

- STOP: I have blocking questions (list questions)
```

---

## Invalid Appointment Rejection Format

Builders MUST REJECT appointment if preconditions are missing:

```
INVALID APPOINTMENT: <specific-violation>

Missing Required Components:
1. <item-1>
2. <item-2>
...

Cannot proceed. Builders accept ONLY "Build to Green" instructions with:
- Architecture Reference: <path>
- QA Suite Location: <path>
- QA Current Status: RED (X tests failing)
- Acceptance Criteria: All tests must pass (100%)
- Scope Boundaries: What IS and IS NOT in scope
- Governance Constraints: Design Freeze, Zero Test Debt, etc.
- Ripple Intelligence Alignment: CONFIRMED

Requesting corrected appointment with complete appointment package.
```

---

## When to Use Each Format

### Use ACKNOWLEDGED Format When:
- ✅ All appointment preconditions met
- ✅ Architecture frozen and complete
- ✅ QA-to-Red tests exist and are RED
- ✅ Scope boundaries clear
- ✅ Success criteria unambiguous

### Use INVALID APPOINTMENT Format When:
- ❌ Architecture not frozen
- ❌ QA-to-Red tests missing
- ❌ Scope boundaries unclear
- ❌ Success criteria ambiguous
- ❌ Missing governance constraints
- ❌ Contradictory instructions

### Use STOP + Blocking Questions When:
- ⚠️ Preconditions appear met but ambiguities exist
- ⚠️ Technical questions before starting
- ⚠️ Clarification needed on scope edge cases

---

## Key Principle

**If builder cannot provide complete acknowledgment → STOP and escalate.**

Builders MUST NOT:
- ❌ Proceed without explicit appointment acknowledgment
- ❌ Begin work before verifying frozen architecture availability
- ❌ Begin work before verifying QA-to-Red suite availability
- ❌ Accept ambiguous or incomplete appointment instructions
- ❌ Assume appointment correctness implicitly

---

## Constitutional Grounding

**Authority**: `governance/ROLE_APPOINTMENT_PROTOCOL.md`  
**FM Integration**: `.github/agents/ForemanApp-agent.md` Section on Builder Appointment  
**All Builders**: qa-builder, api-builder, schema-builder, ui-builder, integration-builder

---

**Last Updated**: 2026-01-07  
**Extracted From**: Builder agent contracts
