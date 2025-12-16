# Catastrophic Failure Workflow — Quick Start Guide

**Version**: 1.0.0  
**Status**: Operational  
**Last Updated**: 2025-12-16

---

## What is a Catastrophic Failure?

Any defect observed **after successful Build-to-Green** that:
- Affects functionality
- Impacts users or systems
- Should have been caught by QA

---

## When to Use This Workflow

Use this workflow when:
- A bug is found in production/staging
- A test failure occurs in CI after merge
- A user reports an issue with released code
- Any defect escapes Build-to-Green gates

**Rule**: If it happened after B2G succeeded, it's catastrophic.

---

## Quick Start: 5 Steps

### 1. Create Issue (2 minutes)

1. Go to repository Issues
2. Click "New issue"
3. Select **"Catastrophic Failure — FL/CI"** template
4. Fill in basic info:
   - What failed (objective)
   - Where observed (screen/flow)
   - Severity (catastrophic/double/multi)
5. Submit

**Failure ID Format**: FLCI-YYYYMMDD-NNN (e.g., FLCI-20251216-001)

### 2. Create Evidence Directory (1 minute)

```bash
mkdir -p foreman/evidence/flci/FLCI-YYYYMMDD-NNN
cd foreman/evidence/flci/FLCI-YYYYMMDD-NNN
cp ../templates/*.* .
```

### 3. Document Failure (10 minutes)

Fill in templates:
- `failure-report.json` - What, where, when, why
- `root-cause-analysis.md` - Detailed RCA

### 4. Fix + Prevent (Variable time)

- Fix the bug
- Add tests (minimum 1) to prevent recurrence
- Document in `prevention-plan.json`

### 5. Validate + Close (5 minutes)

- Fill in `completion-validation.md`
- Request Foreman validation
- Close issue when approved

---

## Severity Levels

### Catastrophic (1st occurrence)
- **What**: First time this defect type occurred
- **Response**: Fix + permanent prevention
- **Approval**: Foreman validation

### Double-Catastrophic (2nd occurrence)
- **What**: Same defect type happened again
- **Response**: Fix + strengthened prevention + governance review
- **Approval**: Foreman validation + Human approval

### Multi-Catastrophic (3rd+ occurrence)
- **What**: Same defect type occurred 3+ times
- **Response**: Systemic investigation + escalation
- **Approval**: Johan approval required

---

## Root Cause Buckets

Choose ONE:

1. **Missing Architecture** - Spec/design gap
2. **Missing QA Coverage** - Test didn't exist
3. **Misaligned QA** - Test existed but wrong
4. **Implementation Bug** - Code error
5. **Governance Gap** - Process failure
6. **Integration Issue** - Module boundary violation
7. **Environmental Issue** - Config/deployment problem
8. **Unknown** - Requires investigation

---

## Evidence Files Required

### Mandatory (Always)

1. `failure-report.json` - Structured failure data
2. `root-cause-analysis.md` - Detailed RCA
3. `prevention-plan.json` - Prevention actions
4. `test-coverage-delta.json` - Coverage improvement
5. `completion-validation.md` - Final validation

### File Locations

```
foreman/evidence/flci/FLCI-YYYYMMDD-NNN/
├── failure-report.json
├── prevention-plan.json
├── test-coverage-delta.json
├── root-cause-analysis.md
└── completion-validation.md
```

---

## Permanent Prevention Requirements

Every catastrophic failure MUST have:

### Minimum Requirements

- [ ] Immediate fix implemented and validated
- [ ] Root cause fully understood
- [ ] Tests added (minimum 1)
- [ ] Prevention mechanism documented
- [ ] Prevention validated (defect cannot recur)
- [ ] Lessons propagated to similar code

**No exceptions. No deferrals.**

### Test Requirements

At least **one** of:
- Unit test
- Integration test
- E2E test
- Regression test

### Documentation Requirements

- Test purpose documented
- Coverage gap analysis done
- Prevention mechanism explained

