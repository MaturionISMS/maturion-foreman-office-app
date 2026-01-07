# Model Tier Agent Contract Binding Policy

**Policy ID**: MODEL-TIER-BINDING-001  
**Version**: 1.0.0  
**Status**:  CANONICAL — MANDATORY  
**Effective Date**: 2026-01-07  
**Authority**:  Governance Escalation Policy + Cognitive Capability Orchestration Model  
**Integration**:  ESCALATION_POLICY.md, COGNITIVE_CAPABILITY_ORCHESTRATION_MODEL.md

---

## Purpose

This policy defines **mandatory model tier specifications** for all agent contracts in the Maturion ISMS ecosystem, ensuring agents operate at cognitive capacity appropriate to their role complexity.

**Core Principle**: The overseeing intelligence must be at least one cognitive tier higher than the implementing intelligence.

---

## I. Mandatory Model Tier Specification

### All Agent Contracts MUST Specify:

Every `.agent. md` contract in `.github/agents/` MUST include the following YAML frontmatter fields:

```yaml
model: <explicit-model-name>     # e.g., claude-sonnet-4-5, gpt-5-1
model_tier: <tier-name>          # standard | premium | reasoning
model_tier_level: <level>        # L1 | L2 | L3 | L4
model_class: <capability-class>  # coding | extended-reasoning | constitutional-interpretation
temperature: <value>             # 0.0 - 1.0
model_fallback: <fallback-model> # Optional: fallback for routine tasks
```

### Field Definitions:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | **MANDATORY** | Explicit model identifier (no `auto`) |
| `model_tier` | enum | **MANDATORY** | Tier classification: `standard`, `premium`, `reasoning` |
| `model_tier_level` | enum | **MANDATORY** | Escalation level: `L1`, `L2`, `L3`, `L4` |
| `model_class` | string | **MANDATORY** | Capability class (see Section III) |
| `temperature` | float | **MANDATORY** | Model temperature setting (0.0-1.0) |
| `model_fallback` | string | OPTIONAL | Fallback model for routine tasks |

---

## II.  Model Tier Hierarchy

### Tier 1: Reasoning (L3/L4) — Strategic & Governance Reasoning

**Cognitive Capacity**: Constitutional interpretation, deep architecture reasoning, governance evolution  
**Use Case**: Long-term decisions, system soundness reviews, crisis resolution  
**Context Window**: Full governance corpus required  
**Usage Rule**: **Use sparingly** — Only when the decision matters long-term

**Model Assignments**: 

| Role | Model | Rationale | Cost Discipline |
|------|-------|-----------|-----------------|
| CodexAdvisor (Chief Advisor) | GPT-5.1 | Best at hierarchy enforcement, governance reasoning, cross-repo coherence, authority disputes | HIGH — Reserve for architecture & governance |
| Deep Architecture Review | GPT-5 | Strong system reasoning, slightly cheaper than 5.1 | MEDIUM-HIGH |
| Crisis / Conflict Resolution | GPT-5.1 | Best long-range reasoning and constraint holding | HIGH |
| "Is This System Sound?" Reviews | GPT-5.1 | Thinks like a systems architect | HIGH |

**Agents at This Tier**:
- `CodexAdvisor-agent.md` (Chief Advisor)
- Johan Ras (CS2) with GPT-5.1 as advisor (L4)

**Frontmatter Template**:
```yaml
model: gpt-5-1
model_tier: reasoning
model_tier_level: L3
model_class: constitutional-interpretation
temperature:  0.3

# Tier Justification: 
# CodexAdvisor requires L3 due to:
# - Constitutional interpretation
# - Cross-repo governance coherence
# - Authority dispute resolution
# - Deep system architecture reasoning
```

---

### Tier 2: Premium (L2) — Advisory, Issues, Reviews (Workhorse Tier)

**Cognitive Capacity**: Multi-document synthesis, strategic planning, governance enforcement  
**Use Case**:  Coordinate builders, enforce governance, create issues, review PRs  
**Context Window**: 128K+ tokens (full repository governance)  
**Usage Rule**: **If a human will read it, use this tier**  
**Target Usage**: **60-70% of total agent usage should be Tier 2**

**Model Assignments**:

