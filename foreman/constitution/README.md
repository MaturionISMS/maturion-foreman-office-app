# Constitutional Documents Index

**Version**: 1.0.0  
**Last Updated**: 2025-12-15  
**Status**: Active and Enforced

---

## I. Supreme Constitutional Authority

### BUILD_PHILOSOPHY.md (Root Level)

**Path**: `/BUILD_PHILOSOPHY.md`  
**Authority**: Supreme constitutional authority for all building  
**Precedence**: Highest (overrides all documents except Owner Override)

**Defines**:
- The Five Core Principles
- The Sacred Build Workflow (Architecture → Red QA → Build to Green → Validation → Merge)
- Governance Supremacy Rule (GSR) foundation
- Quality Integrity Contract (QIC) foundation
- Zero Test Debt principle
- One-Prompt One-Job Doctrine (OPOJD)
- Protected paths
- Evidence requirements

**All agents and processes MUST conform to this document.**

---

## II. Agent Constitutional Contracts

### Foreman Agent Contract

**Path**: `.github/foreman/agent-contract.md`  
**Authority**: Constitutional authority for Foreman  
**Precedence**: Second only to BUILD_PHILOSOPHY.md

**Defines**:
- Foreman's identity and authority
- Core responsibilities (Architecture, QA, Builders, Governance, Memory, Compliance, Runtime)
- Pre-build validation protocol (MANDATORY)
- Builder instruction format
- Governance enforcement protocol
- Protected paths enforcement
- Evidence requirements
- Owner override acknowledgment

### Foreman Agent Definition

**Path**: `.github/agents/foreman.agent.md`  
**Authority**: Agent metadata and activation definition  
**Precedence**: Agent configuration level

**Defines**:
- Agent metadata (name, role, model, temperature)
- Authority level and scope
- Constraints and responsibilities
- Protected paths
- Escalation triggers
- Activation and version info

### Builder Agent Contract

**Path**: `.github/agents/PartPulse-agent.md` (Currently named, will be standardized)  
**Future**: May create separate contracts per builder type  
**Authority**: Constitutional authority for builders  
**Precedence**: Builders must follow this contract

**Defines**:
- Builder identity and purpose
- Build to Green protocol (ABSOLUTE)
- Pre-build validation (MANDATORY)
- Build execution process
- Final validation requirements
- Governance enforcement
- Forbidden actions
- Evidence requirements

---

## III. Governance Constitutional Rules

### Governance Supremacy Rule (GSR)

**Path**: `foreman/governance/governance-supremacy-rule.md`  
**Authority**: Constitutional authority (Build Philosophy implementation)  
**Precedence**: Enforceable at all levels

**Defines**:
- The Four Pillars of Governance Supremacy
  1. 100% QA Passing is ABSOLUTE
  2. Zero Test Debt is MANDATORY
  3. Architecture Conformance is REQUIRED
  4. Constitutional File Protection
- Governance violation response protocol
- Enforcement mechanisms (3 levels)
- Appeals and overrides
- Compliance and auditability

### Zero Test Debt Constitutional Rule

**Path**: `foreman/governance/zero-test-debt-constitutional-rule.md`  
**Authority**: Constitutional authority (GSR implementation)  
**Precedence**: Mandatory enforcement

**Defines**:
- Definition of test debt (all 7 forms)
- Zero Test Debt enforcement protocol
- Detection, fixing, and verification phases
- Prevention strategies
- Common objections and responses
- Test debt vs. test coverage
- Escalation procedures
- Owner override conditions

---

## IV. Builder Operational Rules

### Build to Green Rule

**Path**: `foreman/builder-specs/build-to-green-rule.md`  
**Authority**: Constitutional authority for builders  
**Precedence**: Builders MUST follow this rule

**Defines**:
- The ONLY instruction format (Build to Green)
- Pre-build validation (MANDATORY, 4 checks)
- Build execution process (9 steps)
- Final validation requirements (4 categories)
- Completion reporting format
- Forbidden actions (8 prohibitions)
- Integration with Build Philosophy

---

## V. Quality Constitutional Standards

