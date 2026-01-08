# Agent Contract Migration Guide

**Status**: Active  
**Authority**: CS2 (Agent Contract Minimalism Framework)  
**Source**: PR APGI-cmy/maturion-foreman-governance#895  
**Date**: 2026-01-08  
**Version**: 1.0.0

---

## Purpose

This guide provides systematic process for migrating bloated agent contracts (300-700 lines) to minimal format (150-250 lines) by referencing canonical governance instead of duplicating doctrine.

---

## Background: The Bloat Crisis

**Problem**: Agent contracts in office-app repository exceeded Claude Sonnet 3.5 context capacity (300-700 lines), preventing agent recruitment and contributing to governance failures.

**Root Cause**: Governance doctrine duplicated in every agent contract instead of referenced from canon.

**Solution**: Minimal contracts (150-300 lines) that reference canonical governance.

---

## Migration Principles

### 1. Nothing is Removed, Only Reorganized
- All governance requirements preserved
- Doctrine moved to canon, contracts reference it
- No weakening of governance

### 2. Stronger Through Clarity
- Minimal = Clearer (essential constraints immediately visible)
- References = Comprehensive (all governance via canon, no gaps)
- Single source = Consistent (no drift between contracts and canon)

### 3. Every Requirement Must Trace
- Every contract requirement must trace to canonical governance
- If requirement not in canon: STOP and escalate to add to canon first
- No orphaned requirements

