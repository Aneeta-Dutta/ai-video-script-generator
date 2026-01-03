"""
Direct Sequential Research Orchestrator - CORRECTED VERSION.

Uses Runner.run_async for each individual agent without relying on sub-agent delegation.
"""

import asyncio
from typing import Optional
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.core import get_settings, get_logger
from backend.core.utils import save_text_file, sanitize_filename
from backend.orchestration.session_manager import (
    SessionManager,
    WorkflowType,
    SessionStatus,
)
from backend.orchestration.quality_evaluator import QualityEvaluator

# Import all research sub-agents directly
from backend.agents.research_agents.data_miner import data_miner_agent
from backend.agents.research_agents.grassroots_voice import grassroots_voice_agent
from backend.agents.research_agents.historian import historian_agent
from backend.agents.research_agents.trend_scout import trend_scout_agent
from backend.agents.research_agents.narrative_architect import narrative_architect_agent


logger = get_logger(__name__)


class DirectResearchOrchestrator:
    """Orchestrates research workflow with direct sequential execution."""

    def __init__(self):
        self.settings = get_settings()
        self.session_manager = SessionManager()
        self.quality_evaluator = QualityEvaluator()
        self.logger = get_logger(__name__, agent_name="DirectResearchOrchestrator")

        # Define sub-agents in execution order
        self.sub_agents = [
            ("data_miner", data_miner_agent, "Statistical evidence and data analysis"),
            (
                "grassroots_voice",
                grassroots_voice_agent,
                "Ground-level perspectives and testimonies",
            ),
            ("historian", historian_agent, "Historical context and precedents"),
            ("trend_scout", trend_scout_agent, "Current trends and patterns"),
            (
                "narrative_architect",
                narrative_architect_agent,
                "Story synthesis and narrative structure",
            ),
        ]

    async def execute_research(
        self, topic: str, save_output: bool = True
    ) -> tuple[str, Optional[str]]:
        """
        Execute research workflow by calling each sub-agent directly.

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

        self.logger.info(
            f"Starting direct sequential research for: {topic}", session_id=session_id
        )

        try:
            # Update session status
            self.session_manager.update_session_status(
                session_id, SessionStatus.RUNNING
            )

            # Collect results from all sub-agents
            sub_agent_results = {}

            # Execute each sub-agent sequentially
            for agent_name, agent, description in self.sub_agents:
                self.logger.info(
                    f"Executing {agent_name}: {description}", session_id=session_id
                )

                # Track execution
                agent_exec = self.session_manager.add_agent_execution(
                    session_id, agent_name
                )

                try:
                    # Use direct Gemini API instead of ADK Runner
                    from google.genai import Client

                    if self.settings.api.use_vertex_ai:
                        client = Client(
                            vertexai=True,
                            project=self.settings.api.gcp_project,
                            location=self.settings.api.gcp_location,
                        )
                    else:
                        client = Client(api_key=self.settings.api.google_api_key)

                    # Create input for this agent
                    prompt = f"""Research Topic: {topic}

Your Task: {description}

Agent Instruction: {agent.instruction}

**PRODUCTION HOUSE PROTOCOL: CRISP & PRECISE**
Deliver only high-priority, fact-based findings.
Limit your response to maximum 10 bullet points or 15 sentences. 
Absolutely no conversational filler."""

                    # Execute agent using direct API
                    response = client.models.generate_content(
                        model=agent.model or self.settings.model.default_model,
                        contents=prompt,
                    )

                    agent_output = response.text or ""

                    # Hard truncate if agent is too verbose
                    agent_output = "\n".join(agent_output.split("\n")[:30])

                    sub_agent_results[agent_name] = agent_output

                    self.logger.info(
                        f"✓ {agent_name} completed: {len(agent_output)} chars",
                        session_id=session_id,
                    )

                    # Complete agent execution tracking
                    self.session_manager.complete_agent_execution(
                        session_id, agent_name, output=agent_output[:500]
                    )

                except Exception as e:
                    self.logger.error(
                        f"✗ {agent_name} failed: {str(e)}", session_id=session_id
                    )
                    sub_agent_results[agent_name] = f"[Error: {str(e)}]"
                    self.session_manager.complete_agent_execution(
                        session_id, agent_name, error=str(e)
                    )

            # Synthesize final report
            report_content = self._synthesize_report(topic, sub_agent_results)

            self.logger.info(
                f"Research synthesis complete: {len(report_content)} chars",
                session_id=session_id,
            )

            # Evaluate quality
            quality_report = self.quality_evaluator.evaluate_research_report(
                report_content
            )
            self.logger.info(
                f"Research quality: {quality_report.overall_level.value} (score: {quality_report.overall_score:.2f})",
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

    def _synthesize_report(self, topic: str, results: dict) -> str:
        """Synthesize individual agent results into comprehensive report."""
        report_parts = [
            f"# Research Report: {topic}\n",
            f"*Generated using multi-agent research system*\n\n",
            "---\n\n",
        ]

        # Data & Statistics
        if results.get("data_miner"):
            report_parts.append("## 📊 Data & Statistical Analysis\n\n")
            report_parts.append(results["data_miner"])
            report_parts.append("\n\n---\n\n")

        # Grassroots Perspectives
        if results.get("grassroots_voice"):
            report_parts.append("## 🗣️ Ground-Level Perspectives\n\n")
            report_parts.append(results["grassroots_voice"])
            report_parts.append("\n\n---\n\n")

        # Historical Context
        if results.get("historian"):
            report_parts.append("## 📜 Historical Context\n\n")
            report_parts.append(results["historian"])
            report_parts.append("\n\n---\n\n")

        # Current Trends
        if results.get("trend_scout"):
            report_parts.append("## 📈 Current Trends & Patterns\n\n")
            report_parts.append(results["trend_scout"])
            report_parts.append("\n\n---\n\n")

        # Narrative Synthesis
        if results.get("narrative_architect"):
            report_parts.append("## 🎬 Narrative Structure & Story Arc\n\n")
            report_parts.append(results["narrative_architect"])
            report_parts.append("\n\n")

        return "".join(report_parts)

    def _save_research_report(self, topic: str, content: str, session_id: str) -> Path:
        """Save research report to file."""
        safe_topic = sanitize_filename(topic)
        filename = f"{safe_topic}_{session_id[:8]}.md"

        output_path = self.settings.paths.research_reports_dir / filename
        save_text_file(content, output_path)

        return output_path
