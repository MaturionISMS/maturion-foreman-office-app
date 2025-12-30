# DP-RED (Design-Phase RED) System - Quick Reference

**For Developers, QA Engineers, and Foreman**

---

## TL;DR - What You Need to Know

**DP-RED allows intentionally RED (failing) tests during design phase, without blocking merges.**

- ✅ Valid during **QA_DESIGN phase only**
- ✅ All RED tests **must be registered** in registry
- ✅ Merge allowed if all RED tests registered
- ❌ **Hard block** if registry not empty in build phase
- ❌ **No test debt** allowed (ever)

---

## Quick Commands

### Check DP-RED Status

```bash
# Human-readable report
python foreman/scripts/validate-dp-red-compliance.py

# JSON report
python foreman/scripts/validate-dp-red-compliance.py --json

# Check current phase
cat foreman/qa/current-phase.json

# View registry
cat foreman/qa/dp-red-registry.json
```

### Register a RED Test

1. Add entry to `foreman/qa/dp-red-registry.json`:

```json
{
  "schema_version": "1.0.0",
  "phase": "QA_DESIGN",
  "entries": [
    {
      "test_id": "foreman.liveness.test_heartbeat_generation",
      "test_path": "tests/wave0_minimum_red/test_liveness.py::test_heartbeat_generation",
      "phase": "QA_DESIGN",
      "intent": "INTENTIONAL_RED",
      "reason": "Implementation module foreman.runtime.liveness does not exist yet. Test validates architecture contract before build.",
      "registered_by": "Foreman",
      "registered_date": "2025-12-16T08:00:00Z",
      "module": "foreman",
      "category": "liveness",
      "architecture_ref": "foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#liveness-system",
      "build_blocker": true,
      "future_build_task": "B2G-FM-001: Implement Foreman Liveness System"
    }
  ]
}
```

2. Validate:
```bash
python foreman/scripts/validate-dp-red-compliance.py
```

3. Commit and push:
```bash
git add foreman/qa/dp-red-registry.json
git commit -m "Register test_heartbeat_generation as DP-RED"
git push
```

### Clear a DP-RED Entry

When test is implemented and GREEN:

1. Remove entry from registry
2. Validate:
```bash
python foreman/scripts/validate-dp-red-compliance.py
```
3. Commit:
```bash
git add foreman/qa/dp-red-registry.json
git commit -m "Clear DP-RED for test_heartbeat_generation - now GREEN"
git push
```

### Transition to Build Phase

```bash
# 1. Ensure all tests are GREEN
python -m pytest tests/

# 2. Clear registry
cat > foreman/qa/dp-red-registry.json << 'EOF'
{
  "schema_version": "1.0.0",
  "phase": "QA_BUILD",
  "entries": []
}
EOF

# 3. Update phase
cat > foreman/qa/current-phase.json << 'EOF'
{
  "phase": "QA_BUILD",
  "updated_at": "2025-12-16T12:00:00Z",
  "updated_by": "Foreman"
}
EOF

# 4. Validate
python foreman/scripts/validate-dp-red-compliance.py

# 5. Commit
git add foreman/qa/dp-red-registry.json foreman/qa/current-phase.json
git commit -m "Transition to QA_BUILD - all tests GREEN"
git push
```

---

## What is DP-RED?

**Design-Phase RED (DP-RED)**: Tests that are intentionally failing because the implementation doesn't exist yet, written during the design phase as architectural validation.

### Test Intent Classification (Mandatory)

**Every RED test MUST be classified as either:**

1. **INTENTIONAL_RED**
   - RED because implementation does not yet exist
   - Validates frozen architecture before build
   - Must be traceable to architecture component
   - Must be mapped to future Build-to-Green task
   - Valid input to Phase 3 (Build-to-Green)

2. **UNINTENTIONAL_RED**
   - RED due to defect, misconfiguration, or error
   - Must be fixed immediately
   - Cannot be used for design validation
   - Maximum age: 7 days before blocking

