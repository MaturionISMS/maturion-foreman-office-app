# Build to Green Rule

**Version**: 1.0.0  
**Status**: Constitutional Authority for Builders  
**Authority**: Build Philosophy + Builder Agent Contract  
**Last Updated**: 2025-12-15

---

## I. Principle

**Builders ONLY accept "Build to Green" instructions and ONLY implement code to make failing tests pass.**

This is the ONLY acceptable instruction format.  
This is the ONLY acceptable workflow.  
No exceptions.

---

## II. The ONLY Instruction Format

### Standard Format (MANDATORY)

```
BUILD TO GREEN

Architecture Reference: <path to architecture document>
QA Suite Location: <path to failing test suite>
QA Current Status: RED (X tests failing)
Acceptance Criteria: <specific completion criteria>
```

### What Each Component Means

**"BUILD TO GREEN"** (Exact phrase required)
- Not "Build feature X"
- Not "Implement component Y"
- Not "Fix bug Z"
- Not "Create module A"
- **ONLY**: "BUILD TO GREEN" or "Build to Green"

**Architecture Reference**
- Path to complete, frozen architecture document
- Architecture must exist and be accessible
- Architecture must be validated and complete (no TBD, no TODO)

**QA Suite Location**
- Path to test suite directory or file
- QA suite must exist and be accessible
- QA suite must have been executed

**QA Current Status**
- Must be RED (failing tests)
- Must specify number of failing tests
- If status is GREEN (all passing) → NOTHING TO BUILD

**Acceptance Criteria**
- Typically: "All tests must pass (100% green)"
- Must be unambiguous and measurable
- No subjective criteria

### Example Valid Instruction

```markdown
# Build to Green Instruction

## Task ID
task-user-profile-001

## Instruction
Build to Green

## Architecture Reference
**Location**: `foreman/architecture/user-profile-architecture.md`

**Summary**:
Build the user profile management feature allowing users to view and edit their profile information including name, email, avatar, and preferences.

**Key Components**:
- ProfileView component for displaying user information
- ProfileEdit component for editing profile
- UserService for profile CRUD operations
- Profile validation logic

## QA Suite

**Location**: `tests/qa/user-profile/`

**Current Status**: RED

**Test Statistics**:
- Total tests: 12
- Passing: 0
- Failing: 12

**Critical Failing Tests**:
1. ProfileView should display user name
2. ProfileEdit should allow editing name
3. UserService should save profile changes
4. Profile validation should reject invalid emails

## Acceptance Criteria

All 12 tests must pass (100% green):
- Zero test failures
- Zero test errors
- Zero skipped tests
- Zero warnings
- Build succeeds
- Lint passes
- TypeScript compilation passes

## Expected Deliverables

1. ✅ All QA tests passing (100%)
2. ✅ Zero test debt
3. ✅ Build quality validated
4. ✅ Evidence trail complete
5. ✅ Completion report submitted
```

---

## III. Pre-Build Validation (MANDATORY)

Before accepting ANY build task, builder MUST validate:

### 1. Instruction Format Validation

- [ ] Instruction phrase is exactly: "Build to Green"
- [ ] Not "Build feature X"
- [ ] Not "Implement component Y"
- [ ] Not "Fix bug Z"
- [ ] Not any other phrase

**If validation fails** → Return BuildPhilosophyViolation error

### 2. Architecture Validation

- [ ] Architecture document exists at specified path
- [ ] Architecture document is accessible
- [ ] Architecture is complete (no TBD, no TODO)
- [ ] Architecture defines ALL components to be built
- [ ] Architecture passes validation checklist

**If validation fails** → Return BuildPhilosophyViolation error

### 3. QA Suite Validation

- [ ] QA suite exists at specified path
- [ ] QA suite is accessible
- [ ] QA suite has been executed
- [ ] QA status is RED (at least 1 test failing)
- [ ] Test failures are clear and specific
- [ ] Zero test debt in QA suite

**If validation fails** → Return BuildPhilosophyViolation error

### 4. Acceptance Criteria Validation

- [ ] Acceptance criteria is clearly defined
- [ ] Acceptance criteria is measurable
- [ ] Typically: "All tests must pass (100% green)"
- [ ] No ambiguity about "done"

**If validation fails** → Return BuildPhilosophyViolation error

### Validation Error Response Format

When ANY validation fails:

