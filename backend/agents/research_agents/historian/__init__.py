"""
Historian (The Contextualizer) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import historian_agent

__all__ = ["historian_agent", "MANIFEST"]
