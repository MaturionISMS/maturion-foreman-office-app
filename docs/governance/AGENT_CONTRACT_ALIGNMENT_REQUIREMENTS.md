# Agent Contract Alignment Requirements

**Status:** Governance Specification  
**Authority:** Foreman Governance  
**Source:** Issue #69 (C2) — Bucket D Intent Consolidation  
**Last Updated:** 2025-12-29

---

## Purpose

This specification defines the **permanent governance requirement** for maintaining alignment between agent contracts across all repositories in the Maturion ecosystem.

Agent contracts (`.github/agents/*.md` and `agent.yaml`) encode agent identity, authority, and behavioral constraints. Misalignment between contracts creates governance drift, ambiguous authority boundaries, and execution failures.

This document establishes the rules and mechanisms to ensure agent contracts remain synchronized with canonical governance definitions.

---

## Core Principle

**Agent contracts are projections of governance, not independent definitions.**

- Governance defines the canonical authority model
- Agent contracts express that model in machine-readable form
- Contracts must be kept synchronized with governance source of truth
- Drift between governance and contracts is a governance failure

---

## Scope

This requirement applies to:

### Repositories in Scope
1. **maturion-foreman-office-app** (FM App) — Foreman's execution environment
2. **maturion-foreman** (Governance Repo) — Canonical governance definitions
3. Any future ISMS module repositories with autonomous agent execution
4. Any builder agent repositories if separated in the future

### Agent Contracts in Scope
- `.github/agents/*.md` — Agent instruction files
- `agent.yaml` — Agent metadata and configuration (if present)
- Builder agent contracts (UI, API, Schema, Integration, QA builders)
- Foreman agent contract (supervisory/orchestration agent)
- Any custom or domain-specific agents introduced in future

---

## Alignment Requirements

### Requirement 1: Canonical Governance Source of Truth

**Rule:**  
The `maturion-foreman` governance repository is the **single source of truth** for:
- Agent authority models (POLC model)
- Role boundaries and responsibilities
- Build philosophy and governance principles
- QA governance and compliance requirements

**Enforcement:**  
Agent contracts in FM App and other repos must **derive from** and **reference** canonical governance in the foreman repo.

**Validation:**  
- Agent contracts include explicit references to governance source documents
- Contract updates require verification against current governance
- No contract may define authority or behavior that contradicts governance

---

### Requirement 2: Cross-Repo Contract Consistency

**Rule:**  
Agent contracts for the same agent type must be **consistent across repositories**.

**Example:**  
If the QA Builder agent contract in the FM App defines QA coverage thresholds, and a future ISMS module repo has a QA Builder, both must use the same thresholds unless governance explicitly authorizes repo-specific overrides.

**Enforcement:**  
- Contract alignment sweep performed when governance changes
- Automated checks compare contracts across repos for consistency
- Divergence requires documented governance approval

---

### Requirement 3: Alignment Sweep on Governance Updates

**Rule:**  
When canonical governance is updated in `maturion-foreman`, an **alignment sweep** must be performed across all in-scope repositories.

**Alignment Sweep Procedure:**

1. **Identify Governance Change**
   - Monitor governance repo for commits to agent authority models
   - Detect changes to POLC definitions, role boundaries, or build philosophy

2. **Assess Impact**
   - Determine which agent contracts are affected
   - Identify repositories that need contract updates

3. **Update Agent Contracts**
   - Modify `.github/agents/*.md` files to reflect governance changes
   - Update agent behavior descriptions
   - Add references to updated governance documents

4. **Validate Alignment**
   - Run automated alignment checks
   - Verify no contradictions between governance and contracts
   - Confirm all references are current

5. **Document Alignment**
   - Record alignment sweep in governance audit log
   - Link updated contracts to triggering governance change

**Trigger Conditions for Alignment Sweep:**
- Major governance update (authority model change)
- POLC model refinement
- New agent type introduced
- Role boundary clarification
- Build philosophy or QA governance update

---

### Requirement 4: Contract Versioning and Traceability

**Rule:**  
Agent contracts must include **version metadata** and **governance references**.

**Required Metadata in Agent Contracts:**

```yaml
# Example for .github/agents/fm-repo-builder.md
---
name: FMRepoBuilder
version: 1.2.0
governance_version: 2024-12-29
governance_references:
  - maturion-foreman/foreman/builder/builder-capability-map.json
  - maturion-foreman/foreman/builder/builder-permission-policy.json
  - maturion-foreman/BUILD_PHILOSOPHY.md
last_aligned: 2025-12-29
alignment_status: current
---
```

**Enforcement:**
- Contracts without version metadata are flagged as non-compliant
- Alignment checks verify `governance_references` are valid and current
- `alignment_status` must be "current" before builds are authorized

---

### Requirement 5: Human Authority for Contract Divergence

**Rule:**  
Any intentional divergence from canonical governance requires **explicit human authority** (Johan Ras, CS2).

**Divergence Examples:**
- Repo-specific behavior override (e.g., different QA thresholds for experimental module)
- Temporary authority elevation during bootstrap
- Emergency governance bypass for critical fixes

