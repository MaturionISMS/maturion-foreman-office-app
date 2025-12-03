# ISMS Architecture Index - Quick Start Guide

## What You Got

A comprehensive architecture indexing system that analyzes and reports on the entire Maturion ISMS ecosystem.

## Quick Start

### 1. Run the Indexer

```bash
python3 index-isms-architecture.py
```

### 2. View the Report

```bash
cat ARCHITECTURE_INDEX_REPORT.md
```

Or open `ARCHITECTURE_INDEX_REPORT.md` in your text editor.

### 3. Use the JSON Data

```bash
cat ARCHITECTURE_INDEX.json | jq '.metadata'
```

## What Gets Generated

### ARCHITECTURE_INDEX_REPORT.md

Human-readable comprehensive report with:

- **Executive Summary**: High-level metrics (9 modules, 87 files, 8 True North docs)
- **Module Map**: Completeness analysis for each module
- **True North Index**: All True North architecture documents
- **Dependency Map**: Module integration and dependencies
- **Compliance Coverage**: Tracking against 11 international standards
- **Missing Elements**: Gap analysis (27 missing critical elements found)
- **Inconsistencies**: Circular dependencies and issues (8 detected)
- **Recommendations**: Actionable items to improve architecture
- **Health Score**: Overall architecture quality (0-100 scale)

### ARCHITECTURE_INDEX.json

Machine-readable data for automation:

```json
{
  "metadata": { ... },
  "modules": { ... },
  "true_north_index": { ... },
  "dependency_map": { ... },
  "compliance_mapping": { ... },
  "missing_elements": [ ... ],
  "inconsistencies": [ ... ]
}
```

## Current State (Initial Run)

### Modules Indexed
✓ 9 modules tracked
✓ 87 architecture files indexed

### Completeness
- **Complete (80%+)**: PIT, THREAT, VULNERABILITY
- **Needs Attention (50-79%)**: COURSE_CRAFTER, ERM, WRAC
- **Requires Action (<50%)**: RISK_ASSESSMENT, RISK_THREAT, RISK_VULNERABILITY

### Key Findings

1. **True North Coverage**: 8/9 modules have True North (missing: RISK_VULNERABILITY)
2. **Compliance Coverage**: 3.0% average (needs significant improvement)
3. **Dependencies**: 26 mapped, 8 circular dependencies detected
4. **Health Score**: 0.0/100 (requires attention)

### Top Priorities

1. ✅ Create True North for RISK_VULNERABILITY
2. ✅ Complete RISK_ASSESSMENT specifications (42.9% complete)
3. ✅ Resolve 8 circular dependencies (especially WRAC ↔ ERM, PIT, THREAT)
4. ✅ Improve compliance mapping in all modules

## Integration with Governance

### Use Before Builds

```bash
# Validate architecture before starting build
python3 index-isms-architecture.py
python3 validate-repository.py
```

### Use for Compliance Audits

The compliance coverage report tracks 11 standards:
- ISO 27001, ISO 27005, ISO 31000, ISO 22301
- NIST CSF, NIST 800-53
- COBIT
- GDPR, POPIA
- OWASP ASVS, OWASP Top 10

### Use for Dependency Analysis

Check `dependency_map` section to see:
- Which modules depend on each other
- Most dependent module: THREAT (5 dependencies)
- Most referenced module: PIT (referenced by 7 modules)

## Regular Usage

### Weekly Architecture Review

```bash
# Run indexer
python3 index-isms-architecture.py

# Check health score
grep "ARCHITECTURE HEALTH SCORE" ARCHITECTURE_INDEX_REPORT.md

# Review recommendations
grep -A 20 "RECOMMENDATIONS" ARCHITECTURE_INDEX_REPORT.md
```

### Before Major Changes

1. Run indexer to capture current state
2. Make architectural changes
3. Run indexer again
4. Compare outputs to see impact

### CI/CD Integration

Add to your pipeline:

```yaml
- name: Index ISMS Architecture
  run: python3 index-isms-architecture.py
  
- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: architecture-index-report
    path: ARCHITECTURE_INDEX_REPORT.md
```

## Understanding the Health Score

The health score (0-100) is calculated as:

```
Score = (Module Completeness + Compliance Coverage) / 2
        - (Missing Elements × 5)
        - (High Severity Issues × 10)
```

### Score Interpretation
- **90-100**: Excellent ✅
- **75-89**: Good ✓
- **60-74**: Needs Improvement ⚠️
- **<60**: Requires Attention ❌

## Next Steps

1. **Review the Report**: Read `ARCHITECTURE_INDEX_REPORT.md` thoroughly
2. **Address Critical Items**: Focus on missing True North and critical specs
3. **Resolve Dependencies**: Work on circular dependencies
4. **Improve Compliance**: Add compliance mappings to module specs
5. **Re-run Regularly**: Track improvements over time

## Questions?

See `ARCHITECTURE_INDEXING_README.md` for detailed documentation.

## Foreman Integration

This tool is part of Maturion Foreman's governance system:

- **Pre-Build**: Validates architecture completeness
- **Governance**: Enforces module boundaries
- **Compliance**: Tracks coverage
- **Quality**: Identifies gaps and inconsistencies

The indexer ensures alignment with:
- SRMF Master Build Reference
- Integrated ISMS Architecture
- Module True North documents
- Maturion Build Philosophy
