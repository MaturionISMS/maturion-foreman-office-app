# FM Governance Adoption Policy

**Status**: Foundation  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras

---

## I. Purpose

This policy defines how corporate governance rules become execution constraints within the FM repository.

**Critical Principle**: FM executes governance; FM does not create governance.

---

## II. Adoption Model

### Governance Flow

```
Corporate Governance Canon (maturion-foreman-governance)
                    ↓
            [Translation Layer]
          (Governance Liaison)
                    ↓
       FM Execution Constraints
      (PR Gates, Builder Rules)
                    ↓
            FM Builder Execution
           (Build-to-Green)
                    ↓
      Future: FM Agent Mechanization
    (Real-time Enforcement + Dashboard)
```

### Translation Rules

1. **Direct Translation Only**
   - Governance rules are translated into execution constraints
   - No interpretation
   - No reduction
   - No extension beyond governance intent

2. **Constraint Types**
   - **PR Gate Rules**: Automated checks that must pass before merge
   - **Builder Contract Rules**: Requirements FM Builder must satisfy
   - **Validation Rules**: Checks run during build process
   - **Evidence Rules**: Required proof of compliance

3. **Timing**
   - Governance changes apply immediately once translated
   - No grace periods
   - No delayed adoption
   - No selective application

---

## III. PR Gates as Governance Enforcement

### Current Authoritative Mechanism

**Until FM Agent is implemented, PR gates are the authoritative governance enforcement mechanism.**

### Gate Philosophy

PR gates represent:
- **Mechanized governance** - rules enforced automatically
- **Non-negotiable constraints** - no bypass, no override
- **Pre-merge validation** - prevents non-compliant code from entering codebase
- **Evidence generation** - creates audit trail of compliance

### Current PR Gates

1. **Build-to-Green Enforcement**
   - File: `.github/workflows/build-to-green.yml`
   - Purpose: Ensures FM Builder hands over only when CI is green
   - Status: Active

2. **FM Architecture Gate**
   - File: `.github/workflows/fm-architecture-gate.yml`
   - Purpose: Validates architecture completeness and agent state
   - Status: Active

3. **Future Gates** (to be added as governance mechanization progresses)
   - Test coverage validation
   - Compliance validation
   - Security scanning
   - Documentation completeness

### Unbreakable Gate Rules

1. **No Disable** - PR gates cannot be disabled
2. **No Weakening** - Gate thresholds cannot be reduced
3. **No Bypass** - No merge without green gates
4. **No Temporary Override** - No time-limited exemptions
5. **No Human Override** - Gates are mechanical, not discretionary

---

## IV. Build-to-Green Requirement

### Constitutional Rule

**FM Builder MUST NOT hand over until all required PR checks are GREEN on the latest commit.**

### Definition of Handover

A "handover" occurs when:
- PR is marked "Ready for Review", OR
- Agent requests Johan review/approval

Opening or updating a draft PR is **NOT** a handover.

### Pre-Handover Procedure (Mandatory)

Before any handover, FM Builder MUST:

1. **Identify** all required PR checks
2. **Verify** all checks are GREEN on latest commit
3. **If any red**:
   - Open logs
   - Identify root cause
   - Implement fix
   - Push commit
   - Re-run checks
4. **Repeat** until all green

### Pre-Handover Proof (Required)

FM Builder MUST add a comment to the PR containing:

```
PREHANDOVER_PROOF

Required PR Checks:
- ✅ Build-to-Green Enforcement
- ✅ FM Architecture Gate
- ✅ [Other required checks]

Status: All checks GREEN on commit [sha]
GitHub Checks URL: [link]

Handover authorized: All governance constraints satisfied.
```

**If this proof cannot be provided, handover is forbidden.**

---

## V. Governance as Execution Constraints

### How Governance Becomes Constraints

Each governance rule from corporate canon translates to one or more execution constraints:

#### Example 1: Zero Test Debt Constitutional Rule

**Governance Rule** (from canon):
> "No code may be merged without corresponding test coverage"

**FM Execution Constraints**:
1. PR Gate: Test coverage check must pass
2. Builder Rule: FM Builder must write tests before merge
3. Validation Rule: Coverage must meet minimum threshold
4. Evidence Rule: Coverage report must be attached to PR

