# FM App Backlog Consolidation Report

**Date:** 2025-12-29  
**Authority:** FMRepoBuilder (executing BACKLOG-CONSOLIDATION-01)  
**Status:** Complete  
**Total Issues Surveyed:** 52

---

## Executive Summary

This report classifies all 52 currently open issues in the FM App repository following the completion of Architecture Recovery (ARCH-RECOVERY-01) and the freezing of the True North FM Architecture.

**Classification Summary:**
- **Bucket A (KEEP & QUEUE):** 11 issues - Essential for first app build
- **Bucket B (DEFER - Parking Station):** 4 issues - Valid but not v1
- **Bucket C (CLOSE - Obsolete/Superseded):** 33 issues - Made obsolete by arch recovery
- **Bucket D (MERGE INTO ARCHITECTURE):** 4 issues - Substance belongs in docs

---

## Classification Details

### BUCKET A — KEEP & QUEUE (First App Build Required)

These issues are essential for the first operational FM app build and align with the frozen architecture.

---

#### #208 — BACKLOG-CONSOLIDATION-01 — FM App Backlog Survey & Normalisation
**Bucket:** A  
**Justification:** This is the current issue. It must remain open until the survey is complete and approved. Once this report is accepted, this issue can be closed as complete.

---

#### #201 — ARCH-RECOVERY-01 — FM App Architecture Consolidation & Role Boundary Repair
**Bucket:** A  
**Justification:** This is the foundational architecture recovery issue. While much of the work has been completed (True North architecture is frozen), the issue should remain open as the parent tracking issue until Johan provides final approval and acceptance of the consolidated architecture. This is explicitly referenced in the frozen architecture document.

---

#### #175 — FM-MEM-RT-01 — Add Runtime Memory Lifecycle State Machine Architecture
**Bucket:** A  
**Justification:** The frozen architecture includes memory management as a core FM responsibility (Section 3.3 Memory Governance Layer). This issue defines the runtime memory lifecycle architecture, which is essential for operational FM. The deliverable `MEMORY_LIFECYCLE_STATE_MACHINE.md` is required before memory can be operational.

---

#### #173 — F-U2 — Implement Startup Guard & Forced Redirects
**Bucket:** A  
**Justification:** The frozen architecture specifies commissioning flow as mandatory before app usage (Section 6.4.5 Commissioning Flow Surface). This issue implements the enforcement mechanism (redirects) that prevents use before commissioning is complete. This is critical for preventing users from accessing partially-initialized state.

---

#### #172 — F-U1 — Implement Dummy-Proof Commissioning Wizard UI
**Bucket:** A  
**Justification:** The frozen architecture explicitly includes commissioning flow as a required UI surface (Section 6.4.5). Functional Requirements FR-9.1 mandates a guided commissioning wizard. This issue is the implementation task for that requirement.

---

#### #171 — F-A2 — Implement App Startup Requirement Loader
**Bucket:** A  
**Justification:** The frozen architecture requires that FM validates startup requirements before becoming operational (Section 2.3 Authority Boundaries, Section 4.1 Persistent Memory Requirements). This loader is the implementation of that validation mechanism and is essential for governance enforcement.

---

#### #169 — FM-READINESS-01 — Final Readiness Verification Gate
**Bucket:** A  
**Justification:** Before any build execution can commence, governance requires explicit verification that all governance, memory, agent contracts, and watchdog definitions are complete and aligned. This is the gate issue that confirms FM is ready to execute. Essential for Build-to-Green philosophy.

---

#### #123 — FM Governance Hardening: Architecture & QA Compilation Contracts
**Bucket:** A  
**Justification:** This issue defines the mechanically enforceable governance contracts that FM must use before authorizing builds. It creates the compilation contracts, QA derivation rules, build authorization gate definition, and failure telemetry schema. These are foundational governance enforcement mechanisms required before FM can execute safely. Wave 2.6 is explicitly marked as FM Build Readiness preparation.

---

#### #86 — FM-BEHAV-1 — Enforce "Red Gate Ownership" in FM Reasoning Outputs
**Bucket:** A  
**Justification:** This issue enforces a critical governance behavior: FM cannot dismiss red gates as "legacy debt" without resolution. It ensures FM always produces actionable next steps when gates are red. This is essential for Build-to-Green enforcement and prevents FM from bypassing governance. The frozen architecture requires governance enforcement (Section 2.2.5).

