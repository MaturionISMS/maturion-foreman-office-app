# Deprecation Exception Template (BL-026)

**Use this template to request an exception to the Automated Deprecation Detection Gate**

---

## Exception Request ID

`BL-026-EX-[NUMBER]` (FM will assign number upon approval)

---

## Requestor Information

- **Name**: [Your Name]
- **Role**: [Builder/FM/Other]
- **Date**: [YYYY-MM-DD]
- **Issue/PR**: [Link to issue or PR where exception is needed]

---

## Deprecated API Information

**Deprecated API/Pattern**:
```python
# Example: datetime.utcnow()
[Insert code that requires exception]
```

**File(s) Affected**:
- `path/to/file1.py` (line numbers)
- `path/to/file2.py` (line numbers)

**Ruff Rule**: `UP### - [Rule Description]`

---

## Justification

### Why is this exception necessary?

[Provide detailed justification - must fit one of these categories:]

1. **Third-party library compatibility**: External library requires deprecated API
   - Library name and version:
   - Evidence of compatibility requirement:
   - Issue/documentation link:

2. **Python version compatibility**: Supporting Python <3.9 for specific reason
   - Python version requirement:
   - Reason for supporting older version:
   - Migration timeline:

3. **Performance-critical code**: Modern API has measurable performance regression
   - Performance benchmarks (before/after):
   - Impact analysis:
   - Justification for performance priority:

4. **Temporary compatibility**: During migration period
   - Migration plan:
   - End date for exception:
   - Progress tracking:

### Have you explored alternatives?

[Document what alternatives were considered and why they don't work]

---

## Impact Analysis

**Code Footprint**: [How many lines/files affected]

**Risk Assessment**: [What breaks if this deprecated API is removed from Python]

**Migration Complexity**: [Estimated effort to remediate when ready]

---

## Proposed Exception Period

**Start Date**: [YYYY-MM-DD]

**End Date**: [YYYY-MM-DD] (Maximum 6 months, renewable)

**Review Date**: [Quarterly review date]

**Renewal Conditions**: [What needs to happen for renewal]

---

## Code Annotation

Once approved, annotate code as follows:

```python
# DEPRECATION EXCEPTION: BL-026-EX-[NUMBER]
# Justification: [One-line summary]
# Approved by: FM ([Approval Date])
# Review date: [Next Review Date]
# See: governance/evidence/deprecation-exceptions.json
[deprecated code here]  # noqa: UP###
```

---

## FM Review Section

**Status**: [ ] APPROVED / [ ] REJECTED / [ ] NEEDS MORE INFO

**FM Decision**: [Approval or rejection rationale]

**Approved By**: [FM Name]

**Approval Date**: [YYYY-MM-DD]

**Exception ID Assigned**: `BL-026-EX-[NUMBER]`

**Review Schedule**: Quarterly on [Month]

**Conditions**:
- [Any specific conditions for this exception]

---

## Quarterly Review Log

| Review Date | Status | Notes | Renewed? |
|-------------|--------|-------|----------|
| YYYY-MM-DD  | Active | Initial approval | N/A |
| YYYY-MM-DD  |        |       |          |
| YYYY-MM-DD  |        |       |          |

---

## Exception Closure

**Closed Date**: [YYYY-MM-DD]

**Closure Reason**: 
- [ ] Remediated (deprecated API replaced)
- [ ] No longer needed
- [ ] Library updated
- [ ] Python version no longer supported
- [ ] Expired without renewal

**Evidence**: [Link to PR that removed deprecated API]

---

## References

- **Policy**: `governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md`
- **Exception Registry**: `governance/evidence/deprecation-exceptions.json`
- **Canonical Source**: `maturion-foreman-governance/governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md`
