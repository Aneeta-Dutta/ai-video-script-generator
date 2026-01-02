"""
Direct Sequential Production Orchestrator - CORRECTED VERSION.

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
from backend.orchestration.session_manager import SessionManager, WorkflowType, SessionStatus
from backend.orchestration.quality_evaluator import QualityEvaluator

# Import all production sub-agents directly
from backend.agents.production_agents.director import director_agent
from backend.agents.production_agents.dop import dop_agent
from backend.agents.production_agents.designer import designer_agent
from backend.agents.production_agents.colorist import colorist_agent
from backend.agents.production_agents.writer import writer_agent


logger = get_logger(__name__)


class DirectProductionOrchestrator:
    """Orchestrates production workflow with direct sequential execution."""
    
    def __init__(self):
        self.settings = get_settings()
        self.session_manager = SessionManager()
        self.quality_evaluator = QualityEvaluator()
        self.logger = get_logger(__name__, agent_name="DirectProductionOrchestrator")
        
        # Define sub-agents in execution order
        self.sub_agents = [
            ("director", director_agent, "Vision, scale, and emotional truth"),
            ("designer", designer_agent, "Production design and environment"),
            ("dop", dop_agent, "Cinematography, lighting, and camera work"),
            ("colorist", colorist_agent, "Color grading and visual mood"),
            ("writer", writer_agent, "Dialogue and script refinement"),
        ]
    
    async def execute_production(
        self,
        scene_concept: str,
        save_output: bool = True
    ) -> tuple[str, Optional[str]]:
        """
        Execute production workflow by calling each sub-agent directly.
        
        Args:
            scene_concept: Scene concept or description
            save_output: Whether to save output to file
        
        Returns:
            Tuple of (script_content, session_id)
        """
        # Create session
        session = self.session_manager.create_session(
            workflow_type=WorkflowType.PRODUCTION,
            topic=scene_concept
        )
        session_id = session.session_id
        
        self.logger.info(f"Starting direct sequential production for: {scene_concept[:100]}...", session_id=session_id)
        
        try:
            # Update session status
            self.session_manager.update_session_status(session_id, SessionStatus.RUNNING)
            
            # Collect results from all sub-agents
            sub_agent_results = {}
            
            # Execute each sub-agent sequentially
            for agent_name, agent, description in self.sub_agents:
                self.logger.info(f"Executing {agent_name}: {description}", session_id=session_id)
                
                # Track execution
                agent_exec = self.session_manager.add_agent_execution(session_id, agent_name)
                
                try:
                    # Use direct Gemini API instead of ADK Runner
                    from google.genai import Client
                    
                    if self.settings.api.use_vertex_ai:
                        client = Client(
                            vertexai=True, 
                            project=self.settings.api.gcp_project, 
                            location=self.settings.api.gcp_location
                        )
                    else:
                        client = Client(api_key=self.settings.api.google_api_key)

                    # Create input for this agent
                    prompt = f"""Scene Concept: {scene_concept}

Your Task: {description}

Agent Instruction: {agent.instruction}

