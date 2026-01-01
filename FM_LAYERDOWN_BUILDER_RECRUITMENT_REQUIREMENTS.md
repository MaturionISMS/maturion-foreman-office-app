# FM Layer-Down: Builder Recruitment Requirements

**Document Type**: Authoritative Governance Layer-Down  
**Status**: CANONICAL INSTRUCTION  
**Authority**: Governance Canon Translation  
**Version**: 1.0.0  
**Date**: 2026-01-01  
**Purpose**: Translate governance canon into explicit, machine-operational FM obligations for builder recruitment and governance submission

---

## Document Classification

**This is a LAYER-DOWN document, NOT an implementation.**

- ✅ **IN SCOPE**: Translating governance canon into FM-facing requirements
- ✅ **IN SCOPE**: Making implicit obligations explicit
- ✅ **IN SCOPE**: Defining STOP conditions for non-compliance
- ✅ **IN SCOPE**: Clarifying canonical vs non-canonical artifacts
- ❌ **OUT OF SCOPE**: Changing governance canon
- ❌ **OUT OF SCOPE**: Editing FM app code
- ❌ **OUT OF SCOPE**: Moving or rewriting builder contracts
- ❌ **OUT OF SCOPE**: Implementing automation or CI gates

---

## Executive Summary

This document defines **how FM MUST implement builder recruitment and governance submission** based on existing governance canon. It serves as the single source of truth for:

1. **Canonical Builder Contract Location** — Where builder contracts MUST exist
2. **Mandatory Contract Structure** — What builder contracts MUST contain
3. **Governance Submission Obligations** — What governance rules builders MUST be bound to
4. **FM Responsibilities** — What FM MUST do during builder recruitment
5. **STOP Conditions** — When FM MUST refuse to recruit or execute

**Non-Negotiable Principle**: Builder recruitment is a **governance act**, not a documentation task. All builder contracts MUST be:
- In the canonical location
- Machine-parseable
- Constitutionally bound
- Governance-complete

**Failure to meet any requirement = UNRECRUITED AGENT = EXECUTION FORBIDDEN**

---

## 1. Canonical Builder Contract Location (NON-NEGOTIABLE)

### 1.1 ONLY Canonical Location

**Requirement**: Builder contracts MUST exist at:

```
.github/agents/<builder-id>.md
```

**Examples**:
- `.github/agents/ui-builder.md`
- `.github/agents/api-builder.md`
- `.github/agents/schema-builder.md`
- `.github/agents/integration-builder.md`
- `.github/agents/qa-builder.md`

**Authority**: 
- `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` (Line 271-273)
- `.github/agents/BUILDER_CONTRACT_SCHEMA.md` (File Location section)

### 1.2 Root-Level Contracts Are NON-CANONICAL

**Rule**: Any builder contract found outside `.github/agents/` is **NON-CANONICAL** and MUST be treated as:
- Historical artifact
- Migration remnant
- Documentation reference
- **NOT** a recruited builder

**Examples of NON-CANONICAL locations** (MUST BE IGNORED):
- `/builderui-builder.md` (root-level)
- `/builder-contracts/ui-builder.md` (custom directory)
- `/docs/builders/ui-builder.md` (documentation)
- `/foreman/builder/<builder>-spec.md` (specification, not contract)

**FM Obligation**: FM MUST discover builders ONLY from `.github/agents/`. Builders in any other location are NOT recruited.

### 1.3 STOP Condition: Builder Not in Canonical Location

**IF** a builder contract exists outside `.github/agents/`:
- **THEN** FM MUST NOT recruit that builder
- **AND** FM MUST NOT assign tasks to that builder
- **AND** FM MUST NOT treat that builder as available
- **AND** FM MUST escalate if builder recruitment is attempted

**Escalation Message**:
```
STOP: Builder contract found at non-canonical location.
- Expected: .github/agents/<builder-id>.md
- Found: <actual-path>
- Action Required: Move contract to canonical location or create new canonical contract
- Governance Reference: PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md (Line 271-273)
```

---

## 2. Mandatory Contract Structure (Machine-Operational)

### 2.1 File Format Requirements

**Requirement**: All builder contracts MUST use:
- **YAML frontmatter** for machine-readable metadata
- **Markdown body** for human-readable contract sections

**Authority**: `.github/agents/BUILDER_CONTRACT_SCHEMA.md` (File Format section)

**Structure**:
```markdown
---
# YAML frontmatter (machine-readable)
builder_id: <builder-id>
builder_type: <type>
version: <version>
# ... all required fields
---

# Markdown body (human-readable)
## Section 1
Content...
```

### 2.2 Required YAML Frontmatter Fields

**ALL of the following fields are MANDATORY** (no exceptions):

#### 2.2.1 Universal Required Fields

1. **builder_id** (string)
   - Unique identifier for this builder
   - Format: `lowercase-with-hyphens`
   - Must match filename (e.g., `ui-builder.md` → `builder_id: ui-builder`)
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 1)

2. **builder_type** (string)
   - Classification of builder role
   - Allowed values: `specialized`, `qa`, `cross-cutting`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 2)

3. **version** (string)
   - Contract version (semantic versioning)
   - Format: `major.minor.patch`
   - Example: `version: 1.0.0`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 3)

4. **status** (string)
   - Recruitment status
   - Allowed values: `recruited`, `pending`, `deprecated`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 4)

