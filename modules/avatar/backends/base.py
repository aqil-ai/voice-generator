"""
Base Avatar Backend

Every avatar backend must inherit from this class.
"""

from abc import ABC, abstractmethod


class BaseAvatarBackend(ABC):
    """
    Abstract base class for all avatar backends.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
    ):
        """
        Generate a talking avatar.

        Parameters
        ----------
        image_path : str
            Source portrait image.

        audio_path : str
            Narration audio.

        output_path : str
            Final output video.

        Returns
        -------
        str
            Path to generated video.
        """
        pass

    def info(self):
        return {
            "backend": self.name
        }