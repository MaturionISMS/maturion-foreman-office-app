# Compliance Reference Map

This file maps all modules and components to international standards.

## Standards Covered
- ISO 27001  
- ISO 27005  
- ISO 31000  
- ISO 22301  
- NIST CSF  
- NIST 800-53  
- COBIT  
- GDPR  
- POPIA  
- OWASP ASVS  
- OWASP Top 10  

## Mapping Model
Each architecture file must contain a compliance section mapping the specification to:

### Example:
- ISO 27001: A.5.1 Information Security Policies  
- ISO 27001: A.12.3 Backup  
- ISO 27005: Risk identification  
- ISO 31000: Communication and consultation  
- NIST CSF: Identify → Risk Assessment  
- COBIT: DSS04  
- GDPR: Article 5  
- POPIA: Condition 7  
- OWASP ASVS: V2 Authentication

## Enforcement
- Maturion verifies presence of compliance mapping.
- QA must contain compliance assertions.
- Compliance watchdog monitors drift.