**Approval Process:**
1. Document reason for divergence
2. Specify scope and duration of divergence
3. Obtain Johan approval
4. Add divergence annotation to agent contract
5. Schedule re-alignment after divergence period ends

---

## Alignment Validation Mechanisms

### Automated Alignment Checker

**Tool:** `validate-agent-alignment.py` (to be created)

**Functionality:**
- Compares agent contracts across all in-scope repositories
- Checks for consistency in authority definitions
- Validates governance references are current and reachable
- Detects missing metadata or version drift

**Run Frequency:**
- Pre-commit check in governance repo
- Pre-build check in FM App
- Weekly scheduled audit

**Output:**
- Alignment report (JSON format)
- List of misaligned contracts
- Recommended corrective actions

### Manual Alignment Audit

**Frequency:** Quarterly (or after major governance changes)

**Procedure:**
1. Review all agent contracts across repos
2. Verify alignment with current governance
3. Check for undocumented divergences
4. Update alignment status metadata
5. Report findings to Johan

---

## Integration with Build Authorization Gate

**Rule:**  
The Build Authorization Gate (FR-1.2) must validate agent contract alignment before authorizing builds.

**Gate Check:**
- Verify all relevant agent contracts have `alignment_status: current`
- Ensure governance references are valid
- Confirm no expired alignment dates
- Check for documented divergences with valid approval

**Failure Behavior:**
- If alignment check fails, gate returns FAIL
- Build is blocked until alignment is corrected
- Evidence of alignment failure is logged

---

## Lifecycle Management

### When New Agents Are Introduced

1. **Define Agent Contract**
   - Create contract based on canonical governance
   - Include all required metadata
   - Reference relevant governance documents

2. **Validate Alignment**
   - Run alignment checker
   - Verify consistency with existing agent contracts
   - Obtain governance approval for new agent type

3. **Register Agent**
   - Add agent to builder capability map
   - Update permission policy
   - Document in governance repo

### When Governance Changes

1. **Trigger Alignment Sweep**
   - Identify affected contracts
   - Schedule updates across repos

2. **Update Contracts**
   - Modify contracts to reflect governance changes
   - Update version and alignment metadata

3. **Validate & Test**
   - Run alignment checker
   - Test agents with updated contracts
   - Verify behavior matches governance intent

4. **Document Change**
   - Update governance changelog
   - Link contracts to governance update

### When Contracts Drift

1. **Detect Drift**
   - Automated checker identifies misalignment
   - Manual audit discovers divergence

2. **Assess Severity**
   - Critical: Blocks builds immediately
   - High: Requires correction within 1 sprint
   - Medium: Scheduled for next alignment sweep

3. **Correct Drift**
   - Update drifted contracts
   - Verify governance source is correct
   - Re-run alignment validation

4. **Prevent Recurrence**
   - Investigate root cause of drift
   - Strengthen alignment checks if needed
   - Update alignment procedures

---

## Success Criteria

Agent contract alignment is successful when:

1. **Zero Governance Contradictions**
   - No agent contract contradicts canonical governance
   - All authority boundaries are consistently defined

2. **Timely Synchronization**
   - Contracts are updated within 2 weeks of governance changes
   - Alignment sweeps are completed within 1 sprint

3. **Transparent Traceability**
   - Every contract has clear governance references
   - Alignment history is auditable

4. **Minimal Divergence**
   - Divergences are rare and well-justified
   - Temporary divergences are resolved on schedule

---

## Responsibilities

### Foreman (FM Agent)
- Monitor governance repo for updates
- Trigger alignment sweeps when governance changes
- Validate alignment before build authorization
- Report alignment failures through watchdog system

### Builder Agents
- Operate within authority defined in contracts
- Flag contract ambiguities or contradictions
- Request alignment updates when governance is unclear

### Johan Ras (CS2)
- Approve governance updates
- Authorize intentional contract divergences
- Review alignment audit reports
- Resolve conflicts between governance and contracts

### Governance Repo Maintainer
- Maintain canonical governance definitions
- Ensure governance is clear and unambiguous
- Document changes with impact assessments
- Trigger alignment sweeps after major updates

---

## Future Extensions

Potential enhancements after v1:

- **Automated Contract Generation:** Generate agent contracts directly from governance definitions
- **Real-Time Alignment Monitoring:** Continuous alignment validation during runtime
- **Cross-Org Alignment:** Extend to other organizations using Maturion model
- **Semantic Alignment Validation:** AI-powered check for semantic consistency beyond syntactic matching

---

## References

- **Source Issue:** #69 (C2) — agent.md Alignment Sweep (MANDATORY)
- **Related Governance:** POLC Model (maturion-foreman repository)
- **Related Architecture:** True North FM Architecture Section 2.2 (Authority Boundaries)
- **Builder Contracts:** maturion-foreman/foreman/builder/builder-capability-map.json
- **Bucket D Classification:** BACKLOG_CONSOLIDATION_REPORT.md

---

**Document Status:** CANONICAL  
**Implementation Status:** PARTIAL (FM App contracts aligned, automated checker not yet implemented)  
**Next Action:** Create `validate-agent-alignment.py` tool and integrate with Build Authorization Gate
