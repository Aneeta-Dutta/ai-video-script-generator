"""
Christopher Nolan (Director) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import director_agent

__all__ = ["director_agent", "MANIFEST"]
