# Wave 2 Rollout Plan — Quick Reference

**Version:** 1.0.0  
**Date:** 2026-01-05  
**Status:** Ready for Review  
**Full Plan:** WAVE_2_ROLLOUT_PLAN.md (49.5KB, 1,675 lines)

---

## Wave 2.0 At a Glance

**Scope:** 190 QA components (QA-211 to QA-400)  
**Subwaves:** 14  
**Duration:** 12-16 weeks (3-4 months)  
**Status:** Awaiting CS2 approval to proceed to prerequisites and execution

---

## Subwave Summary

| # | Name | QA Range | Count | Builder(s) | Days | Complexity |
|---|------|----------|-------|------------|------|------------|
| 2.1 | Enhanced Dashboard | 361-375 | 15 | ui-builder | 4-6 | LOW |
| 2.2 | Parking Station Advanced | 376-385 | 10 | ui-builder | 3-4 | LOW |
| 2.3 | System Optimizations Phase 1 | 341-350 | 10 | api-builder | 4-5 | MEDIUM |
| 2.4 | System Optimizations Phase 2 | 351-360 | 10 | integration-builder | 4-5 | MEDIUM |
| 2.5 | Advanced Analytics Phase 1 | 211-225 | 15 | qa-builder | 5-7 | HIGH |
| 2.6 | Advanced Analytics Phase 2 | 226-240 | 15 | api-builder | 5-7 | HIGH |
| 2.7 | Governance Advanced | 386-395 | 10 | integration-builder | 4-5 | MEDIUM |
| 2.8 | Full Watchdog Coverage | 396-400 | 5 | integration-builder | 2-3 | LOW |
| 2.9 | Deep Integration Phase 1 | 271-285 | 15 | integration-builder | 6-8 | MEDIUM |
| 2.10 | Deep Integration Phase 2 | 286-300 | 15 | integration-builder | 6-8 | MEDIUM |
| 2.11 | Complex Failure Modes Phase 1 | 241-255 | 15 | api + qa (collab) | 7-9 | HIGH |
| 2.12 | Complex Failure Modes Phase 2 | 256-270 | 15 | api + qa (collab) | 7-9 | HIGH |
| 2.13 | Complete E2E Flows Phase 1 | 301-320 | 20 | int + qa (collab) | 8-10 | HIGH |
| 2.14 | Complete E2E Flows Phase 2 | 321-340 | 20 | int + qa (collab) | 8-10 | HIGH |

**Total:** 190 QA components, 12-16 weeks

---

## Critical Path

```
Wave 1.0 ✅ → 2.1 → 2.2 → 2.3 → 2.4 → {2.5, 2.7, 2.8} → 2.6 → 2.9 → 2.10 → 2.11 → 2.12 → 2.13 → 2.14
```

**Parallelization:** 2.5, 2.7, 2.8 can execute in parallel after 2.4 completes

---

## Builder Workload Distribution

| Builder | Subwaves | Solo QA | Collab QA | Total | Workload Status |
|---------|----------|---------|-----------|-------|-----------------|
| ui-builder | 2.1, 2.2 | 25 | 0 | 25 | ✅ Under limit (20/subwave) |
| api-builder | 2.3, 2.6, 2.11, 2.12 | 40 | 30 | 70 | ✅ Under limit (25/subwave) |
| integration-builder | 2.4, 2.7, 2.8, 2.9, 2.10, 2.13, 2.14 | 55 | 40 | 95 | ✅ Under limit (20/subwave) |
| qa-builder | 2.5, 2.11, 2.12, 2.13, 2.14 | 15 | 70 | 85 | ✅ At limit (15/subwave solo) |
| schema-builder | (none) | 0 | 0 | 0 | ✅ No Wave 2 assignments |

**All workload limits respected:**
- ✅ ui-builder: max 20 QA/subwave
- ✅ api-builder: max 25 QA/subwave
- ✅ integration-builder: max 20 QA/subwave
- ✅ qa-builder: max 15 QA/subwave (solo)

---

## Gate Structure

```
GATE-WAVE-2.0-COMPLETE
    └── All 14 subwave gates PASS
        ├── 2.14 ← 2.13
        ├── 2.13 ← 2.11, 2.12
        ├── 2.12 ← 2.11
        ├── 2.11 ← 2.9, 2.10
        ├── 2.10 ← 2.9
        ├── 2.9 ← 2.5, 2.6, 2.7, 2.8
        ├── 2.8 ← 2.4
        ├── 2.7 ← 2.4
        ├── 2.6 ← 2.5
        ├── 2.5 ← 2.3, 2.4
        ├── 2.4 ← 2.3
        ├── 2.3 ← 2.1, 2.2
        ├── 2.2 ← 2.1
        └── 2.1 ← Wave 1.0 ✅
```

---

## IBWR Hardening Features

### 1. Workload Sizing Limits
- ✅ Max QA per builder per subwave enforced
- ✅ No subwaves exceed limits
- ✅ Proactive segmentation applied

