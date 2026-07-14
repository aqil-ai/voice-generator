"""
LivePortrait Backend

Temporary implementation.
"""

from .base import BaseAvatarBackend


class LivePortraitBackend(BaseAvatarBackend):

    def __init__(self):
        super().__init__("LivePortrait")

    def generate(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
    ):
        print("LivePortrait backend selected.")
        print(f"Image : {image_path}")
        print(f"Audio : {audio_path}")
        print(f"Output: {output_path}")

        return output_path