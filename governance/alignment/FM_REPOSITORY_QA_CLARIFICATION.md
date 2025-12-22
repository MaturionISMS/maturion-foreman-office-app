# FM Repository QA Clarification

**Status**: Clarification  
**Last Updated**: 2025-12-22  
**Authority**: Governance Alignment Issue  
**Purpose**: Clarify FM QA vs Builder QA distinction

---

## I. The Distinction

### FM Repository (maturion-foreman-office-app)

**QA Type**: FM QA  
**Who Executes**: FM agents (FM Builder)  
**What is Tested**: FM application functionality
- FM orchestration logic
- FM enforcement workflows  
- FM monitoring capabilities
- FM dashboard functionality
- FM integration with governance

**QA Execution**:
- FM runs its own tests via `npm test` (FM QA)
- Build-to-Green Enforcement workflow validates FM QA
- This is NOT Builder QA (different scope)
- This is FM validating itself

**Gate Behavior**:
- `build-to-green-enforcement.yml` runs FM tests (acceptable)
- `builder-qa-gate.yml` finds no Builder QA Report (expected, not applicable)
- `agent-boundary-gate.yml` validates any QA reports are FM QA (correct)

---

### ISMS Module Repositories (isms-*, maturion-isms-*)

**QA Type**: Builder QA  
**Who Executes**: Builder agents (UI Builder, API Builder, etc.)  
**What is Tested**: ISMS module implementation
- Module functionality
- Module integration
- Module compliance
- Module security
- Module UX

**QA Execution**:
- Builder agents run module tests
- Builder agents generate Builder QA Report
- Builder agents declare READY/NOT_READY
- FM gates validate report (do NOT re-run tests)

**Gate Behavior**:
- `builder-qa-gate.yml` validates Builder QA Report (enforcement-only)
- `agent-boundary-gate.yml` validates report authored by builder agent
- Gates do NOT run tests themselves

---

## II. Why FM Repository is Different

### FM Tests Itself

**Reason**: FM is the enforcement layer itself.

FM cannot delegate its own QA to external Builder agents because:
1. FM orchestrates builders (cannot be orchestrated by builders)
2. FM enforces governance (cannot be validated by builders)
3. FM monitors runtime (cannot be monitored by builders)
4. FM is self-contained (no external builders exist for FM)

**Therefore**: FM runs its own QA (FM QA) internally.

---

### FM QA ≠ Builder QA

| Aspect | FM QA | Builder QA |
|--------|-------|------------|
| **Repository** | maturion-foreman-office-app | isms-*, maturion-isms-* |
| **Agent Type** | FM agents | Builder agents |
| **Scope** | fm-qa | builder-qa |
| **Tests** | FM orchestration, enforcement, monitoring | Module implementation |
| **Execution** | FM runs own tests | Builder runs module tests |
| **Report** | FM QA results (internal) | Builder QA Report (canonical) |
| **Gate Validation** | Build-to-Green validates FM tests | Builder QA Gate validates report only |

---

## III. Canonical Alignment Status

### FM Repository Compliance

**Build-to-Green Enforcement Workflow**:
- ✅ Runs FM tests (acceptable - FM QA)
- ✅ Validates test dodging patterns
- ✅ Enforces DP-RED governance
- ✅ Does NOT claim to be Builder QA
- ✅ Scope is FM QA, not Builder QA

**Status**: Compliant (FM QA, not Builder QA)

---

### Builder QA Gate Workflow

**Behavior in FM Repository**:
- ✅ Looks for Builder QA Report
- ✅ Finds none (expected)
- ✅ Reports "Not Applicable" (correct)
- ✅ Does NOT block merge (correct)
- ✅ Explains FM uses FM QA

**Behavior in ISMS Repositories**:
- ✅ Validates Builder QA Report presence
- ✅ Checks schema compliance
- ✅ Validates READY/NOT_READY status
- ✅ Does NOT re-run tests (enforcement-only)
- ✅ Trusts Builder declaration

**Status**: Compliant (enforcement-only)

---

### Agent Boundary Gate Workflow

