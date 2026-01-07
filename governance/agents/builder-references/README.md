# Builder Agent Extended References

**Purpose**: Extended documentation for builder agent contracts  
**Location**: `governance/agents/builder-references/`  
**Created**: 2026-01-07  
**Authority**: APGI-cmy/maturion-foreman-office-app#448

---

## Overview

This directory contains extended reference documentation for builder agent contracts. The builder agent files in `.github/agents/` contain essential constitutional doctrine and obligations. These reference documents provide detailed examples, scenarios, and supporting material.

---

## Structure

### Core + Reference Pattern

**Core Agent File** (`.github/agents/*.md`):
- YAML frontmatter (identity, capabilities, permissions)
- Constitutional obligations (compressed)
- Core responsibilities and forbidden actions
- Essential protocols and gate binding
- **Reference links** to extended documentation

**Extended Reference** (`governance/agents/builder-references/*-extended-reference.md`):
- Detailed appointment acknowledgment examples
- BL-018/BL-019 scenario walkthroughs
- Code checking step-by-step procedures
- Enhancement capture detailed examples
- Memory integration protocols
- Gate report format templates

---

## Files in This Directory

### Builder Extended References

| File | Size | Purpose |
|------|------|---------|
| `qa-builder-extended-reference.md` | 15,943 chars | QA Builder detailed examples and scenarios |
| `api-builder-extended-reference.md` | 10,526 chars | API Builder detailed examples and scenarios |
| `ui-builder-extended-reference.md` | 3,405 chars | UI Builder detailed examples and scenarios |
| `schema-builder-extended-reference.md` | 3,145 chars | Schema Builder detailed examples and scenarios |
| `integration-builder-extended-reference.md` | 3,351 chars | Integration Builder detailed examples and scenarios |

---

## Rationale

### Problem

Builder agent files were approaching or exceeding the 30,000 character GitHub agent prompt limit:
- qa-builder.md: 31,688 characters (OVER LIMIT)
- api-builder.md: 28,737 characters (near limit)
- integration-builder.md: 29,216 characters (near limit)
- schema-builder.md: 29,231 characters (near limit)
- ui-builder.md: 28,549 characters (near limit)

### Solution

**Modular Core + Reference Pattern**:
1. Compress core agent files to essential doctrine
2. Extract detailed examples and scenarios to reference docs
3. Link core to reference with clear pointers
4. Preserve 100% of content (moved, not deleted)

### Results

All builder agent files now under 26,000 characters:
- qa-builder.md: 25,407 characters (✅ 19.8% reduction)
- api-builder.md: 24,828 characters (✅ 13.6% reduction)
- ui-builder.md: 23,637 characters (✅ 17.2% reduction)
- schema-builder.md: 24,319 characters (✅ 16.8% reduction)
- integration-builder.md: 24,304 characters (✅ 16.8% reduction)

**Total savings: 25,977 characters across 5 files**

---

## Usage

### For Builders

When reading your agent contract (e.g., `.github/agents/qa-builder.md`), you will encounter reference links like:

```markdown
**Detailed format**: See `governance/agents/builder-references/qa-builder-extended-reference.md` § "Detailed Appointment Acknowledgment Example"
```

Follow these links to access:
- Step-by-step walkthroughs
- Concrete examples
- Detailed scenarios
- Format templates

### For Governance Maintainers

When updating builder contracts:

1. **Core changes** (constitutional obligations, requirements, prohibitions):
   - Update `.github/agents/*.md`
   - Keep changes concise
   - Update reference links if sections change

2. **Example changes** (new scenarios, updated walkthroughs):
   - Update `governance/agents/builder-references/*-extended-reference.md`
   - No need to touch core agent file
   - Maintains character count compliance

3. **New builders**:
   - Create core agent file in `.github/agents/`
   - Create extended reference in `governance/agents/builder-references/`
   - Follow existing pattern
   - Target <25,000 characters for core file

---

## Content Organization

### What Goes in Core Agent File

- YAML frontmatter (identity, capabilities, permissions)
- Builder Appointment Protocol (compressed)
- In-Between Wave Reconciliation (IBWR) awareness (compressed)
- BL-018/BL-019 awareness (compressed, 1-2K chars)
- Constitutional obligations (essential requirements)
- Mandatory sections (Maturion Builder Mindset, One-Time Build, Zero Debt, Gate-First, Enhancement Capture)
- Core responsibilities and forbidden actions
- Permissions and gate binding
- Memory integration requirements (compressed)
- Code checking requirements (compressed)
- FM Execution State Authority (compressed)

### What Goes in Extended Reference

- **Detailed appointment acknowledgment examples** (full template with all sections)
- **BL-018/BL-019 scenarios** (3-5 concrete examples with correct/incorrect responses)
- **Code checking walkthroughs** (step-by-step process for builder-specific work)
- **Enhancement capture examples** (3-5 examples of parked proposals)
- **Memory integration details** (loading protocols, usage examples)
- **Gate report templates** (full Builder QA Report format examples)
- **Historical context** (background on why certain rules exist)
- **Extended narratives** (detailed explanations of complex requirements)

---

## Maintenance Guidelines

### Character Count Management

- Core agent file **MUST** stay under 30,000 characters (target: <25,000)
- Extended reference has no hard limit (keep reasonable, target <20,000)
- If core file grows, move content to reference
- If reference grows too large, split into multiple sections

### Link Maintenance

- Always use relative paths: `governance/agents/builder-references/*.md`
- Use section anchors for precise linking: `§ "Section Title"`
- Test links after updates
- Keep link text descriptive: "See X for detailed Y"

### Content Synchronization

- Core and reference must stay in sync
- When updating requirements, update both
- Core states the rule, reference provides examples
- No contradictions between core and reference

---

## Pattern Benefits

### Maintainability
- Update examples without touching constitutional doctrine
- Easier to keep core files under character limit
- Single source of truth for detailed guidance

### Clarity
- Core files more readable (less verbose)
- Detailed examples easily accessible via links
- Clear separation: rules vs. guidance

### Compliance
- All builders under 30K character limit
- Room for future growth
- Consistent pattern across all builders

### Preservation
- 100% of original content preserved
- No doctrine loss
- All examples available via reference

---

## Related Documentation

- **Builder Contract Schema**: `.github/agents/BUILDER_CONTRACT_SCHEMA.md`
- **Builder Contracts Validation**: `scripts/validate_builder_contracts.py`
- **Completion Validation**: `BUILDER_AGENT_REFACTORING_COMPLETION_VALIDATION.md`
- **Governance Authority Matrix**: `governance/GOVERNANCE_AUTHORITY_MATRIX.md`
- **Builder Ripple Boundary**: `governance/agents/BUILDER_RIPPLE_BOUNDARY_SPEC.md`

---

**Status**: ✅ ACTIVE  
**Pattern**: Core + Reference Modular  
**Last Updated**: 2026-01-07  
**Maintained By**: Governance Team
