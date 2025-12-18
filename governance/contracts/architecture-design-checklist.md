# Architecture Design Checklist

**Version**: 1.1.0  
**Status**: Constitutional Authority  
**Authority**: Build Philosophy Principle #3 (Full Architectural Alignment)  
**Last Updated**: 2025-12-15

---

## I. Purpose

This checklist is **mandatory validation** before any build can proceed.

**Foreman MUST execute this checklist** before assigning build tasks to builder agents.

**If ANY item fails → Architecture is incomplete → Build cannot proceed.**

---

## II. Checklist Execution Rules

### When to Execute

- Before creating "Build to Green" instructions
- Before assigning tasks to builders
- When architecture is updated
- When new modules are added
- When integration points change

### How to Execute

1. Load architecture document
2. Verify each checklist item
3. Document pass/fail for each item
4. If ALL items pass → Architecture is complete
5. If ANY item fails → Architecture is incomplete → Fix and re-validate

### Failure Protocol

If ANY item fails:
1. **STOP** - Do not proceed with build
2. **DOCUMENT** - Note which items failed and why
3. **FIX** - Complete missing architecture sections
4. **RE-VALIDATE** - Execute checklist again
5. **PROCEED** - Only after 100% pass

---

## III. The Checklist

### Section 1: True North (Module Vision)

**Purpose**: Ensure module has clear purpose and boundaries

- [ ] **1.1** True North document exists
- [ ] **1.2** Module vision is clearly stated
- [ ] **1.3** Module purpose is unambiguous
- [ ] **1.4** Module scope is defined
- [ ] **1.5** Module boundaries are explicit
- [ ] **1.6** Alignment with ISMS True North is documented
- [ ] **1.7** Alignment with SRMF is documented (if applicable)

**Validation Questions**:
- Can someone read True North and understand what this module does?
- Are the boundaries clear (what's in, what's out)?
- Is alignment with platform vision documented?

**If ANY item unchecked** → True North is incomplete

---

### Section 2: Architecture Specification

**Purpose**: Ensure complete architectural design

- [ ] **2.1** Architecture document exists
- [ ] **2.2** All module processes are documented
- [ ] **2.3** All components are identified and described
- [ ] **2.4** All user workflows are documented
- [ ] **2.5** All business rules are explicit
- [ ] **2.6** All validation rules are defined
- [ ] **2.7** All error handling strategies are defined
- [ ] **2.8** All state management approaches are defined
- [ ] **2.9** Module boundaries are enforced in design
- [ ] **2.10** No "TBD" or "TODO" markers exist
- [ ] **2.11** No ambiguous requirements exist
- [ ] **2.12** All assumptions are documented

**Validation Questions**:
- Does architecture define HOW module works?
- Are all components described?
- Are all workflows clear?
- Could a builder implement this without guessing?

**If ANY item unchecked** → Architecture is incomplete

---

### Section 2A: Domain/Business Logic Architecture

**Purpose**: Ensure domain logic and business rules are explicitly documented

**Note**: If module has no complex domain logic (e.g., simple CRUD), mark this section as N/A with justification.

- [ ] **2A.1** Core domain concepts are defined with clear definitions
- [ ] **2A.2** Business rules are explicit and unambiguous
- [ ] **2A.3** Domain invariants (rules that must always hold) are documented
- [ ] **2A.4** Domain constraints are specified
- [ ] **2A.5** Deterministic logic is fully documented (scoring, calculations, thresholds, weightings)
- [ ] **2A.6** Domain logic formulas are specified with inputs and outputs
- [ ] **2A.7** Domain logic is separated from UI concerns
- [ ] **2A.8** Domain logic is separated from persistence concerns
- [ ] **2A.9** Domain validation rules are explicit
- [ ] **2A.10** Domain model relationships and dependencies are clear
- [ ] **2A.11** Business process flows are documented
- [ ] **2A.12** Domain-specific enums, scales, or taxonomies are fully defined

**Validation Questions**:
- Are core business rules explicit and testable?
- Can domain logic be implemented without UI or database knowledge?
- Are all calculations, scores, and thresholds fully specified?
- Could a domain expert validate the logic from this documentation?

**Examples from Existing Architectures**:
- Risk Assessment: 8 sub-engines (UE Intake, Likelihood, Impact, ALE, Control Environment, Risk Matrix, Residual Risk, Projected Risk)
- Threat Module: TTP classification, drift scoring
- Vulnerability Module: Exploitability scoring, TVRE derivation

