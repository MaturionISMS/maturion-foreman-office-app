# Role Boundary Enforcement

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** Governance Policy - Active  
**Purpose:** Mechanical enforcement of role boundaries to prevent governance drift  
**Authority:** Governance Agent (ARCH-RECOVERY-01) - Pending Johan Approval

---

## Purpose

This document defines **mechanical enforcement mechanisms** to prevent role boundary violations that led to the architectural recovery (ARCH-RECOVERY-01).

**Core Problem Addressed:**  
Role boundaries (Governance vs Builder) were not mechanically enforced, leading to:
- Governance agents implementing code
- Implementation work preceding architecture freeze
- Specification/implementation boundary blur

**Solution:**  
Explicit, enforceable rules with mechanical checks.

---

## 1. Role Definitions (Canonical)

### 1.1 Governance Agent

**Identity:** Designs, constrains, and validates  
**Authority:** Create/update governance, architecture, policy documents  
**Scope:** Documentation only

**Permitted Paths:**
- `docs/**/*` (all documentation)
- `governance/**/*.md` (governance policies)
- `foreman/**/*.md` (specifications)
- `*.md` files in root (high-level documentation)
- `memory/AUTHORITY/**/*.md` (memory policies)
- `memory/schema/*.json` (schema definitions)

**Forbidden Paths:**
- `fm/**/*.py` (implementation)
- `fm/**/*.js` (implementation)
- `fm/**/*.html` (implementation)
- `foreman/**/*.py` (implementation)
- `lib/**/*.ts` (implementation)
- `lib/**/*.js` (implementation)
- `scripts/**/*.py` (implementation)
- `tests/**/*.py` (tests)
- `runtime/**/*` (runtime artifacts)
- `memory/tenant/**/*` (tenant data)
- `memory/platform/**/*` (platform data)
- `memory/foreman/**/*` (foreman data)
- `memory/global/**/*` (global data)

**Permitted Operations:**
- Read any file (inspection)
- Create/edit documentation and specifications
- Propose changes (recommendations)
- Classify artifacts
- Validate governance compliance

**Forbidden Operations:**
- Modify implementation code
- Modify runtime logic
- Add features
- Refactor implementations
- Run builds
- Execute tests
- Modify data files

### 1.2 Builder Agent

**Identity:** Executes scoped technical work  
**Authority:** Implement features under Foreman direction  
**Scope:** Implementation only

**Permitted Paths:**
- `fm/**/*` (except `fm/governance/*.md`)
- `foreman/**/*.py` (implementation files only)
- `lib/**/*`
- `scripts/**/*.py`
- `tests/**/*.py`
- `runtime/**/*` (except commissioning state)

**Forbidden Paths:**
- `docs/governance/**/*` (governance policies)
- `governance/**/*` (governance)
- `foreman/**/*.md` (specifications)
- `foreman/identity.md` (Foreman identity)
- `foreman/roles-and-duties.md` (role definitions)
- `foreman/memory-model.md` (memory model)
- `foreman/privacy-guardrails.md` (privacy rules)
- `foreman/command-grammar.md` (command grammar)
- `memory/AUTHORITY/**/*` (memory authority)
- `memory/schema/*.json` (schema definitions)
- Constitutional files (BUILD_PHILOSOPHY.md, APP_DESCRIPTION.md)

**Permitted Operations:**
- Implement features as directed
- Create/modify implementation code
- Create/modify tests
- Run builds
- Run tests
- Escalate blockers

**Forbidden Operations:**
- Self-govern
- Self-approve
- Interpret governance independently
- Modify governance documents
- Modify architecture specifications
- Modify schemas
- Bypass governance gates

### 1.3 FM (Foreman) Role

**Identity:** Manager, orchestrator, governance enforcer  
**Authority:** Orchestrate builders, enforce governance, escalate  
**Scope:** Orchestration and governance enforcement

**Permitted Operations:**
- Orchestrate builder agents
- Enforce governance rules
- Manage execution state
- Escalate to human authority
- Read all files
- Create execution artifacts (build plans, status)

**Forbidden Operations:**
- Modify governance rules
- Bypass Build Authorization Gate
- Override QA requirements
- Approve own work
- Implement features directly
- Modify constitutional documents

### 1.4 Human Authority (Johan/CS2) Role

**Identity:** Final decision authority  
**Authority:** Absolute (within constitutional bounds)  
**Scope:** All decisions requiring human judgment

