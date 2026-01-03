"""Research Agents module."""

from .data_miner import data_miner_agent, MANIFEST as DATA_MINER_MANIFEST
from .grassroots_voice import grassroots_voice_agent, MANIFEST as GRASSROOTS_MANIFEST
from .historian import historian_agent, MANIFEST as HISTORIAN_MANIFEST
from .trend_scout import trend_scout_agent, MANIFEST as TREND_SCOUT_MANIFEST
from .narrative_architect import (
    narrative_architect_agent,
    MANIFEST as NARRATIVE_ARCHITECT_MANIFEST,
)
from .lead_investigator import (
    lead_investigator_agent,
    MANIFEST as LEAD_INVESTIGATOR_MANIFEST,
)

__all__ = [
    "data_miner_agent",
    "grassroots_voice_agent",
    "historian_agent",
    "trend_scout_agent",
    "narrative_architect_agent",
    "lead_investigator_agent",
    "DATA_MINER_MANIFEST",
    "GRASSROOTS_MANIFEST",
    "HISTORIAN_MANIFEST",
    "TREND_SCOUT_MANIFEST",
    "NARRATIVE_ARCHITECT_MANIFEST",
    "LEAD_INVESTIGATOR_MANIFEST",
]
