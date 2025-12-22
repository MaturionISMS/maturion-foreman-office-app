# Build Failure Telemetry Schema

**Status**: Required  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras  
**Wave**: 2.6 - FM Build Readiness

---

## I. Purpose

This schema defines the structure, categories, and tracking requirements for build failures to enable the FL/CI (Failure → Learning → Correction → Improvement) loop.

**Goal**: Transform every build failure into governance improvement and FM evolution.

---

## II. Core Principle

**Every failure is a learning opportunity.**

Build failures are not punished; they are analyzed, understood, prevented, and used to strengthen governance and FM capabilities.

---

## III. Failure Categories

### Category 1: Architecture Failures

**Definition**: Failures caused by incomplete, incorrect, or ambiguous architecture.

**Subcategories**:
1. `ARCHITECTURE_INCOMPLETE` - Architecture elements missing
2. `ARCHITECTURE_AMBIGUOUS` - Architecture elements unclear
3. `ARCHITECTURE_INCORRECT` - Architecture elements wrong
4. `ARCHITECTURE_DRIFT` - Implementation diverged from architecture
5. `ARCHITECTURE_CONFLICT` - Architecture elements contradict

**Root Cause Examples**:
- Missing interface definitions
- Unclear component responsibilities
- Incorrect data model specifications
- Undocumented integration patterns

---

### Category 2: QA Failures

**Definition**: Failures caused by inadequate, incorrect, or missing QA coverage.

**Subcategories**:
1. `QA_COVERAGE_INCOMPLETE` - Missing test coverage
2. `QA_ASSERTION_INCORRECT` - Test validates wrong thing
3. `QA_FALSE_POSITIVE` - Test passes when it should fail
4. `QA_FALSE_NEGATIVE` - Test fails when it should pass
5. `QA_UNMAPPED` - Tests don't trace to architecture
6. `QA_TEST_DEBT` - Skipped or disabled tests

**Root Cause Examples**:
- Unmapped architecture elements
- Incorrect test assertions
- Tests not updated after architecture changes
- Test data issues

---

### Category 3: Scope Failures

**Definition**: Failures caused by scope ambiguity, scope creep, or scope conflicts.

**Subcategories**:
1. `SCOPE_AMBIGUOUS` - Unclear what is in scope
2. `SCOPE_CREEP` - Scope expanded during build
3. `SCOPE_CONFLICT` - Requirements contradict
4. `SCOPE_INCOMPLETE` - Requirements missing
5. `SCOPE_NOT_FROZEN` - Scope changed after freeze

**Root Cause Examples**:
- Requirements not clearly scoped
- Requirements changed during build
- Hidden dependencies discovered mid-build

---

### Category 4: Infrastructure Failures

**Definition**: Failures caused by build environment, dependencies, or tooling issues.

**Subcategories**:
1. `INFRA_ENVIRONMENT` - Build environment issue
2. `INFRA_DEPENDENCY` - External dependency unavailable
3. `INFRA_TOOLING` - Build tool failure
4. `INFRA_RESOURCE` - Insufficient resources (CPU, memory, disk)
5. `INFRA_NETWORK` - Network connectivity issue
6. `INFRA_CREDENTIALS` - Authentication/authorization issue

**Root Cause Examples**:
- Missing build tools
- Dependency version conflicts
- Network timeout
- Insufficient disk space

---

### Category 5: Governance Conflict Failures

**Definition**: Failures caused by conflicting governance rules or governance enforcement gaps.

**Subcategories**:
1. `GOVERNANCE_RULE_CONFLICT` - Two governance rules contradict
2. `GOVERNANCE_INTERPRETATION` - Governance rule ambiguous
3. `GOVERNANCE_ENFORCEMENT_GAP` - Rule exists but not enforced
4. `GOVERNANCE_EXCEPTION_EXPIRED` - Temporary override expired
5. `GOVERNANCE_CHECKLIST_INCOMPLETE` - Checklist missing items

**Root Cause Examples**:
- Contradictory governance policies
- Unclear governance interpretation
- PR gate not enforcing rule
- Expired temporary waiver

---

### Category 6: Integration Failures

**Definition**: Failures caused by integration between modules, services, or systems.

**Subcategories**:
1. `INTEGRATION_API_MISMATCH` - API contract violated
2. `INTEGRATION_DATA_MISMATCH` - Data format mismatch
3. `INTEGRATION_TIMING` - Race condition or timing issue
4. `INTEGRATION_DEPENDENCY_ORDER` - Incorrect initialization order
5. `INTEGRATION_STATE_MISMATCH` - State synchronization issue

**Root Cause Examples**:
- API changed without updating clients
- Data serialization issues
- Async timing problems

---

### Category 7: Unknown/Other Failures

**Definition**: Failures that don't fit other categories or root cause is unclear.

**Subcategories**:
1. `UNKNOWN_ROOT_CAUSE` - Failure occurred but cause unknown
2. `OTHER_TRANSIENT` - Transient failure (e.g., random timeout)
3. `OTHER_EXTERNAL` - External system failure
4. `OTHER_NOVEL` - First-time failure type

---

## IV. Failure Record Schema