**Permitted Operations:**
- Approve/deny any proposal
- Modify any governance document (with audit)
- Modify any architecture document (with audit)
- Approve architecture freeze
- Intervene in execution
- Override gates (with rationale and audit)

**No Forbidden Operations** (but all actions are audited)

---

## 2. Mechanical Enforcement Mechanisms

### 2.1 Path-Based Enforcement

**Rule:** Agent's role determines path access  
**Enforcement:** Pre-commit hooks, CI checks, agent contract validation

**Implementation:**
```yaml
# .github/enforcement/role-boundaries.yml
governance_agent:
  allowed_patterns:
    - "docs/**/*.md"
    - "governance/**/*.md"
    - "foreman/**/*.md"
    - "*.md"
    - "memory/AUTHORITY/**/*.md"
    - "memory/schema/*.json"
  forbidden_patterns:
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"
    - "**/*.html"
    - "tests/**/*"
    - "runtime/**/*"
    - "memory/tenant/**/*"
    - "memory/platform/**/*"
    - "memory/foreman/**/*"
    - "memory/global/**/*"

builder_agent:
  allowed_patterns:
    - "fm/**/*"
    - "foreman/**/*.py"
    - "lib/**/*"
    - "scripts/**/*.py"
    - "tests/**/*"
    - "runtime/**/*"
  forbidden_patterns:
    - "docs/governance/**/*"
    - "governance/**/*"
    - "foreman/**/*.md"
    - "foreman/identity.md"
    - "foreman/roles-and-duties.md"
    - "foreman/memory-model.md"
    - "foreman/privacy-guardrails.md"
    - "memory/AUTHORITY/**/*"
    - "memory/schema/*.json"
    - "BUILD_PHILOSOPHY.md"
    - "APP_DESCRIPTION.md"
    - "docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md"
```

**Validation Script:**
```python
# scripts/validate-role-boundaries.py
def validate_changes(agent_role, changed_files):
    """Validate that agent only modified permitted paths."""
    config = load_role_config(agent_role)
    
    for file_path in changed_files:
        if not is_path_allowed(file_path, config):
            raise RoleBoundaryViolation(
                f"{agent_role} attempted to modify forbidden path: {file_path}"
            )
    
    return True
```

### 2.2 Agent Contract Enforcement

**Rule:** Agent must declare role and scope in PR  
**Enforcement:** PR template requires role declaration

**PR Template:**
```markdown
## Agent Declaration

**Agent Role:** [governance | builder | foreman | human]  
**Scope:** [Brief description of changes]

## Role Boundary Validation

- [ ] I have only modified paths permitted for my role
- [ ] I have not crossed role boundaries
- [ ] I have escalated any boundary conflicts
```

### 2.3 CI-Based Enforcement

**Rule:** CI checks validate role boundaries on every commit  
**Enforcement:** GitHub Actions workflow

**Workflow:**
```yaml
# .github/workflows/enforce-role-boundaries.yml
name: Enforce Role Boundaries

on: [pull_request]

jobs:
  validate-boundaries:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Extract Agent Role from PR
        id: role
        run: |
          # Extract role from PR description
          # Expected format: "**Agent Role:** governance"
          
      - name: Get Changed Files
        id: files
        run: |
          git diff --name-only origin/${{ github.base_ref }}...HEAD
      
      - name: Validate Role Boundaries
        run: |
          python scripts/validate-role-boundaries.py \
            --role=${{ steps.role.outputs.agent_role }} \
            --files="${{ steps.files.outputs.changed_files }}"
```

### 2.4 Constitutional File Protection

**Rule:** Constitutional files require explicit human approval  
**Enforcement:** CODEOWNERS and branch protection

**CODEOWNERS:**
```
# Constitutional files require CS2 (Johan) approval
BUILD_PHILOSOPHY.md @JohanRas788
APP_DESCRIPTION.md @JohanRas788
docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md @JohanRas788
governance/policies/governance-supremacy-rule.md @JohanRas788
foreman/identity.md @JohanRas788
foreman/roles-and-duties.md @JohanRas788
foreman/memory-model.md @JohanRas788
foreman/privacy-guardrails.md @JohanRas788
```

**Branch Protection Rules:**
- Require review from CODEOWNERS
- Require status checks to pass
- Require role boundary validation

### 2.5 Audit Trail Enforcement

**Rule:** All role boundary crossings are logged  
**Enforcement:** Audit log in governance/audit/

