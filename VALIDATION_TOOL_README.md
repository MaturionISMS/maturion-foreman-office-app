# Repository Validation Tool

## Overview

The `validate-repository.py` script performs comprehensive validation of the Maturion AI Foreman repository structure, governance completeness, and specification integrity.

## Usage

### Basic Validation

Run the validation script from the repository root:

```bash
python3 validate-repository.py
```

### Output

The script will:
1. Validate all governance and specification files
2. Check JSON file integrity
3. Generate a detailed validation report
4. Save the report to `VALIDATION_REPORT.md`
5. Exit with code 0 (success) or 1 (critical issues found)

### What It Validates

#### 1. Folder Structure (7 directories)
- Core foreman directory structure
- Admin, builder, compliance, innovation, platform, survey subdirectories

#### 2. Specification Files (Phase 1-5)
For each module (COURSE_CRAFTER, ERM, PIT, THREAT, VULNERABILITY, RISK_ASSESSMENT, WRAC):
- **Phase 1**: True North documents
- **Phase 2**: Database schemas, frontend components, wireframes
- **Phase 3**: Edge functions, integration maps, export specs
- **Phase 4**: QA implementation plans, implementation guides, sprint plans
- **Phase 5**: Changelogs, watchdog logic, model routing specs

#### 3. Governance Completeness (18 files)
- Identity, command grammar, roles and duties
- Architecture standards and validation
- Task distribution, versioning, context awareness
- Memory model, platform awareness, privacy guardrails
- System map, runtime agent plan, templates

#### 4. QA Specifications (4 files)
- QA governance
- Minimum coverage requirements
- QA-of-QA validation
- QA-of-QA checklist

#### 5. Compliance (5 files)
- Compliance reference map
- Compliance control library (JSON)
- Compliance dashboard, QA, and watchdog specs

#### 6. Innovation, Survey, Admin (12 files)
- Innovation: 7 specification files
- Survey: 2 specification files
- Admin: 3 specification files

#### 7. Builder Agent Specifications (6 files)
- API, Integration, QA, Schema, UI builder specs
- Builder collaboration rules

#### 8. Configuration Files (5 JSON files)
- Builder manifest
- Builder task map
- Builder capability map
- Builder permission policy
- Compliance control library

#### 9. JSON File Integrity
- Validates all JSON files are well-formed
- Reports parsing errors if found

## Validation Results

### Status Codes

The script reports status for each validated item:
- ✓ **PASS**: File exists and is valid
- ○ **OPTIONAL**: File is optional for this module
- ✗ **MISSING**: Required file is missing
- ⚠ **EMPTY**: File exists but has no content
- ✗ **INVALID**: JSON file has parsing errors

### Exit Codes

- **0**: Validation passed (no critical errors)
- **1**: Validation failed (critical errors found)

### Readiness Levels

- ✅ **READY FOR ACTIVATION**: No errors, no warnings
- ⚠️ **READY WITH MINOR IMPROVEMENTS RECOMMENDED**: No errors, minor warnings
- ⚠️ **REQUIRES ATTENTION BEFORE ACTIVATION**: Few errors, no critical issues
- ❌ **NOT READY FOR ACTIVATION**: Critical errors present

## Output Files

### VALIDATION_REPORT.md

Detailed markdown report containing:
- Executive summary with readiness status
- Folder structure validation
- Specification files validation by module and phase
- Governance completeness
- QA specifications status
- Compliance infrastructure status
- Innovation/Survey/Admin specifications
- Builder agent specifications
- JSON file integrity
- List of errors and warnings
- Prioritized recommendations

### VALIDATION_SUMMARY.md

Executive summary document with:
- Overall validation status
- Scope of validation
- Issues identified and resolved
- Recommendations by priority
- Activation readiness assessment
- Conclusion and next steps

## Integration with CI/CD

You can integrate this validation into CI/CD pipelines:

```bash
# Run validation and fail build if critical issues found
python3 validate-repository.py || exit 1
```

### GitHub Actions Example

```yaml
- name: Validate Repository Structure
  run: |
    python3 validate-repository.py
    
- name: Upload Validation Report
  uses: actions/upload-artifact@v3
  with:
    name: validation-report
    path: VALIDATION_REPORT.md
```

## Customization

To add additional validation checks, modify the `RepositoryValidator` class in `validate-repository.py`:

1. Add a new validation method (e.g., `validate_custom_check()`)
2. Call it from the `validate_all()` method
3. Store results in `self.validation_results`
4. Update the report generation in `generate_report()`

## Maintenance

### When to Run

- Before major releases
- After significant structural changes
- Quarterly governance reviews
- Before onboarding new builder agents
- After adding new modules

### Updating Validation Rules

When adding new governance requirements:
1. Update the appropriate validation method
2. Add new required files to the respective lists
3. Update the report generation to include new sections
4. Test the changes with `python3 validate-repository.py`

## Troubleshooting

### Common Issues

**Issue**: Script reports "File not found"  
**Solution**: Ensure you're running from the repository root directory

**Issue**: JSON validation fails  
**Solution**: Check the JSON file syntax with `python3 -m json.tool <file.json>`

**Issue**: Missing modules in report  
**Solution**: Verify module names match the pattern `{MODULE}_{SPEC}_v*.md`

## Support

For issues or questions about the validation tool:
1. Check the VALIDATION_REPORT.md for detailed findings
2. Review the script output for specific error messages
3. Consult the Foreman governance documentation in `foreman/`

---

**Last Updated**: 2025-12-03  
**Version**: 1.0  
**Maintained By**: Maturion Foreman
