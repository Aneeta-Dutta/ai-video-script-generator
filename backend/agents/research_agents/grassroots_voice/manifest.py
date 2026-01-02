"""
Grassroots Voice (The Qualitative) Agent Manifest.

Metadata and configuration for the Grassroots Voice (The Qualitative) research agent.
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


# Grassroots Voice (The Qualitative) manifest
MANIFEST = AgentManifest(
    name="grassroots_voice",
    display_name="Grassroots Voice (The Qualitative)",
    description="Human stories and emotional impact specialist",
    version="1.0.0",
    role="Qualitative Research & Human Stories",
    capabilities=['Capture emotional pulse', 'Collect anecdotes', 'Analyze social sentiment', 'Document ground reality'],
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
