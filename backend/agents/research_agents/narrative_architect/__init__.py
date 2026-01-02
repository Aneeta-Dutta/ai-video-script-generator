"""
Narrative Architect (The Story Weaver) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import narrative_architect_agent

__all__ = ["narrative_architect_agent", "MANIFEST"]
