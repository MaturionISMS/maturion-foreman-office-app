# Schema Builder Agent Specification

## Purpose
Build and maintain the database schema and data models.

## Responsibilities
- Database schema files
- Model definitions
- Validation rules
- Indexing strategy
- Relationship mapping
- Migration scripts
- Data lifecycle rules

## Memory Requirements

**Before Accepting Tasks:**
- MUST load memories from scopes: `['global', task_scope]`
- MUST filter by tags: `['schema', 'data', 'architecture']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**After Task Completion:**
- MUST write memory for schema patterns implemented
- MUST write memory for migration strategies
- MUST write memory for relationship decisions

**Example Memory Load:**
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', module_scope],
    tags=['schema', 'data', 'migration'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

## Required Inputs from Foreman
- Database Schema Spec
- Data requirements
- Integration constraints
- Versioning rules

## Outputs
- /apps/{module}/data/models/
- /apps/{module}/data/schema.md
- /apps/{module}/data/migrations/

## Forbidden Actions
- No UI or backend logic
- No modifying another module’s schema
- No altering architecture files

## PR Requirements
- Schema diff summary
- Migration diff summary
- Data QA results
- Include memory context used (if applicable)
