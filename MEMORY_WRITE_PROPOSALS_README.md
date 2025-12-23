# Memory Write Proposals — Implementation Guide

## Purpose

This document describes the **Memory Write Proposal mechanism** for the FM App.

This mechanism allows agents to **propose** memory writes without **automatically executing** them.

All high-impact memory writes require **explicit governance approval**.

---

## Governance Authority

This implementation strictly complies with governance definitions in:

- `/memory/AUTHORITY/MEMORY_WRITE_POLICY.md` — Authority levels and write rules
- `/memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md` — Approval workflow
- `/memory/schema/memory-proposal.json` — Proposal structure
- `/foreman/behaviours/memory-rules.md` — When to write memory

**Governance is the source of truth. Runtime must conform.**

---

## What Are Memory Write Proposals?

Memory write proposals are **non-binding requests** to add entries to the memory fabric.

**Key Characteristics:**

- ✅ **Proposals are separate from memory** — Stored in `/memory/proposals/`
- ✅ **Proposals do NOT change memory** — Memory fabric remains unchanged
- ✅ **Proposals require approval** — Human review before becoming memory
- ✅ **Proposals are visible** — All pending proposals accessible for review
- ✅ **Proposals are auditable** — Full lifecycle tracked

**Anti-Characteristics:**

- ❌ **NOT automatic** — No auto-approval mechanism
- ❌ **NOT learning loops** — No self-modification
- ❌ **NOT tenant-specific** — Only aggregate, anonymized patterns
- ❌ **NOT immediate** — Approval required before memory creation

---

## Why Proposals Instead of Direct Writes?

### Problem: Uncontrolled Learning

Without proposals, agents could:
- Write any memory entry automatically
- Create self-reinforcing patterns
- Pollute memory with low-quality entries
- Violate privacy by recording PII
- Create governance drift over time

### Solution: Governed Learning

With proposals:
- ✅ Human oversight on high-impact memories
- ✅ Quality control before memory creation
- ✅ Privacy validation before approval
- ✅ Governance alignment enforced
- ✅ Audit trail of all proposals

---

## Architecture

### Directory Structure

```
/memory/
  AUTHORITY/
    MEMORY_WRITE_POLICY.md           # Governance rules
    LESSONS_TO_CANON_WORKFLOW.md     # Approval workflow
  proposals/                         # Proposal storage (separate!)
    pending/                         # Awaiting review
    under_review/                    # Being evaluated
    approved/                        # Approved and converted
    rejected/                        # Rejected with reason
  schema/
    memory-proposal.json             # Proposal schema
  global/                            # Actual memory fabric
  foreman/                           # Actual memory fabric
  runtime/                           # Actual memory fabric
```

### Components

```
lib/memory/
├── client.ts              # Memory client (read + write)
├── runtime-loader.ts      # Runtime loader (read-only)
└── proposal-client.ts     # Proposal client (propose only) ← NEW

python_agent/
├── memory_client.py       # Memory client (read + write)
└── memory_proposal_client.py  # Proposal client (propose only) ← NEW
```

---

## Usage

### TypeScript Usage

```typescript
import { submitMemoryProposal, listMemoryProposals } from '@/lib/memory/proposal-client';

// Submit a proposal (does NOT write to memory)
const proposalId = await submitMemoryProposal({
  proposed_by: 'runtime-agent',
  proposed_memory: {
    scope: 'runtime',
    title: 'Auto-fix Pattern Detected',
    summary: 'Pattern for handling database connection timeouts',
    importance: 'high',
    tags: ['runtime', 'auto-fix', 'pattern'],
    details: {
      rationale: 'This pattern successfully resolved 5 incidents',
      context: 'Occurs during high load periods'
    }
  },
  rationale: 'Recording this pattern will enable faster auto-fix responses for similar incidents in the future. Pattern has proven reliable across multiple occurrences.',
  evidence_count: 5,
  first_observed: '2024-12-15T08:00:00Z',
  last_observed: '2024-12-22T16:45:00Z'
});

console.log(`Proposal submitted: ${proposalId}`);

// List pending proposals (for governance review)
const pending = await listMemoryProposals('pending');
console.log(`Pending proposals: ${pending.length}`);

// Check proposal status
const status = await getProposalStatus(proposalId);
console.log(`Proposal status: ${status}`);
```

### Python Usage

```python
from python_agent.memory_proposal_client import (
    submit_memory_proposal,
    list_memory_proposals,
    get_proposal_status
)

# Submit a proposal (does NOT write to memory)
proposal_id = submit_memory_proposal(
    proposed_by='runtime-agent',
    proposed_memory={
        'scope': 'runtime',
        'title': 'Auto-fix Pattern Detected',
        'summary': 'Pattern for handling database connection timeouts',
        'importance': 'high',
        'tags': ['runtime', 'auto-fix', 'pattern']
    },
    rationale='Recording this pattern will enable faster auto-fix responses. Pattern proven reliable.',
    evidence_count=5,
    first_observed='2024-12-15T08:00:00Z',
    last_observed='2024-12-22T16:45:00Z'
)

print(f'Proposal submitted: {proposal_id}')

# List pending proposals
pending = list_memory_proposals(status='pending')
print(f'Pending proposals: {len(pending)}')

# Check status
status = get_proposal_status(proposal_id)
print(f'Proposal status: {status}')
```

