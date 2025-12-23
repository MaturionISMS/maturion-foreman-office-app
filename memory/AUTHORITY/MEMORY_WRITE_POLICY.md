# Memory Write Policy — Governance Authority

## Purpose

This document defines **who** can write to the Unified Memory Fabric, **when**, and **under what conditions**.

Memory write operations are **governance-controlled** and **never automatic**.

---

## Core Principle

**No Self-Authorization**: Runtime agents MUST NEVER self-authorize memory writes.

All memory write operations require explicit governance approval.

---

## 1. Authority Levels

### 1.1 Automatic (No Approval Required)

**Who:** Foreman or authorized builder agents  
**When:** During approved build tasks  
**What:** Task-scoped memory entries only

**Conditions:**
- Entry must be within scope of approved task
- Entry must follow memory schema
- Entry importance must be 'low' or 'medium'
- Entry must not contain sensitive data

**Examples:**
- Build wave completion events
- Task completion records
- QA validation outcomes (pass/fail)

### 1.2 Governance Review Required

**Who:** Any agent (Foreman, builders, runtime)  
**When:** For high-impact memories  
**What:** High or critical importance entries

**Conditions:**
- Entry importance is 'high' or 'critical'
- Entry affects global scope
- Entry modifies governance rules
- Entry creates new patterns or heuristics

**Review Process:** See `LESSONS_TO_CANON_WORKFLOW.md`

**Examples:**
- Architecture decisions
- Governance policy changes
- New compliance patterns
- Critical incident learnings

### 1.3 Human Authorization Required

**Who:** Johan Ras only  
**When:** For platform-wide changes  
**What:** Global scope, critical importance

**Conditions:**
- Entry affects entire platform
- Entry changes foundational rules
- Entry impacts all modules
- Entry modifies build philosophy

**Examples:**
- Build philosophy updates
- Cross-module architecture changes
- Governance framework modifications
- Privacy or security policy changes

---

## 2. Memory Write Proposal Mechanism

### 2.1 Proposal Submission

Any agent can **propose** a memory write by:

1. Creating a memory proposal object
2. Submitting to governance review queue
3. Awaiting approval decision

**Proposal Structure:**
```json
{
  "proposal_id": "prop-2024-12-23-001",
  "proposed_by": "runtime-agent",
  "proposed_at": "2024-12-23T10:30:00Z",
  "status": "pending",
  "proposed_memory": {
    "scope": "runtime",
    "title": "Auto-fix Pattern Detected",
    "summary": "Pattern for handling database connection timeouts",
    "importance": "high",
    "tags": ["runtime", "auto-fix", "pattern"]
  },
  "rationale": "This pattern successfully resolved 5 incidents in the past week",
  "review_notes": []
}
```

### 2.2 Proposal Storage

**Location:** `/memory/proposals/`

**Separation:** Proposals are stored **separately** from memory fabric.

**Visibility:** All proposals are visible for governance review.

### 2.3 Proposal Lifecycle

```
pending → under_review → approved | rejected
```

**State: pending**
- Proposal submitted, awaiting review
- No impact on system behavior
- Memory fabric unchanged

**State: under_review**
- Human reviewer examining proposal
- Gathering additional context
- Memory fabric unchanged

**State: approved**
- Proposal accepted by governance
- Memory entry created in fabric
- Proposal marked as approved

**State: rejected**
- Proposal declined by governance
- No memory entry created
- Proposal marked as rejected with reason

---

## 3. Write Enforcement Rules

### 3.1 Direct Write Prohibition

**Prohibited:**
- ❌ Runtime agents writing memory without approval
- ❌ Builders writing high/critical memories without review
- ❌ Automatic learning loops that write memory
- ❌ Cross-tenant memory writes (always forbidden)

**Allowed:**
- ✅ Submitting memory proposals
- ✅ Writing low/medium importance within approved task scope
- ✅ Writing after explicit human approval
- ✅ Writing governance-approved patterns

### 3.2 Runtime Protection

**Implementation Requirements:**

1. Memory write clients MUST check proposal status before writing
2. High/critical writes MUST go through proposal queue
3. Rejected proposals MUST NOT retry automatically
4. All write operations MUST be logged

**Code Enforcement:**

```typescript
// CORRECT: Proposal-based approach
const proposalId = await submitMemoryProposal({
  scope: 'runtime',
  importance: 'high',
  ...
});
// Wait for approval, do NOT write directly

// INCORRECT: Direct write (forbidden for high importance)
await appendMemory({
  scope: 'runtime',
  importance: 'high',
  ...
}); // ❌ GOVERNANCE VIOLATION
```

---

## 4. Privacy and Security Rules

### 4.1 Forbidden Content

Memory entries MUST NEVER contain:

- ❌ Tenant-specific data (organisation names, user data)
- ❌ Personally identifiable information (PII)
- ❌ Customer secrets or credentials
- ❌ Raw logs with tenant information
- ❌ Cross-tenant references

### 4.2 Anonymization Requirements

If patterns involve tenant data:

1. Aggregate across multiple tenants
2. Remove all identifying information
3. Use statistical summaries only
4. Apply differential privacy where appropriate

---

## 5. Compliance and Audit

### 5.1 Audit Trail

All memory write operations MUST be logged:

- Timestamp
- Author (agent or human)
- Memory entry ID
- Approval mechanism (automatic, governance, human)
- Proposal ID (if applicable)

### 5.2 Governance Review Log

All proposals MUST maintain:

- Submission timestamp
- Review timestamps
- Reviewer identity
- Decision (approved/rejected)
- Decision rationale

---

## 6. Emergency Override

### 6.1 Conditions for Override

Emergency memory writes (bypassing proposal queue) are permitted ONLY when:

1. Platform outage in progress
2. Security incident requiring immediate response
3. Data loss prevention in progress
4. Human authorization explicitly granted

### 6.2 Override Procedure

1. Incident declared by runtime agent
2. Emergency write executed with justification
3. Retrospective review within 24 hours
4. Memory entry validated or reverted

---

## 7. Integration with Existing Systems

### 7.1 Memory Client Behavior

Existing `appendMemory()` function:

- Continues to work for low/medium importance within scope
- Automatically creates proposal for high/critical importance
- Returns proposal ID instead of memory ID for proposals
- Throws error if governance check fails

### 7.2 Runtime Agent Behavior

Runtime agents MUST:

- Submit proposals for all learning insights
- Never write memory without checking authority level
- Log all proposal submissions
- Handle rejected proposals gracefully

---

## 8. Validation and Testing

### 8.1 Required Tests

- ✅ Proposal submission works correctly
- ✅ High importance writes create proposals (not direct writes)
- ✅ Proposals stored separately from memory
- ✅ Memory fabric unchanged by proposals
- ✅ No automatic approval mechanism exists

### 8.2 Compliance Tests

- ✅ No PII in memory entries
- ✅ No cross-tenant references
- ✅ All writes have audit trail
- ✅ Rejected proposals leave no side effects

---

## Summary

**Memory writes are governed, not automatic.**

- ✅ All high/critical writes require governance approval
- ✅ Proposals are non-binding and leave memory unchanged
- ✅ Runtime agents cannot self-authorize memory writes
- ✅ Privacy and security rules are enforced
- ✅ Audit trail maintained for all operations

**Violation of this policy is a governance failure.**

---

## References

- Memory Schema: `/memory/schema/memory-entry.json`
- Memory Rules: `/foreman/behaviours/memory-rules.md`
- Memory Model: `/governance/policies/memory-model.md`
- Approval Workflow: `/memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md`

---

**Authority:** Johan Ras  
**Version:** 1.0.0  
**Status:** Active
