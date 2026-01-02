"""
Kobiyal (Writer) Agent Manifest.

Metadata and configuration for the Kobiyal (Writer) production agent.
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


# Kobiyal (Writer) manifest
MANIFEST = AgentManifest(
    name="writer",
    display_name="Kobiyal (Writer)",
    description="Bengali poet and dialogue specialist",
    version="1.0.0",
    role="Dialogue & Script",
    capabilities=['Dialogue writing', 'Cultural authenticity', 'Emotional resonance', 'Bengali idioms'],
    persona_file="personas/writer_persona.md",
    guide_file="dialogue_guide.md",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
