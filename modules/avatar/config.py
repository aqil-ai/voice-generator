"""
Avatar Configuration
====================

Central configuration for the Avatar Engine.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AvatarConfig:
    """
    Configuration used by the Avatar Engine.
    """

    # Engine
    engine_name: str = "AqilAI Avatar Engine"
    version: str = "3.0"

    # Avatar Backend
    backend: str = "LivePortrait"

    # Device
    device: str = "auto"      # auto / cpu / cuda

    # Output
    output_dir: Path = Path("downloads")
    temp_dir: Path = Path("temp")

    # Video
    fps: int = 30
    width: int = 1080
    height: int = 1920
    video_format: str = "mp4"

    # Supported files
    image_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    audio_extensions = (
        ".wav",
        ".mp3",
    )