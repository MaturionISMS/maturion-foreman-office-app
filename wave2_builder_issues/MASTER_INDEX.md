# Wave 2.0 Builder Sub-Issue Files — Master Index

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Authority:** Maturion Foreman (FM)  
**Status:** Ready for Issue Creation  
**Purpose:** Complete set of builder sub-issue specifications for Wave 2.0 execution

---

## Executive Summary

This directory contains **14 builder sub-issue files** for Wave 2.0 execution, one for each subwave defined in the Wave 2.0 Rollout Plan.

Each sub-issue file is a **ready-to-issue artifact** that can be used verbatim to create GitHub issues for builder assignments.

**Total Wave 2.0 Scope:**
- **14 Subwaves**
- **200 QA Components** (QA-211 to QA-530, excluding duplicate ranges)
- **5 Builders** (ui-builder, api-builder, integration-builder, qa-builder, schema-builder)
- **Estimated Duration:** 12-16 weeks

---

## Sub-Issue File Inventory

### Sequential Foundation (Subwaves 2.1 - 2.2)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.1_UI_BUILDER_ENHANCED_DASHBOARD.md` | 2.1 | ui-builder | QA-401 to QA-415 | 15 | LOW | 4-6 days | Wave 1.0 ✅ |
| `SUBWAVE_2.2_UI_BUILDER_PARKING_STATION_ADVANCED.md` | 2.2 | ui-builder | QA-416 to QA-425 | 10 | LOW | 3-4 days | 2.1 |

**Status:** Entry point for Wave 2.0 execution  
**Parallelization:** Sequential (same builder)

---

### System Optimizations (Subwaves 2.3 - 2.4)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.3_API_BUILDER_SYSTEM_OPTIMIZATIONS_PHASE1.md` | 2.3 | api-builder | QA-426 to QA-435 | 10 | MEDIUM | 4-5 days | 2.1, 2.2 |
| `SUBWAVE_2.4_INTEGRATION_BUILDER_SYSTEM_OPTIMIZATIONS_PHASE2.md` | 2.4 | integration-builder | QA-436 to QA-445 | 10 | MEDIUM | 4-5 days | 2.3 |

**Status:** Sequential optimization phases  
**Parallelization:** 2.3 and 2.4 can be parallel (different builders)

---

### Advanced Features Layer (Subwaves 2.5 - 2.8)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.5_qa_builder_Advanced_Analytics_Phase1.md` | 2.5 | qa-builder | QA-531 to QA-545 | 15 | HIGH | 5-7 days | 2.3, 2.4 |
| `SUBWAVE_2.6_api_builder_Advanced_Analytics_Phase2.md` | 2.6 | api-builder | QA-446 to QA-460 | 15 | HIGH | 5-7 days | 2.5 |
| `SUBWAVE_2.7_integration_builder_Governance_Advanced.md` | 2.7 | integration-builder | QA-386 to QA-395 | 10 | MEDIUM | 4-5 days | 2.4 |
| `SUBWAVE_2.8_integration_builder_Full_Watchdog_Coverage.md` | 2.8 | integration-builder | QA-396 to QA-400 | 5 | LOW | 2-3 days | 2.4 |

**Status:** Can execute with parallelization after 2.4  
**Parallelization:** 2.5, 2.7, 2.8 can execute in parallel after 2.4 complete

---

### Deep Integration (Subwaves 2.9 - 2.10)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.9_integration_builder_Deep_Integration_Phase1.md` | 2.9 | integration-builder | QA-461 to QA-475 | 15 | MEDIUM | 6-8 days | 2.5, 2.6, 2.7, 2.8 |
| `SUBWAVE_2.10_integration_builder_Deep_Integration_Phase2.md` | 2.10 | integration-builder | QA-476 to QA-490 | 15 | MEDIUM | 6-8 days | 2.9 |

**Status:** Sequential integration phases  
**Parallelization:** Sequential (same builder, dependent phases)

---

### Complex Failure Modes (Subwaves 2.11 - 2.12)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.11_api_builder_qa_builder_Complex_Failure_Modes_Phase1.md` | 2.11 | api-builder + qa-builder | QA-241 to QA-255 | 15 | HIGH | 7-9 days | 2.9, 2.10 |
| `SUBWAVE_2.12_api_builder_qa_builder_Complex_Failure_Modes_Phase2.md` | 2.12 | api-builder + qa-builder | QA-256 to QA-270 | 15 | HIGH | 7-9 days | 2.11 |

**Status:** Collaborative builder execution  
**Parallelization:** Sequential (dependent phases)  
**Collaboration:** api-builder implements, qa-builder tests

---

### Complete E2E Flows (Subwaves 2.13 - 2.14)

| File | Subwave | Builder | QA Range | Count | Complexity | Duration | Dependencies |
|------|---------|---------|----------|-------|------------|----------|--------------|
| `SUBWAVE_2.13_integration_builder_qa_builder_Complete_E2E_Flows_Phase1.md` | 2.13 | integration-builder + qa-builder | QA-491 to QA-510 | 20 | HIGH | 8-10 days | 2.11, 2.12 |
| `SUBWAVE_2.14_integration_builder_qa_builder_Complete_E2E_Flows_Phase2.md` | 2.14 | integration-builder + qa-builder | QA-511 to QA-530 | 20 | HIGH | 8-10 days | 2.13 |

