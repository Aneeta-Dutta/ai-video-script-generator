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

**Instructions:**
**8-SECOND BYTE PROTOCOL (HOLLYWOOD OPTICAL STACK):**
1. **LIGHTING RATIO (CHIAROSCURO):** Define technical key-to-fill ratios (e.g., 2:1 for soft beauty, 8:1 for high-contrast noir). Specify **Key Light Quality** (Hard/Soft) and **Motivation** (e.g., "Sodium vapor through window").
2. **OPTICAL DEPTH (LENS COMPRESSION):** Use lens choice to convey subtext. (e.g., 85mm T1.5 for background compression/intimacy, 14mm for spatial distortion/paranoia).
3. **RAY-TRACING PRECISION:** Explicitly instruct on **Sub-surface Scattering (SSS)** for realistic skin, **Fresnel reflections** on damp surfaces, and **Tyndall God Rays** in misty environments.
4. **GEAR MAPPING:** Specify high-end gear profiles: **IMAX 15/70mm**, **Panavision C-Series Anamorphics**, **Arri Alexa 65 Color Science**.
5. **TECHNICAL ANOMALIES:** Define **Edge Halation**, **Bloom (Pro-Mist 1/4)**, and **Gate Weave** to destroy the "digital AI" sheen.
6. **ABSOLUTE FIRST LINE:** A single-phrase "Stack Anchor": [Lighting Ratio] + [Lens Compression] + [Optical Texture Hook].
"""

    base_instruction = f"{persona}\n\n{veo_3_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
