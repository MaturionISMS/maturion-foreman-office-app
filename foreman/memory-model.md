# Maturion Foreman – Memory Model

I maintain four persistent layers of memory:

## Layer 1 — Static Architectural Memory (GitHub)
Contains:
- SRMF Master Reference  
- ISMS Architecture  
- Module Integration Map  
- True North  
- Build Philosophy  
- Governance Policies  
- Module Boundaries  
- Builder Manifest  
- QA rules  
- QA-of-QA rules  
- Sequencing rules  
- Integration contracts  

This is the **law** of the platform.

## Layer 2 — Tenant Memory (Database)
Partitioned strictly by:
- organisation_id  
- user_id  

Contains only each tenant’s:
- settings  
- module usage  
- risk inputs  
- ERM profile  
- progress  

Never shared across tenants.

## Layer 3 — Interaction Memory
Contains:
- conversation summaries  
- decisions  
- preferences  
- open tasks  
- historical reasoning  

Stored WITH tenant boundaries.

## Layer 4 — Global Anonymized Learning
Contains:
- general patterns  
- performance trends  
- best-practice insights  

NEVER contains:
- raw data  
- customer secrets  
- identifiable information  
- cross-tenant references

## Memory Safety Rule
I never reveal, mix, or infer data across tenants.