### 4. CS2 Authorization Required
- No contract inclusions removed without CS2 authorization
- Test removal governance preserved (PR #484)
- Warning handling governance preserved (PR #484)

---

## Migration Process (Step-by-Step)

### Step 1: Extract Core Elements

From existing contract, extract:

**A. Identity**
- Agent name, role, description
- Model configuration (tier, class, fallback)
- Version, status, authority

**B. Scope**
- Mission (1-2 sentences)
- Responsibilities (5-10 bullets)
- Capabilities (3-7 bullets)
- Forbidden actions (5-10 bullets)

**C. Boundaries**
- Read permissions
- Write permissions
- Protected paths

**D. Operational Protocol**
- Pre-work validation checklist
- Execution steps (3-5 bullets)
- Completion criteria (3-5 bullets)

**E. Escalation**
- When to escalate (3-5 triggers)
- How to escalate (3-step process)

### Step 2: Create Governance Bindings

Identify all canonical governance documents the agent references:

```yaml
governance:
  canon:
    repository: APGI-cmy/maturion-foreman-governance
    path: /governance/canon
    reference: main
  
  bindings:
    - id: [unique-id]
      path: [canonical-doc-path]
      role: [how-agent-uses-it]
      summary: [1-sentence summary]
```

**For each section of old contract:**
1. Identify the governance doctrine
2. Find or create canonical document
3. Add binding reference
4. Replace full text with 2-3 sentence summary + link

**Example Bindings:**
- Build Philosophy → `BUILD_PHILOSOPHY.md`
- Zero Test Debt → `governance/policies/zero-test-debt-constitutional-rule.md`
- Test Removal → `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`
- Warning Handling → `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`
- Builder Appointment → `governance/ROLE_APPOINTMENT_PROTOCOL.md`

### Step 3: Condense Operational Sections

**Old Contract Pattern** (20-50 lines per section):
```markdown
## Section Title

[Full governance doctrine duplicated]
[Detailed procedures]
[All edge cases]
[Examples]
[Historical context]
```

**New Contract Pattern** (3-5 lines per section):
```markdown
## Section Title

**Authority**: [canonical-reference]

[2-3 sentence summary of key points]

**Full details**: See [canonical-document-link]
```

### Step 4: Preserve Critical Governance

**MUST preserve via references** (from PR #484):

**A. Test Removal Governance**
- Authority structure
- Traceability methodology
- Approval requirements
- Prohibited justifications
- Test categories that are always valid

**B. Warning Handling Governance**
- Zero-tolerance policy on suppression
- Warning visibility requirement
- Warning categories (blocking vs deferrable)
- Emergency suppression authorization

**Format for preservation**:
```markdown
## Test Removal Authorization

**Authority**: `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`

This agent MUST NOT authorize test removal without FM authorization following traceability analysis (behavior → requirement → architecture → decision). Test dodging = work stoppage.

**Full policy**: See governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md
```

### Step 5: Add Onboarding Section

```markdown
## Quick Onboarding

**New to this role?** Read:
1. `governance/AGENT_ONBOARDING.md` (this repository)
2. [AGENT_ONBOARDING_QUICKSTART.md](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/AGENT_ONBOARDING_QUICKSTART.md)
3. All documents in `governance.bindings` below
```

### Step 6: Verify Migration Completeness

**Verification Checklist:**
- [ ] Line count: 150-250 lines (excluding YAML frontmatter)
- [ ] All core elements extracted and present
- [ ] Governance bindings section complete
- [ ] Every governance requirement traces to canonical doc
- [ ] Test removal governance preserved via reference
- [ ] Warning handling governance preserved via reference
- [ ] No governance doctrine duplicated in contract
- [ ] Onboarding section added
- [ ] Template format followed
- [ ] All forbidden actions preserved
- [ ] All permissions preserved
- [ ] Escalation protocol clear

---

## Common Patterns

### Pattern 1: Constitutional Grounding

**Old** (50+ lines):
```markdown
## Constitutional Grounding

This contract derives from:
1. T0-001: BUILD_PHILOSOPHY.md
   [full text of build philosophy]

2. T0-002: governance-supremacy-rule.md
   [full text of governance supremacy]

[... 12 more Tier-0 documents with full text]
```

**New** (5 lines):
```markdown
## Governance Bindings

See `governance.bindings` section for all Tier-0 canonical documents.

**Authority**: All 14 Tier-0 documents (see TIER_0_CANON_MANIFEST.json)
```

### Pattern 2: Execution Principles

**Old** (30+ lines):
```markdown
## One-Time Build Law

Builders MUST build-to-green exactly once...
[Full doctrine with examples, edge cases, historical context]
```

**New** (4 lines):
```markdown
## One-Time Build Law

**Authority**: `BUILD_PHILOSOPHY.md` Section IV

Builders MUST build-to-green exactly once. Non-green = INVALID. Full details in BUILD_PHILOSOPHY.md.
```

### Pattern 3: Mandatory Protocols

**Old** (40+ lines):
```markdown
## Builder Appointment Protocol

Upon appointment, builder MUST...
[Full protocol with examples, formats, edge cases]
```

**New** (6 lines):
```markdown
## Builder Appointment Protocol

**Authority**: `governance/ROLE_APPOINTMENT_PROTOCOL.md`

Builder MUST verify appointment completeness, acknowledge constitutional obligations, and declare readiness before execution. Full protocol in governance/ROLE_APPOINTMENT_PROTOCOL.md.
```

---

## Validation

### Line Count Check
```bash
# Excluding YAML frontmatter
wc -l .github/agents/[agent-name].md
# Target: 150-250 lines
```

### Forbidden Pattern Detection
```bash
# These patterns indicate doctrine duplication
grep -n "Constitutional Principles" .github/agents/*.md
grep -n "Primary Responsibilities" .github/agents/*.md
grep -n "Authority Hierarchy" .github/agents/*.md
```

### Governance Bindings Validation
```bash
# All contracts must have governance.bindings
grep -A10 "governance:" .github/agents/*.md
```

---

## Migration Order

1. **ForemanApp-agent.md** (Week 1)
   - Largest contract (787 lines)
   - Most governance references
   - Template for others

2. **Builder Contracts** (Week 2)
   - api-builder.md (853 lines)
   - integration-builder.md (836 lines)
   - schema-builder.md (836 lines)
   - qa-builder.md (829 lines)
   - ui-builder.md (820 lines)

3. **CI Enforcement** (Week 3)
   - Update agent-boundary-gate.yml
   - Add size limit checks
   - Add pattern detection

---

## Escalation

**If during migration:**

1. **Requirement not in canon**: STOP, escalate to add to canon first
2. **Uncertain about removal**: STOP, escalate to CS2
3. **Contract still >300 lines**: STOP, review for remaining duplication
4. **Breaking changes needed**: STOP, escalate to CS2 for authorization

---

## Success Criteria

✅ All 6 agent contracts under 300 lines (target: 150-250)  
✅ All governance coverage maintained via references  
✅ Zero governance doctrine duplication  
✅ Agents loadable by Claude Sonnet 3.5  
✅ Test removal governance preserved (PR #484)  
✅ Warning handling governance preserved (PR #484)  
✅ CI enforcement active  
✅ All agents tested and functional

---

*END OF AGENT CONTRACT MIGRATION GUIDE*
