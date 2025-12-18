# QA Dashboard Specification

## Purpose
Provide complete visibility of:
- Total QA runs
- Pass/Fail counts
- Success rate
- Failed categories
- DP-RED (Design-Phase RED) status
- Drill-down test-level details
- Links to architecture and builder PRs

## Levels

### Level 0 — DP-RED Status Panel

**Design-Phase RED (DP-RED) Tracking**

This panel appears when the system is in QA_DESIGN phase or when DP-RED entries exist.

Display:
```
┌─────────────────────────────────────────┐
│ DP-RED Status                           │
├─────────────────────────────────────────┤
│ Current Phase: QA_DESIGN                │
│ Registered: 58 tests                    │
│ Expiring Soon (7 days): 0               │
│ Invalid Entries: 0                      │
│                                         │
│ Categories:                             │
│   Liveness: 9 tests                     │
│   Governance: 11 tests                  │
│   Decision: 11 tests                    │
│   Evidence: 14 tests                    │
│   Integration: 13 tests                 │
│                                         │
│ Status: ✅ All RED tests registered     │
│                                         │
│ [View Registry] [Validation Report]    │
└─────────────────────────────────────────┘
```

Fields:
- **Current Phase**: QA_DESIGN | QA_BUILD | QA_GREEN | QA_VALIDATE
- **Registered**: Count of tests in DP-RED registry
- **Expiring Soon**: Count of entries expiring within 7 days
- **Invalid Entries**: Count of validation failures
- **Categories**: Breakdown by test category
- **Status**: Overall DP-RED compliance status

Colors:
- Green: All RED tests registered, phase allows DP-RED
- Yellow: Warnings (expiring entries, approaching limits)
- Red: Errors (invalid entries, unregistered RED, wrong phase)

### Level 1 — Summary
- total_tests
- total_passed
- total_failed
  - **DP-RED (Registered)**: Count of intentionally RED tests in registry
  - **Actual Failures**: Count of unregistered failures
- success_rate %
  - **Note**: In QA_DESIGN, success rate accounts for DP-RED
  - Formula: (passed + dp_red) / total_tests

Example Display:
```
Test Results Summary:
  Total Tests: 58
  Passing: 0
  Failing: 58
    ├─ DP-RED (Registered): 58 ✅
    └─ Actual Failures: 0 ❌
  
Phase Status: ✅ GREEN for QA_DESIGN phase
Overall Status: ✅ Ready for merge (all RED registered)
```

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
- **Liveness tests** (DP-RED category)
- **Governance tests** (DP-RED category)
- **Decision tests** (DP-RED category)
- **Evidence tests** (DP-RED category)

For each category, show:
- Total count
- Pass count
- Fail count
- **DP-RED count** (if applicable)
- Pass rate

### Level 3 — Test List
For each test:
- name  
- description  
- expected behaviour  
- actual result  
- **DP-RED Status**:
  - If registered: ✅ Registered DP-RED
  - If not registered and RED: ❌ Unregistered failure
  - If GREEN: ✅ Passing
- **DP-RED Details** (if registered):
  - Reason for RED
  - Registered by
  - Registered date
  - Expiry date (if set)
  - Architecture reference
- logs  
- screenshot (UI tests)  
- link to architecture file  
- link to builder PR  

### Level 4 — Test Execution Details
- raw logs  
- input data  
- timestamps  
- failure trace  
- Maturion's fix recommendations
- **DP-RED Entry** (if applicable):
  - Full JSON entry from registry
  - Validation status
  - Phase compliance

## DP-RED Visual Distinctions

### Color Coding
- **DP-RED tests**: Blue background with ⚠️ icon
- **Actual failures**: Red background with ❌ icon  
- **Passing tests**: Green background with ✅ icon

### Icons
- ⚠️ DP-RED (intentional, registered)
- ❌ Failure (unregistered, needs fix)
- ✅ Pass
- 🔒 Phase blocked (DP-RED in build phase)

### Phase Indicators
```
QA_DESIGN:  ✅ DP-RED allowed
QA_BUILD:   🔒 DP-RED blocked
QA_GREEN:   🔒 DP-RED blocked
QA_VALIDATE: 🔒 DP-RED blocked
```

## Dashboard Filters
Add filters:
- **Show DP-RED only**: Filter to show only registered DP-RED tests
- **Show Actual Failures only**: Filter to show unregistered RED tests
- **Hide DP-RED**: Focus on implementation tests only
- **By Category**: Filter by test category
- **By Phase**: Historical view of different phases

## DP-RED Actions
From dashboard:
- **View Registry**: Open dp-red-registry.json
- **Validation Report**: Show latest validation report
- **Register Test**: (Admin only) Register a RED test as DP-RED
- **Remove Entry**: (Admin only) Remove from registry when GREEN
- **Transition Phase**: (Admin only) Move to next QA phase

## Integration Points
- **Registry File**: `foreman/qa/dp-red-registry.json`
- **Phase File**: `foreman/qa/current-phase.json`
- **Validation Script**: `foreman/scripts/validate-dp-red-compliance.py`
- **CI Reports**: `dp-red-compliance-report.json` artifacts

## Alerts and Notifications

### Critical Alerts
- ❌ Unregistered RED test in QA_DESIGN phase
- ❌ DP-RED entries exist in QA_BUILD+ phase
- ❌ Invalid registry entries

### Warnings
- ⚠️  DP-RED entry expiring within 7 days
- ⚠️  DP-RED entry older than 4 weeks
- ⚠️  High DP-RED count (>100 tests)

### Info
- ℹ️  Phase transition available
- ℹ️  All DP-RED tests cleared
- ℹ️  Registry validated successfully

---

*Updated: 2025-12-16 - Added DP-RED tracking*