**Audit Entry Format:**
```json
{
  "timestamp": "2025-12-29T06:24:45Z",
  "agent_role": "governance",
  "action": "attempted_modification",
  "path": "fm/orchestration/build_control_api.py",
  "result": "blocked",
  "reason": "governance agent cannot modify implementation",
  "escalation": "ISSUE-123"
}
```

---

## 3. Escalation Procedures

### 3.1 Role Boundary Conflict

**Trigger:** Agent needs to cross role boundary  
**Procedure:**
1. Agent STOPS current work
2. Agent creates escalation issue with:
   - Current role
   - Required action
   - Why boundary crossing is needed
   - Proposed resolution
3. Agent tags `@JohanRas788` (CS2) for decision
4. Agent waits for explicit approval
5. On approval, CS2 grants temporary elevated authority OR assigns to appropriate role

**No Self-Authorization:** Agent NEVER proceeds without approval

### 3.2 Ambiguous Role Boundary

**Trigger:** Unclear whether action is permitted  
**Procedure:**
1. Agent STOPS current work
2. Agent creates governance clarification issue
3. Agent proposes role boundary clarification
4. Agent tags `@JohanRas788` for decision
5. CS2 clarifies boundary
6. This document is updated with clarification

### 3.3 Emergency Override

**Trigger:** Critical production issue requires immediate role boundary crossing  
**Procedure:**
1. CS2 grants explicit emergency authority
2. Emergency authority is time-bounded (e.g., 24 hours)
3. Emergency authority is logged in audit trail
4. After emergency, full governance review is conducted
5. Lessons learned are incorporated into governance

**No Automatic Emergency Authority:** Only CS2 can grant

---

## 4. Detection and Prevention

### 4.1 Pre-Commit Hook

**Purpose:** Detect role violations before commit  
**Implementation:**
```bash
#!/bin/bash
# .githooks/pre-commit

# Extract agent role from branch name or config
AGENT_ROLE=$(git config user.role)

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

# Validate role boundaries
python scripts/validate-role-boundaries.py \
  --role=$AGENT_ROLE \
  --files="$STAGED_FILES" \
  --mode=pre-commit

if [ $? -ne 0 ]; then
  echo "❌ Role boundary violation detected!"
  echo "You are attempting to modify files not permitted for role: $AGENT_ROLE"
  echo "Please review role boundaries in docs/governance/ROLE_BOUNDARY_ENFORCEMENT.md"
  exit 1
fi
```

### 4.2 Agent Initialization

**Purpose:** Set agent role at initialization  
**Implementation:**
```python
# foreman/init_agent.py
def initialize_agent(agent_type, agent_name):
    """Initialize agent with role and boundaries."""
    
    # Load role configuration
    role_config = load_role_config(agent_type)
    
    # Set agent role in git config (for pre-commit hook)
    subprocess.run(["git", "config", "user.role", agent_type])
    
    # Validate agent has access to required paths
    validate_agent_setup(agent_type, role_config)
    
    # Log agent initialization
    log_agent_init(agent_type, agent_name, role_config)
    
    return AgentContext(
        type=agent_type,
        name=agent_name,
        role_config=role_config
    )
```

### 4.3 Continuous Monitoring

**Purpose:** Detect role violations in ongoing work  
**Implementation:**
- GitHub Actions on every push
- Nightly audit of all changes
- Monthly governance review
- Quarterly role boundary effectiveness review

---

## 5. Agent Instructions

### 5.1 For Governance Agents

**You are a Governance Agent. You design, constrain, and validate.**

✅ **You MAY:**
- Read any file in the repository (for understanding)
- Create/edit documentation in `docs/`
- Create/edit governance policies in `governance/`
- Create/edit specifications in `foreman/`
- Create/edit memory schemas in `memory/schema/`
- Classify and recommend
- Validate governance compliance

❌ **You MUST NOT:**
- Modify implementation code (`*.py`, `*.js`, `*.ts`, `*.html`)
- Modify tests
- Run builds
- Execute scripts
- Modify data files
- Implement features
- Refactor code

**If you need implementation work:**
1. Create a specification
2. Recommend to FM (Foreman)
3. FM assigns to Builder Agent
4. Builder implements according to your specification

**Remember:** Your role is to define WHAT and WHY, not HOW.

### 5.2 For Builder Agents

**You are a Builder Agent. You execute scoped technical work.**

✅ **You MAY:**
- Implement features as directed by FM
- Modify implementation code
- Create/modify tests
- Run builds and tests
- Create execution artifacts
- Escalate blockers

