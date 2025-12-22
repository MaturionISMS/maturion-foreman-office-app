# PR Gate Failure Handling Protocol (Canonical Mirror)

**Status**: Authoritative  
**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  
**Role**: Canonical failure handling semantics

---

## I. Constitutional Statement

**All PR gate failures are classified using canonical categories.**

FM Repository Role:
- ✅ Classify failures using canonical taxonomy
- ✅ Log failures with canonical schema
- ✅ Escalate per canonical protocol
- ❌ NEVER create FM-specific failure types
- ❌ NEVER reinterpret failure severity
- ❌ NEVER weaken failure handling

---

## II. Canonical Failure Categories

### Category 1: ARTIFACT_MISSING

**Definition**: Required artifact not present in PR

**Examples**:
- Builder QA Report missing
- Governance evidence missing
- Architecture validation report missing
- Evidence chain incomplete

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `ARTIFACT_MISSING` classification
3. Return list of missing artifacts
4. Provide artifact requirements documentation link
5. Do NOT retry until artifacts present

**Severity**: HIGH (blocks merge)

**Resolution**: Add missing artifacts, push commit, re-run gates

---

### Category 2: SCHEMA_VIOLATION

**Definition**: Artifact present but schema non-compliant

**Examples**:
- Builder QA Report missing required fields
- Evidence JSON structure invalid
- Timestamp format incorrect
- Required field has wrong type

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `SCHEMA_VIOLATION` classification
3. Return schema validation errors (field-level detail)
4. Provide canonical schema reference
5. Do NOT retry until schema valid

**Severity**: HIGH (blocks merge)

**Resolution**: Fix schema violations, push commit, re-run gates

---

### Category 3: IMMUTABILITY_VIOLATION

**Definition**: Artifact modified after generation (integrity violation)

**Examples**:
- Evidence file timestamp changed
- Evidence content modified
- Immutable flag missing or false
- Hash mismatch detected

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `IMMUTABILITY_VIOLATION` classification
3. Flag as potential integrity compromise
4. Escalate to Johan Ras (mandatory)
5. Require investigation before retry

**Severity**: CRITICAL (integrity violation)

**Resolution**: Regenerate evidence, investigate cause, prevent recurrence

---

### Category 4: AGENT_BOUNDARY_VIOLATION

**Definition**: Agent executed QA outside its scope

**Examples**:
- Builder agent ran Governance QA
- Governance agent ran Builder QA
- FM agent ran Builder QA
- QA report attributed to wrong agent

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `AGENT_BOUNDARY_VIOLATION` classification
3. Flag as CATASTROPHIC governance violation
4. Escalate to Johan Ras (mandatory)
5. Halt all related work
6. Require root cause analysis

**Severity**: CATASTROPHIC (separation of duties violated)

**Resolution**: Remove violating QA, execute in correct scope, update agent contracts

---

### Category 5: NOT_READY_DECLARATION

**Definition**: Builder explicitly declares NOT_READY status

**Examples**:
- Builder QA Report `qa_status: NOT_READY`
- Builder detected failing tests
- Builder detected incomplete implementation
- Builder detected unmet requirements

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `NOT_READY_DECLARATION` classification
3. Trust Builder's declaration (no override)
4. Return Builder's reason for NOT_READY
5. Wait for Builder to fix and declare READY

**Severity**: HIGH (blocks merge, but expected workflow)

**Resolution**: Builder fixes issues, declares READY, re-runs gates

---

### Category 6: ARCHITECTURE_INCOMPLETE

**Definition**: Architecture declares completeness < 100% or drift present

**Examples**:
- Architecture completeness = 99%
- Drift status = OPEN
- Validation report missing
- Canonical checklist reference missing

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `ARCHITECTURE_INCOMPLETE` classification
3. Return completeness percentage and drift items
4. Do NOT allow merge with incomplete architecture
5. Require 100% completeness and zero drift

