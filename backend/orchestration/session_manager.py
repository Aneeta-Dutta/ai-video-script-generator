"""
Session Management for AI Video Production System.

Provides session tracking, state management, and execution history
for both research and production workflows.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from pathlib import Path

from backend.core import get_settings
from backend.core.utils import save_json_file, load_json_file


class SessionStatus(Enum):
    """Session status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowType(Enum):
    """Workflow type enumeration."""

    RESEARCH = "research"
    PRODUCTION = "production"
    E2E = "end_to_end"


@dataclass
class AgentExecution:
    """Record of a single agent execution."""

    agent_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "running"
    output: Optional[str] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None


@dataclass
class Session:
    """Session tracking for a workflow execution."""

    session_id: str
    workflow_type: WorkflowType
    topic: str
    started_at: datetime
    status: SessionStatus = SessionStatus.PENDING
    completed_at: Optional[datetime] = None
    agent_executions: List[AgentExecution] = field(default_factory=list)
    final_output: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate total session duration in seconds."""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> dict:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "workflow_type": self.workflow_type.value,
            "topic": self.topic,
            "started_at": self.started_at.isoformat(),
            "status": self.status.value,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "agent_executions": [
                {
                    "agent_name": ae.agent_name,
                    "started_at": ae.started_at.isoformat(),
                    "completed_at": (
                        ae.completed_at.isoformat() if ae.completed_at else None
                    ),
                    "status": ae.status,
                    "output": ae.output,
                    "error": ae.error,
                    "duration_ms": ae.duration_ms,
                }
                for ae in self.agent_executions
            ],
            "final_output": self.final_output,
            "error_message": self.error_message,
            "duration_seconds": self.duration_seconds,
            "metadata": self.metadata,
        }


class SessionManager:
    """Manages sessions for workflow executions."""

    def __init__(self):
        self.settings = get_settings()
        self.sessions: Dict[str, Session] = {}
        self._ensure_session_dir()

    def _ensure_session_dir(self):
        """Ensure session storage directory exists."""
        session_dir = self.settings.paths.outputs_dir / "sessions"
        session_dir.mkdir(parents=True, exist_ok=True)

    def create_session(
        self,
        workflow_type: WorkflowType,
        topic: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """
        Create a new session.

        Args:
            workflow_type: Type of workflow (research, production, e2e)
            topic: Topic or scene concept
            metadata: Optional metadata

        Returns:
            Created session instance
        """
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            workflow_type=workflow_type,
            topic=topic,
            started_at=datetime.now(),
            metadata=metadata or {},
        )

        self.sessions[session_id] = session
        return session

    def update_session_status(self, session_id: str, status: SessionStatus):
        """Update session status."""
        if session_id in self.sessions:
            self.sessions[session_id].status = status
            if status in [
                SessionStatus.COMPLETED,
                SessionStatus.FAILED,
                SessionStatus.CANCELLED,
            ]:
                self.sessions[session_id].completed_at = datetime.now()

    def add_agent_execution(self, session_id: str, agent_name: str) -> AgentExecution:
        """Start tracking an agent execution."""
        execution = AgentExecution(agent_name=agent_name, started_at=datetime.now())

        if session_id in self.sessions:
            self.sessions[session_id].agent_executions.append(execution)

        return execution

    def complete_agent_execution(
        self,
        session_id: str,
        agent_name: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
    ):
        """Complete an agent execution."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            for execution in reversed(session.agent_executions):
                if execution.agent_name == agent_name and execution.status == "running":
                    execution.completed_at = datetime.now()
                    execution.status = "completed" if not error else "failed"
                    execution.output = output
                    execution.error = error

                    if execution.completed_at:
                        duration = (
                            execution.completed_at - execution.started_at
                        ).total_seconds() * 1000
                        execution.duration_ms = duration
                    break

    def set_final_output(self, session_id: str, output: str):
        """Set the final output for a session."""
        if session_id in self.sessions:
            self.sessions[session_id].final_output = output

    def set_error(self, session_id: str, error: str):
        """Set error message for a session."""
        if session_id in self.sessions:
            self.sessions[session_id].error_message = error
            self.sessions[session_id].status = SessionStatus.FAILED
            self.sessions[session_id].completed_at = datetime.now()

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return self.sessions.get(session_id)

    def save_session(self, session_id: str):
        """Persist session to disk."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session_file = (
                self.settings.paths.outputs_dir / "sessions" / f"{session_id}.json"
            )
            save_json_file(session.to_dict(), session_file)

    def load_session(self, session_id: str) -> Optional[Session]:
        """Load session from disk."""
        session_file = (
            self.settings.paths.outputs_dir / "sessions" / f"{session_id}.json"
        )
        if session_file.exists():
            data = load_json_file(session_file)
            # Reconstruct session (simplified - full reconstruction would need more logic)
            return Session(
                session_id=data["session_id"],
                workflow_type=WorkflowType(data["workflow_type"]),
                topic=data["topic"],
                started_at=datetime.fromisoformat(data["started_at"]),
                status=SessionStatus(data["status"]),
                completed_at=(
                    datetime.fromisoformat(data["completed_at"])
                    if data["completed_at"]
                    else None
                ),
                final_output=data["final_output"],
                error_message=data["error_message"],
                metadata=data["metadata"],
            )
        return None
