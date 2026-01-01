# Automated Builder Recruitment Mechanism — Corrective Design
## Design-Only Specification (No Implementation)

**Date**: 2026-01-01  
**Designer**: Maturion Foreman (FM)  
**Authority**: Catastrophic Failure Corrective Action  
**Status**: DESIGN_COMPLETE — READY FOR IMPLEMENTATION

---

## Executive Summary

This document defines the **correct, automated builder recruitment mechanism** for the Maturion ISMS ecosystem. This design replaces the failed documentation-only approach from Phase 4.5/Wave 0.1 with a GitHub-native, machine-readable, automated system.

**Key Design Principles**:
1. **GitHub-Native**: Uses `.github/agents/` for builder contracts
2. **Machine-Readable**: YAML frontmatter enables programmatic access
3. **Automated**: Builder selection and gate binding are programmable
4. **Validated**: Schema validation enforces correctness
5. **Enforceable**: Platform readiness gates prevent execution without contracts

---

## 1. Builder Contract Location and Format

### 1.1 Canonical Location

**Requirement**: All builder contracts MUST be located in:
```
.github/agents/<builder-id>.md
```

**Rationale**:
- GitHub-native path enables GitHub Actions integration
- Consistent with FM agent contract pattern (`.github/agents/ForemanApp-agent.md`)
- Discoverable by automation tools
- Version controlled alongside workflows

**Example Locations**:
- `.github/agents/ui-builder.md`
- `.github/agents/api-builder.md`
- `.github/agents/schema-builder.md`
- `.github/agents/integration-builder.md`
- `.github/agents/qa-builder.md`

### 1.2 Contract Format

**Requirement**: Builder contracts MUST use hybrid format:
- **YAML frontmatter** for machine-readable metadata
- **Markdown body** for human-readable documentation

**Example Structure**:
```markdown
---
builder_id: ui-builder
builder_type: specialized
version: 1.0.0
status: recruited
capabilities: [ui, frontend, components, styling]
responsibilities: [UI components, Layouts, Wizards]
forbidden: [Backend logic, Cross-module logic]
permissions:
  read: [foreman/**, architecture/**]
  write: [apps/*/frontend/**]
recruitment_date: 2025-12-30
---

# Human-readable documentation
...
```

**Rationale**:
- YAML frontmatter is parseable by GitHub Actions and scripts
- Markdown body provides documentation for humans and FM
- Hybrid format supports both automation and understanding

### 1.3 Schema Conformance

**Requirement**: All builder contracts MUST conform to:
```
.github/agents/BUILDER_CONTRACT_SCHEMA.md
```

**Schema Defines**:
- Required YAML frontmatter fields (10 mandatory)
- Required markdown sections (7 mandatory)
- Validation rules for all fields
- Format specifications

**Enforcement**: Schema validation MUST be automated (see Section 4).

---

## 2. Builder Recruitment Process Design

### 2.1 Recruitment Phases

**Phase 1: Contract Creation**
- Create `.github/agents/<builder>.md` contract
- Populate YAML frontmatter with metadata from:
  - `foreman/builder-manifest.json` (responsibilities, forbidden)
  - `foreman/builder/builder-capability-map.json` (capabilities)
  - `foreman/builder/builder-permission-policy.json` (permissions)
- Write markdown documentation sections
- Set `status: recruited`

**Phase 2: Schema Validation**
- Validate YAML frontmatter against schema
- Validate markdown sections against schema
- Validate alignment with `foreman/` artifacts
- Validate no placeholder text ("TBD", "TODO")

**Phase 3: Automated Registration**
- Register builder in builder registry
- Generate builder recruitment report
- Update platform readiness validation

**Phase 4: CS2 Approval**
- Present recruitment evidence to CS2
- Obtain explicit approval
- Activate builder for task assignment

### 2.2 Recruitment Continuity

**Design Principle**: Builder recruitment is **one-time and continuous**.

- **Recruitment** (Wave 0.1): Create contracts, validate, approve [ONE-TIME]
- **Appointment** (Wave 1.0+): Assign tasks to recruited builders [ONGOING]

**Prohibited**:
- Re-recruiting builders for new waves
- Creating "pending appointment" states
- Re-validating already-recruited builders

**Enforcement**: Recruitment continuity verification required before Wave re-entry.

---

## 3. Automation Mechanisms

### 3.1 Builder Selection Mechanism

**Design**: Foreman selects builders programmatically using contract metadata.

