"""
Hoyte van Hoytema (DoP) Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "personas/dop_persona.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "cinematography_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Veo 3 optimization."""
    persona = load_persona()
    guide = load_guide()

    veo_3_instruction = """
---
## 📹 Veo 3 Protocol: Layer 3 - Lighting & Camera Physics
Your primary goal is to simulate **Ray-Tracing** and **Physical Lens Characteristics**.

**Instructions (Hollywood Standard v1):**
1. **LDS METADATA & FOCUS:** Specify **Focus Distance (cm)** and **DoF (mm)**. (e.g., "Focus: 120cm, DoF: 40mm").
2. **OPTICAL VIGNETTING & VINTAGE GATE:** Specify **1.5 stop vignetting** and **Mechanical Light Leaks** (e.g., "16mm Bolex gate amber-streak").
3. **HALATION / BLOOM / DECAY:** Distinguish between **Red-Channel Halation** and **Pro-Mist Bloom**. Apply **Inverse Square Law** for flare decay.
4. **VARIABLE SHUTTER & TEMPORAL BIAS:** Use **Shutter Angle** (45 to 180). Apply **Temporal Bias** for micro-textures (silk threads) to ensure flow consistency.
5. **ATMOSPHERIC DEPTH:** Specify **20% Contrast Falloff** for backgrounds beyond 15 meters.
6. **NEGATIVE CONSTRAINTS:** NO flat lighting, NO centered AI-default framing, NO oversaturated digital chroma.
7. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [LDS Focus] + [Gate Flare Logic] + [Temporal Bias Hook].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
