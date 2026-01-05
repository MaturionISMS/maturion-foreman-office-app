# ForemanApp Agent Prompt Refactoring Notes

**Date**: 2026-01-05  
**Issue**: GitHub "prompt exceeds max length of 30000" error for ForemanApp agent  
**Authority**: Governance agent (FM governance maintenance)

---

## Problem Statement

The ForemanApp custom agent configuration (`.github/agents/ForemanApp-agent.md`) exceeded GitHub's 30,000 character prompt limit:
- **Original size**: 38,999 characters (30.0% over limit)
- **GitHub error**: "Invalid config: 'prompt' exceeds max length of 30000"
- **Impact**: ForemanApp agent could not be selected when creating GitHub issues

---

## Refactoring Strategy

The refactoring applied a **"Core + References"** model:

### 1. Compression Techniques Applied

#### A. Convert Prose to Concise Bullet Points
- **Before**: Long explanatory paragraphs describing each obligation
- **After**: Dense bullet points with essential requirements only
- **Example**: Section IV "Merge Gate Management" reduced from 6 paragraphs to 4 compact subsections

#### B. Remove Redundant Explanations
- **Before**: Multiple restatements of the same concept in different sections
- **After**: Single, clear statement per concept
- **Example**: "FM does not execute platform actions" stated once in Section II instead of repeated in 3+ sections

#### C. Replace Tables with Dense Text
- **Before**: Multi-column tables with extensive whitespace
- **After**: Inline formatted text preserving all information
- **Example**: Complexity indicators, capability classes

#### D. Compress Repeated Patterns
- **Before**: Each HARD STOP listed with full "FM MUST NOT authorize when:" preamble
- **After**: Standardized "**HARD STOP (Context)**: MUST NOT authorize when:" format
- **Example**: Sections V.F (IBWR), V.G (QA-Catalog-Alignment), VI (Forward-Scan)

#### E. Reference External Specs Instead of Inline Details
- **Before**: Long descriptions of protocols (TARP, IBWR, Forward-Scan) with extensive examples
- **After**: Concise protocol steps with references to detailed specs
- **Example**: TARP protocol compressed from ~200 lines to ~50 lines

### 2. Content Categories

#### KEPT (Essential, Inline):
- **FM Identity**: Governance/orchestration role, non-builder stance
- **All 14 Tier-0 Canon Documents**: Listed with full paths
- **Core Obligations**: One-Time Build Law, 100% QA passing, Zero Test Debt, Architecture Conformance, Design Freeze
- **STOP/HALT/ESCALATE Conditions**: All trigger conditions and required actions
- **HARD STOP Rules**: All blocking conditions for sequencing
- **BL-018/BL-019 Prevention**: QA-Catalog-Alignment Gate, BL Forward-Scan, TARP Protocol (compressed)
- **IBWR Mandatory Execution**: Requirements and blocking conditions
- **Merge Gate Management**: FM ownership, builder boundaries
- **Builder Code Checking**: Mandatory requirements and prohibitions

#### COMPRESSED (Shortened but Present):
- **Constitutional Grounding**: Tier-0 list preserved, long explanations removed
- **Authority & Boundaries**: Core principles stated concisely
- **Sequencing Rules**: All HARD STOPS present, verbose explanations removed
- **STOP/HALT/ESCALATE**: All conditions present, tables converted to dense text
- **Anti-Drift Protections**: Key detection requirements, verbose examples removed

#### REFERENCED (Pointer Only):
- **Detailed Examples**: Pointed to `FM_OPERATIONAL_GUIDANCE.md`
- **Anti-Patterns**: Pointed to `FM_OPERATIONAL_GUIDANCE.md`
- **Complete TARP Template**: Pointed to `SECOND_TIME_FAILURE_PROHIBITION_SPEC.md`
- **Complete IBWR Phases**: Pointed to `IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md`
- **Complete Forward-Scan Protocol**: Pointed to `BL_FORWARD_SCAN_OBLIGATION_SPEC.md`
- **Complete QA-Catalog-Alignment Checks**: Pointed to `QA_CATALOG_ALIGNMENT_GATE_SPEC.md`
- **Constitutional Alignment Checklist**: Pointed to `FM_CONSTITUTIONAL_ALIGNMENT_VERIFICATION.md`
- **Ripple Responsibilities**: Pointed to `FM_RIPPLE_INTELLIGENCE_SPEC.md`

---

## Results

### Character Count Reduction
- **Original**: 38,999 characters
- **Refactored**: 19,984 characters
- **Reduction**: 49% (19,015 characters removed)
- **Margin**: ~10,000 characters below GitHub's 30,000 limit

