# Wave Reports Directory

**Purpose**: Storage location for all In-Between Wave Reconciliation (IBWR) artifacts

**Authority**: `governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md`

---

## Structure

This directory contains IBWR artifacts for all build waves:

```
governance/reports/waves/
├── README.md (this file)
├── WAVE_0_RETROSPECTIVE_CERTIFICATION.md (if applicable)
├── WAVE_1_RECONCILIATION_REPORT.md
├── WAVE_1_RETROSPECTIVE_CERTIFICATION.md
├── WAVE_1_CORRECTIVE_ACTIONS.md (if corrective actions exist)
├── WAVE_2_RECONCILIATION_REPORT.md
├── WAVE_2_RETROSPECTIVE_CERTIFICATION.md
├── WAVE_2_CORRECTIVE_ACTIONS.md (if corrective actions exist)
└── ...
```

---

## Artifact Types

### Wave Reconciliation Report

**Filename Pattern**: `WAVE_<N>_RECONCILIATION_REPORT.md`

**Purpose**: Comprehensive evidence and analysis of wave execution

**Required**: Yes (for Wave 1+)

**Template**: `governance/templates/WAVE_RECONCILIATION_REPORT_TEMPLATE.md`

---

### Retrospective Certification

**Filename Pattern**: `WAVE_<N>_RETROSPECTIVE_CERTIFICATION.md`

**Purpose**: FM certification that IBWR was executed completely

**Required**: Yes (for all waves including Wave 0)

**Template**: `governance/templates/WAVE_RETROSPECTIVE_CERTIFICATION_TEMPLATE.md`

---

### Corrective Actions

**Filename Pattern**: `WAVE_<N>_CORRECTIVE_ACTIONS.md`

**Purpose**: Track corrective actions identified and their completion

**Required**: Conditional (only if corrective actions identified)

**Template**: `governance/templates/WAVE_CORRECTIVE_ACTIONS_TEMPLATE.md`

---

## Usage

### For FM (Generating Artifacts)

1. After wave gate declares PASS, initiate IBWR
2. Execute all IBWR phases (see specification)
3. Generate artifacts using templates
4. Store artifacts in this directory
5. Index artifacts in memory fabric
6. Declare IBWR status

### For Future Wave Planning

1. Load previous wave IBWR artifacts
2. Review learnings and patterns
3. Apply corrective actions to planning
4. Avoid anti-patterns identified
5. Reference patterns that worked

---

## Index

### Wave 0 (Bootstrap - Builder Recruitment)

- [ ] `WAVE_0_RETROSPECTIVE_CERTIFICATION.md` - Abbreviated IBWR

### Wave 1 (First Implementation Wave)

- [ ] `WAVE_1_RECONCILIATION_REPORT.md` - Full reconciliation
- [ ] `WAVE_1_RETROSPECTIVE_CERTIFICATION.md` - IBWR certification
- [ ] `WAVE_1_CORRECTIVE_ACTIONS.md` - Corrective actions (if any)

### Wave 2 (Second Implementation Wave)

- [ ] `WAVE_2_RECONCILIATION_REPORT.md`
- [ ] `WAVE_2_RETROSPECTIVE_CERTIFICATION.md`
- [ ] `WAVE_2_CORRECTIVE_ACTIONS.md` (if any)

---

## Compliance

All artifacts in this directory MUST:

✅ Follow template structure  
✅ Be complete and comprehensive  
✅ Reference evidence sources  
✅ Declare IBWR status  
✅ Be indexed in memory fabric  
✅ Be generated before next wave authorization  

---

## References

**Specification**: `governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md`

**Templates**: `governance/templates/`

**FM Contract**: `.github/agents/ForemanApp-agent.md`

---

**Directory Status**: ✅ ACTIVE  
**Created**: 2026-01-04  
**Authority**: Canonical Governance

---

*END OF WAVE REPORTS DIRECTORY README*
