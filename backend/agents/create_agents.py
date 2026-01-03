"""Script to generate agent modules from legacy agent files."""

import os
from pathlib import Path

# Agent definitions from legacy code
AGENTS = {
    "grassroots_voice": {
        "display_name": "Grassroots Voice (The Qualitative)",
        "description": "Human stories and emotional impact specialist",
        "role": "Qualitative Research & Human Stories",
        "persona": """You are The Grassroots Voice (The Qualitative).
Role: Human Stories & Emotional Impact.
Focus: Anecdotes, viral social media sentiments, ground-level reality.

Your goal is to capturing the emotional pulse of the people.
When given a topic, you ask questions like:
* "What are students saying outside the exam centers?"
* "How does a 30-year-old unemployed youth feel at a family wedding?"
* "The trauma of the 'educated delivery boy'."

Output your findings as a collection of short, powerful anecdotal narratives or sentiment summaries.""",
        "capabilities": [
            "Capture emotional pulse",
            "Collect anecdotes",
            "Analyze social sentiment",
            "Document ground reality",
        ],
    },
    "historian": {
        "display_name": "Historian (The Contextualizer)",
        "description": "Root cause analysis and historical context specialist",
        "role": "Root Cause Analysis & Historical Context",
        "persona": """You are The Historian (The Contextualizer).
Role: Root Cause Analysis.
Focus: Connecting current issues to past policies or systematic decay.

Your goal is to provide deep context.
When given a topic, you ask questions like:
* "How did the 'Flight of Capital' start?"
* "Is this a generational curse?"
* "Comparison with other states' models."

Output your findings as a historical timeline or root-cause analysis summary.""",
        "capabilities": [
            "Provide historical context",
            "Root cause analysis",
            "Policy comparison",
            "Timeline creation",
        ],
    },
    "trend_scout": {
        "display_name": "Trend Scout (The Virality Engineer)",
        "description": "Viral angles and trending topics specialist",
        "role": "Virality Engineering & Trend Analysis",
        "persona": """You are The Trend Scout (The Virality Engineer).
Role: Viral Angle Detection.
Focus: What will make people *share*, what will make people *click*.

Your goal is to find the hook.
When given a topic, you ask questions like:
* "What's the 'punchable' government official?"
* "The clickbait title that doesn't lie."
* "The David vs. Goliath angle."

Output your findings as potential viral hooks, trending hashtags, oremotion-trigger points.""",
        "capabilities": [
            "Identify viral angles",
            "Create engaging hooks",
            "Analyze shareability",
            "Trend detection",
        ],
    },
    "narrative_architect": {
        "display_name": "Narrative Architect (The Story Weaver)",
        "description": "Synthesizes research into compelling video concepts",
        "role": "Narrative Synthesis & Story Construction",
        "persona": """You are The Narrative Architect (The Story Weaver).
Role: Final Synthesis.
Focus: Converting all the research into video concepts and scripts.

Your goal is to create the blueprint.
When given research, you:
* Identify the core message
* Structure the narrative arc (Problem -> Root -> Emotion -> Solution)
* Suggest visual metaphors
* Propose the protagonist (usually Arindam Roy) and antagonist framing

Output your findings as structured video concept briefs with scene suggestions.""",
        "capabilities": [
            "Synthesize research",
            "Create narrative arcs",
            "Suggest visual concepts",
            "Structure stories",
        ],
    },
}


def create_agent_module(agent_name: str, config: dict, base_path: Path):
    """Create a complete agent module."""
    agent_dir = base_path / agent_name
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Create manifest.py
    manifest_content = f'''"""
{config['display_name']} Agent Manifest.

Metadata and configuration for the {config['display_name']} research agent.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AgentManifest:
    """Agent metadata and capabilities."""
    
    name: str
    display_name: str
    description: str
    version: str
    role: str
    capabilities: List[str]
    persona_file: str
    guide_file: Optional[str] = None
    model_override: Optional[str] = None
    requires_sub_agents: bool = False
    sub_agent_names: List[str] = None


# {config['display_name']} manifest
MANIFEST = AgentManifest(
    name="{agent_name}",
    display_name="{config['display_name']}",
    description="{config['description']}",
    version="1.0.0",
    role="{config['role']}",
    capabilities={config['capabilities']},
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
'''

    # Create prompts.py
    prompts_content = f'''"""
{config['display_name']} Agent prompts and persona.
"""

PERSONA = """{config['persona']}"""


def get_persona() -> str:
    """Get the {agent_name} persona."""
    return PERSONA


def construct_instruction() -> str:
    """Construct the full instruction for the agent."""
    return get_persona()
'''

    # Create agent.py
    agent_content = f'''"""
{config['display_name']} Agent implementation.
"""

from google.adk.agents import LlmAgent
from backend.core import get_settings
from .manifest import MANIFEST
from .prompts import construct_instruction


def create_agent() -> LlmAgent:
    """Create and configure the {config['display_name']} agent."""
    settings = get_settings()
    
    # Determine model to use
    model = MANIFEST.model_override or settings.model.get_research_model
    
    return LlmAgent(
        name=MANIFEST.name,
        model=model,
        description=MANIFEST.description,
        instruction=construct_instruction()
    )


# Create singleton instance
{agent_name}_agent = create_agent()
'''

    # Create __init__.py
    init_content = f'''"""
{config['display_name']} Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import {agent_name}_agent

__all__ = ["{agent_name}_agent", "MANIFEST"]
'''

    # Write files
    (agent_dir / "manifest.py").write_text(manifest_content)
    (agent_dir / "prompts.py").write_text(prompts_content)
    (agent_dir / "agent.py").write_text(agent_content)
    (agent_dir / "__init__.py").write_text(init_content)

    print(f"✅ Created {agent_name} module")


if __name__ == "__main__":
    base_path = Path(__file__).parent / "research_agents"

    for agent_name, config in AGENTS.items():
        create_agent_module(agent_name, config, base_path)

    print("\n🎉 All research agent modules created!")
