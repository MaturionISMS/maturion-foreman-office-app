# Governance Policy Sync Specification

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2025-12-29  
**Authority**: Johan Ras  
**Addresses**: Issue #78 - FMSYNC-1

---

## I. Purpose

This specification defines the mechanism by which FM repository governance remains synchronized with corporate governance canon.

**Core Principle**: FM executes governance; FM does not create governance. Synchronization ensures execution alignment.

---

## II. Canonical Governance Source

### Source of Truth

**Corporate Governance Canon Repository**: `maturion-foreman-governance`

**Canonical Governance Directories** (in the canonical repository):
- `/foreman/` - Core Foreman governance specifications
- `/governance/` - Constitutional governance documents
- `/docs/governance/` - Governance documentation and reports
- Any directory containing governance policy, constitutional rules, or enforcement specifications

This repository contains:
- Constitutional rules (Governance Supremacy Rule, Zero Test Debt, Design Freeze, etc.)
- Architecture standards and validation checklists
- QA governance and minimum coverage requirements
- Compliance specifications and control libraries
- PR gate requirements and failure handling protocols
- Agent behavior doctrine
- All canonical governance definitions

**FM Repository Role**: Adopt and execute canonical governance, never modify or reinterpret it.

---

## III. Synchronization Model

### Governance Flow Architecture

```
┌─────────────────────────────────────────────┐
│  Corporate Governance Canon                 │
│  (maturion-foreman-governance)              │
│  - Constitutional rules                     │
│  - Architecture standards                   │
│  - QA governance                            │
│  - Compliance specs                         │
│  - PR gate requirements                     │
└─────────────────┬───────────────────────────┘
                  ↓
         [Governance Change Event]
                  ↓
┌─────────────────────────────────────────────┐
│  Governance Liaison Agent (FM Scoped)       │
│  Role: Monitor, Translate, Align            │
│  - Detects canon changes                    │
│  - Translates to FM constraints             │
│  - Updates FM governance scaffolding        │
│  - Creates alignment PRs                    │
└─────────────────┬───────────────────────────┘
                  ↓
         [Translation Complete]
                  ↓
┌─────────────────────────────────────────────┐
│  FM Repository Governance Scaffolding       │
│  (maturion-foreman-office-app/governance)   │
│  - Alignment documents (references canon)   │
│  - Adoption policies (execution constraints)│
│  - Agent contracts (enforcement specs)      │
│  - PR gate workflows (mechanical enforcement)│
└─────────────────┬───────────────────────────┘
                  ↓
         [Enforcement Active]
                  ↓
┌─────────────────────────────────────────────┐
│  FM Builder / PR Gates                      │
│  Role: Execute governance constraints       │
│  - Enforce gate requirements                │
│  - Validate compliance                      │
│  - Block non-conforming merges              │
└─────────────────────────────────────────────┘
```

### Key Principles

1. **Downward Flow Only (Canonical to FM)**
   - Governance changes originate in canonical repository
   - FM adapts to governance changes
   - FM never pushes governance changes upstream (except lessons learned proposals)

2. **Translation, Not Interpretation**
   - Governance Liaison translates canonical rules to FM execution constraints
   - No interpretation, no reduction, no extension
   - Direct mapping only

3. **Immediate Adoption**
   - Governance changes apply immediately once translated
   - No grace periods, no delayed adoption
   - No selective application

---

## IV. Synchronization Mechanisms

### Mechanism 1: Manual Monitoring (Current State)

**Status**: Active  
**Owner**: Governance Liaison Agent

**Process**:
1. Governance Liaison periodically reviews `maturion-foreman-governance` repository
2. Detects new/changed governance documents
3. Creates alignment PR in FM repository
4. Translates canonical requirements to FM execution constraints
5. Updates FM governance scaffolding documents
6. PR review and merge

**Frequency**: On-demand or when Johan requests sync

**Limitations**:
- Reactive, not proactive
- Depends on manual trigger
- Potential for drift between syncs

### Mechanism 2: Automated Monitoring (Future State)

**Status**: Planned (not yet implemented)  
**Owner**: FM Office App (when operational)

**Process**:
1. FM Office subscribes to `maturion-foreman-governance` repository events
2. Webhook triggers on governance document changes
3. FM Office agent analyzes change impact
4. FM Office creates draft alignment PR automatically
5. Governance Liaison reviews and refines PR
6. Johan approves governance alignment
7. PR merged, enforcement updated

**Triggers** (governance changes only):
- Commit to `maturion-foreman-governance` main branch that modifies governance documents in canonical governance directories
- New governance document added in canonical governance directories
- Existing governance document modified in canonical governance directories
- New governance version tagged (tags matching pattern `governance-v*` or `canon-v*`)

**Note**: The canonical repository (`maturion-foreman-governance`) uses its own directory structure. When these triggers fire, the Governance Liaison analyzes which canonical governance documents changed and determines the corresponding FM repository paths that need updating (typically `/governance/`, `/foreman/governance/`, or `/docs/governance/` in the FM repository).

**Benefits**:
- Proactive sync
- Minimal drift window
- Automated alignment draft generation
- Faster governance propagation

