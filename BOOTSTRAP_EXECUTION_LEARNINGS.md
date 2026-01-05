# Bootstrap Execution Learnings (BL Registry)
## Maturion Foreman — Continuous Improvement Registry

**Purpose**: This registry captures critical learnings from bootstrap execution failures and system design gaps. Each learning becomes a permanent governance constraint to prevent recurrence.

**Authority**: Build Philosophy — Failure → Learning → Continuous Improvement

**Status**: ACTIVE — Continuously Updated

---

## BL-016: Builder Recruitment MUST Be Automated and GitHub-Native

**Date Registered**: 2026-01-01  
**Classification**: CATASTROPHIC  
**Issue Reference**: Builder Recruitment Mechanism Broken  
**Root Cause Analysis**: `ROOT_CAUSE_ANALYSIS_BUILDER_RECRUITMENT_AUTOMATION_FAILURE.md`

### Learning Statement

Builder recruitment MUST be automated, machine-readable, and enforced via `.github`-scoped configuration. Documentation alone is insufficient and constitutes a system failure.

### Rationale

Phase 4.5 and Wave 0.1 treated builder recruitment as a documentation exercise, creating markdown files in the repository root and `foreman/` directory. While content quality was high, this approach failed to establish the automated, GitHub-native recruitment mechanism required for governed build execution.

**Impact**: Phase 5.0 execution became impossible due to lack of automated builder selection, assignment, and gate binding.

**Root Cause**: Misclassification of builder recruitment as documentation instead of system configuration.

### Mandatory Requirements (Permanent)

All future builder recruitment MUST include:

1. **GitHub-Native Location**: Builder contracts MUST exist in `.github/agents/<builder-name>.md`
2. **Machine-Readable Format**: Contracts MUST use structured, parseable format (YAML frontmatter + markdown)
3. **Schema Conformance**: Contracts MUST conform to defined builder contract schema
4. **Automated Validation**: Platform readiness MUST validate builder contract presence and validity
5. **Programmatic Integration**: Builder selection and gate binding MUST be automatable via contracts

### Prohibited Actions (Permanent)

1. ❌ Builder "recruitment" using only root-level documentation files
2. ❌ Builder recruitment without `.github/agents/` contracts
3. ❌ Declaring "recruitment complete" without automated validation
4. ❌ Platform readiness approval without builder contract verification
5. ❌ Treating documentation as sufficient for system configuration

### Enforcement Mechanism

**Validation Gate**: Platform Readiness validation MUST include:
```
- [ ] All required builders have contracts in `.github/agents/<builder>.md`
- [ ] All builder contracts conform to schema
- [ ] Automated recruitment mechanism is testable
- [ ] Builder selection can be performed programmatically
```

**Ratchet Condition**: This learning establishes a permanent constraint. Any future builder recruitment without `.github/agents/` automation requires explicit CS2 override and must document why the standard is being violated.

### Application Examples

**✅ CORRECT Builder Recruitment**:
```
1. Create `.github/agents/ui-builder.md` with YAML frontmatter:
   ---
   builder_id: ui-builder
   builder_type: specialized
   capabilities: [ui, frontend, components, styling]
   responsibilities: [UI components, layouts, wizards]
   forbidden: [backend logic, cross-module logic]
   ---
   
2. Validate contract against schema
3. Test automated builder selection mechanism
4. Update platform readiness with builder contract validation
```

**❌ INCORRECT Builder Recruitment**:
```
1. Create `builderui-builder.md` in root (wrong location)
2. Write comprehensive documentation (not machine-readable)
3. Declare "recruited and validated" (no automation proof)
4. Proceed to next wave (blocked due to no automation)
```

### Related Learnings

- BL-001 through BL-015: (To be backfilled if historical learnings exist)
- Future learnings will reference this as precedent for automation requirements

### Governance Impact

This learning triggers updates to:
1. `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` — Add explicit builder contract validation
2. `foreman/BUILDER_INITIALIZATION.md` — Mandate `.github/agents/` location
3. Platform readiness checklist — Add builder contract verification
4. Builder recruitment specifications — Require automation design

### Status

**Learning Registered**: ✅ COMPLETE  
**Ratchet Activated**: ✅ ACTIVE  
**Corrective Action**: ⏳ IN PROGRESS (This Issue)  
**Governance Updates**: ⏳ PENDING (Post-fix)

---

