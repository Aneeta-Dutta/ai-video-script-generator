"""
Core configuration management for AI Video Production System.

This module provides centralized configuration with environment variable support,
model settings, and agent configurations.
"""

import os
from typing import Optional
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Project root (go up from backend/core/config/ to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.absolute()

# Environment variables
def get_env(key: str, default: Optional[str] = None) -> str:
    """Get environment variable with optional default."""
    value = os.environ.get(key, default)
    if value is None:
        raise ValueError(f"Required environment variable {key} not set")
    return value


@dataclass
class APIConfig:
    """API configuration."""
    google_api_key: Optional[str] = None
    use_vertex_ai: bool = False
    gcp_project: Optional[str] = None
    gcp_location: str = "us-central1"
    
    @classmethod
    def from_env(cls) -> "APIConfig":
        """Load API configuration from environment."""
        # Check if using Vertex AI
        use_vertex_ai = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() == "true"
        
        if use_vertex_ai:
            # Vertex AI mode - requires project ID
            gcp_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not gcp_project:
                raise ValueError("GOOGLE_CLOUD_PROJECT must be set when using Vertex AI")
            
            return cls(
                use_vertex_ai=True,
                gcp_project=gcp_project,
                gcp_location=os.environ.get("GCP_LOCATION", "us-central1")
            )
        else:
            # API key mode
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY must be set when not using Vertex AI")
            
            return cls(
                google_api_key=api_key,
                use_vertex_ai=False
            )


@dataclass
class ModelConfig:
    """Model configuration for agents."""
    default_model: str = "gemini-2.0-flash-exp"
    research_model: Optional[str] = None
    production_model: Optional[str] = None
    temperature: float = 0.7
    max_retries: int = 3
    timeout: int = 60
    
    @property
    def get_research_model(self) -> str:
        """Get model for research agents."""
        return self.research_model or self.default_model
    
    @property
    def get_production_model(self) -> str:
        """Get model for production agents."""
        return self.production_model or self.default_model


@dataclass
class PathConfig:
    """Path configuration for various directories."""
    references_dir: Path
    outputs_dir: Path
    research_reports_dir: Path
    production_scripts_dir: Path
    sessions_dir: Path
    logs_dir: Path
    
    @classmethod
    def from_project_root(cls, root: Path) -> "PathConfig":
        """Create path configuration from project root."""
        outputs = root / "outputs"
        outputs.mkdir(exist_ok=True)
        
        return cls(
            references_dir=root / "production_references",  # Fixed: at root level, not in backend
            outputs_dir=outputs,
            research_reports_dir=outputs / "research_reports",
            production_scripts_dir=outputs / "production_scripts",
            sessions_dir=outputs / "sessions",
            logs_dir=root / "logs"
        )


@dataclass
class Settings:
    """Application settings."""
    api: APIConfig
    model: ModelConfig
    paths: PathConfig
    debug: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment and defaults."""
        # Ensure API key is available
        api = APIConfig.from_env()
        
        # Configure paths
        paths = PathConfig.from_project_root(PROJECT_ROOT)
        
        # Create necessary directories
        paths.outputs_dir.mkdir(exist_ok=True)
        paths.research_reports_dir.mkdir(exist_ok=True)
        paths.production_scripts_dir.mkdir(exist_ok=True)
        paths.sessions_dir.mkdir(exist_ok=True)
        paths.logs_dir.mkdir(exist_ok=True)
        
        # Model configuration
        model = ModelConfig(
            default_model=os.environ.get("DEFAULT_MODEL", "gemini-2.0-flash-exp"),
            temperature=float(os.environ.get("MODEL_TEMPERATURE", "0.7")),
            max_retries=int(os.environ.get("MAX_RETRIES", "3")),
            timeout=int(os.environ.get("TIMEOUT", "60"))
        )
        
        return cls(
            api=api,
            model=model,
            paths=paths,
            debug=os.environ.get("DEBUG", "false").lower() == "true",
            log_level=os.environ.get("LOG_LEVEL", "INFO")
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings


def reload_settings() -> Settings:
    """Reload settings (useful for testing)."""
    global _settings
    _settings = Settings.load()
    return _settings
