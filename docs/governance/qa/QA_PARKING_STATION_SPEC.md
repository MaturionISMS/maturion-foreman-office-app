# QA Parking Station Specification

**Status:** Governance Specification  
**Authority:** Foreman Governance  
**Source:** Issue #76 (FMQA-2) — Bucket D Intent Consolidation  
**Last Updated:** 2025-12-29

---

## Purpose

This specification defines the **QA Parking Station** mechanism — a governance-controlled approach for handling QA work that cannot be completed immediately due to external blockers, future dependencies, or deferred scope decisions.

The parking station ensures that **no test coverage is permanently skipped or lost** while providing a transparent, governed workflow for deferred QA work.

---

## Core Principles

### 1. No Test Dodging
- Tests are **never skipped** without explicit governance approval
- All deferred tests must be registered in the parking station
- Parking station entries require justification and acceptance criteria

### 2. Transparency
- All parked QA items are visible and tracked
- Parking station state is auditable
- Watcher mechanism alerts on stale entries

### 3. Eventual Completion
- Every parked item has defined unblocking criteria
- Parked items are automatically surfaced when unblocking conditions are met
- No indefinite deferral without re-approval

---

## Parking Station Components

### Component 1: Parking Station Registry

**Location:** `qa/parking-station/registry.json`

**Schema:**
```json
{
  "parked_items": [
    {
      "id": "unique-identifier",
      "type": "test" | "coverage-area" | "qa-requirement",
      "title": "Human-readable title",
      "reason": "Why this is parked (blocker, future scope, etc.)",
      "unblocking_criteria": "What must happen before this can be unparked",
      "parked_date": "ISO 8601 timestamp",
      "parked_by": "Agent or human authority",
      "target_module": "Module this QA belongs to",
      "priority": "high" | "medium" | "low",
      "review_by_date": "ISO 8601 timestamp - when this must be reviewed",
      "status": "parked" | "unblocked" | "in-progress" | "completed"
    }
  ]
}
```

### Component 2: QA Parking Watcher

**Purpose:** Monitor parking station for items that require attention

**Trigger Conditions:**
- Item has been parked longer than 30 days without review
- Unblocking criteria may now be satisfied
- Review-by date is approaching or past due
- Priority items remain parked for > 14 days

**Alert Mechanism:**
- Watcher generates alerts via watchdog system
- Alerts are routed to Foreman runtime monitoring
- Human escalation triggered for high-priority overdue items

**Watcher Implementation Location:** `foreman/runtime/watchdog/qa_parking_watcher.py`

### Component 3: Parking Station API

**Operations:**

1. **Park QA Item**
   - Input: QA item details, justification, unblocking criteria
   - Validation: Requires governance approval level authority
   - Output: Parking station entry created, ticket ID returned

2. **Review Parked Item**
   - Input: Parking station entry ID
   - Check: Evaluate if unblocking criteria are met
   - Output: Status update (remains parked, unblocked, escalated)

3. **Unblock QA Item**
   - Input: Parking station entry ID, evidence that criteria are met
   - Validation: Verify unblocking criteria satisfaction
   - Output: Item moved to active QA queue, implementation task created

4. **List Parked Items**
   - Input: Optional filters (module, priority, age)
   - Output: List of parked items matching criteria

---

## Governance Rules

### Rule 1: Parking Requires Justification
- Every parked item MUST include:
  - Clear reason for parking (not "we don't want to do this")
  - Specific unblocking criteria
  - Target review date
  - Priority classification

### Rule 2: Parking Is Not Permanent Deferral
- Items cannot remain parked indefinitely
- After 90 days, parked items must be:
  - Unblocked and implemented
  - Re-justified with new review date
  - Escalated to human authority for decision

### Rule 3: High-Priority Items Have Strict Limits
- High-priority QA cannot be parked longer than 14 days
- High-priority parking requires Johan (CS2) approval
- High-priority items trigger daily watcher alerts after 7 days

### Rule 4: Parking Station Audits
- Monthly audit of all parked items
- Audit report includes:
  - Age distribution of parked items
  - Items approaching review dates
  - Items with satisfied unblocking criteria
  - Recommendations for escalation

---

## Workflow

### Parking Workflow

1. **Identify Need to Park**
   - QA item cannot be completed due to blocker
   - Blocker is external or future-scoped

2. **Create Parking Request**
   - Document item, reason, unblocking criteria
   - Assign priority and review date

3. **Governance Approval**
   - Submit request to parking station API
   - Automated approval for low-priority, <30 day deferrals
   - Human approval required for high-priority or >30 day deferrals

4. **Park Item**
   - Item added to parking station registry
   - Watcher begins monitoring
   - Alert schedule established

5. **Monitor & Review**
   - Watcher checks unblocking criteria periodically
   - Review date triggers re-evaluation
   - Alerts escalate stale items

### Unblocking Workflow

1. **Detect Unblocking Condition**
   - Watcher identifies satisfied criteria
   - OR manual review determines item can be unblocked

2. **Unblock Item**
   - Item status changed to "unblocked"
   - Implementation task created in active queue
   - Original parked item linked to new task

3. **Execute Unblocked QA**
   - QA work proceeds as normal active work
   - Completion closes parking station entry

4. **Close Parking Entry**
   - Entry marked "completed"
   - Audit trail preserved for future reference

---

## Integration Points

### With Build Authorization Gate (FR-1.2)
- Parking station status is checked before builds
- If critical QA is parked without valid justification, gate FAILS
- Gate accepts properly governed parking with valid justification

### With QA Builder Agent
- QA builder can query parking station for unblocked items
- QA builder CANNOT park items without governance approval
- QA builder receives watcher alerts for relevant items

### With Foreman Runtime Monitoring
- Parking station watcher integrates with watchdog system
- Alerts are routed through standard escalation channels
- Metrics on parking station health included in runtime dashboards

---

## Success Criteria

The parking station mechanism is successful when:

1. **Zero Permanent Skips**
   - No tests are skipped in production code without parking station entry
   - All skipped tests have clear unblocking path

2. **Transparent Visibility**
   - All stakeholders can see parked QA status
   - Parking station state is auditable and queryable

3. **Timely Unblocking**
   - Parked items are unblocked within reasonable timeframes
   - No items remain parked longer than governance limits

4. **No Test Dodging**
   - Parking mechanism cannot be abused to avoid QA work
   - Governance approval required for all parking
   - Watcher alerts prevent indefinite deferral

---

## Future Extensions

Potential enhancements to consider after v1:

- **Automatic Dependency Detection:** Watcher automatically checks if blocking issues are resolved
- **Cross-Module Parking:** Support QA items that span multiple modules
- **Historical Analytics:** Track parking patterns to identify systemic blockers
- **Integration with ISMS Modules:** Extend parking station to ISMS module QA

---

## References

- **Source Issue:** #76 (FMQA-2) — Implement Governed QA Parking Station (No Skips) + Watcher
- **Related Governance:** Build Authorization Gate (FR-1.2)
- **Related Architecture:** True North FM Architecture Section 3.1 (QA Governance)
- **Bucket D Classification:** BACKLOG_CONSOLIDATION_REPORT.md

---

**Document Status:** CANONICAL  
**Implementation Status:** NOT YET IMPLEMENTED  
**Next Action:** Implementation tasks to be created when FM v1 build is complete
