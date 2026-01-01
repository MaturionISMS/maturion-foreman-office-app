# FM APP BUILDER LAYER-DOWN SURVEY

**Survey Type:** Diagnostic Only — No Fixes, No Recruitment, No Execution  
**Survey Date:** 2026-01-01  
**Survey Authority:** Issue Request  
**Repository:** maturion-foreman-office-app  
**Purpose:** Verify governance-to-FM-app layer-down of builder recruitment requirements

---

## Executive Summary

This survey verifies whether **builder recruitment requirements defined in governance canon** have been **correctly layered down** into the Foreman Office App repository in a **machine-operational form**.

Following a catastrophic builder recruitment failure, this diagnostic survey examines the structural presence and compliance of builder agent definitions in the FM app repository.

**Key Finding:** Builder agent definitions exist in the repository but are **NOT** in the expected `.github/agents/` machine-discoverable location with machine-readable YAML prefaces. Builder contracts exist as **root-level markdown files** with human-readable frontmatter only.

---

## Survey Questions & Evidence

### Question 1: Directory Presence

**Question:** Does the FM app repository contain `.github/agents/`?

**Answer:** ✅ **YES**

**Evidence:**

```bash
$ ls -la .github/agents/
total 44
drwxr-xr-x 2 runner runner  4096 Jan  1 08:37 .
drwxr-xr-x 7 runner runner  4096 Jan  1 08:37 ..
-rw-r--r-- 1 runner runner 16863 Jan  1 08:37 ForemanApp-agent.md
-rw-r--r-- 1 runner runner 15886 Jan  1 08:37 governance-liaison.md
```

**Directory Contents:**
- `ForemanApp-agent.md` — FM orchestration agent contract
- `governance-liaison.md` — Governance liaison agent contract

**Verdict:** ✅ Directory exists and contains 2 agent files.

---

### Question 2: Builder Agent Files

**Question:** Do builder agent files exist under `.github/agents/`?

**Answer:** ❌ **NOT PRESENT**

**Evidence:**

**Files Found in `.github/agents/`:**
1. `ForemanApp-agent.md` — FM agent (not a builder)
2. `governance-liaison.md` — Governance liaison (not a builder)

**Files Found in Repository Root:**

Builder contract files exist in the **root directory** (not in `.github/agents/`):
1. `builderui-builder.md` — UI Builder contract
2. `builderapi-builder.md` — API Builder contract
3. `builderschema-builder.md` — Schema Builder contract
4. `builderintegration-builder.md` — Integration Builder contract
5. `builderqa-builder.md` — QA Builder contract

**Verdict:** ❌ Builder agent files are **NOT** in `.github/agents/` directory. They exist as root-level files.

---

### Question 3: Structural Compliance

**Question:** For each builder agent file (if any), does it include a machine-readable YAML preface with required declarations?

**Answer:** ⚠️ **PARTIAL COMPLIANCE**

**Evidence:**

#### ForemanApp-agent.md (in `.github/agents/`)

**YAML Preface:** ✅ Present

```yaml
---
name: ForemanApp
role: FM Orchestration Authority (Repository-Scoped, Non-Platform Executor)
description: >
  Foreman (FM) for the Maturion Foreman Office App repository.
  FM is the planning + orchestration authority for building and evolving this repo
  under canonical governance. FM recruits and directs builders...
model: auto
temperature: 0.08

authority:
  level: fm
  scope: repository-only
  platform_actions: prohibited
  execution_mode:
    normal: "FM plans and requests; Maturion executes platform actions via DAI/DAR"
    bootstrap_wave0: "CS2 acts as execution proxy for GitHub mechanics, on FM instruction"

governance_alignment:
  canonical_source: "maturion-foreman-governance"
  layerdown_contract: "GOVERNANCE_LAYERDOWN_CONTRACT.md"
  delegation_model: "DAI/DAR — FM requests; Maturion executes; audit required"
---
```

**Declarations Present:**
- ✅ Builder identity (`name`, `role`, `description`)
- ✅ Authority scope (`authority.level`, `authority.scope`)
- ✅ Lifecycle state (implied by `execution_mode`)
- ⚠️ Gate binding (not explicitly present)
- ⚠️ Escalation routing (present in body, not in YAML preface)

