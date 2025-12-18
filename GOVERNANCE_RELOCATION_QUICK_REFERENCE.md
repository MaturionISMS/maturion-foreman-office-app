# FM-Level Governance Relocation - Quick Reference

**Status**: ✅ COMPLETE  
**Date**: 2025-12-18

---

## What Was Done

Relocated 82 FM-level governance artefacts from `maturion-foreman-office-app` to canonical directories in preparation for the `maturion-foreman-governance` repository.

---

## Directory Structure

```
governance/
├── policies/          # 16 files - Governance policies and rules
├── contracts/         # 12 files - Contracts, checklists, and templates
├── specs/            # 50 files - Specifications and standards
└── dashboards/       # 4 files - Dashboard specifications
```

**Total**: 82 files

---

## Key Files

### In This Repository

1. **`governance/`** - Contains all relocated FM-level governance files
2. **`GOVERNANCE_RELOCATION_SUMMARY.md`** - Complete relocation documentation
3. **`GOVERNANCE_RELOCATION_MANIFEST.json`** - Machine-readable manifest
4. **Original locations** - Now contain pointer READMEs

---

## Pointer READMEs

Every relocated file has a pointer README in its original location that:
- States the document is governed by Foreman Governance
- Provides the canonical URL in maturion-foreman-governance
- Explains the relocation purpose
- Shows how to access the canonical version

---

## What Was NOT Moved

- ✅ Builder agent specifications (`foreman/builder/`)
- ✅ Foreman app architecture (`foreman/architecture/FOREMAN_*.md`)
- ✅ Change management records (`foreman/change-management/CR-*.json`)
- ✅ Instance data (current-phase.json, dp-red-registry.json, etc.)
- ✅ Build orchestration files (init_builders.py, builder-manifest.json, etc.)

---

## Verification Commands

```bash
# Count files by category
ls -1 governance/policies/ | wc -l    # Should be 16
ls -1 governance/contracts/ | wc -l   # Should be 12
ls -1 governance/specs/ | wc -l       # Should be 50
ls -1 governance/dashboards/ | wc -l  # Should be 4

# Check pointer READMEs
head -5 foreman/governance/governance-supremacy-rule.md
head -5 foreman/privacy-guardrails.md

# Verify builder files untouched
head -10 foreman/builder/ui-builder-spec.md
```

---

## Next Steps

1. **In maturion-foreman-governance repository**:
   - Create directory structure
   - Copy files from `governance/` directory
   - Commit and push
   - Verify URLs are accessible

2. **In this repository**:
   - ✅ Pointer READMEs are in place
   - ✅ Builder files are intact
   - ✅ No enforcement/CI changes made

---

## Files by Category

### Policies (16)
- Governance rules (GSR, Zero Test Debt, Design Freeze, DP-RED)
- Platform policies (AI cost, image generation, security)
- Innovation policies (voting, threshold)
- Architecture policies (naming, folder structure, standardisation)
- Privacy, memory, and versioning policies

### Contracts (12)
- Architecture design checklist
- Quality integrity contract
- Governance gate spec
- Evidence templates (JSON and Markdown)

### Specs (50)
- Core governance (build-to-green, execution state, QA)
- Compliance (QA, watchdog, reference map, control library)
- Innovation (submission, workflow, roadmap)
- Survey (engine, analysis)
- Admin (parking lot, chat, self-improvement)
- Runtime (drift monitor, incident detection, state)
- Platform (UI, privacy, watchdog, analytics)
- Test & Evidence (self-test, test-env, evidence schemas)

### Dashboards (4)
- QA dashboard
- Governance QA dashboard
- Compliance dashboard
- Innovation dashboard

---

## Contact & References

- **Full Summary**: `GOVERNANCE_RELOCATION_SUMMARY.md`
- **Machine Manifest**: `GOVERNANCE_RELOCATION_MANIFEST.json`
- **Canonical Repository**: https://github.com/MaturionISMS/maturion-foreman-governance

---

*This is normalization only. No enforcement, CI, doctrine, or runtime changes were made.*
