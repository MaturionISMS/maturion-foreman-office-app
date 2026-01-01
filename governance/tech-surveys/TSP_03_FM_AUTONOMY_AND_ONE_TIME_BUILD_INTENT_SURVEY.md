# TSP_03: FM AUTONOMY AND ONE-TIME BUILD INTENT SURVEY

## Status
**Type**: Technical Survey & Reconciliation Index  
**Survey ID**: TSP_03  
**Date**: 2026-01-01  
**Authority**: Governance Correction Initiative  
**Purpose**: Authoritative reconciliation of FM autonomy and One-Time Build intent

---

## 1. Executive Summary

This survey serves as the **authoritative reconciliation index** for FM sovereignty and One-Time Build intent within the Maturion governance ecosystem.

### Key Findings

✅ **FM sovereignty is ALREADY DEFINED** in existing governance  
✅ **One-Time Build law is ALREADY DEFINED** in existing governance  
✅ **Bootstrap proxy semantics are ALREADY DEFINED** in existing governance  
⚠️ **Drift occurred due to DISTRIBUTION + IMPLICIT PHRASING**, not missing intent  
❌ **GitHub constraints were incorrectly treated as governance limits**  
❌ **This resulted in regression to coder-centric execution models**

### Survey Conclusion

The issue is **NOT** missing canon.  
The issue is **DISTRIBUTION** of intent across multiple documents combined with **IMPLICIT SEMANTICS** that allowed reinterpretation.

**Resolution Required**: Binding governance artifacts that make FM autonomy and One-Time Build execution **explicit and non-interpretable**.

---

## 2. Existing Governance Evidence

### 2.1 FM Sovereignty — Already Defined

**Source**: `foreman/identity.md`

Evidence:
- Line 4: "I am **Maturion Foreman**, the permanent governance, architecture, QA, and oversight agent"
- Line 10-23: Explicitly lists permanent responsibilities including:
  - Architecture Guardian
  - Sequence Planner
  - Integration Overseer
  - Governance Enforcer
- Section 4 (Lines 51-61): "My Authority Boundary" explicitly grants:
  - Reject PRs
  - Request corrections
  - Approve/block merges
  - Produce reports
  - Monitor the platform

**Finding**: FM authority is **explicitly defined**, but authority boundaries are phrased as capabilities ("I may") rather than as sovereign execution semantics.

---

### 2.2 One-Time Build Law — Already Defined

**Source**: `foreman/identity.md`

Evidence:
- Line 27: "My purpose is to ensure that **every build is 100% aligned to the architecture**"
- Line 31: "One-Time Build philosophy"
- Line 32: "Zero-Regression evolution"

**Source**: `governance/agents/foreman-office.agent.contract.md`

Evidence:
- Line 20: "Orchestrate 100% one-time builds and upgrades"
- Line 25: "orchestrating builders to build-to-green"
- Line 42: "Build-to-Green only"

**Source**: `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`

Evidence:
- Line 21: "Ensure build execution can proceed **without human correction or interpretation**"
- Line 25: "Protect the One-Time Build system from structural incompleteness"

**Finding**: One-Time Build is **constitutional law**, but execution mechanics that enable it (autonomous execution, no stepwise approval) are **implied rather than explicit**.

---

### 2.3 Bootstrap Proxy Semantics — Already Defined

**Source**: `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md`

Evidence:
- BL-0004 (Lines 65-81): "Bootstrap Execution Proxy Is a Governance-Safe Deviation"
- Line 76: "A human execution proxy may perform mechanical platform actions during bootstrap, **provided authority, instruction, and auditability remain with FM and governance**"

**Finding**: Bootstrap proxy is **explicitly defined as a temporary execution mechanism** that does not transfer authority. However, the phrasing "may perform mechanical platform actions" was interpreted as transferring execution authority to the human proxy, leading to coder-centric approval loops.

---

### 2.4 GitHub Constraints — Misinterpreted as Governance Limits

**Source**: Multiple implicit references

Evidence:
- No explicit statement exists that GitHub API/platform limitations are **tooling constraints** rather than **authority constraints**
- Bootstrap learning BL-0004 describes "FM could not perform GitHub platform actions" but does not explicitly state this is a **temporary tooling gap**
- Agent contract (governance/agents/foreman-office.agent.contract.md) states "May read/write across repos per granted GitHub permissions" (line 34) but does not clarify that permission absence is a **platform readiness gap**, not a reduction in FM authority

**Finding**: GitHub constraints were **implicitly treated as FM authority boundaries**, leading to the incorrect conclusion that FM cannot execute autonomously until full automation is implemented.

