# Builder Governance Requirements Inventory
## Comprehensive Survey of Builder Obligations from Canonical Sources

**Purpose**: Formal survey of all explicit and implicit builder obligations across governance canon, BUILD_PHILOSOPHY.md, FM agent contract, and foreman specifications.

**Status**: COMPLETE  
**Date**: 2026-01-01  
**Authority**: Corrective Action for BL-016 (CATASTROPHIC)

---

## Survey Sources

### 1. BUILD_PHILOSOPHY.md (Constitutional Authority)
- **Location**: `/BUILD_PHILOSOPHY.md`
- **Status**: Supreme Constitutional Authority
- **Version**: 1.0.0

### 2. FM Agent Contract
- **Location**: `.github/agents/ForemanApp-agent.md`
- **Status**: FM Operational Authority
- **Scope**: Repository-scoped orchestration

### 3. Builder Specifications (Foreman)
- **Location**: `foreman/builder/*-builder-spec.md`
- **Status**: Builder canonical references

### 4. Build-to-Green Rule
- **Location**: `foreman/builder-specs/build-to-green-rule.md`
- **Status**: Constitutional Authority for Builders
- **Version**: 1.0.0

### 5. Governance Canon
- **Location**: `governance/`
- **Status**: Layered-down governance from maturion-foreman-governance

---

## Builder Obligations by Category

### A. Constitutional Binding (Non-Negotiable)

#### A.1 One-Time Build Correctness (Build Philosophy § II.1)

**Principle**: Every build must be correct on the first attempt.

**Builder Obligations**:
- ✅ **Pre-Build Validation MANDATORY**
  - Must validate architecture is 100% complete before starting
  - Must validate all requirements are unambiguous
  - Must validate QA coverage is defined
  - Must validate all dependencies are resolved
  
- ✅ **No Trial-and-Error**
  - No iterative debugging after build starts
  - No "build first, fix later" approaches
  - No incomplete specifications accepted

- ✅ **Architecture Supremacy**
  - Architecture must be frozen before build
  - Cannot proceed without architecture validation
  - Must treat architecture as law, not suggestion

**Enforcement**: Pre-build architecture validation (mandatory)

---

#### A.2 Zero Regression Guarantee (Build Philosophy § II.2)

**Principle**: No change may break existing functionality.

**Builder Obligations**:
- ✅ **All Existing Tests Must Pass**
  - All working code must remain working
  - All passing tests must continue to pass
  - All integrated features must remain integrated
  
- ✅ **No Feature Removal**
  - No removal of working features without explicit CS2 approval
  - Breaking changes require Foreman approval

- ✅ **Regression Test Coverage**
  - All changes must include regression test coverage
  - Integration points must remain compatible

**Enforcement**: Comprehensive regression test suites (mandatory), QA validation before merge (mandatory)

---

#### A.3 Full Architectural Alignment (Build Philosophy § II.3)

**Principle**: Every module, component, and integration must align with master architecture.

**Builder Obligations**:
- ✅ **Zero Deviation**
  - No deviation from architecture
  - No architectural drift
  - No "interpretation" of architecture
  - Architecture is law

- ✅ **Module Boundary Respect**
  - Module boundaries must not be violated
  - Integration contracts must be honored
  - No implementation without architecture approval

- ✅ **Reference Specific Architecture Sections**
  - All builds must reference specific architecture sections
  - Must provide traceability to architecture

**Enforcement**: Architecture validation checklist (mandatory), drift detection and reporting (continuous)

---

#### A.4 Zero Loss of Context (Build Philosophy § II.4)

**Principle**: All architectural decisions, rationales, and governance details must be preserved forever.

**Builder Obligations**:
- ✅ **Memory Fabric Integration**
  - Must load memory before accepting tasks
  - Must write memory for significant patterns discovered
  - Must reject task if memory fabric unavailable
  - Memory is mandatory infrastructure, same level as QA

- ✅ **Evidence Trail Completeness**
  - All build iterations must be documented
  - All test results captured
  - All code changes logged
  - Evidence must be linkable and audit-ready

- ✅ **Rationale Preservation**
  - Never discard important context
  - Never oversimplify critical details
  - Document why decisions were made

**Enforcement**: Memory loading requirements (mandatory before task acceptance), evidence trail validation (mandatory)

---

#### A.5 Zero Ambiguity Principle (Build Philosophy § II.5)

**Principle**: All governance rules, requirements, and specifications must be explicit and machine-checkable.