| Role | Model | Rationale | Cost Discipline |
|------|-------|-----------|-----------------|
| Foreman Planning Aid | GPT-5 | Strategic wave planning, governance enforcement | MEDIUM-HIGH |
| Issue Creation | Claude Sonnet 4.5 | Excellent structure, calm tone, human-readable | LOW-MEDIUM |
| PR Review Comments | Claude Sonnet 4.5 | Reads code well, flags risk without noise | LOW-MEDIUM |
| Governance Commentary | Claude Sonnet 4.5 | Strong policy and declarative reasoning | LOW-MEDIUM |
| Architecture Explanations | Claude Sonnet 4.5 | Clear explanations without over-engineering | LOW-MEDIUM |
| Design Discussions | Claude Sonnet 4 | Slightly cheaper, still solid | LOW |

**Agents at This Tier**:
- `ForemanApp-agent.md` (FM)
- `governance-liaison.md` (Governance Liaison)

**Frontmatter Template (FM)**:
```yaml
model: gpt-5
model_tier:  premium
model_tier_level:  L2
model_class: extended-reasoning
model_fallback: claude-sonnet-4-5
temperature: 0.08

# Tier Justification:
# FM requires L2 due to:
# - Strategic wave planning (GPT-5)
# - Multi-document synthesis (14 Tier-0 docs)
# - Governance enforcement (Sonnet 4.5)
# - Builder coordination (Sonnet 4.5)
# - Escalates to GPT-5.1 (L3) for deep governance reasoning
```

**Frontmatter Template (Governance Liaison)**:
```yaml
model: claude-sonnet-4-5
model_tier:  premium
model_tier_level:  L2
model_class: extended-reasoning
temperature: 0.1

# Tier Justification:
# Liaison requires L2 due to: 
# - Governance commentary and policy reasoning
# - Issue creation for governance updates
# - PR review for governance compliance
# - Cross-repo governance alignment
```

---

### Tier 3: Standard (L1) — Operational & Mechanical Tasks

**Cognitive Capacity**: Focused implementation, scoped work, clear specifications  
**Use Case**: Execute well-defined tasks with frozen architecture and QA-to-Red  
**Context Window**: 8K-32K tokens sufficient  
**Usage Rule**: **Don't spend intelligence where structure is enough**

**Model Assignments**:

| Role | Model | Rationale | Cost Discipline |
|------|-------|-----------|-----------------|
| Builder Implementation | GPT-4.1 | Reliable, cheap, good for structured tasks | LOW |
| Repetitive Issue Templates | GPT-4.1 | Fast, consistent | LOW |
| Summaries / Checklists | GPT-4.1 | Good enough, inexpensive | LOW |
| Repo Hygiene Checks | GPT-4.1 | Adequate for mechanical tasks | LOW |
| Fast Reasoning / Glue Tasks | GPT-5-mini | Very cheap, very fast | VERY LOW |
| Lightweight Code Comments | GPT-5-mini | Adequate, low cost | VERY LOW |

**Agents at This Tier**:
- `ui-builder.md`
- `api-builder.md`
- `schema-builder.md`
- `integration-builder.md`
- `qa-builder.md`

**Frontmatter Template**:
```yaml
model: gpt-4-1
model_tier: standard
model_tier_level: L1
model_class: coding
model_fallback:  gpt-5-mini
temperature: 0.3

# Tier Justification:
# Builders require L1 due to: 
# - Scoped implementation work with frozen architecture
# - Clear QA-to-Red specifications
# - Repetitive, well-defined tasks
# - Cost-effective for high-volume work
```

---

### Tier 4: Specialized / Optional Models

**Use Case**: Edge cases, experimental features, multimodal tasks

| Model | Use Case | Recommendation |
|-------|----------|----------------|
| Claude Haiku 4.5 | Ultra-cheap summarization | Optional |
| GPT-4o | Multimodal / UI explanations | Optional |
| Grok Code Fast 1 | Quick code snippets | Optional |
| Gemini Flash / Pro | Experimental / preview | **Avoid for governance** |
| GPT-5.1-Codex-Max | Heavy coding / IDE agents | Overkill for advisory |

**Usage**:  Case-by-case basis only.  Not for standard governance/build work.

---

## III. Capability Classes

### Capability Class Assignment

Each agent must specify a `model_class` matching their primary function:

| Capability Class | Description | Typical Agents | Tier |
|------------------|-------------|----------------|------|
| `coding` | Implementation-focused, scoped work | Builders | L1 |
| `extended-reasoning` | Strategic planning, multi-doc synthesis | FM, Liaison | L2 |
| `constitutional-interpretation` | Governance evolution, canon arbitration | CodexAdvisor | L3 |
| `advisory` | Read-only consultation, no execution | CodexAdvisor | L3 |

