# QA Governance

## Levels of QA

### Level 1 — Builder QA
Builders test:
- functional correctness  
- schema correctness  
- UI correctness  
- edge logic correctness  
- integration correctness  

### Level 2 — Foreman QA
Maturion tests:
- completeness of QA  
- alignment with architecture  
- sequence correctness  
- boundary protection  
- inter-module integration  

### Level 3 — Human QA (Johan)
Final human inspection for:
- completeness  
- UX quality  
- requirement fulfillment  
- domain correctness

## Memory Fabric Integration

The Memory Fabric is a mandatory subsystem for QA governance:

### Memory Requirements for QA
- All QA validation outcomes must be recorded in memory
- All QA coverage gaps must be logged to memory
- All regression detections must be written to memory
- QA patterns and learnings must feed into memory

### Memory-Informed QA
QA validation must consult memory for:
- Historical test failures and patterns
- Common regression points
- Integration testing lessons
- Coverage gaps from previous builds
- Builder QA quality trends

### QA Readiness Includes Memory
Builds cannot proceed until:
- ✅ Memory Fabric validated
- ✅ QA seed memories present
- ✅ Historical QA patterns loaded
- ✅ Memory read/write functional

**Memory validation is at the same level as QA coverage validation.**
