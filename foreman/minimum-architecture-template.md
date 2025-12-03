# Minimum Architecture Template (MARS)

This template defines the **minimum required architecture** for every Maturion ISMS module.

Each module MUST contain the following architecture components:

---

## 1. True North (Required)
Purpose:
- High-level philosophical direction of the module.
- Defines the module’s contribution to ISMS and SRMF.

Filename:
`{MODULE}_TRUE_NORTH_vX.Y.md`

---

## 2. Architecture Specification (Required)
Purpose:
- System design
- Module-level boundaries
- Functional overview
- Process flows

Filename:
`{MODULE}_ARCHITECTURE_vX.Y.md`

---

## 3. Integration Specification (Required)
Purpose:
- Intra-platform and inter-module interactions
- Events
- Message flows
- API contracts
- External systems

Filename:
`{MODULE}_INTEGRATION_SPEC_vX.Y.md`

---

## 4. Data Specification (Required)
Minimum required data documents:
- Database schema  
- Models  
- Global settings (optional)
- Special scale configuration (likelihood, impact, maturity, etc.)

Filenames:
`{MODULE}_DATABASE_SCHEMA_vX.Y.md`  
`{MODULE}_GLOBAL_SETTINGS_vX.Y.md` (optional)  
`{MODULE}_LIKELIHOOD_SCALE_vX.Y.md` (conditional)  
`{MODULE}_IMPACT_SCALE_vX.Y.md` (conditional)

---

## 5. Frontend Specification (Required)
Minimum:
- Component Map  
- UI Wireframes

Optional:
- ASCII Wireframes

Filenames:
`{MODULE}_FRONTEND_COMPONENT_MAP_vX.Y.md`  
`{MODULE}_WIREFRAMES_vX.Y.md`

---

## 6. Backend Specification (Conditional)
Modules requiring server-side logic must define:

- Edge Functions  
- Export Specs  
- Watchdog Logic  
- Model Routing Logic  

Filenames:
`{MODULE}_EDGE_FUNCTIONS_vX.Y.md`  
`{MODULE}_EXPORT_SPEC_vX.Y.md`  
`{MODULE}_WATCHDOG_LOGIC_vX.Y.md`  
`{MODULE}_MODEL_ROUTING_SPEC_vX.Y.md`

---

## 7. QA Specification (Required)
Minimum requirements:
- QA Implementation Plan  
- QA Coverage Matrix  

Filenames:
`{MODULE}_QA_IMPLEMENTATION_PLAN_vX.Y.md`

---

## 8. Implementation Guide (Required)
Purpose:
- Step-by-step instructions for builders  
- Folder structure  
- Tasks required  
- Component-by-component instructions  

Filename:
`{MODULE}_IMPLEMENTATION_GUIDE_vX.Y.md`

---

## 9. Sprint Plan (Required)
Purpose:
- Structured build sequence  
- Timeline  
- Builder distribution  
- Interdependencies  

Filename:
`{MODULE}_SPRINT_PLAN_vX.Y.md`

---

## 10. Changelog (Required)
Must define:
- Initial version  
- Changes  
- Version increments  

Filename:
`{MODULE}_CHANGELOG_vX.Y.md`