## BL-017: Build-to-Green MUST Be Complete — Time Constraints Are Never Valid Justification for Partial Delivery

**Date Registered**: 2026-01-02  
**Classification**: CATASTROPHIC  
**Issue Reference**: Wave 1.0.7 qa-builder Build-to-Green Partial Delivery  
**Root Cause Analysis**: Inline (Wave 1.0.7 submitted with 9/79 tests passing)

### Learning Statement

Builders MUST deliver 100% complete Build-to-Green implementations. Time constraints, complexity, or scope are NEVER valid justifications for partial delivery. Quality delivery supersedes timely delivery in all cases.

### Rationale

Wave 1.0.7 (qa-builder Build-to-Green) was assigned to implement 79 QA components (QA-132 to QA-210) to make RED tests GREEN. The builder submitted work with only 9 of 79 tests passing (11% completion) and justified the partial delivery by citing:
- "Multi-hour implementation task"
- "Needs additional time to complete all 79 test implementations"
- "This is a large-scale implementation task"

**This represents a catastrophic failure** of Build Philosophy and constitutes a fundamental misunderstanding of delegated build operations.

**Impact**: 
- Gate failure (70 of 79 tests remain RED)
- Zero test debt policy violated (incomplete implementation)
- One-Time Build Correctness principle violated
- Build-to-Green workflow disrupted
- Additional rework cycles required

**Root Cause**: Builder treated time as a superior constraint to completion quality, fundamentally violating the principle that builds are delegated operations that must be executed completely regardless of duration.

### Core Principle (Permanent)

**Quality Delivery > Timely Delivery**

Builds may take:
- 5 times longer than estimated ✅
- Multiple sessions with breaks ✅  
- Days if necessary ✅

But builds MUST NEVER be:
- Partially delivered ❌
- Submitted incomplete ❌
- Justified by time constraints ❌

### Mandatory Requirements (Permanent)

All future Build-to-Green tasks MUST:

1. **100% Completion**: All assigned tests MUST be GREEN before submission
2. **No Partial Delivery**: Builder MUST NOT submit until ALL requirements satisfied
3. **Break Policy**: Builder MUST take breaks/reassess as needed rather than submit partial work
4. **Time Independence**: Builder MUST continue until complete, regardless of duration
5. **Gate Validation**: Builder MUST validate ALL gate requirements before submission
6. **Self-Check**: Builder MUST run full test suite and confirm 100% pass rate

### Prohibited Actions (Permanent)

1. ❌ Submitting Build-to-Green work with ANY failing tests
2. ❌ Justifying incomplete work with "time constraints" or "scope is large"
3. ❌ Treating estimated duration as a hard deadline
4. ❌ Submitting "foundation" or "partial progress" as complete work
5. ❌ Using complexity or scale as rationale for partial delivery
6. ❌ Requesting additional time AFTER submission instead of BEFORE completion

### Enforcement Mechanism

**Pre-Submission Checklist** (Builder MUST self-validate):
```
- [ ] ALL assigned tests executed
- [ ] 100% test pass rate achieved
- [ ] Zero test debt (no skips, no TODOs)
- [ ] Full test suite run and validated
- [ ] Gate requirements ALL satisfied
- [ ] Architecture alignment verified
- [ ] Evidence artifacts complete
```

**Gate Validation**: Any Build-to-Green submission with failing tests is an AUTOMATIC GATE FAILURE requiring complete rework.

**Ratchet Condition**: This learning establishes that partial Build-to-Green delivery is a catastrophic failure, not a progress update.

### Builder Instructions (Permanent)

When assigned Build-to-Green tasks, builders MUST:

1. **Plan for Completion**: Assess full scope before beginning implementation
2. **Work to Completion**: Continue implementation until ALL tests GREEN
3. **Take Breaks**: If exhausted, take breaks and reassess, but do not submit partial work
4. **Request Clarification**: If requirements unclear, request clarification BEFORE implementation
5. **Validate Before Submit**: Run full test suite and confirm 100% pass BEFORE submitting
6. **Never Use Time as Excuse**: Time is NOT a valid reason for incomplete builds

### Application Examples

**✅ CORRECT Approach**:
```
Builder assigned: Make 79 tests GREEN
Builder implements: 30 tests GREEN (Day 1)
Builder status: Continues working (no submission)
Builder implements: 60 tests GREEN (Day 2)  
Builder status: Continues working (no submission)
Builder implements: 79 tests GREEN (Day 3)
Builder validates: All tests pass, zero debt
Builder submits: Complete implementation
Result: GATE PASS ✅
```