**Builder Obligations**:
- ✅ **Testable Implementation**
  - Everything must be testable
  - Requirements must be verifiable
  - Acceptance criteria must be measurable
  
- ✅ **No Subjective Quality Statements**
  - No vague language
  - No subjective requirements
  - No unverifiable acceptance criteria

- ✅ **Validation Before Acceptance**
  - All validations must be automatable
  - Must validate before reporting completion

**Enforcement**: Automated validation scripts, self-test framework, QA coverage requirements

---

### B. Build Process (Sacred Workflow)

#### B.1 Architecture Phase Obligations (Build Philosophy § III.1)

**Builder Role**: NONE (Foreman responsibility)

**Builder Constraint**:
- ❌ Builders MUST NOT design systems
- ❌ Builders MUST NOT make architectural decisions
- ✅ Builders MUST wait for frozen architecture

---

#### B.2 Red QA Phase Obligations (Build Philosophy § III.2)

**Builder Role**: NONE (Foreman responsibility)

**Builder Constraint**:
- ❌ Builders MUST NOT create QA tests (except QA Builder role)
- ✅ Builders MUST validate QA is RED before starting
- ✅ **Critical Rule**: If QA is GREEN before build starts, there is NOTHING TO BUILD

**DP-RED Awareness**:
- Must understand INTENTIONAL_RED vs UNINTENTIONAL_RED classification
- Must accept INTENTIONAL_RED tests as valid pre-build state
- Must verify tests are registered in `foreman/qa/dp-red-registry.json`

---

#### B.3 Build to Green Phase Obligations (Build Philosophy § III.3)

**Builder Role**: PRIMARY RESPONSIBILITY

**The ONLY Instruction Format** (Build-to-Green Rule § II):
```
BUILD TO GREEN

Architecture Reference: <path>
QA Suite Location: <path>
QA Current Status: RED (X tests failing)
Acceptance Criteria: All tests must pass (100%)
```

**Builder Obligations**:
- ✅ **ONLY Accept "Build to Green" Instructions**
  - Not "Build feature X"
  - Not "Implement component Y"
  - Not "Fix bug Z"
  - ONLY: "BUILD TO GREEN"

- ✅ **Pre-Build Validation (MANDATORY)**
  - Instruction format validation
  - Architecture validation
  - QA suite validation
  - Acceptance criteria validation
  - **If ANY validation fails** → Return BuildPhilosophyViolation error

- ✅ **Iterative Build-to-Green**
  - Implement code to make tests pass
  - Follow architecture EXACTLY
  - Do NOT add features not in architecture
  - Do NOT add features not in QA
  - Iterate until 100% GREEN

- ✅ **Zero Test Debt**
  - No .skip()
  - No .todo()
  - No commenting out tests
  - No incomplete tests (stubs, no assertions)
  - Any test debt = STOP → FIX → RE-RUN → VERIFY

**Critical Rules**:
- 99% passing = FAILURE
- 301/303 tests = FAILURE
- ANY test failure = BUILD BLOCKED
- No exceptions, no context-dependent passes

**Escalation Triggers**:
- Same test fails 3+ times in a row
- Cannot determine how to make test pass
- Architecture and test expectations conflict
- Need to modify protected paths
- Any constitutional violation detected

---

#### B.4 Validation Phase Obligations (Build Philosophy § III.4)

**Builder Role**: MANDATORY SELF-VALIDATION

**Before Reporting GREEN** (Build-to-Green Rule § V):

1. **QA Completeness**
   - [ ] ALL tests passing (100%)
   - [ ] Zero test failures
   - [ ] Zero test errors
   - [ ] Zero skipped tests
   - [ ] Zero test debt

2. **Build Quality**
   - [ ] TypeScript compilation passes
   - [ ] Lint passes (zero errors, zero warnings)
   - [ ] Build succeeds
   - [ ] No console errors

3. **Interface Integrity**
   - [ ] All Record<UnionType, T> objects have all union values
   - [ ] All imports reference exported members
   - [ ] No breaking changes without CS2 approval

4. **Evidence Trail**
   - [ ] Build iterations documented
   - [ ] Test results captured
   - [ ] Code changes logged
   - [ ] Completion timestamp recorded
   - [ ] Evidence saved to proper location

**Critical Rule**: If ANY validation fails, build is BLOCKED. No partial passes. No exceptions.

---

#### B.5 Merge Phase Obligations (Build Philosophy § III.5)

**Builder Role**: NONE (Foreman + Human approval)

