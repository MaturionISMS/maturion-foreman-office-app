# Commissioning Evidence Model

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-25

---

## Purpose

This document provides a **quick reference** for the Commissioning Evidence Model used in the Maturion FM build system.

**Primary Authority**: See `BUILD_TREE_EXECUTION_MODEL.md` (Section V) for complete specification.

---

## What is Commissioning Evidence?

**Commissioning Evidence** is the set of artifacts that prove:
- Work was completed correctly
- Quality standards were met
- Governance rules were followed
- All acceptance criteria satisfied

**Purpose**: Enable evidence-based authorization, not opinion-based approval.

---

## Evidence Categories

### 1. Architecture Evidence

**Purpose**: Prove architecture is complete and validated

**Artifacts**:
- Architecture document (Markdown)
- Component diagrams
- Data models
- API specifications
- Integration contracts

**Requirements**:
- MUST exist before build starts
- MUST be 100% complete
- MUST pass architecture validation
- MUST be frozen during build

---

### 2. QA Evidence

**Purpose**: Prove quality standards met

**Artifacts**:
- QA test suite (code)
- QA execution results (logs, JSON)
- QA-of-QA validation report
- Test coverage metrics
- DP-RED registry entries (if applicable)

**Requirements**:
- MUST show 100% pass rate
- MUST have zero test debt
- MUST include QA-of-QA validation
- MUST be frozen during build

---

### 3. Build Evidence

**Purpose**: Prove implementation completed successfully

**Artifacts**:
- PR link (GitHub)
- Code diff
- CI/CD logs
- Build artifacts
- Deployment confirmation

**Requirements**:
- MUST have PR merged
- MUST have CI passing
- MUST match architecture exactly
- MUST pass all QA tests

---

### 4. Completion Evidence

**Purpose**: Prove work meets all governance requirements

**Artifacts**:
- Evidence validation report (by Foreman)
- Foreman sign-off
- Merge confirmation
- Memory entries (decisions, learnings)

**Requirements**:
- MUST have all other evidence categories complete
- MUST have Foreman validation
- MUST have all governance checks pass

---

## Evidence Requirements by Node Type

### Task Requirements

- ✅ MUST have architecture evidence
- ✅ MUST have QA evidence (100% pass)
- ✅ MUST have build evidence (PR merged)
- ✅ MUST have completion evidence (Foreman validation)

**Cannot be COMPLETE without all evidence validated**

---

### Wave Requirements

- ✅ MUST have planning document
- ✅ MUST have all task evidence (recursive)
- ⚠️ MAY have wave-level summary report

**Cannot be COMPLETE without all task evidence validated**

---

### Program Requirements

- ✅ MUST have program charter
- ✅ MUST have all wave evidence (recursive)
- ✅ MUST have program completion report

**Cannot be COMPLETE without all wave evidence validated**

---

## Evidence Validation Rules

### Task Cannot Be COMPLETE Unless:

1. Architecture document exists and validated
2. QA suite exists and shows 100% pass
3. Zero test debt confirmed
4. PR merged to main/master
5. Evidence validation report exists
6. Foreman has signed off

### Wave Cannot Be COMPLETE Unless:

1. All tasks COMPLETE
2. All task evidence validated
3. Wave summary exists (if required)

### Program Cannot Be COMPLETE Unless:

1. All waves COMPLETE
2. All wave evidence validated
3. Program completion report created

---

## Evidence Data Model

```typescript
interface Evidence {
  id: string;
  category: 'ARCHITECTURE' | 'QA' | 'BUILD' | 'COMPLETION';
  artifact_type: string;           // 'markdown', 'json', 'pr', 'report'
  artifact_location: string;       // URL or path
  validated: boolean;
  validated_at?: string;           // ISO 8601
  validated_by?: string;           // 'Foreman', typically
  metadata?: Record<string, any>;  // Additional context
}
```

---

## Evidence in UI

When visualizing build tree:
- Show evidence count per node
- Indicate validated vs. pending
- Link to evidence artifacts
- Show validation status

**Example**:
```
Task: AI Panel  [COMPLETE] [🟢 GREEN] [100%]
  Evidence: 4/4 validated ✅
  ├─ Architecture: ai-panel-spec.md ✅
  ├─ QA: 15/15 tests passing ✅
  ├─ Build: PR#145 merged ✅
  └─ Completion: Validated by Foreman ✅
```

---

## Governance Integration

### GSR Enforcement

Evidence model enforces **Governance Supremacy Rule (GSR)**:

1. **100% QA Passing**: QA evidence MUST show 100% pass
2. **Zero Test Debt**: QA evidence MUST confirm zero skipped/incomplete tests
3. **Architecture Conformance**: Build evidence MUST match architecture
4. **Constitutional Protection**: Evidence MUST show no protected path modifications

### Build Philosophy Alignment

Evidence model enforces **Build Philosophy**:

1. **One-Time Build Correctness**: Architecture evidence required before build
2. **Zero Regression**: Build evidence includes regression test results
3. **Full Architectural Alignment**: Architecture validation required
4. **Zero Loss of Context**: All decisions captured in completion evidence
5. **Zero Ambiguity**: All evidence artifacts must be explicit and verifiable

---

## Evidence Storage

**Location**: Varies by artifact type

- Architecture: `architecture/` directory (Git)
- QA: `tests/` directory + execution logs
- Build: GitHub PR + CI artifacts
- Completion: `foreman/evidence/` directory (Git)

**Retention**: Permanent (version-controlled)

**Access**: Read-only after validation

---

## For Complete Details

See **BUILD_TREE_EXECUTION_MODEL.md (G-C8)** Section V for:
- Complete evidence category definitions
- Detailed validation rules
- Evidence API contracts
- Integration with state transitions

---

*END OF COMMISSIONING EVIDENCE MODEL QUICK REFERENCE*
