# Lessons to Canon Workflow — Memory Proposal Approval

## Purpose

This document defines the **approval workflow** for memory write proposals.

Memory write proposals flow through governance review before becoming permanent memory (canon).

---

## Core Principle

**Lessons must be validated before becoming canon.**

All high-impact memory entries require human review and explicit approval.

---

## 1. Workflow Overview

```
Agent Learning → Proposal Submission → Governance Review → Approval Decision → Canon Update
                                                         ↓
                                                      Rejection → Proposal Archive
```

---

## 2. Proposal Submission

### 2.1 Who Can Submit

Any authorized agent can submit a memory proposal:
- Foreman (build-time)
- Builder agents (during tasks)
- Runtime agent (during operations)
- QA agents (during validation)

### 2.2 When to Submit

Submit a memory proposal when:
- Agent detects a recurring pattern
- Agent learns from multiple similar events
- Agent identifies a governance-relevant insight
- Agent wants to record a high/critical importance memory

### 2.3 Submission Format

```json
{
  "proposal_id": "prop-YYYY-MM-DD-NNN",
  "proposed_by": "agent-identifier",
  "proposed_at": "ISO8601-timestamp",
  "status": "pending",
  "proposed_memory": {
    "scope": "global | foreman | runtime | platform",
    "title": "Human-readable title",
    "summary": "Brief summary",
    "importance": "high | critical",
    "tags": ["tag1", "tag2"],
    "details": {
      "rationale": "Why this memory matters",
      "context": "Background information",
      "evidence": "Supporting data (anonymized)"
    }
  },
  "rationale": "Detailed justification for this proposal",
  "evidence_count": 5,
  "first_observed": "ISO8601-timestamp",
  "last_observed": "ISO8601-timestamp"
}
```

---

## 3. Governance Review

### 3.1 Review Queue

Location: `/memory/proposals/pending/`

All pending proposals are visible to governance reviewers.

### 3.2 Review Criteria

Reviewers evaluate proposals based on:

**Relevance:**
- Does this lesson apply broadly?
- Is it specific to one incident or a pattern?
- Does it duplicate existing memory?

**Quality:**
- Is the summary clear and actionable?
- Is the evidence sufficient?
- Are tags appropriate?

**Privacy:**
- Does it contain PII or tenant data? (reject if yes)
- Is it properly anonymized?
- Does it respect tenant isolation?

**Governance Impact:**
- Does it align with build philosophy?
- Does it contradict existing governance?
- Does it require policy updates?

### 3.3 Review Actions

**Approve:**
- Proposal is valid and valuable
- Convert to permanent memory entry
- Add to appropriate scope directory
- Mark proposal as approved

**Reject:**
- Proposal is invalid, duplicate, or violates governance
- Add rejection reason to proposal
- Move to rejected archive
- DO NOT create memory entry

**Request More Information:**
- Proposal needs clarification
- Mark as "under_review"
- Add reviewer notes
- Agent may update proposal with additional context

---

## 4. Approval Decision

### 4.1 Approval Process

When a proposal is approved:

1. **Validate Proposal:**
   - Check schema compliance
   - Verify no PII or sensitive data
   - Confirm importance level is appropriate

2. **Create Memory Entry:**
   - Generate memory ID
   - Set created_at timestamp
   - Set author to "governance" (human-approved)
   - Copy proposal content to memory entry

3. **Write to Memory Fabric:**
   - Write to appropriate scope directory (global, foreman, runtime)
   - Append to date-based collection file
   - Commit to version control

4. **Update Proposal Status:**
   - Mark proposal as "approved"
   - Add approval timestamp
   - Add reviewer name
   - Link to created memory ID

5. **Archive Proposal:**
   - Move proposal from pending to approved archive
   - Maintain proposal for audit trail

### 4.2 Rejection Process

When a proposal is rejected:

1. **Add Rejection Reason:**
   - Clear explanation of why rejected
   - Specific governance rule violated (if applicable)
   - Guidance for future proposals (if applicable)

2. **Update Proposal Status:**
   - Mark proposal as "rejected"
   - Add rejection timestamp
   - Add reviewer name

