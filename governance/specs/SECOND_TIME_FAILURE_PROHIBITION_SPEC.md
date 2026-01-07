# Second-Time Failure Prohibition and TARP Specification (FM Repository)

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Status:** ACTIVE (Mandatory)  
**Authority:** Derived from Governance PR #877 (maturion-foreman-governance)  
**Canonical Source:** `maturion-foreman-governance` Repository  
**FM Implementation:** This Document

---

## I. Purpose and Authority

### Canonical Grounding

This specification implements the **No Second-Time Failures** principle and **TARP (Targeted Analysis and Recovery Plan)** protocol from the governance repository (PR #877) within the FM repository context.

**Upstream Governance Authority:**
- Governance PR #877: "Canonize BL-018/BL-019: QA Catalog Alignment, BL Forward-Scan, and Second-Time Failure Prohibition"
- Source Document: `BUILD_PHILOSOPHY.md` v1.3 - No Second-Time Failures section
- Source Document: `TARP_SECOND_TIME_FAILURE_TEMPLATE.md` (governance repo)

**This document translates canonical governance into FM-specific execution requirements.**

### Purpose

The Second-Time Failure Prohibition establishes that:

1. **First-time failures are CATASTROPHIC learnings** - handled with great urgency
2. **Second-time failures are EMERGENCY** - invoke TARP protocol immediately
3. **Third-time failures are CONSTITUTIONALLY PROHIBITED** - must be blocked by design

This specification defines:
- How to classify failures by occurrence count
- When and how to invoke TARP
- EMERGENCY procedures for second-time failures
- Prevention mechanisms to block third-time failures

---

## II. Failure Classification by Occurrence

### First-Time Failure
**Definition:** A failure pattern occurs for the FIRST time in the repository/project history.

**Severity:** **CATASTROPHIC**

**Response:**
1. Register as BL/FL/CI immediately
2. Perform root cause analysis
3. Execute forward-scan to find ALL instances of the pattern
4. Correct ALL instances
5. Create governance ratchet to prevent recurrence
6. Persist evidence and learnings

**Example:** BL-018 (Wave 2.2 QA Catalog Misalignment - FIRST time this pattern occurred)

**Expectations:**
- Treated with GREAT URGENCY
- NEVER accept as "normal" or "expected"
- Measures implemented must PREVENT recurrence
- Pattern must NEVER occur again

---

### Second-Time Failure
**Definition:** The SAME failure pattern occurs a SECOND time after:
- BL/FL/CI was registered for first occurrence
- Root cause was analyzed
- Corrections were made
- Governance ratchet was created

**Severity:** **BEYOND CATASTROPHIC** (EMERGENCY)

**Response:**
1. **HALT ALL EXECUTION** immediately
2. Declare **EMERGENCY** status
3. Invoke **TARP (Targeted Analysis and Recovery Plan)** protocol
4. Escalate to CS2 (Johan) immediately
5. Execute TARP analysis (see Section IV)
6. Wait for CS2 approval before resuming ANY work

**Example:** BL-019 (Wave 2.3+ QA Catalog Semantic Misalignment - SECOND occurrence of BL-018 pattern on THE SAME DAY)

**Critical Context:**
> "Second-time failures are not permitted at all. First-time failures are handled with great urgency and the measures we implement are for them to NEVER!!! occur again. This is a second-time failure and is considered beyond catastrophic."
> — CS2 (Johan) via BL-019 declaration

**Expectations:**
- **EMERGENCY** status - all work STOPS
- **ZERO TOLERANCE** - this should never happen
- **SYSTEMIC INVESTIGATION** - something is fundamentally broken
- **GOVERNANCE FAILURE** - ratchets didn't work or weren't applied

---

### Third-Time Failure
**Definition:** The SAME failure pattern occurs a THIRD time after:
- Two prior BL/FL/CI entries
- Two TARPs executed
- Multiple governance ratchets created

**Severity:** **CONSTITUTIONALLY PROHIBITED**

**Response:**
Third-time failures are **BLOCKED BY DESIGN**. The governance, automation, and process architecture must make a third occurrence **IMPOSSIBLE**.

If a third-time failure occurs:
1. **PROJECT HALT** - all activity stops
2. **CONSTITUTIONAL CRISIS** - governance model has failed
3. **ESCALATE TO AUTHORITY** - CS2 (Johan) only
4. **SYSTEMIC REDESIGN REQUIRED** - fundamental process/governance changes needed

**Expectations:**
- Third-time failures should be **IMPOSSIBLE** by governance design
- If they occur, the governance model itself is broken
- Recovery requires fundamental redesign, not tactical fixes

---

## III. Pattern Identification and Matching

### What Constitutes "The Same Pattern"?

A second-time (or third-time) failure occurs when the **ROOT CAUSE** matches a prior BL/FL/CI.

**Matching Criteria:**
- Same failure mechanism (e.g., "verification step omitted")
- Same process gap (e.g., "QA catalog alignment not checked")
- Same governance gap (e.g., "ratchet not applied")

**NOT Matching:**
- Different failure mechanism with similar symptoms
- Different process gap in different area
- Unrelated root causes that happen to affect same artifact

**Example (BL-018 vs BL-019):**
- BL-018: QA range QA-376 to QA-385 misaligned (Subwave 2.2)
- BL-019: QA ranges QA-341 to QA-350, QA-286 to QA-300, QA-301 to QA-320 misaligned (Subwaves 2.3, 2.10, 2.13)
- **Root Cause Match:** BOTH failures caused by "QA catalog semantic verification missing in wave planning"
- **Classification:** BL-019 is SECOND-TIME failure of BL-018 pattern

---

### Pattern Matching Procedure

When a new BL/FL/CI is registered:

1. Review ALL prior BL/FL/CI entries in registry
2. Compare root causes
3. Identify if pattern has occurred before
4. Count occurrences:
   - 0 prior = First-time failure (CATASTROPHIC)
   - 1 prior = Second-time failure (EMERGENCY - invoke TARP)
   - 2+ prior = Third-time failure (CONSTITUTIONALLY PROHIBITED)
5. Document pattern matching analysis in BL/FL/CI entry

**Pattern Matching Responsibility:**
- FM must perform pattern matching analysis
- FM must declare occurrence count explicitly
- FM must invoke TARP if second-time failure detected

---

## IV. TARP Protocol (Second-Time Failure Response)

TARP = **Targeted Analysis and Recovery Plan**

TARP is invoked IMMEDIATELY when a second-time failure is detected.

### TARP Step 1: Emergency Declaration
**Objective:** Halt all work and declare EMERGENCY status.

**Actions:**
1. STOP all active builder work immediately
2. BLOCK all pending subwave authorizations
3. Declare EMERGENCY in all active issues
4. Notify CS2 (Johan) immediately with:
   - Second-time failure summary
   - Pattern match evidence
   - Current execution state
   - Proposed TARP scope

**Output:** EMERGENCY declaration document

---

### TARP Step 2: Second-Order Root Cause Analysis
**Objective:** Understand WHY the first-time failure prevention measures failed.

**Questions to Answer:**
1. **First-Time Failure:**
   - What was the first-time failure pattern?
   - What root cause was identified?
   - What corrections were made?
   - What ratchet was created?

2. **Ratchet Effectiveness:**
   - Was the ratchet correctly designed?
   - Was the ratchet properly documented?
   - Was the ratchet actually implemented in governance?
   - Was the ratchet activated and enforced?

3. **Second-Time Failure:**
   - When/where did the pattern recur?
   - Why didn't the ratchet prevent it?
   - Was the ratchet:
     - Not applied? (enforcement failure)
     - Applied incorrectly? (execution failure)
     - Insufficient? (design failure)
     - Bypassed? (governance failure)

4. **Systemic Gaps:**
   - What systemic issue allowed recurrence?
   - Is this a one-off failure or indicator of broader problems?
   - What governance/process redesign is required?

**Output:** Second-order root cause analysis document

---

### TARP Step 3: Emergency Corrections
**Objective:** Execute immediate corrections to stop further recurrence.

**Actions:**
1. Correct ALL instances of second-time failure pattern (re-do forward-scan if needed)
2. Fix systemic gap that allowed recurrence
3. Strengthen or replace failing ratchet
4. Add redundant prevention mechanisms
5. Update governance to make pattern impossible going forward

**Requirements:**
- ALL corrections must be VERIFIED
- ALL corrections must be DOCUMENTED
- ALL corrections must be PERSISTENT (not temporary workarounds)

**Output:** Emergency correction log with verification evidence

---

### TARP Step 4: Governance Hardening
**Objective:** Update governance to make third-time failure IMPOSSIBLE.

**Actions:**
1. Review and strengthen ratchets:
   - Add automation where manual checks failed
   - Add redundant checks
   - Add enforcement gates
   - Make violations BLOCKING (not just warnings)

2. Update agent contracts:
   - FM contract: Strengthen obligations
   - Builder contracts: Add verification requirements
   - Add STOP conditions for pattern detection

3. Create prevention architecture:
   - Automated validation tools
   - Pre-flight checks
   - Continuous monitoring
   - Alert mechanisms

**Requirements:**
- Hardening must make pattern **structurally impossible**
- Cannot rely solely on human vigilance
- Must have automated enforcement where possible
- Must have redundant prevention layers

**Output:** Governance hardening specification

---

### TARP Step 5: TARP Evidence Pack
**Objective:** Document TARP execution and results for CS2 review.

**Required Sections:**
1. **Executive Summary**
   - First-time failure summary
   - Second-time failure summary
   - Pattern match analysis
   - Second-order root cause
   - Emergency corrections executed
   - Governance hardening implemented

2. **Timeline**
   - First-time failure date
   - First-time ratchet creation date
   - Second-time failure date
   - Time between failures
   - TARP execution timeline

3. **Evidence**
   - First-time BL/FL/CI entry
   - First-time ratchet document
   - Second-time BL/FL/CI entry
   - Pattern match analysis
   - Second-order RCA
   - Correction evidence
   - Governance updates

4. **Prevention Architecture**
   - Updated ratchets
   - New automation
   - Governance changes
   - Agent contract updates

5. **Residual Risk Assessment**
   - Likelihood of third-time failure
   - Remaining gaps (if any)
   - Monitoring mechanisms
   - Escalation triggers

6. **Resumption Readiness Statement**
   - All corrections complete: YES/NO
   - All governance updates complete: YES/NO
   - All automation implemented: YES/NO
   - CS2 approval required: YES/NO

**Output:** TARP Evidence Pack (for CS2 review)

---

### TARP Step 6: CS2 Review and Resumption Authorization
**Objective:** Obtain CS2 approval to resume execution.

**Procedure:**
1. Submit TARP Evidence Pack to CS2 (Johan)
2. Wait for CS2 review
3. Address any CS2 feedback or requirements
4. Obtain explicit CS2 authorization to resume execution
5. Document authorization in TARP Evidence Pack

**Resumption Criteria (CS2 Decision):**
- ✅ Second-order root cause is credible and complete
- ✅ Emergency corrections are sufficient and verified
- ✅ Governance hardening makes third-time failure structurally impossible
- ✅ FM demonstrates understanding of failure and prevention
- ✅ No additional concerns or gaps identified

**FM MUST NOT resume execution without CS2 authorization after TARP.**

**Output:** CS2 authorization to resume (or additional requirements)

---

## V. FM Responsibilities

### During Normal Execution
1. Maintain awareness of all prior BL/FL/CI patterns
2. Execute ratchets correctly and completely
3. Verify ratchet compliance before authorizations
4. Monitor for pattern recurrence

### When Registering New BL/FL/CI
1. Perform pattern matching analysis against all prior BL/FL/CI entries
2. Classify occurrence count (first, second, third)
3. If second-time failure detected:
   - HALT all execution immediately
   - Invoke TARP protocol
   - Escalate to CS2
4. Do not proceed until TARP complete and CS2 authorizes resumption

### During TARP Execution
1. Execute all TARP steps completely
2. Document all analyses, corrections, and governance updates
3. Produce TARP Evidence Pack
4. Submit to CS2 for review
5. Wait for authorization
6. Do NOT resume execution until CS2 approves

### After TARP Completion
1. Apply all governance hardening changes
2. Update agent contracts as required
3. Notify affected builders of changes
4. Resume execution only after CS2 authorization

---

## VI. Builder Expectations

Builders may observe EMERGENCY status and TARP execution when:
- Their work is halted due to second-time failure
- Their subwave specifications are updated due to TARP corrections
- Their agent contracts are updated due to TARP governance hardening

**Builders MUST:**
- STOP immediately when FM declares EMERGENCY
- Acknowledge TARP pause and wait for resumption authorization
- Review and acknowledge updated agent contracts after TARP
- Re-verify preconditions after TARP corrections

**Builders MUST NOT:**
- Continue work during EMERGENCY/TARP
- Bypass updated governance or ratchets
- Assume prior appointments are still valid after TARP

---

## VII. BL-018 and BL-019 Case Study

### BL-018: First-Time Failure (CATASTROPHIC)
- **Date:** 2026-01-05
- **Pattern:** QA Catalog semantic verification missing in Wave 2.2 planning
- **Response:**
  - BL-018 registered
  - Root cause analysis performed
  - Ratchet created: `WAVE_2_EXECUTION_RATCHET_QA_CATALOG_VERIFICATION.md`
  - Forward-scan initiated (but NOT completed before next appointment)

### BL-019: Second-Time Failure (EMERGENCY)
- **Date:** 2026-01-05 (SAME DAY as BL-018)
- **Pattern:** SAME - QA Catalog semantic verification missing in Wave 2.3+ planning
- **Critical Failure:** BL-018 ratchet was created but NOT applied to existing Wave 2.3+ plans before next appointment
- **Response:**
  - EMERGENCY declared
  - TARP invoked (implicitly through emergency corrective action)
  - Complete Wave 2 forward-scan executed
  - Multiple subwaves corrected (2.3, 2.10, 2.13)
  - Governance hardening: QA_CATALOG_ALIGNMENT_GATE_SPEC.md created
  - CS2 oversight increased

### Key Lessons
1. **Forward-scan MUST complete BEFORE next appointment** - BL-019 occurred because forward-scan was incomplete
2. **Ratchets MUST be applied retroactively** - existing plans must be corrected, not just future plans
3. **Second-time failures can occur IMMEDIATELY** - same-day recurrence is possible if forward-scan incomplete
4. **TARP is MANDATORY** - emergency status and complete analysis required

---

## VIII. Prevention Architecture

To make third-time failures **structurally impossible**, the following prevention layers exist:

### Layer 1: Agent Contract Obligations
- FM contract: MUST execute ratchets before authorizations
- Builder contracts: MUST verify preconditions before accepting appointments
- Both: MUST STOP if pattern detected

### Layer 2: Governance Gates
- QA-Catalog-Alignment Gate (mandatory, blocking)
- Forward-scan obligation (mandatory, blocking)
- Other ratchet-specific gates

### Layer 3: Automation (Future)
- Automated pattern detection
- Automated ratchet compliance checking
- Automated forward-scan execution
- Continuous monitoring and alerting

### Layer 4: Redundant Verification
- FM verifies before authorization
- Builder verifies before acceptance
- QA-of-QA verifies in tests
- CS2 audits in oversight

### Layer 5: Constitutional Enforcement
- Third-time failures are PROHIBITED by governance
- Governance supremacy rule makes violations non-negotiable
- CS2 has authority to halt execution if governance violated

**Goal:** Make pattern recurrence **structurally impossible**, not just "unlikely" or "discouraged"

---

## IX. Enforcement and Compliance

### Constitutional Status
Second-time failure prohibition is **MANDATORY** per:
- T0-001: BUILD_PHILOSOPHY.md v1.3 (No Second-Time Failures)
- T0-002: Governance Supremacy Rule (governance is non-negotiable)
- T0-013: FM_EXECUTION_MANDATE.md (FM must enforce governance)
- Governance PR #877: Second-Time Failure Prohibition Canon

### Enforcement Mechanism
- FM MUST perform pattern matching on all new BL/FL/CI entries
- FM MUST invoke TARP if second-time failure detected
- FM MUST halt execution until TARP complete and CS2 authorizes resumption
- CS2 oversight includes TARP review and authorization

### Non-Compliance
Failure to invoke TARP or halt execution for second-time failure is:
- **Constitutional violation**
- **Governance supremacy violation**
- **Potentially a third-time failure enabler** (making third-time failure possible)

Consequences:
- Immediate escalation to CS2
- Potential FM authority review
- Governance hardening around TARP enforcement

---

## X. References

### Upstream Governance
- **Governance PR #877:** Canonization of BL-018/BL-019 learnings and second-time failure prohibition
- **BUILD_PHILOSOPHY.md v1.3:** No Second-Time Failures section
- **TARP_SECOND_TIME_FAILURE_TEMPLATE.md:** TARP protocol template (governance repo)

### FM Repository Documents
- **QA_CATALOG_ALIGNMENT_GATE_SPEC.md:** Ratchet created from BL-018/BL-019
- **BL_FORWARD_SCAN_OBLIGATION_SPEC.md:** Forward-scan protocol (prevents second-time failures)
- **BOOTSTRAP_EXECUTION_LEARNINGS.md:** BL registry (pattern history)
- **FLCI_REGISTRY_UPDATE_BL_*.md:** FL/CI entries (pattern history)

### Case Studies
- **BL-018:** First-time QA Catalog misalignment
- **BL-019:** Second-time QA Catalog misalignment (EMERGENCY)
- **FLCI_REGISTRY_UPDATE_BL_019_SECOND_FAILURE_CATASTROPHIC.md:** BL-019 emergency declaration
- **WAVE_2_EMERGENCY_CORRECTIVE_ACTION_PLAN_BL_019.md:** TARP evidence (BL-019)

---

## XI. Version History

**v1.0.0 (2026-01-05):**
- Initial creation
- Layered down from governance PR #877
- Documents BL-018 and BL-019 learnings
- Establishes TARP protocol for FM repository
- Mandatory for all second-time failure responses

---

**Document Owner:** Maturion Foreman (FM)  
**Maintenance:** Governance updates from canonical source  
**Status:** ACTIVE — All second-time failures MUST trigger TARP immediately
