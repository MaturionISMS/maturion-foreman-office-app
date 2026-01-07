# Builder Agent Modular Compliance Checklist

**Status**: Active Governance Requirement  
**Authority**: PR #453 (Builder Agent Modularization), Issue #456 (Continuous Improvement)  
**Version**: 1.0.0  
**Last Updated**: 2026-01-07  
**Applies To**: All PRs modifying builder agent contracts or extended references

---

## Purpose

This checklist ensures builder agent modular pattern compliance when making changes to:
- Core builder agent files in `.github/agents/*.md`
- Extended reference files in `governance/agents/builder-references/*.md`

The split-modular pattern must maintain integrity across all builder agent documentation.

---

## When This Checklist Applies

Use this checklist when:
- ✅ Modifying any builder agent .md file in `.github/agents/`
- ✅ Modifying any extended reference .md file in `governance/agents/builder-references/`
- ✅ Adding new sections or content to builder contracts
- ✅ Refactoring builder agent documentation
- ✅ Adding new builders to the system

---

## Pre-Change Checklist

Before making changes to builder agent files:

- [ ] **Understand the Pattern**: Review `governance/agents/builder-references/README.md`
- [ ] **Check Character Limits**: Core agent files MUST stay under 30,000 characters (target: <25,000)
- [ ] **Identify Impact**: Determine if changes affect core contract or extended reference
- [ ] **Plan Modularization**: For new content >2,000 chars, plan to place in extended reference

---

## Core Agent File Changes Checklist

When modifying `.github/agents/*.md` files:

- [ ] **YAML Frontmatter Intact**: No changes to identity, capabilities, permissions (unless intentional)
- [ ] **Constitutional Sections Present**: All mandatory sections remain (Maturion Builder Mindset, One-Time Build, etc.)
- [ ] **Character Count Compliant**: File size <30,000 characters (check with `wc -c`)
- [ ] **Reference Links Valid**: All links to extended references use correct paths
- [ ] **Reference Links Use Section Anchors**: Links include § "Section Name" for precise navigation
- [ ] **No Broken References**: All referenced files and sections exist
- [ ] **Content Compressed**: If adding content, compress existing or move to extended reference
- [ ] **Pattern Consistency**: Follow existing modular pattern (core = rules, reference = examples)

---

## Extended Reference Changes Checklist

When modifying `governance/agents/builder-references/*.md` files:

- [ ] **File Structure Consistent**: Follow README.md pattern guidelines
- [ ] **Section Headers Clear**: Use ## for major sections, ### for subsections
- [ ] **Section Names Match Core References**: Section names match what core files reference
- [ ] **Content Detailed**: Provide step-by-step examples, scenarios, walkthroughs
- [ ] **No Constitutional Rules**: Extended reference contains examples/guidance, not new rules
- [ ] **Cross-References Accurate**: If referencing other sections, use correct paths/names
- [ ] **Examples Concrete**: All examples include specific code/text, not placeholders
- [ ] **Formatting Consistent**: Use consistent markdown formatting across all extended refs

---

## Validation Checklist (MANDATORY)

After making any changes:

- [ ] **Run Validation Script**: Execute `python3 scripts/validate_builder_modular_links.py`
- [ ] **All Links Pass**: Validation reports 0 broken links
- [ ] **Evidence Generated**: `builder-modular-link-validation-evidence.json` created
- [ ] **CI Workflow Passes**: `.github/workflows/builder-modular-link-validation.yml` succeeds
- [ ] **Character Counts Checked**: All core agent files remain under limit
- [ ] **Manual Link Testing**: Manually verify 2-3 reference links load correctly

---

## New Builder Addition Checklist

When adding a new builder:

