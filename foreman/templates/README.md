# QA Report Templates - Agent-Scoped QA Boundaries

**Status**: Authoritative  
**Last Updated**: 2025-12-31  
**Authority**: Corporate Governance Canon

---

## Purpose

These templates enforce **agent-scoped QA boundaries**, a constitutional governance invariant that ensures strict separation of duties in QA execution.

**Critical Rule**: Each agent type has exclusive QA responsibility for its domain. Cross-agent QA execution is a **catastrophic governance violation**.

---

## Available Templates

### 1. Builder QA Report

**Location**: `foreman/builder/templates/`
- `builder-qa-report-template.json` - Template for builder QA reports
- `builder-qa-report-schema.json` - JSON schema for validation

**Used By**: Builder agents (ui-builder, api-builder, schema-builder, integration-builder, qa-builder)

**Scope**: Implementation correctness within agent's responsibility domain
- ✅ Functional correctness (features work as specified)
- ✅ Schema correctness (data models match architecture)
- ✅ UI correctness (UI matches specifications)
- ✅ Unit tests, integration tests, E2E tests
- ❌ Governance compliance validation (use Governance QA)
- ❌ FM app runtime behavior (use FM QA)

**Repository**: Any ISMS module repository (e.g., `MaturionISMS/isms-*`)

---

### 2. FM QA Report

**Location**: `foreman/templates/`
- `fm-qa-report-template.json` - Template for FM QA reports
- `fm-qa-report-schema.json` - JSON schema for validation

**Used By**: FM agents (fm-builder, fm-agent)

**Scope**: FM application correctness and runtime behavior
- ✅ FM app feature correctness
- ✅ FM orchestration logic
- ✅ FM dashboard functionality
- ✅ FM enforcement workflows
- ✅ FM integration with governance
- ❌ Builder implementation QA (use Builder QA)
- ❌ Governance policy compliance (use Governance QA)

**Repository**: `maturion-foreman-office-app` (this repository only)

---

### 3. Governance QA Report

**Location**: `foreman/templates/`
- `governance-qa-report-template.json` - Template for Governance QA reports
- `governance-qa-report-schema.json` - JSON schema for validation

**Used By**: Governance agents (governance-administrator, governance-liaison)

**Scope**: Governance compliance and canonical alignment
- ✅ Governance artifact schema compliance
- ✅ Governance invariant enforcement
- ✅ Policy compliance validation
- ✅ Constitutional rule enforcement
- ✅ Canonical alignment verification
- ❌ Implementation correctness (use Builder QA)
- ❌ Feature functionality (use Builder QA)
- ❌ FM app runtime behavior (use FM QA)

**Repository**: `maturion-foreman-governance` only

---

## Required Metadata Structure

All QA reports MUST include a `qa_report_metadata` section for agent boundary enforcement:

```json
{
  "qa_report_metadata": {
    "agent_type": "<builder|fm|governance>",
    "agent_id": "<specific-agent-id>",
    "agent_version": "1.0.0",
    "scope": "<builder-qa|fm-qa|governance-qa>",
    "repository": "<repository-name>",
    "timestamp": "ISO-8601-timestamp"
  }
}
```

### Valid Combinations

| Agent Type | Valid agent_id Values | Valid scope | Valid repository |
|------------|----------------------|-------------|------------------|
| `builder` | ui-builder, api-builder, schema-builder, integration-builder, qa-builder | `builder-qa` | Any ISMS module repo |
| `fm` | fm-builder, fm-agent | `fm-qa` | `maturion-foreman-office-app` |
| `governance` | governance-administrator, governance-liaison | `governance-qa` | `maturion-foreman-governance` |

**Any other combination is a catastrophic governance violation.**

---

## Validation

QA reports are automatically validated by the **Agent QA Boundary Enforcement** CI workflow:

**Workflow**: `.github/workflows/agent-boundary-gate.yml`  
**Script**: `governance/scripts/validate_agent_boundaries.py`

### Local Validation

Test your QA report locally before committing:

```bash
python3 governance/scripts/validate_agent_boundaries.py \
  --reports "path/to/your-qa-report.json" \
  --current-repo "MaturionISMS/your-repo-name"
```

### Expected Output

**Success** (Exit code 0):
```
✅ ALL AGENT BOUNDARIES RESPECTED

All QA reports correctly attributed to appropriate agents.
No cross-agent QA execution detected.
```

**Failure** (Exit code 1):
```
❌ AGENT BOUNDARY VIOLATIONS DETECTED

🚨 CATASTROPHIC VIOLATIONS (Immediate Escalation Required):
  Type: CROSS_AGENT_QA_EXECUTION
  Message: builder agent executed governance-qa (prohibited)

This is a CATASTROPHIC governance violation.
Merge is BLOCKED until violation resolved.
```

---

## Usage Instructions

### For Builder Agents

1. Copy `foreman/builder/templates/builder-qa-report-template.json`
2. Fill in all required fields:
   - Set `agent_id` to your specific builder ID (e.g., "ui-builder")
   - Set `repository` to the ISMS module repo name
   - Set `timestamp` to current ISO-8601 timestamp
   - Update `test_summary` with actual test results
   - Update `gate_compliance` with compliance status
3. Save as `<module>-qa-report.json` in your evidence directory
4. Validate locally before committing
5. Commit to your PR

### For FM Agents

1. Copy `foreman/templates/fm-qa-report-template.json`
2. Fill in all required fields:
   - Set `agent_id` to "fm-builder" or "fm-agent"
   - Repository is fixed: "maturion-foreman-office-app"
   - Update test results and FM-specific metrics
3. Save in evidence directory
4. Validate locally
5. Commit to PR

### For Governance Agents

1. Copy `foreman/templates/governance-qa-report-template.json`
2. Fill in all required fields:
   - Set `agent_id` to "governance-administrator" or "governance-liaison"
   - Repository is fixed: "maturion-foreman-governance"
   - Update compliance summary
3. Save in governance evidence directory
4. Validate locally
5. Commit to PR

---

## Violation Handling

If the Agent QA Boundary Enforcement gate fails:

1. **HALT** all related work immediately
2. **IDENTIFY** which agent executed wrong QA scope
3. **REMOVE** violating QA report(s)
4. **EXECUTE** QA in correct agent scope using correct template
5. **UPDATE** agent contract to prevent recurrence
6. **ESCALATE** to @JohanRas788

**Merge is BLOCKED until violation resolved.**

---

## References

- Governance Canon: `governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`
- Two-Gatekeeper Model: `governance/alignment/TWO_GATEKEEPER_MODEL.md`
- PR Gate Failure Handling: `governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md`
- Validation Script: `governance/scripts/validate_agent_boundaries.py`
- CI Workflow: `.github/workflows/agent-boundary-gate.yml`

---

**Authority**: Corporate Governance Canon  
**Enforcement**: Automatic via CI (no override permitted)  
**Violation Severity**: Catastrophic (requires immediate escalation)
