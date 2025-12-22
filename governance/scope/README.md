# FM Governance Scope Discipline

**Status**: Foundation  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras

---

## Purpose

This document defines scope declaration requirements for FM governance PRs, ensuring alignment with corporate scope discipline.

---

## I. Corporate Governance Scope Discipline

### Source

**Defined in**: `maturion-foreman-governance/policies/change-policy.md`

### Core Principles

1. **One Responsibility Domain Per PR**
   - Each PR addresses exactly one responsibility domain
   - No mixing of unrelated concerns
   - Clear, focused scope

2. **Explicit Scope Declaration Required**
   - Every PR must declare its scope explicitly
   - Scope must be verifiable
   - Scope boundaries must be clear

3. **Governance Separate from Execution**
   - Governance changes in separate PRs from execution changes
   - Governance alignment separate from application logic
   - No mixed-concern PRs

---

## II. FM Repository Scope Categories

### Governance-Related Scopes

1. **Governance Alignment**
   - Documenting how FM adopts corporate governance
   - Updating governance adoption policies
   - Creating governance scaffolding
   - **Example**: This current PR (governance scaffolding initialization)

2. **Governance Enforcement**
   - Adding or updating PR gates
   - Configuring governance constraint enforcement
   - Updating validation scripts to match governance
   - **Example**: Adding test coverage PR gate

3. **Governance Evidence**
   - Creating evidence collection mechanisms
   - Updating evidence templates
   - Building compliance reporting
   - **Example**: Automated coverage report generation

### Execution-Related Scopes

4. **FM Application Logic**
   - Building FM Office features
   - Implementing FM Agent capabilities
   - Creating FM automation
   - **Example**: Building governance dashboard UI

5. **FM Infrastructure**
   - Setting up FM runtime environment
   - Configuring FM databases
   - Building FM deployment automation
   - **Example**: Setting up FM Office server

6. **FM Builder Specifications**
   - Creating or updating builder agent specs
   - Defining builder capabilities
   - Establishing builder contracts
   - **Example**: Updating FM Builder spec

### Other Scopes

7. **Documentation**
   - Writing or updating documentation (not governance)
   - Creating user guides
   - Building reference materials
   - **Example**: FM Office user manual

8. **Testing**
   - Writing or updating tests (not governance)
   - Creating test infrastructure
   - Building test automation
   - **Example**: FM integration tests

---

## III. Scope Declaration Requirements

### Mandatory in Every PR

Every PR MUST include a scope declaration in the PR description:

```markdown
## Scope Declaration

**Responsibility Domain**: [One of the categories above]
**Type**: [Governance | Execution | Documentation | Testing | etc.]
**Boundaries**: [What IS included and what IS NOT included]
```

### Example Scope Declarations

#### Example 1: Governance Alignment PR

```markdown
## Scope Declaration

**Responsibility Domain**: Governance Alignment (Foundation)
**Type**: Governance Scaffolding
**Boundaries**:
- ✅ IN SCOPE: Governance directory structure, adoption docs, alignment docs
- ❌ OUT OF SCOPE: FM application code, automation, execution logic
```

#### Example 2: Execution PR

```markdown
## Scope Declaration

**Responsibility Domain**: FM Application Logic
**Type**: Dashboard Implementation
**Boundaries**:
- ✅ IN SCOPE: Governance dashboard UI components and routing
- ❌ OUT OF SCOPE: Governance policies, PR gates, documentation
```

#### Example 3: Governance Enforcement PR

```markdown
## Scope Declaration

**Responsibility Domain**: Governance Enforcement
**Type**: PR Gate Addition
**Boundaries**:
- ✅ IN SCOPE: Test coverage PR gate workflow, validation script
- ❌ OUT OF SCOPE: Test coverage policy definition (upstream), application code
```

---

## IV. Single Domain Constraint

### The Rule

**Each PR MUST address exactly ONE responsibility domain.**

### What This Means

✅ **ALLOWED**:
- All changes in PR relate to one domain
- Changes are cohesive and focused
- PR has a clear, single purpose

❌ **FORBIDDEN**:
- Mixing governance and execution in same PR
- Addressing multiple unrelated domains
- "While we're here" scope creep
- Bundling unrelated changes for efficiency

### Why This Matters

1. **Review Clarity**: Reviewer knows exactly what to focus on
2. **Rollback Safety**: If rollback needed, only one domain affected
3. **Audit Trail**: Clear history of what changed and why
4. **Parallel Work**: Different domains can be developed in parallel
5. **Governance Separation**: Governance changes never contaminate execution

---

## V. Governance and Execution Separation

### Critical Rule

**Governance changes MUST be in separate PRs from execution changes.**

### Rationale

1. **Authority Separation**
   - Governance requires Foreman authority
   - Execution requires Builder authority
   - Different approval processes

2. **Stability**
   - Governance changes affect all future work
   - Must be stable before execution begins
   - Cannot be mixed with implementation

3. **Audit Requirements**
   - Governance changes must be clearly auditable
   - Cannot be hidden in execution PRs
   - Must be traceable independently

### Examples

✅ **CORRECT - Separate PRs**:
- PR #1: Add test coverage policy to governance (Governance)
- PR #2: Implement test coverage PR gate (Governance Enforcement)
- PR #3: Write tests for FM dashboard (Execution)

