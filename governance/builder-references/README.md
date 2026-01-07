# Builder Reference Documentation

## Purpose

This directory contains **detailed reference material** extracted from builder agent contracts to maintain prompt size compliance (<30,000 characters).

## Structure

Each builder agent file (`.github/agents/*.md`) references specific documentation here to provide:
- Detailed examples
- Extended narratives
- Historical context
- BL case studies
- Execution patterns

## Design Philosophy

**Core + Reference Pattern:**
- **Agent Contract** (`.github/agents/*.md`): Essential constitutional obligations, rules, and workflows
- **Reference Docs** (this directory): Detailed examples, case studies, and extended explanations

## Governance Authority

**Authority**: Issue #447 / #448 - Builder Agent Prompt Size Compliance  
**Status**: ACTIVE  
**Reason**: GitHub agent prompts have 30,000 character limit

## Usage

Builder agents load their core contract from `.github/agents/*.md` and reference additional material here when needed during execution.

**All content maintains constitutional compliance and doctrine integrity.**
