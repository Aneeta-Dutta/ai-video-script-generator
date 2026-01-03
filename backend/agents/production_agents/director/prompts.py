"""
Christopher Nolan (Director) Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "personas/director_persona.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "director_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Veo 3 optimization."""
    persona = load_persona()
    guide = load_guide()

    veo_3_instruction = """
---
## 🎥 Veo 3 Protocol: Layer 1 - Subject Anchor & Action Vector
Your primary goal is to define the **Subject Anchor** and **Action Vector** using the **Nolan Protocol (Hyper-Density)**.

**Instructions:**
**8-SECOND BYTE PROTOCOL (REALISM & CRAFTSMANSHIP):**
1. **NO-AI-MESS:** Avoid generic "AI looks". Focus on **Hyper-Realistic Craftsmanship**. Every frame must look like high-budget cinema.
2. **KINETIC VISION:** Use `cinematography_guide.md`. Focus on **Realistic Performance** where actors deliver intense, grounded roles.
3. **AUDIO-VISUAL FOCUS:** For spoken dialogue, describe the character's facial muscles, lip movement, and vocal strain.
4. **CULTURAL AUTHENTICITY:** Ground everything in **West Bengal / Kolkata** aesthetics. Use standard Bengali cultural markers.
5. **DETAIL DENSITY:** Describe pore-level skin detail, micro-fuzz on fabrics, dust motes in light, and natural skin micro-movements (sweat, twitch).
6. ABSOLUTE FIRST LINE: A single-phrase "Stack Anchor" (Subject + Kinetic Movement + Detail Hook).
7. SECOND LINE (Optional): "CHARACTER STATE UPDATE: [State]"
8. **Physicality:** Describe the subject with micro-texture (scars, pores, fabric weave).
9. **Performance Direction:** Instruct the actor on their specific emotional delivery (e.g., "Arindam delivers with a quiet, suppressed rage").
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
