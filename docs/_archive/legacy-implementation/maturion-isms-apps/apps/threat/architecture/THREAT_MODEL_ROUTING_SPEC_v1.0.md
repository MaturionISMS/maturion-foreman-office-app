# THREAT_MODEL_ROUTING_SPEC_v1.0.md

## Threat Management - AI Model Routing Specification
**Version**: 1.0  
**Date**: 2025-12-04

## Purpose
Define AI model usage and routing logic for Threat Management module.

## Model Categories
### LLM Models
- GPT-4: Complex analysis, decision support
- GPT-3.5: Text generation, summaries
- Claude: Long-context analysis

### Specialized Models
[Module-specific AI models to be defined]

## Routing Rules
### Rule 1: Cost Optimization
- Use GPT-3.5 for standard operations
- Use GPT-4 only for complex tasks
- Cache common queries

### Rule 2: Performance
- Timeout: 30s for AI calls
- Retry: 3 attempts with backoff
- Fallback: Graceful degradation

### Rule 3: Context Management
- Max tokens: 4000 for GPT-3.5, 8000 for GPT-4
- Context window: Last N interactions
- Summarize long contexts

## Model Gateway Integration
- All AI calls through Maturion Model Gateway
- Usage tracking and billing
- Rate limiting per organisation
- Model selection based on tier

## Prompt Templates
[Module-specific prompt templates to be defined]

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
