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
**8-SECOND BYTE PROTOCOL (PRODUCTION DESIGN EXCELLENCE):**
1. **COMPOSITIONAL GEOMETRY:** Build environments that enforce the Director's motifs. Use **Architectural Leading Lines**, **Framing within a Frame**, and **Negative Space** to anchor the subject.
2. **HISTORICAL & MATERIAL AUTHENTICITY:** Move beyond generic prompts. Define **Industrial Patina**, **Oxidation Ratios**, and **Period-Accurate Textures** (e.g., "19th century British-era brickwork with specific moss-displacement [Roughness: 0.9]").
3. **PBR TOKEN STACK:** Use technical tokens: **Anisotropy** (for brushed metal), **Sub-surface Scattering** (for marble/leaves), and **Normal Mapping** (for high-density grime).
4. **ATMOSPHERIC VOLUMETRICS:** Define the **Tyndall Effect**, **Bokeh Shape (Hexagonal)**, and **Airborne Micro-debris** (dust motes, silk fibers) to create depth.
5. **CULTURAL ANCHORING:** Use high-fidelity regional markers (e.g., "Jamdani silk patterns with metallic thread-displacement", "Kolkata Brutalist concrete with monsoon-staining").
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Architectural Motif] + [Material DNA] + [Atmospheric Hook].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
