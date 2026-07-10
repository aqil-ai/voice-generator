from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)
import random
import uuid
from modules.image_engine import compose_image
from modules.fonts import load_font
from PIL import Image, ImageDraw, ImageFont
import textwrap
from PIL import ImageFilter
from moviepy import AudioFileClip, CompositeAudioClip
from moviepy import concatenate_audioclips
from modules.audio_engine import build_audio

VIDEO_SETTINGS = {

    "YouTube Long": {
        "width": 1280,
        "height": 720,
        "font": 45,
        "caption_y": "bottom",
        "zoom": 1.02
    },

    "YouTube Shorts": {
        "width": 1080,
        "height": 1920,
        "font": 70,
        "caption_y": "bottom",
        "zoom": 1.05
    },

    "TikTok": {
        "width": 1080,
        "height": 1920,
        "font": 75,
        "caption_y": "center",
        "zoom": 1.08
    },

    "Instagram Reel": {
        "width": 1080,
        "height": 1920,
        "font": 70,
        "caption_y": "bottom",
        "zoom": 1.05
    },

    "Netflix Documentary": {
        "width": 1920,
        "height": 1080,
        "font": 55,
        "caption_y": "bottom",
        "zoom": 1.01
    }

}

def make_caption(
        text, 
        width=1280, 
        height=250,
        video_type="YouTube Long",
        caption_style="Yellow",
        active_word=None
        ):

    img = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    
    if caption_style == "Yellow":
        text_color = "yellow"
        stroke_color = "black"

    elif caption_style == "White":
        text_color = "white"
        stroke_color = "black"

    elif caption_style == "Red":
        text_color = "red"
        stroke_color = "black"

    elif caption_style == "Blue":
        text_color = "cyan"
        stroke_color = "black"

    elif caption_style == "Neon Green":
        text_color = "lime"
        stroke_color = "black"
    else:
        text_color = "yellow"
        stroke_color = "black"
    font_size = VIDEO_SETTINGS[video_type]["font"]
    font = load_font(
        font_size,
        "Bold"
    )
    # font = ImageFont.truetype(
    #     
    #     font_size
    # )
    words_list = text.split()

    total_width = 0

    for w in words_list:
        bbox = draw.textbbox(
            (0, 0),
            w,
            font=font
        )
        total_width += (bbox[2] - bbox[0]) + 20

    x = (width - total_width) / 2
    y = (height - font_size) / 2

    for w in words_list:
        current_color = "white"
        # print(f"WORD=[{w}] ACTIVE=[{active_word}]")
        if active_word and w.strip().lower() == active_word.strip().lower():
            # print("MATCH FOUND")
        # if active_word and w.lower() == active_word.lower():
            current_color = text_color

        draw.text(
            (x, y),
            w,
            font=font,
            fill=current_color,
            stroke_width=3,
            stroke_fill=stroke_color
        )
        bbox = draw.textbbox(
            (x, y),
            w,
            font=font
        )
        x += (bbox[2] - bbox[0]) + 20

    path = "caption.png"
    # path = f"caption_{uuid.uuid4().hex}.png"

    img.save(path, "PNG")

    return path

# def prepare_vertical_image(image_path):

#     img = Image.open(image_path).convert("RGB")

#     # Background
#     bg = img.resize((1080, 1920))
#     bg = bg.filter(ImageFilter.GaussianBlur(25))

#     # Main image
#     main = img.copy()
#     main.thumbnail((1080, 1920))

#     x = (1080 - main.width) // 2
#     y = (1920 - main.height) // 2

#     bg.paste(main, (x, y))

#     output = image_path.replace(".jpg", "_vertical.jpg")
#     bg.save(output)

#     return output

