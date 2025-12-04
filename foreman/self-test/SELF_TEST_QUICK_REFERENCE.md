# Maturion Foreman Self-Test Quick Reference

## When to Run Self-Test

Run the Foreman Self-Test in these situations:

1. **After Chat Reset** - Verify all systems after a conversation reset
2. **After Repository Clone** - Confirm repository integrity after cloning
3. **After Merge** - Validate system health after merging changes
4. **Before Major Build** - Ensure readiness before starting a build wave
5. **After Refactoring** - Verify no critical files were affected
6. **Environment Changes** - Confirm system after environment updates
7. **Periodic Health Check** - Regular validation (recommended: weekly)
8. **Before Deployment** - Final check before production deployment
9. **After Upgrade** - Validate continuity after Foreman upgrade
10. **Troubleshooting** - Diagnose system issues

## How to Run

### Basic Execution

```bash
cd /path/to/maturion-ai-foreman
python foreman/scripts/run-self-test.py
```

### With Custom Output Directory

```bash
python foreman/scripts/run-self-test.py --output-dir ./reports
```

### Verbose Mode

```bash
python foreman/scripts/run-self-test.py --verbose
```

### JSON Only (for programmatic use)

```bash
python foreman/scripts/run-self-test.py --json-only
```

## Understanding Output

### Overall Status Values

| Status | Meaning | Action Required |
|--------|---------|----------------|
| **PASS** ✅ | All critical systems healthy | None - proceed normally |
| **WARN** ⚠️ | Some warnings, but functional | Review warnings, plan improvements |
| **FAIL** ❌ | Critical systems missing/broken | Address failures before proceeding |

### Subsystem Status Values

Each of the 12 subsystems will have one of these statuses:

- **PASS** - Subsystem fully operational
- **WARN** - Subsystem functional but has issues
- **FAIL** - Subsystem has critical problems

### Exit Codes

The script returns these exit codes:

- `0` - PASS (All systems healthy)
- `1` - WARN (Some warnings present)
- `2` - FAIL (Critical failures detected)

You can use this in scripts:

```bash
python foreman/scripts/run-self-test.py
if [ $? -eq 0 ]; then
    echo "System healthy - proceeding"
else
    echo "Issues detected - check report"
fi
```

## Output Files

After running, you'll get:

1. **self-test-report.json**
   - Machine-readable JSON format
   - Complete validation results
   - Use for automation, monitoring, CI/CD

2. **self-test-report.md**
   - Human-readable Markdown format
   - Executive summary
   - Detailed subsystem results
   - Recommendations and next steps

## What Each Status Means

### PASS ✅

**Meaning:** System is fully operational
- All required files present
- All JSON schemas valid
- All builders registered
- Compliance engine ready
- Runtime system operational

**Next Steps:**
- Proceed with normal operations
- No immediate action required
- Schedule next periodic check

### WARN ⚠️

**Meaning:** System is functional but has gaps
- Some non-critical files may be missing
- Some documentation may be outdated
- Some optional features incomplete

**Next Steps:**
1. Review the warnings section
2. Prioritize which warnings to address
3. Create tasks for improvements
4. System can continue operating

### FAIL ❌

**Meaning:** Critical systems are broken
- Missing core identity/governance files
- Invalid or corrupted JSON schemas
- Builder specifications missing
- Compliance engine not initialized

**Next Steps:**
1. **STOP** - Do not proceed with builds
2. Review missing files list
3. Address critical failures first
4. Re-run self-test after fixes
5. Only proceed when status is PASS or WARN

## Reading the Report

### Section 1: Executive Summary
- Quick overview of system health
- Pass/Warn/Fail counts
- Total files checked

### Section 2: Subsystem Results
- 12 subsystems validated
- Each shows: status, files checked, issues
- Missing files clearly listed
- Recommendations provided

### Section 3: Overall Recommendations
- Prioritized action items
- System-wide improvements
- Integration suggestions

### Section 4: Identified Risks
- Organized by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Impact assessment
- Mitigation suggestions

### Section 5: Next Steps
- Immediate actions required
- Follow-up tasks
- Long-term improvements

## Common Issues and Solutions

### Issue: "Core Governance Files Missing"

**Cause:** Repository incomplete or corrupted

**Solution:**
```bash
# Re-clone the repository
git clone https://github.com/MaturionISMS/maturion-ai-foreman.git
cd maturion-ai-foreman
python foreman/scripts/run-self-test.py
```

### Issue: "Invalid JSON Schema"

**Cause:** JSON file corrupted or malformed

**Solution:**
1. Check the invalid file listed in the report
2. Validate JSON syntax using a JSON validator
3. Restore from git history if needed:
   ```bash
   git checkout HEAD -- path/to/file.json
   ```

