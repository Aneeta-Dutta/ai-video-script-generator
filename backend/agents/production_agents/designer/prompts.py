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

**Instructions:**
**8-SECOND BYTE PROTOCOL (REALISM & DETAIL):**
1. **HYPER-REALISTIC MATERIALITY:** Avoid "AI sheen". Focus on **Physical Grounding**. Every texture must feel tangible.
2. **PBR Detailing:** Use physically-based rendering terms. Crumbling plaster in North Kolkata alleyways must show displacement, dust, and weathering.
3. **Bengal DNA:** Inject regional visual anchors with hyper-detail (Yellow Ambassador Taxi with rust spots, wall graffiti in weathered Bengali script, specific banyan tree roots).
4. **Atmospherics:** Focus on high-fidelity volumetric dust, grime on window panes, and moisture on skin/walls.
5. ABSOLUTE FIRST LINE: A single-phrase "Stack Anchor" (Environment + Material Detail + Weathering).
6. **Materiality:** Define materials with physical properties (Wet Asphalt [Roughness: 0.2], Crumbling Concrete [Disp: High]).
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