- [ ] **Core Agent File Created**: `.github/agents/{builder-name}.md` created
- [ ] **Extended Reference Created**: `governance/agents/builder-references/{builder-name}-extended-reference.md` created
- [ ] **README Updated**: Add new builder to `governance/agents/builder-references/README.md` table
- [ ] **Validation Script Updated**: Add builder to `scripts/validate_builder_modular_links.py` (if hardcoded list exists)
- [ ] **CI Workflow Covers**: New builder included in CI validation
- [ ] **Pattern Followed**: New files follow existing modular pattern
- [ ] **Links Established**: Core file includes at least 1 reference link to extended doc
- [ ] **Validation Passes**: All modular link validation passes for new builder

---

## Pre-PR Merge Checklist

Before requesting PR approval:

- [ ] **Modular Link Validation CI PASSED**: Workflow shows green checkmark
- [ ] **Evidence Artifact Available**: Download and verify evidence JSON
- [ ] **No Broken Links in Evidence**: JSON shows `"links_broken": 0`
- [ ] **All Builders Validated**: JSON shows all 5 builders (or new count) validated
- [ ] **Reference Files Complete**: All expected extended reference files exist
- [ ] **Manual Review Done**: At least one human reviewer verified changes
- [ ] **Character Limits Maintained**: No core file exceeds 30,000 characters

---

## Common Issues and Fixes

### Issue: Broken Link (File Not Found)

**Symptom**: Validation reports "Referenced file does not exist"

**Fix**:
1. Check file path is correct (relative to repo root)
2. Ensure file exists in `governance/agents/builder-references/`
3. Check for typos in filename
4. Verify file committed to branch

### Issue: Broken Link (Section Not Found)

**Symptom**: Validation reports "Section 'X' not found in file"

**Fix**:
1. Open referenced file
2. Check exact section header text
3. Update reference to match exact section name (case-sensitive)
4. Include builder name if section is builder-specific (e.g., "BL-018/BL-019 UI Builder Scenarios")

### Issue: Character Limit Exceeded

**Symptom**: Core agent file >30,000 characters

**Fix**:
1. Identify largest sections (usually examples, scenarios)
2. Move detailed examples to extended reference
3. Replace with compressed summary + reference link
4. Keep constitutional obligations in core file
5. Re-run character count: `wc -c .github/agents/{builder}.md`

### Issue: Missing Extended Reference File

**Symptom**: Validation reports extended reference file missing

**Fix**:
1. Create file: `governance/agents/builder-references/{builder}-extended-reference.md`
2. Follow structure from existing extended references
3. Include sections referenced by core file
4. Update README.md to list new file
5. Re-run validation

---

## Integration with PR Gates

This checklist is enforced by:

- **CI Workflow**: `.github/workflows/builder-modular-link-validation.yml`
- **Validation Script**: `scripts/validate_builder_modular_links.py`
- **Evidence Artifact**: `builder-modular-link-validation-evidence.json`

PR gates will:
- ✅ **PASS** if all modular links valid, reference files complete, pattern compliant
- ❌ **BLOCK** if any links broken, files missing, or validation fails

---

## Maintenance Guidelines

**Frequency**: Review this checklist quarterly or after major refactoring

**Updates Required When**:
- Adding new validation rules
- Changing modular pattern structure
- Adding new builders
- Updating character limits
- Enhancing validation script capabilities

**Owner**: Governance Team / FM Agent

---

## Related Documentation

- **Modular Pattern Overview**: `governance/agents/builder-references/README.md`
- **Builder Contract Schema**: `.github/agents/BUILDER_CONTRACT_SCHEMA.md`
- **Validation Script**: `scripts/validate_builder_modular_links.py`
- **CI Workflow**: `.github/workflows/builder-modular-link-validation.yml`
- **PR Gate Reference**: `governance/alignment/PR_GATE_RELEASE_CHECKLISTS_REFERENCE.md`

---

**Status**: ✅ ACTIVE  
**Enforcement**: CI-Validated  
**Non-Compliance Impact**: PR Merge Blocked  
**Last Validated**: 2026-01-07
