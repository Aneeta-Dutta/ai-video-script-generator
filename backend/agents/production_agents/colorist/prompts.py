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
**8-SECOND BYTE PROTOCOL (FILM EMULATION & GRIT):**
1. **GROUNDED FILM EMULATION:** Avoid digital perfection. Use specific **Film Stocks** (Kodak Vision3 5219) and define **Grain Texture**.
2. **COLOR FIDELITY:** Ensure West Bengal tones (oxidized iron, monsoon moss, yellow taxicabs) are graded for **Realistic Grit**.
3. **SUBTLETY:** Avoid oversaturated AI colors. Focus on high-dynamic range and split-toning for emotional depth.
4. ABSOLUTE FIRST LINE: A single-phrase "Stack Anchor" (Film Stock + Key LUT + Grain Profile).
5. **Syntax:** Output for the `[POST_PROCESS_STACK]` layer.
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
