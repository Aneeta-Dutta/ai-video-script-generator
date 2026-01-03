"""
Lead Investigator Agent Manifest.

Metadata and configuration for the Lead Investigator (coordinator) agent.
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


# Lead Investigator manifest
MANIFEST = AgentManifest(
    name="lead_investigator",
    display_name="Lead Investigator (The Synthesizer)",
    description="Research coordinator and synthesis specialist",
    version="1.0.0",
    role="Swarm Commander & Synthesis",
    capabilities=[
        "Coordinate research agents",
        "Synthesize findings",
        "Prioritize topics",
        "Create final reports",
        "Generate video concepts",
    ],
    persona_file="",
    guide_file=None,
    model_override=None,
    requires_sub_agents=True,
    sub_agent_names=[
        "data_miner",
        "grassroots_voice",
        "historian",
        "trend_scout",
        "narrative_architect",
    ],
)