**If ANY item unchecked** → Domain logic architecture is incomplete

---

### Section 2B: Decision & Evaluation Pipelines

**Purpose**: Ensure decision-making and evaluation processes are fully specified

**Note**: If module has no decision pipelines (e.g., simple display-only module), mark this section as N/A with justification.

- [ ] **2B.1** Decision pipeline stages are identified and documented
- [ ] **2B.2** Input requirements for each pipeline stage are specified
- [ ] **2B.3** Output contracts for each pipeline stage are specified
- [ ] **2B.4** Data transformations between stages are explicit
- [ ] **2B.5** Rule ordering and precedence is defined (which rules apply first)
- [ ] **2B.6** Deterministic steps are distinguished from heuristic steps
- [ ] **2B.7** Decision criteria and thresholds are explicit
- [ ] **2B.8** Failure modes for each stage are defined
- [ ] **2B.9** Fallback behavior is specified for each failure mode
- [ ] **2B.10** Pipeline state management is defined
- [ ] **2B.11** Auditability of decisions is ensured (can trace input → decision → output)
- [ ] **2B.12** Evidence generation at each stage is specified

**Validation Questions**:
- Can each decision stage be tested independently?
- Is it clear what happens when a stage fails?
- Can decisions be audited and explained after the fact?
- Are all inputs to decision points documented?

**Examples from Existing Architectures**:
- Risk Assessment: Threat × Vulnerability → UE → Likelihood → Impact → Inherent Risk → Controls → Residual Risk → Projected Risk
- Threat Module: Threat intake → Classification → TTP mapping → Drift analysis → Risk signal
- Control Efficacy: Control mapping → Effectiveness scoring → Coverage calculation → Gap analysis

**If ANY item unchecked** → Decision pipeline architecture is incomplete

---

### Section 3: Integration Specification

**Purpose**: Ensure all integration points are defined

- [ ] **3.1** Integration specification document exists
- [ ] **3.2** All inbound interactions are declared
- [ ] **3.3** All outbound interactions are declared
- [ ] **3.4** All events consumed are documented
- [ ] **3.5** All events produced are documented
- [ ] **3.6** All API calls made are documented
- [ ] **3.7** All API endpoints exposed are documented
- [ ] **3.8** All cross-module dependencies are explicit
- [ ] **3.9** All data contracts are defined
- [ ] **3.10** All integration error handling is defined
- [ ] **3.11** Module isolation is maintained
- [ ] **3.12** No hidden dependencies exist

**Validation Questions**:
- Are ALL ways this module communicates with others documented?
- Are data contracts clear?
- Is error handling for integrations defined?
- Can module be understood in isolation?

**If ANY item unchecked** → Integration spec is incomplete

---

### Section 4: Data Specification

**Purpose**: Ensure complete data model design

- [ ] **4.1** Database schema specification exists
- [ ] **4.2** All database tables are defined
- [ ] **4.3** All table columns are defined with types
- [ ] **4.4** All relationships are defined (foreign keys)
- [ ] **4.5** All indexes are specified
- [ ] **4.6** All constraints are defined (unique, not null, check)
- [ ] **4.7** All validation rules are defined
- [ ] **4.8** All RLS (Row Level Security) policies are specified
- [ ] **4.9** Multi-tenancy isolation is enforced
- [ ] **4.10** Data privacy requirements are defined
- [ ] **4.11** Data retention policies are defined (if applicable)
- [ ] **4.12** Migration strategy is defined

**Special Requirements (if applicable)**:
- [ ] **4.13** Special scales/enums are defined (e.g., risk scales, maturity levels)
- [ ] **4.14** Computed fields are documented
- [ ] **4.15** Trigger logic is defined (if needed)

**Validation Questions**:
- Is database schema complete and unambiguous?
- Are all data rules and constraints explicit?
- Is multi-tenancy isolation enforced?
- Can schema builder implement this exactly?

**If ANY item unchecked** → Data spec is incomplete

---

### Section 5: Frontend Specification

**Purpose**: Ensure complete UI/UX design

