# Wave 2.0 Builder Sub-Issue Files

**Purpose:** Ready-to-issue builder assignment specifications for Wave 2.0 execution  
**Status:** Complete — 14 sub-issue files ready  
**Authority:** Maturion Foreman (FM)  
**Date:** 2026-01-05

---

## Overview

This directory contains **14 builder sub-issue files** for Wave 2.0, one for each subwave defined in `WAVE_2_ROLLOUT_PLAN.md`.

Each file is a **complete, ready-to-issue specification** that can be used verbatim to create GitHub issues for builder assignments.

---

## What Are These Files?

These are **builder appointment artifacts** — not GitHub issues themselves, but markdown files ready to become GitHub issues when FM is authorized.

**Key Characteristics:**
- ✅ Complete builder appointment packages (all 6 mandatory elements)
- ✅ Explicit scope, architecture, QA-to-Red, execution discipline, evidence, governance
- ✅ Terminal state discipline (BLOCKED or COMPLETE only)
- ✅ Checkpoint requirements (where applicable: >10 QA)
- ✅ Dependency structure and parallelization guidance
- ✅ IBWR-hardened (Wave 1 learnings integrated)

---

## File Inventory

| # | File | Builder | QA Count | Complexity |
|---|------|---------|----------|------------|
| 1 | `SUBWAVE_2.1_UI_BUILDER_ENHANCED_DASHBOARD.md` | ui-builder | 15 | LOW |
| 2 | `SUBWAVE_2.2_UI_BUILDER_PARKING_STATION_ADVANCED.md` | ui-builder | 10 | LOW |
| 3 | `SUBWAVE_2.3_API_BUILDER_SYSTEM_OPTIMIZATIONS_PHASE1.md` | api-builder | 10 | MEDIUM |
| 4 | `SUBWAVE_2.4_INTEGRATION_BUILDER_SYSTEM_OPTIMIZATIONS_PHASE2.md` | integration-builder | 10 | MEDIUM |
| 5 | `SUBWAVE_2.5_qa_builder_Advanced_Analytics_Phase1.md` | qa-builder | 15 | HIGH |
| 6 | `SUBWAVE_2.6_api_builder_Advanced_Analytics_Phase2.md` | api-builder | 15 | HIGH |
| 7 | `SUBWAVE_2.7_integration_builder_Governance_Advanced.md` | integration-builder | 10 | MEDIUM |
| 8 | `SUBWAVE_2.8_integration_builder_Full_Watchdog_Coverage.md` | integration-builder | 5 | LOW |
| 9 | `SUBWAVE_2.9_integration_builder_Deep_Integration_Phase1.md` | integration-builder | 15 | MEDIUM |
| 10 | `SUBWAVE_2.10_integration_builder_Deep_Integration_Phase2.md` | integration-builder | 15 | MEDIUM |
| 11 | `SUBWAVE_2.11_api_builder_qa_builder_Complex_Failure_Modes_Phase1.md` | api-builder + qa-builder | 15 | HIGH |
| 12 | `SUBWAVE_2.12_api_builder_qa_builder_Complex_Failure_Modes_Phase2.md` | api-builder + qa-builder | 15 | HIGH |
| 13 | `SUBWAVE_2.13_integration_builder_qa_builder_Complete_E2E_Flows_Phase1.md` | integration-builder + qa-builder | 20 | HIGH |
| 14 | `SUBWAVE_2.14_integration_builder_qa_builder_Complete_E2E_Flows_Phase2.md` | integration-builder + qa-builder | 20 | HIGH |

**Total:** 190 QA components (QA-211 to QA-400)

---

## How To Use These Files

### For FM (When Authorized)

1. **Verify Wave 2.0 Prerequisites Complete**
   - Wave 2 architecture frozen
   - Wave 2 QA-to-Red compiled
   - Platform readiness GREEN
   - CS2 authorization granted

2. **Create GitHub Issues**
   - Use sub-issue file content **verbatim** as issue body
   - Title format: `[Wave 2.X] [builder] Subwave Name - Build-to-Green`
   - Labels: `wave-2`, `subwave-2.X`, builder label, `build-to-green`
   - Assign to builder agent

3. **Follow Dependency Order**
   - Create Subwave 2.1 first (entry point)
   - Create subsequent issues as dependencies satisfied
   - Maintain sequencing discipline

### For Builders (When Assigned)

1. **Read Complete Sub-Issue**
   - All 6 appointment package elements
   - Understand scope, dependencies, constraints

2. **Execute Per Instructions**
   - Follow frozen architecture exactly
   - Make RED tests GREEN
   - Report checkpoint if required (>10 QA at 50%)
   - Perform code checking (mandatory)

3. **Submit Terminal State Only**
   - BLOCKED (with specific blocker) OR
   - COMPLETE (100% GREEN, all artifacts)
   - Never partial progress

---

## Key Features

### IBWR Hardening
- ✅ Workload limits enforced (max 20 QA per builder, qa-builder max 15)
- ✅ Intermediate checkpoints mandatory (>10 QA at 50%)
- ✅ Complete appointment packages (all 6 elements)
- ✅ Proactive escalation triggers explicit
- ✅ Terminal state discipline (BLOCKED or COMPLETE only)

### Governance Alignment
- ✅ References WAVE_2_ROLLOUT_PLAN.md
- ✅ References WAVE_2_IMPLEMENTATION_PLAN.md
- ✅ References BUILD_PHILOSOPHY.md
- ✅ References builder contracts
- ✅ References BL-016, BL-018, BL-019 learnings

### Dependency Management
- ✅ Blocking conditions explicit
- ✅ Parallelization opportunities identified
- ✅ Downstream dependencies clear
- ✅ Critical path traceable

---

## Important Notes

### Do NOT Create Issues Yet

These files are **ready for issue creation** but issues should NOT be created until:
- ⏳ Wave 2 architecture frozen
- ⏳ Wave 2 QA-to-Red compiled
- ⏳ Platform readiness GREEN
- ⏳ CS2 (Johan) authorization granted

### Use Files Verbatim

When creating GitHub issues, use the sub-issue file content **exactly as written**. Do not:
- ❌ Summarize or shorten
- ❌ Omit sections
- ❌ Modify appointment package elements
- ❌ Change constraints or requirements

The files are complete and ready to use as-is.

---

## Master Index

See `MASTER_INDEX.md` for:
- Complete sub-issue inventory with details
- Dependency graph visualization
- Critical path analysis
- Usage instructions
- Verification checklist
- FM certification

---

## References

- **WAVE_2_ROLLOUT_PLAN.md** — Complete Wave 2.0 rollout specification
- **WAVE_2_IMPLEMENTATION_PLAN.md** — Wave 2.0 implementation plan (IBWR-hardened)
- **.github/agents/ForemanApp-agent.md v3.3.0** — FM agent contract
- **governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md** — IBWR specification
- **BUILD_PHILOSOPHY.md** — One-Time Build Correctness principle

---

## Questions?

- **Architecture:** Refer to frozen Wave 2 architecture (when available)
- **Governance:** Refer to BUILD_PHILOSOPHY.md and governance docs
- **Execution:** Refer to rollout plan and implementation plan
- **Escalation:** Contact FM for clarification

---

**Created:** 2026-01-05  
**Author:** Maturion Foreman (FM)  
**Authority:** FM Execution Mandate (T0-013)