**RED status alone does NOT indicate failure.** The intent classification determines treatment.

### Orphaned Tests (PROHIBITED)

A test is **ORPHANED** (governance violation) if:
- ❌ No declared intent
- ❌ Cannot trace to architecture
- ❌ Missing implementation not identified
- ❌ RED due to ambiguity

**Orphaned tests block all progression.**

### Example: Wave 0 Minimum RED

You have 58 tests for a new module that don't pass yet because the module isn't built:

```python
def test_heartbeat_generation():
    """Test that heartbeat is generated every second."""
    monitor = HeartbeatMonitor()  # Module doesn't exist yet!
    monitor.start()
    time.sleep(2)
    assert monitor.heartbeat_count >= 2
```

**Without DP-RED**: This RED test blocks merge → can't progress

**With DP-RED**: Register the test → merge allowed → build when ready

---

## DP-RED vs Test Debt

| Aspect | DP-RED | Test Debt |
|--------|--------|-----------|
| **Purpose** | Architecture validation before build | Shortcuts or incomplete work |
| **Status** | Registered and tracked | Hidden or informal |
| **Phase** | QA_DESIGN only | Never allowed |
| **Exit** | Implement feature | Fix immediately |
| **Merge** | Allowed (if registered) | BLOCKED |

**Test debt is NEVER allowed. DP-RED is controlled RED during design.**

---

## Phase Rules

### QA_DESIGN (Current Phase)

✅ **DP-RED ALLOWED**

- Register RED tests in registry
- Merge allowed if all RED registered
- Test debt still forbidden
- Unregistered RED → BLOCKED

### QA_BUILD

🔒 **DP-RED BLOCKED**

- Registry MUST be empty
- Any DP-RED entries → HARD BLOCK
- All tests must be GREEN
- Cannot transition from DESIGN with RED

### QA_GREEN / QA_VALIDATE

🔒 **DP-RED BLOCKED**

- Registry must stay empty
- 100% pass required
- No exceptions

---

## CI/CD Workflow

DP-RED validation runs automatically on every commit:

```
1. enforce-zero-test-debt
       ↓
2. validate-dp-red-compliance  ← NEW
       ↓
3. enforce-100-percent-pass
       ↓
4. enforce-no-suppressed-failures
       ↓
5. enforce-constitutional-compliance
```

### What CI Checks

1. ✅ Registry schema is valid
2. ✅ Phase matches current phase
3. ✅ All required fields present
4. ✅ All RED tests registered
5. ✅ No unregistered RED tests
6. ✅ Registry empty in build phase

### CI Artifacts

- `dp-red-compliance-report.json` - Validation report
- `enforcement-summary.md` - Overall enforcement status

---

## Common Scenarios

### Scenario 1: Starting Design Phase

**Situation**: Writing tests for new module before building

**Steps**:
1. Write tests (they'll be RED - that's OK!)
2. Register each RED test in dp-red-registry.json
3. Validate: `python foreman/scripts/validate-dp-red-compliance.py`
4. Commit and push → CI passes, merge allowed

### Scenario 2: During Design Phase

**Situation**: Implementing one module, tests start passing

**Steps**:
1. Implement feature
2. Test goes from RED → GREEN
3. Remove entry from dp-red-registry.json
4. Commit and push

### Scenario 3: Ready to Build

**Situation**: All tests GREEN, ready to transition

**Steps**:
1. Verify: `python -m pytest tests/` → all GREEN
2. Clear registry: `entries: []`
3. Update phase to QA_BUILD
4. Validate and commit

### Scenario 4: Merge Blocked

**Error**: "Unregistered RED tests found"

**Fix**:
1. Run: `python foreman/scripts/validate-dp-red-compliance.py`
2. See which tests are RED but not registered
3. Either:
   - Register as DP-RED (if design-phase validation)
   - Fix the test (if actual failure)

