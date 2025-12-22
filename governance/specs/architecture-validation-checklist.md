# Architecture Validation Checklist

This checklist is executed by Maturion BEFORE builders are allowed to begin.

## 1. True North
- [ ] Does it exist?
- [ ] Does it define module vision & purpose?
- [ ] Does it align with ISMS True North?

## 2. Architecture Spec
- [ ] Exists?
- [ ] Includes module processes?
- [ ] Includes boundaries?
- [ ] Includes functional decomposition?

## 3. Integration Spec
- [ ] Exists?
- [ ] Declares all inbound/outbound interactions?
- [ ] Declares all events and API flows?
- [ ] Declares cross-module dependencies?

## 4. Data Spec
- [ ] Database schema exists?
- [ ] Includes all required models?
- [ ] Includes validation rules?
- [ ] Includes special scales (if required)?

## 5. Frontend Spec
- [ ] Component map complete?
- [ ] Wireframes complete?
- [ ] Coverage for all user roles?

## 6. Backend Spec
If module needs backend:
- [ ] Edge Functions defined?
- [ ] Export Spec defined?
- [ ] Watchdog Logic defined?
- [ ] Model Routing defined?

## 7. QA Spec
- [ ] QA Plan exists?
- [ ] Covers ALL architecture components?
- [ ] No missing mappings?
- [ ] Deployment and configuration changes have test coverage?
- [ ] Runtime behavior changes have test coverage?
- [ ] Non-testable risks explicitly documented and risk-accepted?
- [ ] No "add tests later" statements present?

## 8. Deployment and Runtime Invariants
- [ ] Deployment architecture fully specified?
- [ ] Environment/provider requirements documented?
- [ ] Migration execution responsibility defined?
- [ ] Runtime configuration validated?
- [ ] Deployment failure modes documented?
- [ ] Rollback procedures defined?
- [ ] Environment-specific constraints identified?
- [ ] Provider compatibility verified?

## 9. FL/CI Learning Integration
- [ ] Historical failure classes reviewed?
- [ ] Applicable failure classes identified?
- [ ] Prevention mechanisms documented for each applicable failure?
- [ ] Prevention mechanisms are testable OR risk-accepted?
- [ ] Non-testable failure scenarios explicitly documented?
- [ ] Monitoring/detection strategy defined for non-testable risks?
- [ ] Risk acceptance obtained from Johan Ras (if needed)?
- [ ] No known failure patterns unaddressed?

## 10. Implementation Guide
- [ ] Steps complete?
- [ ] Task breakdown sensible?

## 11. Sprint Plan
- [ ] Tasks sequenced?
- [ ] Dependencies identified?

## 12. Changelog
- [ ] Version present?
- [ ] Correct format?

## FINAL VALIDATION
- [ ] No missing files  
- [ ] No inconsistencies  
- [ ] No contradictions  
- [ ] No ambiguous requirements
- [ ] All deployment and runtime invariants addressed
- [ ] All FL/CI learning requirements satisfied
- [ ] No deferred testing or "add tests later" statements  