def create_video(
        images, 
        captions, 
        words, 
        audio_path, 
        output_path, 
        caption_style, 
        video_type, 
        animation_style, 
        animation_speed, 
        bg_music_path=None, 
        music_volume=20
        ):
    print("VIDEO TYPE =", video_type)
    settings = VIDEO_SETTINGS[video_type]

    video_width = settings["width"]
    video_height = settings["height"]

    zoom = settings["zoom"]
    # Animation Speed

    if animation_speed == "Slow":
        speed = 0.05

    elif animation_speed == "Normal":
        speed = 0.10

    else:
        speed = 0.20

    caption_position = settings["caption_y"]
    audio = AudioFileClip(audio_path)

    total_words = sum(len(scene.split()) for scene in captions)
    scene_durations = []
    for scene in captions:
        word_count = len(scene.split())
        scene_duration = (word_count / total_words) * audio.duration
        scene_durations.append(scene_duration)

    clips = []
    if video_type == "YouTube Long":
        video_width = 1280
        video_height = 720

    elif video_type == "YouTube Shorts":
        video_width = 1080
        video_height = 1920

    elif video_type == "TikTok":
        video_width = 1080
        video_height = 1920

    elif video_type == "Instagram Reel":
        video_width = 1080
        video_height = 1920

    else:
        video_width = 1280
        video_height = 720

    for i, img in enumerate(images):
        img = compose_image(
            img,
            video_type
        )
        print("Images:", len(images))
        print("Captions:", len(captions))
        print("Words:", len(words))
        # if video_type in [
        #     "YouTube Shorts",
        #     "TikTok",
        #     "Instagram Reel"
        # ]:
        #     img = prepare_vertical_image(img)
        duration = scene_durations[i]

        image_clip = (
            ImageClip(img)
                # .resized(height=video_height)
                # .resized(
                #     width=video_width,
                #     height=video_height
            
            # .resized(
            #     width=video_width,
            #     height=video_height)
            .with_duration(duration)
            # .with_position ("center", caption_position)
            # .crop(width=1280, height=720, x_center="center", y_center="center") 
        )
        # -------------------------
# NONE
# -------------------------
        if animation_style == "None":

            pass
        # -------------------------
# RANDOM
# -------------------------
        elif animation_style == "Random":

            animation_style = random.choice([
                "Zoom In",
                "Zoom Out",
                "Ken Burns"
            ])


# -------------------------
# ZOOM IN
# -------------------------
        if animation_style == "Zoom In":

            image_clip = image_clip.resized(
            lambda t: 1 + speed * t
            )


# -------------------------
# ZOOM OUT
# -------------------------
        elif animation_style == "Zoom Out":

            image_clip = image_clip.resized(
            lambda t: zoom - speed * t
            )


