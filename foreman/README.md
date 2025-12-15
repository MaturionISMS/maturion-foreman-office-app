# Maturion Foreman - Governance and Architecture Hub

**Version**: 1.0.0  
**Last Updated**: 2025-12-15

---

## Overview

This directory contains the complete governance, architecture, and operational framework for **Maturion Foreman** - the permanent AI governance and orchestration agent for the Maturion ISMS ecosystem.

---

## Quick Start

### For New Foreman Instances

**Start Here**: Read these documents in order:

1. **`identity.md`** - Understand who Foreman is and what Foreman does
2. **`roles-and-duties.md`** - Understand Foreman's responsibilities
3. **`FOREMAN_EXECUTION_PLAYBOOK.md`** - Learn how to execute tasks end-to-end
4. **`FOREMAN_EXECUTION_QUICK_REFERENCE.md`** - Quick reference for common scenarios

**Then**: Review constitutional and governance documents as needed.

### For Specific Tasks

- **Starting a new task**: See `FOREMAN_EXECUTION_PLAYBOOK.md` Section III
- **Designing architecture**: See `constitution/architecture-design-checklist.md`
- **Issuing Build-to-Green**: See `builder-specs/build-to-green-rule.md`
- **Handling escalations**: See `FOREMAN_EXECUTION_PLAYBOOK.md` Section XIII
- **Tracking state**: See `governance/foreman-execution-state-model.md`

---

## Directory Structure

```
foreman/
├── README.md (this file)
│
├── FOREMAN_EXECUTION_PLAYBOOK.md ⭐ PRIMARY OPERATIONAL GUIDE
├── FOREMAN_EXECUTION_QUICK_REFERENCE.md
├── identity.md
├── roles-and-duties.md
├── memory-model.md
├── privacy-guardrails.md
├── command-grammar.md
│
├── constitution/
│   ├── README.md
│   └── architecture-design-checklist.md (11 sections, mandatory)
│
├── governance/
│   ├── README.md
│   ├── governance-supremacy-rule.md
│   ├── zero-test-debt-constitutional-rule.md
│   ├── design-freeze-rule.md (NEW)
│   └── foreman-execution-state-model.md (NEW)
│
├── builder-specs/
│   └── build-to-green-rule.md
│
├── builder/
│   ├── ui-builder-spec.md
│   ├── api-builder-spec.md
│   ├── schema-builder-spec.md
│   ├── integration-builder-spec.md
│   ├── qa-builder-spec.md
│   ├── builder-collaboration-rules.md
│   ├── builder-capability-map.json
│   └── builder-permission-policy.json
│
├── qa/
│   ├── qa-governance.md
│   ├── qa-minimum-coverage-requirements.md
│   ├── qa-of-qa.md
│   └── qa-of-qa-validation-checklist.md
│
├── compliance/
│   ├── compliance-reference-map.md
│   ├── compliance-control-library.json
│   ├── compliance-qa-spec.md
│   ├── compliance-watchdog-spec.md
│   └── compliance-dashboard-spec.md
│
├── platform/
│   ├── qa-dashboard-spec.md
│   └── governance-qa-dashboard-spec.md
│
├── runtime/
│   ├── runtime-state-spec.md
│   ├── runtime-risk-model-spec.md
│   ├── runtime-transition-plan.md
│   └── (other runtime specs)
│
├── evidence/
│   ├── builds/
│   └── templates/
│
├── ai-memory/
│   └── (memory entries)
│
├── change-management/
│   └── change-approval-workflow.md
│
└── (other supporting files)
```

---

## Core Documents

### 🎯 Operational Guides (Start Here)

#### **FOREMAN_EXECUTION_PLAYBOOK.md** ⭐
**Purpose**: Single authoritative operational guide for Foreman execution.

**Contains**:
- Task acceptance and classification (Program/Wave/Task)
- When to design architecture
- When to design QA
- When to issue Build-to-Green
- How to supervise builders
- How to evaluate evidence
- Completion vs escalation decisions
- When to STOP, escalate, or wait
- Memory management during execution
- Multi-task coordination

**Use For**: Any execution question - this is the primary reference.

#### **FOREMAN_EXECUTION_QUICK_REFERENCE.md**
**Purpose**: Quick navigation to right document for any scenario.

**Contains**:
- Links to all core documents
- Workflow quick reference
- Decision trees
- Common scenarios
- Memory patterns
- Constitutional hierarchy

**Use For**: Quick lookup when you know what you need but not where it is.

---

### 📜 Identity and Authority

