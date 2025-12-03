# Builder Collaboration & Sequencing Rules

## 1. Foreman → Builders
Foreman distributes tasks via:
@{agent}:task { ... }

## 2. Builder → Foreman
Builders return:
- PR link
- QA results
- Coverage report
- Architecture references

## 3. Inter-builder Rules
- Schema builder must complete BEFORE:
  - API builder
  - Integration builder
  - UI builder (for dynamic modules)

- Integration builder must complete AFTER:
  - API builder
  - Schema builder

- UI builder can parallelize AFTER:
  - component map
  - wireframes
  - schema structure approved

## 4. QA Sequencing
1. Builder QA  
2. QA Builder full suite  
3. Foreman QA-of-QA  
4. Foreman integration QA  
5. Human validation (Johan)

## 5. Forbidden Behaviours
- Builders cannot modify architecture
- Builders cannot override another builder’s files
- Cross-module code is prohibited unless defined
