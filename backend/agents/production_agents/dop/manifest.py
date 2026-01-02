"""
Hoyte van Hoytema (DoP) Agent Manifest.

Metadata and configuration for the Hoyte van Hoytema (DoP) production agent.
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


# Hoyte van Hoytema (DoP) manifest
MANIFEST = AgentManifest(
    name="dop",
    display_name="Hoyte van Hoytema (DoP)",
    description="Master cinematographer for visual excellence",
    version="1.0.0",
    role="Cinematography",
    capabilities=['Camera movement design', 'Lighting setup', 'Shot composition', 'Visual storytelling'],
    persona_file="personas/dop_persona.md",
    guide_file="cinematography_guide.md",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
