"""
Character Persona Manager for persistent character profiles.

Handles saving, loading, and searching for character personas in the Persona DB.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from backend.core.config import get_settings


class CharacterPersonaManager:
    """Manages character personas for narrative and visual consistency."""

    def __init__(self):
        self.settings = get_settings()
        self.db_dir = self.settings.paths.persona_db_dir
        self.db_dir.mkdir(parents=True, exist_ok=True)

    def save_persona(self, name: str, role: str, persona_data: Dict[str, Any]) -> Path:
        """Save or update a character persona."""
        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = self.db_dir / filename

        # Merge if exists
        data = self.get_persona(name) or {}
        data.update({"name": name, "role": role, "profile": persona_data})

        filepath.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return filepath

    def get_persona(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a character persona by name."""
        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = self.db_dir / filename

        if filepath.exists():
            return json.loads(filepath.read_text(encoding="utf-8"))
        return None

    def list_all_personas(self) -> List[Dict[str, Any]]:
        """List all available personas in the DB."""
        personas = []
        for file in self.db_dir.glob("*.json"):
            try:
                personas.append(json.loads(file.read_text(encoding="utf-8")))
            except:
                pass
        return personas

    def format_persona_context(self, names: List[str]) -> str:
        """Format a list of personas into a context string for agents."""
        context = []
        for name in names:
            persona = self.get_persona(name)
            if persona:
                summary = f"NAME: {persona['name']}\nROLE: {persona['role']}\nPROFILE: {json.dumps(persona['profile'], indent=2)}"
                context.append(summary)

        return (
            "\n---\n".join(context)
            if context
            else "No existing personas found for these characters."
        )


# Singleton instance
_persona_manager = None


def get_persona_manager() -> CharacterPersonaManager:
    """Get singleton persona manager instance."""
    global _persona_manager
    if _persona_manager is None:
        _persona_manager = CharacterPersonaManager()
    return _persona_manager