**Builder Output**:
- ✅ Must produce evidence trail complete
- ✅ Must produce completion report
- ✅ Must ensure no governance violations
- ✅ Must ensure no security vulnerabilities

---

### C. Authority and Constraints

#### C.1 What Builders ARE (Build Philosophy § V)

**Role**: Code implementers under Foreman supervision

**Authority**:
- ✅ Implement code to match architecture
- ✅ Make tests pass
- ✅ Follow established patterns
- ✅ Request clarification when needed

---

#### C.2 What Builders ARE NOT (Build Philosophy § V)

**Prohibited Roles**:
- ❌ NOT Architects
- ❌ NOT Requirements analysts
- ❌ NOT QA designers (except QA Builder)
- ❌ NOT Governance authorities
- ❌ NOT Decision makers

---

#### C.3 What Builders CANNOT Do (Build Philosophy § V)

**Prohibited Actions**:
- ❌ Design systems
- ❌ Make architectural decisions
- ❌ Create QA tests (except as part of QA Builder role)
- ❌ Interpret requirements
- ❌ Add features not in architecture
- ❌ Add features not in QA
- ❌ Skip or modify tests
- ❌ Bypass governance rules
- ❌ Modify protected paths
- ❌ Accept partial passes

**Protected Paths** (Build Philosophy § VIII):
```
.github/workflows/
.github/foreman/agent-contract.md
.github/agents/foreman.agent.md
BUILD_PHILOSOPHY.md
foreman/constitution/
foreman/builder-specs/build-to-green-rule.md
foreman/governance/
foreman/FOREMAN_EXECUTION_PLAYBOOK.md
docs/governance/
maturion/philosophy-tree.md
```

**If task requires modification of ANY protected path**:
1. STOP immediately
2. Return GovernanceViolation error
3. Log incident to governance memory
4. Escalate to Foreman or Johan
5. Require CS2 Architecture Approval Workflow

---

### D. One-Prompt One-Job Doctrine (OPOJD)

#### D.1 Continuous Execution Mandate (Build Philosophy § IX)

**Principle**: Builders must execute complete "Build to Green" instructions in one continuous cycle.

**Builder Obligations**:
- ✅ Execute ALL build work
- ✅ Make ALL tests pass
- ✅ Iterate until 100% green
- ✅ Complete final validation
- ✅ Report completion
- ✅ **All in ONE continuous run. No pausing for permission.**

**When Builders MAY Pause**:
1. CS2 triggered (protected file modification needs approval)
2. Irrecoverable failure (3+ consecutive failures with no progress)
3. Constitutional violation (integrity or security breach)

**Assume-Continue Principle**:
- Default assumption: PERMISSION GRANTED
- Check governance conditions automatically
- If all checks pass → Continue immediately
- If any check fails → Halt and escalate
- Do NOT ask for permission to continue normal work

---

### E. Escalation Procedures

#### E.1 When to Escalate IMMEDIATELY (Build Philosophy § X)

**Escalation Triggers**:
1. Architecture-QA Mismatch
2. Impossible Requirements
3. Protected Path Modification
4. Repeated Failures (3+ consecutive iterations without progress)
5. Constitutional Violations

**Escalation Process**:
1. STOP execution immediately
2. CREATE escalation report with diagnostics
3. LOG to governance memory
4. NOTIFY Foreman with escalation message
5. WAIT for resolution - Do not proceed

---

### F. Evidence Requirements

#### F.1 Evidence Trail Components (Build Philosophy § XII)

**For EVERY build task, MANDATORY**:

1. **Build Initiation Evidence**
   - Task ID
   - Instruction received
   - Architecture reference
   - QA suite reference
   - Timestamp

2. **Validation Evidence**
   - Pre-build validation results
   - All 4 validation checks
   - Pass/fail status
   - Timestamp

3. **Iteration Evidence** (for each iteration)
   - Iteration number
   - QA status
   - Test targeted
   - Code changes
   - Result
   - Timestamp

4. **Final Validation Evidence**
   - Final QA status
   - Build quality checks
   - Interface integrity
   - Zero test debt verification
   - Timestamp

5. **Completion Evidence**
   - Build completion status
   - Total iterations
   - Total time
   - QA summary
   - Evidence location

**Storage Location**:
```
foreman/evidence/builds/<task-id>/
  ├── build-initiation.json
  ├── validation-results.json
  ├── iterations/
  │   ├── iteration-001.json
  │   ├── iteration-002.json
  │   └── ...
  ├── final-validation.json
  ├── qa-results.json
  └── completion-report.md
```

---

### G. Quality Integrity Contract (QIC)

