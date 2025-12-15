"""
Maturion Foreman Test Suite

This package contains the QA test suite for the Maturion Foreman governance agent.

Wave 0 Minimum RED QA Suite validates:
1. Liveness & Continuity (heartbeat, stall detection, recovery)
2. Governance Supremacy (architecture freeze, QA bypass prevention)
3. Decision Determinism (same input → same output, replayable traces)
4. Evidence Integrity (evidence generation, schema validation, traceability)
5. Minimal Integration Sanity (task lifecycle, observable failure states)

All tests are expected to be RED (failing) until implementation is complete.
"""
