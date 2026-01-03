"""
Output storage manager for local and cloud environments.

Handles saving research reports, production scripts, and session data
to local filesystem or cloud storage (GCS).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import os

from backend.core.config import get_settings


class OutputManager:
    """Manages output storage with support for local and cloud storage."""

    def __init__(self, use_cloud: bool = False):
        """
        Initialize output manager.

        Args:
            use_cloud: If True, use GCS for storage. If False, use local filesystem.
        """
        self.settings = get_settings()
        self.use_cloud = (
            use_cloud or os.getenv("USE_CLOUD_STORAGE", "false").lower() == "true"
        )

        # Initialize cloud storage if needed
        self.gcs_client = None
        self.bucket = None

        if self.use_cloud:
            try:
                from google.cloud import storage

                self.gcs_client = storage.Client(
                    project=self.settings.api.google_cloud_project
                )
                bucket_name = os.getenv(
                    "GCS_BUCKET_NAME",
                    f"{self.settings.api.google_cloud_project}-outputs",
                )
                self.bucket = self.gcs_client.bucket(bucket_name)
            except Exception as e:
                print(f"Warning: Could not initialize cloud storage: {e}")
                print("Falling back to local storage")
                self.use_cloud = False

    def save_research_report(
        self, topic: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save research report.

        Args:
            topic: Research topic
            content: Report content
            metadata: Optional metadata (session_id, timestamp, etc.)

        Returns:
            Path or URL to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = self._get_slug(topic)
        filename = f"research_{slug}_{timestamp}.md"

        # Add metadata header to content
        full_content = self._add_metadata_header(content, metadata, "Research Report")

        if self.use_cloud:
            path = self._save_to_cloud(f"research_reports/{filename}", full_content)
        else:
            path = self._save_to_local(
                self.settings.paths.research_reports_dir, filename, full_content
            )

        self._update_manifest("research", topic, path, metadata)
        return path

    def save_production_script(
        self, topic: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save production script.

        Args:
            topic: Topic
            content: Script content
            metadata: Optional metadata

        Returns:
            Path or URL to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = self._get_slug(topic)
        filename = f"prod_{slug}_{timestamp}.md"

        # Add metadata header
        full_content = self._add_metadata_header(content, metadata, "Production Script")

        if self.use_cloud:
            path = self._save_to_cloud(f"production_scripts/{filename}", full_content)
        else:
            path = self._save_to_local(
                self.settings.paths.production_scripts_dir, filename, full_content
            )

        self._update_manifest("production", topic, path, metadata)
        return path

    def save_session_data(self, session_id: str, data: Dict[str, Any]) -> str:
        """
        Save session data as JSON.

        Args:
            session_id: Session ID
            data: Session data dictionary

        Returns:
            Path or URL to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic = data.get("project_metadata", {}).get("topic", "unknown")
        slug = self._get_slug(topic)
        filename = f"session_{slug}_{timestamp}.json"

        content = json.dumps(data, indent=2, ensure_ascii=False)

        if self.use_cloud:
            path = self._save_to_cloud(f"sessions/{filename}", content)
        else:
            path = self._save_to_local(
                self.settings.paths.sessions_dir, filename, content
            )

        self._update_manifest("session", topic, path, data.get("project_metadata", {}))
        return path

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename to remove invalid characters."""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")

        # Limit length
        if len(name) > 50:
            name = name[:50]

        return name.strip().replace(" ", "_")

    def _add_metadata_header(
        self, content: str, metadata: Optional[Dict[str, Any]], doc_type: str
    ) -> str:
        """Add metadata header to document."""
        if not metadata:
            metadata = {}

        metadata["generated_at"] = datetime.now().isoformat()
        metadata["document_type"] = doc_type

        header = f"""---