**Behavior in FM Repository**:
- ✅ Validates any QA reports found
- ✅ Ensures FM QA attributed to FM agents
- ✅ Detects cross-agent QA violations
- ✅ Reports catastrophic if violation

**Behavior in ISMS Repositories**:
- ✅ Validates Builder QA Report attribution
- ✅ Ensures Builder QA by builder agents only
- ✅ Detects cross-agent QA violations
- ✅ Reports catastrophic if violation

**Status**: Compliant (agent-scoped enforcement)

---

## IV. No Governance Violation

### FM Running Own Tests is NOT a Violation

**Canonical Principle**: "Builder agents run Builder QA only"

**FM Application**: FM agents run FM QA only

**Key Point**: FM is not running Builder QA. FM is running FM QA (testing itself).

**Analogy**:
- Builder agents test ISMS modules (Builder QA)
- FM agents test FM app (FM QA)
- Governance agents test governance (Governance QA)

Each agent tests its own domain. This is correct.

---

### Enforcement-Only Applies to Cross-Repo Validation

**Enforcement-Only Principle**: "FM gates do NOT run Builder QA"

**FM Application**:
- ✅ FM gates do NOT run Builder QA (in ISMS repos)
- ✅ FM gates validate Builder QA Reports only (enforcement-only)
- ✅ FM gates trust Builder READY/NOT_READY declarations
- ✅ FM runs its own FM QA (testing FM app itself)

**Distinction**:
- Enforcement-only applies to validating other repos' Builder QA
- Does NOT prohibit FM from testing itself (FM QA)

---

## V. Canonical Model Alignment Summary

### Two-Gatekeeper Model

**Gatekeeper 1 (Governance Administrator)**:
- Validates governance artifacts
- Does NOT run Builder QA ✅
- Does NOT run FM QA ✅
- Enforcement-only ✅

**Gatekeeper 2 (FM Builder)**:
- Validates Builder QA Reports (enforcement-only) ✅
- Does NOT re-run Builder QA tests ✅
- Runs FM QA (tests FM app) ✅ (FM's own QA)
- Trusts Builder READY/NOT_READY ✅

**Status**: Aligned

---

### Agent-Scoped QA Boundaries

**Builder agents** → Builder QA only ✅  
**Governance agents** → Governance QA only ✅  
**FM agents** → FM QA only ✅

**Cross-agent QA** = Catastrophic violation ✅

**FM Repository**:
- FM agents run FM QA ✅ (correct scope)
- FM agents do NOT run Builder QA ✅
- FM agents do NOT run Governance QA ✅

**Status**: Aligned

---

### PR Gate Requirements

**Gate 1: Builder QA Report**:
- ISMS repos: Builder QA Report required
- FM repo: Not applicable (uses FM QA)
- Enforcement-only: Gates validate report, don't run tests

**Gate 2: Agent Boundaries**:
- All repos: Agent attribution validated
- FM repo: FM QA by FM agents
- ISMS repos: Builder QA by builder agents

**Gate 3: Build-to-Green**:
- All repos: 100% pass rate
- FM repo: FM tests pass 100%
- ISMS repos: Builder tests pass 100%

**Status**: Aligned

---

## VI. Action Items: None

**No changes required**.

FM repository governance structure is already aligned with canonical model:
- FM runs FM QA (correct)
- FM gates validate Builder QA Reports in ISMS repos (enforcement-only)
- Agent boundaries respected
- No CI-discovery logic
- No duplicate enforcement

**Governance alignment complete.**

---

## VII. References

- **PR Gate Requirements**: `/governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Agent-Scoped QA Boundaries**: `/governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`
- **Two-Gatekeeper Model**: `/governance/alignment/TWO_GATEKEEPER_MODEL.md`
- **Build-to-Green Enforcement**: `.github/workflows/build-to-green-enforcement.yml`
- **Builder QA Gate**: `.github/workflows/builder-qa-gate.yml`

---

**FM tests itself. Builders test modules. Governance tests governance. All correct.**

*END OF FM REPOSITORY QA CLARIFICATION*
