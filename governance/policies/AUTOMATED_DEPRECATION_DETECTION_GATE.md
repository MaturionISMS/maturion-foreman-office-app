# Automated Deprecation Detection Gate (BL-026)

**Authority**: Bootstrap Learning BL-026, Zero Warning Test Debt Constitutional Rule  
**Version**: 1.0.0  
**Date**: 2026-01-11  
**Status**: ACTIVE  
**Scope**: All Python code in maturion-foreman-office-app repository

---

## Constitutional Authority

This gate is a **Tier-1 Constitutional requirement** enforced by:

1. **BL-026 Bootstrap Learning**: Automated deprecation detection prevents future runtime failures
2. **Zero Warning Test Debt Constitutional Rule**: Warnings about deprecated APIs constitute test debt
3. **One-Time Build Correctness**: Code must be forward-compatible with supported Python versions

**This gate CANNOT be waived. Exceptions require FM approval and quarterly review.**

---

## Purpose & Rationale

Deprecated Python APIs represent **latent technical debt** that will cause:
- **Runtime failures** when deprecated APIs are removed
- **Security vulnerabilities** when deprecated patterns have known issues
- **Maintenance burden** when upgrading Python versions
- **Build fragility** as warnings escalate to errors

**Prevention is mandatory**. Deprecated code must not enter the repository.

---

## Scope

### APIs Detected

This gate enforces modern Python 3.12+ patterns and detects:

#### 1. Deprecated datetime Module (HIGH PRIORITY)
```python
# BLOCKED ❌
datetime.utcnow()
datetime.utcfromtimestamp(timestamp)

# REQUIRED ✅
from datetime import timezone
datetime.now(timezone.utc)
datetime.fromtimestamp(timestamp, tz=timezone.utc)
```

**Rationale**: `datetime.utcnow()` deprecated in Python 3.12, removal planned.

#### 2. Deprecated typing Module (MEDIUM PRIORITY)
```python
# BLOCKED ❌
from typing import Dict, List, Tuple, Set, Optional

# REQUIRED ✅  (Python 3.9+)
# Use built-in types directly
def func(data: dict[str, list[int]]) -> tuple | None:
    pass

# For Callable, use collections.abc
from collections.abc import Callable
```

**Rationale**: PEP 585 (Python 3.9+) and PEP 604 (Python 3.10+) obsolete typing generics.

#### 3. Other Pyupgrade Rules
All `UP` rules from `ruff` are enabled, including:
- Unnecessary string formatting
- Deprecated unittest aliases
- Outdated syntax patterns
- Unnecessary file mode arguments

---

## Enforcement

### Pre-Commit Hook

**Location**: `.githooks/pre-commit-deprecation`

**Behavior**:
- Runs `ruff check --select UP` on all staged Python files
- **BLOCKS** commit if violations found
- Provides remediation guidance
- Suggests `ruff --fix` for auto-fixable issues

**Installation** (automatic via main pre-commit):
```bash
cp .githooks/pre-commit-deprecation .git/hooks/
chmod +x .git/hooks/pre-commit-deprecation
```

### CI/CD Gate

**Workflow**: `.github/workflows/deprecation-detection-gate.yml`

**Behavior**:
- Runs on all PRs and pushes to main/develop
- Scans all changed Python files
- **BLOCKS** merge if violations detected
- Comments on PR with violation details
- Provides auto-fix suggestions

**Gate Classification**: Hard Gate (blocks merge)

---

## Auto-Fix Capability

Many violations can be auto-fixed:

```bash
# Fix single file
ruff check --select UP --fix <file.py>

# Fix all Python files
ruff check --select UP --fix .

# Preview fixes without applying
ruff check --select UP --diff .
```

**After auto-fix**:
1. Review all changes for correctness
2. Run full test suite
3. Commit fixed code

---

## Exception Process

### When Exceptions Are Justified

Exceptions are **rare** and only justified when:

