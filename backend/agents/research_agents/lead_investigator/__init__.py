"""
Lead Investigator Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import lead_investigator_agent

__all__ = ["lead_investigator_agent", "MANIFEST"]
