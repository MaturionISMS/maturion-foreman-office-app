# Bootstrap Execution Learnings (BL Registry)
## Maturion Foreman — Continuous Improvement Registry

**Purpose**: This registry captures critical learnings from bootstrap execution failures and system design gaps. Each learning becomes a permanent governance constraint to prevent recurrence.

**Authority**: Build Philosophy — Failure → Learning → Continuous Improvement

**Status**: ACTIVE — Continuously Updated

---

## BL-016: Builder Recruitment MUST Be Automated and GitHub-Native

**Date Registered**: 2026-01-01  
**Classification**: CATASTROPHIC  
**Issue Reference**: Builder Recruitment Mechanism Broken  
**Root Cause Analysis**: `ROOT_CAUSE_ANALYSIS_BUILDER_RECRUITMENT_AUTOMATION_FAILURE.md`

### Learning Statement

Builder recruitment MUST be automated, machine-readable, and enforced via `.github`-scoped configuration. Documentation alone is insufficient and constitutes a system failure.

### Rationale

Phase 4.5 and Wave 0.1 treated builder recruitment as a documentation exercise, creating markdown files in the repository root and `foreman/` directory. While content quality was high, this approach failed to establish the automated, GitHub-native recruitment mechanism required for governed build execution.

**Impact**: Phase 5.0 execution became impossible due to lack of automated builder selection, assignment, and gate binding.

**Root Cause**: Misclassification of builder recruitment as documentation instead of system configuration.

### Mandatory Requirements (Permanent)

All future builder recruitment MUST include:

1. **GitHub-Native Location**: Builder contracts MUST exist in `.github/agents/<builder-name>.md`
2. **Machine-Readable Format**: Contracts MUST use structured, parseable format (YAML frontmatter + markdown)
3. **Schema Conformance**: Contracts MUST conform to defined builder contract schema
4. **Automated Validation**: Platform readiness MUST validate builder contract presence and validity
5. **Programmatic Integration**: Builder selection and gate binding MUST be automatable via contracts

### Prohibited Actions (Permanent)

1. ❌ Builder "recruitment" using only root-level documentation files
2. ❌ Builder recruitment without `.github/agents/` contracts
3. ❌ Declaring "recruitment complete" without automated validation
4. ❌ Platform readiness approval without builder contract verification
5. ❌ Treating documentation as sufficient for system configuration

### Enforcement Mechanism

**Validation Gate**: Platform Readiness validation MUST include:
```
- [ ] All required builders have contracts in `.github/agents/<builder>.md`
- [ ] All builder contracts conform to schema
- [ ] Automated recruitment mechanism is testable
- [ ] Builder selection can be performed programmatically
```

**Ratchet Condition**: This learning establishes a permanent constraint. Any future builder recruitment without `.github/agents/` automation requires explicit CS2 override and must document why the standard is being violated.

### Application Examples

**✅ CORRECT Builder Recruitment**:
```
1. Create `.github/agents/ui-builder.md` with YAML frontmatter:
   ---
   builder_id: ui-builder
   builder_type: specialized
   capabilities: [ui, frontend, components, styling]
   responsibilities: [UI components, layouts, wizards]
   forbidden: [backend logic, cross-module logic]
   ---
   
2. Validate contract against schema
3. Test automated builder selection mechanism
4. Update platform readiness with builder contract validation
```

**❌ INCORRECT Builder Recruitment**:
```
1. Create `builderui-builder.md` in root (wrong location)
2. Write comprehensive documentation (not machine-readable)
3. Declare "recruited and validated" (no automation proof)
4. Proceed to next wave (blocked due to no automation)
```

### Related Learnings

- BL-001 through BL-015: (To be backfilled if historical learnings exist)
- Future learnings will reference this as precedent for automation requirements

### Governance Impact

This learning triggers updates to:
1. `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` — Add explicit builder contract validation
2. `foreman/BUILDER_INITIALIZATION.md` — Mandate `.github/agents/` location
3. Platform readiness checklist — Add builder contract verification
4. Builder recruitment specifications — Require automation design

### Status

**Learning Registered**: ✅ COMPLETE  
**Ratchet Activated**: ✅ ACTIVE  
**Corrective Action**: ⏳ IN PROGRESS (This Issue)  
**Governance Updates**: ⏳ PENDING (Post-fix)

---

## Bootstrap Learning Template (For Future Use)

```markdown
## BL-XXX: [Learning Title]

**Date Registered**: YYYY-MM-DD  
**Classification**: [CRITICAL | MAJOR | MODERATE | MINOR]  
**Issue Reference**: [Issue title or reference]  
**Root Cause Analysis**: [RCA document reference]

### Learning Statement

[Single sentence summary of the learning]

### Rationale

[What happened, why it matters, what the impact was]

### Mandatory Requirements (Permanent)

[What MUST be done in future to prevent recurrence]

### Prohibited Actions (Permanent)

[What MUST NOT be done in future]

### Enforcement Mechanism

[How this learning will be enforced]

### Application Examples

**✅ CORRECT**: [Example of correct approach]
**❌ INCORRECT**: [Example of incorrect approach]

### Status

**Learning Registered**: [Status]  
**Ratchet Activated**: [Status]  
**Corrective Action**: [Status]
```

---

## Registry Metadata

**Total Learnings Registered**: 1  
**Catastrophic**: 1 (BL-016)  
**Critical**: 0  
**Major**: 0  
**Moderate**: 0  
**Minor**: 0

**Next Learning ID**: BL-017

---

**Maintained by**: Maturion Foreman (FM)  
**Last Updated**: 2026-01-01  
**Registry Status**: ACTIVE
