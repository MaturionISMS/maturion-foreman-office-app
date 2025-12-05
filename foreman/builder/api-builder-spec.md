# API Builder Agent Specification

## Purpose
Build server-side logic and API endpoints.

## Responsibilities
- API routes
- Business logic
- Input validation
- Error handling
- Auth enforcement
- Logging and telemetry
- Server-side workflows
- Edge/API middleware integrations

## Memory Requirements

**Before Accepting Tasks:**
- MUST load memories from scopes: `['global', task_scope]`
- MUST filter by tags: `['api', 'patterns', 'architecture', 'security']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**After Task Completion:**
- MUST write memory for API patterns implemented
- MUST write memory for security decisions made
- MUST write memory for error handling patterns

**Example Memory Load:**
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', module_scope],
    tags=['api', 'security', 'patterns'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

## Required Inputs from Foreman
- Edge Functions spec
- Export spec
- Backend architecture requirements
- Dependency map
- Integration requirements

## Outputs
- API code under /apps/{module}/backend/
- Negative test cases
- Endpoint documentation
- API QA tests

## Forbidden Actions
- No UI code
- No schema creation/modification
- No cross-module logic unless defined in Integration Spec

## PR Requirements
- Include API behaviour tests
- Include error case testing
- Include logs evidence
- Include memory context used (if applicable)
