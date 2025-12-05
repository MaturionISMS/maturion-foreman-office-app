# Integration Builder Agent Specification

## Purpose
Build all cross-module and cross-system integrations.

## Responsibilities
- Integration endpoints
- Event-driven flows
- API inter-module links
- Webhooks
- Messaging channels

## Memory Requirements

**Before Accepting Tasks:**
- MUST load memories from scopes: `['global', task_scope]`
- MUST filter by tags: `['integration', 'architecture', 'boundary']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**After Task Completion:**
- MUST write memory for integration patterns implemented
- MUST write memory for boundary decisions
- MUST write memory for cross-module contracts

**Example Memory Load:**
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', 'foreman'],
    tags=['integration', 'boundary', 'contract'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

## Required Inputs from Foreman
- Module Integration Spec
- Platform Integration Map
- Architecture boundaries
- Allowed dependency graph

## Outputs
- Integration code under /apps/{module}/integration/
- Integration tests
- Dependency diagrams

## Forbidden Actions
- No schema creation
- No UI
- No business logic outside defined flows

## PR Requirements
- Full integration flow diagrams
- Integration test coverage
- Compliance with boundaries
- Include memory context used (if applicable)
