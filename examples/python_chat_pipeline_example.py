"""
Memory Integration Example - Python Chat Pipeline

This example demonstrates how to integrate the Unified Memory Fabric
into a Python-based chat/command processing pipeline.

This pattern is suitable for:
- Local builder agents
- Python-based foreman components
- Command-line tools
- Background job processors
"""

import sys
from pathlib import Path

# Add python_agent to path (adjust as needed for your setup)
sys.path.insert(0, str(Path(__file__).parent.parent / "python_agent"))

from memory_client import load_memory, write_memory, format_memories_for_prompt


def process_chat_command(user_input: str, context: dict) -> dict:
    """
    Process a chat command with memory-enriched context.
    
    Args:
        user_input: The user's command or question
        context: Additional context (user_id, module, etc.)
    
    Returns:
        Response dictionary with result and metadata
    """
    
    print("\n" + "="*60)
    print("Chat Command Processing with Memory Integration")
    print("="*60 + "\n")
    
    # Step 1: Load relevant memories BEFORE processing
    print("Step 1: Loading memory context...")
    
    # Determine which scopes and tags are relevant
    scopes = ['global', 'foreman']
    tags = ['governance', 'architecture']
    
    # Add context-specific tags
    if context.get('task_type'):
        tags.append(context['task_type'])
    
    # Load memories
    memories = load_memory(
        scopes=scopes,
        tags=tags,
        importance_min='high'  # Only high and critical memories
    )
    
    print(f"✓ Loaded {len(memories)} relevant memories\n")
    
    # Step 2: Format memories for system prompt
    print("Step 2: Enriching system prompt with memory context...")
    
    memory_context = format_memories_for_prompt(memories, max_memories=10)
    
    base_system_prompt = """You are Maturion Foreman, the governance and orchestration AI.

Your responsibilities:
- Enforce architecture and governance rules
- Coordinate builder agents
- Ensure one-time build correctness
- Maintain zero regression
- Validate all work against standards

You MUST respect all memories provided below.
"""
    
    enriched_system_prompt = f"{base_system_prompt}\n\n{memory_context}"
    
    print(f"✓ System prompt enriched ({len(enriched_system_prompt)} characters)\n")
    
    # Step 3: Process the command (this would call OpenAI/LLM in real implementation)
    print("Step 3: Processing command...")
    print(f"User Input: {user_input}\n")
    
    # Simulate AI processing
    response = {
        'status': 'success',
        'message': f'Processed command with {len(memories)} memory entries as context',
        'action_taken': 'Simulated governance validation',
        'memories_used': len(memories)
    }
    
    print(f"✓ Command processed\n")
    
    # Step 4: Write memory entry for significant actions
    print("Step 4: Writing memory entry for this action...")
    
    # Only write memory for significant actions
    if context.get('is_significant', False):
        entry_id = write_memory({
            'scope': 'foreman',
            'title': f"Chat Command: {context.get('action_name', 'Unknown')}",
            'summary': f"Processed user command: {user_input[:100]}",
            'importance': 'low',
            'tags': ['chat', 'command', 'governance'],
            'details': {
                'user_input': user_input[:200],  # Truncate for privacy
                'memories_used': len(memories),
                'context': context
            }
        })
        print(f"✓ Memory entry created: {entry_id}\n")
    else:
        print("ℹ️  Command not significant enough for memory entry\n")
    
    print("="*60)
    print("Chat Command Processing Complete")
    print("="*60 + "\n")
    
    return response


def example_governance_command():
    """Example: Governance decision command"""
    print("\n" + "#"*60)
    print("# EXAMPLE 1: Governance Decision")
    print("#"*60)
    
    result = process_chat_command(
        user_input="Approve the Asset module architecture for build",
        context={
            'task_type': 'architecture',
            'action_name': 'Architecture Approval',
            'is_significant': True  # This should be remembered
        }
    )
    
    print(f"Result: {result['status']}")
    print(f"Message: {result['message']}\n")


def example_query_command():
    """Example: Information query"""
    print("\n" + "#"*60)
    print("# EXAMPLE 2: Information Query")
    print("#"*60)
    
    result = process_chat_command(
        user_input="What are the QA requirements for API builders?",
        context={
            'task_type': 'qa',
            'action_name': 'QA Information Query',
            'is_significant': False  # Queries don't need memory
        }
    )
    
    print(f"Result: {result['status']}")
    print(f"Message: {result['message']}\n")


def example_build_wave_planning():
    """Example: Build wave planning"""
    print("\n" + "#"*60)
    print("# EXAMPLE 3: Build Wave Planning")
    print("#"*60)
    
    result = process_chat_command(
        user_input="Plan build wave for modules: Asset, Threat, Control",
        context={
            'task_type': 'build',
            'action_name': 'Build Wave Planning',
            'is_significant': True,
            'modules': ['Asset', 'Threat', 'Control']
        }
    )
    
    print(f"Result: {result['status']}")
    print(f"Message: {result['message']}\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MEMORY INTEGRATION EXAMPLES - PYTHON CHAT PIPELINE")
    print("="*60)
    
    # Run examples
    example_governance_command()
    example_query_command()
    example_build_wave_planning()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")
    
    print("Key Takeaways:")
    print("1. Always load memory BEFORE processing commands")
    print("2. Enrich system prompt with memory context")
    print("3. Write memory for significant actions only")
    print("4. Filter memories by scope, tags, and importance")
    print("5. Memory ensures consistency across sessions\n")
