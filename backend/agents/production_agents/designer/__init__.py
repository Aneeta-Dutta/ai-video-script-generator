"""
Nathan Crowley (Designer) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import designer_agent

__all__ = ["designer_agent", "MANIFEST"]