#### governance-liaison.md (in `.github/agents/`)

**YAML Preface:** ✅ Present

```yaml
---
name: GovernanceLiaison_FM
role: Governance Liaison Agent (FM Repository)
description: >
  FM-repository-scoped governance alignment agent...
model: auto
temperature: 0.1
authority:
  default: governance-liaison-fm
  escalation:
    allowed: true
    authority: Johan Ras
scope:
  allowed_repos:
    - maturion-foreman-office-app
  allowed_paths:
    - ".github/agents/**"
    - "governance/**"
    - "docs/**"
    - "README.md"
  forbidden_paths:
    - "**/*.env"
    - "**/secrets/**"
    ...
---
```

**Declarations Present:**
- ✅ Builder identity
- ✅ Authority scope
- ✅ Lifecycle state (implied)
- ⚠️ Gate binding (not explicitly present)
- ✅ Escalation routing (`authority.escalation`)

#### Builder Contract Files (root-level: `builder*-builder.md`)

**YAML Preface:** ❌ **NOT PRESENT**

**Example Structure (builderui-builder.md):**

```markdown
# Builder Contract: ui-builder

**Contract Version:** 1.0  
**Date Issued:** 2025-12-31  
**Issued By:** Foreman (FM)  
**Authority:** Phase 4.5 — Builder Task Assignment  
**Wave:** Wave 1.0  
**Status:** ACTIVE — READY FOR EXECUTION

---

## Builder Identity

**Builder Name:** ui-builder  
**Builder Type:** Specialized Builder (UI & Frontend)  
**Recruitment Date:** 2025-12-30 (Wave 0.1)  
**Recruitment Status:** ✅ RECRUITED & VALIDATED
...
```

**Format:** Human-readable markdown frontmatter (not YAML preface)

**Declarations Present:**
- ✅ Builder identity (as markdown headers)
- ✅ Authority scope (as markdown sections)
- ✅ Lifecycle state (Status: ACTIVE — READY FOR EXECUTION)
- ✅ Gate binding (Gate Definition section with YAML block inside markdown)
- ✅ Escalation routing (Escalation Rules section)

**Machine-Readability:** ⚠️ Human-readable structure, not parseable YAML preface

**Verdict:** 
- ✅ `.github/agents/` files (ForemanApp, governance-liaison) have machine-readable YAML prefaces
- ❌ Builder contract files (root-level) do **NOT** have machine-readable YAML prefaces
- ⚠️ Builder contracts use human-readable markdown frontmatter instead

---

### Question 4: FM Agent Awareness

**Question:** Does the FM agent contract explicitly reference automated builder recruitment and `.github/agents` as the authoritative location?

**Answer:** ⚠️ **PARTIAL AWARENESS**

**Evidence:**

**File:** `.github/agents/ForemanApp-agent.md`

#### Section 1: Builder Recruitment References

**Line 7 (description):**
```yaml
description: >
  ...FM recruits and directs builders, compiles app description
  → functional requirements → architecture → QA-to-red → build plan...
```
✅ **References:** FM recruits builders

**Line 40 (FM MAY):**
```markdown
FM MAY:
- plan, orchestrate, and instruct
- recruit builders and assign work
- request platform actions via delegated execution (DAI/DAR)
```
✅ **References:** Recruit builders and assign work

**Section 6E: Builder Recruitment Continuity**

```markdown
## 6E) Builder Recruitment Continuity (One-Time Canonical Recruitment)

FM MUST treat builder recruitment as **one-time and continuous across waves**.

### 6E.1 Recruitment vs Appointment Distinction

FM MUST distinguish between:
- **Recruitment**: One-time canonical registration of builders into the system (Wave 0.1)
- **Appointment**: Assignment of recruited builders to specific tasks (Wave 1.0+)

### 6E.3 Recruitment Artifact Requirements

Canonical builder recruitment MUST be evidenced by:
- Builder manifest (foreman/builder-manifest.json)
- Builder specifications (foreman/builder/*-builder-spec.md)
- Builder capability map (foreman/builder/builder-capability-map.json)
- Builder permission policy (foreman/builder/builder-permission-policy.json)
- Builder registry report (foreman/builder-registry-report.md)
```

✅ **References:** Builder recruitment requirements and artifact locations

