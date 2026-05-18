"""
Production Orchestrator for AI Video Production System.

Coordinates production agents and manages the production workflow.
"""

import asyncio
from typing import Optional
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.core import get_settings, get_logger
from backend.core.utils import save_text_file, sanitize_filename
from backend.agents.production_agents import executive_producer_agent
from backend.orchestration.session_manager import (
    SessionManager,
    WorkflowType,
    SessionStatus,
)
from backend.orchestration.quality_evaluator import QualityEvaluator


logger = get_logger(__name__)


class ProductionOrchestrator:
    """Orchestrates the production workflow."""

    def __init__(self):
        self.settings = get_settings()
        self.session_manager = SessionManager()
        self.quality_evaluator = QualityEvaluator()
        self.logger = get_logger(__name__, agent_name="ProductionOrchestrator")

    async def execute_production(
        self, scene_concept: str, save_output: bool = True
    ) -> tuple[str, Optional[str]]:
        """
        Execute production workflow for a given scene concept.

        Args:
            scene_concept: Scene concept or description
            save_output: Whether to save output to file

        Returns:
            Tuple of (script_content, session_id)
        """
        # Create session
        session = self.session_manager.create_session(
            workflow_type=WorkflowType.PRODUCTION, topic=scene_concept
        )
        session_id = session.session_id

        self.logger.info(
            f"Starting production for concept: {scene_concept[:100]}...",
            session_id=session_id,
        )

        try:
            # Update session status
            self.session_manager.update_session_status(
                session_id, SessionStatus.RUNNING
            )

            # Initialize ADK Runner
            session_service = InMemorySessionService()
            runner = Runner(
                agent=executive_producer_agent,
                session_service=session_service,
                app_name="production_agency",
            )

            # Create ADK session
            await session_service.create_session(
                user_id="user_01",
                session_id=f"adk_session_{session_id}",
                app_name="production_agency",
            )

            # Prepare input
            input_content = types.Content(
                role="user",
                parts=[types.Part(text=f"Create shooting script for: {scene_concept}")],
            )

            # Track agent execution
            agent_exec = self.session_manager.add_agent_execution(
                session_id, "executive_producer"
            )

            # Run production
            script_content = ""
            async for event in runner.run_async(
                user_id="user_01",
                session_id=f"adk_session_{session_id}",
                new_message=input_content,
            ):
                # Collect text output from event.content.parts (ADK Event shape)
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            script_content += part.text

            # Complete agent execution
            self.session_manager.complete_agent_execution(
                session_id,
                "executive_producer",
                output=script_content[:500],  # Store truncated output
            )

            # Evaluate quality
            quality_report = self.quality_evaluator.evaluate_production_script(
                script_content
            )
            self.logger.info(
                f"Production quality: {quality_report.overall_level.value} (score: {quality_report.overall_score:.2f})",
                session_id=session_id,
            )

            # Handle empty or poor quality output
            if not quality_report.passed:
                self.logger.warning(
                    f"Production output quality below threshold. Recommendations: {quality_report.recommendations}",
                    session_id=session_id,
                )

            # Save output if requested
            if save_output:
                output_path = self._save_production_script(
                    scene_concept, script_content, session_id
                )
                self.logger.info(
                    f"Production script saved to: {output_path}", session_id=session_id
                )

            # Update session
            self.session_manager.set_final_output(session_id, script_content)
            self.session_manager.update_session_status(
                session_id, SessionStatus.COMPLETED
            )
            self.session_manager.save_session(session_id)

            return script_content, session_id

        except Exception as e:
            self.logger.error(
                f"Production execution failed: {str(e)}", session_id=session_id
            )
            self.session_manager.set_error(session_id, str(e))
            self.session_manager.save_session(session_id)
            raise

    def _save_production_script(
        self, concept: str, content: str, session_id: str
    ) -> Path:
        """Save production script to file."""
        # Sanitize concept for filename
        safe_concept = sanitize_filename(concept[:50])
        filename = f"{safe_concept}_{session_id[:8]}.md"

        output_path = self.settings.paths.production_scripts_dir / filename
        save_text_file(content, output_path)

        return output_path
