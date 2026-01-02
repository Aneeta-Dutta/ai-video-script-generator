"""
Narrative Architect (The Story Weaver) Agent Manifest.

Metadata and configuration for the Narrative Architect (The Story Weaver) research agent.
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


# Narrative Architect (The Story Weaver) manifest
MANIFEST = AgentManifest(
    name="narrative_architect",
    display_name="Narrative Architect (The Story Weaver)",
    description="Synthesizes research into compelling video concepts",
    version="1.0.0",
    role="Narrative Synthesis & Story Construction",
    capabilities=['Synthesize research', 'Create narrative arcs', 'Suggest visual concepts', 'Structure stories'],
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
