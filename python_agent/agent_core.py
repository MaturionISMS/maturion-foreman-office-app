#!/usr/bin/env python3
"""
Python Agent Core - Local Builder with Memory Integration

This is a template/reference implementation showing how to integrate
the Unified Memory Fabric into a Python-based builder agent.

Usage:
    from agent_core import AgentCore
    
    agent = AgentCore(agent_name="schema-builder", task_scope="isms")
    result = agent.execute_task(task_definition)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import memory client
try:
    from memory_client import load_memory, write_memory, format_memories_for_prompt
    MEMORY_AVAILABLE = True
except ImportError:
    print("WARNING: Memory client not available. Install python_agent/memory_client.py")
    MEMORY_AVAILABLE = False


class AgentCore:
    """
    Core agent class with integrated memory fabric support.
    
    This class demonstrates the pattern for integrating memory
    into any Python-based builder agent.
    """
    
    def __init__(
        self, 
        agent_name: str,
        task_scope: str = "foreman",
        base_system_prompt: Optional[str] = None
    ):
        """
        Initialize the agent with memory integration.
        
        Args:
            agent_name: Name of this agent (e.g., "schema-builder", "api-builder")
            task_scope: Primary memory scope for this agent's tasks
            base_system_prompt: Base system prompt (memory context will be prepended)
        """
        self.agent_name = agent_name
        self.task_scope = task_scope
        self.base_system_prompt = base_system_prompt or self._get_default_prompt()
        
        # Memory-enriched system prompt (built on first task)
        self.system_prompt = None
        
        # Task execution state
        self.current_task = None
        self.task_history = []
    
    def _get_default_prompt(self) -> str:
        """Get default system prompt for this agent."""
        return f"""You are {self.agent_name}, a specialized builder agent in the Maturion ecosystem.

Your responsibilities:
- Follow architecture and governance rules strictly
- Implement tasks according to specifications
- Write comprehensive tests for all code
- Maintain zero regression
- Report completion status accurately