- [ ] **5.1** Frontend specification document exists
- [ ] **5.2** Component hierarchy is defined
- [ ] **5.3** All pages/views are listed
- [ ] **5.4** All components are described
- [ ] **5.5** Component props and state are defined
- [ ] **5.6** Wireframes or mockups exist for all views
- [ ] **5.7** User interactions are documented
- [ ] **5.8** Form validation rules are defined
- [ ] **5.9** Error states are designed
- [ ] **5.10** Loading states are designed
- [ ] **5.11** Empty states are designed
- [ ] **5.12** Responsive behavior is defined
- [ ] **5.13** Accessibility requirements are specified
- [ ] **5.14** All user roles and their views are covered
- [ ] **5.15** Navigation flows are documented

**Validation Questions**:
- Can UI builder see exactly what to build?
- Are all user interactions defined?
- Are all edge cases (loading, error, empty) designed?
- Is accessibility considered?

**If ANY item unchecked** → Frontend spec is incomplete

---

### Section 6: Backend Specification

**Purpose**: Ensure complete backend logic design (if module needs backend)

**Note**: If module is frontend-only with no backend logic, skip this section.

- [ ] **6.1** Backend specification document exists
- [ ] **6.2** All Edge Functions are defined
- [ ] **6.3** All function inputs are specified
- [ ] **6.4** All function outputs are specified
- [ ] **6.5** All business logic is documented
- [ ] **6.6** All validation logic is documented
- [ ] **6.7** All error handling is defined
- [ ] **6.8** Export specifications are defined (if applicable)
- [ ] **6.9** Watchdog logic is defined (if applicable)
- [ ] **6.10** Scheduled jobs are defined (if applicable)
- [ ] **6.11** Model routing logic is defined
- [ ] **6.12** Performance considerations are documented
- [ ] **6.13** Rate limiting is specified (if applicable)
- [ ] **6.14** Authentication requirements are clear
- [ ] **6.15** Authorization rules are explicit

**Validation Questions**:
- Are all backend functions described in detail?
- Is business logic unambiguous?
- Are error cases handled?
- Can API builder implement this without guessing?

**If ANY item unchecked** → Backend spec is incomplete

---

### Section 7: QA Specification

**Purpose**: Ensure comprehensive test coverage is planned

- [ ] **7.1** QA plan document exists
- [ ] **7.2** All architecture components are mapped to tests
- [ ] **7.3** All user workflows are covered by tests
- [ ] **7.4** All business rules are covered by tests
- [ ] **7.5** All validation rules are covered by tests
- [ ] **7.6** All error cases are covered by tests
- [ ] **7.7** All integration points are covered by tests
- [ ] **7.8** All edge cases are covered by tests
- [ ] **7.9** Test data requirements are defined
- [ ] **7.10** Test environment requirements are defined
- [ ] **7.11** Minimum coverage thresholds are specified
- [ ] **7.12** No architecture component is unmapped to tests

**Validation Questions**:
- Is there a test for EVERY architecture component?
- Are all edge cases covered?
- Is test data defined?
- Can QA builder create complete test suite from this?

**If ANY item unchecked** → QA spec is incomplete

---

### Section 8: Implementation Guide

**Purpose**: Ensure build execution can be sequenced

- [ ] **8.1** Implementation guide exists
- [ ] **8.2** Build steps are listed in order
- [ ] **8.3** Dependencies between steps are clear
- [ ] **8.4** Task breakdown is sensible
- [ ] **8.5** Each task has clear acceptance criteria
- [ ] **8.6** Estimated effort is reasonable
- [ ] **8.7** Risk areas are identified
- [ ] **8.8** Rollback strategy is defined

**Validation Questions**:
- Can Foreman sequence build tasks from this?
- Are dependencies clear?
- Is order of implementation logical?

**If ANY item unchecked** → Implementation guide is incomplete

---

### Section 9: Sprint Plan / Build Sequencing

**Purpose**: Ensure work can be distributed and tracked

- [ ] **9.1** Sprint plan or build sequence exists
- [ ] **9.2** Tasks are sequenced logically
- [ ] **9.3** Dependencies are respected in sequence
- [ ] **9.4** Critical path is identified
- [ ] **9.5** Parallel work opportunities are identified
- [ ] **9.6** Integration points are scheduled appropriately
- [ ] **9.7** Testing phases are included
- [ ] **9.8** Review/validation points are scheduled

**Validation Questions**:
- Can Foreman distribute work to builders?
- Is sequencing logical?
- Are integration points well-timed?

**If ANY item unchecked** → Sprint plan is incomplete

---

### Section 10: Compliance and Security

**Purpose**: Ensure regulatory and security requirements are met