#### Example 2: Design Freeze Rule

**Governance Rule** (from canon):
> "Architecture and QA design must be frozen before implementation begins"

**FM Execution Constraints**:
1. PR Gate: Architecture completeness check must pass
2. Builder Rule: FM Builder cannot start implementation until architecture approved
3. Validation Rule: Architecture document must be marked "FROZEN"
4. Evidence Rule: Foreman approval required on architecture doc

#### Example 3: Build-to-Green Enforcement

**Governance Rule** (from canon):
> "No handover until all CI checks are green"

**FM Execution Constraints**:
1. PR Gate: Build-to-green workflow blocks merge
2. Builder Rule: FM Builder must provide pre-handover proof
3. Validation Rule: All checks must be green on latest commit
4. Evidence Rule: Pre-handover proof comment required

---

## VI. FM Builder Compliance Requirements

### Mandatory FM Builder Behavior

FM Builder MUST:

1. **Build-to-Green**
   - Never hand over with red checks
   - Never hand over with pending checks
   - Never hand over with cancelled checks

2. **Provide Evidence**
   - Pre-handover proof comment
   - Test coverage reports (when implemented)
   - Compliance validation (when implemented)

3. **Escalate When Blocked**
   - Document exact blocker
   - Provide proposed solutions
   - Wait for authority decision
   - Do NOT bypass or weaken gates

4. **Follow Scope Discipline**
   - One responsibility domain per PR
   - Explicit scope declaration
   - No mixed concerns

### Prohibited FM Builder Behavior

FM Builder MUST NOT:

1. ❌ Disable or modify PR gates
2. ❌ Weaken governance constraints
3. ❌ Hand over before green
4. ❌ Request temporary overrides
5. ❌ Shift responsibility ("CI will sort it out")
6. ❌ Claim completion while checks are not green
7. ❌ Mark gates as "deprecated" to pass
8. ❌ Proceed without escalating blockers

---

## VII. Future FM App Mechanization

### Vision

FM app will eventually mechanize governance enforcement, providing:

1. **Real-Time Feedback**
   - Governance violations detected during development
   - Instant feedback in IDE/editor
   - Prevents non-compliant code before commit

2. **FM Office Dashboard**
   - Live governance state visualization
   - Compliance metrics and trends
   - Violation history and resolution tracking

3. **Audible Alerts**
   - Sound notifications for governance violations
   - Escalating alerts for repeated violations
   - Celebratory sounds for compliance milestones

4. **Automatic Evidence Collection**
   - Evidence gathered automatically during build
   - Compliance reports generated without manual work
   - Audit trail maintained continuously

### Current State vs Future State

| Capability | Current (PR Gates) | Future (FM Agent) |
|------------|-------------------|-------------------|
| **When Enforced** | Pre-merge | Real-time during development |
| **Feedback Speed** | Minutes (CI run) | Instant (sub-second) |
| **Prevention** | Blocks merge | Prevents writing non-compliant code |
| **Visibility** | GitHub UI | FM Office Dashboard + IDE |
| **Evidence** | Manual collection | Automatic collection |
| **Alerts** | GitHub notifications | Audible + visual alerts |

### Transition Plan

**Phase 1 (Current)**: PR gates are authoritative
- All governance enforced by GitHub Actions
- Manual evidence collection
- FM Builder provides pre-handover proof

**Phase 2 (Near Future)**: Enhanced PR gates
- Additional gates added (test coverage, compliance, security)
- Automated evidence collection begins
- Dashboard shows PR gate status

**Phase 3 (Future)**: FM Agent operational
- Real-time governance enforcement in development
- FM Office dashboard live
- Audible alerts active
- Evidence fully automated

**Phase 4 (Long-term)**: Full mechanization
- Governance violations become impossible
- Predictive governance warns before violation
- Full audit trail automatic
- Zero manual governance work

---

## VIII. Governance Update Process

### When Governance Canon Changes

1. **Detection**
   - Governance Liaison monitors `maturion-foreman-governance` repo
   - Change detected via commit, release, or notification

