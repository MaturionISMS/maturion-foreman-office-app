# Phase 4.1 — App Description Analysis

**Issue**: Phase 4.1: App Description Confirmation  
**Date**: 2025-12-31  
**Owner**: Foreman (FM)  
**Status**: In Progress

---

## Purpose

This analysis compares the two existing App Description documents to determine:
1. Which one is canonical
2. What needs to be reconciled
3. Whether a single authoritative App Description exists
4. What changes (if any) are required

---

## Current State

### Two App Descriptions Exist

1. **Root-Level App Description**
   - **Location**: `/APP_DESCRIPTION.md`
   - **Title**: "Maturion Foreman Office App — Canonical Application Description & Operating Contract"
   - **Version**: 1.1
   - **Status**: Authoritative
   - **Length**: 296 lines
   - **Last Updated**: Not explicitly stated

2. **Governance-Level App Description**
   - **Location**: `/docs/governance/FM_APP_DESCRIPTION.md`
   - **Title**: "FM Office App — Product Description (Authoritative)"
   - **Status**: Authoritative v1
   - **Owner**: Johan Ras
   - **Length**: 344 lines
   - **Last Updated**: Not explicitly stated

---

## Key Differences

### Structural Differences

**Root-Level (`APP_DESCRIPTION.md`)**:
- More formal, constitutional tone
- Emphasizes governance supremacy and continuous supervision
- Focuses on roles and authority model (Human Owner, Foreman, Builders)
- Strong emphasis on memory & provenance
- Explicit non-goals and constraints section
- References "True North" architecture explicitly
- Written as an "Operating Contract"

**Governance-Level (`FM_APP_DESCRIPTION.md`)**:
- More product-focused, user-centered tone
- Emphasizes conversational interface and UX
- Detailed interaction model (ping-based attention system)
- Extensive coverage of Parking Station (continuous improvement)
- Detailed Intent → Execution loop
- Analytics interface section
- More operational and practical focus
- Written as "Product Description"

### Content Coverage Comparison

| Section/Topic | Root-Level | Governance-Level |
|---------------|-----------|------------------|
| Purpose | ✅ Supervisory control system | ✅ One-man operations control |
| What app is/is not | ✅ Comprehensive | ✅ Comprehensive |
| Platform-wide scope | ✅ Explicit | ⚠️ Less explicit |
| Roles & Authority | ✅ Detailed (3 roles) | ✅ Brief (Johan focus) |
| Governance Supremacy | ✅ Dedicated section | ⚠️ Embedded |
| Continuous Supervision | ✅ Dedicated section | ✅ Via operational dashboard |
| Memory & Provenance | ✅ Dedicated section | ❌ Not covered |
| UI/UX Operating Contract | ✅ Dedicated section | ✅ Much more detailed |
| Conversational Interface | ⚠️ Implicit | ✅ Extensive (Section 4) |
| Parking Station | ❌ Not covered | ✅ Extensive (Section 6) |
| Intent → Execution Loop | ⚠️ Implicit | ✅ Detailed (Section 7) |
| Analytics Interface | ❌ Not covered | ✅ Yes (Section 9) |
| Operational Dashboard | ⚠️ Brief | ✅ Detailed (Section 5) |
| Watchdog | ✅ Yes | ❌ Not covered |
| Cost & Performance | ✅ Yes | ✅ Yes (Section 12) |
| Non-Goals | ✅ Explicit section | ✅ Yes (Section 13) |
| Success Definition | ✅ Yes (outcome-based) | ✅ Yes (operational) |
| Architecture Reference | ✅ Explicit reference to True North | ❌ Not referenced |

---

## Governance Policy Requirements

Per `APP_DESCRIPTION_REQUIREMENT_POLICY.md`, the App Description MUST include:

### 1. App Purpose ✅
- Both documents include this
- Root-level: "Continuous supervisory control system"
- Governance-level: "One-man operations control centre"
- **Assessment**: Both valid, complementary perspectives

### 2. Target Users ✅
- Both documents define Johan (Human Owner) as primary user
- Root-level: More formal "Human Owner" construct
- Governance-level: More personal "Johan Ras" focus
- **Assessment**: Both valid

### 3. Core Capabilities (High-Level) ✅
- Both documents describe capabilities
- Root-level: More abstract (supervision, enforcement, escalation)
- Governance-level: More concrete (dashboard, parking station, analytics)
- **Assessment**: Governance-level more complete

