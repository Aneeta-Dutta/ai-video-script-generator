"""
Post-Production Colorist Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "personas/colorist_persona.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "post_production_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Veo 3 optimization."""
    persona = load_persona()
    guide = load_guide()

    veo_3_instruction = """
---
## 🎨 Veo 3 Protocol: Layer 4 - Post-Process Stack
Your primary goal is to define the **Post-Process Stack** and **Film Emulation**.

**Instructions:**
**8-SECOND BYTE PROTOCOL (HOLLYWOOD COLOR SCIENCE):**
1. **LMT & FILM STOCK EMULATION:** Use specific **Look Modification Transforms (LMTs)**. Define **Kodak Vision3 500T (5219)** for tungsten or **250D (5207)** for daylight. Specify **Print Emulation (Kodak 2383)**.
2. **SKIN TONE PROTECTION:** Ensure all grading (Split-toning, LUTs) preserves the **Melanin-accurate skin tones** of the West Bengal subject. No "orange skin". Use **Sub-surface Scattering (SSS)** anchors.
3. **BLACK POINT & GRAIN:** Define a **Lush Black Point** (not crushed) and **Temporal Grain Profiles** (35mm Coarse for low-light, 16mm for memory/introspection).
4. **BLOOM & HALATION:** Specify technical **Red-Channel Halation** on high-contrast edges and **Anamorphic Blue-streak Flare** where motived.
5. **MASTERING TARGET:** Anchor for **HDR (Rec.2100 PQ)** with specific peak nit brightness for specular highlights (catchlights in eyes, wet pavement).
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Film Stock] + [Skin Tone Protection Hook] + [Mastering Target].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