5. **capabilities** (array of strings)
   - Technical skills and domains
   - Example: `[ui, frontend, components, styling]`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 5)

6. **responsibilities** (array of strings)
   - What this builder is responsible for
   - Example: `[UI components, Layouts, Wizards]`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 6)

7. **forbidden** (array of strings)
   - What this builder MUST NOT do
   - Example: `[Backend logic, Database schema changes]`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 7)

8. **permissions** (object)
   - Read/write paths this builder can access
   - Structure: `{ read: [paths...], write: [paths...] }`
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 8)

9. **recruitment_date** (string)
   - Date builder was recruited (YYYY-MM-DD)
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 9)

#### 2.2.2 Maturion Doctrine Fields (REQUIRED — CANNOT VALIDATE WITHOUT THESE)

**As of Schema Version 2.0, these fields are MANDATORY.**

10. **canonical_authorities** (array of strings)
    - List of canonical governance sources this builder is bound to
    - **MUST include at minimum**:
      - `BUILD_PHILOSOPHY.md`
      - `foreman/builder-specs/build-to-green-rule.md`
      - `.github/agents/ForemanApp-agent.md`
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 10)

11. **maturion_doctrine_version** (string)
    - Version of Maturion Build Philosophy
    - Current version: `"1.0.0"`
    - Must match BUILD_PHILOSOPHY.md version
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 11)

12. **handover_protocol** (string)
    - Handover semantics
    - Required value: `"gate-first-deterministic"`
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 12)

13. **no_debt_rules** (string)
    - Test debt policy
    - Required value: `"zero-test-debt-mandatory"`
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 13)

14. **evidence_requirements** (string)
    - Evidence trail policy
    - Required value: `"complete-audit-trail-mandatory"`
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 14)

### 2.3 Required Markdown Sections

**ALL of the following sections are MANDATORY in the contract body:**

#### 2.3.1 Maturion Doctrine Sections (REQUIRED — CANNOT VALIDATE WITHOUT THESE)

1. **## Maturion Builder Mindset — MANDATORY**
   - Core mindset: NOT a generic developer
   - Principle: Governance-first, not code-first
   - Sacred Workflow: Architecture → QA-to-Red → Build-to-Green → Validation → Merge
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 1 of Markdown Sections)

2. **## One-Time Build Discipline — MANDATORY**
   - Commitment to One-Time Build Correctness
   - Pre-build validation checklist
   - Prohibited actions (no trial-and-error, no build-first-fix-later)
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 2 of Markdown Sections)

3. **## Zero Test & Test Debt Rules — MANDATORY**
   - Absolute prohibition of test debt
   - 100% pass requirement (99% = FAILURE)
   - Test debt response protocol (STOP → FIX → RE-RUN → VERIFY)
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 3 of Markdown Sections)

4. **## Gate-First Handover Protocol — MANDATORY**
   - Deterministic gate-based completion semantics
   - Completion checklist
   - No reinterpretation of gate conditions
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 4 of Markdown Sections)

5. **## Mandatory Enhancement Capture — MANDATORY**
   - Required end-of-work enhancement evaluation
   - Submission or explicit negation required
   - Parking station routing
   - Prohibition of proactive implementation
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 5 of Markdown Sections)

#### 2.3.2 Standard Sections (REQUIRED)

6. **## Purpose**
   - Why this builder exists
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 6 of Markdown Sections)

7. **## Responsibilities**
   - Detailed list of responsibilities
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 7 of Markdown Sections)

8. **## Capabilities**
   - Technical skills and domains
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 8 of Markdown Sections)

9. **## Forbidden Actions**
   - Explicit list of prohibited actions
   - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 9 of Markdown Sections)

10. **## Scope Boundaries**
    - What is in/out of scope
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 10 of Markdown Sections)

11. **## Integration Points**
    - How this builder coordinates with others
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 11 of Markdown Sections)

12. **## Escalation Procedures**
    - When and how to escalate
    - Authority: BUILDER_CONTRACT_SCHEMA.md (§ 12 of Markdown Sections)

### 2.4 STOP Condition: Missing or Invalid YAML Preface

**IF** any required YAML field is missing or invalid:
- **THEN** FM MUST NOT recruit that builder
- **AND** FM MUST NOT assign tasks to that builder
- **AND** FM MUST escalate with specific field list

**Escalation Message**:
```
STOP: Builder contract YAML preface invalid.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Missing/Invalid Fields: <list of fields>
- Required Fields Reference: BUILDER_CONTRACT_SCHEMA.md
- Action Required: Add/correct all required YAML fields
```

### 2.5 STOP Condition: Missing Mandatory Sections

**IF** any required markdown section is missing:
- **THEN** FM MUST NOT recruit that builder
- **AND** FM MUST NOT assign tasks to that builder
- **AND** FM MUST escalate with specific section list

**Escalation Message**:
```
STOP: Builder contract missing mandatory sections.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Missing Sections: <list of sections>
- Required Sections Reference: BUILDER_CONTRACT_SCHEMA.md
- Action Required: Add all missing mandatory sections
```

---

## 3. Governance Submission Obligations (Exhaustive)

**Purpose**: Define ALL governance aspects that builders MUST be explicitly bound to.

**Principle**: No assumptions. Every governance rule, discipline, and constraint MUST be explicitly stated in builder contracts.