# -------------------------
# KEN BURNS
# -------------------------
        elif animation_style == "Ken Burns":

            image_clip = (
                image_clip
                .resized(
                lambda t: 1 + speed * t
                )
                .with_position(
                    lambda t: (-20*t, -10*t)
    
            )
        )
    
    #     zoom_type = random.choice([
    #         "in",
    #         "out"
    #     ])
    #     if zoom_type == "in":
    #         image_clip = image_clip.resized(
    #             lambda t: 1 + (zoom - 1) * (t / duration)
    #         )

    #     else:
    #         image_clip = image_clip.resized(
    #             lambda t: zoom - (zoom - 1) * (t / duration)
    # )
        
    #     zoom_type = random.choice([
    #         "zoom_in",
    #         "zoom_out",
    #         "slow_zoom_in",
    #         "slow_zoom_out"
    #     ])
    #     if zoom_type == "zoom_in":
    #         image_clip = (
    #             ImageClip(img)
    #             .resized(width=1280, height=720)
    #             .with_duration(duration)
    #             .resized(lambda t: 1 + 0.05 * t)
    #         )
    #     elif zoom_type == "zoom_out":
    #         image_clip = (
    #             ImageClip(img)
    #             .resized(width=1280, height=720)
    #             .with_duration(duration)
    #             .resized(lambda t: 1.20 - 0.05 * t)
    #         )
    #     elif zoom_type == "slow_zoom_in":
    #         image_clip = (
    #             ImageClip(img)
    #             .resized(width=1280, height=720)
    #             .with_duration(duration)
    #             .resized(lambda t: 1 + 0.02 * t)
    #         )
    # else:
    #     image_clip = (
    #         ImageClip(img)
    #         .resized(width=1280, height=720)
    #         .with_duration(duration)
    #         .resized(lambda t: 1.10 - 0.02 * t)
    #     )


        caption_path = make_caption(
            captions[i],
            video_type=video_type,
            caption_style=caption_style,
            active_word=words[i]["text"]
        )


        caption_clip = (
            ImageClip(caption_path)
            .with_duration(duration)
            .with_position(
                ("center","bottom")
            )
        )


        final_clip = image_clip
        clips.append(final_clip)


    video = concatenate_videoclips(
        clips,
        method="compose"
    )

    word_clips = []
    chunk_size = 3
    for i in range(len(words)):
        start_index = max(0, i - 1)
        end_index = min(len(words), start_index + chunk_size)
        chunk_words = []
        for j in range(start_index, end_index):
            if j == i:
                chunk_words.append(
                    words[j]["text"].upper()
                )
            
            else:
                chunk_words.append(
                    words[j]["text"].lower()
                )
            
        caption_text = " ".join(chunk_words)
        caption_path = make_caption(
        caption_text,
        video_type=video_type,
        caption_style=caption_style,
        active_word=words[i]["text"]
    )
        clip = (
        ImageClip(caption_path)
        .with_start(words[i]["start"])
        .with_duration(
            words[i]["end"] - words[i]["start"]
        )
        .with_position(
            ("center", "bottom")
        )
    )
        word_clips.append(clip)

    # word_clips = []
    # for word in words:
    #     caption_path = make_caption(
    #         word["text"],
    #         caption_style=caption_style
    #     )
        # clip = (
        #     ImageClip(caption_path)
        #     .with_start(word["start"])
        #     .with_duration(
        #         word["end"] - word["start"]
        #     )
        #     .with_position(
        #         ("center", "bottom")
        #     )
        # )
        # word_clips.append(clip)
    video = CompositeVideoClip(
        [video] + word_clips,
        size=(video_width, video_height)
    )
    # video = video.with_audio(audio)
    # ===========================
# Background Music
# ===========================
      
    final_audio = build_audio(
        voice_path=audio_path,
        bg_music_path=bg_music_path,
        music_volume=music_volume
        )
#     final_audio = audio
#     if bg_music_path is not None:
#         try:
#             bg_music = AudioFileClip(bg_music_path)

#             # =====================================
# # # Auto Loop Music
# # # =====================================

#             if bg_music.duration < audio.duration:
#                 loops = int(audio.duration // bg_music.duration) + 1
#                 bg_music = concatenate_audioclips(
#                     [bg_music] * loops
#                     )

# # Trim to narration length
#             bg_music = bg_music.subclipped(
#                 0,
#                 audio.duration
#                 )

# # Apply user volume
#             bg_music = bg_music.with_volume_scaled(
#                 music_volume / 100
#                 )

# # Merge voice + music
#             final_audio = CompositeAudioClip(
#                 [
#                     audio,
#                     bg_music
#                     ]
#                     )
#             # bg_music = AudioFileClip(bg_music_path)
#             # bg_music = bg_music.with_volume_scaled(
#             # music_volume / 100
#             # )
#             # final_audio = CompositeAudioClip(
#             #     [
#             #         audio,
#             #         bg_music
#             #         ]
#             #         )
#         except Exception as e:
#             print("Music Error:", e)

    video = video.with_audio(final_audio)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=[
        "-pix_fmt",
        "yuv420p"
        ]
        )
    video.close()
    try:
        audio.close()
    except:
        pass
    try:
        final_audio.close()
    except:
        pass
    return output_path

def create_custom_video(
        images,
        captions,
        words,
        audio_path,
        output_path,
        caption_style,
        video_type,
        animation_style,
        animation_speed,
        bg_music_path=None, 
        music_volume=20
        ):
    return create_video(
        images,
        captions,
        words,
        audio_path,
        output_path,
        caption_style,
        video_type,
        animation_style,
        animation_speed,
        bg_music_path=None, 
        music_volume=20
        )