### Required Fields

```json
{
  "failure_id": "string (UUID)",
  "build_id": "string",
  "timestamp": "ISO-8601 timestamp",
  "category": "ARCHITECTURE | QA | SCOPE | INFRA | GOVERNANCE | INTEGRATION | UNKNOWN",
  "subcategory": "string (see subcategories above)",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW",
  "status": "OPEN | INVESTIGATING | RESOLVED | PREVENTED",
  
  "failure_description": {
    "summary": "string (1-2 sentences)",
    "details": "string (detailed description)",
    "error_message": "string (actual error output)",
    "stack_trace": "string (if applicable)",
    "logs_url": "string (link to logs)"
  },
  
  "context": {
    "phase": "AUTHORIZATION | COMPILATION | TESTING | INTEGRATION | DEPLOYMENT",
    "component": "string (affected component)",
    "file_path": "string (file where failure occurred)",
    "line_number": "integer (if applicable)"
  },
  
  "root_cause": {
    "analysis_status": "PENDING | IN_PROGRESS | COMPLETE",
    "root_cause_summary": "string",
    "contributing_factors": ["string"],
    "why_not_prevented": "string (why did preconditions not catch this?)"
  },
  
  "resolution": {
    "resolution_type": "FIX | ARCHITECTURE_CHANGE | GOVERNANCE_UPDATE | PREVENTION_ADDED",
    "resolution_description": "string",
    "resolution_commit": "string (commit SHA)",
    "resolution_pr": "string (PR number)",
    "resolution_timestamp": "ISO-8601 timestamp",
    "resolved_by": "string (person or system)"
  },
  
  "prevention": {
    "prevention_measures": ["string"],
    "governance_updates": ["string (files updated)"],
    "precondition_updates": ["string (which preconditions strengthened)"],
    "test_additions": ["string (new tests added)"],
    "documentation_updates": ["string (docs updated)"]
  },
  
  "repetition_tracking": {
    "is_repeat": "boolean",
    "previous_occurrence_ids": ["string (failure IDs)"],
    "repeat_count": "integer",
    "days_since_last_occurrence": "integer"
  },
  
  "learning": {
    "lessons_learned": ["string"],
    "governance_implications": "string",
    "fm_evolution_implications": "string",
    "propagation_required": "boolean (should this be shared to other repos?)",
    "propagation_status": "PENDING | IN_PROGRESS | COMPLETE"
  },
  
  "metadata": {
    "reporter": "string (person or system)",
    "owner": "string (assigned to)",
    "priority": "P0 | P1 | P2 | P3",
    "sla_resolution_target": "ISO-8601 timestamp",
    "tags": ["string"]
  }
}
```

---

## V. Severity Levels

### CRITICAL
- Build completely blocked
- Cannot proceed without resolution
- Production impact if not caught
- Immediate escalation required

**SLA**: Resolve within 4 hours

---

### HIGH
- Build blocked or significantly delayed
- Workaround may exist but not acceptable long-term
- Could impact production if not addressed
- Escalation recommended

**SLA**: Resolve within 24 hours

---

### MEDIUM
- Build degraded but can proceed
- No production impact expected
- Should be resolved before next build
- Standard priority

**SLA**: Resolve within 1 week

---

### LOW
- Minor issue or improvement opportunity
- No immediate impact
- Can be addressed in future build
- Tracked but not urgent

**SLA**: Resolve within 1 month

---

## VI. Failure Status Lifecycle

```
OPEN → INVESTIGATING → RESOLVED → PREVENTED
  ↓         ↓              ↓           ↓
  └─────────┴──────────────┴───────────┘
              (can reopen if recurs)
```

### OPEN
- Failure detected and recorded
- Awaiting root cause analysis
- Owner assigned

### INVESTIGATING
- Root cause analysis in progress
- Resolution being developed
- May include architecture/governance review

### RESOLVED
- Root cause identified
- Fix implemented and validated
- Failure no longer occurring

### PREVENTED
- Preconditions updated to prevent recurrence
- Governance strengthened
- Tests added to catch future occurrences
- Failure structurally impossible now

---

## VII. Root Cause Analysis Requirements

### Required Analysis

For each failure, root cause analysis MUST answer:

1. **What happened?**
   - Exact failure sequence
   - Error messages and symptoms
   - Impact and consequences

2. **Why did it happen?**
   - Root cause (not just proximate cause)
   - Contributing factors
   - Environmental factors

3. **Why wasn't it prevented?**
   - Which precondition should have caught it?
   - Why did precondition validation pass?
   - Gap in architecture/QA/governance?

4. **How do we prevent recurrence?**
   - Immediate fix
   - Precondition strengthening
   - Governance updates
   - Test additions

5. **What do we learn?**
   - Lessons for future builds
   - Governance implications
   - FM evolution needs

---

## VIII. Repetition Detection

### Repeat Failure Criteria

A failure is a "repeat" if:
1. Same category and subcategory
2. Same or similar root cause
3. Same or similar component/area
4. Occurred previously in last 90 days

### Repeat Failure Handling

**First Occurrence**:
- Standard resolution process
- Root cause analysis
- Prevention measures