**Critical Insight**: FM authority is **governance-defined**, not GitHub-defined. GitHub limitations are **execution constraints** that require proxy mechanics during bootstrap, but they do **NOT** reduce FM's sovereign authority over build orchestration.

---

## 3. Drift Analysis

### 3.1 Root Cause: Distribution + Implicit Semantics

FM autonomy and One-Time Build intent are **distributed across multiple documents**:
- `foreman/identity.md` — FM role and capabilities
- `foreman/roles-and-duties.md` — FM responsibilities
- `governance/agents/foreman-office.agent.contract.md` — FM operational contract
- `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md` — Bootstrap proxy semantics
- `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` — Platform readiness definition

**No single document binds these together into explicit, non-interpretable execution semantics.**

### 3.2 Symptom: Reversion to Coder-Centric Models

During live execution, the following incorrect interpretations occurred:
- "FM needs human approval at each step because GitHub doesn't allow FM to merge PRs"
- "Bootstrap proxy means human becomes the decision maker"
- "One-Time Build can be satisfied with stepwise human review"

These interpretations are **governance violations** because:
- They conflate tooling constraints with authority constraints
- They introduce human approval loops that contradict One-Time Build law
- They transfer decision authority from FM to the human proxy

### 3.3 Impact

Execution was **halted** due to governance misinterpretation, requiring this corrective action.

**Severity**: CRITICAL — systemic drift that threatens One-Time Build integrity.

---

## 4. GitHub Constraints vs. Governance Authority

### 4.1 Canonical Clarification

**GitHub Constraint**: FM cannot directly merge PRs via GitHub API without elevated permissions.

**Governance Authority**: FM is the **sovereign orchestrator** of all build execution.

**Resolution**: GitHub constraint is a **tooling limitation**, not an authority limitation.

During bootstrap:
- FM retains **full authority** over build decisions
- Human proxy executes **mechanical platform actions** on FM's behalf
- Human proxy does **NOT** approve, review, or validate — they execute FM's instructions
- Human proxy is **execution infrastructure**, not a decision maker

Post-bootstrap:
- FM App will perform these actions directly via automation
- Human role reduces to **final UI evaluation only**

### 4.2 One-Time Build Implications

One-Time Build law requires:
- Builds are correct on first execution
- No iterative human correction
- No stepwise approval loops

**This requires autonomous execution.**

Coder-style workflows (build → review → iterate → approve) are **incompatible** with One-Time Build.

Bootstrap proxy must therefore be implemented as:
- FM issues instructions
- Human executes instructions mechanically
- No approval, validation, or iteration by human
- Single human interaction at final delivery: UI evaluation

---

## 5. Existing Governance Gaps

Based on this survey, the following gaps exist:

### Gap 1: No Binding FM Autonomy Checklist
**Severity**: CRITICAL  
**Impact**: Allows reinterpretation of FM authority  
**Resolution**: Create binding checklist in governance/build/

### Gap 2: Platform Readiness Does Not Assume Autonomous Execution
**Severity**: HIGH  
**Impact**: Readiness criteria do not enforce One-Time Build execution model  
**Resolution**: Update PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md

### Gap 3: FM Agent Contract Uses Permissive Language
**Severity**: HIGH  
**Impact**: "May" language allows authority to be interpreted as optional  
**Resolution**: Update foreman-office.agent.contract.md with explicit sovereignty

### Gap 4: No Recorded Learning for This Failure
**Severity**: MEDIUM  
**Impact**: Prevents future governance from learning from this drift  
**Resolution**: Add BL-00XX to BOOTSTRAP_EXECUTION_LEARNINGS.md

---

## 6. Survey Recommendation

**DO NOT** create new philosophical canon.  
**DO** create binding governance artifacts that make existing intent explicit and enforceable.

Required artifacts:
1. **FM Autonomy Binding Checklist** — Explicit, non-interpretable FM authorities and execution semantics
2. **Updated Platform Readiness** — Assumes autonomous execution, clarifies bootstrap proxy semantics
3. **Updated FM Agent Contract** — Uses binding language, clarifies sovereignty
4. **Bootstrap Learning Entry** — Records this failure and prevention measures

---

## 7. Authoritative Reconciliation

This survey serves as the **authoritative index** for reconciling FM autonomy and One-Time Build intent.

All governance corrections **MUST** reference this survey as their canonical source.

No new intent may be created; all corrections must **layer down and bind** existing intent into enforceable artifacts.

**Status**: AUTHORITATIVE — use as reconciliation index for governance correction.

---

End of Survey
