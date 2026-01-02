# Tier-0 Document Addition Checklist

**Purpose**: Prevent incomplete system updates when adding Tier-0 canonical documents  
**Authority**: Preventive measure created in response to PR #338 failures  
**Status**: MANDATORY for all Tier-0 changes  
**Created**: 2026-01-02

---

## Quick Reference: 5 Files That MUST Change

When adding/removing Tier-0 document:

1. **governance/TIER_0_CANON_MANIFEST.json** - Add/remove entry, bump version
2. **.agent** - Add/remove entry, update manifest_version  
3. **scripts/validate_tier0_activation.py** - Update EXPECTED_TIER0_COUNT
4. **.github/agents/ForemanApp-agent.md** - Update count references
5. **.github/workflows/tier0-activation-gate.yml** - Update count references

**Validation**: Run `python3 scripts/validate_tier0_consistency.py` (MUST PASS)

**Pre-Handover**: Run `python3 scripts/validate_tier0_activation.py` (MUST PASS)

---

## Automated Prevention Tools

### Tool 1: Consistency Validator
**File**: `scripts/validate_tier0_consistency.py`  
**Purpose**: Catch mismatches BEFORE commit  
**Run**: `python3 scripts/validate_tier0_consistency.py`

### Tool 2: Pre-Commit Hook
**File**: `.githooks/pre-commit-tier0-consistency`  
**Setup**: `ln -sf ../../.githooks/pre-commit-tier0-consistency .git/hooks/pre-commit`  
**Behavior**: Auto-runs consistency check, blocks commit if fails

---

## Lessons from PR #338

**Files updated**: ✅ manifest, ✅ markdown  
**Files NOT updated**: ❌ .agent, ❌ validation script, ❌ workflow  
**Result**: Two catastrophic merge gate failures

**Solution**: Use consistency validator + run actual CI scripts

---

*Use this checklist. Every time. No exceptions.*
