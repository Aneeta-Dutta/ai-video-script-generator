"""
Nathan Crowley (Designer) Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "personas/designer_persona.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "production_design_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Veo 3 optimization."""
    persona = load_persona()
    guide = load_guide()

    veo_3_instruction = """
---
## 🏗️ Veo 3 Protocol: Layer 2 - The Environment Mesh
Your primary goal is to define the **Environment Mesh** and **Materiality** using the **Bengal Palette**.

**Instructions (Hollywood Standard v1):**
1. **PBR MASTER STACK:** Use **Universal Wear-Level (0-1.0)**, **Roughness Variance Mapping**, and **Anisotropic Vector Mapping (90-deg for silk)**.
2. **STRUCTURAL TENSION:** Build environments with **Structural Subtext** (e.g., "unbalanced weights", "braced beams").
3. **MATERIAL PHYSICS:** Define **IOR-accurate moisture (1.33)** and **Sub-surface Scattering (SSS)** for Clay/Silk/Paper.
4. **VOLUMETRIC FIDELITY:** Specify **Sub-pixel Airborne Micro-debris density**.
5. **NEGATIVE CONSTRAINTS:** NO generic clean surfaces, NO repeated textures/patterns, NO floating objects.
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Structural Motif] + [Anisotropic Detail] + [Wear-Level Logic].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