---

#### #78 — FMSYNC-1 — Add "Governance Policy Sync" Mechanism
**Bucket:** A  
**Justification:** The frozen architecture establishes governance supremacy (Section 2.2 Authority Boundaries). This issue creates the mechanism for FM to stay synchronized with the governance repository, preventing policy drift. Essential for maintaining governance alignment over time.

---

#### #74 — W0 — Build FM App to Green (Wave 0)
**Bucket:** A  
**Justification:** This is THE execution issue. Once all preparatory work is complete (#169 passes, governance is hardened, architecture is approved), this issue becomes the actual first build of the FM app to operational green state. This is the culmination of all architecture and governance work.

---

### BUCKET B — DEFER (Parking Station - Future Scope)

These issues represent valid future work but are explicitly not required for the first app build.

---

#### #207 — REQ-GAP-01 — Mobile UI: Requirement or Implementation Choice?
**Bucket:** B  
**Parking Station Reference:** Future/Non-Blocking Requirements Decisions  
**Justification:** This issue explicitly states it is "non-blocking for current build orchestration" and is marked as "decision required." Mobile UI is not mentioned in the frozen architecture's UI surfaces (Section 6.4). This decision can be deferred until after the desktop browser-based FM app is operational. The question itself is valid for future clarity but doesn't block v1.

---

#### #206 — ARCH-GAP-02 — Post-Deployment Application Performance Monitoring (Future Scope)
**Bucket:** B  
**Parking Station Reference:** Future FM Modules / Post-V1 Capabilities  
**Justification:** Explicitly marked "Out-of-scope for v1" and "Future architecture extension" and "Non-blocking." This issue correctly captures a future need (monitoring deployed applications) but states clearly it's not part of True North v1. Should remain parked until FM v1 is operational and the need becomes concrete.

---

#### #204 — ARCH-GAP-01 — Explicit FM → Maturion Delegation Reference in True North Architecture
**Bucket:** B  
**Parking Station Reference:** Post-Freeze Architecture Refinement  
**Justification:** Marked "Non-blocking" and "Post-freeze refinement." This is an architecture documentation improvement (adding explicit DAI/DAR references) but doesn't change behavior or implementation. The delegation model is already operational in governance canon. This is a traceability enhancement that can be addressed after v1 is operational.

---

#### #200 — 🅿️ Parking Item — Future Governance Hardening (Post-Bootstrap)
**Bucket:** B  
**Parking Station Reference:** Self-parking (explicitly marked as parking station item)  
**Justification:** This issue is already explicitly marked as a parking station item. It identifies two future governance tightenings (inspection data authorization separation, emergency stop authorization tightening) that become relevant only after Maturion is live and autonomous execution is enabled. Should remain parked until FM is operational and executing autonomously.

---

### BUCKET C — CLOSE (Obsolete / Superseded)

These issues were made obsolete by the architecture recovery work, completion of governance scaffolding, or shifts in execution model.

---

#### #168 — M-AGENT-ALIGN-01 — Agent Contract Alignment (Foreman & Builders)
**Bucket:** C  
**Justification:** This issue was created before the Architecture Recovery (ARCH-RECOVERY-01) to align agent contracts with POLC model. However, the agent contracts have since been updated and aligned through the architecture recovery process. The `.github/agents/` directory now contains aligned contracts. This work is complete and superseded by #201 (ARCH-RECOVERY-01).

---

#### #167 — M-GOV-ALIGN-01 — FM App Governance Alignment Corrections
**Bucket:** C  
**Justification:** This issue was intended to implement governance alignment corrections after a survey. However, the Architecture Recovery (#201) has already performed this work comprehensively. The frozen True North architecture and the inventory documents demonstrate full alignment with governance. This issue's scope is now complete via the architecture recovery.

---

#### #166 — FM-GOV-AUDIT-01 — FM App Governance Alignment Survey (Read-Only)
**Bucket:** C  
**Justification:** This issue called for a read-only governance alignment survey. The Architecture Recovery process (#201) included this survey as Phase 1 (Inventory). The ARCHITECTURE_RECOVERY_INVENTORY.md document serves as this survey's output. Issue superseded by #201.

---

#### #164 — G-FM-A1 — Formalise Foreman Supervisory Authority (POLC Model)
**Bucket:** C  
**Justification:** This governance definition work has been completed and incorporated into the frozen architecture. The True North FM Architecture document (Section 2.2, 2.3) explicitly defines FM authority boundaries and supervisory model. The governance repository contains the canonical authority model. Work complete, issue obsolete.

---

#### #120 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 18, 2025. These are procedural issues that were relevant during the bootstrap phase. With the completion of architecture recovery and governance hardening, the root causes have been addressed. Should be closed as part of bootstrap completion.

---

#### #119 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 18, 2025. Same rationale as #120. Bootstrap-era tracking issue, now obsolete.

---

#### #117 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #116 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #115 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #114 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #113 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #112 — GOV-BOOT-03 — Reinstate Full Governance Enforcement (Exit Condition)
**Bucket:** C  
**Justification:** This issue was part of a bootstrap governance sequence (GOV-BOOT-01, GOV-VAL-01, GOV-VAL-02, GOV-BOOT-03). These were created to manage temporary governance bypass during validator corrections. The architecture recovery and governance hardening work (#123, #201) have superseded this sequence. Full governance is now enforced via the frozen architecture model.

---

#### #111 — GOV-VAL-02 — Validator Totality & Infrastructure Handling
**Bucket:** C  
**Justification:** Part of the governance bootstrap sequence. This work (ensuring validators fail-closed) is now incorporated into the governance hardening work (#123) and the Build Authorization Gate definition in the frozen architecture. Superseded.

---

#### #110 — GOV-VAL-01 — Make Governance Validators Fail-Closed (Core Fix)
**Bucket:** C  
**Justification:** Part of the governance bootstrap sequence. Fail-closed semantics are now canonical in the frozen architecture (Section 4.2 Build Authorization Gate explicitly requires binary PASS/FAIL). This validator work is incorporated into #123. Superseded.

---

#### #108 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #107 — GOV-BOOT-01 — Verify Governance Bootstrap Is Active (Entry Condition)
**Bucket:** C  
**Justification:** This was the entry point issue for the governance bootstrap sequence. The bootstrap phase is now complete. The architecture is frozen and governance is operational. Bootstrap tracking no longer needed.

---

#### #106 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #104 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #102 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #101 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #100 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #97 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #96 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #95 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #94 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #93 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #92 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #91 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #90 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #89 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #88 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #87 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #85 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

#### #84 — Catastrophic Failure — Build-to-Green Enforcement
**Bucket:** C  
**Justification:** Auto-generated catastrophic failure tracking issue from December 16, 2025. Bootstrap-era tracking issue, now obsolete.

---

### BUCKET D — MERGE INTO ARCHITECTURE / REQUIREMENTS

These issues contain substance that should be incorporated into documentation rather than tracked as tasks.

---

#### #76 — FMQA-2 — Implement Governed QA Parking Station (No Skips) + Watcher
**Bucket:** D  
**Target Document:** docs/governance/qa/QA_PARKING_STATION_SPEC.md (to be created)  
**Justification:** This issue describes a governance mechanism (QA parking station with watcher) rather than a single implementation task. The concept should be documented in governance as the canonical "how to handle future/blocked QA without test dodging" specification. Once documented in governance, implementation can be broken into specific technical tasks if needed.

---

#### #69 — C2 — agent.md Alignment Sweep (MANDATORY)
**Bucket:** D  
**Target Document:** docs/governance/AGENT_CONTRACT_ALIGNMENT_REQUIREMENTS.md (to be created)  
**Justification:** This issue describes a requirement for ongoing agent contract alignment across all repos. Rather than a one-time task, this should be documented as a permanent governance requirement in a specification that defines how agent contracts must remain aligned. The frozen architecture already addresses agent contracts for FM; this is a cross-repo governance requirement.

---

#### #68 — C1 — End-to-End Governance Gate Dry Run
**Bucket:** D  
**Target Document:** Merge into FR-2.1 (Build Authorization Gate testing requirements) in FUNCTIONAL_REQUIREMENTS.md  
**Justification:** This describes a testing requirement (E2E dry run of governance gate) that should be part of the Build Authorization Gate's acceptance criteria in the functional requirements. It's not a separate implementation issue but rather a validation requirement for the gate itself. The frozen architecture already includes the gate; this is a testing/validation requirement.

---

#### #87 — Catastrophic Failure — Build-to-Green Enforcement (Exception for Comment)
**Bucket:** D  
**Target Document:** docs/governance/BOOTSTRAP_LESSONS_LEARNED.md (to be created)  
**Justification:** Issue #87 has a unique comment (not present in other CF issues) that documents a governance observation about pre-existing failures. The comment reads: "The governance-gate failure should be investigated and resolved. However, it appears the failures are pre-existing and unrelated to the changes in this PR. If this is a legacy issue, it should be tracked separately." This represents a lesson learned about legacy debt handling that should be extracted and incorporated into a bootstrap lessons document, then the issue closed.

---

## Recommended Active Queue (Bucket A - Sequenced)

Based on dependency analysis and the frozen architecture, the recommended execution sequence for Bucket A issues is:

### Phase 1: Complete Architecture Foundation (Prerequisites)
1. **#201** - ARCH-RECOVERY-01 (await Johan approval)
2. **#208** - BACKLOG-CONSOLIDATION-01 (this survey - close after approval)

### Phase 2: Harden Governance Enforcement (Build Readiness)
3. **#123** - FM Governance Hardening (compilation contracts, QA rules, build auth gate, telemetry)
4. **#78** - FMSYNC-1 (governance policy sync mechanism)
5. **#86** - FM-BEHAV-1 (red gate ownership enforcement)

### Phase 3: Complete Memory Architecture
6. **#175** - FM-MEM-RT-01 (memory lifecycle state machine)

### Phase 4: Implement Commissioning Flow
7. **#171** - F-A2 (startup requirement loader)
8. **#172** - F-U1 (commissioning wizard UI)
9. **#173** - F-U2 (startup guard & redirects)

### Phase 5: Final Verification & Build
10. **#169** - FM-READINESS-01 (final readiness verification gate)
11. **#74** - W0 (Build FM App to Green - Wave 0)

---

## Closure Recommendations

### Immediate Closure (Bucket C - 33 issues)
The following 33 issues should be closed immediately as obsolete/superseded:

**Governance Bootstrap Sequence (5 issues):**
- #164, #112, #111, #110, #107

**Agent Alignment Pre-Recovery (3 issues):**
- #168, #167, #166

**Catastrophic Failure Tracking (25 issues):**
- #120, #119, #117, #116, #115, #114, #113, #108, #106, #104, #102, #101, #100, #97, #96, #95, #94, #93, #92, #91, #90, #89, #88, #85, #84

### Defer to Parking Station (Bucket B - 4 issues)
The following 4 issues should be labeled "parking-station" and kept open but deprioritized:
- #207, #206, #204, #200

### Migrate to Documentation (Bucket D - 4 issues)
The following 4 issues should have their substance extracted into documentation, then closed:
- #76 → Create QA_PARKING_STATION_SPEC.md
- #69 → Create AGENT_CONTRACT_ALIGNMENT_REQUIREMENTS.md
- #68 → Merge into FUNCTIONAL_REQUIREMENTS.md (FR-2.1 testing)
- #87 → Extract comment to BOOTSTRAP_LESSONS_LEARNED.md

---

## Summary Statistics

| Bucket | Count | Action |
|--------|-------|--------|
| A - KEEP & QUEUE | 11 | Execute in sequence |
| B - DEFER | 4 | Label parking-station, deprioritize |
| C - CLOSE | 33 | Close as obsolete/superseded |
| D - MERGE INTO DOCS | 4 | Extract to docs, then close |
| **TOTAL** | **52** | All classified |

---

## Exit Criteria Validation

✅ **Every open issue is classified** - All 52 issues assigned to buckets A/B/C/D  
✅ **Recommended Active Queue identified** - 11 issues in Bucket A with clear sequencing  
✅ **No issue left unclassified** - Complete coverage achieved  
✅ **Critical intent preserved** - Essential work (Bucket A) retained, future ideas (Bucket B) parked, obsolete work (Bucket C) identified for closure

---

## Notes

This consolidation represents the convergence point after architecture recovery. The backlog is now normalized such that:

1. **Only essential v1 work remains queued** (11 issues)
2. **Valid future ideas are explicitly parked** (4 issues)
3. **Bootstrap/exploration debt is identified for cleanup** (33 issues)
4. **Governance/architecture content is extracted to permanent docs** (4 issues)

Johan (CS2) can now confidently close, defer, or re-sequence the backlog without losing critical intent.

---

**Report Status:** COMPLETE  
**Next Action:** Await Johan approval to execute closure/deferral actions