**Authority**:
- BUILD_PHILOSOPHY.md
- .github/agents/ForemanApp-agent.md
- Governance canon (referenced in issue comments as GOVERNANCE_BUILDER_SUBMISSION_SURVEY.md)
- BUILDER_CONTRACT_BINDING_CHECKLIST.md (referenced in issue)

### 3.1 Authority Hierarchy & Override Semantics

**Requirement**: Builder contracts MUST explicitly state:

1. **Constitutional Supremacy**
   - BUILD_PHILOSOPHY.md is supreme constitutional authority
   - Canonical governance (maturion-foreman-governance) is binding
   - FM agent contract is operational authority
   - Builder spec is role-specific guidance

2. **Override Authority**
   - Johan (repository owner) has absolute override authority
   - Overrides are temporary and explicit
   - Overrides do not modify governance documents
   - Authority: BUILD_PHILOSOPHY.md (§ XI - Owner Override Authority)

3. **Escalation Chain**
   - Builder → FM → Johan
   - No lateral escalation
   - No skipping FM

**Contract Section**: Must be covered in "Maturion Builder Mindset" or dedicated "Authority & Governance" section

**STOP Condition**: If authority hierarchy is not explicit or conflicts with BUILD_PHILOSOPHY.md → DO NOT RECRUIT

---

### 3.2 Protected Paths & STOP Rules

**Requirement**: Builder contracts MUST explicitly state:

1. **Protected Path Awareness**
   - Builders MUST check permissions before modifying files
   - Protected paths require CS2 (Change Sequence 2) approval
   - Authority: FM agent contract (protected paths policy)

2. **STOP Triggers**
   - Modification of file outside permitted write paths
   - Modification of constitutional governance files
   - Architectural drift detected
   - Test failures that cannot be resolved
   - Authority: BUILD_PHILOSOPHY.md (§ X - Escalation Procedures)

**Contract Section**: Must be covered in "Scope Boundaries" or "Forbidden Actions"

**STOP Condition**: If protected path rules are not explicit → DO NOT RECRUIT

---

### 3.3 OPOJD (One-Prompt One-Job Doctrine)

**Requirement**: Builder contracts MUST explicitly bind to OPOJD principles:

1. **Continuous Execution Mandate**
   - Execute ALL build work in one continuous cycle
   - Make ALL tests pass
   - Iterate until 100% green
   - Complete final validation
   - Report completion
   - **All in ONE continuous run. No pausing for permission.**
   - Authority: BUILD_PHILOSOPHY.md (§ IX - One-Prompt One-Job Doctrine)

2. **When Builders MAY Pause**
   - ONLY pause for:
     - CS2 triggered (protected file modification)
     - Irrecoverable failure (3+ consecutive failures with no progress)
     - Constitutional violation (integrity or security breach)
   - Authority: BUILD_PHILOSOPHY.md (§ IX)

3. **Assume-Continue Principle**
   - Default assumption: PERMISSION GRANTED
   - Check governance conditions automatically
   - If all checks pass → Continue immediately
   - If any check fails → Halt and escalate
   - Do NOT ask for permission to continue normal work
   - Authority: BUILD_PHILOSOPHY.md (§ IX)

**Contract Section**: Must be covered in "Gate-First Handover Protocol" or dedicated "OPOJD" section

**STOP Condition**: If OPOJD is not explicitly declared → DO NOT RECRUIT

---

### 3.4 One-Time Build Discipline

**Requirement**: Builder contracts MUST explicitly commit to:

1. **One-Time Build Correctness Principle**
   - Every build must be correct on the first attempt
   - No iterative debugging after build starts
   - No trial-and-error implementation
   - No "build first, fix later" approaches
   - Authority: BUILD_PHILOSOPHY.md (§ II.1)

2. **Pre-Build Validation (MANDATORY)**
   - Architecture document exists and is complete (no TBD, no TODO)
   - Architecture has been validated and frozen
   - All requirements are unambiguous
   - QA coverage is defined and RED
   - All dependencies resolved
   - Memory fabric available and loaded
   - Authority: BUILD_PHILOSOPHY.md (§ II.1)

3. **Prohibited Actions**
   - Starting implementation before architecture is frozen
   - Trial-and-error debugging during build
   - "Build first, fix later" approaches
   - Interpreting or inferring from incomplete specifications
   - Adding features not in architecture
   - Adding features not in QA
   - Authority: BUILD_PHILOSOPHY.md (§ II.1)

**Contract Section**: Must be covered in "One-Time Build Discipline — MANDATORY" section (REQUIRED)

**STOP Condition**: If One-Time Build discipline is not explicit → DO NOT RECRUIT

---

### 3.5 Zero Test Debt (99% = FAILURE)

**Requirement**: Builder contracts MUST explicitly enforce:

1. **Absolutely Prohibited**
   - `.skip()` — No skipped tests
   - `.todo()` — No TODO tests
   - Commented-out tests
   - Incomplete tests (stubs without assertions)
   - Partial passes (99% passing = FAILURE)
   - Authority: BUILD_PHILOSOPHY.md (§ III - Build Process)

2. **100% Pass Requirement**
   - 99% passing = TOTAL FAILURE
   - 301/303 tests = TOTAL FAILURE
   - ANY test failure = BUILD BLOCKED
   - No exceptions, no context-dependent passes
   - Authority: BUILD_PHILOSOPHY.md (§ III)

