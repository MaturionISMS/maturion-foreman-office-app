# Architecture Governance

## Core Rules
1. Architecture is the single source of truth.
2. Every build must reference architecture sections.
3. All architecture files must pass QA-of-QA before being used.
4. No module may implement logic owned by another module.
5. All module integration paths must be declared.
6. **Memory Fabric is a mandatory governance subsystem** - all modules, tasks, and builders must reference it.
7. **Builds cannot proceed until memory readiness = PASS.**

## Architecture Files
Maintained by Maturion:
- ISMS Architecture
- SRMF Master Reference
- Integration Map
- Module Boundaries
- Builder Manifest
- Sequencing Rules
- QA and QA-of-QA specs

## Drift Detection
Maturion must:
- scan for architecture drift  
- produce drift reports  
- request corrections

## Memory Fabric Integration

The Memory Fabric is a mandatory subsystem for architecture governance:

### Memory Requirements
- All architectural decisions must be recorded in memory
- All architecture validations must consult relevant memories
- All drift detections must be logged to memory
- Architecture evolution must reference historical memory

### Memory Scope
Architecture-related memories include:
- Module boundary definitions and changes
- Integration contract decisions
- Design pattern selections
- Breaking change approvals
- Version increment rationales

### Validation
Memory presence and validity are verified as part of architecture readiness checks:
- ✅ Memory directory structure exists
- ✅ Architecture seed memories present
- ✅ Memory schema valid
- ✅ Memory read/write functional
