"""
Hoyte van Hoytema (DoP) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import dop_agent

__all__ = ["dop_agent", "MANIFEST"]
