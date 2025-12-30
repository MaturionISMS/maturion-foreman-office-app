# Wave 1.0 — Architecture Freeze + QA-to-Red Compilation + Build-to-Green Task Distribution

**Version:** 1.0.0 (Corrected)  
**Status:** Governance-Compliant Plan  
**Authority:** Maturion Foreman (FM)  
**Date:** 2025-12-30  
**Wave:** 1.0 (Production Implementation)

---

## Document Purpose

This document defines the **corrected Wave 1.0 execution plan** for the Maturion Foreman Office App, following the **canonical build pipeline**:

1. **Architecture Freeze** (Phase A) — Confirm architecture as canonical build target
2. **QA-to-Red Compilation** (Phase B) — Tests that fail until implementation exists
3. **Build-to-Green Task Distribution** (Phase C) — Implementation work per builder

**Previous invalid plan (withdrawn):** Violated governance by skipping architecture freeze and QA-to-Red compilation.

**This corrected plan:** Follows BUILD_PHILOSOPHY.md and governance standards.

---

## I. Governance Correction Acknowledgment

### CS2 Feedback (Comment 3698461021)

> "STOP: Current Wave 1.0 plan is invalid due to governance sequencing drift. Non-negotiable build pipeline:
> 1) Architecture must be frozen/confirmed as canonical build target
> 2) QA-to-Red must be compiled (tests/gates that fail until build-to-green work is done)
> 3) Builders only receive build-to-green tasks (implementation), distributed by FM in waves"

### FM Response

- ✅ Invalid Wave 1.0 plan withdrawn
- ✅ Governance sequencing understood and enforced
- ✅ Corrected plan follows canonical pipeline
- ✅ Builder PR merge gates included
- ✅ Architecture freeze precedes all implementation
- ✅ QA-to-Red precedes all build-to-green work

---

## II. Canonical Build Pipeline (Authority)

### Source Authority

- **BUILD_PHILOSOPHY.md** — Supreme constitutional authority
- **foreman/qa/dp-red-registry-spec.md** — DP-RED (Design-Phase RED) specification
- **architecture/FM_ARCHITECTURE_EXECUTION_CONTRACT.md** — Architecture freeze authority

### Pipeline Sequence (NON-NEGOTIABLE)

```
Phase A: Architecture Freeze
  ↓ (MUST complete before Phase B)
Phase B: QA-to-Red Compilation
  ↓ (MUST complete before Phase C)
Phase C: Build-to-Green Task Distribution
  ↓ (Each task turns RED tests GREEN)
Final: All Tests GREEN (Wave 1.0 Complete)
```

**No implementation work may begin until:**
1. Architecture is frozen (Phase A complete)
2. QA-to-Red suite is compiled (Phase B complete)
3. Builder PR merge gates are configured (Task 1.C.1 complete)

---

## III. Phase A: Architecture Freeze (MANDATORY FIRST)

### Task 1.A: Architecture Freeze & Validation

**Duration:** 1-2 days  
**Builder:** None (FM orchestrates)

**Deliverables:**
1. Architecture Freeze Statement
2. Architecture Reference Index
3. Architecture Validation Report
4. Architecture Canonical Lock (git hash + signatures)

**Architecture to Freeze:**
- `architecture/FM_ARCHITECTURE_EXECUTION_CONTRACT.md`
- `docs/ui/FOREMAN_UI_COMPONENT_INVENTORY.md` (Wave 0.2)
- `foreman/builder/*.md` — Builder specifications
- `foreman/platform/*.md` — Platform specifications
- `APP_DESCRIPTION.md`, `BUILD_PHILOSOPHY.md`
- All architecture artifacts

**Acceptance Criteria:**
- ✅ All architecture documents catalogued
- ✅ Architecture 100% complete (no gaps, TODOs, TBDs)
- ✅ Architecture version locked with git hash
- ✅ FM signs freeze statement
- ✅ CS2 approves as canonical build target

---

## IV. Phase B: QA-to-Red Compilation (MANDATORY SECOND)

### Task 1.B: QA-to-Red Suite Compilation

**Duration:** 3-5 days  
**Builder:** qa-builder  
**Dependencies:** Task 1.A complete

**Deliverables:**
1. DP-RED Registry (`foreman/qa/dp-red-registry.json`)
2. Complete test suite (unit, integration, E2E) — all RED
3. Test coverage map (≥95% architecture coverage)
4. Red gate definitions
5. QA-to-Red validation report

