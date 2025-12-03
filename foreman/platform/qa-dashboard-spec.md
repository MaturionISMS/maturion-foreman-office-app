# QA Dashboard Specification

## Purpose
Provide complete visibility of:
- Total QA runs
- Pass/Fail counts
- Success rate
- Failed categories
- Drill-down test-level details
- Links to architecture and builder PRs

## Levels

### Level 1 — Summary
- total_tests
- total_passed
- total_failed
- success_rate %

### Level 2 — Category Breakdown
Categories:
- Architecture tests
- Data tests
- Schema tests
- UI tests
- Backend logic tests
- Edge function tests
- Integration tests
- Negative tests
- Performance tests

### Level 3 — Test List
For each test:
- name  
- description  
- expected behaviour  
- actual result  
- logs  
- screenshot (UI tests)  
- link to architecture file  
- link to builder PR  

### Level 4 — Test Execution Details
- raw logs  
- input data  
- timestamps  
- failure trace  
- Maturion’s fix recommendations  