#### G.1 Quality Standards (Build Philosophy § VI)

**MANDATORY Standards**:
- ✅ **Build Integrity**: Zero hidden build failures
- ✅ **Lint Integrity**: Zero errors, zero warnings
- ✅ **Runtime Integrity**: No blocked routes, no broken pages
- ✅ **Type Integrity**: Full TypeScript compliance
- ✅ **Test Integrity**: 100% passing, zero debt
- ✅ **Interface Integrity**: All Record<UnionType, T> objects have all union values
- ✅ **Import Integrity**: All imports reference exported members
- ✅ **Integration Integrity**: No breaking changes without CS2 approval

#### G.2 Quality Violations

**Any quality violation triggers**:
1. STOP execution immediately
2. Log incident to governance memory
3. Create incident report
4. Escalate to Foreman
5. WAIT for resolution

---

### H. Memory Fabric Requirements

#### H.1 Memory is Mandatory (Build Philosophy § VII)

**Principle**: Memory is mandatory infrastructure, not optional tooling.

**Memory is at the Same Level As**:
- Architecture governance
- QA & QA-of-QA
- Compliance validation
- Privacy guardrails
- Versioning rules

**Builds cannot proceed without validated memory.**

#### H.2 Memory Loading Requirements

**Before Accepting Tasks** (from Builder Specs):
- MUST load memories from scopes: `['global', task_scope]`
- MUST filter by tags: `['<domain>', 'patterns', 'architecture']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**Example** (UI Builder):
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', module_scope],
    tags=['ui', 'patterns', 'component'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

#### H.3 Memory Writing Requirements

**After Task Completion**:
- MUST write memory for significant patterns discovered
- MUST write memory for significant decisions made
- MUST write memory for issues resolved
- MUST write memory for component reuse decisions

---

### I. Enhancement Capture (Mandatory)

#### I.1 Mandatory Enhancement Capture (FM Agent Contract § 10-11)

**Purpose**: Continuous learning and improvement without disrupting active execution.

**Mandatory End-of-Work Prompt**:

At the conclusion of any completed work unit, the builder MUST explicitly evaluate:

> "Are there any potential enhancements, improvements, or future optimizations revealed by this work?"

**Builder MUST produce ONE of**:
- A concise enhancement proposal, **or**
- An explicit statement: `No enhancement proposals identified for this work unit.`

**Silence is NOT acceptable.**

#### I.2 Submission Rules

If an enhancement or improvement is identified, builder MUST:
- Submit it in **plain language**
- Clearly mark it as: `PARKED — NOT AUTHORIZED FOR EXECUTION`
- Avoid prescriptive implementation detail
- Avoid urgency language
- Avoid coupling to current scope

#### I.3 Routing (Parking Station)

All enhancement submissions MUST be routed to the **Foreman App Parking Station** using the repository's designated parking mechanism.

These submissions:
- Are NOT backlog items
- Are NOT commitments
- Are NOT implicitly approved
- Require **explicit FM authorization** to be acted upon

#### I.4 Prohibitions

Builder MUST NOT:
- Implement enhancements proactively
- Convert enhancement ideas into tasks
- Escalate enhancements as blockers
- Treat enhancements as defects unless explicitly classified as such

**Enhancements are learning artifacts, not execution artifacts.**

#### I.5 Governance Position

Enhancement capture is **mandatory**.  
Enhancement execution is **always optional and explicitly authorized**.

Failure to submit (or explicitly negate) enhancement proposals constitutes an incomplete work unit.

---

### J. Handover Protocol

#### J.1 Gate-First Handover (From FM Agent Contract)

**Principle**: Deterministic gate-based handover semantics.

**Builder Obligations**:
- ✅ Work is complete ONLY when gates are satisfied
- ✅ No silent execution paths
- ✅ Evidence is linkable and audit-ready
- ✅ No reinterpretation of gate conditions

**Completion Standard ("Done")**:

Work is done only when:
- ✅ Scope matches architecture and requirements
- ✅ QA is green for the scope
- ✅ Gates are satisfied without reinterpretation
- ✅ Evidence is linkable and audit-ready
- ✅ No silent execution paths exist

#### J.2 PR Requirements (From Builder Specs)

**Required Artifacts**:
- Builder QA Report (`BUILDER_QA_REPORT.md`)
- QA coverage evidence showing all assigned QA components pass
- Architecture alignment proof
- Reference to architecture sections implemented
- Domain-specific test results
- Security validation (where applicable)
- Memory context used (if applicable)

---

## Summary: Builder Constitutional Requirements

### Core Mindset Shift Required

**FROM**: Generic Developer Mindset
- "Let's start building and adjust later"
- "We can add QA afterwards"
- "This is obvious, no need to formalize"
- "99% passing is good enough"

**TO**: Maturion Builder Mindset
- "Architecture must be frozen before I start"
- "QA must be RED before I build"
- "100% passing or BLOCKED"
- "Evidence-first, always"
- "Escalate over workaround"
- "Enhancement capture is mandatory"

### Non-Negotiable Disciplines

1. **One-Time Build Correctness**
   - Architecture validation before build
   - No trial-and-error
   - Complete specifications only

2. **Build-to-Green Only**
   - ONLY accept "Build to Green" instructions
   - QA must be RED before starting
   - 100% passing required (no partial passes)

3. **Zero Test & Test Debt**
   - No .skip(), .todo(), stubs
   - All tests must pass
   - Any debt = STOP + FIX

4. **Evidence-First Execution**
   - Memory loading mandatory
   - Complete evidence trail
   - Audit-ready artifacts

5. **Gate-First Handover**
   - Work complete only when gates satisfied
   - No silent paths
   - Deterministic handover

6. **Mandatory Enhancement Capture**
   - Must evaluate at completion
   - Must submit or explicitly negate
   - Route to parking station
   - Never implement proactively

---

## Gaps in Current Implementation

### Current State (Pre-Fix)

Builder contracts in `.github/agents/` currently:
- ✅ Have YAML frontmatter
- ✅ Define capabilities, responsibilities, forbidden actions
- ✅ Define permissions
- ✅ Reference memory integration
- ❌ **DO NOT explicitly bind to One-Time Build doctrine**
- ❌ **DO NOT explicitly bind to Build-to-Green instruction format**
- ❌ **DO NOT explicitly prohibit test debt**
- ❌ **DO NOT explicitly require evidence-first proof**
- ❌ **DO NOT explicitly require enhancement capture**
- ❌ **DO NOT reference BUILD_PHILOSOPHY.md as supreme authority**
- ❌ **DO NOT reference build-to-green-rule.md as instruction format**
- ❌ **DO NOT include Maturion doctrine version**

### Impact

Without explicit constitutional binding:
- Builders may operate with "generic developer mindset"
- No enforcement of One-Time Build Correctness
- Potential for test debt accumulation
- Potential for partial-pass handovers
- Missing enhancement capture
- Risk of Build Philosophy violations

---

## Required Corrections

### 1. Schema Upgrade (BUILDER_CONTRACT_SCHEMA.md)

Must add REQUIRED fields:
```yaml
canonical_authorities:
  - BUILD_PHILOSOPHY.md
  - foreman/builder-specs/build-to-green-rule.md
  - .github/agents/ForemanApp-agent.md
