"""
Execution Reporter for AI Video Production System.

Generates comprehensive execution reports with metrics, errors,
and detailed analysis of workflow performance.
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json

from backend.core.config import get_settings
from backend.core.logging.metrics import get_metrics, MetricStats
from backend.core.logging.error_tracker import get_error_tracker, ErrorSeverity

if TYPE_CHECKING:
    from backend.orchestration.session_manager import Session, SessionStatus


@dataclass
class ExecutionSummary:
    """Summary of an execution."""

    session_id: str
    workflow_type: str
    topic: str
    status: str
    duration_seconds: Optional[float]
    agent_count: int
    error_count: int
    quality_score: Optional[float] = None


class ExecutionReporter:
    """Generates detailed execution reports."""

    def __init__(self):
        self.settings = get_settings()
        self.metrics = get_metrics()
        self.error_tracker = get_error_tracker()

    def generate_session_report(
        self,
        session: "Session",
        include_metrics: bool = True,
        include_errors: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate a detailed report for a session.

        Args:
            session: Session to report on
            include_metrics: Include performance metrics
            include_errors: Include error details

        Returns:
            Comprehensive session report
        """
        # Import here to avoid circular dependency
        from backend.orchestration.session_manager import SessionStatus

        report = {
            "session_id": session.session_id,
            "workflow_type": session.workflow_type.value,
            "topic": session.topic,
            "status": session.status.value,
            "started_at": session.started_at.isoformat(),
            "completed_at": (
                session.completed_at.isoformat() if session.completed_at else None
            ),
            "duration_seconds": session.duration_seconds,
            "metadata": session.metadata,
        }

        # Agent executions
        report["agent_executions"] = []
        for agent_exec in session.agent_executions:
            report["agent_executions"].append(
                {
                    "agent_name": agent_exec.agent_name,
                    "started_at": agent_exec.started_at.isoformat(),
                    "completed_at": (
                        agent_exec.completed_at.isoformat()
                        if agent_exec.completed_at
                        else None
                    ),
                    "status": agent_exec.status,
                    "duration_ms": agent_exec.duration_ms,
                    "output_preview": (
                        agent_exec.output[:200] if agent_exec.output else None
                    ),
                    "error": agent_exec.error,
                }
            )

        # Output summary
        if session.final_output:
            report["output_summary"] = {
                "length": len(session.final_output),
                "preview": (
                    session.final_output[:500] + "..."
                    if len(session.final_output) > 500
                    else session.final_output
                ),
            }

        # Metrics
        if include_metrics:
            report["performance_metrics"] = self._get_session_metrics(
                session.session_id
            )

        # Errors
        if include_errors:
            session_errors = self.error_tracker.get_errors_by_session(
                session.session_id
            )
            report["errors"] = {
                "count": len(session_errors),
                "by_severity": self._count_errors_by_severity(session_errors),
                "details": [e.to_dict() for e in session_errors],
            }

        return report

    def generate_summary_report(self, sessions: List["Session"]) -> Dict[str, Any]:
        """
        Generate a summary report across multiple sessions.

        Args:
            sessions: List of sessions to summarize

        Returns:
            Summary report
        """
        from backend.orchestration.session_manager import SessionStatus

        if not sessions:
            return {
                "total_sessions": 0,
                "successful_sessions": 0,
                "failed_sessions": 0,
                "average_duration_seconds": 0,
            }

        successful = [s for s in sessions if s.status == SessionStatus.COMPLETED]
        failed = [s for s in sessions if s.status == SessionStatus.FAILED]

        durations = [s.duration_seconds for s in sessions if s.duration_seconds]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_sessions": len(sessions),
            "successful_sessions": len(successful),
            "failed_sessions": len(failed),
            "success_rate": len(successful) / len(sessions) if sessions else 0,
            "average_duration_seconds": avg_duration,
            "by_workflow_type": self._count_by_workflow_type(sessions),
            "total_errors": sum(
                len(self.error_tracker.get_errors_by_session(s.session_id))
                for s in sessions
            ),
        }

    def generate_performance_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.

        Returns:
            Performance metrics report
        """
        metrics_data = self.metrics.export_metrics()

        report = {
            "generated_at": datetime.now().isoformat(),
            "metrics_summary": {
                "total_metrics": len(self.metrics.metrics),
                "metrics_list": list(self.metrics.metrics.keys()),
            },
            "detailed_metrics": metrics_data["metrics"],
        }

        # Add performance insights
        insights = []

        # Check for slow operations
        for metric_name, data in metrics_data["metrics"].items():
            if "duration_ms" in metric_name and data["stats"]:
                if data["stats"]["mean"] > 5000:  # > 5 seconds
                    insights.append(
                        {
                            "type": "slow_operation",
                            "metric": metric_name,
                            "mean_duration_ms": data["stats"]["mean"],
                            "recommendation": f"Consider optimizing {metric_name.replace('_duration_ms', '')}",
                        }
                    )

        report["performance_insights"] = insights

        return report

    def save_report(
        self, report: Dict[str, Any], report_type: str, identifier: Optional[str] = None
    ) -> Path:
        """
        Save a report to disk.

        Args:
            report: Report data
            report_type: Type of report (session, summary, performance)
            identifier: Optional identifier (e.g., session_id)

        Returns:
            Path to saved report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if identifier:
            filename = f"{report_type}_{identifier}_{timestamp}.json"
        else:
            filename = f"{report_type}_{timestamp}.json"

        reports_dir = self.settings.paths.logs_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_path = reports_dir / filename

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        return report_path

    def _get_session_metrics(self, session_id: str) -> Dict[str, Any]:
        """Get metrics for a specific session."""
        # This is a simplified version - in production, you'd filter metrics by session_id
        return {
            "note": "Session-specific metrics filtering not yet implemented",
            "global_metrics": self.metrics.export_metrics(),
        }

    def _count_errors_by_severity(self, errors: List) -> Dict[str, int]:
        """Count errors by severity."""
        counts = {severity.value: 0 for severity in ErrorSeverity}
        for error in errors:
            counts[error.severity.value] += 1
        return counts

    def _count_by_workflow_type(self, sessions: List["Session"]) -> Dict[str, int]:
        """Count sessions by workflow type."""
        counts = {}
        for session in sessions:
            workflow = session.workflow_type.value
            counts[workflow] = counts.get(workflow, 0) + 1
        return counts


# Global reporter instance
_reporter_instance: Optional[ExecutionReporter] = None


def get_reporter() -> ExecutionReporter:
    """Get or create global reporter instance."""
    global _reporter_instance
    if _reporter_instance is None:
        _reporter_instance = ExecutionReporter()
    return _reporter_instance