#### Section 2: `.github/agents/` as Authoritative Location

**Search Result:** ❌ **NOT EXPLICITLY STATED**

The FM agent contract does **NOT** explicitly declare `.github/agents/` as the authoritative location for builder definitions.

**Artifact Locations Referenced:**
- `foreman/builder-manifest.json`
- `foreman/builder/*-builder-spec.md`
- `foreman/builder/builder-capability-map.json`
- `foreman/builder/builder-permission-policy.json`
- `foreman/builder-registry-report.md`

**No Reference To:**
- `.github/agents/` as builder definition location
- Machine-discoverable builder registry
- Automated builder recruitment from `.github/agents/`

**Verdict:**
- ✅ FM agent contract explicitly references builder recruitment as a role
- ✅ FM agent contract defines recruitment artifact requirements
- ❌ FM agent contract does **NOT** reference `.github/agents/` as the authoritative location for builder definitions
- ❌ FM agent contract does **NOT** reference automated builder discovery/recruitment

---

### Question 5: Platform Readiness Integration

**Question:** Do platform readiness checks or documentation require builders to be recruited, selectable, and machine-discoverable? Or is builder existence assumed?

**Answer:** ⚠️ **PARTIALLY REQUIRED, NOT MACHINE-DISCOVERABLE**

**Evidence:**

**File:** `PLATFORM_READINESS_EVIDENCE.md`

**Section: Builder Recruitment**

Line 63-66:
```markdown
3. **FM Role Canon Defined**
   - Agent Contract: `.github/agents/ForemanApp-agent.md`
   - Role: FM Orchestration Authority (Repository-Scoped)
   - Authority chain: CS2 (Johan) → FM → Builders
   - Platform actions: Delegated execution model (DAI/DAR)
```

✅ **References:** Builder existence in authority chain

**Section: Builder Recruitment Requirements**

No explicit section found titled "Builder Recruitment" or "Builder Discovery".

**Search Pattern:** `builder recruitment|selectable|machine.discoverable`

**File:** `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`

Line 255-258:
```markdown
**Operational Definition** (Addressing GAP-008):
- **"Exists"**: Contract file present at canonical path (`.github/agents/` or `governance/agents/`)
- **"Canonical"**: Contract conforms to `.agent.schema.md` and includes all required sections
- **"Bound"**: Contract is active (agent recruited/activated) and agent acknowledges contract authority
```

✅ **References:** `.github/agents/` as canonical path for contracts

Line 272-274:
```markdown
1. **Contract Existence Validation** (per agent role, per repository):
   - Verify FM contract exists: `.github/agents/foreman.md` or repository-specific path
   - Verify Builder contracts exist: `.github/agents/<builder-role>.md` (e.g., `ui-builder.md`)
```

✅ **Explicitly Requires:** Builder contracts in `.github/agents/<builder-role>.md`

**Verdict:**
- ✅ Platform readiness requires builder contract existence
- ✅ Platform readiness references `.github/agents/` as canonical location for builder contracts
- ⚠️ Platform readiness does **NOT** explicitly require machine-discoverability
- ⚠️ Platform readiness does **NOT** explicitly require builder selection mechanism
- ❌ **GAP:** Platform readiness governance requires builders in `.github/agents/`, but FM app has them in root

---

## Summary Matrix

| Aspect | Governance Requirement | FM App Reality | Compliance |
|--------|----------------------|----------------|------------|
| `.github/agents/` directory | Required | ✅ Exists | ✅ |
| Builder files in `.github/agents/` | Required (per governance canon) | ❌ In root instead | ❌ |
| Machine-readable YAML preface | Required (per governance canon) | ❌ Human-readable markdown | ❌ |
| Builder identity declaration | Required | ✅ Present (as markdown) | ⚠️ |
| Authority scope declaration | Required | ✅ Present (as markdown) | ⚠️ |
| Lifecycle state declaration | Required | ✅ Present (as markdown) | ⚠️ |
| Gate binding declaration | Required | ✅ Present (as markdown) | ⚠️ |
| Escalation routing declaration | Required | ✅ Present (as markdown) | ⚠️ |
| FM agent awareness of `.github/agents/` | Required | ❌ Not referenced | ❌ |
| Platform readiness builder requirement | Required | ✅ Present but GAP | ⚠️ |

