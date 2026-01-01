# Code Review Closure Artifact

## Purpose

Enforces machine-verifiable code review closure for all FM work sessions.

**Authority**: `.agent` governance.compliance.code_review_closure  
**Enforcement**: UNBREAKABLE  
**Timing**: End of session (before marking PR ready for review)

---

## Requirement

Every work session MUST end with a code review closure artifact that documents:
1. What was reviewed
2. What changed after review
3. Final verdict (APPROVED or REQUIRES_CHANGES)

**No artifact → No completion → No merge**

---

## Schema

Schema location: `governance/schemas/code-review-closure-schema.json`

### Required Fields

```json
{
  "artifact_metadata": {
    "artifact_type": "code_review_closure",
    "version": "1.0.0",
    "timestamp": "ISO 8601 timestamp",
    "session_id": "unique session identifier",
    "pr_number": null or PR number
  },
  "what_was_reviewed": {
    "files": ["list", "of", "files"],
    "components": ["list", "of", "components"],
    "summary": "Brief summary of review scope"
  },
  "review_findings": [
    {
      "category": "architecture|security|quality|performance|maintainability|governance|none",
      "description": "Finding description",
      "severity": "critical|high|medium|low|informational",
      "location": "File or component"
    }
  ],
  "what_changed_after_review": {
    "changes_made": [
      {
        "finding_reference": "Reference to finding",
        "action_taken": "What was done",
        "files_modified": ["list", "of", "files"]
      }
    ],
    "unaddressed_findings": [
      {
        "finding_reference": "Reference to finding",
        "reason": "Explicit reasoning for not addressing"
      }
    ]
  },
  "final_verdict": {
    "status": "APPROVED or REQUIRES_CHANGES",
    "reasoning": "Explicit reasoning (minimum 20 characters)",
    "reviewer": "Agent or human name"
  },
  "immutable": true
}
```

---

## Usage

### 1. Create Artifact

Create `code-review-closure.json` in repository root:

```bash
cp governance/templates/code-review-closure-template.json code-review-closure.json
```

### 2. Fill Required Fields

Edit the artifact with your review details:
- List all files reviewed
- Document any findings
- Record changes made in response to review
- Provide final verdict with explicit reasoning

### 3. Validate Locally

```bash
python scripts/validate_code_review_closure.py
```

### 4. Commit and Push

```bash
git add code-review-closure.json
git commit -m "Add code review closure artifact"
git push
```

---

## CI Validation

**Workflow**: `.github/workflows/code-review-closure-gate.yml`

### When it Runs

- On pull request (opened, synchronize, reopened, ready_for_review)
- On push to main/develop

### What it Checks

1. ✅ Artifact exists (`code-review-closure.json`)
2. ✅ Valid JSON
3. ✅ Schema compliance
4. ✅ Artifact type is `code_review_closure`
5. ✅ Marked immutable
6. ✅ At least one file reviewed
7. ✅ Final verdict present and complete

### Draft PRs

Code review closure is **not required** for draft PRs.

When you mark PR as "Ready for review", the gate activates and validates the artifact.

---

## Failure Handling

### Artifact Missing

```
❌ Code review closure artifact not found: code-review-closure.json
```

**Action**: Create the artifact using the template

### Schema Validation Failed

```
❌ Schema validation failed: 'final_verdict' is a required property
```

**Action**: Add missing required fields

### Verdict Reasoning Too Short

```
❌ Verdict reasoning too short (minimum 20 characters)
```

**Action**: Provide explicit reasoning for the verdict

---

## Rationale

### Why This Exists

Code review is mandatory but was not machine-verifiable, risking:
- Skipped reviews
- Incomplete reviews
- Undocumented review decisions
- Loss of audit trail

### Governance Authority

From `.agent`:

```yaml
code_review_closure:
  required: true
  timing: end_of_session
  enforcement: UNBREAKABLE
  output_requirements:
    - what_was_reviewed: "List of files, components, or changes reviewed"
    - what_changed_after_review: "Changes made in response to review feedback"
    - final_verdict: "APPROVED or REQUIRES_CHANGES with explicit reasoning"
```

### Unbreakable Semantics

```yaml
failure_semantics:
  on_review_skipped:
    action: STOP
    message: "INVALID: Work unit completed without code review"
    blocking: true
```

**No exceptions. No overrides. No "we'll add it later".**

---

## Templates and Examples

### Template

`governance/templates/code-review-closure-template.json`

### Minimal Valid Artifact

```json
{
  "artifact_metadata": {
    "artifact_type": "code_review_closure",
    "version": "1.0.0",
    "timestamp": "2026-01-01T17:00:00Z",
    "session_id": "session-001",
    "pr_number": null
  },
  "what_was_reviewed": {
    "files": ["scripts/example.py"],
    "components": ["Example Component"],
    "summary": "Reviewed example implementation"
  },
  "review_findings": [
    {
      "category": "none",
      "description": "No issues found",
      "severity": "informational"
    }
  ],
  "what_changed_after_review": {
    "changes_made": [],
    "unaddressed_findings": []
  },
  "final_verdict": {
    "status": "APPROVED",
    "reasoning": "Implementation is correct and follows all governance requirements",
    "reviewer": "FMRepoBuilder"
  },
  "immutable": true
}
```

---

## Integration with Build-to-Green

Code review closure is part of the Build-to-Green contract:

1. **Design** → Architecture frozen
2. **Build** → Implementation
3. **Review** → Code review closure artifact ← **YOU ARE HERE**
4. **Green** → All tests pass, all gates green

No handover without:
- All tests green ✅
- All CI gates green ✅
- Code review closure artifact ✅

---

## Issue Reference

**Issue**: #2 - Fix Residual Tier-1 Risk (Code Review Artifact)  
**Severity**: HIGH (Tier-1, Delivery Integrity)  
**Ratchet**: No review artifact → No completion

---

## Related Documentation

- `.agent` governance.compliance.code_review_closure
- `governance/schemas/code-review-closure-schema.json`
- `scripts/validate_code_review_closure.py`
- `.github/workflows/code-review-closure-gate.yml`
- `.github/BRANCH_PROTECTION.md` (required checks)