**❌ INCORRECT Approach (Wave 1.0.7 Actual)**:
```
Builder assigned: Make 79 tests GREEN
Builder implements: 9 tests GREEN
Builder justifies: "Multi-hour task, needs additional time"
Builder submits: Partial work (11% complete)
Result: CATASTROPHIC FAILURE ❌
```

### Issue-Specific Application

**For Wave 1.0.7 Builder**:

This is a catastrophic failure. Builds are delegated operations and time should NEVER be a constraint superior to completion. Timeous delivery is important, but quality delivery is paramount.

**Instructions**:
1. **Continue Work**: Complete implementation of ALL 79 QA components
2. **No Time Pressure**: Take as long as needed (5x estimate is acceptable)
3. **Take Breaks**: Rest and reassess if needed, but do not submit until complete
4. **100% Validation**: Ensure ALL 79 tests GREEN before next submission
5. **Zero Compromise**: Do not skip, TODO, or leave any test incomplete

Builds can take 5 times longer as long as they are submitted correct and QA passes 100%.

### Related Learnings

- BL-016: Builder Recruitment Automation (automation requirements)
- BL-015: (If it exists) Build Philosophy adherence
- Future learnings will reference this as precedent for completion requirements

### Governance Impact

This learning triggers:
1. **Builder Contract Updates**: Add explicit "100% completion" requirement
2. **Issue Templates**: Add pre-submission validation checklist
3. **Gate Definitions**: Clarify that partial delivery = automatic failure
4. **Build Philosophy**: Reinforce quality > speed principle

### Status

**Learning Registered**: ✅ COMPLETE  
**Ratchet Activated**: ✅ ACTIVE  
**Corrective Action**: ⏳ REQUIRED (Builder must complete Wave 1.0.7)  
**Governance Updates**: ⏳ PENDING

---

## Bootstrap Learning Template (For Future Use)

```markdown
## BL-XXX: [Learning Title]

**Date Registered**: YYYY-MM-DD  
**Classification**: [CRITICAL | MAJOR | MODERATE | MINOR]  
**Issue Reference**: [Issue title or reference]  
**Root Cause Analysis**: [RCA document reference]

### Learning Statement

[Single sentence summary of the learning]

### Rationale

[What happened, why it matters, what the impact was]

### Mandatory Requirements (Permanent)

[What MUST be done in future to prevent recurrence]

### Prohibited Actions (Permanent)

[What MUST NOT be done in future]

### Enforcement Mechanism

[How this learning will be enforced]

### Application Examples

**✅ CORRECT**: [Example of correct approach]
**❌ INCORRECT**: [Example of incorrect approach]

### Status

**Learning Registered**: [Status]  
**Ratchet Activated**: [Status]  
**Corrective Action**: [Status]
```

---

## BL-018: Wave Planning MUST Verify QA Catalog Before Subwave Assignment