# {doc_type}
# Generated: {metadata['generated_at']}
"""
        for key, value in metadata.items():
            if key not in ["generated_at", "document_type"]:
                header += f"# {key}: {value}\n"

        header += "---\n\n"

        return header + content

    def _get_slug(self, topic: str) -> str:
        """Create a URL-safe slug from a topic."""
        import re

        topic = topic.lower()
        # Remove special markdown or long research titles
        if topic.startswith("# research report:"):
            topic = topic.replace("# research report:", "").strip()
        topic = re.sub(r"[^a-z0-9\s-]", "", topic)
        topic = re.sub(r"\s+", "_", topic).strip("_")
        return topic[:40]

    def _update_manifest(
        self, entry_type: str, topic: str, path: str, metadata: Dict[str, Any]
    ) -> None:
        """Update the output manifest tracking file."""
        manifest_path = self.settings.paths.outputs_dir / "MANIFEST.json"
        readme_path = self.settings.paths.outputs_dir / "README.md"

        # Update JSON Manifest
        manifest = []
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
            except:
                manifest = []

        manifest.append(
            {
                "type": entry_type,
                "topic": topic,
                "path": path,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata,
            }
        )

        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Update Human-Readable README
        readme_content = "# 🎥 AI Video Production: Output Hub\n\n"
        readme_content += (
            "Track all generated research, scripts, and production sessions here.\n\n"
        )
        readme_content += "## 🚀 Recent Deliveries\n\n"
        readme_content += "| Timestamp | Type | Topic | File |\n"
        readme_content += "|-----------|------|-------|------|\n"

        for entry in reversed(manifest[-20:]):  # Last 20
            ts = entry["timestamp"][:16].replace("T", " ")
            filename = Path(entry["path"]).name
            readme_content += f"| {ts} | {entry['type'].upper()} | {entry['topic'][:50]} | [{filename}]({entry['path']}) |\n"

        readme_path.write_text(readme_content)

    def _save_to_local(self, directory: Path, filename: str, content: str) -> str:
        """Save to local filesystem."""
        directory.mkdir(parents=True, exist_ok=True)
        filepath = directory / filename
        filepath.write_text(content, encoding="utf-8")
        return str(filepath.absolute())

    def _save_to_cloud(self, blob_path: str, content: str) -> str:
        """Save to Google Cloud Storage."""
        try:
            blob = self.bucket.blob(blob_path)
            blob.upload_from_string(content, content_type="text/plain")
            return f"gs://{self.bucket.name}/{blob_path}"
        except Exception as e:
            print(f"Error saving to cloud: {e}")
            # Fallback to local
            parts = blob_path.split("/")
            directory = Path("outputs") / parts[0]
            filename = parts[-1]
            return self._save_to_local(directory, filename, content)

    def list_outputs(self, output_type: str = "all") -> list:
        """
        List all outputs of a given type.

        Args:
            output_type: 'research', 'production', 'sessions', or 'all'

        Returns:
            List of file paths or URLs
        """
        outputs = []

        if self.use_cloud:
            # List from GCS
            prefixes = {
                "research": "research_reports/",
                "production": "production_scripts/",
                "sessions": "sessions/",
                "all": "",
            }
            prefix = prefixes.get(output_type, "")
            blobs = self.bucket.list_blobs(prefix=prefix)
            outputs = [f"gs://{self.bucket.name}/{blob.name}" for blob in blobs]
        else:
            # List from local filesystem
            dirs = {
                "research": self.settings.paths.research_reports_dir,
                "production": self.settings.paths.production_scripts_dir,
                "sessions": self.settings.paths.sessions_dir,
            }

            if output_type == "all":
                for dir_path in dirs.values():
                    if dir_path.exists():
                        outputs.extend(
                            [
                                str(f.absolute())
                                for f in dir_path.iterdir()
                                if f.is_file()
                            ]
                        )
            else:
                dir_path = dirs.get(output_type)
                if dir_path and dir_path.exists():
                    outputs = [
                        str(f.absolute()) for f in dir_path.iterdir() if f.is_file()
                    ]

        return sorted(outputs, reverse=True)  # Most recent first


# Singleton instance
_output_manager = None


def get_output_manager(use_cloud: Optional[bool] = None) -> OutputManager:
    """
    Get singleton output manager instance.

    Args:
        use_cloud: Override cloud storage setting

    Returns:
        OutputManager instance
    """
    global _output_manager

    if _output_manager is None or use_cloud is not None:
        _output_manager = OutputManager(use_cloud=use_cloud or False)

    return _output_manager
