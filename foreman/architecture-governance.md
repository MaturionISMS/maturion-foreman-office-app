# Architecture Governance

## Core Rules
1. Architecture is the single source of truth.
2. Every build must reference architecture sections.
3. All architecture files must pass QA-of-QA before being used.
4. No module may implement logic owned by another module.
5. All module integration paths must be declared.

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
