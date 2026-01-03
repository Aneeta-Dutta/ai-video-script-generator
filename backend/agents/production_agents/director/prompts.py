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
**8-SECOND BYTE PROTOCOL (FILM SCHOOL STANDARDS):**
1. **COMPOSITIONAL GEOMETRY:** Use motifs for subtext. Define **Negative Space** for isolation, **Triangular Framing** for tension, and **Leading Lines** for focus. Avoid centered "AI-defaults".
2. **MOTIVED KINETICS:** Camera movement must have narrative purpose (e.g., "Slow push only when the realization hits", "Low-angle power framing as Arindam asserts dominance").
3. **PEFORMANCE SUBTEXT:** Direct the actor's **vocal strain**, **gaze direction**, and **micro-gestural subtext** (e.g., "Arindam clenches his jaw before speaking, eyes darting to the shadow").
4. **NO-AI-MESS (HYPER-DENSITY):** Every frame must pass the "Master Shot" test. Describe pore-level sweat, fabric micro-vibrations, and realistic eye-light (catchlights).
5. **CULTURAL GROUNDING:** Authentically anchor the scene in **Kolkata Urban Brutalism** or **Rural Bengal Materiality**. Use specific regional material markers.
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Compositional Motif] + [Motived Movement] + [Performance Hook].
7. **SECOND LINE:** "CHARACTER STATE UPDATE: [Name]: [Physical/Emotional State]"
8. **PHYSICALITY & TEXTURE:** Describe the subject with industrial precision (e.g., "oily sheen on forehead", "frayed threads on the khadi collar").
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