- [ ] **10.1** Compliance requirements are identified
- [ ] **10.2** ISO 27001 controls are mapped (if applicable)
- [ ] **10.3** NIST controls are mapped (if applicable)
- [ ] **10.4** COBIT controls are mapped (if applicable)
- [ ] **10.5** Data privacy requirements are specified
- [ ] **10.6** Security controls are defined
- [ ] **10.7** Access control rules are explicit
- [ ] **10.8** Audit trail requirements are defined
- [ ] **10.9** Encryption requirements are defined (if applicable)
- [ ] **10.10** Compliance validation tests are planned

**Validation Questions**:
- Are compliance requirements clear?
- Are security controls explicit?
- Is audit trail defined?
- Can compliance be validated?

**If ANY item unchecked** → Compliance spec is incomplete

---

### Section 11: Versioning & Evolution Strategy

**Purpose**: Ensure changes can be tracked, versioned, and evolved safely

- [ ] **11.1** Initial version number is assigned (e.g., v1.0.0)
- [ ] **11.2** Versioning scheme is documented (semantic versioning recommended)
- [ ] **11.3** Version number interpretation is clear (what triggers major/minor/patch)
- [ ] **11.4** Change record template is created
- [ ] **11.5** Breaking change policy is understood and documented
- [ ] **11.6** Backward compatibility guarantees are explicitly stated
- [ ] **11.7** Backward compatibility validation approach is defined
- [ ] **11.8** Deprecation strategy is defined (if applicable)
- [ ] **11.9** Deprecation timeline and notification process is specified
- [ ] **11.10** Migration path is documented (if replacing existing functionality)
- [ ] **11.11** Migration scripts or tools are specified (if needed)
- [ ] **11.12** Impact analysis for version changes is defined
- [ ] **11.13** Version compatibility matrix is created (if multi-module)
- [ ] **11.14** Rollback procedure is documented
- [ ] **11.15** Version-specific data migration is addressed
- [ ] **11.16** API/interface version negotiation is defined (if applicable)

**Validation Questions**:
- Is it clear when to increment major, minor, or patch versions?
- Are backward compatibility guarantees explicit and testable?
- Is there a safe migration path from previous versions?
- Can changes be rolled back safely?
- How are breaking changes communicated and managed?

**If ANY item unchecked** → Versioning strategy is incomplete

---

### Section 12: Evidence & Audit Architecture

**Purpose**: Ensure auditability, traceability, and evidence generation are designed into the system

- [ ] **12.1** Evidence generation requirements are identified
- [ ] **12.2** Types of evidence to be captured are enumerated
- [ ] **12.3** Evidence formats and schemas are defined
- [ ] **12.4** Evidence storage locations are specified
- [ ] **12.5** Evidence retention policies are defined
- [ ] **12.6** Evidence access controls are specified
- [ ] **12.7** Traceability between inputs and outputs is ensured
- [ ] **12.8** Traceability between decisions and outcomes is ensured
- [ ] **12.9** Audit trail completeness is validated
- [ ] **12.10** Audit replay capability is specified (can reconstruct past states)
- [ ] **12.11** Evidence integrity is protected (tamper detection)
- [ ] **12.12** Evidence versioning is addressed (evidence changes over time)
- [ ] **12.13** Provenance tracking is specified (who/what/when/why)
- [ ] **12.14** Compliance evidence mapping is defined
- [ ] **12.15** Evidence export and reporting capabilities are specified

**Validation Questions**:
- Can every decision be traced back to its inputs?
- Can system state be reconstructed from audit logs?
- Is evidence sufficient for compliance audits?
- Are evidence generation points identified in workflows?
- Can evidence be exported in required formats?

**Examples from Existing Architectures**:
- PIT: Audit logging for all operations (entity_type, entity_id, action, user_id, organisation_id, timestamp, changes JSON)
- Risk Assessment: Evidence contracts at each pipeline stage, versioned UE/threat/vulnerability references
- Control Library: Control implementation evidence, effectiveness evidence, audit trail

**If ANY item unchecked** → Evidence and audit architecture is incomplete

---

## IV. Validation Reporting

### Checklist Report Format

