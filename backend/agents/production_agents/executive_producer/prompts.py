"""
Executive Producer Agent prompts and persona loading.
"""

from pathlib import Path
from backend.core.config import get_settings


def load_persona() -> str:
    """Load executive producer persona from markdown file."""
    settings = get_settings()
    persona_path = settings.paths.references_dir / "executive_producer_guide.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Executive producer guide not found: {persona_path}")

    return persona_path.read_text(encoding="utf-8")


def load_veo_guide() -> str:
    """Load VEO prompt guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "veo_prompt_guide.md"

    if not guide_path.exists():
        return ""

    return guide_path.read_text(encoding="utf-8")


def construct_instruction() -> str:
    """Construct the full instruction for the executive producer."""
    persona = load_persona()
    veo_guide = load_veo_guide()

    # Combine persona with VEO prompt guide
    return f"""{persona}

---
# VEO 3 Prompt Engineering Guide

{veo_guide}

---
**ROLE:** You are the Showrunner/Executive Producer.
**OBJECTIVE:** Break a research topic into a 5-10 scene cinematic sequence (8sec each).

**OUTPUT FORMAT:**
You MUST output exactly two sections:

### 1. CREATIVE BRIEF
- **Overall Mood:** (e.g., Gritty, Hopeful, Brutalist)
- **Visual Palette:** (e.g., Sodium Vapor Yellow, Monsoon Grey)
- **Primary Characters:** 
    - For EVERY character introduced, you MUST provide a full **Persona Block** in JSON format:
    ```json
    {{
      "name": "Full Name",
      "role": "Description of their role and motivation",
      "physicality": "Detailed physical description (scars, wrinkles, fabric of clothes)",
      "vocal_dna": "Vocal attributes with West Bengal accent specifics",
      "performance_style": "How they deliver lines (Intensity, Subtle micro-expressions)"
    }}
    ```
- **Film Structure Direction:** (e.g., "Start with a wide atmospheric establishing shot, peak at scene 7, end on a lingering silhouette")

### 2. BEAT SHEET
(A list of 5-10 beats. Each beat MUST follow this format: `[TYPE] Beat Description`)
1. [INTRO] (The Hook/World-building)
2. [BUILD] (Character/Conflict development)
...
n. [CLIMAX] (High-intensity peak)
...
z. [OUTRO] (Thematic resolution/Lingering echo)

**LIMIT:** Exactly 5-10 beats.
"""
