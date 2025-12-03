# QA-of-QA Specification

## Purpose
QA-of-QA ensures that:
- QA covers ALL required behaviours  
- No architectural requirement is untested  
- No integration requirement is untested  
- No UX requirement is untested  
- No failure mode is ignored  

## Rules
1. Every architecture requirement must map to at least one QA test.
2. Every QA test must map to one architecture requirement.
3. Missing mappings are blockers.
4. Maturion runs QA-of-QA BEFORE delegating to builders.
