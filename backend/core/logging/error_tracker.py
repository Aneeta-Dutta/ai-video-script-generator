"""
Error Tracking and Categorization for AI Video Production System.

Provides detailed error tracking, categorization, and analysis
with stack trace capture and error pattern detection.
"""

import sys
import traceback
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict
import json
from pathlib import Path

from backend.core.config import get_settings


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    AGENT_EXECUTION = "agent_execution"
    API_CALL = "api_call"
    FILE_IO = "file_io"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class ErrorRecord:
    """Detailed error record."""
    error_id: str
    timestamp: datetime
    category: ErrorCategory
    severity: ErrorSeverity
    error_type: str
    error_message: str
    stack_trace: str
    context: Dict[str, Any] = field(default_factory=dict)
    agent_name: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category.value,
            "severity": self.severity.value,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "stack_trace": self.stack_trace,
            "context": self.context,
            "agent_name": self.agent_name,
            "session_id": self.session_id
        }


class ErrorTracker:
    """Tracks and analyzes errors across the system."""
    
    def __init__(self):
        self.settings = get_settings()
        self.errors: List[ErrorRecord] = []
        self.error_counts: Dict[str, int] = defaultdict(int)
        self._error_counter = 0
    
    def track_error(
        self,
        exception: Exception,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> ErrorRecord:
        """
        Track an error with full context.
        
        Args:
            exception: The exception that occurred
            category: Error category
            severity: Error severity
            context: Additional context information
            agent_name: Name of agent where error occurred
            session_id: Session ID if applicable
        
        Returns:
            Created error record
        """
        self._error_counter += 1
        error_id = f"ERR_{self._error_counter:06d}"
        
        # Capture stack trace
        exc_type, exc_value, exc_tb = sys.exc_info()
        stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        
        # Create error record
        error_record = ErrorRecord(
            error_id=error_id,
            timestamp=datetime.now(),
            category=category,
            severity=severity,
            error_type=type(exception).__name__,
            error_message=str(exception),
            stack_trace=stack_trace,
            context=context or {},
            agent_name=agent_name,
            session_id=session_id
        )
        
        self.errors.append(error_record)
        
        # Update error counts
        count_key = f"{category.value}:{error_record.error_type}"
        self.error_counts[count_key] += 1
        
        return error_record
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorRecord]:
        """Get all errors for a specific category."""
        return [e for e in self.errors if e.category == category]
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorRecord]:
        """Get all errors of a specific severity."""
        return [e for e in self.errors if e.severity == severity]
    
    def get_errors_by_agent(self, agent_name: str) -> List[ErrorRecord]:
        """Get all errors for a specific agent."""
        return [e for e in self.errors if e.agent_name == agent_name]
    
    def get_errors_by_session(self, session_id: str) -> List[ErrorRecord]:
        """Get all errors for a specific session."""
        return [e for e in self.errors if e.session_id == session_id]
    
    def get_recent_errors(self, limit: int = 10) -> List[ErrorRecord]:
        """Get most recent errors."""
        return self.errors[-limit:]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of all errors.
        
        Returns:
            Dictionary with error statistics
        """
        if not self.errors:
            return {
                "total_errors": 0,
                "by_category": {},
                "by_severity": {},
                "by_type": {},
                "recent_errors": []
            }
        
        # Count by category
        by_category = defaultdict(int)
        for error in self.errors:
            by_category[error.category.value] += 1
        
        # Count by severity
        by_severity = defaultdict(int)
        for error in self.errors:
            by_severity[error.severity.value] += 1
        
        # Count by type
        by_type = defaultdict(int)
        for error in self.errors:
            by_type[error.error_type] += 1
        
        return {
            "total_errors": len(self.errors),
            "by_category": dict(by_category),
            "by_severity": dict(by_severity),
            "by_type": dict(by_type),
            "most_common_errors": sorted(
                by_type.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "recent_errors": [e.to_dict() for e in self.get_recent_errors(5)]
        }
    
    def export_errors(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Export all errors to JSON.
        
        Args:
            output_path: Optional path to save errors
        
        Returns:
            Dictionary of all errors
        """
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "summary": self.get_error_summary(),
            "errors": [e.to_dict() for e in self.errors]
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
    
    def clear(self):
        """Clear all error records."""
        self.errors.clear()
        self.error_counts.clear()
        self._error_counter = 0


# Global error tracker instance
_error_tracker_instance: Optional[ErrorTracker] = None


def get_error_tracker() -> ErrorTracker:
    """Get or create global error tracker instance."""
    global _error_tracker_instance
    if _error_tracker_instance is None:
        _error_tracker_instance = ErrorTracker()
    return _error_tracker_instance


def track_error(
    exception: Exception,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    **kwargs
) -> ErrorRecord:
    """
    Convenience function to track an error.
    
    Args:
        exception: The exception
        category: Error category
        severity: Error severity
        **kwargs: Additional context
    
    Returns:
        Error record
    """
    tracker = get_error_tracker()
    return tracker.track_error(exception, category, severity, context=kwargs)
