# Test Suite Documentation

## Overview

This repository contains a multi-phase test suite designed to support Build-to-Green methodology and governance enforcement.

## Test Organization

### Wave 0: Minimum RED QA Suite (`tests/wave0_minimum_red/`)

Wave 0 tests are **expected to FAIL** (RED) by design. These tests define the required functionality and governance rules that must be implemented.

**Purpose:**
- Define the complete governance and QA specification
- Serve as acceptance criteria for implementations
- Enable Build-to-Green workflow (RED → GREEN)

**Test Categories:**
- `@pytest.mark.liveness` - Liveness and continuity (heartbeat, stall detection, recovery)
- `@pytest.mark.governance` - Governance supremacy (architecture freeze, QA bypass prevention)
- `@pytest.mark.determinism` - Decision determinism (reproducible outcomes)
- `@pytest.mark.evidence` - Evidence integrity (generation, schema, traceability)
- `@pytest.mark.integration` - Integration sanity (task lifecycle, failure states)

**Expected Status:** RED until implementations exist

### Future Waves

Additional test waves will be added as implementations progress:
- Wave 1: Core functionality tests (GREEN when implemented)
- Wave 2: Integration tests (GREEN when integrated)
- Wave 3: End-to-end tests (GREEN when complete)

## Running Tests

### Default (CI/PR Merge Gate)
```bash
npm test
# Runs all tests EXCEPT wave0 (only tests that should be GREEN)
```

### All Tests (Including Wave 0 RED Tests)
```bash
npm run test:all
# Runs ALL tests including wave0 (will show RED failures)
```

### Wave 0 Tests Only
```bash
npm run test:wave0
# Runs only wave0 minimum RED tests
```

### Specific Test Markers
```bash
# Run only liveness tests
pytest tests/ -v -m liveness

# Run only governance tests
pytest tests/ -v -m governance

# Run only evidence tests
pytest tests/ -v -m evidence
```

## CI/CD Behavior

### PR Merge Gate
- Runs: `npm test` (excludes wave0)
- Expectation: 100% pass for all non-wave0 tests
- Wave 0 tests are excluded because they are expected to be RED

### Build-to-Green Workflow
1. Wave 0 tests define requirements (RED)
2. Implementation work begins
3. Tests turn GREEN one by one
4. When all tests GREEN → Build-to-Green complete

## Test Development Guidelines

### Adding New Tests

**For New Requirements (Pre-Implementation):**
- Add to `tests/wave0_minimum_red/`
- Mark with `@pytest.mark.wave0`
- Tests should FAIL until implementation exists

**For Implemented Features:**
- Add to appropriate test directory (wave1/, wave2/, etc.)
- Tests should PASS immediately
- Include in default test suite

### Test Markers

Always use appropriate pytest markers:

```python
@pytest.mark.wave0        # Wave 0 minimum RED tests
@pytest.mark.liveness     # Liveness/continuity tests
@pytest.mark.governance   # Governance enforcement tests
@pytest.mark.determinism  # Decision determinism tests
@pytest.mark.evidence     # Evidence integrity tests
@pytest.mark.integration  # Integration sanity tests
```

## Governance Integration

### Zero Test Debt Rule

Test dodging is forbidden:
- No `.skip()`, `.only()`, `.todo()`
- No `|| true` or error suppression
- Use governed QA parking or DP-RED instead

See: `foreman/governance/zero-test-debt-constitutional-rule.md`

### Catastrophic Failure Workflow

Any test failure after Build-to-Green is treated as catastrophic:
- Requires permanent prevention
- Requires root cause analysis
- Requires structured evidence

See: `CATASTROPHIC_FAILURE_QUICK_START.md`

## Architecture

Tests follow the same architecture as the main codebase:
- Evidence-based validation
- Governance-first approach
- Immutable audit trails
- Constitutional compliance

---

**Status:** Active  
**Last Updated:** 2025-12-16  
**Owner:** Maturion Foreman
