"""
Grassroots Voice (The Qualitative) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import grassroots_voice_agent

__all__ = ["grassroots_voice_agent", "MANIFEST"]
