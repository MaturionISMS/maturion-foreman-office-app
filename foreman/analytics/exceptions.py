"""
Analytics exceptions for proper error handling.

QA Coverage: QA-136, QA-141, QA-146 (failure modes)
"""

class AnalyticsException(Exception):
    """Base exception for analytics subsystem."""
    pass

class DataLoadError(AnalyticsException):
    """Raised when data cannot be loaded."""
    pass

class CalculationError(AnalyticsException):
    """Raised when metric calculation fails."""
    pass

class CalculationOverflowError(CalculationError):
    """Raised when calculation results in overflow."""
    pass

class DataCorruptionError(AnalyticsException):
    """Raised when data corruption is detected."""
    
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}

class TokenCountingError(AnalyticsException):
    """Raised when token counting fails."""
    pass

class CostCalculationError(AnalyticsException):
    """Raised when cost calculation fails."""
    pass
