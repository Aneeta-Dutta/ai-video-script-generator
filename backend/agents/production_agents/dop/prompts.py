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
    
    return persona_path.read_text(encoding='utf-8')


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "cinematography_guide.md"
    
    if not guide_path.exists():
        return ""
    
    return guide_path.read_text(encoding='utf-8')


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Veo 3 optimization."""
    persona = load_persona()
    guide = load_guide()
    
    veo_3_instruction = """
---
## 📹 Veo 3 Protocol: Layer 3 - Lighting & Camera Physics
Your primary goal is to simulate **Ray-Tracing** and **Physical Lens Characteristics**.

**Instructions:**
**8-SECOND BYTE PROTOCOL (REALISTIC LENS PHYSICS):**
1. **PHYSICAL LENS CHARACTERISTICS:** Focus on **Ray-Tracing** accuracy. No flat AI lighting. Use sub-surface scattering for skin.
2. **CINEMATOGRAPHY BIBLE:** Use specific techniques from `cinematography_guide.md`. Focus on **Performance-Driven Framing** (Close-ups that capture facial twitches).
3. **Lens Specs:** Specify focal length (35mm Anamorphic, 50mm Prime), Aperture (f/1.4), and real-world Shutter Angle (180 degree).
4. **Optical Anomalies:** Include realistic lens flare, halation, and chromatic aberration to break the "perfect AI" look.
5. ABSOLUTE FIRST LINE: A single-phrase "Stack Anchor" (Lighting Setup + Camera Movement + Lens Choice).
6. **Lighting Engine:** Use Rembrandt Lighting, Negative Fill, and Tyndall Effects with technical precision.
"""
    
    base_instruction = f"{persona}\n\n{veo_3_instruction}"
    
    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"
    
    return base_instruction
