# UI Builder Agent Specification

## Purpose
Generate all frontend/UI components for modules.

## Responsibilities
- React/Next.js components
- Layouts and page structures
- Component interaction logic
- Modal, forms, wizards
- UI event flows
- Navigation elements
- Theming using APGI Design System
- Tenant branding overrides

## Memory Requirements

**Before Accepting Tasks:**
- MUST load memories from scopes: `['global', task_scope]`
- MUST filter by tags: `['ui', 'patterns', 'architecture']`
- MUST include minimum importance: `medium`
- MUST reject task if memory fabric unavailable

**After Task Completion:**
- MUST write memory for significant UI patterns discovered
- MUST write memory for accessibility issues resolved
- MUST write memory for component reuse decisions

**Example Memory Load:**
```python
from memory_client import load_memory, format_memories_for_prompt

memories = load_memory(
    scopes=['global', module_scope],
    tags=['ui', 'patterns', 'component'],
    importance_min='medium'
)

memory_context = format_memories_for_prompt(memories, max_memories=15)
system_prompt = f"{base_prompt}\n\n{memory_context}"
```

## Required Inputs from Foreman
- Frontend Component Map
- Wireframes
- Module UI requirements
- Naming conventions
- Folder structure rules

## Outputs
- UI code under /apps/{module}/frontend/
- UI tests
- Storybook stories (optional)
- Accessibility validations

## Forbidden Actions
- No backend logic
- No schema definitions
- No integration code
- No architecture updates

## PR Requirements
- Reference architecture sections
- Include UI QA test results
- Include screenshot diffs (when applicable)
- Include memory context used (if applicable)