```markdown
# Architecture Validation Report

## Module
<module-name>

## Architecture Document
<path-to-architecture-doc>

## Validation Date
<ISO 8601 timestamp>

## Validated By
Maturion Foreman

## Overall Status
<COMPLETE | INCOMPLETE>

## Section Results

### Section 1: True North
Status: <PASS | FAIL>
Items Passed: X/7
Failed Items: <list if any>

### Section 2: Architecture Specification
Status: <PASS | FAIL>
Items Passed: X/12
Failed Items: <list if any>

### Section 2A: Domain/Business Logic Architecture
Status: <PASS | FAIL | N/A>
Items Passed: X/12
Failed Items: <list if any>
Notes: <If N/A, provide justification>

### Section 2B: Decision & Evaluation Pipelines
Status: <PASS | FAIL | N/A>
Items Passed: X/12
Failed Items: <list if any>
Notes: <If N/A, provide justification>

### Section 3: Integration Specification
Status: <PASS | FAIL>
Items Passed: X/12
Failed Items: <list if any>

### Section 4: Data Specification
Status: <PASS | FAIL>
Items Passed: X/15
Failed Items: <list if any>

### Section 5: Frontend Specification
Status: <PASS | FAIL>
Items Passed: X/15
Failed Items: <list if any>

### Section 6: Backend Specification
Status: <PASS | FAIL | N/A>
Items Passed: X/15
Failed Items: <list if any>

### Section 7: QA Specification
Status: <PASS | FAIL>
Items Passed: X/12
Failed Items: <list if any>

### Section 8: Implementation Guide
Status: <PASS | FAIL>
Items Passed: X/8
Failed Items: <list if any>

### Section 9: Sprint Plan
Status: <PASS | FAIL>
Items Passed: X/8
Failed Items: <list if any>

### Section 10: Compliance and Security
Status: <PASS | FAIL>
Items Passed: X/10
Failed Items: <list if any>

### Section 11: Versioning & Evolution Strategy
Status: <PASS | FAIL>
Items Passed: X/16
Failed Items: <list if any>

### Section 12: Evidence & Audit Architecture
Status: <PASS | FAIL>
Items Passed: X/15
Failed Items: <list if any>

## Final Determination

- Total Items: X
- Items Passed: Y
- Items Failed: Z
- Pass Rate: Y/X = XX%

**BUILD READINESS**: <READY | NOT READY>

## Action Required

<If NOT READY, list what must be completed>

## Approver
Maturion Foreman

## Timestamp
<ISO 8601 timestamp>
```

---

## V. Integration with Build Philosophy

Architecture Design Checklist implements Build Philosophy Principle #1: **One-Time Build Correctness**

**Ensures**:
- Architecture is 100% complete before build
- All requirements are unambiguous
- No guessing required by builders
- First build attempt is correct

**Hierarchy**:
```
BUILD_PHILOSOPHY.md (Principle #1)
    ↓
architecture-design-checklist.md (This Document)
    ↓
Architecture Validation (Enforcement)
```

---

## VI. Version and Authority

**Version**: 1.1.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority (Build Philosophy Implementation)  
**Precedence**: Mandatory pre-build validation  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman

**Changelog**:
- 1.1.0 (2025-12-15): **Critical Structural Extension**
  - Added Section 2A: Domain/Business Logic Architecture (12 items)
  - Added Section 2B: Decision & Evaluation Pipelines (12 items)
  - Extended Section 11: Versioning & Evolution Strategy (16 items, expanded from 7)
  - Added Section 12: Evidence & Audit Architecture (15 items)
  - **Rationale**: Aligns checklist with existing mature architectures (ERM, Risk Assessment, Threat, Vulnerability) that include domain logic, decision pipelines, comprehensive versioning, and evidence generation
  - **Impact**: Closes structural gaps identified during governance review; prevents architectures from passing validation while omitting critical dimensions
- 1.0.0 (2025-12-15): Initial Architecture Design Checklist

---

## VII. Summary: The Commitment

Architecture Design Checklist ensures:

1. ✅ **Complete Architecture** - All sections defined, including domain logic and decision pipelines
2. ✅ **Zero Ambiguity** - All requirements clear, testable, and enforceable
3. ✅ **Full Coverage** - All aspects addressed: domain, decisions, versioning, evidence, and audit
4. ✅ **Build Readiness** - Builders can execute without guessing
5. ✅ **Governance Alignment** - Aligns with mature architectures across the ISMS ecosystem

**Architecture must be perfect before building begins.**  
**This checklist ensures it.**

**Total Checklist Items**: ~175+ validation points across 14 sections (including N/A options for 2A, 2B, and Section 6)

---

*END OF ARCHITECTURE DESIGN CHECKLIST*
