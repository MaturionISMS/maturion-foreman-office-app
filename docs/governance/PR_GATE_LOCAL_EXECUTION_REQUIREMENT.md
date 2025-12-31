# PR-Gate Local Execution Requirement

**Document Type:** Governance Rule  
**Authority:** Corporate Governance Canon  
**Status:** ACTIVE  
**Effective Date:** 2025-12-31  
**Severity:** MANDATORY

---

## Purpose

This document establishes the **mandatory requirement** for agents to execute all PR-gate workflows locally before initiating handover.

---

## The Rule (Explicit and Unambiguous)

**All PR-gate workflows MUST be executed locally by the agent before handover.**

The agent MUST:

1. **Identify all PR-gate workflows** for the current repository
2. **Execute each workflow locally** using the same scripts CI uses
3. **Verify all gates return GREEN** (exit code 0)
4. **Inspect logs** for each gate execution
5. **Document results** in PREHANDOVER_PROOF
6. **Provide evidence** of local execution

**Handover is FORBIDDEN unless all of the above steps are complete.**

---

## What This Means

### Before This Rule

- Agent could push changes and wait for CI
- Agent could rely on CI-first verification
- Local execution was optional/implicit
- Evidence was not required

### After This Rule

- Agent MUST run gates locally FIRST
- Agent MUST verify GREEN locally BEFORE pushing
- Local execution is MANDATORY
- Evidence is REQUIRED for handover

---

## Rationale

### Why Local Execution First?

1. **Faster Feedback** — Catch issues immediately, not after CI delay
2. **Governance Chain of Custody** — Agent owns verification, CI confirms
3. **Reduced CI Load** — Don't push broken changes
4. **Agent Accountability** — Agent attests to local verification
5. **Mechanical Enforcement** — Evidence requirement blocks handover

### Why Not Just Rely on CI?

CI is **confirmatory**, not **diagnostic**:

- CI confirms what agent already verified
- CI detects drift between local and CI environments
- CI provides independent validation
- CI does NOT replace agent responsibility

**The agent is the first line of defense.**

---

## Workflow-by-Workflow Requirements

### For Each PR-Gate Workflow

The agent must:

1. **Read the workflow YAML** (`.github/workflows/*.yml`)
2. **Identify the validation script** called by the workflow
3. **Run the script locally** with same parameters as CI
4. **Capture the output** (stdout, stderr, exit code)
5. **Verify exit code 0** (GREEN)
6. **Inspect logs** for warnings or issues
7. **Document in PREHANDOVER_PROOF**

---

## Required Evidence Format

### PREHANDOVER_PROOF Must Include

```markdown
## Local PR-Gate Execution Evidence

### Gate: Agent QA Boundary Enforcement
- **Script:** `governance/scripts/validate_agent_boundaries.py`
- **Command:** `python3 governance/scripts/validate_agent_boundaries.py --reports "." --current-repo "MaturionISMS/maturion-foreman-office-app"`
- **Exit Code:** 0 ✅
- **Result:** PASS - No QA reports found (acceptable for governance-only change)
- **Log Summary:** No QA report files found in repository. This is correct for governance/documentation changes.

### Gate: Build-to-Green Enforcement
- **Script:** `foreman/scripts/detect-test-debt.py`
- **Command:** `python3 foreman/scripts/detect-test-debt.py --test-dir tests`
- **Exit Code:** 0 ✅
- **Result:** PASS - No test debt detected
- **Log Summary:** All tests valid, no skip markers, no TODO comments.

[... continue for all gates ...]

### Attestation

I, [Agent Name], attest that:
- All PR-gate workflows were executed locally
- All gates returned GREEN (exit code 0)
- All logs were inspected
- No issues were found
- This evidence is accurate and complete

**Handover is authorized based on local verification.**
```

---

## Enforcement

### Mechanical Enforcement

1. **Template Requirement** — PREHANDOVER_PROOF must use template
2. **Evidence Completeness Check** — All gates must be documented
3. **Attestation Required** — Agent must explicitly attest
4. **Handover Blocker** — Missing evidence = no handover

### Manual Enforcement (Until Automation)

1. CS2 reviews PREHANDOVER_PROOF before accepting PR
2. Missing evidence = handover invalidated
3. Incomplete evidence = handover rejected
4. False attestation = escalation to Johan

---

## Exceptions

### When Local Execution May Be Skipped

**NONE.**

There are **no exceptions** to this rule.

If a gate cannot be run locally due to:
- Missing dependencies
- Environment constraints
- Infrastructure issues

Then the agent MUST:
1. Document the blocker
2. Escalate to Johan
3. Request temporary override (bounded + time-limited)
4. Await explicit approval

**The agent may NOT proceed without approval.**

---

## Consequences of Non-Compliance

### First Offense
- Handover invalidated
- RCA required
- Corrective action plan required

### Second Offense
- Handover invalidated
- Agent contract review
- Additional training required

### Third Offense
- Handover invalidated
- Agent suspension pending review
- Escalation to Johan for determination

---

## Related Documents

- `.agent/instructions.md` — Agent contract
- `.agent/PREHANDOVER_PROOF_TEMPLATE.md` — Evidence template
- `ROOT_CAUSE_ANALYSIS_GOV_RCA_AGENT_QA_BOUNDARY_001.md` — Incident that led to this rule

---

## Version History

- **v1.0 (2025-12-31):** Initial creation following GOV-RCA-AGENT-QA-BOUNDARY-001

---

**This rule is MANDATORY and ENFORCEABLE.**

**No agent may hand over without complying with this rule.**

---

*END OF GOVERNANCE RULE*
