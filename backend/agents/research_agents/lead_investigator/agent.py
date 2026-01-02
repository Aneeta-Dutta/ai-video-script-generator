"""
Lead Investigator Agent implementation.
"""

from google.adk.agents import LlmAgent
from backend.core import get_settings
from .manifest import MANIFEST
from .prompts import construct_instruction


def create_agent() -> LlmAgent:
    """Create and configure the Lead Investigator agent (stateless, no sub-agents)."""
    settings = get_settings()
    
    # Determine model to use
    model = MANIFEST.model_override or settings.model.get_research_model
    
    return LlmAgent(
        name=MANIFEST.name,
        model=model,
        description=MANIFEST.description,
        instruction=construct_instruction()
    )


# Create singleton instance
lead_investigator_agent = create_agent()
