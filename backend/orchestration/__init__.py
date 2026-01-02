"""
Orchestration layer exports.

Simplified to only export the SequentialAgent-based pipelines.
"""

from .research_pipeline import research_pipeline_agent
from .production_pipeline import production_pipeline_agent

__all__ = [
    'research_pipeline_agent',
    'production_pipeline_agent',
]