3. **Archive Proposal:**
   - Move proposal from pending to rejected archive
   - DO NOT create memory entry
   - Memory fabric remains unchanged

4. **Notify Agent (optional):**
   - Log rejection for agent learning
   - Agent may refine and resubmit later

---

## 5. Review SLA

### 5.1 Review Timing

- **Standard Proposals:** Review within 7 days
- **Critical Proposals:** Review within 24 hours
- **Emergency Proposals:** Review immediately (if justified)

### 5.2 Escalation

If proposals are not reviewed within SLA:
- Notify Johan Ras
- Review governance review capacity
- Prioritize high-impact proposals

---

## 6. Proposal Management

### 6.1 Directory Structure

```
/memory/proposals/
  pending/          # Awaiting review
  under_review/     # Being evaluated
  approved/         # Approved and converted to memory
  rejected/         # Rejected proposals
```

### 6.2 Proposal Lifecycle Tracking

Each proposal maintains full history:
- Submission timestamp
- All status changes
- Reviewer actions
- Final decision and rationale

### 6.3 Proposal Queries

Governance reviewers can query:
- All pending proposals
- Proposals by agent
- Proposals by scope
- Proposals by importance
- Recently approved/rejected proposals

---

## 7. Automation Boundaries

### 7.1 What Can Be Automated

- ✅ Proposal submission
- ✅ Schema validation
- ✅ PII detection (basic checks)
- ✅ Duplicate detection
- ✅ Moving proposals between states

### 7.2 What Cannot Be Automated

- ❌ Approval decisions (human only)
- ❌ Rejection decisions (human only)
- ❌ Governance impact assessment
- ❌ Overriding governance rules
- ❌ Creating memory entries without approval

---

## 8. Special Cases

### 8.1 Emergency Proposals

For critical platform incidents:

1. Agent submits proposal marked as "emergency"
2. Reviewer notified immediately
3. Fast-track review (< 1 hour target)
4. If approved, memory created immediately
5. Retrospective full review within 24 hours

### 8.2 Batch Proposals

For multiple related proposals:

1. Agent submits proposals as batch
2. Reviewer can approve/reject batch atomically
3. Batch rationale provided
4. Individual proposals still tracked

### 8.3 Provisional Approvals

For time-sensitive patterns:

1. Reviewer can grant provisional approval
2. Memory entry created with "provisional" flag
3. Full review completed within 7 days
4. Memory validated or reverted after full review

---

## 9. Audit and Compliance

### 9.1 Audit Trail

All proposal lifecycle events logged:
- Submission
- Status changes
- Reviewer actions
- Approval/rejection decisions
- Memory entry creation

### 9.2 Compliance Checks

Regular audits verify:
- No unauthorized memory writes
- All high/critical memories have proposal trail
- No PII in approved proposals
- Rejection reasons documented
- SLA compliance

---

## 10. Integration with Memory Fabric

### 10.1 Memory Entry Creation

Approved proposals become memory entries with:
- **Author:** Set to "governance" (not agent)
- **Created_at:** Set to approval timestamp
- **Metadata:** Link to source proposal ID
- **Tags:** Include "governance-approved"

### 10.2 Memory Entry Validation

After creation:
- Validate against memory schema
- Run health check on memory fabric
- Verify no duplicate entries
- Confirm version control commit

---

## Summary

**The Lessons to Canon workflow ensures quality and governance compliance.**

- ✅ Agents propose, humans approve
- ✅ All high/critical memories require review
- ✅ Proposals are non-binding until approved
- ✅ Memory fabric remains clean and governed
- ✅ Full audit trail maintained

**This workflow prevents automatic learning loops while enabling safe memory growth.**

---

## References

- Memory Write Policy: `/memory/AUTHORITY/MEMORY_WRITE_POLICY.md`
- Memory Schema: `/memory/schema/memory-entry.json`
- Memory Rules: `/foreman/behaviours/memory-rules.md`

---

**Authority:** Johan Ras  
**Version:** 1.0.0  
**Status:** Active