---

## Proposal Lifecycle

### 1. Submission

**Who:** Any agent (Foreman, builders, runtime)  
**What:** Agent detects a pattern worth recording  
**How:** Call `submitMemoryProposal()` with complete proposal

**Validation:**
- ✅ Required fields present
- ✅ Rationale at least 50 characters
- ✅ No PII or sensitive data detected
- ✅ Proposed memory follows schema

**Result:** Proposal ID returned, proposal saved to `pending/`

### 2. Pending Review

**Status:** `pending`  
**Location:** `/memory/proposals/pending/`  
**Visibility:** Available for governance review  
**Impact:** **NONE** — Memory fabric unchanged

Governance reviewers:
- Access pending proposals via dashboard or CLI
- Review rationale and evidence
- Evaluate against governance criteria
- Move to `under_review` or make decision

### 3. Under Review

**Status:** `under_review`  
**Location:** `/memory/proposals/under_review/`  
**Visibility:** In active review  
**Impact:** **NONE** — Memory fabric unchanged

Reviewers can:
- Add review notes
- Request more information
- Gather additional context
- Prepare for decision

### 4. Approved

**Status:** `approved`  
**Location:** `/memory/proposals/approved/`  
**Visibility:** Archived with decision  
**Impact:** **Memory entry CREATED** in fabric

When approved:
1. Proposal validated against schema
2. Memory entry created in appropriate scope
3. Proposal marked as approved
4. Proposal links to created memory ID
5. Proposal archived

### 5. Rejected

**Status:** `rejected`  
**Location:** `/memory/proposals/rejected/`  
**Visibility:** Archived with reason  
**Impact:** **NONE** — Memory fabric unchanged

When rejected:
1. Rejection reason documented
2. Proposal marked as rejected
3. Proposal archived
4. **NO** memory entry created

---

## Governance Review Criteria

Reviewers evaluate proposals based on:

### 1. Relevance

- Does this lesson apply broadly?
- Is it specific to one incident or a pattern?
- Does it duplicate existing memory?

### 2. Quality

- Is the summary clear and actionable?
- Is the evidence sufficient?
- Are tags appropriate?
- Is importance level correct?

### 3. Privacy

- Does it contain PII or tenant data? (reject if yes)
- Is it properly anonymized?
- Does it respect tenant isolation?

### 4. Governance Impact

- Does it align with build philosophy?
- Does it contradict existing governance?
- Does it require policy updates?

---

## Safety Guarantees

### Guarantee 1: No Auto-Approval

**Enforcement:**
- All proposals start with `pending` status
- Status can ONLY be changed by human reviewer
- No code path exists for automatic approval
- Tests validate no auto-approval mechanism

### Guarantee 2: Memory Isolation

**Enforcement:**
- Proposals stored in `/memory/proposals/`
- Memory fabric in `/memory/{scope}/`
- Proposals NOT loadable as memory scope
- Tests validate separation

### Guarantee 3: No Side Effects

**Enforcement:**
- Submitting proposal does NOT modify memory
- Rejected proposals leave NO artifacts in memory
- Tests validate memory count unchanged

### Guarantee 4: Privacy Protection

**Enforcement:**
- Basic PII detection in validation
- Forbidden patterns rejected
- Manual review catches subtle violations
- Tests validate PII rejection

---

## Integration Points

### When to Use Proposals

**REQUIRED for:**
- High importance memories
- Critical importance memories
- Global scope entries (unless approved task)
- Governance rule changes
- Architecture pattern additions

**OPTIONAL for:**
- Low importance task-scoped entries
- Medium importance within approved task
- Explicit human-directed entries

### Integration with Existing Memory Client

The existing `appendMemory()` function continues to work for low/medium importance.

**Future Enhancement (Out of Scope):**

```typescript
// In future, appendMemory could auto-route high importance to proposals
await appendMemory({
  scope: 'runtime',
  importance: 'high',  // Triggers proposal instead of direct write
  ...
});
// Returns proposal ID, not memory ID
```

**Current Behavior:**

```typescript
// Currently, use proposal client explicitly for high importance
const proposalId = await submitMemoryProposal({
  proposed_memory: {
    importance: 'high',
    ...
  }
});
```

---

## Testing

### Test Suite: `tests/test_memory_proposals.py`

**Coverage:**

- ✅ Proposal submission functionality
- ✅ Proposal storage (separate from memory)
- ✅ Memory fabric isolation (unchanged by proposals)
- ✅ Governance review path visibility
- ✅ No auto-approval enforcement
- ✅ PII validation
- ✅ Required field validation
- ✅ Directory structure