**Date Registered**: 2026-01-05  
**Classification**: CATASTROPHIC  
**Issue Reference**: Wave 2.2 Block — Parking Station Subwave (Issue #399)  
**Root Cause Analysis**: `ROOT_CAUSE_ANALYSIS_WAVE_2_2_BLOCK.md`

### Learning Statement

Wave planning and subwave assignment MUST verify that all assigned QA ranges exist in the canonical QA Catalog and match the intended feature scope. QA ranges cannot be assumed or assigned sequentially without validation.

### Rationale

Wave 2.2 (Parking Station Advanced) was planned and documented with QA-376 to QA-385 as the assigned QA range for parking station features (prioritization and bulk operations). However, these QA IDs are actually defined in `QA_CATALOG.md` as:
- **QA-376 to QA-380**: Network Failure Modes (network partition, WebSocket loss, API timeout, GitHub API failure, notification failure)
- **QA-381 to QA-385**: Resource Failure Modes (memory exhaustion, CPU overload, disk space, file handle exhaustion, thread pool exhaustion)

**Impact:**
- Wave 2.2 subwave specification was structurally invalid and could not be executed
- Builder (ui-builder) would have been assigned to implement failure mode tests instead of UI features
- Issue #398 was created with non-existent QA components as scope
- Wave 2 execution was blocked at subwave 2.2

**Root Cause:** Wave 2 planning occurred without verifying QA component existence in the canonical QA Catalog, violating the One-Time Build principle of "Architecture → QA Catalog → QA-to-Red → Planning → Execution."

**Governance Failure:** The planning process assumed QA components existed or would be created, but no validation step ensured QA Catalog alignment before sub-issue creation.

### Mandatory Requirements (Permanent)

All future wave planning and subwave assignment MUST include:

1. **QA Catalog Verification**: Before assigning QA ranges to subwaves, verify all QA IDs exist in `QA_CATALOG.md`
2. **QA Definition Alignment**: Verify QA component definitions match the intended feature scope of the subwave
3. **QA ID Collision Check**: Verify assigned QA ranges are not already allocated to other features
4. **Architecture Completeness**: Verify architecture sections exist for all subwave features before QA assignment
5. **QA Catalog Extension (If Needed)**: If new features require QA components, extend `QA_CATALOG.md` BEFORE wave planning
6. **Sequential Governance**: Architecture → QA Catalog → QA-to-Red → Wave Planning (in that order, no skipping)

### Prohibited Actions (Permanent)

1. ❌ Assigning QA ranges to subwaves without verifying QA_CATALOG.md
2. ❌ Assuming QA components exist based on sequential numbering
3. ❌ Planning waves before architecture is extended with new features
4. ❌ Creating sub-issue specifications without QA Catalog validation
5. ❌ Skipping QA-to-Red precondition verification before builder assignment
6. ❌ Allowing builders to proceed with structurally invalid QA assignments

### Enforcement Mechanism

**Wave Planning Validation Gate** (Mandatory):
```
Before creating subwave sub-issue files:
- [ ] All assigned QA ranges verified in QA_CATALOG.md
- [ ] All QA definitions match subwave intent
- [ ] No QA ID collisions with existing allocations
- [ ] Architecture sections exist and are frozen for all subwave features
- [ ] QA-to-Red tests exist (or planned) for all assigned QA ranges
```

**QA Catalog Extension Process** (If New Features):
```
1. Extend TRUE_NORTH_FM_ARCHITECTURE.md with new feature definitions
2. Extend QA_CATALOG.md with new QA components and assign IDs
3. Implement QA-to-Red tests for new QA components
4. Verify QA-to-Red precondition satisfied (all tests RED)
5. THEN proceed with wave planning and subwave assignment
```

**Ratchet Condition**: This learning establishes that wave planning without QA Catalog verification is a catastrophic structural failure requiring complete rework.

### Application Examples

**✅ CORRECT Wave Planning**:
```
1. Review TRUE_NORTH_FM_ARCHITECTURE.md for Wave N features
2. Check QA_CATALOG.md: Do QA components exist for all features?
   - If YES: Proceed with step 3
   - If NO: Extend QA_CATALOG.md first, then create QA-to-Red tests
3. Assign QA ranges to subwaves based on verified QA_CATALOG.md entries
4. Validate: All QA IDs exist and match intended feature scope
5. Create sub-issue specifications with verified QA ranges
6. Issue to builders with QA-to-Red precondition satisfied

Example: Subwave X.Y requires "Feature Z" (10 QA)
- Verify QA_CATALOG.md contains QA-XXX to QA-YYY for "Feature Z"
- Verify QA definitions describe "Feature Z" capabilities
- Assign QA-XXX to QA-YYY to Subwave X.Y
- Create sub-issue with verified QA range
```

**❌ INCORRECT Wave Planning (Wave 2.2 Actual)**:
```
1. Identify desired feature: "Parking Station Advanced"
2. Assume QA-376 to QA-385 are available (sequential numbering)
3. Assign QA-376 to QA-385 to "Parking Station Advanced"
4. Create sub-issue specification describing parking features
5. Issue to builder with structurally invalid scope
6. Builder discovers QA-376 to QA-385 are failure modes, not parking features
7. Builder declares BLOCKED, wave execution halts

Result: CATASTROPHIC FAILURE — Wave planning without QA Catalog verification ❌
```

### Issue-Specific Application

**For Wave 2.2 (Parking Station Advanced):**

This subwave was created with an invalid QA range. FM must decide:

**Option A**: "Parking Station Advanced" is Wave 2 scope
- Extend TRUE_NORTH_FM_ARCHITECTURE.md with parking advanced definition
- Extend QA_CATALOG.md with QA-401 to QA-410 (new IDs, avoiding collision)
- Implement QA-to-Red tests for parking prioritization and bulk operations
- Regenerate SUBWAVE_2.2_UI_BUILDER_PARKING_STATION_ADVANCED.md with correct QA range
- Update issue #398 with corrected scope
- Authorize builder to proceed

**Option B**: "Parking Station Advanced" is NOT Wave 2 scope
- Remove Subwave 2.2 from Wave 2 Rollout Plan
- Close issue #398 as "Structurally Invalid / Scope Change"
- Update Wave 2 sequencing (Subwave 2.3 depends on 2.1, not 2.2)
- Proceed with remaining Wave 2 subwaves

**Option C**: Defer to Wave 3+
- Remove Subwave 2.2 from Wave 2 Rollout Plan
- Close issue #398 as "Deferred to Wave 3+"
- Create backlog entry for future implementation
- Proceed with remaining Wave 2 subwaves

### Verification Actions

**Immediate (Wave 2):**
1. Audit ALL remaining Wave 2 subwaves (2.3 to 2.14)
2. Verify QA ranges exist in QA_CATALOG.md and match subwave intent
3. Correct any additional misalignments before authorization
4. Update WAVE_2_ROLLOUT_PLAN.md with verified QA ranges

**Long-Term (All Future Waves):**
1. Add mandatory QA Catalog verification to wave planning process
2. Update Platform Readiness Checklist with QA Catalog extension verification
3. Enforce Architecture → QA → Planning sequence constitutionally
4. Automated validation: Check QA ranges against QA_CATALOG.md before sub-issue creation

### Related Learnings

- BL-016: Builder Recruitment Automation (governance automation requirements)
- BL-017: Build-to-Green Completeness (quality over speed)
- Future learnings will reference this as precedent for wave planning discipline

### Governance Impact

This learning triggers updates to:
1. **Wave Planning Process** — Add mandatory QA Catalog verification gate
2. **Platform Readiness Checklist** — Add QA Catalog extension verification for new waves
3. **Subwave Creation Protocol** — Enforce QA validation before sub-issue file generation
4. **FM Agent Contract** — Add QA Catalog verification to mandatory sequencing (Section XIV)
5. **QA_CATALOG.md** — Document QA extension process for future waves

### Status

**Learning Registered**: ✅ COMPLETE  
**Ratchet Activated**: ✅ ACTIVE  
**Corrective Action**: ⏳ IN PROGRESS (Issue #399)  
**Governance Updates**: ⏳ PENDING (Post-fix)

---

## Registry Metadata

**Total Learnings Registered**: 3  
**Catastrophic**: 3 (BL-016, BL-017, BL-018)  
**Critical**: 0  
**Major**: 0  
**Moderate**: 0  
**Minor**: 0

**Next Learning ID**: BL-021

---

## BL-019: QA Catalog Semantic Alignment MUST Be Verified Before Subwave Authorization (EMERGENCY - SECOND CATASTROPHIC FAILURE)

**Date Registered**: 2026-01-05  
**Classification**: CATASTROPHIC  
**Issue Reference**: Wave 2.2 Block (Issue #399), Subwave 2.3 Block  
**Root Cause Analysis**: `ROOT_CAUSE_ANALYSIS_WAVE_2_2_BLOCK.md`, Emergency Corrective Action Plan BL-019

### Learning Statement

QA Catalog alignment verification is MANDATORY before subwave authorization. FM MUST verify not only that QA IDs exist, but that QA **semantic content** matches the subwave's intended scope. Failure to do so causes catastrophic builder blocks and execution halts.

### Rationale

BL-018 established that FM must verify QA ranges exist in QA_CATALOG.md. However, BL-018 did NOT require semantic verification (checking that QA definitions match subwave intent).

**Wave 2.2 and 2.3 Failures:**
- Subwave 2.2 ("Parking Station Advanced") was assigned QA-376 to QA-385
- QA Catalog showed QA-376 to QA-385 exist ✓
- BUT QA-376 to QA-385 describe "failure modes", not "parking station features" ✗
- Builder correctly declared BLOCKED — impossible requirement

**Similar failure in Subwave 2.3:**
- Subwave 2.3 ("System Optimizations Phase 1") assigned QA-426 to QA-435
- QA Catalog semantic mismatch discovered during verification
- Second catastrophic failure of same class

**Root Cause:** BL-018 was necessary but insufficient. FM verified QA IDs exist but did not verify semantic alignment between QA definitions and subwave scope.

### Mandatory Requirements (Permanent)

Before authorizing ANY subwave, FM MUST verify:

1. **QA Range Exists** (BL-018): QA IDs exist in QA_CATALOG.md
2. **Semantic Alignment** (BL-019): QA definitions semantically match subwave scope
3. **No Semantic Conflicts**: QA range describes the features the subwave claims to implement
4. **Architecture Traceability**: QA components trace to architecture elements that subwave will implement

### Prohibited Actions (Permanent)

1. ❌ Authorizing subwaves based only on QA ID existence (BL-018 alone is insufficient)
2. ❌ Assuming sequential QA numbering implies semantic grouping
3. ❌ Assuming subwave names match QA content without verification
4. ❌ Proceeding with authorization when semantic mismatch is detected

### Enforcement Mechanism

**Enhanced Pre-Authorization Gate (extends BL-018):**
```
For Subwave X.Y with QA range QA-AAA to QA-BBB:

1. Verify QA-AAA to QA-BBB exist in QA_CATALOG.md (BL-018)
2. Read QA-AAA to QA-BBB definitions from QA_CATALOG.md
3. Verify QA definitions semantically describe subwave X.Y scope
4. If mismatch detected:
   - HALT authorization
   - Document mismatch
   - ESCALATE to CS2 for architecture decision
5. If aligned:
   - Document verification evidence
   - Proceed to authorization
```

### Application Examples

**✅ CORRECT Semantic Verification (Subwave 2.1)**:
```
Subwave: "Enhanced Dashboard"
QA Range: QA-401 to QA-415
QA Definitions (from catalog):
  - QA-401: Drill-down navigation
  - QA-402: Advanced filtering
  - QA-403 to QA-415: Dashboard real-time updates

Semantic Check: ✅ PASS
- "Enhanced Dashboard" semantically matches drill-down, filtering, real-time updates
- Architecture element (Dashboard subsystem) exists
- Proceed to authorization
```

**❌ INCORRECT Semantic Verification (Subwave 2.2)**:
```
Subwave: "Parking Station Advanced"
QA Range: QA-376 to QA-385
QA Definitions (from catalog):
  - QA-376: Database write failure handling
  - QA-377: State conflict resolution
  - QA-378 to QA-385: Various failure mode handling

Semantic Check: ❌ FAIL
- "Parking Station Advanced" does NOT match failure mode handling
- QA-376 to QA-385 are cross-cutting failure modes, not parking features
- HALT authorization
- ESCALATE: Architecture decision required
```

### Issue-Specific Application

**For Wave 2.2, 2.3 (and any future misalignments):**

1. **Forward Scan**: Review ALL remaining Wave 2 subwaves (2.3 to 2.14)
2. **Semantic Verification**: Check each QA range against subwave intent
3. **Correct Misalignments**:
   - Option A: Reassign correct QA ranges from catalog
   - Option B: Extend QA_CATALOG.md with new QA IDs for subwave scope
   - Option C: Remove subwave from wave (out of scope)
4. **Update Documentation**: Correct WAVE_2_ROLLOUT_PLAN.md, sub-issue specs
5. **Re-authorize**: Only after semantic alignment is verified

### Related Learnings

- BL-016: Builder Recruitment Automation
- BL-017: Build-to-Green Completeness
- BL-018: QA Catalog Range Verification (PREREQUISITE — BL-019 extends BL-018)

### Governance Impact

This learning triggers updates to:
1. **FM Agent Contract Section XIV** — Add semantic verification to mandatory sequencing
2. **Wave Planning Process** — Add QA semantic alignment verification gate
3. **Pre-Authorization Checklist** — Add semantic verification step
4. **Subwave Creation Protocol** — Require QA definition review before sub-issue creation
5. **Emergency Corrective Action Plan** — Execute forward scan for Wave 2 immediately

### Status

**Learning Registered**: ✅ COMPLETE  
**Classification Escalation**: CATASTROPHIC (second occurrence of structural planning failure)  
**Ratchet Activated**: ✅ ACTIVE  
**Emergency Corrective Action**: ✅ INITIATED (WAVE_2_EMERGENCY_CORRECTIVE_ACTION_PLAN_BL_019.md)  
**Forward Scan**: ✅ REQUIRED (All Wave 2 subwaves 2.3 to 2.14)  
**Governance Updates**: ⏳ PENDING (Post-emergency-fix)

---

## BL-020: FM MUST Verify QA-to-Red Test Existence Before Subwave Authorization (THIRD-TIME PATTERN — QA-to-Red Layer Failure)

**Date Registered**: 2026-01-05  
**Classification**: CATASTROPHIC  
**Issue Reference**: Subwave 2.5 Block (Issue #417, PR #418)  
**Root Cause Analysis**: FM Third-Time Failure (QA-211 to QA-225 Missing Tests)

### Learning Statement

QA-to-Red test **existence and location** verification is MANDATORY before subwave authorization. FM MUST verify not only that QA IDs exist and semantics align (BL-018, BL-019), but that the actual **RED test files** exist at the claimed location in the repository. Failure to do so causes catastrophic builder blocks.

### Rationale

**This is the THIRD occurrence of the same structural failure class:**

1. **BL-018**: FM authorized subwaves without verifying QA IDs exist in QA_CATALOG.md
2. **BL-019**: FM authorized subwaves without verifying QA semantic alignment with subwave scope
3. **BL-020**: FM authorized subwaves without verifying QA-to-Red **tests exist in repository**

**Subwave 2.5 Failure:**
- Subwave 2.5 spec claimed tests exist at: `tests/wave2_0_qa_infrastructure/test_advanced_analytics_phase1_*.py`
- QA-211 to QA-225 exist in QA_CATALOG.md ✓
- Semantic mismatch: Rollout plan said "Advanced Analytics", QA Catalog said "Flow-Based QA" ✗
- **Critical failure: No test files exist for QA-211 to QA-225** ✗
- Builder correctly declared BLOCKED — impossible requirement (no tests to make GREEN)

**Pattern:** FM is verifying documentation (QA_CATALOG.md, specs) but NOT verifying actual **repository artifacts** (test files, code).

### Mandatory Requirements (Permanent)

Before authorizing ANY subwave, FM MUST verify:

1. **QA Range Exists** (BL-018): QA IDs exist in QA_CATALOG.md
2. **Semantic Alignment** (BL-019): QA definitions semantically match subwave scope
3. **QA-to-Red Tests Exist** (BL-020): Actual RED test files exist in repository at claimed location
4. **Test File Location Accuracy**: Sub-issue spec test file paths are accurate and verifiable

### Prohibited Actions (Permanent)

1. ❌ Authorizing subwaves based only on documentation claims (specs, rollout plans)
2. ❌ Assuming tests exist because QA Catalog entries exist
3. ❌ Trusting sub-issue spec file paths without verification
4. ❌ Proceeding when test files are missing or path is incorrect

### Enforcement Mechanism

**Complete Pre-Authorization Gate (extends BL-018, BL-019):**
```
For Subwave X.Y with QA range QA-AAA to QA-BBB:

1. Verify QA-AAA to QA-BBB exist in QA_CATALOG.md (BL-018)
2. Verify QA definitions semantically match subwave scope (BL-019)
3. Verify QA-to-Red test files exist (BL-020):
   a. Check sub-issue spec for claimed test file path
   b. Verify file exists in repository at that path
   c. Verify file contains tests for QA-AAA to QA-BBB
   d. Verify tests are in RED state (NotImplementedError or similar)
4. If tests missing:
   - HALT authorization
   - Create missing QA-to-Red tests OR correct file path
   - Document correction in sub-issue spec
5. If tests exist:
   - Document verification evidence
   - Proceed to authorization
```

### Application Examples

**✅ CORRECT QA-to-Red Verification**:
```
Subwave: "Enhanced Dashboard"
QA Range: QA-401 to QA-415
Sub-issue claims: tests/wave2_0_qa_infrastructure/test_enhanced_dashboard.py

Verification:
1. QA-401 to QA-415 exist in QA_CATALOG.md ✓ (BL-018)
2. Semantics match "Enhanced Dashboard" ✓ (BL-019)
3. File exists: tests/wave2_0_qa_infrastructure/test_enhanced_dashboard.py ✓
4. File contains test_qa_401 through test_qa_415 ✓
5. Tests raise NotImplementedError (RED state) ✓

Result: PASS — Proceed to authorization
```

**❌ INCORRECT QA-to-Red Verification (Subwave 2.5 Actual)**:
```
Subwave: "Advanced Analytics Phase 1"
QA Range: QA-211 to QA-225
Sub-issue claims: tests/wave2_0_qa_infrastructure/test_advanced_analytics_phase1_*.py

Verification:
1. QA-211 to QA-225 exist in QA_CATALOG.md ✓ (BL-018)
2. Semantic check: ❌ FAIL
   - QA Catalog says "Flow-Based QA", not "Analytics"
   - Subwave name mismatch
3. File existence: ❌ FAIL
   - No file matching test_advanced_analytics_phase1_*.py exists
   - No tests exist for QA-211 to QA-225 anywhere in repository

Result: CATASTROPHIC BLOCK — Builder cannot execute Build-to-Green without RED tests
Action: HALT, create missing tests, fix semantic mismatch, re-authorize
```

### Corrective Actions (Immediate)

**For Subwave 2.5:**

1. **Fix Semantic Mismatch**:
   - QA-211 to QA-225 are "Flow-Based QA" (per QA_CATALOG.md)
   - Rename Subwave 2.5 from "Advanced Analytics Phase 1" to "Advanced Flow Scenarios"
   - Update WAVE_2_ROLLOUT_PLAN.md and sub-issue spec

2. **Create Missing QA-to-Red Tests**:
   - Create `tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py`
   - Implement QA-211 to QA-225 as RED tests (NotImplementedError)
   - Verify all 15 tests exist and are RED

3. **Update Sub-Issue Spec**:
   - Correct file path to: `test_advanced_flow_scenarios.py`
   - Correct scope description to: "Advanced Flow Scenarios"
   - Update architecture references to Flow-Based QA specification

4. **Re-Authorize**:
   - Only after tests exist and semantic alignment is correct

**For All Future Subwaves:**

1. **Forward Scan Wave 2** (2.6 to 2.14):
   - Verify QA-to-Red tests exist for all remaining subwaves
   - Correct any missing tests or path errors before authorization

2. **Add Automated Validation**:
   - Consider creating `validate-qa-tests-existence.py` script:
     - Takes subwave spec as input
     - Verifies QA range, semantic alignment, test existence
     - Reports missing tests or misalignments
     - Machine-readable output for FM pre-authorization

3. **Update FM Pre-Authorization Checklist**:
   - Add mandatory step: "Verify QA-to-Red tests exist in repository"
   - Require evidence artifact: Test file verification report

### Related Learnings

- BL-016: Builder Recruitment Automation (system configuration vs documentation)
- BL-017: Build-to-Green Completeness
- BL-018: QA Catalog Range Verification (PREREQUISITE)
- BL-019: QA Semantic Alignment Verification (PREREQUISITE)

**Pattern:** All three (BL-018, BL-019, BL-020) are the **same root failure** at different layers:
- BL-018: FM verified specs but not QA Catalog
- BL-019: FM verified QA Catalog IDs but not semantics
- BL-020: FM verified QA Catalog but not actual test files

**Systemic Root Cause:** FM planning operates on documentation without verifying repository artifacts.

### Governance Impact

This learning triggers updates to:
1. **FM Agent Contract Section XIV** — Add QA-to-Red existence verification to mandatory sequencing
2. **Pre-Authorization Checklist** — Add test file existence verification step
3. **Subwave Creation Protocol** — Require QA-to-Red test creation BEFORE sub-issue generation
4. **Wave Planning Process** — QA-to-Red compilation MUST be complete before any subwave authorization
5. **Validation Tooling** — Create automated QA-to-Red existence checker

### Status

**Learning Registered**: ✅ COMPLETE  
**Classification Escalation**: CATASTROPHIC (third occurrence of structural verification failure)  
**Ratchet Activated**: ✅ ACTIVE  
**Corrective Action**: ⏳ IN PROGRESS (Creating missing tests, fixing semantic mismatch)  
**Forward Scan**: ✅ REQUIRED (All Wave 2 subwaves 2.5 to 2.14)  
**Governance Updates**: ⏳ PENDING (Post-fix)  
**Tooling**: 🔄 RECOMMENDED (Automated QA-to-Red existence validation)

---

## Registry Metadata

**Total Learnings Registered**: 5  
**Catastrophic**: 5 (BL-016, BL-017, BL-018, BL-019, BL-020)  
**Critical**: 0  
**Major**: 0  
**Moderate**: 0  
**Minor**: 0

---

**Maintained by**: Maturion Foreman (FM)  
**Last Updated**: 2026-01-05  
**Registry Status**: ACTIVE