1. **Third-party library compatibility**: External library requires deprecated API
2. **Python version compatibility**: Supporting Python <3.9 for specific reason
3. **Performance-critical code**: Modern API has measurable performance regression
4. **Temporary compatibility**: During migration period with documented end date

### Exception Request Process

1. **Document Justification**
   - Create issue with `deprecation-exception` label
   - Explain why exception is needed
   - Provide evidence (compatibility requirements, benchmarks, etc.)
   - Propose end date for exception

2. **FM Review & Approval**
   - FM reviews technical merit
   - FM approves or rejects with rationale
   - Approval logged in `governance/evidence/deprecation-exceptions.json`

3. **Code Annotation**
   ```python
   # DEPRECATION EXCEPTION: BL-026-EX-001
   # Justification: Required for library X compatibility
   # Approved by: FM (2026-01-15)
   # Review date: 2026-04-15
   # See: governance/evidence/deprecation-exceptions.json
   datetime.utcnow()  # noqa: UP017
   ```

4. **Quarterly Review**
   - All exceptions reviewed every quarter
   - Expired exceptions must be remediated or renewed
   - Renewal requires updated justification

---

## Remediation Guidance

### For datetime Deprecations

```python
# Step 1: Add import
from datetime import timezone

# Step 2: Replace utcnow()
# OLD
timestamp = datetime.utcnow()
# NEW
timestamp = datetime.now(timezone.utc)

# Step 3: Replace utcfromtimestamp()
# OLD
dt = datetime.utcfromtimestamp(unix_time)
# NEW
dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
```

### For typing Deprecations

```python
# Step 1: Remove typing imports (Python 3.9+)
# OLD
from typing import Dict, List, Optional, Tuple
# NEW
# (no import needed for built-in types)

# Step 2: Update type hints
# OLD
def process(data: Dict[str, List[int]]) -> Optional[Tuple[str, int]]:
# NEW
def process(data: dict[str, list[int]]) -> tuple[str, int] | None:

# Step 3: For Callable, use collections.abc
# OLD
from typing import Callable
# NEW
from collections.abc import Callable
```

---

## Integration with Build Process

### Wave 0: QA to RED
- Gate is **informational** during RED phase
- Violations logged but do not block

### Wave 1+: Build to GREEN
- Gate is **enforcing** starting Wave 1
- All violations must be fixed before merge
- No exceptions without FM approval

### Pre-Wave 3 Mandate
- All existing violations must be remediated
- See `governance/evidence/BL_026_DEPRECATION_AUDIT_REPORT.md`
- Remediation plan due: 2 weeks before Wave 3

---

## Monitoring & Metrics

### Dashboard (Future)
Track deprecation health:
- Violation count over time
- Auto-fix vs manual fix ratio
- Exception count and expiration dates
- Python version upgrade readiness

### Quarterly Review
Every quarter, review:
- All active exceptions
- New deprecations in Python roadmap
- Gate configuration updates
- Remediation backlog

---

## References

### Canonical Governance
- **Source**: `maturion-foreman-governance/governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md`
- **Bootstrap Learning**: BL-026 in BOOTSTRAP_EXECUTION_LEARNINGS.md
- **Zero Warning Rule**: `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`

### Technical References
- **Ruff Documentation**: https://docs.astral.sh/ruff/rules/#pyupgrade-up
- **PEP 585** (Type Hinting Generics): https://peps.python.org/pep-0585/
- **PEP 604** (Union Operator): https://peps.python.org/pep-0604/
- **Python datetime deprecations**: https://docs.python.org/3/library/datetime.html

### Repository Files
- Pre-commit hook: `.githooks/pre-commit-deprecation`
- CI workflow: `.github/workflows/deprecation-detection-gate.yml`
- Ruff config: `ruff.toml`
- Audit report: `governance/evidence/BL_026_DEPRECATION_AUDIT_REPORT.md`

---

## Revision History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0.0 | 2026-01-11 | Initial policy creation | Governance Liaison |

---

**Status**: ACTIVE  
**Next Review**: 2026-04-11 (Quarterly)  
**Contact**: FM for exceptions, Johan for constitutional matters