**Second Occurrence** (Repeat):
- ⚠️ Escalation to build owner
- Why did prevention fail?
- Strengthen prevention measures
- Update governance

**Third Occurrence** (Double Repeat):
- 🚨 Escalation to Johan Ras
- Catastrophic prevention failure
- Mandatory governance review
- Mandatory precondition review
- Mandatory prevention verification

**Goal**: Learn from first occurrence, prevent second occurrence, never have third occurrence.

---

## IX. Relationship to Governance Improvement

### Failure → Governance Evolution

Each failure can trigger:

1. **Precondition Updates**
   - Strengthen authorization gate validation
   - Add new validation checks
   - Improve validation accuracy

2. **Governance Rule Updates**
   - Create new governance rules
   - Clarify existing rules
   - Resolve rule conflicts

3. **Checklist Updates**
   - Add checklist items
   - Clarify checklist requirements
   - Update checklist validation

4. **Documentation Updates**
   - Improve architecture templates
   - Add examples and anti-patterns
   - Update best practices

---

### FL/CI Loop (Failure → Learning → Correction → Improvement)

```
FAILURE
   ↓
ROOT CAUSE ANALYSIS
   ↓
LEARNING (lessons, patterns, gaps)
   ↓
CORRECTION (immediate fix)
   ↓
IMPROVEMENT (prevention measures)
   ↓
GOVERNANCE EVOLUTION (rules, preconditions, checklists)
   ↓
NEXT BUILD (structurally more correct)
```

---

## X. Relationship to FM Evolution

### Failure-Driven FM Capabilities

Build failures inform:

1. **FM Agent Intelligence**
   - What patterns indicate failure risk?
   - What preconditions need automation?
   - What validations need real-time feedback?

2. **FM Office Dashboard**
   - What failure metrics to display?
   - What failure trends to track?
   - What alerts to generate?

3. **FM Automation Priorities**
   - Which failures are most common?
   - Which failures are most costly?
   - Which failures are most preventable?

---

## XI. Evidence Storage

### Failure Record Storage

**Location**: `governance/events/failures/<failure-id>.json`

**Retention**: Indefinite

**Access**: Organization-wide

---

### Failure Analytics

Aggregate data stored in:
- `governance/events/failures/analytics/failure-trends.json`
- `governance/events/failures/analytics/failure-by-category.json`
- `governance/events/failures/analytics/repeat-failures.json`
- `governance/events/failures/analytics/mttr-metrics.json` (Mean Time To Resolution)

---

## XII. Failure Reporting Requirements

### Weekly Failure Report

**Contents**:
1. Total failures this week
2. Failures by category
3. Failures by severity
4. Repeat failures
5. MTTR (Mean Time To Resolution)
6. Prevention measures implemented
7. Governance updates made

**Audience**: Build owners, governance team, Johan Ras

---

### Monthly Failure Trends

**Contents**:
1. Failure trends over time
2. Most common failure categories
3. Repeat failure rate
4. Prevention effectiveness
5. Governance evolution summary
6. FM evolution priorities

**Audience**: Leadership, governance team

---

## XIII. Failure Prevention Verification

### Verification Requirements

When prevention measures are implemented, verify:

1. ✅ Precondition updated to catch this failure
2. ✅ Precondition validation passes on compliant builds
3. ✅ Precondition validation fails on non-compliant builds (test with known-bad case)
4. ✅ Governance documentation updated
5. ✅ Failure record marked PREVENTED

**Only mark failure as PREVENTED after verification complete.**

---

## XIV. Cross-Repository Propagation

### When to Propagate

Propagate failure lessons to other repositories if:
1. Failure is not FM-specific
2. Failure likely to occur in other repos
3. Prevention measures are generalizable
4. Governance update applies broadly

### Propagation Process

1. Identify affected repositories
2. Create propagation plan
3. Update governance canon (if applicable)
4. Notify repository owners
5. Assist with implementation
6. Verify propagation complete
7. Update failure record: `propagation_status: COMPLETE`

---

## XV. Machine Decidability

**This schema is designed to support automated failure analysis.**

Future FM Agent will:
- Auto-detect failures
- Auto-categorize failures
- Auto-generate failure records
- Auto-trigger root cause analysis
- Auto-detect repeat failures
- Auto-escalate on repeat failures
- Auto-suggest prevention measures

---

## XVI. Success Criteria

Failure telemetry is successful when:
1. ✅ All failures recorded
2. ✅ All failures categorized
3. ✅ Root cause analysis complete
4. ✅ Prevention measures implemented
5. ✅ Repeat failures eliminated
6. ✅ Governance continuously improving
7. ✅ Build quality increasing over time

---

## XVII. References

- **Corporate Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Build Authorization Gate**: `governance/build/BUILD_AUTHORIZATION_GATE.md`
- **Architecture Compilation Contract**: `governance/architecture/ARCHITECTURE_COMPILATION_CONTRACT.md`
- **QA Derivation & Coverage Rules**: `governance/qa/QA_DERIVATION_AND_COVERAGE_RULES.md`

---

*Build Failure Telemetry - Learn, Correct, Improve*
