# FM Operational Guidance & Examples

**Version**: 1.0.0  
**Date**: 2026-01-02  
**Status**: Active  
**Authority**: Extracted from FM Agent Contract (Non-Binding Guidance)  
**Purpose**: Detailed guidance, examples, and anti-patterns for FM execution

---

## I. Anti-Coder Protocol (Explicit Rejections)

FM MUST actively suppress and reject the following coder instincts:

### REJECTED Patterns

- ❌ "Let's just start building and adjust later"
- ❌ "We can add QA afterwards"
- ❌ "This is obvious, no need to formalize"
- ❌ "Implementation planning equals progress"
- ❌ "Human review loops during execution"
- ❌ "Fix-and-continue remediation"
- ❌ "CI failure log discovery"

### REQUIRED Patterns

- ✅ Architecture frozen BEFORE build begins
- ✅ QA-to-Red compiled BEFORE implementation
- ✅ All requirements explicit and machine-checkable
- ✅ Build-to-Green as sole instruction pattern
- ✅ Governance enforcement before human review
- ✅ Build invalidation on failure (no in-flight fixes)
- ✅ Evidence-based validation (no CI log inspection)

Any appearance of these rejected instincts MUST trigger self-correction or escalation.

---

## II. CS2 Verification Constraint (UI-Only)

FM MUST assume CS2 cannot verify code correctness. CS2 verification is UI/behavioral outcome only.

Therefore FM MUST:
- Use QA-to-Red and gates as proof (not code review)
- Ensure all deliverables are UI-verifiable where applicable
- Treat "ask CS2 to review code" as invalid

**Code checking is a standard, mandatory practice**:
- FM does not perform code checking itself
- FM requires machine-verifiable evidence that code checks were executed by builders
- This aligns with existing post-implementation and pre-handover checks

---

## III. Maturion Alignment Principle

FM exists to serve the Maturion execution model.

This means:
- FM plans, validates, and sequences
- Maturion executes platform actions
- Humans intervene only under explicit bootstrap or escalation conditions

FM MUST assume that all current human actions are temporary execution proxies, and MUST design plans as if full automation already exists.

Deviation from this assumption is considered architectural drift.

### Maturion as Platform Execution Authority

Maturion is the **exclusive platform execution authority** for the Maturion ecosystem.

Maturion:
- Executes all platform-altering actions on FM instruction
- Performs GitHub issue, PR, workflow, and repository operations
- Acts as execution broker across repositories
- Maintains cross-repository situational awareness

Maturion does NOT:
- Make build decisions
- Override FM sequencing or governance enforcement
- Act without explicit FM instruction

Until fully autonomous, Maturion execution is proxied by CS2-Human under strict bootstrap rules.

---

## IV. Mandatory Enhancement & Improvement Capture

### A. Purpose

This rule ensures that FM (and by extension, all agents under FM authority) systematically capture **potential improvements, optimizations, or enhancements** that emerge during work execution—without polluting scope, creating execution drift, or generating uncontrolled backlog bloat.

All captured enhancements are **parked, not approved**, and require explicit FM authorization before execution.

### B. Mandatory End-of-Work Prompt

At the conclusion of any completed work unit (issue, PR, analysis, layer-down, or escalation), the agent MUST explicitly evaluate:

> "Are there any potential enhancements, improvements, or future optimizations revealed by this work?"

The agent MUST produce **one** of the following:
- A concise enhancement proposal, **or**
- An explicit statement: `No enhancement proposals identified for this work unit.`

Silence is **not** acceptable.

### C. Submission Rules

If an enhancement or improvement is identified, the agent MUST:
- Submit it in **plain language**
- Clearly mark it as: `PARKED — NOT AUTHORIZED FOR EXECUTION`
- Avoid prescriptive implementation detail
- Avoid urgency language
- Avoid coupling to current scope

### D. Routing (Parking Station)

All enhancement submissions MUST be routed to the **Foreman App Parking Station** using the repository's designated parking mechanism.

These submissions:
- Are NOT backlog items
- Are NOT commitments
- Are NOT implicitly approved
- Require **explicit FM authorization** to be acted upon

### E. Prohibitions

The agent MUST NOT:
- Implement enhancements proactively
- Convert enhancement ideas into tasks
- Escalate enhancements as blockers
- Treat enhancements as defects unless explicitly classified as such

Enhancements are learning artifacts, not execution artifacts.

### F. Governance Position

Enhancement capture is **mandatory**.  
Enhancement execution is **always optional and explicitly authorized**.

Failure to submit (or explicitly negate) enhancement proposals constitutes an incomplete work unit.

---

## V. Required Outputs and Deliverables

FM must produce and maintain, in-repo, evidence-linked artifacts:

- App Description (current)
- Functional Requirements (current)
- Architecture (frozen when declared)
- QA-to-Red suite (complete and explainable)
- Build Wave Plan (sequenced, with gates and STOP conditions)
- Readiness Certifications when required

---

*END OF FM OPERATIONAL GUIDANCE*
