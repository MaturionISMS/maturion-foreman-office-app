# Architecture Standardisation System

## Overview

The Architecture Standardisation System is a comprehensive tool for validating and standardising architecture across the entire Maturion ISMS ecosystem. It ensures all modules comply with the **Minimum Architecture Template** (MARS) and identifies gaps, inconsistencies, and dependencies.

---

## Quick Start

```bash
python3 standardise-architecture.py
```

This single command executes a full standardisation pass and generates all reports.

---

## What It Does

The standardisation system performs the following tasks:

1. **Scans All Modules** - Discovers all architecture files in `maturion-isms/apps/`
2. **Validates Completeness** - Checks against minimum-architecture-template requirements
3. **Identifies Missing Components** - Lists all missing architecture documents
4. **Validates True North** - Ensures every module has a True North document
5. **Analyzes Dependencies** - Maps module dependencies and detects circular dependencies
6. **Checks Version Consistency** - Identifies version spread across documents
7. **Verifies Linkages** - Validates architecture → QA → compliance chain
8. **Generates Reports** - Creates comprehensive readiness and fix reports

---

## Generated Outputs

After running, the following files are created:

### 1. STANDARDISATION_REPORT.md
**Executive Summary** of the entire standardisation pass.

**Contains**:
- Module readiness overview
- Key findings and gaps
- Dependency analysis
- Compliance coverage
- Next steps and recommendations

**Purpose**: High-level view for governance and decision-making.

---

### 2. MODULE_READINESS_REPORTS/
**Individual readiness reports** for each module.

**Files**:
- `COURSE_CRAFTER_READINESS_REPORT.md`
- `ERM_READINESS_REPORT.md`
- `PIT_READINESS_REPORT.md`
- `THREAT_READINESS_REPORT.md`
- `VULNERABILITY_READINESS_REPORT.md`
- `RISK_ASSESSMENT_READINESS_REPORT.md`
- `WRAC_READINESS_REPORT.md`

**Each Report Contains**:
- Completeness score (%)
- Readiness status (READY, MOSTLY_READY, PARTIALLY_READY, NOT_READY)
- Required components status (✅/❌)
- Missing components list
- QA and compliance linkage status
- Dependencies
- Recommended actions

**Purpose**: Detailed module-level assessment for targeted fixes.

---

### 3. FIX_BACKLOG.md
**Prioritized list of all issues** requiring resolution.

**Structure**:
- **Priority 1**: Critical blockers (missing module directories, missing True North)
- **Priority 2**: High issues (missing architecture specs)
- **Priority 3**: Medium issues (missing component specs)
- **Dependency Issues**: Circular dependencies
- **Version Issues**: Version inconsistencies
- **Compliance Gaps**: Missing compliance linkages

**Purpose**: Actionable task list for addressing standardisation gaps.

---

### 4. BUILDER_SEQUENCING_PLAN.md
**Build sequencing strategy** for builder agents.

**Contains**:
- **Phase 1**: Foundation modules (no dependencies)
- **Phase 2**: Dependent modules
- **Parallelization opportunities**
- **Builder agent task distribution**
- **Estimated timeline**

**Purpose**: Guides builder agents on what to build and in what order.

---

### 5. standardisation_results.json
**Machine-readable results** in JSON format.

**Contains**:
- All module data
- Missing components
- Version issues
- Dependency graph
- Compliance gaps
- Readiness summary

**Purpose**: Integration with other tools and automation.

---

## Understanding Readiness Scores

Modules are assigned a completeness score and readiness status:

| Score | Status | Meaning |
|-------|--------|---------|
| 90-100% | **READY** | All required components present, ready for build |
| 70-89% | **MOSTLY_READY** | Most components present, minor gaps |
| 50-69% | **PARTIALLY_READY** | Significant gaps, needs work before build |
| 0-49% | **NOT_READY** | Major components missing, substantial work required |

---

## Minimum Architecture Template (MARS)

Every module MUST have the following components:

### Required (All Modules)
1. ✅ **TRUE_NORTH** - Module vision and purpose
2. ✅ **ARCHITECTURE** - System design and boundaries
3. ✅ **INTEGRATION_SPEC** - Module integration points
4. ✅ **DATABASE_SCHEMA** - Data model
5. ✅ **FRONTEND_COMPONENT_MAP** - UI components
6. ✅ **WIREFRAMES** - UI design
7. ✅ **QA_IMPLEMENTATION_PLAN** - Quality assurance
8. ✅ **IMPLEMENTATION_GUIDE** - Build instructions
9. ✅ **SPRINT_PLAN** - Development plan
10. ✅ **CHANGELOG** - Version history

### Conditional (Module-Specific)
- **EDGE_FUNCTIONS** - Required for: COURSE_CRAFTER, ERM, PIT, THREAT, VULNERABILITY
- **EXPORT_SPEC** - Required for: COURSE_CRAFTER, ERM, RISK_ASSESSMENT
- **WATCHDOG_LOGIC** - Required for: PIT, THREAT, VULNERABILITY
- **MODEL_ROUTING_SPEC** - Required for: PIT, THREAT, VULNERABILITY

---

## Compliance Standards Tracked

The system tracks references to the following compliance standards:

- ISO 27001 - Information Security Management
- ISO 27005 - Information Security Risk Management
- ISO 31000 - Risk Management
- ISO 22301 - Business Continuity Management
- NIST CSF - Cybersecurity Framework
- NIST 800-53 - Security and Privacy Controls
- COBIT - Control Objectives
- GDPR - Data Protection Regulation
- POPIA - Protection of Personal Information Act
- OWASP ASVS - Application Security Verification
- OWASP Top 10 - Web Application Security Risks

---

## Dependency Analysis

