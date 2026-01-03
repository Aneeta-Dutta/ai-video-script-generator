"""
Enhanced Orchestrator Base Class with Observability.

Provides base functionality for orchestrators with integrated
logging, metrics, error tracking, and reporting.
"""

import asyncio
from typing import Optional, Any
from contextlib import asynccontextmanager

from backend.core import get_logger
from backend.core.logging import (
    get_metrics,
    get_error_tracker,
    ErrorCategory,
    ErrorSeverity,
)
from backend.orchestration.session_manager import SessionManager, SessionStatus


class ObservableOrchestrator:
    """Base class for orchestrators with full observability."""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(__name__, agent_name=name)
        self.metrics = get_metrics()
        self.error_tracker = get_error_tracker()
        self.session_manager = SessionManager()

    @asynccontextmanager
    async def track_execution(
        self, operation_name: str, session_id: Optional[str] = None
    ):
        """
        Context manager for tracking operation execution with metrics and errors.

        Args:
            operation_name: Name of the operation
            session_id: Optional session ID

        Yields:
            None

        Example:
            async with self.track_execution("agent_call", session_id):
                result = await some_async_operation()
        """
        timer_name = f"{self.name}_{operation_name}"
        self.metrics.start_timer(timer_name)

        try:
            self.logger.info(f"Starting {operation_name}", session_id=session_id)
            yield

            duration = self.metrics.stop_timer(
                timer_name, labels={"operation": operation_name}
            )
            self.logger.info(
                f"Completed {operation_name} in {duration:.2f}ms",
                session_id=session_id,
                duration=duration,
            )

        except Exception as e:
            duration = self.metrics.stop_timer(
                timer_name, labels={"operation": operation_name, "error": str(e)}
            )

            # Track error
            error_record = self.error_tracker.track_error(
                e,
                category=self._categorize_error(e),
                severity=self._determine_severity(e),
                context={"operation": operation_name, "orchestrator": self.name},
                session_id=session_id,
            )

            self.logger.error(
                f"Failed {operation_name}: {str(e)} (Error ID: {error_record.error_id})",
                session_id=session_id,
                duration=duration,
            )

            raise

    def _categorize_error(self, exception: Exception) -> ErrorCategory:
        """
        Categorize an exception.

        Args:
            exception: The exception to categorize

        Returns:
            Error category
        """
        error_type = type(exception).__name__

        # API/Network errors
        if (
            "Connection" in error_type
            or "Timeout" in error_type
            or "Network" in error_type
        ):
            return ErrorCategory.NETWORK

        # File I/O errors
        if isinstance(exception, (FileNotFoundError, IOError, OSError)):
            return ErrorCategory.FILE_IO

        # Validation errors
        if isinstance(exception, (ValueError, TypeError, KeyError)):
            return ErrorCategory.VALIDATION

        # Configuration errors
        if isinstance(exception, (AttributeError, ImportError)):
            return ErrorCategory.CONFIGURATION

        # Timeout errors
        if "Timeout" in error_type:
            return ErrorCategory.TIMEOUT

        # Default
        return ErrorCategory.AGENT_EXECUTION

    def _determine_severity(self, exception: Exception) -> ErrorSeverity:
        """
        Determine severity of an exception.

        Args:
            exception: The exception

        Returns:
            Error severity
        """
        # Critical errors
        if isinstance(exception, (SystemError, MemoryError)):
            return ErrorSeverity.CRITICAL

        # High severity
        if isinstance(exception, (RuntimeError, ConnectionError)):
            return ErrorSeverity.HIGH

        # Medium severity (default for most)
        if isinstance(exception, (ValueError, TypeError, KeyError)):
            return ErrorSeverity.MEDIUM

        # Low severity
        if isinstance(exception, (FileNotFoundError, Warning)):
            return ErrorSeverity.LOW

        return ErrorSeverity.MEDIUM

    def record_metric(self, metric_name: str, value: float, **labels):
        """
        Record a metric with labels.

        Args:
            metric_name: Name of the metric
            value: Metric value
            **labels: Labels for categorization
        """
        full_metric_name = f"{self.name}_{metric_name}"
        self.metrics.record(full_metric_name, value, labels)

        self.logger.debug(f"Recorded metric: {full_metric_name}={value}")