---

## V. Sync Artifact Types

### Type 1: Canonical Mirror Documents

**Purpose**: Direct reference to canonical governance documents

**Location**: `governance/alignment/`

**Examples**:
- `PR_GATE_REQUIREMENTS_CANON.md` (mirrors canonical PR gate requirements)
- `TWO_GATEKEEPER_MODEL.md` (mirrors canonical gatekeeper model)
- `PR_GATE_FAILURE_HANDLING_PROTOCOL.md` (mirrors canonical failure handling)

**Structure**:
```markdown
# [Document Title] (Canonical Mirror)

**Status**: Authoritative  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  

[Mirror content - should match canon exactly or reference canon with FM-specific adoption notes]
```

**Update Policy**: Must be updated whenever canonical source changes

---

### Type 2: FM Adoption Documents

**Purpose**: Define how FM adopts and executes canonical governance

**Location**: `governance/policies/`

**Examples**:
- `FM_GOVERNANCE_ADOPTION_POLICY.md` (how governance becomes execution)
- `RED_GATE_AUTHORITY_AND_OWNERSHIP.md` (FM-specific authority application)

**Structure**:
```markdown
# [Policy Title]

**Authority**: Johan Ras  
**Source**: Derived from Corporate Governance Canon  

[FM-specific adoption and execution constraints]
```

**Update Policy**: Updated when canonical governance requires new FM execution behavior

---

### Type 3: FM Enforcement Artifacts

**Purpose**: Mechanical enforcement of governance

**Location**: `.github/workflows/`, `governance/specs/`

**Examples**:
- `.github/workflows/builder-qa-gate.yml` (enforces Builder QA gate requirements)
- `.github/workflows/fm-architecture-gate.yml` (enforces architecture gate requirements)
- `governance/specs/build-to-green-enforcement-spec.md` (enforcement specification)

**Structure**: GitHub Actions workflows + enforcement specifications

**Update Policy**: Updated when canonical gate requirements change

---

### Type 4: Agent Contracts

**Purpose**: Define agent governance behavior

**Location**: `.github/agents/`

**Examples**:
- `governance-liaison.md` (Governance Liaison agent contract)
- `foreman.agent.md` (Foreman agent contract)

**Structure**:
```markdown
---
name: AgentName
role: Agent Role
authority: governance-liaison-fm
...
# AGENT CONTRACT
[Agent responsibilities, scope, prohibitions based on canonical governance]
```

**Update Policy**: Updated when canonical agent behavior doctrine changes

---

## VI. Synchronization Workflow

### Step 1: Governance Change Detection

**Trigger**: Change in `maturion-foreman-governance` repository

**Detection Methods**:
- Manual review by Governance Liaison (current)
- Automated webhook notification (future)
- Johan explicit sync request

**Output**: List of changed governance documents

---

### Step 2: Impact Analysis

**Performed By**: Governance Liaison Agent

**Analysis Questions**:
1. Which canonical document changed?
2. Does this impact FM execution constraints?
3. Which FM documents must be updated?
4. Which PR gate workflows must be modified?
5. Which agent contracts must be updated?
6. Does this require new enforcement artifacts?

**Output**: Impact assessment document

---

### Step 3: Alignment PR Creation

**Performed By**: Governance Liaison Agent

**PR Contents**:
1. Updated canonical mirror documents (if canon changed)
2. Updated FM adoption policies (if execution constraints changed)
3. Updated PR gate workflows (if gate requirements changed)
4. Updated agent contracts (if agent behavior doctrine changed)
5. Impact assessment document
6. Sync completion checklist

**PR Title Format**: `[GOVERNANCE SYNC] <Canonical Change Summary>`

**PR Labels**: `governance-sync`, `alignment`

---

### Step 4: Review and Validation

**Reviewers**:
1. Governance Liaison (self-review for translation accuracy)
2. Johan Ras (governance alignment approval)

**Validation Criteria**:
- ✅ Canonical governance correctly mirrored/referenced
- ✅ No interpretation or reinterpretation introduced
- ✅ FM execution constraints correctly derived
- ✅ No governance weakening
- ✅ All affected artifacts updated
- ✅ Agent contracts updated
- ✅ PR gate workflows updated (if needed)

**Blocking Conditions**:
- ❌ Governance reinterpretation detected
- ❌ Canonical requirements weakened
- ❌ Incomplete artifact updates
- ❌ Agent contract violations introduced

---

### Step 5: Merge and Activation

**Merge Authority**: Johan Ras (or delegated reviewer)

**Post-Merge Actions**:
1. PR gate workflows activate immediately (if updated)
2. Agent contracts take effect immediately (if updated)
3. Builder agents adopt new constraints (if updated)
4. Sync record logged to governance memory

**Verification**:
- Verify PR gates reflect new requirements
- Verify agent contracts updated
- Verify enforcement active

---

## VII. Drift Detection and Prevention

### Drift Definition

**Governance Drift**: FM execution constraints diverge from canonical governance requirements