**Severity**: HIGH (blocks merge)

**Resolution**: Complete architecture, clear drift, re-run gates

---

### Category 7: TEST_DEBT_DETECTED

**Definition**: Test dodging patterns or DP-RED violations detected

**Examples**:
- `.skip()`, `.only()`, `.todo()` patterns found
- Commented out tests
- DP-RED present in Build-to-Green phase
- Skipped tests in Builder QA Report

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `TEST_DEBT_DETECTED` classification
3. Return list of test debt locations (file + line)
4. Reference Zero Test Debt Constitutional Rule
5. Require complete test implementation

**Severity**: HIGH (constitutional violation)

**Resolution**: Implement all tests, clear DP-RED, achieve 100% pass

---

### Category 8: GOVERNANCE_INVARIANT_VIOLATED

**Definition**: Governance rule or invariant broken

**Examples**:
- Constitutional rule violated
- Mandatory field missing
- Governance policy not followed
- Compliance control not satisfied

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `GOVERNANCE_INVARIANT_VIOLATED` classification
3. Return specific governance rule violated
4. Reference canonical governance documentation
5. Require compliance before retry

**Severity**: HIGH (governance violation)

**Resolution**: Fix violation, comply with governance, re-run gates

---

### Category 9: TRACEABILITY_BROKEN

**Definition**: Evidence chain incomplete or parent references missing

**Examples**:
- Evidence missing parent_evidence_id
- Build initiation ID not found
- Evidence chain gap detected
- Chronological inconsistency

**FM Action**:
1. BLOCK merge immediately
2. Log failure with `TRACEABILITY_BROKEN` classification
3. Return evidence chain gap details
4. Require complete traceability
5. Do NOT allow merge with broken chain

**Severity**: HIGH (audit trail incomplete)

**Resolution**: Complete evidence chain, fix traceability, re-run gates

---

### Category 10: CATASTROPHIC_FAILURE

**Definition**: Unexpected failure requiring immediate escalation

**Examples**:
- PR gate script crash
- Governance schema corruption
- Build environment failure
- Canonical governance unreachable

**FM Action**:
1. HALT all work immediately
2. Log failure with `CATASTROPHIC_FAILURE` classification
3. Escalate to Johan Ras (mandatory)
4. Create catastrophic failure issue
5. Require investigation before any retry

**Severity**: CATASTROPHIC (system integrity at risk)

**Resolution**: Investigate root cause, implement prevention, verify fix

---

## III. Failure Record Schema

**Canonical Schema**: All failures logged using this structure

```json
{
  "failure_id": "uuid",
  "failure_category": "ARTIFACT_MISSING | SCHEMA_VIOLATION | IMMUTABILITY_VIOLATION | AGENT_BOUNDARY_VIOLATION | NOT_READY_DECLARATION | ARCHITECTURE_INCOMPLETE | TEST_DEBT_DETECTED | GOVERNANCE_INVARIANT_VIOLATED | TRACEABILITY_BROKEN | CATASTROPHIC_FAILURE",
  "severity": "LOW | MEDIUM | HIGH | CRITICAL | CATASTROPHIC",
  "pr_number": "integer",
  "commit_sha": "string",
  "gate_name": "string",
  "timestamp": "ISO-8601",
  "failure_details": {
    "summary": "string (1-2 sentences)",
    "details": "string (detailed description)",
    "artifacts_affected": ["string"],
    "error_messages": ["string"]
  },
  "resolution_required": {
    "actions": ["string"],
    "documentation_links": ["string"],
    "escalation_required": "boolean",
    "escalation_target": "string or null"
  },
  "canonical_reference": {
    "failure_protocol_version": "string",
    "governance_canon_version": "string",
    "classification_source": "maturion-foreman-governance"
  },
  "immutable": true
}
```

---

## IV. Escalation Protocol

### When to Escalate

