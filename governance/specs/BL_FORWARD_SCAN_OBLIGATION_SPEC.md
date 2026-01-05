# BL Forward-Scan Obligation Specification (FM Repository)

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Status:** ACTIVE (Mandatory)  
**Authority:** Derived from Governance PR #877 (maturion-foreman-governance)  
**Canonical Source:** `maturion-foreman-governance` Repository  
**FM Implementation:** This Document

---

## I. Purpose and Authority

### Canonical Grounding

This specification implements the **BL Forward-Scan Obligation** from the governance repository (PR #877) within the FM repository context.

**Upstream Governance Authority:**
- Governance PR #877: "Canonize BL-018/BL-019: QA Catalog Alignment, BL Forward-Scan, and Second-Time Failure Prohibition"
- Source Document: `LEARNING_INTAKE_AND_PROMOTION_MODEL.md` §6.3 (BL Forward-Scan Obligation)
- BUILD_PHILOSOPHY.md v1.3 - Learning and continuous improvement

**This document translates canonical governance into FM-specific execution requirements.**

### Purpose

The BL Forward-Scan Obligation ensures that when a failure pattern is discovered (BL/FL/CI), FM:

1. **Identifies the root pattern** that caused the failure
2. **Scans ALL in-scope work** (current, planned, and future) for the same pattern
3. **Corrects EVERY instance** of the pattern, not just the one that triggered the BL
4. **Produces and persists evidence** of the scan and corrections
5. **Prevents recurrence** through governance ratchets and process updates

This obligation is **MANDATORY** and **BLOCKING**. FM MUST complete forward-scan before authorizing any new work that could be affected by the pattern.

---

## II. Trigger Conditions (When Forward-Scan is Required)

FM MUST execute a forward-scan in the following circumstances:

### A. BL (Bootstrap Learning) Discovery
- **Trigger:** Any BL entry is registered in `BOOTSTRAP_EXECUTION_LEARNINGS.md`
- **Scope:** All waves, subwaves, and future planning affected by the pattern
- **Timing:** IMMEDIATELY after BL registration, BEFORE next subwave authorization

### B. FL (Field Learning) Discovery
- **Trigger:** Any FL entry is registered in governance FL/CI registry
- **Scope:** All waves, subwaves, and future planning affected by the pattern
- **Timing:** IMMEDIATELY after FL registration, BEFORE next subwave authorization

### C. CI (Continuous Improvement) Discovery
- **Trigger:** Any CI entry is registered in governance FL/CI registry
- **Scope:** All waves, subwaves, and future planning affected by the pattern
- **Timing:** IMMEDIATELY after CI registration, BEFORE next subwave authorization

### D. Second-Time Failure Discovery
- **Trigger:** Discovery that a BL/FL/CI pattern has recurred
- **Severity:** CATASTROPHIC - triggers TARP (see SECOND_TIME_FAILURE_PROHIBITION_SPEC.md)
- **Scope:** ENTIRE repository and all governance
- **Timing:** IMMEDIATE EMERGENCY forward-scan with elevated priority

---

## III. Forward-Scan Execution Protocol

### Step 1: Pattern Identification
**Objective:** Clearly define the failure pattern that must be scanned for.

**Procedure:**
1. Review the BL/FL/CI entry and root cause analysis
2. Identify the core pattern (e.g., "QA Catalog verification missing in wave planning")
3. Generalize the pattern to identify other potential occurrences
4. Document the pattern definition clearly

**Example (BL-018/BL-019):**
- **Pattern:** "QA range assigned to subwave without verifying QA catalog entries exist and semantically match"
- **Generalization:** "Any subwave with a QA range assignment that was not verified against QA_CATALOG.md"

**Output:** Pattern definition document

---

### Step 2: Scope Determination
**Objective:** Identify ALL work that could be affected by the pattern.

**Procedure:**
1. Identify all current waves/subwaves
2. Identify all planned waves/subwaves
3. Identify all future work areas that could exhibit the pattern
4. Document the scan scope boundaries

**Categories to Scan:**
- ✅ Current wave subwaves (authorized but not yet complete)
- ✅ Current wave subwaves (planned but not yet authorized)
- ✅ Future wave planning documents
- ✅ Builder sub-issue specifications
- ✅ Architecture documents (if pattern relates to architecture)
- ✅ QA Catalog (if pattern relates to QA)
- ✅ Governance documents (if pattern relates to process)

**Example (BL-018/BL-019):**
- **Scope:** All Wave 2 subwaves (2.1 to 2.14)
- **Scan:** Each subwave's QA range assignment in rollout plan and sub-issue files

**Output:** Scope definition with explicit boundaries

---

### Step 3: Systematic Scan Execution
**Objective:** Examine EVERY item in scope for the pattern.

**Procedure:**
1. For each item in scope:
   - Apply pattern detection criteria
   - Document whether pattern is present
   - Record evidence (file location, line number, description)
2. Create a scan log with findings
3. Mark each finding as:
   - **CONFIRMED:** Pattern definitely present, correction required
   - **SUSPECTED:** Pattern may be present, further investigation required
   - **CLEAR:** Pattern not present, no action required

**Scan Requirements:**
- ✅ Must be EXHAUSTIVE (cannot skip items)
- ✅ Must be DOCUMENTED (evidence for each item scanned)
- ✅ Must be REPRODUCIBLE (someone else can verify scan completeness)

**Example (BL-018/BL-019 Scan):**
```
Subwave 2.1: QA-331 to QA-340
- Catalog Verification: ✅ CLEAR (all QA IDs exist)
- Semantic Alignment: ✅ CLEAR (matches subwave intent)

Subwave 2.2: QA-376 to QA-385
- Catalog Verification: ❌ CONFIRMED (QA IDs allocated to different features)
- Semantic Alignment: ❌ CONFIRMED (failure modes vs. parking advanced)

Subwave 2.3: QA-341 to QA-350
- Catalog Verification: ❌ CONFIRMED (semantic mismatch with subwave intent)
- Semantic Alignment: ❌ CONFIRMED (analytics/cross vs. optimizations)
```

**Output:** Forward-scan log with findings for EVERY item in scope

---

### Step 4: Correction Execution
**Objective:** Fix EVERY confirmed instance of the pattern.

**Procedure:**
1. For each CONFIRMED finding:
   - Design correction (e.g., reassign QA range, extend QA catalog, update documentation)
   - Execute correction
   - Verify correction resolves the pattern instance
   - Document correction evidence
2. For each SUSPECTED finding:
   - Investigate further
   - Either confirm and correct, or clear and document rationale
3. Create correction log

**Correction Requirements:**
- ✅ Must address ALL confirmed findings (no partial fixes)
- ✅ Must be VERIFIED after implementation
- ✅ Must be DOCUMENTED with before/after evidence

**Example (BL-018/BL-019 Corrections):**
```
Subwave 2.2:
- Action: Remove from Wave 2 (not in scope)
- Verification: Rollout plan updated, issue closed
- Evidence: WAVE_2_ROLLOUT_PLAN.md diff, issue #398 closure comment

Subwave 2.3:
- Action: Extend QA Catalog with System Optimizations entries
- Action: Reassign subwave to new QA range (QA-401 to QA-410)
- Verification: QA_CATALOG.md updated, sub-issue file regenerated
- Evidence: QA_CATALOG.md diff, SUBWAVE_2.3_API_BUILDER_SYSTEM_OPTIMIZATIONS.md update
```

**Output:** Correction log with evidence for EVERY confirmed finding

---

### Step 5: Evidence Persistence
**Objective:** Create permanent record of forward-scan execution and results.

**Procedure:**
1. Create forward-scan evidence document:
   - BL/FL/CI reference
   - Pattern definition
   - Scope definition
   - Scan log (all items examined)
   - Findings summary (confirmed, suspected, clear counts)
   - Correction log (all corrections executed)
   - Verification results
2. Store in appropriate location:
   - Root directory for Wave-level scans
   - `governance/reports/` for governance scans
   - Evidence directory for historical scans
3. Link from BL/FL/CI entry

**Required Document Sections:**
- Executive Summary
- Pattern Definition
- Scope and Methodology
- Scan Results (complete log)
- Corrections Executed (complete log)
- Verification Evidence
- Residual Risk Assessment
- Governance Impact

**Example (BL-018/BL-019):**
- Document: `WAVE_2_FORWARD_SCAN_QA_ALIGNMENT_VERIFICATION.md`
- Location: Root directory (Wave 2 scope)
- Linked from: `FLCI_REGISTRY_UPDATE_BL_018.md`, `FLCI_REGISTRY_UPDATE_BL_019_SECOND_FAILURE_CATASTROPHIC.md`

**Output:** Forward-scan evidence document (persisted)

---

### Step 6: Governance Ratchet Creation
**Objective:** Prevent pattern recurrence through process/governance updates.

**Procedure:**
1. Identify governance/process gaps that allowed the pattern
2. Design ratchet (checklist, gate, automation, policy update)
3. Implement ratchet in governance documents
4. Update relevant agent contracts to enforce ratchet
5. Document ratchet in BL/FL/CI entry

**Ratchet Requirements:**
- ✅ Must be ENFORCEABLE (can verify compliance)
- ✅ Must be MANDATORY (not optional)
- ✅ Must be DOCUMENTED (clear requirements)
- ✅ Must be INTEGRATED (part of standard process)

**Example (BL-018/BL-019 Ratchet):**
- Ratchet: QA-Catalog-Alignment Gate (this spec's companion)
- Implementation: `governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md`
- Enforcement: FM Agent Contract Section XIV, Builder Agent Contracts
- Documentation: `WAVE_2_EXECUTION_RATCHET_QA_CATALOG_VERIFICATION.md`

**Output:** Governance ratchet document(s)

---

## IV. Forward-Scan Outcomes

### Outcome: COMPLETE
All steps executed, all findings corrected, evidence persisted, ratchets created.

**FM may proceed with:**
- Authorizing next subwave
- Continuing wave execution
- Planning future waves

**Required Evidence:**
- ✅ Forward-scan evidence document exists and is complete
- ✅ All confirmed findings have corrections executed and verified
- ✅ Governance ratchets created and activated
- ✅ BL/FL/CI entry updated with forward-scan link

---

### Outcome: BLOCKED
Forward-scan cannot complete due to:
- Scope ambiguity (cannot determine all affected work)
- Missing information (cannot verify pattern presence)
- Correction complexity (requires architecture changes, new waves, etc.)
- Resource constraints (cannot execute all corrections immediately)

**FM MUST:**
1. Document the blocker
2. Escalate to CS2 (Johan) with:
   - Blocker description
   - What was completed
   - What cannot be completed
   - Proposed resolution pathway
   - Timeline impact
3. HALT further wave execution until blocker resolved
4. Wait for CS2 decision

**FM MUST NOT:**
- Proceed with incomplete forward-scan
- Skip findings to unblock
- Assume low-risk findings can be deferred

---

### Outcome: PARTIAL (NOT PERMITTED)
Some findings corrected, but not all.

**This outcome is NOT PERMITTED.**

Forward-scan is **ALL OR NOTHING**:
- Either ALL findings are corrected and verified, OR
- Execution is BLOCKED pending correction

**There is no "partial forward-scan."**

---

## V. FM Responsibilities

### After BL/FL/CI Registration
1. IMMEDIATELY initiate forward-scan
2. BLOCK all new subwave authorizations until forward-scan complete
3. Execute forward-scan protocol (Steps 1-6)
4. Persist evidence
5. Update governance

### During Forward-Scan Execution
1. Document all steps and findings
2. Correct ALL confirmed instances
3. Create governance ratchets
4. Escalate if blocked

### After Forward-Scan Completion
1. Link forward-scan evidence to BL/FL/CI entry
2. Update wave planning with corrections
3. Notify affected builders (if any)
4. Resume wave authorization (if appropriate)

---

## VI. Builder Expectations

Builders may observe forward-scan execution if:
- Their current work is paused pending forward-scan completion
- Their appointment is delayed pending forward-scan completion
- Their subwave specification is updated due to forward-scan corrections

**Builders MUST:**
- Acknowledge forward-scan pause and wait for FM clearance
- Review updated subwave specifications after forward-scan corrections
- Re-verify preconditions if subwave specification changed

**Builders MUST NOT:**
- Proceed with work if FM declares forward-scan in progress
- Ignore updated subwave specifications
- Assume prior appointment is still valid after specification changes

---

## VII. Relationship to BL-018 and BL-019

This forward-scan obligation was triggered by:

- **BL-018:** Wave 2.2 QA Catalog Misalignment (first-time failure)
  - Forward-scan required: ALL Wave 2 subwaves for QA catalog alignment
  - Result: BL-019 discovered (multiple additional misalignments)

- **BL-019:** Wave 2.3+ QA Catalog Semantic Misalignment (second-time failure)
  - Forward-scan required: RE-SCAN ALL Wave 2 subwaves with increased rigor
  - Result: Additional misalignments corrected, Wave 2 execution unblocked

**Critical Lesson:**
BL-019 occurred because **forward-scan was not executed after BL-018 before issuing next appointment.**

**Prevention:**
This spec makes forward-scan MANDATORY and BLOCKING. FM cannot authorize new work until forward-scan is COMPLETE.

---

## VIII. Second-Time Failure Impact

If forward-scan reveals a **second-time failure** (same pattern recurs after BL/ratchet):
- **Severity escalates to CATASTROPHIC**
- **TARP (Targeted Analysis and Recovery Plan) is invoked**
- **EMERGENCY status** - all work halts pending analysis
- See: `SECOND_TIME_FAILURE_PROHIBITION_SPEC.md` for TARP protocol

---

## IX. Enforcement and Compliance

### Constitutional Status
Forward-scan obligation is **MANDATORY** per:
- T0-001: BUILD_PHILOSOPHY.md (Learning and continuous improvement)
- T0-013: FM_EXECUTION_MANDATE.md (FM governance enforcement authority)
- Governance PR #877: BL Forward-Scan Obligation Canon

### Enforcement Mechanism
- FM Agent Contract requires forward-scan after any BL/FL/CI
- Builder Agent Contracts acknowledge forward-scan may pause work
- CS2 oversight includes forward-scan completion verification

### Non-Compliance
Failure to execute forward-scan is a **constitutional violation** and will result in:
- BL/FL/CI entry documenting the omission
- Potential for second-time failure (CATASTROPHIC)
- Emergency corrective action
- Governance escalation to CS2

---

## X. References

### Upstream Governance
- **Governance PR #877:** Canonization of BL-018/BL-019 learnings
- **LEARNING_INTAKE_AND_PROMOTION_MODEL.md §6.3:** BL Forward-Scan Obligation
- **BUILD_PHILOSOPHY.md v1.3:** Learning and continuous improvement

### FM Repository Documents
- **QA_CATALOG_ALIGNMENT_GATE_SPEC.md:** Gate created from BL-018/BL-019 forward-scan
- **SECOND_TIME_FAILURE_PROHIBITION_SPEC.md:** TARP protocol for second-time failures
- **BOOTSTRAP_EXECUTION_LEARNINGS.md:** BL registry (canonical source)
- **FLCI_REGISTRY_UPDATE_BL_*.md:** FL/CI entries

### Related Learnings
- **BL-018:** Wave 2.2 QA Catalog Misalignment (triggered forward-scan requirement)
- **BL-019:** Wave 2.3+ QA Catalog Semantic Misalignment (result of insufficient forward-scan)

### Forward-Scan Evidence Examples
- **WAVE_2_FORWARD_SCAN_QA_ALIGNMENT_VERIFICATION.md:** BL-018/BL-019 forward-scan evidence
- **WAVE_2_BL_019_CORRECTIONS_COMPLETION_EVIDENCE.md:** BL-019 correction evidence

---

## XI. Automation and Tooling

### Current State (Manual)
Forward-scan execution is currently MANUAL:
- FM manually identifies pattern
- FM manually scans all in-scope items
- FM manually executes corrections
- FM manually persists evidence

### Future State (Automated)
Potential automation:
1. **Pattern Detection Tools:** AI-powered pattern identification from BL/FL/CI descriptions
2. **Scope Identification Tools:** Automated identification of affected work items
3. **Scan Execution Tools:** Automated pattern scanning across repository
4. **Evidence Generation Tools:** Automated forward-scan report generation

Automation MUST NOT:
- Replace FM judgment on pattern definition
- Skip items in scope
- Auto-correct without verification
- Auto-clear findings without FM approval

---

## XII. Version History

**v1.0.0 (2026-01-05):**
- Initial creation
- Layered down from governance PR #877
- Addresses BL-018 and BL-019 learnings
- Mandatory forward-scan protocol for all BL/FL/CI

---

**Document Owner:** Maturion Foreman (FM)  
**Maintenance:** Governance updates from canonical source  
**Status:** ACTIVE — All BL/FL/CI entries MUST trigger forward-scan