3. **Test Debt Response Protocol**
   - STOP execution immediately
   - FIX test debt
   - RE-RUN full test suite
   - VERIFY 100% passing
   - Only then continue
   - Authority: BUILD_PHILOSOPHY.md (§ III)

4. **Escalation Rule**
   - If same test fails 3+ times → STOP and escalate to Foreman
   - Authority: BUILD_PHILOSOPHY.md (§ X)

**Contract Section**: Must be covered in "Zero Test & Test Debt Rules — MANDATORY" section (REQUIRED)

**STOP Condition**: If Zero Test Debt is not explicit or 100% rule is not stated → DO NOT RECRUIT

---

### 3.6 Evidence Production Obligations

**Requirement**: Builder contracts MUST explicitly commit to producing:

1. **Build Initiation Evidence**
   - Task ID, instruction received
   - Architecture reference
   - QA suite reference
   - Timestamp
   - Authority: BUILD_PHILOSOPHY.md (§ XII - Evidence Requirements)

2. **Validation Evidence**
   - Pre-build validation results
   - All 4 validation checks
   - Pass/fail status
   - Timestamp
   - Authority: BUILD_PHILOSOPHY.md (§ XII)

3. **Iteration Evidence**
   - For each iteration: iteration number, QA status, test targeted, code changes, result, timestamp
   - Authority: BUILD_PHILOSOPHY.md (§ XII)

4. **Final Validation Evidence**
   - Final QA status
   - Build quality checks
   - Interface integrity
   - Zero test debt verification
   - Timestamp
   - Authority: BUILD_PHILOSOPHY.md (§ XII)

5. **Completion Evidence**
   - Final report
   - All gates satisfied
   - Evidence trail complete
   - Authority: BUILD_PHILOSOPHY.md (§ XII)

**Contract Section**: Must be covered in "Gate-First Handover Protocol" or "Evidence Requirements" section

**STOP Condition**: If evidence obligations are not explicit → DO NOT RECRUIT

---

### 3.7 Pre-Merge Gate Obligations

**Requirement**: Builder contracts MUST explicitly bind to ALL gate types:

1. **Architecture Validation Gate**
   - Architecture must be complete and frozen
   - No TBD, no TODO, no placeholder text
   - Authority: BUILD_PHILOSOPHY.md (§ III.1)

2. **QA-to-Red Gate**
   - QA suite must exist and be RED
   - All architecture components must be tested
   - Test failures must be clear and specific
   - No test debt
   - Authority: BUILD_PHILOSOPHY.md (§ III.2)

3. **Build-to-Green Gate**
   - 100% tests passing (no exceptions)
   - Zero test debt
   - Zero lint warnings/errors
   - Build succeeds
   - TypeScript compiles
   - Authority: BUILD_PHILOSOPHY.md (§ III.3)

4. **Zero Regression Gate**
   - All existing tests must pass
   - No working features removed
   - Integration points remain compatible
   - Authority: BUILD_PHILOSOPHY.md (§ II.2)

5. **Memory & Evidence Gate**
   - All evidence trail components present
   - Memory fabric updated
   - Governance events logged
   - Authority: BUILD_PHILOSOPHY.md (§ XII)

**Contract Section**: Must be covered in "Gate-First Handover Protocol — MANDATORY" section

**STOP Condition**: If any gate type is not explicitly covered → DO NOT RECRUIT

---

### 3.8 Architecture-as-Law Binding

**Requirement**: Builder contracts MUST explicitly bind to:

1. **Full Architectural Alignment**
   - No deviation from architecture
   - No architectural drift
   - No "interpretation" of architecture
   - Architecture is law
   - Authority: BUILD_PHILOSOPHY.md (§ II.3)

2. **Architecture Freeze Point**
   - Architecture is FROZEN once builders start
   - No changes allowed without stopping build and re-planning
   - Authority: BUILD_PHILOSOPHY.md (§ III.1)

3. **Architecture-QA Mismatch → STOP**
   - Architecture specifies something not tested → ESCALATE
   - QA tests something not in architecture → ESCALATE
   - Authority: BUILD_PHILOSOPHY.md (§ X.1)

4. **No Feature Addition**
   - Builders do NOT add features not in architecture
   - Builders do NOT add features not in QA
   - Authority: BUILD_PHILOSOPHY.md (§ III.3)

**Contract Section**: Must be covered in "Maturion Builder Mindset — MANDATORY" section

**STOP Condition**: If architecture supremacy is not explicit or mismatch handling is not defined → DO NOT RECRUIT

---

### 3.9 Technology Governance (TED / TSP)

**Requirement**: Builder contracts MUST acknowledge:

1. **Technology Governance Awareness**
   - Technology decisions follow governance (TED - Technology Evaluation Directive)
   - Technology stack changes require TSP (Technology Stack Proposal)
   - Builders do NOT make unilateral technology choices

2. **Escalation for Technology Changes**
   - Any new library, framework, or tool → ESCALATE
   - Any change to build toolchain → ESCALATE
   - Any change to runtime dependencies → ESCALATE

**Contract Section**: Must be covered in "Forbidden Actions" or "Escalation Procedures"

**STOP Condition**: If technology governance is not acknowledged → DO NOT RECRUIT