You operate within the {self.task_scope} scope.
"""
    
    def load_task_memory(
        self, 
        task_type: Optional[str] = None,
        additional_tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Load relevant memories for the current task.
        
        This MUST be called before accepting or executing any task.
        
        Args:
            task_type: Type of task (e.g., "schema", "api", "ui")
            additional_tags: Additional tags to filter memories
        
        Returns:
            List of relevant memory entries
        """
        if not MEMORY_AVAILABLE:
            print("WARNING: Cannot load memory - memory client not available")
            return []
        
        # Determine scopes to load
        scopes = ['global', self.task_scope]
        
        # Determine tags
        tags = additional_tags or []
        if task_type:
            tags.append(task_type)
        tags.extend(['architecture', 'patterns', 'governance'])
        
        # Load memories
        try:
            memories = load_memory(
                scopes=scopes,
                tags=tags,
                importance_min='medium'
            )
            
            print(f"✓ Loaded {len(memories)} relevant memories for task")
            return memories
        
        except Exception as e:
            print(f"WARNING: Error loading memories: {e}")
            return []
    
    def enrich_system_prompt(self, memories: List[Dict[str, Any]]) -> str:
        """
        Enrich the base system prompt with memory context.
        
        Args:
            memories: List of memory entries from load_task_memory()
        
        Returns:
            Enriched system prompt with memory context
        """
        if not MEMORY_AVAILABLE or not memories:
            return self.base_system_prompt
        
        memory_context = format_memories_for_prompt(memories, max_memories=15)
        
        enriched_prompt = f"""{self.base_system_prompt}

{memory_context}

IMPORTANT: The memory context above contains critical governance rules,
architectural decisions, and learned patterns. You MUST respect and apply
all relevant memories when executing your task.
"""
        
        return enriched_prompt
    
    def accept_task(self, task: Dict[str, Any]) -> bool:
        """
        Accept a task for execution.
        
        This method:
        1. Loads relevant memories
        2. Enriches system prompt
        3. Validates task can be accepted
        
        Args:
            task: Task definition dictionary
        
        Returns:
            True if task accepted, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Agent: {self.agent_name}")
        print(f"Task: {task.get('title', 'Unnamed task')}")
        print(f"{'='*60}\n")
        
        # Reject if memory not available
        if not MEMORY_AVAILABLE:
            print("❌ REJECTING TASK: Memory fabric not available")
            print("   Install python_agent/memory_client.py before proceeding")
            return False
        
        # Load memories
        task_type = task.get('type')
        memories = self.load_task_memory(task_type=task_type)
        
        if len(memories) == 0:
            print("⚠️  WARNING: No memories loaded - task acceptance risky")
            print("   Consider initializing memory fabric first")
            # Could reject here, but we'll allow with warning
        
        # Enrich system prompt
        self.system_prompt = self.enrich_system_prompt(memories)
        
        # Store current task
        self.current_task = task
        
        print("✅ Task accepted - ready for execution")
        return True
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task with memory-enriched context.
        
        This is a placeholder - actual implementation would:
        1. Accept the task
        2. Call OpenAI/LLM with enriched prompt
        3. Execute the work
        4. Write completion memory
        
        Args:
            task: Task definition
        
        Returns:
            Task result dictionary
        """
        # Accept task (loads memory and enriches prompt)
        if not self.accept_task(task):
            return {
                'status': 'rejected',
                'reason': 'Memory fabric not available or task invalid'
            }
        
        # TODO: Actual task execution would happen here
        # For now, just simulate
        print("\n[Task Execution Simulation]")
        print(f"System prompt length: {len(self.system_prompt)} characters")
        print(f"Task type: {task.get('type')}")
        print(f"Task scope: {self.task_scope}")
        
        result = {
            'status': 'completed',
            'agent': self.agent_name,
            'task_id': task.get('id', 'unknown'),
            'output': 'Simulated task completion'
        }
        
        # Write completion memory
        self.write_completion_memory(task, result)
        
        return result
    
    def write_completion_memory(
        self, 
        task: Dict[str, Any], 
        result: Dict[str, Any]
    ) -> Optional[str]:
        """
        Write a memory entry after task completion.
        
        Args:
            task: Task definition
            result: Task execution result
        
        Returns:
            Memory entry ID if written, None otherwise
        """
        if not MEMORY_AVAILABLE:
            return None
        
        # Only write memory for significant tasks
        task_type = task.get('type', 'unknown')
        is_significant = task.get('importance', 'low') in ['medium', 'high', 'critical']
        
        if not is_significant:
            print("ℹ️  Task not significant enough for memory entry")
            return None
        
        try:
            entry_id = write_memory({
                'scope': self.task_scope,
                'title': f"{self.agent_name}: {task.get('title', 'Task Completed')}",
                'summary': f"Completed {task_type} task: {task.get('summary', 'No summary')}",
                'importance': 'low',
                'tags': [task_type, 'task', 'completion', self.agent_name],
                'details': {
                    'agent': self.agent_name,
                    'task_id': task.get('id', 'unknown'),
                    'status': result.get('status', 'unknown')
                }
            })
            
            print(f"✓ Wrote completion memory: {entry_id}")
            return entry_id
        
        except Exception as e:
            print(f"WARNING: Could not write completion memory: {e}")
            return None


def demo_usage():
    """Demonstrate agent usage with memory integration."""
    print("\n" + "="*60)
    print("Python Agent Core - Memory Integration Demo")
    print("="*60 + "\n")
    
    # Create agent
    agent = AgentCore(
        agent_name="schema-builder",
        task_scope="isms"
    )
    
    # Define a sample task
    sample_task = {
        'id': 'task-001',
        'type': 'schema',
        'title': 'Create Asset table schema',
        'summary': 'Define database schema for Asset module',
        'importance': 'high',
        'description': 'Create comprehensive schema with all required fields'
    }
    
    # Execute task
    result = agent.execute_task(sample_task)
    
    print("\n" + "="*60)
    print(f"Result: {result['status']}")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_usage()
