"""
Kobiyal (Writer) Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import writer_agent

__all__ = ["writer_agent", "MANIFEST"]