```json
{
  "success": false,
  "error": "BuildPhilosophyViolation",
  "message": "REJECTED: <specific reason>",
  "details": {
    "received": "<what was received>",
    "required": "<what is required>",
    "reason": "<why this is required>",
    "philosophy_reference": "/BUILD_PHILOSOPHY.md",
    "action_required": "<what Foreman must do to fix this>"
  },
  "timestamp": "<ISO 8601 timestamp>"
}
```

### Example Validation Failures

**Example 1: Wrong Instruction Format**

```json
{
  "success": false,
  "error": "BuildPhilosophyViolation",
  "message": "REJECTED: Instruction format invalid",
  "details": {
    "received": "Build user profile feature",
    "required": "BUILD TO GREEN",
    "reason": "Builders only accept 'Build to Green' instructions per Build Philosophy",
    "philosophy_reference": "/BUILD_PHILOSOPHY.md",
    "action_required": "Reformat instruction to 'Build to Green' format with architecture reference, QA suite location, and acceptance criteria"
  },
  "timestamp": "2025-12-15T16:00:00Z"
}
```

**Example 2: QA Suite is GREEN**

```json
{
  "success": false,
  "error": "BuildPhilosophyViolation",
  "message": "REJECTED: QA suite status is GREEN (not RED)",
  "details": {
    "received": "QA Status: GREEN (0 failing)",
    "required": "QA Status: RED (at least 1 failing test)",
    "reason": "If tests are already passing, there is nothing to build",
    "philosophy_reference": "/BUILD_PHILOSOPHY.md",
    "action_required": "Verify QA suite is RED before assigning build task. If suite is GREEN, task is already complete."
  },
  "timestamp": "2025-12-15T16:00:00Z"
}
```

**Example 3: Architecture Incomplete**

```json
{
  "success": false,
  "error": "BuildPhilosophyViolation",
  "message": "REJECTED: Architecture document incomplete",
  "details": {
    "received": "Architecture with 'TBD' sections and missing component definitions",
    "required": "Complete architecture with all components defined, zero TBD/TODO markers",
    "reason": "Cannot build from incomplete architecture (One-Time Build Correctness)",
    "philosophy_reference": "/BUILD_PHILOSOPHY.md",
    "action_required": "Complete architecture document per architecture-design-checklist.md, then resubmit build task"
  },
  "timestamp": "2025-12-15T16:00:00Z"
}
```

---

## IV. Build Execution Process

After validation passes, execute this process:

### Step-by-Step Process

```
1. Load Architecture
   ↓
2. Load QA Suite
   ↓
3. Run QA Suite → Identify failing tests
   ↓
4. Select simplest failing test
   ↓
5. Implement minimal code to pass that test
   ↓
6. Run QA Suite again
   ↓
7. Check result:
   - If all tests pass → Go to Final Validation (Step 8)
   - If tests still failing → Go back to Step 4
   - If same test fails 3+ times → Escalate
   ↓
8. Final Validation (Section V)
   ↓
9. Report Completion
```

### Iteration Guidelines

**For Each Iteration**:
1. Document iteration number
2. Document current QA status (X/Y tests passing)
3. Document which test is being targeted
4. Implement minimal code to pass that specific test
5. Document code changes made
6. Run full QA suite
7. Document new QA status
8. Document timestamp