---

### 3.10 Escalation Rules (Format, Triggers, Destinations)

**Requirement**: Builder contracts MUST explicitly define:

1. **When to Escalate IMMEDIATELY**
   - Architecture-QA mismatch
   - Impossible requirements
   - Protected path modification
   - Repeated failures (3+ iterations without progress)
   - Constitutional violations
   - Authority: BUILD_PHILOSOPHY.md (§ X)

2. **Escalation Process**
   - STOP execution immediately
   - CREATE escalation report with diagnostics
   - LOG to governance memory
   - NOTIFY Foreman with escalation message
   - WAIT for resolution - Do not proceed
   - Authority: BUILD_PHILOSOPHY.md (§ X)

3. **Escalation Message Format**
   - Clear problem statement
   - Diagnostic evidence
   - Governance reference
   - Proposed resolution (if known)

**Contract Section**: Must be covered in "Escalation Procedures" section (REQUIRED)

**STOP Condition**: If escalation triggers or process are not explicit → DO NOT RECRUIT

---

### 3.11 Prohibited Builder Roles ("What Builders Are NOT")

**Requirement**: Builder contracts MUST explicitly state what builders are NOT:

1. **NOT Generic Developers**
   - NOT agents who iterate to solutions
   - NOT agents who interpret vague requirements
   - NOT agents who "figure things out"
   - Authority: BUILDER_CONTRACT_SCHEMA.md (Maturion Builder Mindset)

2. **NOT Architecture Authors**
   - Builders do NOT design architecture
   - Builders do NOT modify architecture
   - Builders do NOT interpret ambiguous architecture
   - Authority: BUILD_PHILOSOPHY.md (§ III)

3. **NOT QA Authors**
   - Builders do NOT design test suites (except QA builder)
   - Builders do NOT modify test intent
   - Builders do NOT skip tests to make builds pass
   - Authority: BUILD_PHILOSOPHY.md (§ III)

4. **NOT Governance Decision-Makers**
   - Builders do NOT override governance
   - Builders do NOT interpret governance
   - Builders do NOT bypass governance checks
   - Authority: BUILD_PHILOSOPHY.md (§ I)

5. **NOT Platform Executors** (for specialist builders)
   - Builders do NOT open/close issues
   - Builders do NOT open/merge/close PRs
   - Builders do NOT modify repo settings
   - Authority: FM agent contract (platform actions prohibited)

**Contract Section**: Must be covered in "Maturion Builder Mindset — MANDATORY" section

**STOP Condition**: If "what builders are NOT" is not explicit → DO NOT RECRUIT

---

### 3.12 Summary Checklist: Governance Submission Obligations

**ALL of the following MUST be explicit in builder contracts:**

- [ ] 3.1 Authority hierarchy & override semantics
- [ ] 3.2 Protected paths & STOP rules
- [ ] 3.3 OPOJD (One-Prompt One-Job Doctrine) continuous execution
- [ ] 3.4 One-Time Build discipline
- [ ] 3.5 Zero Test Debt (99% = FAILURE)
- [ ] 3.6 Evidence production obligations
- [ ] 3.7 Pre-merge gate obligations (all 5 gate types)
- [ ] 3.8 Architecture-as-Law binding (mismatch → STOP + escalation)
- [ ] 3.9 Technology governance (TED / TSP awareness)
- [ ] 3.10 Escalation rules (format, triggers, destinations)
- [ ] 3.11 Prohibited builder roles ("what builders are NOT")

**IF ANY item is not explicit → DO NOT RECRUIT**

---

## 4. FM Responsibilities (Explicit)

**Purpose**: Define what FM MUST do to ensure builder recruitment is a governance act.

### 4.1 Discovering Builders ONLY from Canonical Location

**FM MUST**:
- Scan `.github/agents/` for builder contracts
- Identify files matching pattern `*-builder.md`
- Parse YAML frontmatter to extract builder metadata
- Ignore all files outside `.github/agents/`

**FM MUST NOT**:
- Scan root directory for builder contracts
- Scan custom directories for builder contracts
- Treat documentation files as builder contracts
- Treat specification files as builder contracts

**Authority**: PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md (Line 271-273)

---

### 4.2 Treating Builder Recruitment as Governance Act

**FM MUST**:
- Validate EVERY builder contract against BUILDER_CONTRACT_SCHEMA.md
- Validate ALL required YAML fields are present and valid
- Validate ALL required markdown sections are present
- Validate ALL governance submission obligations are explicit
- Refuse recruitment if ANY validation fails
- Escalate validation failures with specific diagnostics

**FM MUST NOT**:
- Recruit builders with incomplete contracts
- Recruit builders with invalid YAML
- Recruit builders missing mandatory sections
- Assume governance obligations are implicit
- Proceed with "partial compliance" or "good enough"

**Authority**: 
- BUILDER_CONTRACT_SCHEMA.md (entire document)
- BUILD_PHILOSOPHY.md (§ V - Builder Authority and Constraints)

---

### 4.3 Refusing Execution if Builder Contract is Missing or Invalid

**FM MUST**:
- Check builder contract existence BEFORE task assignment
- Check builder contract validity BEFORE task assignment
- STOP execution if builder is not recruited
- STOP execution if builder contract is invalid
- Escalate with clear diagnostics

