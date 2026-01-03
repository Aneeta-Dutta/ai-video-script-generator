"""
Post-Production Colorist Agent Manifest.

Metadata and configuration for the Post-Production Colorist production agent.
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


# Post-Production Colorist manifest
MANIFEST = AgentManifest(
    name="colorist",
    display_name="Post-Production Colorist",
    description="Color grading and post-production specialist",
    version="1.0.0",
    role="Color Grading",
    capabilities=[
        "Color grading",
        "Mood enhancement",
        "Visual consistency",
        "Atmospheric tones",
    ],
    persona_file="personas/colorist_persona.md",
    guide_file="post_production_guide.md",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[],
)