### 4. Explicit Non-Goals ✅
- Both documents include non-goals
- Root-level: Governance and constraint focus
- Governance-level: Tool/product focus
- **Assessment**: Both valid, complementary

### 5. Build Boundary ⚠️
- Root-level: References True North Architecture explicitly
- Governance-level: Does NOT reference downstream phases explicitly
- **Assessment**: Root-level more complete, governance-level missing this

---

## Analysis: Which is Canonical?

### Per Governance Policy

`APP_DESCRIPTION_REQUIREMENT_POLICY.md` states:

> **Canonical Location**: `docs/governance/{APP}_APP_DESCRIPTION.md`
> 
> **Optional Duplicate**: A duplicate copy MAY exist at repository root (`/APP_DESCRIPTION.md`) for convenience, but **governance validation MUST reference the canonical location**.

**Conclusion**: The **canonical** App Description should be at:
- **`docs/governance/FM_APP_DESCRIPTION.md`**

The root-level `APP_DESCRIPTION.md` is permitted as a convenience duplicate but is NOT canonical.

### However...

The root-level document has:
1. Stronger governance alignment
2. Explicit True North reference (required by policy)
3. More constitutional/authority focus
4. Better build boundary definition

The governance-level document has:
1. More practical/operational detail
2. Better UX/product definition
3. More complete capability description
4. Better user-centered perspective

**Neither document alone fully satisfies all requirements.**

---

## Recommendation

**Option 1: Merge Both Documents** (Recommended)
- Create a single authoritative App Description at the canonical location
- Incorporate governance/authority content from root-level
- Incorporate product/UX detail from governance-level
- Ensure all policy requirements are met
- Update root-level to be a reference/pointer to canonical location

**Option 2: Elevate Governance-Level**
- Keep governance-level as primary
- Add missing governance/authority sections from root-level
- Add explicit True North reference
- Add build boundary definition
- Update root-level to reference canonical

**Option 3: Elevate Root-Level**
- Keep root-level as primary (but move to canonical location)
- Add missing UX/product sections from governance-level
- Maintain governance supremacy focus
- Risk: Less user-centered

---

## Proposed Solution

**I recommend Option 1 (Merge)** because:

1. **Governance Compliance**: Ensures canonical location is correct
2. **Completeness**: Captures both governance and product perspectives
3. **Non-Regression**: Preserves all existing content
4. **Policy Alignment**: Explicitly satisfies all policy requirements
5. **Single Source of Truth**: Eliminates ambiguity

### Structure of Merged Document

```
# Foreman Office App — Authoritative Application Description

## Metadata
- Version
- Status: Authoritative
- Owner: Johan Ras
- Canonical Location
- Architecture Reference: TRUE_NORTH_FM_ARCHITECTURE.md

## 1. App Purpose
(Core problem statement)

## 2. What This App Is (and Is Not)
2.1 What It IS
2.2 What It IS NOT
2.3 Platform-Wide Supervisory Role

## 3. Target Users
3.1 Human Owner (Johan)
3.2 Interaction Model

## 4. Core Capabilities (High-Level)
4.1 Conversational Interface
4.2 Operational Dashboard
4.3 Parking Station
4.4 Intent → Execution Loop
4.5 Analytics Interface

## 5. Roles and Authority Model
5.1 Human Owner (Johan)
5.2 Foreman (AI Supervisor)
5.3 Builder Agents

## 6. Governance Supremacy
6.1 Canonical Governance
6.2 Governance Enforcement Semantics

## 7. Continuous Supervision Model

## 8. Memory & Provenance

## 9. Human Interaction Model (UI/UX Operating Contract)
9.1 Purpose of the UI
9.2 Default UI State
9.3 Escalation UX
9.4 Drill-Down Rule
9.5 Explicit UI Non-Goals

## 10. Cost, Performance, and Oversight

## 11. Watchdog & Independent Oversight

## 12. Explicit Non-Goals and Constraints

## 13. Success Definition

## 14. Build Boundary
(Explicit statement that this description governs Phase 4.2, 4.3, 4.4, 4.5)

## 15. Architecture Reference
(Explicit reference to TRUE_NORTH_FM_ARCHITECTURE.md)
```

---

## Next Steps

1. ✅ Complete this analysis
2. Create merged App Description at canonical location
3. Update root-level APP_DESCRIPTION.md to reference canonical location
4. Validate against policy requirements
5. Produce completion evidence
6. Declare Phase 4.1 complete

---

**Status**: Analysis Complete — Ready to Proceed with Merge