**Selection Algorithm** (Pseudocode):
```python
def select_builder_for_task(task):
    # Load all builder contracts
    builders = load_builder_contracts('.github/agents/')
    
    # Filter by required capabilities
    capable_builders = [b for b in builders 
                        if task.required_capabilities.issubset(b.capabilities)]
    
    # Filter by forbidden actions
    allowed_builders = [b for b in capable_builders
                        if not any(forbidden in task.actions 
                                   for forbidden in b.forbidden)]
    
    # Filter by status
    active_builders = [b for b in allowed_builders 
                       if b.status in ['recruited', 'active']]
    
    # Select best match
    return select_best_match(active_builders, task)
```

**Automation Requirements**:
- GitHub Actions can read `.github/agents/*.md` YAML frontmatter
- Python scripts can parse YAML frontmatter using `python-frontmatter` library
- Builder selection is deterministic and auditable

### 3.2 Gate Binding Mechanism

**Design**: QA gates automatically bind to builder PRs using contract metadata.

**Gate Binding Algorithm** (Pseudocode):
```yaml
# .github/workflows/builder-qa-gate.yml
on:
  pull_request:
    paths:
      - 'apps/**/frontend/**'
      - 'apps/**/backend/**'
      - 'apps/**/data/**'

jobs:
  identify_builder:
    runs-on: ubuntu-latest
    steps:
      - name: Identify builder from PR files
        id: builder
        run: |
          # Detect changed paths
          # Match paths to builder write permissions
          # Load corresponding .github/agents/<builder>.md
          # Extract QA requirements
          echo "builder_id=ui-builder" >> $GITHUB_OUTPUT
      
      - name: Validate Builder QA Report
        uses: ./.github/actions/validate-builder-qa
        with:
          builder_id: ${{ steps.builder.id }}
          builder_contract: .github/agents/${{ steps.builder.id }}.md
```

**Automation Requirements**:
- Workflows can dynamically load builder contracts
- Gate validation rules reference contract metadata
- Builder identification is path-based and permission-based

### 3.3 Task Routing Mechanism

**Design**: Tasks are routed to builders based on contract metadata.

**Task Routing Algorithm** (Pseudocode):
```python
def route_task_to_builder(task, qa_range):
    # Load builder contracts
    builders = load_builder_contracts('.github/agents/')
    
    # Find builder matching task domain
    builder = select_builder_for_task(task)
    
    # Create builder assignment
    assignment = {
        'builder_id': builder.builder_id,
        'task_id': task.id,
        'qa_range': qa_range,
        'architecture_refs': task.architecture_refs,
        'contract_version': builder.version
    }
    
    # Generate builder task specification
    generate_builder_task_spec(assignment)
    
    return assignment
```

**Automation Requirements**:
- Task routing is based on contract capabilities and responsibilities
- QA ranges are assigned per builder
- Task specifications reference builder contracts

---

## 4. Validation and Enforcement

### 4.1 Schema Validation Automation

**Design**: Automated schema validation on contract creation/modification.

**GitHub Action Design**:
```yaml
# .github/workflows/validate-builder-contracts.yml
name: Validate Builder Contracts

on:
  pull_request:
    paths:
      - '.github/agents/*-builder.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Validate Builder Contracts
        run: |
          python scripts/validate_builder_contracts.py \
            --schema .github/agents/BUILDER_CONTRACT_SCHEMA.md \
            --contracts .github/agents/*-builder.md
```

**Validation Script Design** (`scripts/validate_builder_contracts.py`):
```python
import frontmatter
import json

def validate_contract(contract_path, schema):
    # Load contract
    with open(contract_path) as f:
        post = frontmatter.load(f)
    
    # Validate YAML frontmatter
    validate_yaml_fields(post.metadata, schema)
    
    # Validate markdown sections
    validate_markdown_sections(post.content, schema)
    
    # Validate alignment
    validate_alignment_with_foreman_artifacts(post.metadata)
    
    # Report results
    return validation_result
```

### 4.2 Platform Readiness Validation

**Design**: Platform readiness MUST validate builder contract presence.

