"""
Kobiyal (Writer) Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "personas/writer_persona.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "dialogue_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Bengali and crispness optimization."""
    persona = load_persona()
    guide = load_guide()

    production_house_instruction = """
---
## ✍️ Production House Protocol: Crisp & Precise Bengali Script
Your objective is to deliver the final screenplay elements in a format optimized for a high-end production house.

**8-SECOND BYTE PROTOCOL (HOLLYWOOD PERFORMANCE STANDARDS):**
1. **PSYCHOLOGICAL SUBTEXT:** Specify the character's `inner_monologue` and **Gaze Direction**.
2. **ACOUSTIC OCCLUSION:** Define **Audio Occlusion logic** (e.g., muffled by wall) and **Reverb Profiles**.
3. **TONAL NUANCE:** Use sophisticated Kolkata Standard Bengali.
4. **NEGATIVE CONSTRAINTS:** NO robotic dialogue, NO generic English-to-Bengali literal translations (use idioms).

**OUTPUT SCHEMA:**
```json
{
  "scene_description_precise": "...",
  "spoken_dialogue": {
    "text_bengali": "...",
    "text_english_ref": "...",
    "inner_monologue": "...",
    "lip_sync_notes": "...",
    "gaze_direction": "...",
    "breath_markers": "...",
    "eye_saccade_intensity": 0.0,
    "accent_variant": "West Bengal Standard (Sophisticated/Urban)",
    "performance_intensity": 0.8
  },
  "background_soundscape": {
    "reverb_profile": "...",
    "audio_occlusion_logic": "...",
    "material_audio_cues": "...",
    "sfx_spatial": [
      {"clip": "...", "pos": "2 o'clock", "depth": "distant"}
    ]
  },
  "speaker_id": "...",
  "voice_dna_applied": "..."
}
```
"""

    base_instruction = f"{persona}\n\n{production_house_instruction}"

    if guide:
        return f"{base_instruction}\n\n# Reference Guide\n\n{guide}"

    return base_instruction
