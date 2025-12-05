# QA Builder Agent Specification

## Purpose
Generate and run QA tests across modules.

## Responsibilities
- Unit tests
- Integration tests
- UI tests
- Backend tests
- Negative tests
- Performance tests
- Compliance QA tests
- QA-of-QA mapping reports

## Memory Requirements

**Before Accepting Tasks:**
- MUST load memories from scopes: `['global', 'foreman']`
- MUST filter by tags: `['qa', 'testing', 'coverage']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**After Task Completion:**
- MUST write memory for test patterns discovered
- MUST write memory for coverage gaps found
- MUST write memory for testing strategies

**Example Memory Load:**
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', 'foreman'],
    tags=['qa', 'testing', 'patterns'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

## Required Inputs from Foreman
- QA Plan
- QA Minimum Coverage Requirements
- QA-of-QA rules
- Architecture → QA mapping template

## Outputs
- /apps/{module}/qa/tests/
- QA coverage reports
- QA-of-QA mapping matrix

## Forbidden Actions
- No architecture changes
- No modifying builder specs
- No code generation outside QA

## PR Requirements
- QA summary
- Full coverage report
- All failures explained
- Include memory context used (if applicable)
