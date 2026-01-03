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

**Instructions (Hollywood Standard v1):**
1. **ACES PIPELINE:** Specify **IDT (Input Display Transform)** and **ODT (Rec.709/2020)**. Define **Gamut Mapping** for emissive sources.
2. **SKIN TONE & LIGHT WRAP:** Preserve **Melanin-accurate tones**. Apply **Optical Light Wrap** for background integration.
3. **GRAIN & BLACKS:** Use **Monochromatic Temporal Grain** and define a **Lush Black Point**. 
4. **Specular Fidelity:** Target **1000 nits Specular Peak** without clipping.
5. **NEGATIVE CONSTRAINTS:** NO digital noise, NO oversaturated "AI teal/orange", NO crushed blacks.
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [ACES Pipeline] + [Light Wrap Detail] + [Skin Tone Protection].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