**Updated Platform Readiness Checklist**:
```markdown
## Builder Contract Validation

- [ ] All 5 builder contracts exist in `.github/agents/`
  - [ ] ui-builder.md
  - [ ] api-builder.md
  - [ ] schema-builder.md
  - [ ] integration-builder.md
  - [ ] qa-builder.md

- [ ] All builder contracts conform to schema
  - [ ] YAML frontmatter validation: PASS
  - [ ] Markdown sections validation: PASS
  - [ ] Alignment with foreman/ artifacts: PASS

- [ ] Automated builder selection is testable
  - [ ] Builder selection script exists
  - [ ] Test cases pass

- [ ] Gate binding is operational
  - [ ] Builder QA Gate workflow references contracts
  - [ ] Test PR validates gate binding
```

**Enforcement**: Platform readiness approval BLOCKED if validation fails.

### 4.3 Recruitment Verification

**Design**: Verify builder recruitment status programmatically.

**Verification Script Design**:
```python
def verify_builder_recruitment():
    required_builders = ['ui-builder', 'api-builder', 'schema-builder', 
                         'integration-builder', 'qa-builder']
    
    for builder_id in required_builders:
        contract_path = f'.github/agents/{builder_id}.md'
        
        # Check existence
        assert os.path.exists(contract_path), \
            f"Builder contract missing: {contract_path}"
        
        # Load contract
        contract = load_contract(contract_path)
        
        # Verify status
        assert contract.status in ['recruited', 'active'], \
            f"Builder {builder_id} not recruited: status={contract.status}"
        
        # Verify schema compliance
        assert validate_schema(contract), \
            f"Builder {builder_id} contract invalid"
    
    return True  # All builders recruited
```

---

## 5. Integration with Existing Artifacts

### 5.1 Relationship to foreman/ Artifacts

**Design**: Builder contracts in `.github/agents/` are **authoritative** for automation.

**Artifact Hierarchy**:
1. **`.github/agents/<builder>.md`** — AUTHORITATIVE for automation (machine-readable)
2. **`foreman/builder/<builder>-spec.md`** — DETAILED specifications (human-readable)
3. **`foreman/builder-manifest.json`** — SOURCE for responsibilities/forbidden
4. **`foreman/builder/builder-capability-map.json`** — SOURCE for capabilities
5. **`foreman/builder/builder-permission-policy.json`** — SOURCE for permissions

**Consistency Requirements**:
- `.github/agents/<builder>.md` YAML frontmatter MUST align with `foreman/` artifacts
- Changes to `foreman/` artifacts MUST trigger `.github/agents/` updates
- Validation scripts MUST check alignment

**Design Rationale**:
- `.github/agents/` enables automation
- `foreman/` provides detailed specifications
- Both are necessary but serve different purposes

### 5.2 Wave 0.1 Artifacts Preservation

**Design**: Existing Wave 0.1 artifacts remain valid but are supplemented.

**Preserved Artifacts**:
- ✅ `WAVE_0.1_BUILDER_RECRUITMENT_REPORT.md` — Historical evidence
- ✅ `foreman/builder/*-builder-spec.md` — Detailed specifications
- ✅ `foreman/builder-manifest.json` — Source of truth for metadata
- ✅ `foreman/builder/builder-capability-map.json` — Capability definitions
- ✅ `foreman/builder/builder-permission-policy.json` — Permission definitions

**New Artifacts** (This Corrective Action):
- ✅ `.github/agents/ui-builder.md` — Automation contract
- ✅ `.github/agents/api-builder.md` — Automation contract
- ✅ `.github/agents/schema-builder.md` — Automation contract
- ✅ `.github/agents/integration-builder.md` — Automation contract
- ✅ `.github/agents/qa-builder.md` — Automation contract
- ✅ `.github/agents/BUILDER_CONTRACT_SCHEMA.md` — Schema definition

**No Deletion**: Root-level `builder*.md` files remain for backward compatibility.

---

## 6. Ratchet Condition and Enforcement

### 6.1 Permanent Constraint (BL-016)

**Ratchet**: Builder recruitment without `.github/agents/` contracts is permanently prohibited.

**Enforcement Mechanism**:
1. **Platform Readiness Gate**: BLOCKS approval without contracts
2. **CI Validation**: FAILS PRs that bypass contracts
3. **Wave Planning**: REQUIRES contract verification before Wave 1.0+
4. **Governance Canon**: MANDATES `.github/agents/` location

### 6.2 Future Recruitment Process

**For Any New Builder** (future):
1. Create `.github/agents/<new-builder>.md` contract
2. Validate against schema
3. Update `foreman/builder-manifest.json` and related artifacts
4. Run automated recruitment verification
5. Update platform readiness validation
6. Obtain CS2 approval

