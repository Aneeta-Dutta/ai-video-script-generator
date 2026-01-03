"""
Research Pipeline using ADK SequentialAgent.

Uses ADK's built-in workflow agents for deterministic orchestration
with output_key for state management.
"""

from google.adk.agents import SequentialAgent, LlmAgent
from backend.core import get_settings

# Import individual research agents (will be recreated with output_key)
from backend.agents.research_agents.data_miner import MANIFEST as DATA_MINER_MANIFEST
from backend.agents.research_agents.grassroots_voice import (
    MANIFEST as GRASSROOTS_MANIFEST,
)
from backend.agents.research_agents.historian import MANIFEST as HISTORIAN_MANIFEST
from backend.agents.research_agents.trend_scout import MANIFEST as TREND_SCOUT_MANIFEST
from backend.agents.research_agents.narrative_architect import (
    MANIFEST as NARRATIVE_MANIFEST,
)

from backend.agents.research_agents.data_miner.prompts import (
    construct_instruction as data_miner_instruction,
)
from backend.agents.research_agents.grassroots_voice.prompts import (
    construct_instruction as grassroots_instruction,
)
from backend.agents.research_agents.historian.prompts import (
    construct_instruction as historian_instruction,
)
from backend.agents.research_agents.trend_scout.prompts import (
    construct_instruction as trend_scout_instruction,
)
from backend.agents.research_agents.narrative_architect.prompts import (
    construct_instruction as narrative_instruction,
)


def create_research_pipeline() -> SequentialAgent:
    """
    Create research pipeline using ADK's SequentialAgent pattern.

    Each agent stores output in state via output_key.
    Next agents can access previous outputs using {key} placeholders.
    """
    settings = get_settings()
    model = settings.model.get_research_model

    # Create each research agent with output_key
    data_miner = LlmAgent(
        name="data_miner",
        model=model,
        description="Analyzes statistical evidence and data",
        instruction=data_miner_instruction(),
        output_key="data_analysis",  # Stores in state['data_analysis']
        include_contents="none",  # Don't include chat history
    )

    grassroots_voice = LlmAgent(
        name="grassroots_voice",
        model=model,
        description="Captures ground-level perspectives",
        instruction=grassroots_instruction(),
        output_key="grassroots_perspectives",
        include_contents="none",
    )

    historian = LlmAgent(
        name="historian",
        model=model,
        description="Provides historical context",
        instruction=historian_instruction(),
        output_key="historical_context",
        include_contents="none",
    )

    trend_scout = LlmAgent(
        name="trend_scout",
        model=model,
        description="Identifies current trends",
        instruction=trend_scout_instruction(),
        output_key="current_trends",
        include_contents="none",
    )

    # Final synthesis agent that combines all previous outputs
    narrative_architect = LlmAgent(
        name="narrative_architect",
        model=model,
        description="Synthesizes all research into cohesive narrative",
        instruction=f"""You are a Narrative Architect. Create a comprehensive research report.

**Data Analysis:**
{{data_analysis}}

**Grassroots Perspectives:**
{{grassroots_perspectives}}

**Historical Context:**
{{historical_context}}

**Current Trends:**
{{current_trends}}

Synthesize all the above into a cohesive, well-structured research report.
Include introduction, key findings, and conclusion.
Minimum 500 words.
""",
        output_key="final_report",
        include_contents="none",
    )

    # Create Sequential Agent that runs all in order
    return SequentialAgent(
        name="ResearchPipeline",
        sub_agents=[
            data_miner,
            grassroots_voice,
            historian,
            trend_scout,
            narrative_architect,
        ],
        description="Sequential research pipeline with state-based data passing",
    )


# Create singleton pipeline instance
research_pipeline_agent = create_research_pipeline()
