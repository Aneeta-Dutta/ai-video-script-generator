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
    """Construct the full instruction for the agent."""
    persona = load_persona()
    guide = load_guide()
    
    if guide:
        # Combine persona with guide
        return f"""{persona}

---
# Reference Guide

{guide}
"""
    
    return persona
