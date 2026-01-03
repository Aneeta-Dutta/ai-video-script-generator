"""
Trend Scout (The Virality Engineer) Agent Manifest.

Metadata and configuration for the Trend Scout (The Virality Engineer) research agent.
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


# Trend Scout (The Virality Engineer) manifest
MANIFEST = AgentManifest(
    name="trend_scout",
    display_name="Trend Scout (The Virality Engineer)",
    description="Viral angles and trending topics specialist",
    version="1.0.0",
    role="Virality Engineering & Trend Analysis",
    capabilities=[
        "Identify viral angles",
        "Create engaging hooks",
        "Analyze shareability",
        "Trend detection",
    ],
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[],
)