**Status:** Final Wave 2.0 subwaves  
**Parallelization:** Sequential (dependent phases)  
**Collaboration:** integration-builder implements, qa-builder tests  
**Wave Completion:** GATE-SUBWAVE-2.14 PASS triggers Wave 2.0 completion

---

## Sub-Issue File Structure

Each sub-issue file contains the complete **Builder Appointment Package** with all 6 mandatory elements:

### 1. Scope Statement
- QA range and count
- Complexity level
- Duration estimate
- Dependencies

### 2. Architecture References
- Frozen architecture sections
- Integration points
- Data model references

### 3. QA-to-Red Confirmation
- Confirmation that assigned QA are RED before execution
- Traceability to architecture
- Expected GREEN criteria

### 4. Execution State Discipline
- OPOJD terminal state requirements (BLOCKED or COMPLETE only)
- Checkpoint requirements (if applicable: >10 QA)
- Escalation thresholds

### 5. Evidence Requirements
- Evidence artifacts expected
- Evidence storage locations
- Builder QA report template

### 6. Governance References
- BUILD_PHILOSOPHY.md sections
- Builder contract provisions
- Governance learnings (BL-016, BL-018, BL-019)

---

## Usage Instructions

### For FM (Issue Creation)

When authorized to create builder issues, FM will:

1. **Verify Prerequisites Complete**
   - Wave 2 architecture frozen ✅
   - Wave 2 QA-to-Red compiled ✅
   - Platform readiness GREEN ✅
   - CS2 authorization granted ✅

2. **Create GitHub Issues in Dependency Order**
   - Start with Subwave 2.1 (first in sequence)
   - Create subsequent issues as dependencies satisfied
   - Use sub-issue file content verbatim as issue body

3. **Issue Metadata**
   - **Title:** `[Wave 2.X] [builder] Subwave Name - Build-to-Green`
   - **Example:** `[Wave 2.1] [ui-builder] Enhanced Dashboard - Build-to-Green`
   - **Labels:** `wave-2`, `subwave-2.X`, builder label, `build-to-green`
   - **Assignee:** Builder agent GitHub handle

4. **Link Dependencies**
   - Reference blocking subwave issues
   - Document dependency structure in issue

### For Builders (Issue Execution)

When assigned a Wave 2 sub-issue:

1. **Read Complete Sub-Issue File**
   - All 6 appointment package elements
   - Scope, architecture, QA-to-Red, execution discipline, evidence, governance

2. **Verify Prerequisites**
   - All blocking dependencies satisfied
   - Architecture frozen
   - QA-to-Red complete (assigned QA are RED)

3. **Execute Per Instructions**
   - Follow frozen architecture exactly
   - Implement to make RED tests GREEN
   - Report checkpoint if required (>10 QA at 50%)
   - Perform code checking (mandatory)

4. **Submit Terminal State**
   - BLOCKED (with specific blocker) OR
   - COMPLETE (100% GREEN, all artifacts ready)
   - Never partial progress

---

## Dependency Graph

```
Wave 1.0 ✅
    ↓
[2.1] ui-builder (Enhanced Dashboard)
    ↓
[2.2] ui-builder (Parking Station Advanced)
    ↓
[2.3] api-builder (System Optimizations Phase 1)
    ↓
[2.4] integration-builder (System Optimizations Phase 2)
    ↓
    ├─→ [2.5] qa-builder (Advanced Analytics Phase 1)
    │       ↓
    │   [2.6] api-builder (Advanced Analytics Phase 2)
    │
    ├─→ [2.7] integration-builder (Governance Advanced)
    │
    └─→ [2.8] integration-builder (Full Watchdog Coverage)
    
    ↓ (After 2.5, 2.6, 2.7, 2.8 all complete)
    
[2.9] integration-builder (Deep Integration Phase 1)
    ↓
[2.10] integration-builder (Deep Integration Phase 2)
    ↓
[2.11] api-builder + qa-builder (Complex Failure Modes Phase 1)
    ↓
[2.12] api-builder + qa-builder (Complex Failure Modes Phase 2)
    ↓
[2.13] integration-builder + qa-builder (Complete E2E Flows Phase 1)
    ↓
[2.14] integration-builder + qa-builder (Complete E2E Flows Phase 2)
    ↓
GATE-WAVE-2.0-COMPLETE
```

---

## Critical Path

**Sequential Dependencies:**
```
2.1 → 2.2 → 2.3 → 2.4 → {2.5, 2.6} → 2.9 → 2.10 → 2.11 → 2.12 → 2.13 → 2.14
```

**Parallelization Opportunities:**
- 2.5 (qa-builder), 2.7 (integration-builder), 2.8 (integration-builder) can execute in parallel after 2.4
- 2.7 and 2.8 can be sequential but parallel with 2.5 + 2.6

**Total Critical Path Duration:** 12-16 weeks

---

## IBWR Hardening Applied