**Run Tests:**

```bash
# Run proposal tests only
pytest tests/test_memory_proposals.py -v

# Run with markers
pytest -m memory -v
```

**Expected Results:**

All tests pass, validating:

1. Proposals can be submitted
2. Proposals stored separately from memory
3. Memory fabric unchanged after proposals
4. Pending proposals visible for review
5. No automatic approval occurs
6. PII detection works
7. Governance policies exist

---

## Operational Procedures

### For Agents

**When to submit a proposal:**

1. Detect recurring pattern (3+ occurrences)
2. Identify governance-relevant insight
3. Learn from multiple similar events
4. Want to record high/critical memory

**How to submit:**

```python
proposal_id = submit_memory_proposal(
    proposed_by='my-agent-name',
    proposed_memory={...},
    rationale='Clear justification (50+ chars)',
    evidence_count=5,  # How many times observed
    first_observed='ISO8601',
    last_observed='ISO8601'
)
```

**After submission:**

- Log proposal ID for tracking
- Continue normal operations
- Do NOT assume proposal will be approved
- Do NOT retry if rejected

### For Governance Reviewers

**Access pending proposals:**

```python
from python_agent.memory_proposal_client import list_memory_proposals

pending = list_memory_proposals(status='pending')
for proposal in pending:
    print(f"ID: {proposal['proposal_id']}")
    print(f"By: {proposal['proposed_by']}")
    print(f"Title: {proposal['proposed_memory']['title']}")
    print(f"Rationale: {proposal['rationale']}")
    print("---")
```

**Review workflow:**

1. Read proposal rationale and evidence
2. Evaluate against governance criteria
3. Check for PII or policy violations
4. Make decision: approve or reject
5. Document decision reason
6. Update proposal status
7. If approved, create memory entry

---

## Compliance and Audit

### Audit Trail

Every proposal maintains:

- Submission timestamp
- Submitting agent
- All status changes
- Review notes
- Final decision and reason
- Created memory ID (if approved)

### Compliance Checks

Regular audits verify:

- ✅ No unauthorized memory writes (all high/critical via proposals)
- ✅ All proposals have complete audit trail
- ✅ Rejected proposals have documented reasons
- ✅ No PII in approved proposals
- ✅ SLA compliance on review timing

---

## Future Enhancements (Out of Scope)

**Phase 2 Enhancements:**

1. **Dashboard UI:** Visual interface for reviewing proposals
2. **Batch Review:** Approve/reject multiple related proposals
3. **Auto-routing:** High importance writes auto-create proposals
4. **Notifications:** Alert reviewers of pending proposals
5. **Analytics:** Track proposal approval rates, patterns
6. **Provisional Approval:** Temporary approval with follow-up review

**These are NOT in this PR.**

---

## Troubleshooting

### Proposal Submission Fails

**Symptom:** `ValueError: rationale is required and must be at least 50 characters`

**Solution:** Provide detailed rationale (minimum 50 characters)

### Proposal Contains Forbidden Content

**Symptom:** `ValueError: Proposal may contain forbidden content`

**Solution:** Remove PII, tenant data, or sensitive information. Anonymize all examples.

### Proposal Not Visible

**Symptom:** Submitted proposal not in pending list

**Solution:**

1. Check proposal ID was returned
2. Verify `/memory/proposals/pending/` directory exists
3. Check proposal file exists: `proposals/pending/{proposal_id}.json`
4. Verify no file system permissions issues

### Memory Not Updated After Approval

**Symptom:** Approved proposal but memory unchanged

**Solution:** Approval process must explicitly create memory entry. Check approval implementation includes memory creation step.

---

## References

- **Governance Policy:** `/memory/AUTHORITY/MEMORY_WRITE_POLICY.md`
- **Approval Workflow:** `/memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md`
- **Proposal Schema:** `/memory/schema/memory-proposal.json`
- **Memory Schema:** `/memory/schema/memory-entry.json`
- **Memory Rules:** `/foreman/behaviours/memory-rules.md`
- **TypeScript Client:** `/lib/memory/proposal-client.ts`
- **Python Client:** `/python_agent/memory_proposal_client.py`
- **Test Suite:** `/tests/test_memory_proposals.py`

---

## Compliance Statement

This implementation:

✅ Complies with `/memory/AUTHORITY/MEMORY_WRITE_POLICY.md`  
✅ Follows `/memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md`  
✅ Uses governance-defined proposal structure  
✅ Enforces proposal-based approval for high/critical writes  
✅ Validates proposals against privacy rules  
✅ Maintains separation between proposals and memory  
✅ Prevents automatic approval  
✅ Documents all behavior explicitly  
✅ Provides comprehensive test coverage  

**No governance rules were bypassed or weakened.**

**Proposals are disabled by default (require explicit human approval).**

---

**End of Memory Write Proposals Implementation Guide**
