"""Agents module."""

from .research_agents import (
    lead_investigator_agent,
    data_miner_agent,
    grassroots_voice_agent,
    historian_agent,
    trend_scout_agent,
    narrative_architect_agent,
)

from .production_agents import (
    executive_producer_agent,
    director_agent,
    dop_agent,
    designer_agent,
    colorist_agent,
    writer_agent,
)

__all__ = [
    # Research agents
    "lead_investigator_agent",
    "data_miner_agent",
    "grassroots_voice_agent",
    "historian_agent",
    "trend_scout_agent",
    "narrative_architect_agent",
    # Production agents
    "executive_producer_agent",
    "director_agent",
    "dop_agent",
    "designer_agent",
    "colorist_agent",
    "writer_agent",
]
