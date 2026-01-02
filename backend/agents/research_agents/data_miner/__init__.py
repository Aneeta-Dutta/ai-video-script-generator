"""
Data Miner Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import data_miner_agent

__all__ = ["data_miner_agent", "MANIFEST"]
