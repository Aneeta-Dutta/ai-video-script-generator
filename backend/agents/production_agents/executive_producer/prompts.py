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
    
    return persona_path.read_text(encoding='utf-8')


def load_veo_guide() -> str:
    """Load VEO prompt guide from markdown file."""
    settings = get_settings()
    guide_path = settings.paths.references_dir / "veo_prompt_guide.md"
    
    if not guide_path.exists():
        return ""
    
    return guide_path.read_text(encoding='utf-8')


def construct_instruction() -> str:
    """Construct the full instruction for the executive producer."""
    persona = load_persona()
    veo_guide = load_veo_guide()
    
    # Combine persona with VEO prompt guide
    return f"""{persona}

---
# VEO 3 Prompt Engineering Guide

{veo_guide}
"""