### 2. Gate Density & Checkpoints
- ✅ Intermediate checkpoints mandatory for >10 QA subwaves
- ✅ Checkpoint at 50% for 11-20 QA subwaves
- ✅ 9 subwaves have checkpoints (2.1, 2.5, 2.6, 2.9, 2.10, 2.11, 2.12, 2.13, 2.14)
- ✅ 5 subwaves ≤10 QA, no checkpoint required (2.2, 2.3, 2.4, 2.7, 2.8)

### 3. Builder Appointment Discipline
- ✅ Mandatory 6-element appointment package:
  1. Scope Statement
  2. Architecture References
  3. QA-to-Red Confirmation
  4. Execution State Discipline
  5. Evidence Requirements
  6. Governance References

### 4. Escalation & Halt Semantics
- ✅ Proactive complexity assessment before execution
- ✅ Builder escalation triggers explicit
- ✅ FM response times defined (4h ack, 24h resolution)
- ✅ Early warning signals identified

### 5. Progress Recording
- ✅ Mandatory artifacts per subwave:
  - Builder Appointment Instruction
  - Builder Completion Report
  - FM Gate Review
  - Subwave Completion Summary

### 6. Terminal State Enforcement
- ✅ Only BLOCKED or COMPLETE allowed
- ✅ No partial progress reports
- ✅ No "in progress" states
- ✅ FM rejection of non-terminal states

---

## Prerequisites (Blocking)

Wave 2 execution CANNOT start until:

- [ ] Wave 1 IBWR Complete ✅ (DONE)
- [ ] Wave 2 Architecture Frozen ⏳
- [ ] Wave 2 QA-to-Red Complete ⏳
- [ ] Platform Readiness GREEN ✅ (DONE)
- [ ] Builder Readiness Confirmed ⏳
- [ ] Wave 2 Rollout Plan Approved ⏳ (awaiting CS2 review)

---

## Completion Criteria

**Wave 2.0 is complete when:**

1. ✅ All 400 QA (QA-001 to QA-400) GREEN
2. ✅ All 14 subwave gates PASS
3. ✅ GATE-WAVE-2.0-COMPLETE PASS
4. ✅ No Wave 1 regressions (QA-001 to QA-210 remain GREEN)
5. ✅ Zero test debt
6. ✅ All evidence artifacts complete
7. ✅ IBWR executed with status PASS

---

## Post-Wave 2 IBWR

**Mandatory after GATE-WAVE-2.0-COMPLETE = PASS:**

1. Initiation
2. Evidence Collection (14 subwave artifacts)
3. Analysis & Pattern Recognition
4. Corrective Action Planning (if needed)
5. Ripple Propagation (if needed)
6. Artifact Generation (reports, certification)
7. IBWR Declaration (PASS / CORRECTIVE_ACTIONS_REQUIRED)
8. Next Wave Authorization Gate (blocks Wave 3 if IBWR ≠ PASS)

**Mandatory Artifacts:**
- `governance/reports/waves/WAVE_2_RECONCILIATION_REPORT.md`
- `governance/reports/waves/WAVE_2_RETROSPECTIVE_CERTIFICATION.md`
- `governance/reports/waves/WAVE_2_CORRECTIVE_ACTIONS.md` (if applicable)

---

## Next Steps

### Immediate
1. CS2 (Johan) reviews Wave 2 Rollout Plan
2. CS2 provides feedback or approval

### Prerequisites Phase (If Approved)
1. Wave 2 architecture freeze
2. Wave 2 QA-to-Red compilation
3. Platform readiness validation
4. Builder readiness confirmation

### Execution Phase (When Prerequisites Satisfied)
1. FM creates individual builder issues per subwave
2. Wave 2.1 execution starts (Enhanced Dashboard)
3. Subwaves execute per dependency structure
4. Wave 2.0 gate evaluation
5. IBWR execution

---

## Document References

**Primary Documents:**
- **WAVE_2_ROLLOUT_PLAN.md** — Full rollout specification (49.5KB)
- **WAVE_2_ROLLOUT_PLAN_COMPLETION_VERIFICATION.md** — Verification report (18KB)
- **WAVE_2_IMPLEMENTATION_PLAN.md** — Implementation plan (32KB)
- **WAVE_2_READINESS_STATEMENT.md** — Readiness statement

**Governance References:**
- `.github/agents/ForemanApp-agent.md` v3.3.0 (FM Agent Contract)
- `governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md` (IBWR Specification)
- `BUILD_PHILOSOPHY.md` (One-Time Build Law)

**Builder Contracts:**
- `.github/agents/ui-builder.md`
- `.github/agents/api-builder.md`
- `.github/agents/integration-builder.md`
- `.github/agents/qa-builder.md`
- `.github/agents/schema-builder.md`

---

## FM Certification

**FM certifies:**

> Wave 2.0 Rollout Plan is COMPLETE, COMPREHENSIVE, IBWR-HARDENED, and READY FOR CS2 REVIEW.
>
> All 14 subwaves fully specified with explicit builder assignments, sequencing, dependencies, and deliverables.
>
> No individual builder issues created yet (as required).

**Date:** 2026-01-05  
**Authority:** FM Execution Mandate (T0-013)  
**Version:** FM Agent Contract v3.3.0

---

**END OF QUICK REFERENCE**