### Content Preservation Verification

All critical governance elements **preserved**:

✅ **Tier-0 Canon Binding**: All 14 documents listed with full paths  
✅ **One-Time Build Law**: Full principle and enforcement rules  
✅ **Merge Gate Management (T0-014)**: FM ownership, builder boundaries  
✅ **QA-Catalog-Alignment Gate (BL-018/BL-019)**: All mandatory checks, HARD STOP conditions  
✅ **BL Forward-Scan Obligation**: 6-step protocol, blocking requirement  
✅ **TARP Protocol (BL-019)**: Full protocol, second-time failure semantics  
✅ **IBWR Mandatory Execution**: Blocking requirement, mandatory artifacts  
✅ **STOP/HALT/ESCALATE Semantics**: All trigger conditions, state distinctions  
✅ **Mandatory Code Checking**: Builder obligations, FM verification authority  
✅ **Governance Binding (Absolute)**: All 7 absolute rules  
✅ **Anti-Drift Protections**: Memory fabric, arch drift, governance drift detection  
✅ **Constitutional Alignment**: Reference to verification checklist  

All **HARD STOP conditions** preserved:
- Architecture Freeze / Confirmation
- QA-to-Red Compilation (Pre-Implementation)
- Build-to-Green Only
- Platform Readiness Gate
- Builder Recruitment Continuity
- IBWR Gate (Next Wave Authorization)
- QA-Catalog-Alignment Gate (Subwave Authorization)
- BL Forward-Scan (Next Authorization)
- TARP Protocol (Execution Resumption)

All **FM MUST** and **FM MUST NOT** statements preserved in compressed form.

All **References** to detailed specs maintained with full paths.

---

## Safety Margin Strategy

The refactored contract maintains **~10,000 character safety margin** to allow:
- Small governance additions without immediate re-refactoring
- Versioning and signature updates
- Emergency clarifications if needed

### Future-Proofing Recommendations

When extending the ForemanApp contract in the future:

1. **Add New Obligations as Compressed Bullet Points**
   - Use dense format: "**FM MUST**: action1, action2, action3."
   - Avoid long prose explanations

2. **Create New Specs for Complex Features**
   - Add new features as separate specs in `governance/specs/`
   - Reference them in the `reference_documents` section
   - Include only essential enforcement rules inline

3. **Monitor Character Count**
   - Check character count after each addition: `wc -c .github/agents/ForemanApp-agent.md`
   - Target: Stay below 28,000 characters (leave 2,000 margin)

4. **Refactor Again at 27,000+ Characters**
   - If approaching 27,000 characters, perform another compression pass
   - Move more detailed content to external specs
   - Further compress verbose sections

5. **Never Inline Long Specs**
   - Specs like TARP, IBWR, Forward-Scan should NEVER be fully inlined
   - Always use "Protocol + Reference" pattern (short steps + pointer to full spec)

---

## Validation Checklist

This refactoring is COMPLETE when:

- [x] ForemanApp-agent.md is under 30,000 characters (✅ 19,984 characters)
- [x] All 14 Tier-0 documents listed with full paths
- [x] All critical governance obligations preserved
- [x] All HARD STOP conditions present
- [x] All STOP/HALT/ESCALATE triggers present
- [x] All FM MUST / FM MUST NOT statements preserved (compressed)
- [x] All references to detailed specs maintained
- [x] BL-018/BL-019 prevention measures preserved
- [x] IBWR mandatory execution preserved
- [x] Merge Gate Management (T0-014) preserved
- [x] Original backed up to `_archive/` with timestamp
- [ ] GitHub UI verification (agent selectable without error) — **Requires Johan test**

---

## Backup Location

Original version backed up to:
- `.github/agents/_archive/ForemanApp-agent-BEFORE-REFACTOR-2026-01-05.md`

Previous backups:
- `.github/agents/_archive/ForemanApp-agent-ARCHIVE-2026-01-02.md`
- `.github/agents/_archive/ForemanApp-agent-ORIGINAL-BACKUP.md`

---

## Governance Compliance

This refactoring is a **governance configuration change** (not runtime implementation):
- **Authority**: Governance agent (FM governance maintenance)
- **Scope**: `.github/agents/ForemanApp-agent.md` only
- **Impact**: No change to FM functional behavior, only prompt compression
- **Ripple Effects**: None (agent contract content unchanged, only format compressed)
- **Constitutional Alignment**: All Tier-0 obligations preserved

**No runtime code, tests, or Wave 2 implementation affected.**

---

*END OF REFACTORING NOTES*
