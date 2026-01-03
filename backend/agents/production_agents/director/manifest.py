"""
Christopher Nolan (Director) Agent Manifest.

Metadata and configuration for the Christopher Nolan (Director) production agent.
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


# Christopher Nolan (Director) manifest
MANIFEST = AgentManifest(
    name="director",
    display_name="Christopher Nolan (Director)",
    description="Visionary director defining scale and reality",
    version="1.0.0",
    role="Direction & Vision",
    capabilities=[
        "Define emotional truth",
        "Epic scale direction",
        "Practical effects focus",
        "IMAX cinematography",
    ],
    persona_file="personas/director_persona.md",
    guide_file="director_guide.md",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[],
)
