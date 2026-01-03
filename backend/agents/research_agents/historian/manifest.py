"""
Historian (The Contextualizer) Agent Manifest.

Metadata and configuration for the Historian (The Contextualizer) research agent.
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


# Historian (The Contextualizer) manifest
MANIFEST = AgentManifest(
    name="historian",
    display_name="Historian (The Contextualizer)",
    description="Root cause analysis and historical context specialist",
    version="1.0.0",
    role="Root Cause Analysis & Historical Context",
    capabilities=[
        "Provide historical context",
        "Root cause analysis",
        "Policy comparison",
        "Timeline creation",
    ],
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[],
)