**Mandatory Escalation** (no exceptions):
- CATASTROPHIC severity failures
- AGENT_BOUNDARY_VIOLATION
- IMMUTABILITY_VIOLATION
- Repeat failures (3rd occurrence)
- Governance conflicts
- Canonical governance unreachable

**Recommended Escalation**:
- CRITICAL severity failures
- Unresolvable gate failures
- Governance ambiguities
- Emergency override requests

**Optional Escalation**:
- HIGH severity failures (after 2 attempts)
- Governance clarification needed
- Prevention measure proposals

---

### Escalation Targets

**Johan Ras (Owner)**: All CATASTROPHIC and CRITICAL failures

**Governance Liaison**: Governance-related failures, canonical updates

**FM Builder**: Implementation-related failures, Builder QA issues

---

### Escalation Evidence Required

When escalating, provide:
1. Failure record (canonical schema)
2. PR number and commit SHA
3. Detailed error messages
4. Steps to reproduce
5. Attempted resolutions
6. Proposed solution (if known)
7. Impact assessment

---

## V. Failure Handling Workflow

### Step 1: Detect Failure

**Who**: PR gate workflow (Gatekeeper 1 or 2)

**Action**:
- Execute gate validation
- Detect failure condition
- Capture failure details

---

### Step 2: Classify Failure

**Who**: PR gate workflow

**Action**:
- Map failure to canonical category
- Determine severity
- Identify affected artifacts

**Prohibited**:
- ❌ Create FM-specific categories
- ❌ Reinterpret severity
- ❌ Downgrade severity to pass

---

### Step 3: Log Failure

**Who**: PR gate workflow

**Action**:
- Create failure record (canonical schema)
- Write to `governance/events/failures/<failure-id>.json`
- Set immutable flag

**Required Fields**: All fields in canonical schema

---

### Step 4: Block Merge

**Who**: PR gate workflow

**Action**:
- Set gate status to RED
- Prevent merge (no override)
- Return failure details to PR

**Prohibited**:
- ❌ Allow merge with RED gate
- ❌ Auto-retry without fix
- ❌ Weaken gate to pass

---

### Step 5: Report Failure

**Who**: PR gate workflow

**Action**:
- Comment on PR with failure details
- Provide resolution instructions
- Link to relevant documentation
- List required actions

**Comment Template**:
```markdown
❌ **PR Gate Failure: {CATEGORY}**

**Gate**: {gate_name}  
**Severity**: {severity}  
**Classification**: {failure_category}

**Summary**: {failure_summary}

**Details**:
{failure_details}

**Required Actions**:
1. {action_1}
2. {action_2}
...

**Documentation**: {doc_links}

**Escalation**: {escalation_required ? escalation_instructions : "Not required"}

**Failure ID**: {failure_id}
```

---

### Step 6: Wait for Fix

**Who**: Builder / Developer

**Action**:
- Read failure details
- Understand root cause
- Implement fix
- Push commit
- Re-run PR gates

**Prohibited**:
- ❌ Bypass gate
- ❌ Disable gate
- ❌ Request override without fix

---

### Step 7: Re-run Gates

**Who**: PR gate workflow (triggered by new commit)

**Action**:
- Re-validate all gates
- Check if failure resolved
- If resolved: PASS (allow merge)
- If not resolved: FAIL (repeat from Step 1)

---

### Step 8: Log Resolution

**Who**: PR gate workflow (on success)

**Action**:
- Update failure record with resolution
- Mark failure as RESOLVED
- Record resolution commit SHA
- Keep failure record (immutable)

**Resolution Record**:
```json
{
  "resolution": {
    "resolved": true,
    "resolution_timestamp": "ISO-8601",
    "resolution_commit": "string",
    "resolution_pr": "integer",
    "resolution_summary": "string"
  }
}
```

---

## VI. Repeat Failure Handling

### First Occurrence

**Action**: Standard failure handling (Steps 1-8)

**Severity**: As classified

**Escalation**: Per category

---

### Second Occurrence (Repeat)