❌ **INCORRECT - Mixed PR**:
- PR #1: Add test coverage policy + implement gate + write tests (MIXED)

---

## VI. Scope Verification

### How Scope is Verified

1. **PR Description Check**
   - Does PR have scope declaration?
   - Is scope declaration clear?
   - Is single domain constraint satisfied?

2. **File Change Analysis**
   - Do all file changes align with declared scope?
   - Are there changes outside declared scope?
   - Is there scope creep?

3. **Governance/Execution Separation Check**
   - Are governance files and execution files mixed?
   - Are policy changes mixed with implementation?

### Verification Gates (Future)

Planned PR gate to automatically verify:
- Scope declaration exists
- File changes match declared scope
- No governance/execution mixing
- No multi-domain changes

---

## VII. Scope Boundaries

### What Defines a Boundary?

A scope boundary is the line between:
- What IS in the responsibility domain
- What IS NOT in the responsibility domain

### Boundary Definition Template

For every PR scope, define:

```markdown
**IN SCOPE**:
- [Specific files/directories affected]
- [Specific functionality changed]
- [Specific documentation updated]

**OUT OF SCOPE (Explicitly)**:
- [What could be related but is NOT included]
- [What will be addressed in future PRs]
- [What is explicitly deferred]
```

### Why Explicit OUT OF SCOPE?

1. **Prevents Scope Creep**: Reviewer knows what NOT to expect
2. **Documents Decisions**: Shows what was intentionally deferred
3. **Plans Future Work**: Creates backlog of follow-up PRs
4. **Justifies Incompleteness**: Explains why related work not included

---

## VIII. Scope Escalation

### When Scope Needs to Change

If during PR work, scope needs to expand:

1. **STOP Work** - Do not continue with expanded scope
2. **Document Need** - Why does scope need to expand?
3. **Choose Path**:
   - **A. Split PR** - Complete original scope, new PR for expansion (preferred)
   - **B. Update Scope** - If truly inseparable, update scope declaration and get approval
4. **Get Approval** - From Johan Ras before proceeding

### Scope Creep Prevention

❌ **Common Scope Creep Scenarios**:
- "While I'm here, let me also..."
- "This is a small change, I'll include it"
- "These are related, so same PR"
- "It's more efficient to do together"

✅ **Correct Response**:
- Document the additional work needed
- Create a follow-up issue/PR
- Complete original scope
- Address additional work separately

---

## IX. Scope Templates by Category

### Template: Governance Alignment PR

```markdown
## Scope Declaration

**Responsibility Domain**: Governance Alignment
**Type**: [Policy Documentation | Alignment Documentation | Scaffolding]

**IN SCOPE**:
- Governance directory structure: [directories]
- Alignment documents: [files]
- Adoption policy documents: [files]

**OUT OF SCOPE**:
- FM application code
- PR gate implementations
- Automation scripts
- Builder specifications (unless explicitly about governance)

**Governance Canon Reference**: [Link to relevant upstream governance]
```

### Template: Governance Enforcement PR

```markdown
## Scope Declaration

**Responsibility Domain**: Governance Enforcement
**Type**: [PR Gate | Validation Script | Constraint Configuration]

**IN SCOPE**:
- PR gate workflow files: [files]
- Validation scripts: [files]
- Enforcement configuration: [files]

**OUT OF SCOPE**:
- Governance policy definitions (defined upstream)
- Application logic
- Test writing (unless for gate itself)

**Enforces Governance Rule**: [Link to upstream governance rule]
```

### Template: FM Application Logic PR

```markdown
## Scope Declaration

**Responsibility Domain**: FM Application Logic
**Type**: [Feature | Bug Fix | Enhancement]

**IN SCOPE**:
- Source files: [files]
- Tests for source files: [files]
- Related documentation: [files]

**OUT OF SCOPE**:
- Governance policy changes
- PR gate changes
- Infrastructure changes
- Unrelated features

**Complies With Governance**: [How this complies with relevant governance]
```

---

## X. Multi-Repository Scope Coordination

### Governance Changes Across Repositories

When governance changes affect multiple repositories:

1. **Governance Change (maturion-foreman-governance)**
   - PR #1: Update governance canon

2. **FM Adoption (maturion-foreman-office-app)**
   - PR #2: Update FM governance alignment docs
   - PR #3: Implement enforcement in FM PR gates

3. **Module Adoption (individual module repos)**
   - PR #4+: Module-specific governance adoption

**Each PR** addresses one repository and one domain.

### Coordination via Issues

Use GitHub issues to coordinate:
- Issue describes cross-repo change need
- Issue links to all related PRs
- Each PR scoped to one repo and one domain
- Issues track overall completion

---

## XI. Success Criteria

FM scope discipline is successful when:

1. ✅ Every PR has explicit scope declaration
2. ✅ Every PR addresses exactly one responsibility domain
3. ✅ Governance and execution never mixed in same PR
4. ✅ Scope boundaries clear and verifiable
5. ✅ Scope creep prevented (not just detected)
6. ✅ Multi-repo coordination works smoothly
7. ✅ Reviewers can quickly understand PR scope

---

## XII. References

- **Corporate Change Policy**: `maturion-foreman-governance/policies/change-policy.md`
- **Governance Alignment Overview**: `governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **FM Governance Adoption Policy**: `governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`

---

*FM Scope Discipline - One Domain, One PR, Always*
