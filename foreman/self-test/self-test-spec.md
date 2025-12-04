# Maturion Foreman Self-Test Specification

## 1. Purpose

This specification defines the complete self-test system that allows Maturion Foreman to verify:

- Initialization status
- Governance system health
- Architecture completeness
- Orchestration readiness
- Builder agent readiness
- Compliance engine readiness
- QA & QA-of-QA readiness
- Runtime maturity integration
- Upgrade & continuity conditions
- Change-management state
- Test-environment readiness

The self-test must be runnable at any time, especially after:
- Chat resets
- Refactors
- Merges
- Environment changes

## 2. Subsystems to Validate

### 2.1 Core Governance System

**Required Files:**
- `foreman/identity.md`
- `foreman/roles-and-duties.md`
- `foreman/command-grammar.md`
- `foreman/privacy-guardrails.md`
- `foreman/memory-model.md`
- `foreman/system-map.md`
- `foreman/context-awareness.md`
- `foreman/platform-awareness.md`

**Validation Criteria:**
- All files must exist
- All files must be readable
- Files must not be empty (> 100 bytes)
- Must contain core identity markers (e.g., "Maturion Foreman")

**Pass/Fail:**
- PASS: All required files present and valid
- WARN: Files present but some may be outdated or incomplete
- FAIL: Any required file missing or unreadable

### 2.2 Architecture System

**Required Files:**
- `foreman/minimum-architecture-template.md`
- `foreman/architecture-validation-checklist.md`
- `foreman/architecture-naming-conventions.md`
- `foreman/architecture-folder-structure.md`
- `foreman/architecture-governance.md`
- `foreman/architecture-standardisation-policy.md`
- `foreman/versioning-rules.md`
- `ARCHITECTURE_INDEX.json` (root)

**Validation Criteria:**
- All specification files must exist
- ARCHITECTURE_INDEX.json must be valid JSON
- Index must contain module entries
- Index must have health scores

**Pass/Fail:**
- PASS: All files present, JSON valid, index contains data
- WARN: Index may be outdated
- FAIL: Missing critical files or invalid JSON

### 2.3 Builder Agent System

**Required Files:**
- `foreman/builder/ui-builder-spec.md`
- `foreman/builder/api-builder-spec.md`
- `foreman/builder/schema-builder-spec.md`
- `foreman/builder/integration-builder-spec.md`
- `foreman/builder/qa-builder-spec.md`
- `foreman/builder/builder-collaboration-rules.md`
- `foreman/builder/builder-capability-map.json`
- `foreman/builder/builder-permission-policy.json`
- `foreman/builder-manifest.json`
- `foreman/builder-task-map.json`

**Validation Criteria:**
- All specification files must exist
- JSON files must be valid
- builder-capability-map.json must contain all 5 builders
- builder-permission-policy.json must define permissions

**Pass/Fail:**
- PASS: All files present, all 5 builders registered
- WARN: Files present but may be incomplete
- FAIL: Missing builder specs or invalid JSON

### 2.4 Compliance Engine

**Required Files:**
- `foreman/compliance/compliance-reference-map.md`
- `foreman/compliance/compliance-control-library.json`
- `foreman/compliance/compliance-qa-spec.md`
- `foreman/compliance/compliance-watchdog-spec.md`
- `foreman/compliance/compliance-dashboard-spec.md`

**Validation Criteria:**
- All files must exist
- compliance-control-library.json must be valid JSON
- Must contain ISO, NIST, COBIT, OWASP standards

**Pass/Fail:**
- PASS: All files present, standards mapped
- WARN: Some standards may be incomplete
- FAIL: Missing compliance files or invalid JSON

### 2.5 QA & QA-of-QA System

**Required Files:**
- `foreman/qa-governance.md`
- `foreman/qa-minimum-coverage-requirements.md`
- `foreman/qa-of-qa.md`
- `foreman/qa-of-qa-validation-checklist.md`
- `foreman/platform/qa-dashboard-spec.md`
- `foreman/platform/governance-qa-dashboard-spec.md`

**Validation Criteria:**
- All files must exist
- QA governance rules must be defined
- Minimum coverage requirements must be specified

**Pass/Fail:**
- PASS: All QA specs present and complete
- WARN: Specs present but may need updates
- FAIL: Missing critical QA specifications

### 2.6 Runtime & Continuity System