### Capability vs. Tier Distinction: 

- **Tier** (L1/L2/L3/L4): Hierarchical authority and cognitive capacity
- **Capability Class**:  Functional specialization within tier

Example:  Both FM and Governance Liaison are L2, but: 
- FM:  `extended-reasoning` (wave orchestration, uses GPT-5)
- Liaison: `extended-reasoning` (governance alignment, uses Sonnet 4.5)

---

## IV. Quick Decision Rule

**One-line decision (easy to remember)**: 

| Question | Answer |
|----------|--------|
| **Thinking about the system? ** | → GPT-5.1 (Tier 1, L3) |
| **Talking to humans?** | → Claude Sonnet 4.5 (Tier 2, L2) |
| **Doing repetitive work?** | → GPT-4.1 / GPT-5-mini (Tier 3, L1) |

---

## V. Enforcement

### Platform Integration: 

**Copilot Workspaces / GitHub Copilot Agents**:
- Platform MUST honor `model` field (explicit model selection)
- Platform SHOULD honor `model_tier` (if custom orchestration exists)
- Platform MUST honor `temperature` field
- Platform MAY use `model_fallback` for routine tasks

### Validation Requirements:

**Pre-Authorization Check (FM)**:

Before authorizing any wave, FM MUST verify:
1. ✅ All agent contracts specify `model`, `model_tier`, `model_tier_level`, `model_class`
2. ✅ FM contract specifies L2 tier minimum
3. ✅ Builders specify L1 tier
4. ✅ No agent uses `model:  auto` (explicit model required)
5. ✅ CodexAdvisor specifies L3 tier

### Governance Gate: 

**New Gate**:  `model-tier-compliance-gate. yml`

**Checks**:
- All `.github/agents/*. md` files have valid frontmatter
- `model` field is explicit (not `auto`)
- `model_tier`, `model_tier_level`, `model_class` present
- FM is L2 or higher
- CodexAdvisor is L3
- Builders are L1

---

## VI. Tier Assignment Rules

### Rule 1: FM MUST Be Higher Tier Than Builders

**FM Tier ≥ L2**  
**Builder Tier = L1**

**Rationale**: FM oversees builders; must have higher cognitive capacity. 

**Violation**: If FM is L1, this is a **CONSTITUTIONAL VIOLATION**.

---

### Rule 2: CodexAdvisor MUST Be Highest Tier

**CodexAdvisor Tier = L3**  
**FM Tier = L2**  
**Builder Tier = L1**

**Rationale**: CodexAdvisor advises FM; must have highest reasoning capacity.

---

### Rule 3: No Tier Downgrade Without Approval

**Agents CANNOT downgrade their tier** without CS2 (Johan) approval.

**Example**:
- ❌ Changing FM from L2 to L1 → **PROHIBITED**
- ✅ Changing FM from L2 to L3 → Allowed (upgrade)

---

### Rule 4: Tier Justification Required

Every agent contract MUST include an inline comment justifying tier assignment:

```yaml
model_tier: premium
model_tier_level: L2

# Tier Justification: 
# FM requires L2 due to:
# - Multi-document synthesis (14 Tier-0 docs)
# - Strategic wave orchestration
# - Governance enforcement complexity
```

---

## VII. Escalation Integration

### Proactive Escalation (Complexity-Aware):

When FM detects cognitive limits: 
1. **HALT** current work
2. **ESCALATE** to L3 (CodexAdvisor) or L4 (Johan with GPT-5.1)
3. **REQUEST** higher tier model or human intervention
4. **WAIT** for authorization

**Example Escalation Path**:
```
Builder (L1, GPT-4.1) → encounters complexity
  ↓ ESCALATE
FM (L2, GPT-5) → encounters governance ambiguity
  ↓ ESCALATE
CodexAdvisor (L3, GPT-5.1) → resolves constitutional question
  ↓ RETURN GUIDANCE
FM (L2) → resumes with clarity
  ↓ INSTRUCT
Builder (L1) → executes with updated guidance
```

### Reactive Escalation (Failure-Based):

When builders fail repeatedly:
1. Builder STOPS and escalates to FM (L1 → L2)
2. FM investigates and may escalate to L3/L4
3. L3/L4 resolves governance ambiguity
4. FM resumes with clarified governance

**Reference**: `governance/escalation/ESCALATION_POLICY.md`

---

## VIII. Cost Management

### Cost Optimization Strategy:

**Start at Lowest Viable Tier**:
- Use L1 for implementation (GPT-4.1, GPT-5-mini)
- Use L2 for orchestration (GPT-5, Sonnet 4.5)
- Use L3 only for constitutional issues (GPT-5.1)
- Use L4 for emergencies (Johan + GPT-5.1)

**Target Usage Distribution**:
- **60-70%**:  Tier 2 (L2) — Advisory, coordination, governance
- **20-30%**: Tier 3 (L1) — Builder implementation
- **5-10%**: Tier 1 (L3) — Deep reasoning, architecture
- **<5%**: Human escalation (L4)

**Do NOT**:
- ❌ Use L3 models for L1 work (waste)
- ❌ Use L1 models for L2 work (failure risk)
- ❌ Downgrade tier to save cost (governance violation)

**Cost Multipliers** (approximate):
- L1 (GPT-4.1): 1x baseline
- L1 (GPT-5-mini): 0.3x baseline (very cheap)
- L2 (Sonnet 4.5): 2-3x baseline
- L2 (GPT-5): 4-5x baseline
- L3 (GPT-5.1): 10-15x baseline
- L4 (Human): Project-dependent

---

## IX. Agent-Specific Model Assignments

### FM Agent (ForemanApp-agent. md)

```yaml
name: ForemanApp
role: FM Orchestration Authority
model: gpt-5
model_tier: premium
model_tier_level: L2
model_class: extended-reasoning
model_fallback: claude-sonnet-4-5
temperature: 0.08
```

**Usage Pattern**:
- **Strategic planning**: GPT-5 (higher reasoning)
- **Issue creation / PR reviews**: Claude Sonnet 4.5 (better human communication)
- **Routine coordination**: Claude Sonnet 4.5 (cost-effective)
- **Deep governance questions**:  Escalate to GPT-5.1 (L3)

---

### CodexAdvisor (CodexAdvisor-agent. md)

```yaml
name: CodexAdvisor
role:  Chief Advisor (Advisory-Only)
model: gpt-5-1
model_tier: reasoning
model_tier_level: L3
model_class: constitutional-interpretation
temperature: 0.3
```

**Usage Pattern**:
- **Always**: GPT-5.1 (constitutional reasoning, governance interpretation)
- **Never downgrade**: CodexAdvisor is always highest tier

---

### Governance Liaison (governance-liaison. md)

```yaml
name: Governance Liaison
role:  Governance Alignment Authority
model: claude-sonnet-4-5
model_tier:  premium
model_tier_level:  L2
model_class: extended-reasoning
temperature: 0.1
```

**Usage Pattern**:
- **Always**: Claude Sonnet 4.5 (governance commentary, policy reasoning)
- **Issue creation**: Claude Sonnet 4.5 (excellent structure)
- **PR reviews**: Claude Sonnet 4.5 (reads code well)

---

### Builders (All 5 Builders)

```yaml
name: UI Builder
role: builder
model: gpt-4-1
model_tier: standard
model_tier_level: L1
model_class: coding
model_fallback: gpt-5-mini
temperature: 0.3
```

**Usage Pattern**:
- **Implementation**: GPT-4.1 (reliable, cost-effective)
- **Simple summaries / checklists**: GPT-5-mini (very cheap)
- **Complex architecture questions**:  Escalate to FM (L2)

---

## X. Compliance Verification

### Pre-Merge Checklist:

Before merging any agent contract update:
- [ ] `model` field is explicit (not `auto`)
- [ ] `model_tier` is valid (`standard`, `premium`, `reasoning`)
- [ ] `model_tier_level` is valid (`L1`, `L2`, `L3`, `L4`)
- [ ] `model_class` is specified
- [ ] Tier assignment matches role complexity
- [ ] FM is L2 or higher
- [ ] CodexAdvisor is L3
- [ ] Builders are L1
- [ ] Inline justification comment present
- [ ] Model matches tier (e.g., L1 uses GPT-4.1, not GPT-5.1)

### Audit Trail:

All tier changes MUST be: 
- Documented in commit message
- Justified in PR description
- Reviewed by Governance Administrator (for L2/L3 changes)
- Approved by Johan (for tier downgrades or L3+ changes)

---

## XI. Exception Handling

### Temporary Tier Upgrades:

FM MAY temporarily escalate a builder to L2 for:
- Emergency governance interpretation
- Complex architectural decision
- RCA requiring deep reasoning

