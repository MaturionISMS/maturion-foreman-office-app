# Minimum QA Coverage Requirements

## 1. Architecture Coverage
- Every architecture requirement must map to a QA test.

## 2. Data Coverage
- All schema fields must have test coverage.
- All validation rules must be tested.

## 3. Frontend Coverage
- Every UI component must have:
  - Render test
  - Behaviour test
  - Integration test
  - Error-state test

## 4. Backend Coverage
- Edge Functions:
  - Success test
  - Failure test
  - Timeout test
  - Auth test

- Watchdog Logic:
  - Trigger correctness
  - Severity mapping

## 5. Integration Coverage
- All calls between modules must be tested:
  - success paths
  - error paths
  - missing data scenarios

## 6. Performance Baselines
- API response time limits:
  - <300ms simple  
  - <800ms complex  
  - <1500ms analytics or risk calculations  

## 7. Negative Test Cases
- Required for:
  - invalid inputs  
  - permission issues  
  - broken connections  
  - missing required fields  