**FM MUST NOT**:
- Assign tasks to non-existent builders
- Assign tasks to builders with invalid contracts
- Proceed with "temporary" or "draft" builder contracts
- Accept verbal or informal builder agreements

**Authority**: BUILD_PHILOSOPHY.md (§ III - Build Process prerequisites)

---

### 4.4 Updating FM Agent Contract to Reference Canonical Builder Location

**FM MUST**:
- Ensure FM agent contract (`.github/agents/ForemanApp-agent.md`) references:
  - Canonical builder location (`.github/agents/`)
  - BUILDER_CONTRACT_SCHEMA.md as validation authority
  - Builder recruitment as governance act (not documentation)
- Keep FM agent contract synchronized with governance canon

**Authority**: FM agent contract (governance alignment section)

---

### 4.5 Builder Validation Procedure (MANDATORY)

**For EVERY builder recruitment, FM MUST execute this validation sequence:**

#### Step 1: Location Validation
```
1. Check file exists at .github/agents/<builder-id>.md
2. IF NOT → STOP and escalate (non-canonical location)
```

#### Step 2: YAML Structure Validation
```
3. Parse YAML frontmatter
4. Check ALL required YAML fields present
5. Check ALL Maturion doctrine fields present
6. IF ANY missing → STOP and escalate (invalid YAML)
```

#### Step 3: Markdown Section Validation
```
7. Parse markdown body
8. Check ALL 5 Maturion doctrine sections present:
   - Maturion Builder Mindset
   - One-Time Build Discipline
   - Zero Test & Test Debt Rules
   - Gate-First Handover Protocol
   - Mandatory Enhancement Capture
9. Check ALL standard sections present
10. IF ANY missing → STOP and escalate (incomplete contract)
```

#### Step 4: Governance Submission Validation
```
11. Check ALL 11 governance submission obligations are explicit:
    - Authority hierarchy (3.1)
    - Protected paths (3.2)
    - OPOJD (3.3)
    - One-Time Build (3.4)
    - Zero Test Debt (3.5)
    - Evidence obligations (3.6)
    - Gate obligations (3.7)
    - Architecture-as-Law (3.8)
    - Technology governance (3.9)
    - Escalation rules (3.10)
    - Prohibited roles (3.11)
12. IF ANY not explicit → STOP and escalate (governance incomplete)
```

#### Step 5: Recruitment Confirmation
```
13. IF all validations pass → Mark builder as RECRUITED
14. IF any validation fails → Mark builder as NOT_RECRUITED
15. Log recruitment status to memory
```

**This validation sequence is NON-NEGOTIABLE.**

---

## 5. STOP Conditions (Non-Negotiable)

**Purpose**: Define explicit conditions under which FM MUST refuse builder recruitment or execution.

**Principle**: Better to STOP early than execute with non-compliant builders.

### 5.1 STOP: Builder Contract Missing from Canonical Location

**Condition**: 
- Builder contract does NOT exist at `.github/agents/<builder-id>.md`
- OR builder contract exists ONLY outside `.github/agents/`

**FM Action**:
```
STOP: Builder contract not found in canonical location.
- Expected: .github/agents/<builder-id>.md
- Found: <none | non-canonical-path>
- Action Required: Create builder contract in canonical location
- Governance Reference: PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md (Line 271-273)
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.2 STOP: Missing or Invalid YAML Preface

**Condition**:
- YAML frontmatter missing
- OR any required YAML field missing
- OR any Maturion doctrine field missing
- OR any YAML field has invalid value

**FM Action**:
```
STOP: Builder contract YAML preface invalid.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Missing/Invalid Fields: <list>
- Required Fields: BUILDER_CONTRACT_SCHEMA.md
- Action Required: Add/correct all required YAML fields
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.3 STOP: Missing Governance Submission Sections

**Condition**:
- Any of the 5 Maturion doctrine sections missing:
  - Maturion Builder Mindset
  - One-Time Build Discipline
  - Zero Test & Test Debt Rules
  - Gate-First Handover Protocol
  - Mandatory Enhancement Capture

**FM Action**:
```
STOP: Builder contract missing mandatory sections.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Missing Sections: <list>
- Required Sections: BUILDER_CONTRACT_SCHEMA.md (Maturion Doctrine Sections)
- Action Required: Add all missing mandatory sections
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.4 STOP: Architecture Not Bound as Law

**Condition**:
- "Architecture is law" not explicitly stated
- OR Architecture-QA mismatch handling not defined
- OR No feature addition rule not explicit

**FM Action**:
```
STOP: Architecture-as-Law binding not explicit in builder contract.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Requirement: § 3.8 Architecture-as-Law Binding
- Missing Elements: <list>
- Action Required: Add explicit architecture supremacy statements
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.5 STOP: OPOJD Not Explicitly Declared

**Condition**:
- One-Prompt One-Job Doctrine not mentioned
- OR Continuous execution mandate not explicit
- OR Assume-continue principle not stated

**FM Action**:
```
STOP: OPOJD (One-Prompt One-Job Doctrine) not explicit in builder contract.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Requirement: § 3.3 OPOJD
- Missing Elements: <list>
- Action Required: Add explicit OPOJD continuous execution mandate
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.6 STOP: Zero Test Debt Not Enforced

**Condition**:
- Zero Test Debt policy not explicit
- OR 100% pass requirement not stated
- OR "99% = FAILURE" not explicit

**FM Action**:
```
STOP: Zero Test Debt policy not explicit in builder contract.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Requirement: § 3.5 Zero Test Debt
- Missing Elements: <list>
- Action Required: Add explicit Zero Test Debt enforcement
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.7 STOP: Incomplete Gate Obligations