**Process**:
1. FM documents escalation need
2. FM requests tier upgrade for specific task
3. Johan approves
4. Builder executes at L2 (using GPT-5 or Sonnet 4.5)
5. Builder reverts to L1 after task

### Platform Limitations:

If platform does not support explicit model selection:
- Document desired tier in frontmatter
- Use best available model
- Record limitation in governance notes
- Advocate for platform enhancement

---

## XII. Future Evolution

### Roadmap: 

**Phase 1 (Current)**: Manual tier specification in agent contracts  
**Phase 2**: Automated tier validation in governance gates  
**Phase 3**: Dynamic tier scaling based on task complexity  
**Phase 4**:  Cost-aware tier optimization with quality guarantees

---

## XIII. Success Criteria

This policy succeeds when:
- ✅ All agents specify explicit model tiers
- ✅ FM operates at L2 (GPT-5 / Sonnet 4.5)
- ✅ CodexAdvisor operates at L3 (GPT-5.1)
- ✅ Builders operate at L1 (GPT-4.1 / GPT-5-mini)
- ✅ Tier hierarchy is enforced
- ✅ Escalation paths are clear
- ✅ 60-70% of usage is Tier 2 (cost-optimized workhorse)
- ✅ Cost is optimized without compromising quality
- ✅ No governance failures due to insufficient cognitive capacity

---

## XIV. Quick Reference Summary

### Recommended Default Mapping

| Agent | Model | Tier | Level | Cost |
|-------|-------|------|-------|------|
| CodexAdvisor | GPT-5.1 | Reasoning | L3 | HIGH |
| ForemanApp (Strategic) | GPT-5 | Premium | L2 | MEDIUM-HIGH |
| ForemanApp (Routine) | Claude Sonnet 4.5 | Premium | L2 | LOW-MEDIUM |
| Governance Liaison | Claude Sonnet 4.5 | Premium | L2 | LOW-MEDIUM |
| Builders (Implementation) | GPT-4.1 | Standard | L1 | LOW |
| Builders (Lightweight) | GPT-5-mini | Standard | L1 | VERY LOW |

---

## XV. References

- **Escalation Policy**: `governance/escalation/ESCALATION_POLICY. md`
- **Cognitive Capability Model**: `governance/canon/COGNITIVE_CAPABILITY_ORCHESTRATION_MODEL.md`
- **Model Tier Matrix**: `docs/governance/model-tier-matrix.md`
- **GitHub Model Scaling Policy**: `docs/governance/github-model-scaling-policy.md`
- **Quick Reference Guide**: `governance/reference/MODEL_ASSIGNMENT_GUIDE.md`

---

**Policy Owner**: Governance Administrator  
**Enforcement**:  FM Agent + Governance Gates  
**Review Cycle**:  Quarterly or after platform changes  
**Last Updated**: 2026-01-07  
**Next Review**: 2026-04-07

---

## XVI. Model Transparency and Signature Requirements

### Purpose

All agents operating at L2 (Premium) or L3 (Reasoning) tiers MUST declare their active model tier in strategic decisions, governance enforcement actions, and upon request. This ensures transparency about which cognitive tier was used for critical decisions.

---

### Mandatory Model Declaration Scenarios

**L2 Agents (FM, Governance Liaison) MUST declare model in**:
1. Wave authorization decisions
2. Architecture freeze declarations
3. Builder appointment notifications
4. Escalation requests
5. Gate pass/fail declarations
6. Strategic planning summaries
7. Upon explicit user request

**L3 Agents (CodexAdvisor) MUST declare model in**: 
1. Constitutional interpretations
2. Governance canon recommendations
3. Architecture soundness reviews
4. Authority dispute resolutions
5. Crisis/conflict resolution guidance
6. Upon explicit user request

**L1 Agents (Builders)**:
- Model declaration OPTIONAL (cost-sensitive, high-volume work)
- Required only when escalating to FM or upon explicit request

---

### Signature Formats

#### Strategic Decisions (L2/L3 — Full Signature)

**Format**:
```
---
**Agent**:  [Agent Name]
**Model**:  [Model Name] (Tier [Level] [Tier Name])
**Temperature**: [Value]
**Decision Type**: [Type]
**Date**:  YYYY-MM-DD
**Authority**: [Contract Reference]
---
```

**Example (FM Wave Authorization)**:
```
---
**Agent**: ForemanApp
**Model**: GPT-5 (Tier L2 Premium)
**Temperature**: 0.08
**Decision Type**: Wave 2. 0 Authorization
**Date**: 2026-01-07
**Authority**:  FM Agent Contract v3.5. 0
---
```