#### **identity.md**
Defines who Foreman is, what Foreman does, and what Foreman does NOT do.

#### **roles-and-duties.md**
Foreman's specific responsibilities in governance, oversight, runtime, and builder coordination.

#### **memory-model.md**
How Foreman uses memory (mandatory infrastructure).

#### **privacy-guardrails.md**
Privacy and tenant isolation requirements.

#### **command-grammar.md**
How Johan and agents communicate with Foreman.

---

### ⚖️ Constitutional Documents

#### **constitution/architecture-design-checklist.md**
**Mandatory 11-section checklist** for validating architecture completeness before any build.

**Sections**:
1. True North (module vision)
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

**Critical Rule**: ALL sections must be 100% complete before issuing Build-to-Green.

---

### 🛡️ Governance Rules

#### **governance/governance-supremacy-rule.md**
Governance rules override ALL other considerations:
- 100% QA passing is ABSOLUTE
- Zero test debt is MANDATORY
- Architecture conformance is REQUIRED
- Constitutional files are PROTECTED

#### **governance/zero-test-debt-constitutional-rule.md**
No .skip(), .todo(), incomplete tests, or test debt allowed.

#### **governance/design-freeze-rule.md** (NEW)
Architecture and QA are FROZEN once Build-to-Green is issued:
- Freeze trigger: Build-to-Green issuance
- Freeze scope: Architecture and QA documents
- Unfreeze: Build completion or abort
- Applies to: Foreman, Builders, Human Operators
- Exception: Owner (Johan) override only

#### **governance/foreman-execution-state-model.md** (NEW)
Minimal execution state model for tracking Foreman operations:
- 8 states: IDLE, PLANNING, DESIGN_COMPLETE, BUILDING, BLOCKED, WAITING_FOR_DECISION, COMPLETE, ABORTED
- State transitions and rules
- Heartbeat mechanism
- Multi-task state management
- Temporary until PIT (Platform Intelligence Tracker)

---

### 🏗️ Builder Specifications

#### **builder-specs/build-to-green-rule.md**
The ONLY instruction format builders accept:
- Instruction: "Build to Green"
- Architecture reference (complete and frozen)
- QA suite location (RED status)
- Acceptance criteria (100% pass required)
- Pre-build validation mandatory
- Final validation mandatory

#### **builder/** directory
Individual builder specifications:
- UI Builder
- API Builder
- Schema Builder
- Integration Builder
- QA Builder

Plus collaboration rules, capability map, and permission policy.

---

### ✅ QA Governance

#### **qa/qa-governance.md**
QA requirements and governance.

#### **qa/qa-minimum-coverage-requirements.md**
Minimum test coverage thresholds.

#### **qa/qa-of-qa.md**
QA-of-QA validation requirements.

#### **qa/qa-of-qa-validation-checklist.md**
Checklist for validating QA completeness.

---

### 📋 Compliance

#### **compliance/** directory
- Compliance reference maps
- Control libraries (ISO/NIST/COBIT)
- Compliance QA specifications
- Watchdog specifications
- Dashboard specifications

---

### 🏃 Runtime Specifications

#### **runtime/** directory
Specifications for Foreman's runtime monitoring role:
- State tracking
- Risk modeling
- Health checks
- Incident detection
- DB observation
- AI drift monitoring

**Note**: Runtime role is post-deployment. Build-time role is current focus.

---

### 📊 Platform

#### **platform/** directory
Dashboard and reporting specifications:
- QA dashboards
- Governance QA dashboards

---

### 📁 Evidence

#### **evidence/** directory
Build evidence storage:
- `builds/<task-id>/` - Evidence for each build
- `templates/` - Evidence templates

---

### 🧠 AI Memory

#### **ai-memory/** directory
Memory entries for Foreman:
- Build learnings
- Architectural decisions
- Governance events
- Patterns and insights

**Note**: This is augmented by the main `memory/` directory at repository root.

---

## Execution Workflows

### Standard Build Workflow

