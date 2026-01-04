"""Memory Manager Exceptions. QA-152"""


class MemoryException(Exception):
    """Base memory exception."""
    pass


class FabricCorruptionError(MemoryException):
    """Fabric corruption detected."""
    pass


class ProposalRejectedError(MemoryException):
    """Proposal was rejected."""
    
    def __init__(self, message, reason=None):
        super().__init__(message)
        self.reason = reason