**Example (CodexAdvisor Constitutional Interpretation)**:
```
---
**Agent**: CodexAdvisor
**Model**: GPT-5.1 (Tier L3 Reasoning)
**Temperature**: 0.3
**Decision Type**: Constitutional Interpretation
**Date**:  2026-01-07
**Authority**: Model Tier Binding Policy Section XVI
---
```

---

#### Routine Responses (L2 — Short Signature)

**Format**: `[Agent | Model Tier-Level | Date]`

**Examples**:
- `[ForemanApp | GPT-5 L2 | 2026-01-07]`
- `[ForemanApp | Sonnet-4.5 L2 | 2026-01-07]` (when using fallback)
- `[Governance Liaison | Sonnet-4.5 L2 | 2026-01-07]`

**Usage**:  End of issue comments, PR reviews, routine coordination

---

#### Escalation Requests (All Tiers — Full Signature Required)

**Format**:
```
---
**Escalation From**: [Agent Name] ([Current Tier])
**Escalation To**: [Target Tier/Agent]
**Current Model**: [Model Name]
**Reason**: [Brief reason]
**Requested Tier**: [L2/L3/L4]
**Date**: YYYY-MM-DD
---
```

**Example (Builder → FM)**:
```
---
**Escalation From**: UI Builder (L1 Standard)
**Escalation To**: ForemanApp (L2)
**Current Model**: GPT-4.1
**Reason**: Governance ambiguity in architecture freeze interpretation
**Requested Tier**: L2
**Date**: 2026-01-07
---
```

**Example (FM → CodexAdvisor)**:
```
---
**Escalation From**: ForemanApp (L2 Premium)
**Escalation To**: CodexAdvisor (L3)
**Current Model**: GPT-5
**Reason**: Constitutional question regarding Zero Test Debt interpretation
**Requested Tier**: L3
**Date**: 2026-01-07
---
```

---

### Model Fallback Declaration

When using `model_fallback`, agents MUST indicate which model was actually used: 

**Example (FM using fallback)**:
```
[ForemanApp | Sonnet-4.5 L2 (fallback) | 2026-01-07]
```

This indicates FM used Claude Sonnet 4.5 (fallback) instead of primary GPT-5.

---

### Enforcement

**FM Pre-Authorization Check MUST verify**:
- [ ] All L2/L3 agents include model signature in strategic decisions
- [ ] All escalation requests include full signature
- [ ] Model declared matches agent contract specification
- [ ] Fallback usage is declared when applicable

**Violation**:  Missing model signature in strategic decision = **GOVERNANCE VIOLATION**

---

### Observability Integration

Model signatures enable:
1. **Audit Trail**: Track which model made which decision
2. **Cost Analysis**: Correlate decisions with model tier costs
3. **Quality Analysis**: Assess decision quality by model tier
4. **Compliance**: Verify tier usage matches policy

**Future Enhancement**:  Automated logging to `governance/events/model-usage-log.jsonl`

---

### User Request Response

When user asks "What model are you using?", agent MUST respond with: 

**Format**:
```
I am currently using [Model Name] (Tier [Level] [Tier Name]) as specified in my agent contract ([Contract File]).

**Model Details**:
- Model:  [Model Name]
- Tier: [Tier Name]
- Level: [Level]
- Temperature: [Value]
- Fallback: [Fallback Model] (if applicable)
- Contract: [Contract File] v[Version]

For strategic decisions, I use [Primary Model]. 
For routine coordination, I may use [Fallback Model] (if specified).
```

**Example Response (FM)**:
```
I am currently using GPT-5 (Tier L2 Premium) as specified in my agent contract (ForemanApp-agent.md v3.5.0).

**Model Details**:
- Model:  GPT-5
- Tier: Premium
- Level: L2
- Temperature: 0.08
- Fallback: Claude Sonnet 4.5
- Contract: . github/agents/ForemanApp-agent.md v3.5.0

For strategic wave planning and governance enforcement, I use GPT-5.
For routine issue creation and PR reviews, I may use Claude Sonnet 4.5 (fallback).
```

---

### Signature Placement

**Strategic Decisions**:  Signature at **END** of response (after content)

**Routine Responses**: Signature at **END** (optional, but recommended)

**Escalations**: Signature in **HEADER** (before escalation content)

---

**END OF MODEL TIER AGENT CONTRACT BINDING POLICY**
