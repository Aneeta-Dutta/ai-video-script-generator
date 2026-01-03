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

**Instructions (Hollywood Standard v1):**
1. **PSYCHOLOGICAL ANCHOR:** Output an `inner_monologue` for the character to guide the subtextual performance.
2. **SUB-DERMAL HISTORY:** Describe **Micro-scars**, **Visible Veins**, and **Progressive Perspiration** (sweat logic tied to scene intensity).
3. **PEFORMANCE MICRO-GESTURES:** Direct **eye saccades**, **vocal strain**, and **textural conflict** (soft skin vs jagged metal).
4. **NEGATIVE CONSTRAINTS:** NO generic AI facial symmetry, NO static "staring", NO stock expressions.
5. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Inner Monologue Motif] + [Sub-dermal Detail] + [Progressive Sweat Hook].
6. **SECOND LINE:** "CHARACTER STATE UPDATE: [Name]: [Physical/Emotional State]"
7. **PHYSICALITY & TEXTURE:** Describe the subject with sub-pixel industrial precision.
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