**Condition**:
- Any of the 5 gate types not covered:
  - Architecture Validation Gate
  - QA-to-Red Gate
  - Build-to-Green Gate
  - Zero Regression Gate
  - Memory & Evidence Gate

**FM Action**:
```
STOP: Pre-merge gate obligations incomplete in builder contract.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Requirement: § 3.7 Pre-Merge Gate Obligations
- Missing Gates: <list>
- Action Required: Add explicit binding to all 5 gate types
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.8 STOP: Prohibited Roles Not Defined

**Condition**:
- "What builders are NOT" section missing
- OR NOT generic developers not stated
- OR NOT architecture authors not stated
- OR NOT governance decision-makers not stated

**FM Action**:
```
STOP: Prohibited builder roles not explicit in builder contract.
- Builder: <builder-id>
- Location: .github/agents/<builder-id>.md
- Requirement: § 3.11 Prohibited Builder Roles
- Missing Elements: <list>
- Action Required: Add explicit "what builders are NOT" statements
- Builder Status: NOT_RECRUITED
- Execution: FORBIDDEN
```

---

### 5.9 Summary: When STOP Means STOP

**STOP means**:
- ❌ No builder recruitment
- ❌ No builder appointment
- ❌ No task assignment
- ❌ No execution delegation
- ❌ No "temporary" or "partial" recruitment

**STOP does NOT mean**:
- ❓ "We'll fix it later"
- ❓ "Close enough"
- ❓ "Most requirements are met"
- ❓ "We can proceed with warnings"

**IF any STOP condition is triggered → FM MUST refuse to proceed and escalate.**

---

## 6. Canonical References

**This document layer-down is based on the following canonical sources:**

### 6.1 Primary Governance Canon

1. **BUILD_PHILOSOPHY.md**
   - Supreme constitutional authority for all building activities
   - Defines: One-Time Build, Zero Regression, Architecture Alignment, OPOJD
   - Location: `/BUILD_PHILOSOPHY.md`

2. **BUILDER_CONTRACT_SCHEMA.md**
   - Canonical schema for builder contracts
   - Defines: Required YAML fields, Required markdown sections
   - Location: `.github/agents/BUILDER_CONTRACT_SCHEMA.md`

3. **ForemanApp-agent.md**
   - FM agent operational contract
   - Defines: FM authority, FM responsibilities, FM constraints
   - Location: `.github/agents/ForemanApp-agent.md`

4. **PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md**
   - Platform readiness canon
   - Defines: Canonical builder location (`.github/agents/`)
   - Location: `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`

### 6.2 Referenced External Canon (Not Present in FM App Repo)

**These documents were referenced in issue comments as existing in the governance repository:**

5. **GOVERNANCE_BUILDER_SUBMISSION_SURVEY.md**
   - Exhaustive survey of governance aspects builders must submit to
   - Location: `governance/canon/GOVERNANCE_BUILDER_SUBMISSION_SURVEY.md` (governance repo)
   - Status: Referenced but not present in FM app repo

6. **BUILDER_CONTRACT_BINDING_CHECKLIST.md**
   - Machine-checkable checklist for builder contract validation
   - Location: `governance/canon/BUILDER_CONTRACT_BINDING_CHECKLIST.md` (governance repo)
   - Status: Referenced but not present in FM app repo

7. **ENFORCEMENT_DESIGN_NOTE.md**
   - Enforcement design and validation tooling specification
   - Location: `governance/canon/ENFORCEMENT_DESIGN_NOTE.md` (governance repo)
   - Status: Referenced but not present in FM app repo

**Note**: While these documents are not present in the FM app repository, their requirements have been incorporated into this layer-down based on issue description and comments.

---

## 7. Compliance Verification

**FM MUST be able to answer YES to ALL of the following:**

- [ ] FM discovers builders ONLY from `.github/agents/`?
- [ ] FM validates EVERY builder contract against BUILDER_CONTRACT_SCHEMA.md?
- [ ] FM checks ALL required YAML fields before recruitment?
- [ ] FM checks ALL required markdown sections before recruitment?
- [ ] FM verifies ALL 11 governance submission obligations are explicit?
- [ ] FM refuses recruitment if ANY validation fails?
- [ ] FM escalates validation failures with specific diagnostics?
- [ ] FM treats builder recruitment as governance act (not documentation)?
- [ ] FM STOPs execution if builder contract is invalid?
- [ ] FM STOPs execution if builder is not recruited?
- [ ] FM follows the 5-step validation procedure for EVERY builder?

**IF any answer is NO → FM is NOT in compliance with governance canon.**

---

## 8. Ratchet Statement

**This document establishes the following non-regression guarantees:**

1. **Canonical Location is Immutable**
   - `.github/agents/` is the ONLY canonical location for builder contracts
   - This MUST NOT change without constitutional governance update

2. **No Implicit Governance Binding**
   - ALL governance obligations MUST be explicit in builder contracts
   - NO assumptions about "obvious" or "implied" governance rules

3. **No Partial Compliance**
   - 99% compliance = 0% compliance
   - ALL required fields and sections are MANDATORY
   - NO "close enough" or "good enough" recruitment

4. **STOP is Non-Negotiable**
   - IF any STOP condition is triggered → FM MUST refuse to proceed
   - NO context-dependent STOP bypassing
   - NO "temporary" or "emergency" STOP overrides (except Johan's explicit override)

5. **Validation is Mandatory**
   - EVERY builder recruitment MUST execute full validation sequence
   - NO shortcuts or fast-paths
   - NO "trusted" or "pre-validated" builders

**These guarantees are permanent and cannot be weakened.**

---

## 9. Document Status & Ownership

**Status**: CANONICAL INSTRUCTION (Authoritative)  
**Ownership**: Governance (maturion-foreman-governance canon)  
**Execution Ownership**: FM (maturion-foreman-office-app)  
**Version**: 1.0.0  
**Last Updated**: 2026-01-01  
**Next Review**: When governance canon updates

**Change Policy**:
- This document MAY be updated to reflect governance canon changes
- This document MUST NOT be weakened or simplified
- All changes MUST preserve or strengthen governance guarantees
- All changes MUST be traceable to governance canon updates

---

## 10. Acceptance Criteria (From Issue)

**This document satisfies the following acceptance criteria from Issue #[number]:**

✅ **No new governance canon introduced**
- This document translates existing canon, does not create new canon

✅ **No fixes performed in FM app**
- This is a specification document, not an implementation

✅ **Deliverable is explicit, unambiguous, and actionable**
- All requirements are stated explicitly
- All STOP conditions are defined clearly
- All FM obligations are actionable

✅ **FM agent cannot misinterpret builder recruitment requirements**
- Canonical location is explicit (§ 1)
- Mandatory structure is explicit (§ 2)
- Governance obligations are exhaustive (§ 3)
- FM responsibilities are explicit (§ 4)
- STOP conditions are non-negotiable (§ 5)

✅ **Document can be used verbatim to drive corrective execution**
- Section 4 defines exact FM responsibilities
- Section 5 defines exact STOP conditions
- Validation procedure is step-by-step (§ 4.5)

---

## Appendix A: Builder Contract Validation Checklist

**Use this checklist to validate ANY builder contract before recruitment:**

### Location Validation
- [ ] Contract exists at `.github/agents/<builder-id>.md`
- [ ] Contract filename matches `builder_id` in YAML
- [ ] No duplicate contracts in other locations

### YAML Frontmatter Validation
- [ ] YAML frontmatter present and parseable
- [ ] `builder_id` (string, lowercase-with-hyphens)
- [ ] `builder_type` (specialized | qa | cross-cutting)
- [ ] `version` (semver format)
- [ ] `status` (recruited | pending | deprecated)
- [ ] `capabilities` (array of strings)
- [ ] `responsibilities` (array of strings)
- [ ] `forbidden` (array of strings)
- [ ] `permissions` (object with read/write arrays)
- [ ] `recruitment_date` (YYYY-MM-DD)
- [ ] `canonical_authorities` (array, includes BUILD_PHILOSOPHY.md, build-to-green-rule.md, ForemanApp-agent.md)
- [ ] `maturion_doctrine_version` ("1.0.0")
- [ ] `handover_protocol` ("gate-first-deterministic")
- [ ] `no_debt_rules` ("zero-test-debt-mandatory")
- [ ] `evidence_requirements` ("complete-audit-trail-mandatory")

### Markdown Section Validation (Maturion Doctrine)
- [ ] ## Maturion Builder Mindset — MANDATORY
- [ ] ## One-Time Build Discipline — MANDATORY
- [ ] ## Zero Test & Test Debt Rules — MANDATORY
- [ ] ## Gate-First Handover Protocol — MANDATORY
- [ ] ## Mandatory Enhancement Capture — MANDATORY

### Markdown Section Validation (Standard)
- [ ] ## Purpose
- [ ] ## Responsibilities
- [ ] ## Capabilities
- [ ] ## Forbidden Actions
- [ ] ## Scope Boundaries
- [ ] ## Integration Points
- [ ] ## Escalation Procedures

### Governance Submission Validation
- [ ] 3.1 Authority hierarchy & override semantics explicit
- [ ] 3.2 Protected paths & STOP rules explicit
- [ ] 3.3 OPOJD continuous execution explicit
- [ ] 3.4 One-Time Build discipline explicit
- [ ] 3.5 Zero Test Debt (99% = FAILURE) explicit
- [ ] 3.6 Evidence production obligations explicit
- [ ] 3.7 Pre-merge gate obligations (all 5 gates) explicit
- [ ] 3.8 Architecture-as-Law binding explicit
- [ ] 3.9 Technology governance awareness explicit
- [ ] 3.10 Escalation rules explicit
- [ ] 3.11 Prohibited builder roles explicit

### Final Decision
- [ ] ALL validations pass → RECRUITED
- [ ] ANY validation fails → NOT_RECRUITED → ESCALATE

**IF any checkbox is unchecked → DO NOT RECRUIT**

---

## END OF DOCUMENT

**This is the authoritative layer-down of governance canon into FM builder recruitment requirements.**

**FM MUST comply with ALL requirements in this document.**

**Non-compliance = Builder recruitment is invalid = Execution is forbidden.**