Provide your creative input for this scene. Be specific and detailed."""
                    
                    # Execute agent using direct API
                    response = client.models.generate_content(
                        model=agent.model or self.settings.model.default_model,
                        contents=prompt
                    )
                    
                    agent_output = response.text or ""
                    
                    sub_agent_results[agent_name] = agent_output
                    
                    self.logger.info(
                        f"✓ {agent_name} completed: {len(agent_output)} chars",
                        session_id=session_id
                    )
                    
                    # Complete agent execution tracking
                    self.session_manager.complete_agent_execution(
                        session_id,
                        agent_name,
                        output=agent_output[:500]
                    )
                    
                except Exception as e:
                    self.logger.error(f"✗ {agent_name} failed: {str(e)}", session_id=session_id)
                    sub_agent_results[agent_name] = f"[Error: {str(e)}]"
                    self.session_manager.complete_agent_execution(
                        session_id,
                        agent_name,
                        error=str(e)
                    )
            
            # Synthesize final shooting script
            script_content = self._synthesize_script(scene_concept, sub_agent_results)
            
            self.logger.info(
                f"Production synthesis complete: {len(script_content)} chars",
                session_id=session_id
            )
            
            # Evaluate quality
            quality_report = self.quality_evaluator.evaluate_production_script(script_content)
            self.logger.info(
                f"Production quality: {quality_report.overall_level.value} (score: {quality_report.overall_score:.2f})",
                session_id=session_id
            )
            
            # Save output if requested
            if save_output:
                output_path = self._save_production_script(scene_concept, script_content, session_id)
                self.logger.info(f"Production script saved to: {output_path}", session_id=session_id)
            
            # Update session
            self.session_manager.set_final_output(session_id, script_content)
            self.session_manager.update_session_status(session_id, SessionStatus.COMPLETED)
            self.session_manager.save_session(session_id)
            
            return script_content, session_id
            
        except Exception as e:
            self.logger.error(f"Production execution failed: {str(e)}", session_id=session_id)
            self.session_manager.set_error(session_id, str(e))
            self.session_manager.save_session(session_id)
            raise
    
    def _synthesize_script(self, concept: str, results: dict) -> str:
        """Synthesize individual agent results into shooting script."""
        script_parts = [
            f"# Shooting Script\n\n",
            f"**Scene Concept:** {concept}\n\n",
            "---\n\n"
        ]
        
        # Director's Vision
        if results.get("director"):
            script_parts.append("## 🎬 Director's Vision\n\n")
            script_parts.append(results["director"])
            script_parts.append("\n\n---\n\n")
        
        # Production Design
        if results.get("designer"):
            script_parts.append("## 🏗️ Production Design\n\n")
            script_parts.append(results["designer"])
            script_parts.append("\n\n---\n\n")
        
        # Cinematography
        if results.get("dop"):
            script_parts.append("## 📹 Cinematography\n\n")
            script_parts.append(results["dop"])
            script_parts.append("\n\n---\n\n")
        
        # Color Grading
        if results.get("colorist"):
            script_parts.append("## 🎨 Color Grading\n\n")
            script_parts.append(results["colorist"])
            script_parts.append("\n\n---\n\n")
        
        # Dialogue & Script
        if results.get("writer"):
            script_parts.append("## ✍️ Dialogue & Script\n\n")
            script_parts.append(results["writer"])
            script_parts.append("\n\n---\n\n")
        
        # Generate VEO Prompt Block
        script_parts.append("## 🎥 VEO 3 PROMPT BLOCK\n\n")
        script_parts.append(self._generate_veo_prompt(concept, results))
        script_parts.append("\n\n")
        
        return "".join(script_parts)
    
    def _generate_veo_prompt(self, concept: str, results: dict) -> str:
        """Generate VEO 3 prompt from combined creative input."""
        # Extract key elements
        subject = concept[:200]
        
        prompt_parts = ["```"]
        prompt_parts.append(f"[SUBJECT] {subject}")
        
        # Add camera specs from DoP if available
        if results.get("dop") and "camera" in results["dop"].lower():
            prompt_parts.append("[CAMERA] 65mm IMAX, wide establishing shot, slow dolly forward")
        else:
            prompt_parts.append("[CAMERA] Cinematic framing, dynamic composition")
        
        # Add lighting from DoP/Designer
        if results.get("dop") and "light" in results["dop"].lower():
            prompt_parts.append("[LIGHTING] Natural lighting, golden hour ambiance")
        else:
            prompt_parts.append("[LIGHTING] Dramatic contrast, volumetric atmosphere")
        
        prompt_parts.append("--style cinematic documentary")
        prompt_parts.append("--aspect 16:9")
        prompt_parts.append("```")
        
        return "\n".join(prompt_parts)
    
    def _save_production_script(self, concept: str, content: str, session_id: str) -> Path:
        """Save production script to file."""
        safe_concept = sanitize_filename(concept[:50])
        filename = f"{safe_concept}_{session_id[:8]}.md"
        
        output_path = self.settings.paths.production_scripts_dir / filename
        save_text_file(content, output_path)
        
        return output_path
