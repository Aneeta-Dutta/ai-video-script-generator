"""
Production Pipeline using ADK SequentialAgent.

Uses ADK's built-in workflow agents for deterministic orchestration
with output_key for state management.
"""

from google.adk.agents import SequentialAgent, LlmAgent
from backend.core import get_settings

# Import production agent manifests
from backend.agents.production_agents.director import MANIFEST as DIRECTOR_MANIFEST
from backend.agents.production_agents.designer import MANIFEST as DESIGNER_MANIFEST
from backend.agents.production_agents.dop import MANIFEST as DOP_MANIFEST
from backend.agents.production_agents.colorist import MANIFEST as COLORIST_MANIFEST
from backend.agents.production_agents.writer import MANIFEST as WRITER_MANIFEST

from backend.agents.production_agents.director.prompts import (
    construct_instruction as director_instruction,
)
from backend.agents.production_agents.designer.prompts import (
    construct_instruction as designer_instruction,
)
from backend.agents.production_agents.dop.prompts import (
    construct_instruction as dop_instruction,
)
from backend.agents.production_agents.colorist.prompts import (
    construct_instruction as colorist_instruction,
)
from backend.agents.production_agents.writer.prompts import (
    construct_instruction as writer_instruction,
)


def create_production_pipeline() -> SequentialAgent:
    """
    Create production pipeline using ADK's SequentialAgent pattern.

    Each agent stores output in state via output_key.
    Next agents can access previous outputs using {key} placeholders.
    """
    settings = get_settings()
    model = settings.model.get_production_model

    # Create each production agent with output_key
    director = LlmAgent(
        name="director",
        model=model,
        description="Establishes vision and scale",
        instruction=director_instruction(),
        output_key="director_vision",
        include_contents="none",
    )

    designer = LlmAgent(
        name="designer",
        model=model,
        description="Designs production environment",
        instruction=designer_instruction(),
        output_key="production_design",
        include_contents="none",
    )

    dop = LlmAgent(
        name="dop",
        model=model,
        description="Plans cinematography",
        instruction=dop_instruction(),
        output_key="cinematography",
        include_contents="none",
    )

    colorist = LlmAgent(
        name="colorist",
        model=model,
        description="Defines color grading",
        instruction=colorist_instruction(),
        output_key="color_grading",
        include_contents="none",
    )

    # Final writer synthesizes everything into shooting script
    writer = LlmAgent(
        name="writer",
        model=model,
        description="Creates final shooting script",
        instruction=f"""You are a Script Writer. Create a comprehensive shooting script.

**Director's Vision:**
{{director_vision}}

**Production Design:**
{{production_design}}

**Cinematography:**
{{cinematography}}

**Color Grading:**
{{color_grading}}

Synthesize all the above into a detailed shooting script with:
1. Scene description
2. Camera movements
3. Lighting setup
4. Color palette
5. VEO 3 prompt block

Minimum 300 words.
""",
        output_key="shooting_script",
        include_contents="none",
    )

    # Create Sequential Agent
    return SequentialAgent(
        name="ProductionPipeline",
        sub_agents=[director, designer, dop, colorist, writer],
        description="Sequential production pipeline with state-based data passing",
    )


# Create singleton pipeline instance
production_pipeline_agent = create_production_pipeline()