**Prohibited**:
- Recruitment without `.github/agents/` contract
- "Documentation-only" recruitment
- Manual-only recruitment processes

---

## 7. Success Criteria

### 7.1 Design Completeness Criteria

This design is complete when:
- ✅ Builder contract location specified (`.github/agents/`)
- ✅ Builder contract format specified (YAML + Markdown)
- ✅ Schema defined and documented
- ✅ Recruitment process designed (4 phases)
- ✅ Automation mechanisms designed (selection, gate binding, routing)
- ✅ Validation and enforcement designed
- ✅ Integration with existing artifacts designed
- ✅ Ratchet condition specified

### 7.2 Implementation Readiness Criteria

This design is ready for implementation when:
- ✅ All 5 builder contracts created
- ✅ Schema validation tooling designed
- ✅ Platform readiness updates designed
- ✅ Enforcement mechanisms designed
- ✅ No ambiguity in design specifications

### 7.3 Operational Readiness Criteria

Implementation is complete when:
- ⏳ All 5 builder contracts exist and are valid
- ⏳ Schema validation tooling implemented and tested
- ⏳ Platform readiness validation updated
- ⏳ Automated builder selection tested
- ⏳ Gate binding tested with test PR
- ⏳ Phase 5.0 unblocked

---

## 8. Design Trade-Offs and Rationale

### 8.1 Why .github/agents/ ?

**Alternative Considered**: Keep builders in `foreman/builder/`

**Rationale for .github/agents/**:
- ✅ GitHub-native path enables GitHub Actions integration
- ✅ Consistent with existing FM agent contract pattern
- ✅ Discoverable by automation tools
- ✅ Clearly signals "automation contract" vs "documentation"
- ✅ Governance canon explicitly requires this location

**Trade-Off Accepted**: Requires duplication with `foreman/` artifacts, but benefits outweigh costs.

### 8.2 Why YAML Frontmatter?

**Alternative Considered**: Pure JSON or pure YAML files

**Rationale for YAML + Markdown Hybrid**:
- ✅ YAML frontmatter is parseable by standard tools
- ✅ Markdown body provides human-readable context
- ✅ Hybrid format serves both automation and understanding
- ✅ Standard pattern in documentation-as-code ecosystems

**Trade-Off Accepted**: More complex parsing than pure JSON, but better human readability.

### 8.3 Why Schema Validation?

**Alternative Considered**: Trust builders to format contracts correctly

**Rationale for Mandatory Schema Validation**:
- ✅ Prevents malformed contracts from breaking automation
- ✅ Enforces consistency across all builders
- ✅ Catches errors early (at PR time)
- ✅ Provides clear error messages for corrections

**Trade-Off Accepted**: Additional CI complexity, but prevents systemic failures.

---

## 9. Open Questions and Assumptions

### 9.1 Assumptions Made

1. **GitHub Actions Support**: Assumed GitHub Actions can read YAML frontmatter from markdown files
2. **Python Availability**: Assumed validation scripts can use Python with `python-frontmatter` library
3. **Contract Stability**: Assumed builder contracts are relatively stable (low change frequency)
4. **Single Repository**: Assumed all builders operate in this repository (no cross-repo builders yet)

### 9.2 Open Questions (Not Blocking)

1. **Contract Versioning**: How to handle breaking changes to builder contracts? (Design: use version field, but process TBD)
2. **Multi-Repository**: How to share builder contracts across repositories? (Design: duplicate contracts per repo for now)
3. **Builder Retirement**: How to retire/revoke builders? (Design: set `status: revoked`, but lifecycle TBD)

---

## 10. Conclusion

**Design Status**: ✅ COMPLETE

This design provides a **correct, automated, GitHub-native builder recruitment mechanism** that:
- Uses `.github/agents/` for automation contracts
- Uses YAML frontmatter for machine readability
- Enforces schema validation
- Enables automated builder selection, gate binding, and task routing
- Integrates with existing `foreman/` artifacts
- Establishes permanent ratchet condition (BL-016)

**Next Steps**:
1. ✅ Create 5 builder contracts (DONE)
2. ⏳ Implement schema validation tooling
3. ⏳ Update platform readiness validation
4. ⏳ Test automated builder selection
5. ⏳ Unblock Phase 5.0

---

**Designer**: Maturion Foreman (FM)  
**Design Status**: ✅ COMPLETE — READY FOR IMPLEMENTATION  
**Date**: 2026-01-01