---

## Gap Analysis

### GAP-1: Builder Location Mismatch

**Governance Requirement:**
```
Verify Builder contracts exist: `.github/agents/<builder-role>.md` (e.g., `ui-builder.md`)
```
**Source:** `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` Line 273

**FM App Reality:**
- Builders exist as: `builder<name>-builder.md` (root level)
- Examples: `builderui-builder.md`, `builderapi-builder.md`

**Impact:** ❌ Builders are **NOT machine-discoverable** via `.github/agents/` path

---

### GAP-2: YAML Preface Missing

**Governance Requirement:**
```
Contract conforms to `.agent.schema.md` and includes all required sections
```
**Source:** `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` Line 256

**FM App Reality:**
- Builder contracts use human-readable markdown frontmatter
- No YAML preface (no `---` delimited YAML block at file start)

**Impact:** ❌ Builders are **NOT machine-parseable** for automated recruitment

---

### GAP-3: FM Agent Contract Silent on `.github/agents/`

**Governance Requirement:**
```
FM recruits and directs builders
```
**Source:** `.github/agents/ForemanApp-agent.md` Line 7

**FM App Reality:**
- FM agent contract references `foreman/builder/*-builder-spec.md`
- FM agent contract does **NOT** reference `.github/agents/` for builder definitions

**Impact:** ⚠️ FM agent unaware of canonical builder definition location

---

### GAP-4: No Machine-Discoverable Builder Registry

**Governance Requirement:**
```
- **"Exists"**: Contract file present at canonical path (`.github/agents/` or `governance/agents/`)
```
**Source:** `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` Line 255

**FM App Reality:**
- No builder registry at `.github/agents/`
- No automated discovery mechanism
- Manual builder initialization via `foreman/init_builders.py`

**Impact:** ❌ No automated builder recruitment possible

---

## Verdict Summary

| Question | Verdict | Symbol |
|----------|---------|--------|
| 1. Directory Presence | Directory exists with 2 non-builder agents | ✅ |
| 2. Builder Agent Files | NOT in `.github/agents/` (exist in root) | ❌ |
| 3. Structural Compliance | No YAML preface for builders | ❌ |
| 4. FM Agent Awareness | No reference to `.github/agents/` for builders | ❌ |
| 5. Platform Readiness | Requires but GAP exists | ⚠️ |

**Overall Verdict:** ❌ **LAYER-DOWN INCOMPLETE**

Builder recruitment requirements from governance canon have **NOT** been correctly layered down into the FM app repository in machine-operational form.

---

## Root Cause Hypothesis

The catastrophic builder recruitment failure likely occurred because:

1. **Governance Layer Requires:** `.github/agents/<builder-role>.md` with YAML prefaces
2. **FM App Layer Implements:** Root-level `builder*-builder.md` with markdown frontmatter
3. **Automated Recruitment Expects:** Machine-parseable YAML at canonical path
4. **Automated Recruitment Receives:** Human-readable markdown at non-canonical path

**Result:** Automated builder recruitment fails due to path and format mismatch.

---

## Corrective Action Requirement Determination

Based on survey findings, corrective action is required at:

- ✅ **FM App Layer:** Builder files must be moved to `.github/agents/` and converted to YAML-preface format
- ⚠️ **Governance Layer:** Platform readiness validation must verify actual builder file locations (may be sufficient)
- ✅ **Both Layers:** FM agent contract must reference `.github/agents/` as authoritative builder location

---

## References

**Files Surveyed:**
- `.github/agents/ForemanApp-agent.md`
- `.github/agents/governance-liaison.md`
- `builderui-builder.md`
- `builderapi-builder.md`
- `builderschema-builder.md`
- `builderintegration-builder.md`
- `builderqa-builder.md`
- `foreman/BUILDER_INITIALIZATION.md`
- `foreman/builder/BUILDER_RECRUITMENT_CONTINUITY_CHECKLIST.md`
- `PLATFORM_READINESS_EVIDENCE.md`
- `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`
- `WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md`

**Survey Completion Date:** 2026-01-01  
**Survey Status:** ✅ COMPLETE  
**No Changes Made:** ✅ CONFIRMED (Diagnostic only)

---

**END OF FM APP BUILDER LAYER-DOWN SURVEY**