**Action**:
- Mark as REPEAT in failure record
- Link to first occurrence
- Escalate to gate owner
- Investigate why prevention failed

**Additional Fields**:
```json
{
  "repetition_tracking": {
    "is_repeat": true,
    "previous_occurrence_ids": ["failure-id-1"],
    "repeat_count": 2,
    "days_since_last": "integer"
  }
}
```

**Required Actions**:
- Why did same failure recur?
- What prevention measure failed?
- How to prevent third occurrence?

---

### Third Occurrence (Double Repeat)

**Action**:
- Mark as DOUBLE_REPEAT
- Escalate to Johan Ras (mandatory)
- Halt work (no further attempts)
- Require governance review

**Severity**: Upgraded to CATASTROPHIC

**Investigation Required**:
- Root cause analysis mandatory
- Prevention measure review mandatory
- Governance update may be required
- Agent contract update may be required

---

## VII. Emergency Override Protocol

### When Override Permitted

Only Johan Ras may authorize emergency override for:
- Critical production fix (blocking release)
- Critical security patch (exploit mitigation)
- Infrastructure emergency (platform down)

**Override Characteristics**:
- Temporary (single instance only)
- Explicit (written authorization required)
- Bounded (48-hour cleanup deadline)
- Logged (full audit trail)
- Tracked (cleanup issue mandatory)

---

### Override Procedure

1. **Request**: Builder requests override from Johan
2. **Justification**: Emergency nature documented
3. **Authorization**: Johan explicitly authorizes
4. **Override**: Gate manually bypassed (logged)
5. **Merge**: PR merged with RED gate (tracked)
6. **Cleanup Issue**: Created automatically
7. **Cleanup Deadline**: 48 hours mandatory
8. **Cleanup**: Fix applied, gate passes
9. **Verification**: Cleanup verified
10. **Closure**: Override closed, normal enforcement resumes

**Override Record**:
```json
{
  "override_id": "uuid",
  "pr_number": "integer",
  "gate_name": "string",
  "failure_category": "string",
  "override_reason": "PRODUCTION_FIX | SECURITY_PATCH | INFRASTRUCTURE_EMERGENCY",
  "authorized_by": "Johan Ras",
  "authorization_timestamp": "ISO-8601",
  "cleanup_deadline": "ISO-8601 (48 hours)",
  "cleanup_issue": "integer",
  "override_status": "ACTIVE | CLEANUP_COMPLETE",
  "immutable": true
}
```

---

### Override Prohibitions

Emergency override NEVER permitted for:
- ❌ AGENT_BOUNDARY_VIOLATION
- ❌ IMMUTABILITY_VIOLATION
- ❌ CATASTROPHIC_FAILURE
- ❌ Convenience (not emergency)
- ❌ Schedule pressure
- ❌ Test debt

---

## VIII. Success Criteria

Failure handling is successful when:

1. ✅ All failures classified using canonical categories
2. ✅ All failures logged with canonical schema
3. ✅ All failures block merge (no bypass)
4. ✅ All escalations follow protocol
5. ✅ All overrides by Johan only
6. ✅ All repeat failures investigated
7. ✅ Zero FM-specific failure handling
8. ✅ Zero reinterpretation of severity

---

## IX. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Mirror)  
**Canonical Source**: `maturion-foreman-governance/pr-gates/failure-handling/`  
**Last Canonical Sync**: 2025-12-22  
**Owner**: Johan Ras (Authority)  
**Maintainer**: Governance Liaison (FM-scoped)

---

## X. References

- **Canonical Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **PR Gate Requirements**: `/governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Build Failure Schema**: `/governance/events/BUILD_FAILURE_SCHEMA.md`
- **Two-Gatekeeper Model**: `/governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

**Classify canonically. Escalate appropriately. Never reinterpret.**

*END OF PR GATE FAILURE HANDLING PROTOCOL (CANONICAL MIRROR)*
