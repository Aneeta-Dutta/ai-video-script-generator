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
1. **SUBTEXT VS. TEXT:** Dialogue must carry an internal weight. Specify the **Unspoken Emotion** and **Gaze Direction** (e.g., "Arindam maintains eye contact but his pupils dilate as he lies").
2. **REGIONAL TONAL NUANCE:** Use sophisticated **Kolkata Standard Bengali** with specific class-based or generational tonal markers.
3. **LIP-SYNC & MICRO-GESTURE:** In `lip_sync_notes`, include micro-movements like "jaw clenching", "lip quivering", or "rapid blinking".
4. **PERFORMANCE INTENSITY:** Use a dynamic range (0.1 for a whisper/silence to 1.0 for a scream/climax).

**OUTPUT SCHEMA:**
```json
{
  "scene_description_precise": "...",
  "spoken_dialogue": {
    "text_bengali": "...",
    "text_english_ref": "...",
    "lip_sync_notes": "...",
    "gaze_direction": "...",
    "subtext_internal": "...",
    "accent_variant": "West Bengal Standard (Sophisticated/Urban)",
    "performance_intensity": 0.8
  },
  "background_soundscape": {
    "music_mood": "...",
    "ambient_noise": "...",
    "sfx": "..."
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
