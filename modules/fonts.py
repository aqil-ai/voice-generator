import os
from PIL import ImageFont

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FONT_DIR = os.path.join(
    BASE_DIR,
    "fonts"
)

FONT_CACHE = {}


def load_font(
    size,
    weight="Bold"
):

    font_name = f"Poppins-{weight}.ttf"

    font_path = os.path.join(
        FONT_DIR,
        font_name
    )

    cache_key = (
        font_name,
        size
    )

    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]

    try:

        font = ImageFont.truetype(
            font_path,
            size
        )

    except Exception:

        font = ImageFont.load_default()

    FONT_CACHE[cache_key] = font

    return font