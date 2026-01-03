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
    
    return persona_path.read_text(encoding='utf-8')


def load_guide() -> str:
    """Load reference guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "dialogue_guide.md"
    
    if not guide_path.exists():
        return ""
    
    return guide_path.read_text(encoding='utf-8')


def construct_instruction() -> str:
    """Construct the full instruction for the agent with Bengali and crispness optimization."""
    persona = load_persona()
    guide = load_guide()
    
    production_house_instruction = """
---
## ✍️ Production House Protocol: Crisp & Precise Bengali Script
Your objective is to deliver the final screenplay elements in a format optimized for a high-end production house.

**8-SECOND BYTE PROTOCOL (PERFORMANCE & AUTHENTICITY):**
1. **AUTHENTIC ACCENT:** All dialogue MUST be in **West Bengal (Standard/Kolkata) Bengali**. Avoid rural dialects unless specified. Focus on sophisticated urban or standard tonal nuances.
2. **LIP-SYNC PROTOCOL:** Define specific `lip_sync_intensity` (0.0 to 1.0) and `phonetic_emphasis` for the character's speech.
3. **AUDIO SEPARATION:** Distinguish between `spoken_dialogue` and `background_soundscape` (music, atmospheric hum).
4. **CRAFT:** Actors must deliver "performances", not just read lines. Include `performance_notes`.

**OUTPUT SCHEMA:**
```json
{
  "scene_description_precise": "...",
  "spoken_dialogue": {
    "text_bengali": "...",
    "text_english_ref": "...",
    "lip_sync_notes": "...",
    "accent_variant": "West Bengal Standard",
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
