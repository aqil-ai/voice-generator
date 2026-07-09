import os
import random

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MUSIC_DIR = os.path.join(
    BASE_DIR,
    "music"
)


def get_music(style):

    if style == "None":
        return None

    folder = os.path.join(
        MUSIC_DIR,
        style.lower()
    )

    if not os.path.exists(folder):
        return None

    music_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".mp3")
    ]

    if len(music_files) == 0:
        return None

    return random.choice(music_files)