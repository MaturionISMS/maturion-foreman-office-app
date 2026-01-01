# Archived Builder Contracts (v1.0)

**Archive Date**: 2026-01-01  
**Reason**: Replaced by Schema v2.0 contracts with Maturion Doctrine enforcement  
**Authority**: BL-016 Constitutional Alignment

---

## Contents

This directory contains the original builder contracts (v1.0) that were created during Wave 0.1 builder recruitment.

**Files**:
- `builderui-builder.md` (v1.0)
- `builderapi-builder.md` (v1.0)
- `builderschema-builder.md` (v1.0)
- `builderintegration-builder.md` (v1.0)
- `builderqa-builder.md` (v1.0)

---

## Why Archived?

These contracts were functionally correct but **constitutionally incomplete**.

**Missing**:
- Explicit binding to Maturion Build Philosophy
- One-Time Build Discipline requirements
- Zero Test Debt enforcement
- Gate-First Handover Protocol
- Mandatory Enhancement Capture

This created a **CATASTROPHIC risk** where builders could operate with "generic developer mindset" instead of governed Maturion execution model.

---

## Current Contracts (v2.0)

**Location**: `.github/agents/<builder-id>.md`

**Schema**: BUILDER_CONTRACT_SCHEMA v2.0 (Maturion Doctrine Enforced)

All active builder contracts now include:

**YAML Frontmatter**:
- `canonical_authorities` (BUILD_PHILOSOPHY.md, build-to-green-rule.md, FM agent)
- `maturion_doctrine_version: "1.0.0"`
- `handover_protocol: "gate-first-deterministic"`
- `no_debt_rules: "zero-test-debt-mandatory"`
- `evidence_requirements: "complete-audit-trail-mandatory"`

**Mandatory Sections**:
1. Maturion Builder Mindset — MANDATORY
2. One-Time Build Discipline — MANDATORY
3. Zero Test & Test Debt Rules — MANDATORY
4. Gate-First Handover Protocol — MANDATORY
5. Mandatory Enhancement Capture — MANDATORY

---

## Single Source of Truth

**Authoritative Contracts**: `.github/agents/<builder-id>.md` (v2.0)

Do NOT reference these archived contracts. They are preserved for historical record only.

---

**Authority**: Maturion Foreman (FM)  
**Reference**: BL-016, BUILD_PHILOSOPHY.md § V  
**Status**: ARCHIVED — DO NOT USE
