"""Production Agents module."""

from .director import director_agent, MANIFEST as DIRECTOR_MANIFEST
from .dop import dop_agent, MANIFEST as DOP_MANIFEST
from .designer import designer_agent, MANIFEST as DESIGNER_MANIFEST
from .colorist import colorist_agent, MANIFEST as COLORIST_MANIFEST
from .writer import writer_agent, MANIFEST as WRITER_MANIFEST
from .executive_producer import (
    executive_producer_agent,
    MANIFEST as EXECUTIVE_PRODUCER_MANIFEST,
)

__all__ = [
    "director_agent",
    "dop_agent",
    "designer_agent",
    "colorist_agent",
    "writer_agent",
    "executive_producer_agent",
    "DIRECTOR_MANIFEST",
    "DOP_MANIFEST",
    "DESIGNER_MANIFEST",
    "COLORIST_MANIFEST",
    "WRITER_MANIFEST",
    "EXECUTIVE_PRODUCER_MANIFEST",
]