---

## Error Messages and Fixes

### "DP-RED entries exist but phase is QA_BUILD"

**Cause**: Trying to build with RED tests still registered

**Fix**: Implement all features, make tests GREEN, clear registry

### "Unregistered RED tests found"

**Cause**: Tests failing but not in registry

**Fix**: Register as DP-RED or fix the failure

### "Registry phase does not match current phase"

**Cause**: Registry says QA_DESIGN, phase file says QA_BUILD

**Fix**: Update registry phase to match

### "Entry #1: Missing field 'reason'"

**Cause**: Invalid registry entry

**Fix**: Add all required fields to entry

---

## Abuse Prevention

DP-RED **mechanically prevents abuse**:

1. ❌ Can't fake phase (version-controlled phase file)
2. ❌ Can't hide failures (validation maps to actual tests)
3. ❌ Can't skip registration (unregistered RED blocked)
4. ❌ Can't carry into build (registry must be empty)
5. ❌ Can't use for test debt (debt detection still runs)

**You literally cannot cheat the system.**

---

## Dashboard

### DP-RED Status Panel

```
┌─────────────────────────────────────────┐
│ DP-RED Status                           │
├─────────────────────────────────────────┤
│ Current Phase: QA_DESIGN                │
│ Registered: 58 tests                    │
│ Expiring Soon: 0                        │
│ Invalid Entries: 0                      │
│                                         │
│ Status: ✅ All RED tests registered     │
└─────────────────────────────────────────┘
```

### Test Results with DP-RED

```
Test Results:
  Total: 58
  Passing: 0
  Failing: 58
    ├─ DP-RED (Registered): 58 ✅
    └─ Actual Failures: 0 ❌
  
Phase Status: ✅ GREEN for QA_DESIGN
Overall: ✅ Ready for merge
```

---

## Documentation

**Full Specifications**:
- `foreman/qa/dp-red-registry-spec.md` - Complete registry specification (14KB)
- `foreman/governance/dp-red-policy.md` - Full policy document (12KB)
- `foreman/platform/qa-dashboard-spec.md` - Dashboard integration

**Implementation**:
- `foreman/scripts/validate-dp-red-compliance.py` - Validation script
- `foreman/qa/dp-red-registry.json` - Registry file
- `foreman/qa/current-phase.json` - Phase tracking
- `.github/workflows/build-to-green-enforcement.yml` - CI integration

---

## FAQ

### Q: Can I skip tests instead of using DP-RED?

**A: NO.** Skipped tests are test debt and always blocked.

### Q: Can I use DP-RED in build phase?

**A: NO.** DP-RED only in QA_DESIGN. Build phase = all tests GREEN.

### Q: What if I need to defer work past design phase?

**A: Use Enhancement Parking Lot**, not DP-RED. Remove test or make it pass, then add to parking lot.

### Q: Does DP-RED weaken QA standards?

**A: NO.** DP-RED is a controlled exception for design phase only. Build phase still requires 100% GREEN.

### Q: Can I register a failing test that's broken?

**A: NO.** DP-RED is for intentional validation before implementation, not bugs.

---

## Support

**Issues or Questions**:
- Check documentation above
- Review violation reports from validation script
- Contact repository maintainers
- Escalate to Foreman if unclear

**DO NOT**:
- Bypass enforcement
- Hide RED tests
- Use DP-RED for test debt
- Fake phase or registry

---

## Constitutional Authority

DP-RED is authorized by and extends:
- BUILD_PHILOSOPHY.md Phase 2: RED QA
- Governance Supremacy Rule
- Zero Test Debt Constitutional Rule
- Build-to-Green Enforcement

**DP-RED does not weaken these rules. It provides controlled flexibility for design phase.**

---

**Last Updated**: 2025-12-16  
**Version**: 1.0.0  
**Status**: Active and Enforced

---

*Intentional RED is not test debt. It's architectural validation.*