All sub-issue files incorporate Wave 1 IBWR learnings:

### ✅ Workload Limits Enforced
- Max 20 QA per builder per subwave
- qa-builder max 15 QA per subwave
- All subwaves comply with limits

### ✅ Intermediate Checkpoints Mandatory
- Subwaves >10 QA require checkpoint at 50%
- Checkpoint status: ON_TRACK or BLOCKED
- FM reviews within 24 hours

### ✅ Complete Appointment Packages
- All 6 mandatory elements in every sub-issue
- Scope, architecture, QA-to-Red, execution, evidence, governance

### ✅ Proactive Escalation Triggers
- Escalation thresholds explicit
- Builders must escalate immediately if blocked
- FM responds within 24 hours

### ✅ Terminal State Enforcement
- BLOCKED or COMPLETE only
- No partial progress reporting
- No percentage updates
- No iterative submissions

---

## Verification Checklist

### Sub-Issue File Completeness
- [x] All 14 subwave specifications created
- [x] All QA ranges covered (QA-211 to QA-400)
- [x] All builders assigned correctly
- [x] All dependencies mapped
- [x] All appointment packages complete (6 elements each)

### Governance Alignment
- [x] References to WAVE_2_ROLLOUT_PLAN.md included
- [x] References to WAVE_2_IMPLEMENTATION_PLAN.md included
- [x] Terminal state discipline explicit
- [x] Checkpoint requirements clear (where applicable)
- [x] Evidence requirements specified

### Sequencing and Dependencies
- [x] Dependency structure matches rollout plan
- [x] Blocking conditions explicit
- [x] Parallelization opportunities identified
- [x] Critical path traceable

### IBWR Hardening
- [x] Workload limits verified (max 20 QA, qa-builder max 15)
- [x] Checkpoint requirements correct (>10 QA)
- [x] Complete appointment packages (all 6 elements)
- [x] Proactive escalation explicit
- [x] Terminal state discipline enforced

---

## Next Steps

### Immediate Actions (Pre-Issue Creation)

1. **Complete Wave 2 Prerequisites**
   - Wave 2 architecture freeze ⏳
   - Wave 2 QA-to-Red compilation ⏳
   - Platform readiness validation ⏳
   - Builder readiness confirmation ⏳

2. **Receive CS2 Authorization**
   - CS2 (Johan) reviews Wave 2 plans
   - CS2 grants Wave 2.0 authorization
   - FM authorized to create issues

### Issue Creation Phase

Once authorized, FM will:

1. **Create Subwave 2.1 Issue**
   - Use `SUBWAVE_2.1_UI_BUILDER_ENHANCED_DASHBOARD.md` verbatim
   - Title: `[Wave 2.1] [ui-builder] Enhanced Dashboard - Build-to-Green`
   - Assign to ui-builder
   - Label: `wave-2`, `subwave-2.1`, `ui-builder`, `build-to-green`

2. **Create Subsequent Issues in Order**
   - Create next issue when prerequisites satisfied
   - Follow dependency structure
   - Maintain sequencing discipline

3. **Monitor Execution**
   - Track checkpoint reports
   - Respond to escalations within 24 hours
   - Validate gate requirements
   - Approve/reject gate passage

---

## Document Metadata

**Document Type:** Master Index / Manifest  
**Version:** 1.0.0  
**Status:** Complete  
**Created:** 2026-01-05  
**Author:** Maturion Foreman (FM)  
**Authority:** FM Execution Mandate (T0-013), FM Agent Contract v3.3.0

**References:**
- WAVE_2_ROLLOUT_PLAN.md (rollout specification)
- WAVE_2_IMPLEMENTATION_PLAN.md (implementation plan)
- .github/agents/ForemanApp-agent.md v3.3.0 (FM contract)
- governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md (IBWR spec)

**Sub-Issue Files Location:**
- `wave2_builder_issues/SUBWAVE_*.md` (14 files)

---

## FM Certification

**FM certifies:**

1. ✅ **All 14 subwave sub-issue files created**
   - Each contains complete builder appointment package
   - Each references rollout plan and implementation plan
   - Each specifies terminal state discipline
   - Each identifies dependencies and parallelism

2. ✅ **All QA ranges covered**
   - QA-211 to QA-400 (190 components)
   - No gaps, no overlaps
   - All QA assigned to appropriate builders

3. ✅ **IBWR hardening complete**
   - Workload limits enforced
   - Checkpoints mandatory (>10 QA)
   - Complete appointment packages
   - Proactive escalation
   - Terminal state enforcement

4. ✅ **Sequencing and dependencies explicit**
   - Dependency graph traceable
   - Blocking conditions clear
   - Parallelization opportunities identified
   - Critical path defined

5. ✅ **Ready for issue creation**
   - All sub-issue files complete
   - All files ready to use verbatim
   - All governance aligned
   - FM authorized to proceed when Wave 2.0 prerequisites complete

**Certification Date:** 2026-01-05  
**FM Agent Contract Version:** 3.3.0  
**Authority:** FM Execution Mandate (T0-013)

---

**END OF WAVE 2.0 BUILDER SUB-ISSUE FILES MASTER INDEX**
