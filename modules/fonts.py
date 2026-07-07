import os
from PIL import ImageFont

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

FONT_DIR = os.path.join(BASE_DIR, "fonts")

FONT_CACHE = {}


def load_font(size, weight="Bold"):

    font_name = f"Poppins-{weight}.ttf"
    font_path = os.path.join(FONT_DIR, font_name)

    cache_key = (font_name, size)

    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]

    print("BASE_DIR:", BASE_DIR)
    print("FONT_DIR:", FONT_DIR)
    print("FONT PATH:", font_path)

    if not os.path.exists(font_path):
        raise FileNotFoundError(
            f"Font file not found:\n{font_path}"
        )

    font = ImageFont.truetype(font_path, size)

    FONT_CACHE[cache_key] = font

    return font