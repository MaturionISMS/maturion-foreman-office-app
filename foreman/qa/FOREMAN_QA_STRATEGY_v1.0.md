# FOREMAN_QA_STRATEGY_v1.0.md

## Version: 1.0  
## Date: 2025-12-15

---

## 1. QA PHILOSOPHY

**Core Principle**: QA-to-Red before Build-to-Green

**Requirements**:
- QA designed BEFORE implementation
- QA must be RED (failing) before build starts
- QA must be GREEN (100% passing) before completion
- ZERO test debt permitted

---

## 2. TEST PYRAMID

```
          /\
         /E2E\        (10% - End-to-end workflows)
        /______\
       /        \
      /Integration\   (30% - Pipeline and engine integration)
     /____________\
    /              \
   /   Unit Tests   \ (60% - Domain logic and business rules)
  /__________________\
```

---

## 3. TEST COVERAGE BY LAYER

### 3.1 Domain Logic Tests (Unit - 60%)

**Programs, Waves, Tasks, Builders, Blockers Models**:
- ✅ State machine transitions
- ✅ Business rule enforcement (BR-1 through BR-7)
- ✅ Progress calculations
- ✅ Domain constraints
- ✅ Invariant validation

**Test Count**: ~150 tests

**Coverage Target**: 100% of domain logic

### 3.2 Decision Pipeline Tests (Integration - 30%)

**Architecture Validation Pipeline**:
- ✅ Document existence check
- ✅ Checklist validation execution
- ✅ Pass rate calculation
- ✅ Build readiness determination

**QA Validation Pipeline**:
- ✅ QA suite existence check
- ✅ QA execution
- ✅ RED status validation
- ✅ Test debt detection

**Task Assignment Pipeline**:
- ✅ Governance pre-check
- ✅ Architecture validation
- ✅ QA validation
- ✅ Builder selection
- ✅ Instruction generation

**Task Completion Validation Pipeline**:
- ✅ Final QA execution
- ✅ 100% pass validation
- ✅ Test debt re-check
- ✅ Build quality checks
- ✅ Evidence completeness

**Stall Detection Pipeline**:
- ✅ Heartbeat monitoring
- ✅ Stall classification
- ✅ Recovery strategy selection
- ✅ Recovery execution

**Governance Violation Detection Pipeline**:
- ✅ Continuous monitoring
- ✅ Violation classification
- ✅ Automatic halt
- ✅ Blocker creation
- ✅ Escalation

**Test Count**: ~80 tests

**Coverage Target**: 100% of pipeline stages

### 3.3 Workflow Tests (End-to-End - 10%)

**Program Initiation Workflow**:
- ✅ Johan defines intent
- ✅ Foreman creates program
- ✅ Foreman decomposes into waves/tasks
- ✅ Foreman validates architecture
- ✅ Foreman creates QA-to-Red
- ✅ Johan approves plan
- ✅ Program execution begins

**Task Execution Workflow**:
- ✅ Task assigned to builder
- ✅ Builder receives instruction
- ✅ Builder executes build
- ✅ Builder reports progress
- ✅ Builder claims completion
- ✅ Foreman validates completion
- ✅ Task marked completed

**Blocker Resolution Workflow**:
- ✅ Blocker detected
- ✅ Blocker escalated to Johan
- ✅ Johan provides resolution
- ✅ Foreman executes resolution
- ✅ Execution resumes

**Test Count**: ~20 tests

**Coverage Target**: All critical user workflows

---

## 4. TEST DATA REQUIREMENTS

### 4.1 Sample Programs
- Simple program (1 wave, 3 tasks)
- Complex program (3 waves, 10 tasks)
- Program with dependencies between waves

### 4.2 Sample Architecture Documents
- Complete architecture (passes 100% checklist)
- Incomplete architecture (fails checklist)
- Architecture with missing sections

### 4.3 Sample QA Suites
- RED QA suite (all tests failing)
- GREEN QA suite (all tests passing)
- QA suite with test debt

### 4.4 Sample Builders
- Mock builders (local, hosted, burst)
- Builder that sends heartbeats
- Builder that stalls (for stall detection tests)

---

## 5. TEST ENVIRONMENT REQUIREMENTS

### 5.1 Database
- PostgreSQL test database
- Migrations applied
- Clean state before each test

### 5.2 External Services (Mocked)
- GitHub API (mocked)
- Builder backends (mocked)
- Memory Fabric (mocked)

### 5.3 Test Frameworks
- **Unit Tests**: pytest (Python) or Jest (TypeScript)
- **Integration Tests**: pytest with database fixtures
- **E2E Tests**: Playwright or Cypress

---

## 6. MINIMUM COVERAGE THRESHOLDS

- **Unit Tests**: 100% of domain logic
- **Integration Tests**: 100% of pipeline stages
- **E2E Tests**: 100% of critical user workflows
- **Overall Code Coverage**: ≥95%

**Enforcement**: CI pipeline blocks merge if coverage < 95%

---

## 7. TEST CATEGORIES

### 7.1 Positive Tests (Happy Path)
- All business rules followed
- All validations pass
- Expected outcomes achieved

### 7.2 Negative Tests (Error Cases)
- Business rule violations
- Validation failures
- Error handling

### 7.3 Edge Cases
- Empty programs (no waves)
- Single-task waves
- Concurrent task execution
- Builder failures during execution

### 7.4 Performance Tests
- Large programs (100+ tasks)
- High-frequency heartbeats
- Concurrent builder execution

---

## 8. QUALITY GATES

### Gate 1: Unit Tests Pass
- All domain logic tests pass
- Code coverage ≥95%

### Gate 2: Integration Tests Pass
- All pipeline tests pass
- Integration coverage ≥95%

### Gate 3: E2E Tests Pass
- All workflow tests pass
- No flaky tests

### Gate 4: Zero Test Debt
- No .skip(), .todo(), commented tests
- No incomplete tests
- No stub test infrastructure

---

## 9. CI/CD INTEGRATION

**On PR Creation**:
1. Run unit tests
2. Run integration tests
3. Calculate coverage
4. Block merge if coverage < 95%

**On PR Merge**:
1. Run full test suite (including E2E)
2. Deploy to staging
3. Run smoke tests
4. Deploy to production (manual approval)

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
