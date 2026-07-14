"""
Avatar Engine
==============

Central engine responsible for coordinating the avatar generation
pipeline inside AqilAI Studio.

Version: 3.0
"""

from pathlib import Path
from datetime import datetime
from .config import AvatarConfig

class AvatarEngine:
    """
    Main Avatar Engine.

    This class will coordinate the complete avatar generation pipeline.

    Future Pipeline:

    Image
        ↓
    Voice
        ↓
    LivePortrait
        ↓
    Video Export
    """

    def __init__(self):

        self.config = AvatarConfig()
        self.status = "Ready"
        self.created_at = datetime.now()

    def info(self):
        """
        Returns engine information.
        """

        return {
            "Engine": self.config.engine_name,
            "Version": self.config.version,
            "Backend": self.config.backend,
            "Status": self.status,
            "Output Folder": str(self.config.output_dir),
            "Device": self.config.device,
            "FPS": self.config.fps,
            "Resolution": f"{self.config.width}x{self.config.height}"
            }

    def __str__(self):

        return (
            f"{self.config.engine_name} "
            f"(v{self.config.version}) "
            f"- Backend: {self.config.backend}"
            )