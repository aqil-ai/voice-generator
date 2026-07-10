from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
)

from modules.video import (
    VIDEO_SETTINGS,
    make_caption,
)

from modules.image_engine import compose_image
from modules.audio_engine import build_audio

import random


def create_custom_video(
    scenes,
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
    """
    scenes format:

    [
        {
            "text": "...",
            "images": [
                "temp/scene_0_0.jpg",
                "temp/scene_0_1.jpg"
            ]
        }
    ]
    """

    settings = VIDEO_SETTINGS[video_type]

    video_width = settings["width"]
    video_height = settings["height"]

    zoom = settings["zoom"]

    
    audio = AudioFileClip(audio_path)

    total_words = sum(
        len(scene["text"].split())
        for scene in scenes
    )

    scene_durations = []

    for scene in scenes:

        duration = (
            len(scene["text"].split())
            / total_words
        ) * audio.duration

        scene_durations.append(duration)

    clips = []
    current_time = 0
    for scene_index, scene in enumerate(scenes):

        scene_duration = scene_durations[scene_index]

        scene_images = scene["images"]

        if len(scene_images) == 0:
            continue

        image_duration = scene_duration / len(scene_images)

        for image_path in scene_images:

            img = compose_image(
                image_path,
                video_type
            )

            image_clip = (
                ImageClip(img)
                .with_duration(image_duration)
            )
                        # Animation Speed
            if animation_speed == "Slow":
                zoom_value = 1.08

            elif animation_speed == "Fast":
                zoom_value = 1.25

            else:
                zoom_value = zoom


            # Animation Style

            if animation_style == "None":

                pass


            elif animation_style == "Zoom In":

                image_clip = image_clip.resized(
                    lambda t: 1 + (zoom_value - 1) * (t / image_duration)
                )


            elif animation_style == "Zoom Out":

                image_clip = image_clip.resized(
                    lambda t: zoom_value - (zoom_value - 1) * (t / image_duration)
                )


            elif animation_style == "Random":

                random_style = random.choice(
                    [
                        "Zoom In",
                        "Zoom Out",
                    ]
                )

                if random_style == "Zoom In":

                    image_clip = image_clip.resized(
                        lambda t: 1 + (zoom_value - 1) * (t / image_duration)
                    )

                else:

                    image_clip = image_clip.resized(
                        lambda t: zoom_value - (zoom_value - 1) * (t / image_duration)
                    )


            elif animation_style == "Ken Burns":

                image_clip = image_clip.resized(
                    lambda t: 1 + (zoom_value - 1) * (t / image_duration)
                )
            image_clip = image_clip.with_start(current_time)
                

            clips.append(image_clip)
            current_time += image_duration
        video = CompositeVideoClip(
            clips,
        size=(video_width, video_height)
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

    video = CompositeVideoClip(
        [video] + word_clips,
        size=(video_width, video_height)
    )

    final_audio = build_audio(
        audio_path,
        bg_music_path,
        music_volume
        )
    video = video.with_audio(final_audio)
    # video = video.with_audio(audio)
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