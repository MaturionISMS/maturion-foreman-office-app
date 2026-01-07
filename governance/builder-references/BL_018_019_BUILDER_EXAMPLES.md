# BL-018/BL-019 QA-Catalog-Alignment: Builder Examples

## Purpose

This document provides **detailed examples** for builders responding to BL-018/BL-019 precondition failures.

**Authority**: Extracted from builder agent contracts per Issue #447/#448 (prompt size compliance)  
**Status**: ACTIVE - Referenced by all builder agent contracts

---

## Example: Correct Builder Response to Missing Preconditions

### Scenario

Builder appointed to **Subwave 2.3 (System Optimizations)**, QA range **QA-341 to QA-350**

### Builder Discovery

During appointment verification, builder discovers:
- QA_CATALOG.md defines QA-341 to QA-350 as **"Analytics and Cross-Module Failure Modes"**
- Subwave description says **"System Optimizations Phase 1 (Caching, Query Optimization)"**
- **Semantic mismatch detected** ❌

### Correct Builder Response

```
BLOCKED: QA-Catalog-Alignment Gate Precondition Failure

I have discovered that the QA-Catalog-Alignment Gate preconditions are NOT met for this appointment:

**Issue**: Semantic mismatch between subwave scope and QA catalog allocation

**Evidence**:
- Subwave Description: "System Optimizations Phase 1 (Caching, Query Optimization)"
- QA Range Assigned: QA-341 to QA-350
- QA Catalog Actual: "Analytics and Cross-Module Failure Modes"

**QA Catalog Verification**: QA_CATALOG.md lines 545-554

**Conclusion**: QA range QA-341 to QA-350 does NOT semantically match System Optimizations scope.

**Builder Action**: STOPPED work, declaring BLOCKED per BL-018/BL-019 governance.

**Escalation**: @Foreman - Please correct QA range assignment or extend QA_CATALOG.md with System Optimizations entries.

I am awaiting FM structural correction before proceeding.
```

### What Builder Did Correctly ✅

- ✅ Verified QA catalog before starting implementation
- ✅ Detected semantic mismatch
- ✅ STOPPED immediately (did not attempt implementation)
- ✅ Declared BLOCKED with evidence
- ✅ Escalated to FM with specific gap description
- ✅ Waited for FM correction

### What Builder Did NOT Do ✅ (correct prohibitions)

- ❌ Did not "invent" QA catalog entries
- ❌ Did not proceed despite mismatch
- ❌ Did not assume FM would fix later
- ❌ Did not attempt to implement without foundation

---

## Example: Correct Builder Response to Missing QA-to-Red Tests

### Scenario

Builder appointed to **Subwave 2.4 (Data Export)**

### Builder Discovery

During appointment verification:
- QA_CATALOG.md defines QA-360 to QA-365 as "Data Export Workflow"
- Architecture exists and is frozen
- **QA-to-Red tests MISSING** for QA-362, QA-364

### Correct Builder Response

```
BLOCKED: QA-to-Red Foundation Incomplete

I have discovered missing QA-to-Red tests for assigned QA range:

**QA Range Assigned**: QA-360 to QA-365
**Missing Tests**:
- QA-362: Export Format Validation
- QA-364: Export Permissions Check

**Catalog Verification**: QA_CATALOG.md lines 580-585
**Test Location Expected**: tests/qa/data-export/

**Builder Action**: STOPPED work per BL-018/BL-019 governance. Cannot execute Build-to-Green without RED test foundation.

**Escalation**: @Foreman - Please create missing QA-to-Red tests OR reassign QA range.

I am awaiting FM structural correction before proceeding.
```

### Key Points

- Builder detected missing foundation **before** starting work
- Builder did NOT attempt to create missing tests
- Builder escalated with specific evidence
- Builder waited for FM correction

---

## Anti-Pattern: Incorrect Builder Response (DO NOT DO THIS)

### ❌ WRONG Response Example

```
I noticed QA-362 and QA-364 tests are missing. I'll create them quickly and then proceed with implementation.
```

**Why This Is Wrong**:
- Builder has NO AUTHORITY to create QA-to-Red tests outside explicit appointment
- Violates BL-018/BL-019 precondition verification
- Bypasses QA-Catalog-Alignment Gate
- Creates technical debt and governance violations

### ✅ CORRECT Response

```
BLOCKED: Missing QA-to-Red foundation. Escalating to FM for structural correction.
```

---

## Constitutional Grounding

**Governance Authority**:
- Governance PR #877: BL-018/BL-019 Canonization
- `governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md`
- `governance/specs/BL_FORWARD_SCAN_OBLIGATION_SPEC.md`

**FM Agent Contract Integration**:
- `.github/agents/ForemanApp-agent.md` Section XIV.G
- `.github/agents/ForemanApp-agent.md` Section XV
- `.github/agents/ForemanApp-agent.md` Section XVI

---

**Last Updated**: 2026-01-07  
**Extracted From**: Builder agent contracts (qa-builder, api-builder, schema-builder, ui-builder, integration-builder)