**Minimal Code Principle**:
- Implement ONLY what is needed to pass the current test
- Do NOT add features not tested
- Do NOT add "nice to have" functionality
- Do NOT over-engineer
- Follow YAGNI (You Aren't Gonna Need It)

**Escalation Triggers**:
- Same test fails 3+ times in a row
- Cannot determine how to make test pass
- Architecture and test expectations conflict
- Need to modify protected paths
- Any constitutional violation detected

---

## V. Final Validation (Before Reporting Green)

Before reporting "QA is Green", builder MUST validate ALL of these:

### 1. QA Completeness

- [ ] ALL tests passing (100%)
- [ ] Zero test failures
- [ ] Zero test errors
- [ ] Zero skipped tests
- [ ] Zero test debt

**If ANY item not checked** → Continue iteration, do NOT report green

### 2. Build Quality

- [ ] TypeScript compilation passes (`tsc --noEmit`)
- [ ] Lint passes (zero errors, zero warnings)
- [ ] Build succeeds (no build errors)
- [ ] No console errors

**If ANY item not checked** → Fix issues, do NOT report green

### 3. Interface Integrity

- [ ] All Record<UnionType, T> objects have all union values
- [ ] All imports reference exported members
- [ ] No breaking interface changes (or CS2 approved if breaking)
- [ ] Pre-build validation script passes (if exists)

**If ANY item not checked** → Fix issues, do NOT report green

### 4. Evidence Trail

- [ ] Build iterations documented
- [ ] Test results captured for each iteration
- [ ] Code changes logged
- [ ] Completion timestamp recorded
- [ ] Evidence saved to proper location

**If ANY item not checked** → Complete evidence, do NOT report green

### Final Validation Checklist

```
Final Validation Checklist:
□ QA Status: 100% passing (X/X tests)
□ Test Failures: 0
□ Test Errors: 0
□ Skipped Tests: 0
□ Test Debt: 0
□ TypeScript: ✅ compiles
□ Lint: ✅ zero errors, zero warnings
□ Build: ✅ succeeds
□ Console: ✅ no errors
□ Interface Integrity: ✅ validated
□ Evidence Trail: ✅ complete

IF ALL CHECKED → Report Green
IF ANY UNCHECKED → Continue iteration
```

---

## VI. Completion Reporting

### When to Report Completion

ONLY report completion when:
- Final Validation is 100% complete (all items checked)
- Evidence trail is saved
- All deliverables met

### Completion Report Format

```json
{
  "type": "completion",
  "taskId": "<task-id>",
  "status": "complete",
  "message": "Build to Green: SUCCESS - All tests passing",
  "details": {
    "totalIterations": 12,
    "totalTime": "45 minutes",
    "qaStatus": "GREEN",
    "testsTotal": 10,
    "testsPassing": 10,
    "testsFailing": 0,
    "buildQuality": {
      "typescript": "PASS",
      "lint": "PASS",
      "build": "PASS",
      "console": "CLEAN"
    },
    "interfaceIntegrity": "PASS",
    "testDebt": "ZERO",
    "evidenceLocation": "foreman/evidence/builds/<task-id>/"
  },
  "timestamp": "<ISO 8601>"
}
```

---

## VII. Forbidden Actions

### Builders MUST NEVER

1. **Accept instructions in any other format**
   - No "Build feature X" instructions
   - No "Implement component Y" instructions
   - No "Fix bug Z" instructions
   - ONLY "Build to Green" format

2. **Build without RED QA**
   - If QA is GREEN → Nothing to build
   - If QA doesn't exist → Cannot build
   - ONLY build when QA is RED

3. **Report green with partial passes**
   - 99% passing = FAILURE
   - 301/303 tests = FAILURE
   - ANY failure = BUILD BLOCKED

4. **Skip or modify tests**
   - No .skip()
   - No .todo()
   - No commenting out tests
   - Tests are sacred

5. **Add features not in architecture**
   - No "improvements"
   - No "optimizations"
   - Follow architecture EXACTLY

6. **Add features not in QA**
   - If not tested, don't build it
   - QA defines scope

7. **Modify protected paths**
   - Constitutional files are immutable
   - Modification = HALT + ESCALATE

8. **Bypass governance rules**
   - All rules must be followed
   - No shortcuts
   - No exceptions

---

## VIII. Integration with Build Philosophy

Build to Green Rule is the implementation of Build Philosophy Phase 3.

**Hierarchy**:
```
BUILD_PHILOSOPHY.md (Supreme Authority)
    ↓
Phase 3: Build to Green
    ↓
build-to-green-rule.md (This Document)
    ↓
Builder Agent Contract (Operational Details)
```

**Implements**:
- One-Time Build Correctness (complete architecture before building)
- Zero Regression (all tests must pass)
- Full Architectural Alignment (follow architecture exactly)
- Zero Ambiguity (clear success criteria)

---

## IX. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority for All Builders  
**Precedence**: Builders MUST follow this rule (no exceptions)  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial Build to Green Rule

---

## X. Summary: The Commitment

Build to Green Rule commits to:

1. ✅ **ONLY "Build to Green" Instructions** - No other format accepted
2. ✅ **Mandatory Pre-Build Validation** - Architecture and QA must be complete
3. ✅ **RED QA Required** - If tests pass, nothing to build
4. ✅ **100% Pass Required** - No partial passes
5. ✅ **Complete Evidence Trail** - All work documented

**This is the ONLY way builders work.**  
**No exceptions.**  
**No variations.**

---

*END OF BUILD TO GREEN RULE*