### Quality Integrity Contract (QIC)

**Path**: `foreman/qa/quality-integrity-contract.md`  
**Authority**: Constitutional authority (Build Philosophy + GSR)  
**Precedence**: Enforceable at all quality gates

**Defines**:
- The Seven Quality Integrity Standards
  1. Build Integrity
  2. Lint Integrity
  3. Runtime Integrity
  4. Type Integrity
  5. Test Integrity
  6. Interface Integrity
  7. Integration Integrity
- Quality violation response protocol
- Quality gates (4 enforcement points)
- Quality metrics and reporting
- Owner override conditions

---

## VI. Architecture Constitutional Standards

### Architecture Design Checklist

**Path**: `foreman/constitution/architecture-design-checklist.md`  
**Authority**: Constitutional authority (Build Philosophy Principle #1)  
**Precedence**: Mandatory pre-build validation

**Defines**:
- Complete architecture validation checklist (11 sections)
  1. True North (Module Vision)
  2. Architecture Specification
  3. Integration Specification
  4. Data Specification
  5. Frontend Specification
  6. Backend Specification
  7. QA Specification
  8. Implementation Guide
  9. Sprint Plan / Build Sequencing
  10. Compliance and Security
  11. Change Management and Versioning
- Checklist execution rules
- Validation reporting format
- Build readiness determination

### Architecture Validation Checklist (Legacy)

**Path**: `foreman/architecture-validation-checklist.md`  
**Status**: May be superseded by architecture-design-checklist.md  
**Note**: Review for consolidation or retirement

---

## VII. Supporting Constitutional Documents

### Identity and Roles

**Paths**:
- `foreman/identity.md` - Foreman identity specification
- `foreman/roles-and-duties.md` - Foreman responsibilities

**Authority**: Foundational identity documents  
**Precedence**: Reference documents

**Define**:
- Who Foreman is (and is not)
- Core purpose and guarantees
- Permanent Memory Mandate
- Governance, oversight, runtime, and builder coordination responsibilities

### Memory Model

**Path**: `foreman/memory-model.md`  
**Authority**: Constitutional requirement (Build Philosophy Principle #4)  
**Precedence**: Mandatory infrastructure

**Defines**:
- Memory as mandatory governance subsystem
- Memory loading requirements
- Memory writing requirements
- Memory as build readiness precondition
- Memory survival guarantees

### Privacy Guardrails

**Path**: `foreman/privacy-guardrails.md`  
**Authority**: Constitutional requirement  
**Precedence**: Mandatory enforcement

**Defines**:
- Strict tenant isolation
- Data access restrictions
- Privacy requirements
- Multi-tenancy enforcement

### QA Governance

**Path**: `foreman/qa-governance.md`  
**Authority**: QA constitutional requirements  
**Precedence**: Mandatory enforcement

**Defines**:
- Levels of QA (Builder, Foreman, Human)
- Memory Fabric integration with QA
- QA readiness requirements

### Other QA Documents

**Paths**:
- `foreman/qa-minimum-coverage-requirements.md`
- `foreman/qa-of-qa.md`
- `foreman/qa-of-qa-validation-checklist.md`

**Authority**: QA operational standards  
**Status**: Review for consolidation into QIC or separate governance docs

---

## VIII. Evidence and Documentation

### Evidence Templates

**Path**: `foreman/evidence/templates/`

**Templates**:
1. `build-initiation.template.json` - Build start evidence
2. `validation-results.template.json` - Pre-build validation
3. `iteration.template.json` - Build iteration evidence
4. `completion-report.template.md` - Build completion report

**Purpose**: Standardized evidence collection for all builds

### Evidence Storage

**Path**: `foreman/evidence/builds/<task-id>/`

**Structure**:
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

## IX. Protected Paths (Constitutional Protection)

These paths are **constitutionally protected** and MUST NEVER be modified without CS2 approval:

```
.github/workflows/                              # CI/CD workflows
.github/foreman/agent-contract.md               # Foreman constitution
.github/agents/foreman.agent.md                 # Foreman agent definition
BUILD_PHILOSOPHY.md                             # Build Philosophy (supreme authority)
foreman/constitution/                           # Constitutional documents
foreman/architecture-design-checklist.md        # Architecture validation (may move to constitution/)
foreman/builder-specs/build-to-green-rule.md    # Builder protocol
foreman/governance/                             # Governance rules
docs/governance/                                # Governance documentation
maturion/philosophy-tree.md                     # Platform ontology (if exists)
```

**Modification requires**:
- STOP immediately
- Escalate to Foreman or Johan
- CS2 Architecture Approval Workflow
- Owner (Johan) approval
- Documentation of change rationale

---

## X. Document Hierarchy and Precedence

### Precedence Order (Highest to Lowest)

1. **Johan (Owner Override)** - Temporary, explicit overrides
2. **BUILD_PHILOSOPHY.md** - Supreme constitutional authority
3. **Foreman Agent Contract** - Governance authority
4. **Constitutional Rules** (GSR, Zero Test Debt, Build to Green, QIC, Architecture Checklist)
5. **Agent Definitions** - Agent-level configuration
6. **Operational Documents** - Implementation guidance
7. **Templates and Tools** - Supporting materials

### Conflict Resolution

If documents conflict:
1. Higher precedence document wins
2. Escalate to Foreman for interpretation
3. Escalate to Johan if Foreman cannot resolve
4. Update lower precedence document to align

---

## XI. Change Management

### How to Modify Constitutional Documents

**Process**:
1. Identify need for change
2. Document rationale
3. Escalate to Johan for approval
4. If approved, follow CS2 workflow
5. Update document with version increment
6. Update changelog
7. Notify all affected parties
8. Update this index

**Version Control**:
- All changes tracked in git
- Version numbers in documents
- Changelog in each document
- Update date in header

### Document Review Cycle

**Frequency**: Quarterly or as needed  
**Reviewer**: Johan + Foreman  
**Purpose**: Ensure accuracy, completeness, and effectiveness

---

## XII. Quick Reference

### For Foreman

**Before ANY build, check**:
1. ✅ BUILD_PHILOSOPHY.md - Supreme authority
2. ✅ .github/foreman/agent-contract.md - Your contract
3. ✅ foreman/constitution/architecture-design-checklist.md - Architecture validation
4. ✅ foreman/governance/governance-supremacy-rule.md - GSR enforcement
5. ✅ foreman/governance/zero-test-debt-constitutional-rule.md - Test debt rules
6. ✅ foreman/qa/quality-integrity-contract.md - Quality standards

### For Builders

**Before accepting ANY task, check**:
1. ✅ BUILD_PHILOSOPHY.md - Supreme authority
2. ✅ .github/agents/PartPulse-agent.md - Your contract (or specific builder contract)
3. ✅ foreman/builder-specs/build-to-green-rule.md - Your protocol
4. ✅ foreman/governance/governance-supremacy-rule.md - Rules you must follow
5. ✅ foreman/governance/zero-test-debt-constitutional-rule.md - Test debt prohibition

### For Humans (Johan, Developers)

**Understanding governance**:
1. ✅ BUILD_PHILOSOPHY.md - Start here
2. ✅ This index (constitution/README.md) - Overview
3. ✅ .github/foreman/agent-contract.md - How Foreman operates
4. ✅ Specific documents as needed

---

## XIII. Version and Status

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Maintainer**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial constitutional documents index

---

## XIV. Summary

This repository contains **complete governance structure** for the Maturion ISMS ecosystem:

- ✅ Supreme constitutional authority (BUILD_PHILOSOPHY.md)
- ✅ Agent contracts (Foreman, Builders)
- ✅ Governance rules (GSR, Zero Test Debt)
- ✅ Builder protocols (Build to Green)
- ✅ Quality standards (QIC)
- ✅ Architecture validation (Design Checklist)
- ✅ Evidence templates and storage
- ✅ Protected path enforcement

**All pieces in place for perfect, governed, auditable builds.**

---

*END OF CONSTITUTIONAL DOCUMENTS INDEX*