---

## Closure Criteria (All Required)

- [ ] Immediate fix applied and validated
- [ ] Root cause fully understood and documented
- [ ] Permanent prevention implemented
- [ ] Prevention validated
- [ ] Lessons propagated
- [ ] Complete evidence trail
- [ ] Foreman validation passed
- [ ] Human approval (if double-catastrophic+)

**Cannot close issue until ALL criteria met.**

---

## Templates Location

**Directory**: `foreman/evidence/flci/templates/`

**Files**:
- `failure-report.template.json`
- `prevention-plan.template.json`
- `test-coverage-delta.template.json`
- `root-cause-analysis.template.md`
- `completion-validation.template.md`

**Usage**: Copy to evidence directory and fill in `<placeholders>`

---

## Commands

### Create Evidence Directory
```bash
# Use next available number for the day (e.g., 001, 002, 003, etc.)
mkdir -p foreman/evidence/flci/FLCI-$(date +%Y%m%d)-001
```

### Copy Templates
```bash
cp foreman/evidence/flci/templates/*.* \
   foreman/evidence/flci/FLCI-$(date +%Y%m%d)-001/
```

### Validate JSON
```bash
python3 -m json.tool failure-report.json > /dev/null
```

### Check Schema
```bash
python foreman/evidence/schema_validator.py \
  --schema foreman/evidence/flci/FLCI_EVIDENCE_SCHEMA.json \
  --evidence foreman/evidence/flci/FLCI-YYYYMMDD-NNN/failure-report.json
```

---

## Common Mistakes to Avoid

### ❌ Don't Do This

- Skip root cause analysis
- Close without adding tests
- Add tests without validation
- Ignore lesson propagation
- Close without Foreman validation
- Skip evidence files

### ✅ Do This

- Complete detailed RCA
- Add minimum 1 test
- Validate prevention works
- Propagate lessons to similar code
- Request Foreman validation
- Complete all evidence files

---

## Example Workflow

### Real Example: User Profile Save Bug

**1. Defect Observed**
- User reports: "Save button doesn't work on profile edit"
- Observed in production
- No error message shown

**2. Issue Created**
- Issue #123: "FLCI-20251216-001: Profile save silently fails"
- Severity: Catastrophic (first occurrence)
- Root cause bucket: Missing QA Coverage

**3. Evidence Created**
```bash
mkdir -p foreman/evidence/flci/FLCI-20251216-001
cp templates/*.* foreman/evidence/flci/FLCI-20251216-001/
```

**4. RCA Done**
- Root cause: Validation logic returns false for valid data
- Why escaped: No integration test for edit flow
- Contributing factor: Edge case in phone number validation

**5. Fix Applied**
- PR #124: Fix phone validation logic
- Added 3 tests:
  - Unit test for phone validator
  - Integration test for profile edit
  - E2E test for save button

**6. Prevention Validated**
- Tests pass ✅
- Cannot reproduce bug ✅
- Coverage increased 85% → 87%

**7. Lessons Propagated**
- Similar pattern in account settings
- Added tests there too
- Updated validation architecture doc

**8. Issue Closed**
- All criteria met ✅
- Foreman validated ✅
- Issue closed

**Result**: Bug fixed permanently, similar bugs prevented, process improved.

---

## Help and Documentation

**Full Documentation**: `foreman/evidence/flci/README.md`

**Schema Reference**: `foreman/evidence/flci/FLCI_EVIDENCE_SCHEMA.json`

**Implementation Details**: `FMQA-3_IMPLEMENTATION_SUMMARY.md`

**Questions**: Ask Foreman or Johan

---

## Remember

> **"A failure may occur once. Implement permanent prevention."**
> 
> — One-Time Failure Doctrine

Every catastrophic failure is an opportunity to:
- Learn what went wrong
- Strengthen our QA
- Improve our process
- Build better software

---

*This quick start guide provides the essential steps for handling catastrophic failures in the Maturion ISMS ecosystem.*
