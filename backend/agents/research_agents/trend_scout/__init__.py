"""
Trend Scout (The Virality Engineer) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import trend_scout_agent

__all__ = ["trend_scout_agent", "MANIFEST"]