### Issue: "Builder Not Registered"

**Cause:** Builder manifest incomplete

**Solution:**
```bash
# Re-initialize builders
python foreman/init_builders.py
# Then re-run self-test
python foreman/scripts/run-self-test.py
```

### Issue: "Architecture Index Missing"

**Cause:** Index not generated or outdated

**Solution:**
```bash
# Regenerate architecture index
python index-isms-architecture.py
# Then re-run self-test
python foreman/scripts/run-self-test.py
```

### Issue: "Compliance Engine Not Ready"

**Cause:** Compliance files not activated

**Solution:**
```bash
# Activate compliance engine
python activate-compliance-engine.py
# Then re-run self-test
python foreman/scripts/run-self-test.py
```

## Integration with Other Tools

### After Chat Reset

```
User: "Run Foreman Self-Test"
Foreman: [executes self-test]
Foreman: "Self-test complete. Status: PASS. All systems healthy."
```

### In Build Workflow

```bash
# Before starting a build
python foreman/scripts/run-self-test.py
if [ $? -ne 0 ]; then
    echo "Foreman not ready - aborting build"
    exit 1
fi

# Proceed with build
python plan-build.py
```

### In CI/CD Pipeline

```yaml
# .github/workflows/foreman-health.yml
- name: Run Foreman Self-Test
  run: python foreman/scripts/run-self-test.py
  
- name: Upload Self-Test Report
  uses: actions/upload-artifact@v3
  with:
    name: self-test-report
    path: self-test-report.*
```

## Interpreting Specific Subsystems

### Core Governance System
- **Critical** - System cannot operate without this
- Checks identity, roles, command grammar, privacy

### Architecture System
- **Critical** - Required for builds
- Validates architecture specs, indexing, standards

### Builder Agent System
- **Critical** - Needed for all builds
- Ensures all 5 builders are registered and ready

### Compliance Engine
- **High Priority** - Required for production
- Validates ISO, NIST, COBIT, OWASP coverage

### QA & QA-of-QA System
- **High Priority** - Required for quality
- Ensures QA governance and coverage

### Runtime & Continuity
- **Medium Priority** - Important for operations
- Validates runtime profiles, memory, export

### Change Management
- **Medium Priority** - Important for governance
- Checks change policies, workflows, records

### Upgrade & Continuity
- **Medium Priority** - Important for upgrades
- Validates upgrade specs, export scripts

### Test Environment
- **Medium Priority** - Important for testing
- Validates test environment specifications

### Orchestration & Build Pipeline
- **High Priority** - Required for builds
- Checks build plans, tasks, sequencing

### Platform & UI Standards
- **Low Priority** - Nice to have
- Validates platform and UI specifications

### Innovation & Admin Intelligence
- **Low Priority** - Enhancement focused
- Checks innovation and admin specs

## Best Practices

1. **Run regularly** - At least weekly, or after any major change
2. **Keep reports** - Archive reports for trend analysis
3. **Act on WARN** - Don't ignore warnings indefinitely
4. **Never build on FAIL** - Always resolve critical issues first
5. **Document fixes** - Use change management for corrections
6. **Automate checks** - Integrate into CI/CD if possible
7. **Share results** - Keep team informed of system health

## Quick Commands Cheat Sheet

```bash
# Basic self-test
python foreman/scripts/run-self-test.py

# Verbose output
python foreman/scripts/run-self-test.py --verbose

# Custom output directory
python foreman/scripts/run-self-test.py --output-dir ./my-reports

# JSON only
python foreman/scripts/run-self-test.py --json-only

# Check exit code
python foreman/scripts/run-self-test.py && echo "PASS" || echo "ISSUES"

# View JSON results
cat self-test-report.json | python -m json.tool

# View Markdown results
cat self-test-report.md
```

## Getting Help

If self-test fails unexpectedly:

1. Check the detailed report for specific errors
2. Review recent commits that may have caused issues
3. Consult `foreman/self-test/self-test-spec.md` for requirements
4. Restore missing files from git history
5. Contact Foreman administrator if persistent issues

## Related Documentation

- `foreman/self-test/self-test-spec.md` - Full specification
- `foreman/self-test/self-test-schema.json` - JSON schema
- `foreman/identity.md` - Foreman identity and purpose
- `foreman/roles-and-duties.md` - Foreman responsibilities
- `foreman/command-grammar.md` - Command structure
- `foreman/reports/SELF_TEST_IMPLEMENTATION_REPORT.md` - Implementation details

---

**Remember:** Self-test is your health check. Run it often, act on results, and keep Foreman ready!