2. **Analysis**
   - Understand governance change intent
   - Identify affected FM execution areas
   - Determine required constraint updates

3. **Translation**
   - Translate governance change to execution constraints
   - Update PR gate configurations if needed
   - Update builder specifications if needed
   - Update validation scripts if needed

4. **Testing**
   - Test new constraints in isolation
   - Verify no false positives
   - Verify compliance checking works correctly

5. **Deployment**
   - Deploy updated constraints to FM repository
   - Announce change to FM Builder
   - Update governance documentation
   - Create evidence of alignment

6. **Verification**
   - Verify constraints working as expected
   - Monitor first few PRs under new constraints
   - Adjust if false positives detected (without weakening)

### Emergency Governance Updates

If governance change is urgent (security, compliance, legal):

1. **Immediate Translation** - No delay
2. **Notify All Agents** - Urgent communication
3. **Block Existing PRs** - May need rework under new constraints
4. **Escalate Conflicts** - If urgent governance conflicts with in-flight work

---

## IX. Governance Compliance Evidence

### Required Evidence Types

1. **Pre-Handover Proof**
   - Status: Required now
   - Content: All PR checks green on latest commit
   - Location: PR comment

2. **Test Coverage Reports** (Future)
   - Status: Not yet implemented
   - Content: Coverage percentage, uncovered lines
   - Location: PR comment + dashboard

3. **Compliance Validation** (Future)
   - Status: Not yet implemented
   - Content: Compliance control satisfaction status
   - Location: PR comment + dashboard

4. **Security Scan Results** (Future)
   - Status: Not yet implemented
   - Content: Vulnerability scan results
   - Location: PR comment + dashboard

### Evidence Retention

- All evidence stored in PR comments (GitHub native)
- Future: Evidence also stored in FM Office database
- Retention: Indefinite (audit requirement)
- Access: Public within organization

---

## X. Governance Violation Handling

### If Governance Violation Detected

**During Development** (Future FM Agent):
1. Immediate feedback to developer
2. Audible alert (if configured)
3. Block commit until fixed
4. Log violation for metrics

**During PR** (Current PR Gates):
1. PR check fails (red)
2. PR cannot merge
3. FM Builder must fix
4. No bypass allowed

**Post-Merge** (Should never happen, but if detected):
1. Immediate escalation to Johan Ras
2. Root cause analysis required
3. Fix in next PR
4. Strengthen gates to prevent recurrence

### No Punishment Philosophy

Governance violations are:
- **System failures**, not people failures
- **Prevention opportunities**, not blame targets
- **Learning moments**, not disciplinary events

Response to violations:
1. Fix the violation
2. Understand why gates didn't catch it
3. Strengthen gates
4. Move forward

---

## XI. Governance Audit Support

### Audit Trail

Governance compliance maintained through:

1. **PR History**
   - All PRs show governance compliance evidence
   - Pre-handover proofs in comments
   - PR gate results in GitHub

2. **Commit History**
   - All commits traceable to governance-compliant PRs
   - No direct-to-main commits allowed

3. **CI/CD Logs**
   - All PR gate runs logged
   - Evidence of governance checking
   - Failure and success records

4. **Future: FM Office Database**
   - Comprehensive governance state history
   - Compliance metrics over time
   - Violation and resolution tracking

### Audit Queries

Auditors can answer:
- Was this PR compliant with governance at merge time?
- Have there been any governance violations?
- What is the compliance trend over time?
- What governance constraints apply to this module?

---

## XII. Success Criteria

This adoption policy is successful when:

1. ✅ All governance rules have clear execution constraints
2. ✅ PR gates mechanically enforce all constraints
3. ✅ FM Builder always builds-to-green
4. ✅ Zero governance violations occur
5. ✅ Evidence collection is automatic (future)
6. ✅ Governance state is visible in real-time (future)
7. ✅ Audit trail is complete and accessible

---

## XIII. References

- **Corporate Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Governance Alignment Overview**: `governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **FM Builder Contract**: `.github/agents/FMRepoBuilder.yaml`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **PR Gate Workflows**: `.github/workflows/`

---

*FM Governance Adoption - Execution, Not Creation*