**Test Categories (All Intentionally RED):**
1. Foundation Tests (~15 tests) — Project structure, TypeScript, CI
2. UI Component Tests (~20 tests) — Theme, navigation, all components
3. API & Backend Tests (~25 tests) — Builder registry API, PostgreSQL, Prisma
4. Builder Registry Tests (~12 tests) — Builder service, task assignment
5. Integration Tests (~18 tests) — UI→API→DB flows
6. Governance Tests (~10 tests) — Compliance dashboard, DAI generator
7. E2E Scenarios (~12 tests) — Complete user workflows

**Total:** ~112 tests, all RED, ≥95% architecture coverage

**Acceptance Criteria:**
- ✅ All tests compiled and registered in DP-RED registry
- ✅ Test coverage ≥95% of architecture
- ✅ All tests currently RED (confirmed)
- ✅ Zero test debt
- ✅ FM validates completeness
- ✅ CS2 approves QA-to-Red suite

---

## V. Phase C: Build-to-Green Task Distribution

### Builder PR Merge Gates (ENFORCED FOR ALL PRs)

1. ✅ All unit tests pass
2. ✅ All integration tests for modified code pass
3. ✅ No new DP-RED entries (unless authorized)
4. ✅ Code coverage ≥80% for changed code
5. ✅ ESLint/Prettier pass
6. ✅ TypeScript compilation pass
7. ✅ No security vulnerabilities
8. ✅ FM validation approval
9. ✅ At least one previously RED test now GREEN

**Gate Activation:** Configured in Task 1.C.1, enforced from Phase C start

---

### Build-to-Green Tasks (10 Tasks)

#### Task 1.C.1: Project Foundation & Scaffolding
- **Builder:** integration-builder
- **Makes GREEN:** ~15 foundation tests
- **Deliverables:** Next.js setup, TypeScript, ESLint, CI workflow with all 9 gates
- **PR Size:** ~500 lines | **Duration:** 2-3 days
- **Dependencies:** Tasks 1.A, 1.B complete

#### Task 1.C.2: Shared UI Components & Theme
- **Builder:** ui-builder
- **Makes GREEN:** ~20 UI component tests
- **Deliverables:** Theme provider, navigation, shared components (shadcn/ui), layouts
- **PR Size:** ~800 lines | **Duration:** 2-3 days
- **Dependencies:** Task 1.C.1

#### Task 1.C.3: Builder Registry Service & Database
- **Builder:** api-builder + schema-builder
- **Makes GREEN:** ~25 API + schema tests
- **Deliverables:** PostgreSQL schema, Builder registry API, CRUD operations, Prisma
- **PR Size:** ~1000 lines | **Duration:** 3-4 days
- **Dependencies:** Task 1.C.1

#### Task 1.C.4: Foreman Dashboard
- **Builder:** ui-builder
- **Makes GREEN:** ~15 dashboard tests
- **Deliverables:** Dashboard page, builder status display, activity feed, system health
- **PR Size:** ~1200 lines | **Duration:** 3-4 days
- **Dependencies:** Tasks 1.C.2, 1.C.3

#### Task 1.C.5: Task Assignment System
- **Builder:** ui-builder + api-builder
- **Makes GREEN:** ~20 task assignment tests
- **Deliverables:** Task assignment UI, task API, task schema, builder task queue
- **PR Size:** ~1500 lines | **Duration:** 4-5 days
- **Dependencies:** Tasks 1.C.2, 1.C.3

#### Task 1.C.6: Evidence Management System
- **Builder:** ui-builder + api-builder + schema-builder
- **Makes GREEN:** ~18 evidence tests
- **Deliverables:** Evidence storage API, evidence schema, evidence viewer, file uploads
- **PR Size:** ~1400 lines | **Duration:** 4-5 days
- **Dependencies:** Tasks 1.C.2, 1.C.3

#### Task 1.C.7: QA Results & Validation Display
- **Builder:** ui-builder + api-builder
- **Makes GREEN:** ~12 QA display tests
- **Deliverables:** QA results UI, test execution API, coverage display, red gate indicators
- **PR Size:** ~1000 lines | **Duration:** 3-4 days
- **Dependencies:** Tasks 1.C.2, 1.C.3, 1.C.4

#### Task 1.C.8: Governance Compliance Dashboard
- **Builder:** ui-builder + api-builder
- **Makes GREEN:** ~10 governance tests
- **Deliverables:** Governance dashboard, compliance monitoring API, authority boundary checks
- **PR Size:** ~900 lines | **Duration:** 3-4 days
- **Dependencies:** Tasks 1.C.2, 1.C.3

#### Task 1.C.9: DAI Generator & Build Wave Progress
- **Builder:** ui-builder + api-builder
- **Makes GREEN:** ~15 DAI + wave tracking tests
- **Deliverables:** DAI generator UI, DAI templates, wave progress UI, timeline visualization
- **PR Size:** ~1200 lines | **Duration:** 3-4 days
- **Dependencies:** Tasks 1.C.2, 1.C.3, 1.C.5

