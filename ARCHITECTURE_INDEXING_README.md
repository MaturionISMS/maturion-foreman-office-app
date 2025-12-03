# ISMS Architecture Indexing System

## Overview

The ISMS Architecture Indexing System is a comprehensive tool that indexes, analyzes, and reports on the entire Maturion ISMS architecture across all modules.

## Purpose

This tool provides:

- **Complete Module Inventory**: Maps all architecture files across the ISMS ecosystem
- **True North Analysis**: Indexes all True North architecture documents
- **Dependency Mapping**: Builds a comprehensive dependency graph showing module relationships
- **Compliance Coverage**: Tracks compliance mapping against international standards
- **Gap Analysis**: Identifies missing architecture elements and specifications
- **Consistency Checks**: Detects circular dependencies and other architectural inconsistencies

## Usage

### Running the Indexer

```bash
python3 index-isms-architecture.py
```

### Output Files

The indexer generates two primary outputs:

1. **ARCHITECTURE_INDEX_REPORT.md** - Human-readable comprehensive report
2. **ARCHITECTURE_INDEX.json** - Machine-readable structured index data

## What Gets Indexed

### Modules Tracked

- COURSE_CRAFTER
- ERM (Enterprise Risk Management)
- PIT (Project Implementation Tracker)
- THREAT
- VULNERABILITY
- RISK_ASSESSMENT
- WRAC (Workspace Risk Analysis & Controls)
- RISK_THREAT
- RISK_VULNERABILITY

### Specification Types

For each module, the following specifications are tracked:

1. **Phase 1 - True North**
   - TRUE_NORTH: Module architecture foundation

2. **Phase 2 - Architecture & Data**
   - DATABASE_SCHEMA: Data model
   - FRONTEND_COMPONENT_MAP: UI components
   - WIREFRAMES: UI design

3. **Phase 3 - Backend & Integration**
   - EDGE_FUNCTIONS: Backend API
   - INTEGRATION_MAP: Module integration
   - EXPORT_SPEC: Data export

4. **Phase 4 - QA & Implementation**
   - QA_IMPLEMENTATION_PLAN: Quality assurance
   - IMPLEMENTATION_GUIDE: Implementation
   - SPRINT_PLAN: Development plan

5. **Phase 5 - Advanced Features**
   - CHANGELOG: Version history
   - WATCHDOG_LOGIC: Monitoring
   - MODEL_ROUTING_SPEC: AI routing

### Compliance Standards

The indexer tracks compliance mapping against:

- ISO 27001 (Information Security)
- ISO 27005 (Risk Management)
- ISO 31000 (Risk Management)
- ISO 22301 (Business Continuity)
- NIST CSF (Cybersecurity Framework)
- NIST 800-53 (Security Controls)
- COBIT (IT Governance)
- GDPR (Data Protection)
- POPIA (Privacy)
- OWASP ASVS (Application Security)
- OWASP Top 10 (Web Security)

## Report Sections

### 1. Executive Summary

- Total modules indexed
- Total architecture files
- True North document count
- Overall compliance coverage percentage
- Missing critical elements count
- Detected inconsistencies count

### 2. Module Map

For each module:
- Completeness percentage
- File count
- Missing critical specifications
- Version information for key files

### 3. True North Index

- Path to each True North document
- Version information
- Content analysis (sections, key elements)

### 4. Architecture Dependency Map

- Master integration map reference
- Module-to-module dependencies
- Dependency statistics:
  - Total dependencies
  - Average dependencies per module
  - Most dependent module
  - Most referenced module

### 5. Compliance Coverage

- Overall coverage percentage
- Coverage by standard (with visual bar charts)
- Modules covered per standard

### 6. Missing Architecture Elements

Categorized by severity:
- **Critical**: Missing True North documents, critical specifications
- **Medium**: Missing non-critical specifications

### 7. Dependency Inconsistencies

Categorized by severity:
- **High**: Circular dependencies
- **Medium**: Integration issues
- **Low**: Orphaned modules, version spread

### 8. Recommendations

Actionable recommendations based on:
- Module completeness gaps
- Missing True North documents
- Low compliance coverage
- Circular dependencies

### 9. Architecture Health Score

Overall health score (0-100) calculated from:
- Module completeness
- Compliance coverage
- Missing elements (penalty)
- Critical inconsistencies (penalty)

## Integration with Existing Tools

This indexer complements the existing `validate-repository.py` tool:

- **validate-repository.py**: Validates governance structure, file presence, and JSON integrity
- **index-isms-architecture.py**: Indexes architecture content, dependencies, and compliance

Both tools should be run as part of architectural governance.

## Maintenance

### Adding New Modules

To track a new module:

1. Add the module name to the `MODULES` list in `index-isms-architecture.py`
2. Ensure the module follows the naming convention: `MODULE_SPEC_vX.Y.md`
3. Run the indexer to include the new module

### Adding New Specification Types

To track a new specification type:

1. Add the spec type to the `SPEC_TYPES` dictionary
2. Specify whether it's optional for certain modules
3. Run the indexer to track the new spec

### Adding New Compliance Standards

To track a new compliance standard:

1. Add the standard to the `COMPLIANCE_STANDARDS` list
2. Run the indexer to track coverage

## Interpreting Results

### Module Completeness

- **80%+**: Good (✓)
- **50-79%**: Needs attention (⚠)
- **<50%**: Requires immediate action (✗)

### Compliance Coverage

- **100%**: Fully covered standard
- **50-99%**: Partial coverage
- **<50%**: Low coverage, needs improvement
- **0%**: Not tracked in modules

### Health Score

- **90-100**: Excellent ✅
- **75-89**: Good ✓
- **60-74**: Needs Improvement ⚠️
- **<60**: Requires Attention ❌

## Governance Integration

This tool supports the Maturion Build Philosophy:

- **One-Time Build Correctness**: Identifies missing specifications before build
- **Zero Regression**: Detects inconsistencies that could cause regression
- **Architectural Fidelity**: Ensures compliance with True North documents
- **Cross-Module Integration**: Maps dependencies and integration points

## Foreman Usage

Maturion Foreman uses this index to:

1. Validate architectural completeness before builds
2. Enforce module boundaries and dependencies
3. Ensure compliance coverage
4. Identify missing architecture elements
5. Prevent circular dependencies
6. Maintain architectural consistency

## Future Enhancements

Potential improvements:

- Content-based similarity analysis between True North documents
- Automated compliance mapping extraction from file content
- Integration with CI/CD pipeline
- Historical tracking of architecture evolution
- Automated recommendations for missing compliance mappings
- Visual dependency graph generation

## Support

For issues or questions about the indexing system, refer to:

- `foreman/identity.md` - Maturion Foreman identity and authority
- `foreman/architecture-governance.md` - Architecture governance rules
- `SRMF_MASTER_BUILD_REFERENCE_v1.0.md` - Master build reference

## License

Part of the Maturion ISMS ecosystem.
