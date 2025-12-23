# Execution Regressions - Phase 3B Batch 2 (PR Gate Friction)

**Batch**: Phase 3B Memory Ingestion Batch 2  
**Date**: 2025-12-23  
**Source**: Historical Issues #677, #687  
**Theme**: PR Gate Friction  
**Scope**: Operational memory (documentation-only)  
**Authority**: FM Repository governance  

---

## Purpose

This document records execution-level regressions discovered through historical PR gate friction analysis. These regressions represent patterns of gate friction or validation failures observed in past work.

---

## Regression 1: Opaque Gate Failure Messages

During Issue #677, PR gates were configured with comprehensive validation rules but failure messages provided minimal diagnostic context. Agents encountered gate failures with generic error messages that required manual investigation to determine root cause and remediation path.

This pattern manifested as repeated gate failures where agents could see that validation failed but could not immediately determine which specific requirement was violated or what corrective action was needed. Investigation required examining gate logs, reviewing gate configuration, and cross-referencing documentation.

The root cause was implementing gate logic without corresponding diagnostic output design. The impact was increased PR cycle time and repeated submissions as agents iteratively discovered requirements through trial and error rather than through clear failure diagnostics.

---

## Regression 2: Simultaneous Multi-Gate Introduction

Issue #687 introduced five new PR gate checks simultaneously without staged rollout or stabilization periods. Agents encountered compound friction where satisfying one new gate requirement would surface failures in another new gate, creating extended remediation cycles.

This pattern manifested as PRs requiring multiple revision cycles to satisfy all new gates, with each revision addressing one or two gates while potentially introducing new failures in others. The compound effect created longer PR cycles and higher friction than any individual gate would have caused.

The root cause was treating PR gate introduction as a configuration deployment task rather than a change management task requiring gradual adoption. The impact was reduced development velocity during the transition period and agent frustration with perceived "moving targets" as multiple requirements were learned simultaneously.
