"""Build State Manager - Stub implementation"""


class BuildStateManager:
    """Stub class for managing build state"""
    
    def start_build(self, task_id, module, builder):
        """
        Start a build.
        
        Args:
            task_id: Task identifier
            module: Module name
            builder: Builder type
        """
        pass
    
    def get_state(self):
        """Get current build state"""
        return {"status": "not_started"}
    
    def update_state(self, state):
        """Update build state"""
        pass