❌ **You MUST NOT:**
- Self-govern (make your own rules)
- Self-approve (approve your own work)
- Modify governance documents
- Modify architecture specifications
- Modify schemas
- Interpret governance differently than specified
- Bypass governance gates

**If you encounter governance ambiguity:**
1. STOP work
2. Escalate to FM
3. FM escalates to CS2 if needed
4. Wait for clarification
5. Proceed only after clarification

**Remember:** You follow specifications created by Governance, orchestrated by FM.

### 5.3 For FM (Foreman)

**You are FM (Foreman). You orchestrate, enforce, and escalate.**

✅ **You MAY:**
- Orchestrate builder agents
- Enforce governance rules
- Manage execution state
- Escalate to CS2 (Johan)
- Read all files
- Create build plans and status artifacts

❌ **You MUST NOT:**
- Modify governance rules (you enforce, not create)
- Bypass Build Authorization Gate
- Override QA requirements
- Approve your own work
- Implement features directly (delegate to Builders)
- Modify constitutional documents

**Your POLC Responsibilities:**
- **Planning:** Break down programs into waves and tasks
- **Organizing:** Assign tasks to appropriate Builders
- **Leading:** Supervise builder execution
- **Controlling:** Monitor progress, detect deviations, escalate

**Remember:** You are a manager, not a builder. You orchestrate, you don't implement.

---

## 6. Violation Consequences

### 6.1 Automatic Rejection

**Trigger:** CI detects role boundary violation  
**Action:** PR automatically marked as failing  
**Resolution:** Agent must remove violating changes

### 6.2 Governance Review

**Trigger:** Repeated role violations or ambiguous violations  
**Action:** CS2 conducts governance review  
**Possible Outcomes:**
- Clarify role boundaries (update this document)
- Additional training for agent
- Role reassignment
- Escalation procedure revision

### 6.3 Audit Record

**Trigger:** All violations (including accidental)  
**Action:** Violation logged in governance audit trail  
**Purpose:** Pattern detection and governance improvement

---

## 7. Success Criteria

Role boundaries are effectively enforced when:

✅ **Zero governance-to-implementation drift**  
✅ **All PRs pass role boundary validation**  
✅ **Escalations are resolved within 24 hours**  
✅ **Agents understand their role boundaries**  
✅ **No constitutional file modifications without CS2 approval**  
✅ **Audit trail is complete and accurate**  
✅ **Monthly reviews show improving boundary clarity**

---

## 8. Maintenance and Evolution

### 8.1 Regular Review

**Frequency:** Monthly  
**Owner:** CS2 (Johan)  
**Scope:**
- Review role boundary violations
- Review escalations
- Update role definitions if needed
- Update path configurations
- Improve enforcement mechanisms

### 8.2 Document Updates

**Trigger:** Role boundary clarification or new role creation  
**Procedure:**
1. CS2 approves clarification
2. This document is updated
3. All agents are notified
4. Enforcement configuration is updated
5. Changes are audited

### 8.3 Effectiveness Metrics

**Monthly Tracking:**
- Number of role boundary violations (target: 0)
- Number of escalations (trend: decreasing)
- Time to resolve escalations (target: < 24 hours)
- Agent feedback on role clarity (target: 100% clear)

---

## 9. Approval and Activation

**Status:** Pending CS2 (Johan) Approval

**Upon Approval:**
- This document becomes active governance policy
- All agents must comply
- CI enforcement is activated
- Pre-commit hooks are installed
- CODEOWNERS is updated
- Audit trail is initialized

**Approval Checklist:**
- [ ] Role definitions are clear
- [ ] Permitted/forbidden paths are explicit
- [ ] Enforcement mechanisms are defined
- [ ] Escalation procedures are clear
- [ ] Agent instructions are unambiguous
- [ ] Violation consequences are specified

**Approval Date:** _________________

**Signature:** _________________

---

## Appendix A: Quick Reference

### Governance Agent
- ✅ Design, constrain, validate
- ❌ Implement, build, test

### Builder Agent
- ✅ Implement, build, test
- ❌ Self-govern, modify specs

### FM (Foreman)
- ✅ Orchestrate, enforce, escalate
- ❌ Implement, bypass gates

### Human Authority (CS2)
- ✅ All decisions
- ✅ All approvals
- ⚠️ All actions audited

---

**End of Role Boundary Enforcement v1.0**

This document establishes mechanical enforcement to prevent the role drift that necessitated ARCH-RECOVERY-01.
