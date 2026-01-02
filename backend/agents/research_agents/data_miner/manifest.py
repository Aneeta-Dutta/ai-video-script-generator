"""
Data Miner Agent Manifest.

Metadata and configuration for the Data Miner research agent.
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


# Data Miner manifest
MANIFEST = AgentManifest(
    name="data_miner",
    display_name="Data Miner (The Quant)",
    description="Statistical analysis and official records specialist",
    version="1.0.0",
    role="Statistical Analysis & Data Verification",
    capabilities=[
        "Extract statistical data",
        "Verify claims with numbers",
        "Analyze government reports",
        "Compare economic indices",
        "Provide sourced data points"
    ],
    persona_file="",  # Uses inline persona for now
    guide_file=None,
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
