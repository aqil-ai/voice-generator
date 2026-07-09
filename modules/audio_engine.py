from moviepy import (
    AudioFileClip,
    CompositeAudioClip
)
def build_audio(
    voice_path,
    bg_music_path=None,
    music_volume=20
):

    voice = AudioFileClip(
        voice_path
    )

    final_audio = voice

    if bg_music_path is not None:

        try:

            music = AudioFileClip(
                bg_music_path
            )

            music = music.subclipped(
                0,
                min(
                    music.duration,
                    voice.duration
                )
            )

            music = music.with_volume_scaled(
                music_volume / 100
            )

            final_audio = CompositeAudioClip(
                [
                    voice,
                    music
                ]
            )

        except Exception as e:

            print(
                "Music Error:",
                e
            )

    return final_audio