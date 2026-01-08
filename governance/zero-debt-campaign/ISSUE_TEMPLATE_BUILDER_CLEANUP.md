# ZWZDI Builder Cleanup Issue Template

**Use this template to create cleanup issues for each wave**

---

## Issue Title

```
ZWZDI: [WAVE_ID] Cleanup - [BUILDER_NAME]
```

**Example**: `ZWZDI: Wave 1.0 Cleanup - UI Builder`

---

## Issue Body

```markdown
## ZWZDI Wave Cleanup Assignment

**Campaign**: Zero Warning, Zero Debt Initiative (ZWZDI-2026-001)  
**Wave**: [WAVE_ID]  
**Builder**: @[BUILDER_GITHUB_USERNAME]  
**Priority**: CRITICAL  
**Type**: Technical Debt Elimination

---

### Assignment Summary

You are assigned to eliminate ALL warnings and test debt from **[WAVE_ID]** scope.

**Why you**: You implemented [WAVE_ID], making you accountable for its quality.

**Authority**: This assignment has CS2 (Johan Ras) authority. Participation is mandatory.

---

### Scope

**Test Directories**:
- `tests/[TEST_DIR_1]/`
- `tests/[TEST_DIR_2]/`
- [additional directories]

**Test Files**:
- `tests/[TEST_FILE_1].py`
- `tests/[TEST_FILE_2].py`
- [additional files]

---

### Current State (Baseline)

**Warnings**: [X] warnings in scope  
**Failing Tests**: [Y] RED tests in scope  
**Passing Tests**: [Z] GREEN tests  
**Test Pass Rate**: [Z/(Y+Z) * 100]%

#### Warning Breakdown:
- [Category 1]: [count] warnings
- [Category 2]: [count] warnings
- [Category 3]: [count] warnings
- [Additional categories...]

#### Test Failure Breakdown:
- [Failure Type 1]: [count] tests
- [Failure Type 2]: [count] tests
- [Additional types...]

**Baseline Evidence**: See [link to test output or evidence file]

---

### Target State

**Warnings**: 0 (ZERO)  
**Failing Tests**: 0 (ZERO - excluding documented QA-to-Red)  
**Passing Tests**: [Z + Y fixed] GREEN tests  
**Test Pass Rate**: 100%

**Success Criteria**: See section below

---

### Prerequisites (MANDATORY)

Before starting cleanup, you MUST:

1. **Read**: `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md`
   - [ ] I have read and understood the Governance Learning Brief

2. **Review**: `governance/zero-debt-campaign/waves/[wave_id]_cleanup_plan.md`
   - [ ] I have reviewed my wave-specific cleanup plan

3. **Acknowledge**: I understand this is my accountability as the original builder
   - [ ] I acknowledge accountability for this cleanup

---

### Execution Instructions

#### Step 1: Setup
1. Pull latest code from main branch
2. Install all dependencies
3. Run test suite locally to reproduce baseline
4. Verify you see [X] warnings and [Y] failures

#### Step 2: Eliminate Warnings
1. Run tests with warnings enabled: `pytest [scope] -W default`
2. For EACH warning:
   - Read the warning carefully
   - Identify root cause
   - Fix the root cause (DO NOT suppress)
   - Verify warning eliminated
   - Document fix if non-obvious
3. Continue until ZERO warnings

#### Step 3: Resolve Test Debt
1. For EACH failing test:
   - Investigate why it fails
   - If missing implementation: IMPLEMENT
   - If broken test: FIX
   - If obsolete test: REMOVE with traceability doc
   - Verify test now GREEN
2. Continue until ZERO failures

#### Step 4: Verification
1. Run full test suite in your scope
2. Verify: 0 warnings
3. Verify: 0 failures (excluding QA-to-Red)
4. Verify: 100% GREEN
5. Document any removed tests with rationale

#### Step 5: Evidence Collection
1. Run test suite and capture output
2. Save output to: `evidence/zwzdi/[wave_id]/test_output.txt`
3. Create completion summary
4. List all fixes made
5. Document any removed tests

---

### Success Criteria

Your cleanup is COMPLETE when ALL of the following are met:

- ✅ **Zero warnings** in scope test files
- ✅ **Zero failing tests** (excluding documented QA-to-Red)
- ✅ **100% test pass rate** in scope
- ✅ **All fixes documented** (what was changed and why)
- ✅ **Completion evidence provided** (test output, summary)
- ✅ **FM verification PASS**

**99% is NOT sufficient. 100% or FAIL.**

---

### Completion Evidence Requirements

Create the following files in `evidence/zwzdi/[wave_id]/`:

1. **COMPLETION_SUMMARY.md**
   - Summary of work done
   - List of warnings eliminated
   - List of tests fixed
   - List of tests removed (if any) with rationale
   - Time spent
   - Lessons learned

2. **test_output.txt**
   - Full pytest output showing 0 warnings, 0 failures

3. **fixes_detailed.md** (if needed)
   - Detailed explanation of non-obvious fixes
   - Root causes identified
   - Solutions implemented

---

### Prohibited Actions

You MUST NOT:

❌ Suppress warnings (use `warnings.filterwarnings("ignore")`)  
❌ Skip tests (use `@pytest.mark.skip`)  
❌ Comment out failing tests  
❌ Use `pass` as test implementation  
❌ Defer fixes to "later"  
❌ Delegate cleanup to others  
❌ Say "someone else will fix it"  

**If you're uncertain, STOP and ESCALATE to FM.**

---

### Timeline

**Estimated Effort**: [X] days  
**Start Date**: [YYYY-MM-DD]  
**Target Completion**: [YYYY-MM-DD]  
**Actual Completion**: TBD

**Note**: If you need more time, provide updated estimate immediately. Do NOT rush to meet deadline at expense of quality.

---

### Support and Escalation

**Questions**: Comment on this issue or escalate to @ForemanApp  
**Blockers**: Escalate immediately to FM  
**Systemic Issues**: Escalate immediately to FM  

**Do NOT proceed if blocked. Wait for FM guidance.**

---

### Wave Dependencies

**This wave depends on**: [Previous wave or "None" if first]  
**Status**: [BLOCKED/READY]

**Can start when**: [Previous wave] cleanup is FM-verified PASS

---

### Verification Process

When you believe cleanup is complete:

1. **Comment** on this issue: "Ready for verification"
2. **Provide links** to all completion evidence
3. **FM will verify**:
   - Run tests in scope
   - Check for warnings
   - Check for failures
   - Review evidence
   - Verify completeness
4. **FM verdict**:
   - **PASS**: Wave complete, next wave authorized
   - **FAIL**: Issues identified, continue cleanup

**If FAIL**: Do NOT argue. Fix issues and resubmit.

---

### Campaign Context

**Full Campaign Details**: `governance/zero-debt-campaign/CAMPAIGN_OVERVIEW.md`  
**Execution Sequence**: `governance/zero-debt-campaign/EXECUTION_SEQUENCE.md`  
**Governance Brief**: `governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md`  
**Wave Cleanup Plan**: `governance/zero-debt-campaign/waves/[wave_id]_cleanup_plan.md`

---

### Checklist

Before marking this issue complete, verify:

- [ ] Read GOVERNANCE_LEARNING_BRIEF.md
- [ ] Reviewed wave cleanup plan
- [ ] Acknowledged accountability
- [ ] Reproduced baseline locally
- [ ] Eliminated ALL warnings
- [ ] Resolved ALL test debt
- [ ] 100% test pass rate achieved
- [ ] Completion evidence created
- [ ] Evidence files uploaded
- [ ] FM verification requested
- [ ] FM verification PASSED

---

**Status**: [BLOCKED/READY/IN_PROGRESS/VERIFICATION/COMPLETE]  
**Assigned**: @[BUILDER_GITHUB_USERNAME]  
**Priority**: CRITICAL  
**Authority**: CS2 (Johan Ras)
```

---

## Issue Labels

Apply the following labels:

- `zwzdi-campaign`
- `technical-debt`
- `[wave-id]` (e.g., `wave-1.0`)
- `[builder-role]` (e.g., `ui-builder`)
- `critical`

---

## Usage Instructions for FM

1. **Copy template** for each wave
2. **Fill in placeholders**:
   - `[WAVE_ID]`
   - `[BUILDER_NAME]`
   - `[BUILDER_GITHUB_USERNAME]`
   - `[X]` warnings count
   - `[Y]` failures count
   - `[Z]` passing tests count
   - `[TEST_DIR_X]` directories
   - `[TEST_FILE_X]` files
   - Timeline dates
3. **Add warning/failure breakdowns** from inventory
4. **Create issue** in GitHub
5. **Assign builder**
6. **Link** to wave cleanup plan

---

**Template Version**: 1.0  
**Last Updated**: 2026-01-08  
**Owner**: Foreman (FM)
