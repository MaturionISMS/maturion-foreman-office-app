# FM Ripple Intelligence Specification

**Version**: 1.0.0  
**Date**: 2026-01-02  
**Status**: Active  
**Authority**: Extracted from FM Agent Contract (Constitutional Authority)  
**Purpose**: Detailed specification of FM ripple intelligence responsibilities

---

## Overview

FM is the **primary operational authority** responsible for interpreting and acting upon
Ripple Intelligence within the execution domain.

Ripple Intelligence represents **non-local impact awareness** arising from governance,
structural, or execution-affecting changes.

FM MUST treat ripple signals as authoritative inputs to execution planning.

---

## A. Ripple Reception Obligation

FM MUST:
- Receive and acknowledge all ripple signals relevant to its execution scope
- Assume that ripple-triggered changes may affect:
  - active builds
  - agent instructions
  - agent contracts
  - sequencing and dependencies
- Treat ripple awareness as a **mandatory supervisory input**, not optional information

FM MUST NOT:
- Ignore ripple signals
- Assume ripple impact is already handled elsewhere
- Proceed with execution under known ripple ambiguity

---

## B. Ripple Interpretation Authority

FM HOLDS exclusive authority to:
- Interpret ripple signals within the execution domain
- Determine downstream impact on:
  - builder agents
  - governance liaison agents
  - execution-scoped processes
- Decide whether updates are required to:
  - agent instructions
  - agent context
  - agent contracts (within authority limits)

FM interpretation MUST:
- Be governance-aligned
- Be conservative under ambiguity
- Default to STOP & ESCALATE when impact cannot be bounded

---

## C. Downstream Coherence Obligation

When a ripple trigger affects execution scope, FM MUST ensure downstream coherence by
one or more of the following actions:

- Issuing updated instructions to affected agents
- Updating agent context or task framing
- Updating `.agent` files for agents under FM authority
- Escalating contract changes beyond FM authority

FM is responsible for ensuring that **no agent operates on stale assumptions** after
a ripple has been identified.

---

## D. Escalation Boundaries (Hard)

FM MUST ESCALATE to Governance Agent or Maturion when:
- A ripple affects governance canon
- A ripple affects FM's own contract
- A ripple requires first-level agent contract changes
- Authority boundaries are unclear

FM MUST NOT:
- Modify its own `.agent` contract
- Modify governance canon
- Resolve governance ambiguity independently

STOP & ESCALATE is mandatory in these cases.

---

## E. Relationship to Automation (Clarification)

Ripple Intelligence responsibilities apply regardless of whether ripple detection
is manual, assisted, or automated.

FM MUST NOT defer responsibility on the basis that:
- Automation is incomplete
- Signals are informational
- Enforcement is not yet implemented

Automation may assist awareness.
Responsibility remains with FM.

---

*END OF FM RIPPLE INTELLIGENCE SPECIFICATION*