The system builds a complete dependency graph and detects:

1. **Direct Dependencies** - Modules that depend on other modules
2. **Circular Dependencies** - Modules that have mutual dependencies (flagged as issues)
3. **Dependency Chains** - Multi-hop dependency paths

**Example Circular Dependency**:
```
WRAC → PIT → WRAC
```

These must be resolved by refactoring integration patterns.

---

## Version Consistency Checks

The system identifies:

- **Multiple versions** of the same document (e.g., TRUE_NORTH v1.0 and v0.1)
- **Wide version spread** (too many different versions across a module)
- **Draft versions** (v0.x) that should be finalized

**Recommendation**: Consolidate to single latest version per document type.

---

## Architecture → QA → Compliance Linkage

The system verifies the complete chain:

1. **Architecture**: Module has TRUE_NORTH and ARCHITECTURE specs
2. **QA**: QA plans reference architecture components
3. **Compliance**: QA plans reference compliance standards

**Example**:
```
Architecture ✓ → QA ✓ → Compliance ✗
```

This indicates compliance mappings are missing from QA specs.

---

## Running the System

### Prerequisites

- Python 3.7 or later
- Repository cloned locally
- Standard Python libraries (no external dependencies)

### Execution

```bash
cd /path/to/maturion-ai-foreman
python3 standardise-architecture.py
```

### Expected Output

```
🔧 Starting Full Architecture Standardisation Pass...

📊 Scanning all modules for architecture components...
  ✓ Scanned 7 modules

🔍 Identifying missing architecture components...
  ✓ Identified 76 missing components

🧭 Validating True North documents...
  ✓ COURSE_CRAFTER: True North v1.0 found
  ...

🔗 Analyzing module dependencies...
  ⚠️  Found 2 circular dependency chains:
      WRAC → PIT → WRAC
      THREAT → VULNERABILITY → THREAT

📋 Checking version consistency...
  ✓ Version spread acceptable

🔗 Verifying architecture → QA → compliance linkage...
  COURSE_CRAFTER: Architecture ✓ → QA ✓ → Compliance ✗
  ...

📄 Generating module readiness reports...
  ✓ Generated: COURSE_CRAFTER_READINESS_REPORT.md (NOT_READY)
  ...

📋 Generating fix backlog...
  ✓ Generated FIX_BACKLOG.md

📊 Generating standardisation report...
  ✓ Generated STANDARDISATION_REPORT.md
  ✓ Generated standardisation_results.json

🗓️ Generating builder sequencing plan...
  ✓ Generated BUILDER_SEQUENCING_PLAN.md

✅ Standardisation pass complete!
```

---

## Interpreting Results

### High-Level Summary

Start with **STANDARDISATION_REPORT.md**:
- Review executive summary
- Check readiness overview table
- Identify critical gaps
- Note circular dependencies

### Module-Level Details

Review individual reports in **MODULE_READINESS_REPORTS/**:
- Focus on modules with lowest completeness scores
- Check which components are missing
- Review recommended actions

### Action Planning

Use **FIX_BACKLOG.md**:
- Address Priority 1 issues first (blockers)
- Work through Priority 2 (high issues)
- Plan for Priority 3 (medium issues)
- Coordinate dependency resolution

### Build Planning

Use **BUILDER_SEQUENCING_PLAN.md**:
- Follow phase-based approach
- Leverage parallelization opportunities
- Assign tasks to appropriate builder agents
- Track estimated timeline

---

## Next Steps After Standardisation

1. **Review Reports** - Read STANDARDISATION_REPORT.md and module reports
2. **Prioritize Fixes** - Use FIX_BACKLOG.md to create action items
3. **Generate Missing Docs** - Create placeholder architecture documents
4. **Resolve Dependencies** - Refactor circular dependencies
5. **Normalize Versions** - Consolidate document versions
6. **Add Compliance** - Complete compliance mappings in QA specs
7. **Re-run** - Execute standardisation again to validate fixes
8. **Begin Builds** - Follow sequencing plan once modules are ready

---

## Integration with Foreman Workflow

This standardisation system integrates with the Foreman governance workflow:

1. **Pre-Build Validation** - Run before initiating any build
2. **Architecture Gate** - Modules must pass readiness check
3. **Builder Coordination** - Use sequencing plan for task distribution
4. **QA-of-QA** - Readiness reports inform QA validation
5. **Compliance Verification** - Ensure linkage completeness

---

## Maintenance

### When to Re-run

- After adding new architecture documents
- Before starting a new build cycle
- After resolving standardisation issues
- Periodically (monthly) for drift detection

### Updating the System

The standardisation script can be extended to:
- Add new spec types
- Modify completeness scoring
- Enhance dependency detection
- Add new compliance standards
- Customize report formats

---

## Troubleshooting

### No modules found

**Issue**: Script reports no files found for modules.

**Solution**: 
- Verify `maturion-isms/apps/` directory exists
- Check module directory naming (lowercase, hyphenated)
- Ensure architecture files are in `architecture/` subdirectories

### Version extraction errors

**Issue**: Versions not detected correctly.

**Solution**:
- Ensure files follow naming convention: `{MODULE}_{SPEC}_vX.Y.md`
- Check version format: `v1.0`, `v0.1`, etc.

### Circular dependency false positives

**Issue**: Circular dependencies reported incorrectly.

**Solution**:
- Review dependency detection logic
- Check if module references are in comments/examples
- Verify actual integration patterns in specs

---

## Support

For issues, questions, or enhancements:

1. Review generated reports
2. Check FIX_BACKLOG.md for known issues
3. Consult foreman governance documentation
4. Contact Maturion Foreman team

---

*Part of the Maturion AI Foreman Architecture Governance System*
