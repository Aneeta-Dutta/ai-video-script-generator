"""Script to generate production agent modules."""

import os
from pathlib import Path

# Production agents configuration
# These load personas from external markdown files
PRODUCTION_AGENTS = {
    "director": {
        "display_name": "Christopher Nolan (Director)",
        "description": "Visionary director defining scale and reality",
        "role": "Direction & Vision",
        "agent_var_name": "director_agent",
        "persona_file": "personas/director_persona.md",
        "guide_file": "director_guide.md",
        "capabilities": [
            "Define emotional truth",
            "Epic scale direction",
            "Practical effects focus",
            "IMAX cinematography",
        ],
    },
    "dop": {
        "display_name": "Hoyte van Hoytema (DoP)",
        "description": "Master cinematographer for visual excellence",
        "role": "Cinematography",
        "agent_var_name": "dop_agent",
        "persona_file": "personas/dop_persona.md",
        "guide_file": "cinematography_guide.md",
        "capabilities": [
            "Camera movement design",
            "Lighting setup",
            "Shot composition",
            "Visual storytelling",
        ],
    },
    "designer": {
        "display_name": "Nathan Crowley (Designer)",
        "description": "Production designer crafting authentic environments",
        "role": "Production Design",
        "agent_var_name": "designer_agent",
        "persona_file": "personas/designer_persona.md",
        "guide_file": "production_design_guide.md",
        "capabilities": [
            "Set design",
            "Environment creation",
            "Authentic atmosphere",
            "Visual metaphors",
        ],
    },
    "colorist": {
        "display_name": "Post-Production Colorist",
        "description": "Color grading and post-production specialist",
        "role": "Color Grading",
        "agent_var_name": "colorist_agent",
        "persona_file": "personas/colorist_persona.md",
        "guide_file": "post_production_guide.md",
        "capabilities": [
            "Color grading",
            "Mood enhancement",
            "Visual consistency",
            "Atmospheric tones",
        ],
    },
    "writer": {
        "display_name": "Kobiyal (Writer)",
        "description": "Bengali poet and dialogue specialist",
        "role": "Dialogue & Script",
        "agent_var_name": "writer_agent",
        "persona_file": "personas/writer_persona.md",
        "guide_file": "dialogue_guide.md",
        "capabilities": [
            "Dialogue writing",
            "Cultural authenticity",
            "Emotional resonance",
            "Bengali idioms",
        ],
    },
}


def create_production_agent_module(agent_name: str, config: dict, base_path: Path):
    """Create a production agent module with persona file loading."""
    agent_dir = base_path / agent_name
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Create manifest.py
    manifest_content = f'''"""
{config['display_name']} Agent Manifest.

Metadata and configuration for the {config['display_name']} production agent.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AgentManifest:
    """Agent metadata and capabilities."""
    
    name: str
    display_name: str
    description: str
    version: str
    role: str
    capabilities: List[str]
    persona_file: str
    guide_file: Optional[str] = None
    model_override: Optional[str] = None
    requires_sub_agents: bool = False
    sub_agent_names: List[str] = None


# {config['display_name']} manifest
MANIFEST = AgentManifest(
    name="{agent_name}",
    display_name="{config['display_name']}",
    description="{config['description']}",
    version="1.0.0",
    role="{config['role']}",
    capabilities={config['capabilities']},
    persona_file="{config['persona_file']}",
    guide_file="{config.get('guide_file', '')}",
    model_override=None,
    requires_sub_agents=False,
    sub_agent_names=[]
)
'''

    # Create prompts.py with file loading
    prompts_content = f'''"""
{config['display_name']} Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "{config['persona_file']}"
    
    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {{persona_path}}")
    
    return persona_path.read_text(encoding='utf-8')


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "{config.get('guide_file', '')}"
    
    if not guide_path.exists():
        return ""
    
    return guide_path.read_text(encoding='utf-8')


def construct_instruction() -> str:
    """Construct the full instruction for the agent."""
    persona = load_persona()
    guide = load_guide()
    
    if guide:
        # Combine persona with guide
        return f"""{{persona}}

---
# Reference Guide

{{guide}}
"""
    
    return persona
'''

    # Create agent.py
    agent_content = f'''"""
{config['display_name']} Agent implementation.
"""

from google.adk.agents import LlmAgent
from backend.core import get_settings
from .manifest import MANIFEST
from .prompts import construct_instruction


def create_agent() -> LlmAgent:
    """Create and configure the {config['display_name']} agent."""
    settings = get_settings()
    
    # Determine model to use
    model = MANIFEST.model_override or settings.model.get_production_model
    
    return LlmAgent(
        name=MANIFEST.name,
        model=model,
        description=MANIFEST.description,
        instruction=construct_instruction()
    )


# Create singleton instance
{config['agent_var_name']} = create_agent()
'''

    # Create __init__.py
    init_content = f'''"""
{config['display_name']} Agent module.

Exports the configured agent instance and metadata.
"""

from .manifest import MANIFEST
from .agent import {config['agent_var_name']}

__all__ = ["{config['agent_var_name']}", "MANIFEST"]
'''

    # Write files
    (agent_dir / "manifest.py").write_text(manifest_content)
    (agent_dir / "prompts.py").write_text(prompts_content)
    (agent_dir / "agent.py").write_text(agent_content)
    (agent_dir / "__init__.py").write_text(init_content)

    print(f"✅ Created {agent_name} module")


if __name__ == "__main__":
    base_path = Path(__file__).parent / "production_agents"

    for agent_name, config in PRODUCTION_AGENTS.items():
        create_production_agent_module(agent_name, config, base_path)

    print("\n🎉 All production agent modules created!")
