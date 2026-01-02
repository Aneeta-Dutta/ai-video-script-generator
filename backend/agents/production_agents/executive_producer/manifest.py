"""
Executive Producer Agent Manifest.

Metadata and configuration for the Executive Producer (coordinator) agent.
"""

from dataclasses import dataclass, field
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
    sub_agent_names: List[str] = field(default_factory=list)


# Executive Producer manifest
MANIFEST = AgentManifest(
    name="executive_producer",
    display_name="Executive Producer (The Showrunner)",
    description="Production coordinator and script synthesizer",
    version="1.0.0",
    role="Production Orchestration & Synthesis",
    capabilities=[
        "Coordinate production team",
        "Synthesize creative outputs",
        "Generate final VEO prompts",
        "Quality control",
        "JSON output formatting"
    ],
    persona_file="executive_producer_guide.md",
    guide_file="veo_prompt_guide.md",
    model_override=None,
    requires_sub_agents=True,
    sub_agent_names=["director", "dop", "designer", "colorist", "writer"]
)
