"""
Nathan Crowley (Designer) Agent Manifest.

Metadata and configuration for the Nathan Crowley (Designer) production agent.
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


# Nathan Crowley (Designer) manifest
MANIFEST = AgentManifest(
    name="designer",
    display_name="Nathan Crowley (Designer)",
    description="Production designer crafting authentic environments",
    version="1.0.0",
    role="Production Design",
    capabilities=['Set design', 'Environment creation', 'Authentic atmosphere', 'Visual metaphors'],
    persona_file="personas/designer_persona.md",
    guide_file="production_design_guide.md",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