**Required Files:**
- `foreman/runtime-agent-plan.md`
- `foreman/runtime-maturion-profile.md`
- `foreman/runtime-memory-ingestion.md`
- `foreman/runtime/runtime-state-spec.md`
- `foreman/runtime/runtime-risk-model-spec.md`
- `foreman/runtime/runtime-transition-plan.md`
- `foreman/runtime/system-health-checks-spec.md`
- `foreman/runtime/memory-spine.json`
- `foreman/runtime/environment-map.json`
- `foreman/ai-memory/knowledge-base-schema.json`
- `foreman/ai-memory/historical-issues-schema.json`
- `foreman/ai-memory/reasoning-patterns-schema.json`

**Validation Criteria:**
- All specification files must exist
- JSON schemas must be valid
- Memory spine must define key storage areas
- Environment map must contain prod/test/dev environments

**Pass/Fail:**
- PASS: All runtime specs present, schemas valid
- WARN: Some schemas may be outdated
- FAIL: Missing critical runtime files

### 2.7 Change Management System

**Required Files:**
- `foreman/change-management/change-policy.md`
- `foreman/change-management/change-process.md`
- `foreman/change-management/change-approval-workflow.md`
- `foreman/change-management/change-log-schema.json`
- `foreman/change-management/change-impact-analysis-template.md`
- `foreman/change-management/change-risk-assessment-template.md`
- `foreman/change-management/change-rollback-plan-template.md`
- `foreman/change-management/change-test-plan-template.md`
- `foreman/change-management-spec.md`

**Validation Criteria:**
- All policy and process files must exist
- change-log-schema.json must be valid JSON
- Templates must be present
- Change records (CR-*.json) may exist

**Pass/Fail:**
- PASS: All change management files present
- WARN: Some templates may need updates
- FAIL: Missing critical change management specs

### 2.8 Upgrade & Continuity System

**Required Files:**
- `foreman/upgrade/upgrade-cycle.md`
- `foreman/upgrade/foreman-import-spec.md`
- `foreman/upgrade/runtime-export-spec.md`
- `foreman/upgrade/upgrade-insights-schema.json`
- `export-runtime-context.py` (root)

**Validation Criteria:**
- All upgrade specification files must exist
- upgrade-insights-schema.json must be valid JSON
- Export script must be executable

**Pass/Fail:**
- PASS: All upgrade files present, export script exists
- WARN: Export script may not have been tested recently
- FAIL: Missing upgrade specifications

### 2.9 Test Environment System

**Required Files:**
- `foreman/test-environment/test-env-architecture.md`
- `foreman/test-environment/test-env-deployment-plan.md`
- `foreman/test-environment/test-env-data-policy.md`
- `foreman/test-environment/prod-to-test-switch-protocol.md`

**Validation Criteria:**
- All test environment specs must exist
- Deployment plan must be defined
- Data policy must enforce privacy

**Pass/Fail:**
- PASS: All test environment specs present
- WARN: Specs present but may need updates
- FAIL: Missing test environment specifications

### 2.10 Orchestration & Build Pipeline

**Required Files:**
- `build-plan.json` (root)
- `build-tasks.json` (root)
- `build-status.json` (root)
- `foreman/task-distribution-rules.md`
- `BUILDER_SEQUENCING_PLAN.md` (root)
- `BUILD_ORCHESTRATION_READINESS.md` (root)

**Validation Criteria:**
- Build pipeline files must exist
- JSON files must be valid
- Task distribution rules must be defined

**Pass/Fail:**
- PASS: All orchestration files present and valid
- WARN: Build status may be outdated
- FAIL: Missing critical orchestration files

### 2.11 Platform & UI Standards

**Required Files:**
- `foreman/platform/watchdog-standard-spec.md`
- `foreman/platform/ui-navigation-spec.md`
- `foreman/platform/ui-branding-standard.md`
- `foreman/platform/ui-theme-overrides.md`
- `foreman/platform/ai-usage-analytics-spec.md`
- `foreman/platform/ai-cost-optimization-policy.md`

**Validation Criteria:**
- Platform standards must exist
- UI standards must be defined

**Pass/Fail:**
- PASS: All platform standards present
- WARN: Standards may need updates
- FAIL: Missing critical platform specs

### 2.12 Innovation & Admin Intelligence

**Required Files:**
- `foreman/admin/admin-innovation-chat-spec.md`
- `foreman/admin/ai-self-improvement-spec.md`
- `foreman/admin/enhancement-parking-lot-spec.md`
- `foreman/innovation/` (directory)
- `foreman/survey/` (directory)

