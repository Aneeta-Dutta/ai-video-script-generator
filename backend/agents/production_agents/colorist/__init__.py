"""
Post-Production Colorist Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import colorist_agent

__all__ = ["colorist_agent", "MANIFEST"]