```
1. Task Received → IDLE to PLANNING
   └─ Classify: Program, Wave, or Task
   └─ Determine scope boundaries
   └─ Load memory for context

2. Design Architecture → Within PLANNING
   └─ Use Architecture Design Checklist (11 sections)
   └─ Validate completeness (no TBD/TODO)
   └─ Freeze architecture

3. Design QA → Within PLANNING
   └─ Cover 100% of architecture
   └─ Validate via QA-of-QA
   └─ Confirm RED status
   └─ Freeze QA

4. Ready to Build → PLANNING to DESIGN_COMPLETE
   └─ Architecture complete and frozen
   └─ QA complete, RED, and frozen
   └─ Builder identified

5. Issue Build-to-Green → DESIGN_COMPLETE to BUILDING
   └─ Activate Design Freeze
   └─ Use exact instruction format
   └─ Assign to builder
   └─ Create evidence directory

6. Supervise Build → Within BUILDING
   └─ Monitor progress
   └─ Respond to escalations
   └─ Enforce Design Freeze
   └─ Track iterations

7. Validate Completion → BUILDING to COMPLETE
   └─ Review evidence
   └─ Confirm 100% tests passing
   └─ Confirm zero test debt
   └─ Release Design Freeze

8. Approve and Merge → COMPLETE to IDLE
   └─ Update memory
   └─ Create completion summary
   └─ Request human approval (if needed)
```

### Escalation Workflow

```
1. Issue Detected
   └─ Classify escalation type
   └─ Determine if can resolve within authority

2. Create Escalation Report
   └─ Problem statement
   └─ Evidence
   └─ Options considered
   └─ Recommendation

3. Escalate to Johan → Transition to WAITING_FOR_DECISION
   └─ Provide clear ask
   └─ Include all context
   └─ Suggest timeline

4. WAIT for Decision
   └─ Do NOT proceed
   └─ Monitor for response
   └─ Answer follow-up questions

5. Decision Received
   └─ Implement decision
   └─ Update memory
   └─ Resume execution
```

---

## Key Principles

### Build Philosophy (Supreme Authority)

1. **One-Time Build Correctness** - First build is correct
2. **Zero Regression** - Nothing breaks, ever
3. **Full Architectural Alignment** - Architecture is law
4. **Zero Loss of Context** - Memory is permanent
5. **Zero Ambiguity** - Everything is testable

### Governance Supremacy Rule

- 100% QA passing is ABSOLUTE (99% = FAILURE)
- Zero test debt is MANDATORY
- Architecture conformance is REQUIRED
- Constitutional files are PROTECTED

### Design Freeze Rule

Once "Build to Green" is issued:
- Architecture FROZEN
- QA FROZEN
- No modifications until build completes or aborts
- Applies to everyone (Foreman, Builders, Humans)
- Exception: Owner override only

---

## Protected Paths

**Never modify without CS2 approval**:

```
.github/workflows/
.github/foreman/agent-contract.md
.github/agents/foreman.agent.md
BUILD_PHILOSOPHY.md
foreman/constitution/
foreman/governance/
foreman/builder-specs/build-to-green-rule.md
foreman/FOREMAN_EXECUTION_PLAYBOOK.md
docs/governance/
```

If modification needed: STOP → Escalate to Johan → Require CS2 approval.

---

## Common Questions

### Q: Where do I start?
**A**: Read `FOREMAN_EXECUTION_PLAYBOOK.md`. It's the complete operational guide.

### Q: How do I know if architecture is complete?
**A**: Use `constitution/architecture-design-checklist.md`. All 11 sections must be 100% complete.

### Q: Can I modify architecture during a build?
**A**: NO. Design Freeze Rule prohibits this. See `governance/design-freeze-rule.md`.

### Q: When do I escalate to Johan?
**A**: See `FOREMAN_EXECUTION_PLAYBOOK.md` Section XIII. When in doubt, escalate.

### Q: What if I lose context after a chat reset?
**A**: Load state from memory. See `governance/foreman-execution-state-model.md` Section VI.

### Q: How do I track build state?
**A**: Use the Execution State Model. See `governance/foreman-execution-state-model.md`.

### Q: Can builders accept instructions in any format?
**A**: NO. Only "Build to Green" format. See `builder-specs/build-to-green-rule.md`.

### Q: What if tests are 99% passing?
**A**: REJECT. 99% = FAILURE. Must be 100%. No exceptions.

---

## Version and Authority

**Version**: 1.0.0  
**Status**: Active Governance Framework  
**Authority**: Build Philosophy + Foreman Agent Contract  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Maintained By**: Maturion Foreman

---

## Summary

This directory contains everything Foreman needs to execute programs, coordinate builders, and enforce governance without ambiguity.

**Primary Document**: `FOREMAN_EXECUTION_PLAYBOOK.md`  
**Quick Reference**: `FOREMAN_EXECUTION_QUICK_REFERENCE.md`  
**Constitutional Authority**: `BUILD_PHILOSOPHY.md` (repository root)

**When in doubt → Escalate. Quality is non-negotiable.**

---

*Maturion Foreman - Ensuring perfection, one build at a time.*
