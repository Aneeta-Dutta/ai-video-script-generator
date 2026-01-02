"""
Executive Producer Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import executive_producer_agent

__all__ = ["executive_producer_agent", "MANIFEST"]