**Causes**:
- Canonical governance updated but FM not synced
- FM-specific modifications introduced without canon basis
- Agent contracts outdated
- PR gate workflows not updated
- Manual governance weakening

### Drift Detection

**Detection Mechanisms**:

1. **Manual Audit**
   - Governance Liaison periodically compares FM artifacts to canon
   - Identifies divergences
   - Creates sync PR to resolve

2. **Version Tracking**
   - Canonical documents have version numbers
   - FM mirror documents reference canonical version
   - Mismatched versions indicate drift

3. **Automated Diff (Future)**
   - FM Office compares canonical governance to FM governance
   - Flags divergences automatically
   - Creates drift alerts

**Drift Response**:
1. HALT new governance enforcement until drift resolved
2. Create emergency sync PR
3. Escalate to Johan if drift is significant
4. Merge sync PR
5. Verify alignment restored

### Drift Prevention

**Prevention Strategies**:

1. **Frequent Sync**
   - Sync immediately after canonical changes
   - Don't allow drift window to grow

2. **Strict Translation Discipline**
   - Never interpret, only translate
   - Never weaken, only adopt
   - Never extend, only mirror

3. **Prohibition Enforcement**
   - FM agents MUST NOT modify governance
   - FM builders MUST NOT weaken gates
   - Only Governance Liaison may update governance artifacts

4. **Audit Trail**
   - All governance changes logged
   - All sync PRs documented
   - All drift incidents recorded

---

## VIII. Synchronization Checklist

**Use this checklist for every governance sync PR**:

### Canonical Change Analysis
- [ ] Canonical governance document(s) identified
- [ ] Canonical change version/date recorded
- [ ] Impact on FM execution assessed
- [ ] Affected FM artifacts identified

### FM Artifact Updates
- [ ] Canonical mirror documents updated (if applicable)
- [ ] FM adoption policies updated (if applicable)
- [ ] PR gate workflows updated (if applicable)
- [ ] Agent contracts updated (if applicable)
- [ ] Enforcement specs updated (if applicable)

### Translation Validation
- [ ] No governance reinterpretation introduced
- [ ] No governance weakening introduced
- [ ] Direct translation only
- [ ] Canonical authority preserved

### Review and Approval
- [ ] Governance Liaison self-review complete
- [ ] Johan Ras approval obtained
- [ ] All reviewers satisfied

### Post-Merge Verification
- [ ] PR gates reflect new requirements
- [ ] Agent contracts updated
- [ ] Enforcement active
- [ ] Sync logged to governance memory

---

## IX. Escalation: When Canon Conflicts with FM Reality

### Conflict Scenarios

Sometimes canonical governance may conflict with FM operational reality:

**Example Conflicts**:
- Canonical requirement cannot be mechanically enforced in FM
- Canonical requirement conflicts with existing FM architecture
- Canonical requirement requires resources not available to FM
- Canonical requirement ambiguous or incomplete

### Escalation Protocol

**DO NOT**:
- ❌ Weaken canonical requirement to fit FM
- ❌ Interpret canonical requirement differently
- ❌ Bypass canonical requirement
- ❌ Create FM-specific governance exception

**DO**:
1. ✅ Document the conflict clearly
2. ✅ Escalate to Johan with:
   - Canonical requirement (exact text)
   - FM reality (exact constraint)
   - Conflict description
   - Proposed resolution options
3. ✅ Wait for Johan decision
4. ✅ Implement Johan decision (may involve updating canon or FM)

**Resolution Authority**: Johan Ras ONLY

---

## X. Upward Ripple: FM Lessons to Canon

### Lesson Learned Promotion

While governance flows downward (canon → FM), lessons learned may flow upward (FM → canon).

**When to Propose Canon Update**:
- FM discovers governance gap during execution
- FM identifies governance ambiguity during enforcement
- FM learns from governance failure/incident
- FM identifies governance improvement opportunity

**Upward Ripple Process**:
1. FM documents lesson learned
2. Governance Liaison analyzes lesson for canonical applicability
3. Governance Liaison creates proposal for canonical governance update
4. Proposal escalated to Johan + Governance Administrator (governance repo)
5. If accepted, canonical governance updated
6. FM syncs updated canon back down

**Key Principle**: FM proposes, canon decides. FM never modifies canon directly.

---

## XI. Integration with Existing Governance

This specification integrates with:

- **Governance Alignment Overview** (`governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`) - Defines FM relationship with canon
- **FM Governance Adoption Policy** (`governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`) - Defines adoption execution
- **Governance Ripple Compatibility** (`governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md`) - Defines ripple model
- **Two-Gatekeeper Model** (`governance/alignment/TWO_GATEKEEPER_MODEL.md`) - Defines Governance Liaison role in sync

**Precedence**: This specification is execution authority for governance synchronization.

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: Governance Execution Authority  
**Last Updated**: 2025-12-29  
**Owner**: Johan Ras (MaturionISMS)  
**Executor**: Governance Liaison Agent (FM-scoped)

**Changelog**:
- 1.0.0 (2025-12-29): Initial Governance Policy Sync Specification (addresses #78)

---

*END OF GOVERNANCE POLICY SYNC SPECIFICATION*
