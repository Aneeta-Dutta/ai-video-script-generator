"""
Research Orchestrator for AI Video Production System.

Coordinates research agents and manages the research workflow.
"""

import asyncio
from typing import Optional
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.core import get_settings, get_logger
from backend.core.utils import save_text_file, sanitize_filename
from backend.agents.research_agents import lead_investigator_agent
from backend.orchestration.session_manager import (
    SessionManager,
    WorkflowType,
    SessionStatus,
)
from backend.orchestration.quality_evaluator import QualityEvaluator


logger = get_logger(__name__)


class ResearchOrchestrator:
    """Orchestrates the research workflow."""

    def __init__(self):
        self.settings = get_settings()
        self.session_manager = SessionManager()
        self.quality_evaluator = QualityEvaluator()
        self.logger = get_logger(__name__, agent_name="ResearchOrchestrator")

    async def execute_research(
        self, topic: str, save_output: bool = True
    ) -> tuple[str, Optional[str]]:
        """
        Execute research workflow for a given topic.

        Args:
            topic: Research topic
            save_output: Whether to save output to file

        Returns:
            Tuple of (report_content, session_id)
        """
        # Create session
        session = self.session_manager.create_session(
            workflow_type=WorkflowType.RESEARCH, topic=topic
        )
        session_id = session.session_id

        self.logger.info(f"Starting research for topic: {topic}", session_id=session_id)

        try:
            # Update session status
            self.session_manager.update_session_status(
                session_id, SessionStatus.RUNNING
            )

            # Initialize ADK Runner
            session_service = InMemorySessionService()
            runner = Runner(
                agent=lead_investigator_agent,
                session_service=session_service,
                app_name="research_agency",
            )

            # Create ADK session
            await session_service.create_session(
                user_id="user_01",
                session_id=f"adk_session_{session_id}",
                app_name="research_agency",
            )

            # Prepare input
            input_content = types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=f"Activate Research Swarm. Topic: {topic}. Deploy all agents."
                    )
                ],
            )

            # Track agent execution
            agent_exec = self.session_manager.add_agent_execution(
                session_id, "lead_investigator"
            )

            # Run research
            report_content = ""
            async for event in runner.run_async(
                user_id="user_01",
                session_id=f"adk_session_{session_id}",
                new_message=input_content,
            ):
                # Collect text output from event.content.parts (ADK Event shape)
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            report_content += part.text

            # Complete agent execution
            self.session_manager.complete_agent_execution(
                session_id,
                "lead_investigator",
                output=report_content[:500],  # Store truncated output
            )

            # Evaluate quality
            quality_report = self.quality_evaluator.evaluate_research_report(
                report_content
            )
            self.logger.info(
                f"Research quality: {quality_report.overall_level.value} (score: {quality_report.overall_score:.2f})",
                session_id=session_id,
            )

            # Handle empty or poor quality output
            if not quality_report.passed:
                self.logger.warning(
                    f"Research output quality below threshold. Recommendations: {quality_report.recommendations}",
                    session_id=session_id,
                )

            # Save output if requested
            if save_output:
                output_path = self._save_research_report(
                    topic, report_content, session_id
                )
                self.logger.info(
                    f"Research report saved to: {output_path}", session_id=session_id
                )

            # Update session
            self.session_manager.set_final_output(session_id, report_content)
            self.session_manager.update_session_status(
                session_id, SessionStatus.COMPLETED
            )
            self.session_manager.save_session(session_id)

            return report_content, session_id

        except Exception as e:
            self.logger.error(
                f"Research execution failed: {str(e)}", session_id=session_id
            )
            self.session_manager.set_error(session_id, str(e))
            self.session_manager.save_session(session_id)
            raise

    def _save_research_report(self, topic: str, content: str, session_id: str) -> Path:
        """Save research report to file."""
        # Sanitize topic for filename
        safe_topic = sanitize_filename(topic)
        filename = f"{safe_topic}_{session_id[:8]}.md"

        output_path = self.settings.paths.research_reports_dir / filename
        save_text_file(content, output_path)

        return output_path