#### Task 1.C.10: E2E Integration Testing & QA-to-Green
- **Builder:** qa-builder
- **Makes GREEN:** ALL remaining RED tests
- **Deliverables:** E2E execution, QA-to-Green report, security scan, performance tests, zero DP-RED
- **PR Size:** ~700 lines | **Duration:** 2-3 days
- **Dependencies:** All Tasks 1.C.1-C.9

---

## VI. Execution Sequencing & Critical Path

```
Phase A (1-2d) → Phase B (3-5d) → 1.C.1 (2-3d)
                                     ↓
                          ┌──────────┴──────────┐
                       1.C.2 (2-3d)          1.C.3 (3-4d)
                          └──────────┬──────────┘
                                     ↓
                    ┌────────────────┼────────────────┐
                 1.C.4     1.C.5   1.C.6   1.C.7   1.C.8
                (3-4d)    (4-5d)  (4-5d)  (3-4d)  (3-4d)
                    └────────────────┼────────────────┘
                                     ↓
                                  1.C.9 (3-4d)
                                     ↓
                                  1.C.10 (2-3d)
```

**Parallel Opportunities:** Tasks 1.C.2/1.C.3 after 1.C.1; Tasks 1.C.4/1.C.5/1.C.6/1.C.8 after 1.C.2+1.C.3

---

## VII. Timeline Estimates

| Scenario | Phase A | Phase B | Phase C | Total |
|----------|---------|---------|---------|-------|
| **Optimistic** | 1d | 3d | 14d | **18d (~3 weeks)** |
| **Realistic** ⭐ | 2d | 4d | 21d | **27d (~4 weeks)** |
| **Conservative** | 2d | 5d | 35d | **42d (~6 weeks)** |

---

## VIII. Success Criteria

### Phase A: Architecture Freeze
- ✅ Architecture freeze statement signed
- ✅ Architecture 100% complete
- ✅ Architecture version locked
- ✅ CS2 approves

### Phase B: QA-to-Red
- ✅ All tests registered in DP-RED registry
- ✅ Test coverage ≥95%
- ✅ All tests RED
- ✅ Zero test debt
- ✅ FM validates, CS2 approves

### Phase C: Build-to-Green
- ✅ All 10 tasks complete
- ✅ ALL tests GREEN (zero DP-RED)
- ✅ All PR merge gates passed
- ✅ Coverage ≥80%
- ✅ Zero critical vulnerabilities
- ✅ Architecture alignment validated

---

## IX. Governance Compliance

### Canonical Pipeline Followed ✅
1. Architecture Freeze FIRST
2. QA-to-Red Compilation SECOND
3. Build-to-Green THIRD
4. PR Merge Gates ENFORCED

### Authority Boundaries
- **FM:** Plan, validate, assign, approve (no GitHub ops)
- **Builders:** Compile QA, implement tasks (no PR ops)
- **CS2:** Approve phases, execute GitHub ops

---

## X. Technology Stack

**Frontend:** Next.js 14+ (TypeScript), React 18+, Tailwind CSS, shadcn/ui  
**Backend:** Node.js 20+, Next.js API Routes, PostgreSQL 15+, Prisma  
**Testing:** Jest, React Testing Library, Playwright  
**Infrastructure:** Git/GitHub, GitHub Actions CI/CD

---

## XI. Risk Assessment

### High Priority Risks
1. **QA-to-Red Suite Incomplete** — Mitigation: FM validates ≥95% coverage
2. **Builder PR Merge Gate Failures** — Mitigation: Gates configured early, training
3. **Architecture Gaps During QA-to-Red** — Mitigation: Thorough Phase A validation

---

## XII. Next Steps (Immediate)

**Awaiting CS2 confirmation:**
1. CS2 reviews corrected Wave 1.0 plan
2. CS2 approves governance-compliant sequencing
3. CS2 authorizes FM to begin **Phase A: Architecture Freeze**
4. FM executes architecture freeze
5. FM assigns **Task 1.B: QA-to-Red Compilation** to qa-builder
6. Wave 1.0 execution proceeds per plan

---

## XIII. Key Documents

**Wave 1.0 Plan:**
- [x] WAVE_1.0_EXECUTION_PLAN.md — This document

**Governance References:**
- BUILD_PHILOSOPHY.md
- foreman/qa/dp-red-registry-spec.md
- architecture/FM_ARCHITECTURE_EXECUTION_CONTRACT.md

---

**Status:** Wave 1.0 corrected plan complete, governance sequencing validated, awaiting CS2 approval

**Maturion Foreman**  
Planning and Sequencing Authority  
2025-12-30 06:55 UTC

---

**End of Wave 1.0 Execution Plan**