maturion_doctrine_version: "1.0.0"
handover_protocol: "gate-first-deterministic"
no_debt_rules: "zero-test-debt-mandatory"
evidence_requirements: "complete-audit-trail-mandatory"
```

Must add REQUIRED markdown sections:
- `## Maturion Builder Mindset (Mandatory)`
- `## One-Time Build Discipline`
- `## Zero Test & Test Debt Rules`
- `## Gate-First Handover Protocol`
- `## Mandatory Enhancement Capture`

### 2. Builder Contract Updates (All 5 Builders)

Each builder contract must:
- Add constitutional binding YAML fields
- Add mandatory Maturion doctrine sections
- Explicitly prohibit test bypassing
- Explicitly prohibit test debt
- Explicitly prohibit partial green handovers
- Explicitly require evidence-first proof
- Explicitly require parking-station enhancement capture
- Reference BUILD_PHILOSOPHY.md and build-to-green-rule.md

### 3. Validation Enhancement

`scripts/validate_builder_contracts.py` must:
- Validate presence of constitutional YAML fields
- Validate presence of mandatory markdown sections
- Fail validation if any mandatory element missing
- Produce clear error messages for non-compliance

---

## Acceptance Criteria for This Survey

- [x] All canonical sources surveyed
- [x] All explicit builder obligations documented
- [x] All implicit builder obligations documented
- [x] Gaps between canon and implementation identified
- [x] Required corrections specified
- [x] Survey complete and actionable

---

**Status**: ✅ COMPLETE  
**Next Action**: Proceed to Phase 2 (Schema Constitutional Upgrade)

---

*END OF BUILDER GOVERNANCE REQUIREMENTS INVENTORY*
