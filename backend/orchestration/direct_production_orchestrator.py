"""
Direct Sequential Production Orchestrator - CORRECTED VERSION.

Uses Runner.run_async for each individual agent without relying on sub-agent delegation.
"""

import asyncio
import json
from datetime import datetime
from typing import Optional, Union, Dict
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.core import get_settings, get_logger
from backend.core.output_manager import get_output_manager
from backend.core.persona_manager import get_persona_manager
from backend.core.utils import save_text_file, sanitize_filename
from backend.orchestration.session_manager import (
    SessionManager,
    WorkflowType,
    SessionStatus,
)
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
        self.output_manager = get_output_manager()
        self.persona_manager = get_persona_manager()
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
        self, scene_concept: str, save_output: bool = True, output_format: str = "json"
    ) -> tuple[Union[str, dict], str]:
        """
        Execute production workflow by calling each sub-agent directly.
        Supports both 'markdown' and 'json' (default) output formats.
        """
        # Create session
        session = self.session_manager.create_session(
            workflow_type=WorkflowType.PRODUCTION, topic=scene_concept
        )
        session_id = session.session_id

        self.logger.info(
            f"🚀 Starting [PROD-HOUSE] Sequential Production: {scene_concept[:100]}...",
            session_id=session_id,
        )

        try:
            # Update session status
            self.session_manager.update_session_status(
                session_id, SessionStatus.RUNNING
            )

            # --- PHASE 1: Sequence Planning (Executive Producer) ---
            self.logger.info(
                "🎬 Planning cinematic sequence (Executive Producer)...",
                session_id=session_id,
            )
            from backend.agents.production_agents.executive_producer import (
                executive_producer_agent,
            )
            from google.genai import Client

            client = Client(
                vertexai=self.settings.api.use_vertex_ai,
                project=(
                    self.settings.api.gcp_project
                    if self.settings.api.use_vertex_ai
                    else None
                ),
                location=(
                    self.settings.api.gcp_location
                    if self.settings.api.use_vertex_ai
                    else None
                ),
                api_key=(
                    None
                    if self.settings.api.use_vertex_ai
                    else self.settings.api.google_api_key
                ),
            )

            plan_prompt = f"Topic & Research: {scene_concept}\n\nTask: {executive_producer_agent.instruction}"
            plan_response = client.models.generate_content(
                model=executive_producer_agent.model
                or self.settings.model.default_model,
                contents=plan_prompt,
            )
            ep_output = plan_response.text or ""

            # Simple parsing of EP output
            creative_brief = ""
            if "### 1. CREATIVE BRIEF" in ep_output:
                creative_brief = (
                    ep_output.split("### 1. CREATIVE BRIEF")[1]
                    .split("### 2. BEAT SHEET")[0]
                    .strip()
                )

            beat_sheet = ""
            if "### 2. BEAT SHEET" in ep_output:
                beat_sheet = ep_output.split("### 2. BEAT SHEET")[1].strip()
            else:
                beat_sheet = ep_output

            beats = [
                b.strip()
                for b in beat_sheet.split("\n")
                if b.strip() and (b.strip()[0].isdigit() or b.strip().startswith("-"))
            ]
            beats = beats[:10]  # Max 10 scenes

            self.logger.info(
                f"✅ Planned {len(beats)} beats for the short movie.",
                session_id=session_id,
            )

            # --- Persona Management ---
            # Extract and save personas from creative brief
            personas_found = []
            try:
                # Look for JSON blocks in ep_output
                import re

                json_blocks = re.findall(
                    r"```json\s*(\{.*?\})\s*```", ep_output, re.DOTALL
                )
                for block in json_blocks:
                    try:
                        p_data = json.loads(block)
                        if "name" in p_data and "role" in p_data:
                            self.persona_manager.save_persona(
                                p_data["name"], p_data["role"], p_data
                            )
                            personas_found.append(p_data["name"])
                            self.logger.info(f"👤 Persona saved: {p_data['name']}")
                    except:
                        continue
            except Exception as e:
                self.logger.warning(f"Failed to parse personas: {str(e)}")

            persona_context = (
                f"\nCHARACTER PERSONAS:\n{self.persona_manager.format_persona_context(personas_found)}"
                if personas_found
                else ""
            )

            # --- PHASE 2: Multi-Scene Execution ---
            all_scenes_data = []
            character_states = {}  # Track visual/emotional states across scenes

            for i, beat in enumerate(beats):
                scene_num = i + 1

                # Extract beat type
                beat_type = "BUILD"
                if "[INTRO]" in beat.upper():
                    beat_type = "INTRO"
                elif "[CLIMAX]" in beat.upper():
                    beat_type = "CLIMAX"
                elif "[OUTRO]" in beat.upper():
                    beat_type = "OUTRO"

                self.logger.info(
                    f"🎥 Executing Scene {scene_num}/{len(beats)} [{beat_type}]: {beat[:50]}...",
                    session_id=session_id,
                )

                # Define cinematic directive based on beat type
                directives = {
                    "INTRO": "FOCUS: World-building, Wide Establising shots, Atmosphere. Mood-setting is priority.",
                    "BUILD": "FOCUS: Narrative progression, Character interaction, Kinetic movement.",
                    "CLIMAX": "FOCUS: High intensity, Tight Close-ups, Dynamic/Fast camera movement, High contrast.",
                    "OUTRO": "FOCUS: Thematic resolution, Lingering shots, Silhouette, Emotional echo.",
                }
                directive = directives.get(beat_type, "")

                sub_agent_results = {}
                for agent_name, agent, description in self.sub_agents:
                    # Create input for this agent
                    context = self._format_context(sub_agent_results)
                    # Include previous scene context for continuity
                    prev_scene_summary = f"\nPREV SCENE: {beats[i-1]}" if i > 0 else ""
                    char_state_context = (
                        f"\nCURRENT CHARACTER PHYSICAL STATES: {character_states}. Ensure visual consistency with these attributes."
                        if character_states
                        else ""
                    )

                    # Dynamic intensity based on beat type
                    intensity_instruction = ""
                    if beat_type == "CLIMAX":
                        intensity_instruction = "\nCLIMAX OVERRIDE: Increase performance_intensity to 0.9-1.0. High stakes, intense delivery."
                    elif beat_type == "INTRO":
                        intensity_instruction = "\nINTRO OVERRIDE: Keep performance_intensity at 0.4-0.6. Subtle, atmospheric, world-building."

                    prompt = f"""MOVIE CREATIVE BRIEF:
{creative_brief}

CINEMATIC DIRECTIVE FOR THIS BEAT:
{directive}
{intensity_instruction}

CURRENT BEAT ({beat_type} - Scene {scene_num}/{len(beats)}):
{beat}
{prev_scene_summary}
{char_state_context}
{persona_context}

Your Task: {description}

Context from previous departments for THIS scene:
{context}

Agent Protocol: {agent.instruction}

Deliver your output for this 8-SECOND BYTE. Be extremely brief."""

                    response = client.models.generate_content(
                        model=agent.model or self.settings.model.default_model,
                        contents=prompt,
                    )

                    agent_output = response.text or ""
                    sub_agent_results[agent_name] = agent_output

                    # Extract character state updates from Director
                    if (
                        agent_name == "director"
                        and "CHARACTER STATE UPDATE:" in agent_output
                    ):
                        try:
                            state_line = [
                                l
                                for l in agent_output.split("\n")
                                if "CHARACTER STATE UPDATE:" in l
                            ][0]
                            new_state = state_line.split("CHARACTER STATE UPDATE:")[
                                1
                            ].strip()
                            # Update character_states dictionary
                            if ":" in new_state:
                                char_name, char_val = new_state.split(":", 1)
                                character_states[char_name.strip()] = char_val.strip()
                            else:
                                character_states["primary"] = new_state

                            self.logger.info(f"🎭 Character State Updated: {new_state}")
                        except Exception as e:
                            self.logger.warning(f"Failed to parse character state: {e}")

                # Synthesize scene data
                scene_json = self._synthesize_scene_json(
                    beat, sub_agent_results, scene_num, len(beats), beat_type=beat_type
                )
                all_scenes_data.append(scene_json)
                self.logger.info(f"   ✓ Scene {scene_num} synthesized.")

            # Final Assembly
            final_json = {
                "project_metadata": {
                    "topic": scene_concept,
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat(),
                    "total_scenes": len(all_scenes_data),
                    "creative_brief": creative_brief,
                },
                "directors_cut": {
                    "music_mood": "Dynamic orchestral hybrid with regional fold elements",
                    "editing_rhythm": "Fast-paced assembly (0.8s cuts) for CLIMAX, slow dissolves for INTRO/OUTRO",
                    "color_grade_master": "Consistency across all scenes using the Teak & Orange palette",
                    "target_duration_total": len(all_scenes_data) * 8,
                },
                "research_summary_crisp": "Structural Cinematic Short Movie optimized for Veo 3.",
                "scenes": all_scenes_data,
            }

            if save_output:
                self.output_manager.save_session_data(f"prod_{session_id}", final_json)

            # Update session
            self.session_manager.set_final_output(session_id, str(final_json)[:1000])
            self.session_manager.update_session_status(
                session_id, SessionStatus.COMPLETED
            )
            self.session_manager.save_session(session_id)

            return final_json, session_id

        except Exception as e:
            self.logger.error(
                f"Production execution failed: {str(e)}", session_id=session_id
            )
            self.session_manager.set_error(session_id, str(e))
            self.session_manager.save_session(session_id)
            raise

    def _format_context(self, results: dict) -> str:
        """Format previous results for the next agent."""
        if not results:
            return "No previous context."
        context = []
        for agent, output in results.items():
            # Only provide the first line (Stack Anchor) to keep context crisp for agents
            first_line = output.split("\n")[0]
            context.append(f"[{agent.upper()} STACK]: {first_line}")
        return "\n".join(context)

    def _synthesize_scene_json(
        self,
        beat: str,
        results: dict,
        scene_num: int,
        total_scenes: int,
        beat_type: str = "BUILD",
    ) -> dict:
        """Synthesize results for a single scene with performance detailing."""
        import re
        import json

        writer_text = results.get("writer", "")
        writer_data = {}

        try:
            clean_json = writer_text.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[-1].split("```")[0]
            writer_data = json.loads(clean_json.strip())
        except:
            # Enhanced fallback for new schema
            def extract_crude(tag, text):
                pattern = rf"{tag}:?\s*(.*?)(?=\n\w+[:_]|$)"
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                return match.group(1).strip() if match else ""

            writer_data = {
                "scene_description_precise": results.get("director", "").split("\n", 1)[
                -1
                ],
                "spoken_dialogue": {
                    "text_bengali": extract_crude("text_bengali", writer_text)
                    or extract_crude("dialogue_bengali", writer_text),
                    "text_english_ref": extract_crude("text_english_ref", writer_text)
                    or extract_crude("dialogue_english_ref", writer_text),
                    "inner_monologue": extract_crude("inner_monologue", writer_text),
                    "lip_sync_notes": extract_crude("lip_sync_notes", writer_text),
                    "gaze_direction": extract_crude("gaze_direction", writer_text),
                    "breath_markers": extract_crude("breath_markers", writer_text),
                    "subtext_internal": extract_crude("subtext_internal", writer_text),
                    "eye_saccade_intensity": 0.0,
                    "accent_variant": "West Bengal Standard",
                    "performance_intensity": 0.8,
                },
                "background_soundscape": {
                    "music_mood": extract_crude("music_mood", writer_text),
                    "reverb_profile": extract_crude("reverb_profile", writer_text),
                    "audio_occlusion_logic": extract_crude("audio_occlusion_logic", writer_text),
                    "ambient_noise": extract_crude("ambient_noise", writer_text),
                    "sfx": extract_crude("sfx", writer_text),
                },
                "speaker_id": extract_crude("speaker_id", writer_text) or "N/A",
                "voice_dna_applied": extract_crude("voice_dna_applied", writer_text)
                or "N/A",
            }

        veo3_stack = self._generate_veo_prompt(
            beat, results, voice_dna=writer_data.get("voice_dna_applied", "")
        )

        # Prune description
        desc_raw = writer_data.get("scene_description_precise", "")
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.!?])\s+", desc_raw)
        desc_pruned = " ".join(sentences[:5])

        return {
            "scene_number": scene_num,
            "scene_type": beat_type,
            "title": beat[:100],
            "scene_description_precise": desc_pruned,
            "duration_seconds": 8,
            "veo3_stack": veo3_stack,
            "hollywood_standard_v1": True,
            "performance_detailing": {
                "speaker_id": writer_data.get("speaker_id", "N/A"),
                "voice_dna": writer_data.get("voice_dna_applied", "N/A"),
                "spoken_dialogue": writer_data.get("spoken_dialogue", {}),
                "background_soundscape": writer_data.get("background_soundscape", {}),
            },
            # Compatibility layer for legacy consumers
            "dialogue_bengali": writer_data.get("spoken_dialogue", {}).get(
                "text_bengali", ""
            ),
            "dialogue_english_ref": writer_data.get("spoken_dialogue", {}).get(
                "text_english_ref", ""
            ),
        }

    def _synthesize_script(self, concept: str, results: dict) -> str:
        """Synthesize individual agent results into shooting script with Veo 3 optimization."""
        script_parts = [
            f"# Shooting Script: Cinema-Grade Production\n\n",
            f"**Scene Concept:** {concept}\n\n",
            "--- \n\n",
            "## 🎬 ULTIMATE VEO 3 PRODUCTION EXPORT\n\n",
            "**[COPY THIS FOR VEO 3]**\n\n",
            "```text\n",
            self._generate_veo_prompt(concept, results),
            "\n```\n\n",
            "---\n\n",
        ]

        # Director's Vision (Subject & Micro-Details)
        if results.get("director"):
            script_parts.append(
                "### 🎥 Layer 1: Subject Anchor & Action Vector (The Nolan Protocol)\n\n"
            )
            script_parts.append(results["director"])
            script_parts.append("\n\n---\n\n")

        # Production Design (Environment & Materiality)
        if results.get("designer"):
            script_parts.append(
                "### 🏗️ Layer 2: The Environment Mesh (Bengal Palette)\n\n"
            )
            script_parts.append(results["designer"])
            script_parts.append("\n\n---\n\n")

        # Cinematography (Lighting & Camera Physics)
        if results.get("dop"):
            script_parts.append(
                "### 📹 Layer 3: The Lighting Engine & Camera Physics\n\n"
            )
            script_parts.append(results["dop"])
            script_parts.append("\n\n---\n\n")

        # Color Grading (Post-Process Stack)
        if results.get("colorist"):
            script_parts.append(
                "### 🎨 Layer 4: The Post-Process Stack (Film Emulation)\n\n"
            )
            script_parts.append(results["colorist"])
            script_parts.append("\n\n---\n\n")

        # Dialogue & Script
        if results.get("writer"):
            script_parts.append("### ✍️ Dialogue & Script Refinement\n\n")
            script_parts.append(results["writer"])
            script_parts.append("\n\n")

        return "".join(script_parts)

    def _generate_veo_prompt(
        self, concept: str, results: dict, voice_dna: str = ""
    ) -> str:
        """Engineer Nolan-Grade Veo 3 prompt using the Stack Method."""

        def clean_line(line):
            """Remove common prefixes and cleaners to extract the core visual phrase."""
            prefixes = [
                "Stack Anchor:",
                "Technical Anchor:",
                "Anchor:",
                "First Line:",
                "Draft:",
                "Script:",
                "Visual Anchor:",
                "Subject:",
                "Subject Anchor:",
                "Scene Anchor:",
                "Character State Update:",
                "Director Note:",
                "Director's Note:",
            ]
            line = line.strip("# *")
            for p in prefixes:
                if line.lower().startswith(p.lower()):
                    line = line[len(p) :].strip()

            # Ensure it's a single phrase and not a full paragraph
            if "." in line:
                line = line.split(".")[0].strip()

            # Limit word count for extreme brevity in the stack
            words = line.split()
            if len(words) > 15:
                line = " ".join(words[:15])

            return line

        # Layer 1: Subject Anchor
        subject_raw = results.get("director", concept[:200]).split("\n")[0]
        subject = clean_line(subject_raw)
        subject_layer = f"[SUBJECT_ANCHOR]: {subject} + (pore-level skin detail:1.2) + (physics-accurate movement:1.3)"

        # Layer 1.5: Voice DNA
        voice_layer = f"[CHARACTER_VOICE_DNA]: {voice_dna}" if voice_dna else ""

        # Layer 2: Environment
        env_raw = results.get("designer", "Bengal street scene").split("\n")[0]
        env = clean_line(env_raw)
        env_layer = f"[ENVIRONMENT_MESH]: {env} + Atmospheric Perspective + (Bengal Registry: Yellow Ambassador Taxi, Wall Graffiti in Bengali Script:1.2)"

        # Layer 3: Lighting
        light_raw = results.get("dop", "High contrast").split("\n")[0]
        light = clean_line(light_raw)
        light_layer = f"[LIGHTING_COMPLEXITY]: {light} :: Tyndall Effect (God Rays) :: Sub-Surface Scattering"

        # Layer 4: Camera
        camera_layer = "[CAMERA_PHYSICS]: IMAX 15/70mm Film Camera :: 35mm Anamorphic :: f/1.4 (Razor thin focus) :: 180 degree shutter"

        # Layer 5: Post
        post_layer = "[POST_PROCESS_STACK]: Kodak Vision3 5219 (500T) :: 35mm Fine Grain :: Rec.709 :: Teal and Orange (Split Tone)"

        # Compile Stack
        stack_parts = [subject_layer]
        if voice_layer:
            stack_parts.append(voice_layer)
        stack_parts.extend([env_layer, light_layer, camera_layer, post_layer])

        stack = " :: ".join(stack_parts)

        # Flags
        flags = '--ar 16:9 --style cinematic --motion 5 --quality 2 --no "morphing hands, extra digits, text overlay, watermarks, oversaturated colors, cartoon style, 3d render, plastic skin"'

        return f"{stack} {flags}"

    def _save_production_script(
        self, concept: str, content: str, session_id: str
    ) -> Path:
        """Save production script to file."""
        safe_concept = sanitize_filename(concept[:50])
        filename = f"{safe_concept}_{session_id[:8]}.md"

        output_path = self.settings.paths.production_scripts_dir / filename
        save_text_file(content, output_path)

        return output_path