**Validation Criteria:**
- Admin specs must exist
- Innovation and survey directories must exist

**Pass/Fail:**
- PASS: All admin and innovation specs present
- WARN: Specs may need expansion
- FAIL: Missing critical admin specifications

## 3. Severity Levels

### Critical (FAIL)
- Missing core identity files
- Missing governance specifications
- Invalid or corrupted JSON schemas
- Missing builder specifications
- Missing compliance engine files

### Warning (WARN)
- Outdated documentation
- Incomplete coverage in some areas
- Missing optional specifications
- Outdated build status files

### Informational (INFO)
- Recommendations for improvements
- Optional enhancements
- Documentation updates suggested

## 4. Output Format

### 4.1 JSON Output (`self-test-report.json`)

```json
{
  "test_timestamp": "ISO 8601 timestamp",
  "foreman_version": "1.0.0",
  "overall_status": "PASS | WARN | FAIL",
  "subsystems": [
    {
      "subsystem_name": "Core Governance System",
      "status": "PASS | WARN | FAIL",
      "details": "Detailed status message",
      "files_checked": 8,
      "files_passed": 8,
      "files_failed": 0,
      "missing_files": [],
      "invalid_files": [],
      "risks": [],
      "recommended_actions": []
    }
  ],
  "summary": {
    "total_subsystems": 12,
    "passed": 10,
    "warnings": 2,
    "failed": 0,
    "total_files_checked": 100,
    "missing_files_count": 0,
    "invalid_json_count": 0
  },
  "recommendations": [
    "Update ARCHITECTURE_INDEX.json",
    "Run compliance engine activation"
  ]
}
```

### 4.2 Markdown Output (`self-test-report.md`)

Structured report including:
- Executive Summary
- Overall Status
- Subsystem-by-Subsystem Results
- Missing Files List
- Invalid Files List
- Risks Identified
- Recommended Actions
- Next Steps

## 5. Integration Points

### 5.1 Orchestration Integration
- Validate module readiness
- Check build plan alignment
- Verify builder capability mapping
- Validate gating rules
- Check for change-management blockers
- Check for compliance blockers

### 5.2 Runtime Integration
- Verify continuity-export scripts
- Validate AI-memory schemas
- Check runtime maturity profiles
- Validate risk registers
- Verify watchdog alert schemas

### 5.3 Change Management Integration
- Check for pending change records
- Validate change approval status
- Verify rollback plans exist
- Check test plans

## 6. Execution Requirements

### 6.1 Command
```bash
python foreman/scripts/run-self-test.py
```

### 6.2 Prerequisites
- Python 3.8+
- Read access to all foreman/ directories
- Write access for report generation

### 6.3 Expected Outputs
- `self-test-report.json` (in current directory or specified output path)
- `self-test-report.md` (in current directory or specified output path)

### 6.4 Exit Codes
- 0: PASS - All critical systems healthy
- 1: WARN - Some warnings present, but functional
- 2: FAIL - Critical systems missing or broken

## 7. Compliance Requirements

The self-test system must:

1. **Never access or inspect tenant data**
2. **Never expose secrets or credentials**
3. **Respect privacy-guardrails.md** at all times
4. **Align with identity.md** - Foreman as governance, not builder
5. **Follow command-grammar.md** - Proper terminology
6. **Support change-management-spec.md** - Track changes to self-test
7. **Support upgrade-cycle.md** - Ensure continuity across upgrades

## 8. Success Criteria

A successful self-test implementation must:

1. ✅ Validate all 12 subsystems
2. ✅ Check 100+ critical files
3. ✅ Validate all JSON schemas
4. ✅ Generate structured JSON output
5. ✅ Generate human-readable Markdown output
6. ✅ Provide actionable recommendations
7. ✅ Support chat reset recovery
8. ✅ Never break on missing optional files
9. ✅ Respect all privacy and security guardrails
10. ✅ Be runnable without external dependencies

## 9. Maintenance & Evolution

The self-test system should:

- Be updated when new subsystems are added
- Track changes via change management system
- Be versioned alongside Foreman
- Include self-test validation in CI/CD (if applicable)
- Be documented in SELF_TEST_IMPLEMENTATION_REPORT.md

## 10. Future Enhancements

Potential future additions:

- Performance benchmarking
- Dependency graph validation
- Module health score calculation
- Automated remediation suggestions
- Integration with GitHub Actions
- Slack/email notifications
- Historical trend analysis
