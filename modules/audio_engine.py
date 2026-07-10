from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    concatenate_audioclips
)

from moviepy import AudioFileClip, concatenate_audioclips

def loop_music(music_path, target_duration):

    clips = []
    total = 0

    while total < target_duration:
        clip = AudioFileClip(music_path)
        clips.append(clip)
        total += clip.duration

    music = concatenate_audioclips(clips)

    return music.subclipped(0, target_duration)
# def loop_music(
#     music_path,
#     target_duration
# ):
#     music = AudioFileClip(music_path)

#     # Agar music pehle hi lambi hai
#     if music.duration >= target_duration:

#         final = music.subclipped(
#             0,
#             target_duration
#         )
#         music.close()
#         return final

#     clips = []

#     total_duration = 0

#     while total_duration < target_duration:

#         clip = AudioFileClip(
#             music_path
#         )

#         clips.append(
#             clip
#         )

#         total_duration += clip.duration
    
#     final_music = concatenate_audioclips(clips)

# # Close all temporary clips
#     for clip in clips:
#         clip.close()
#     return final_music.subclipped(
#         0,
#         target_duration
#         )
    # music = concatenate_audioclips(
    #     clips
    # )

    # return music.subclipped(
    #     0,
    #     target_duration
    # )
# 
def build_audio(
    voice_path,
    bg_music_path=None,
    music_volume=20
):

    voice = AudioFileClip(voice_path)

    if bg_music_path is None:
        return voice

    music = loop_music(
        bg_music_path,
        voice.duration
    )

    music = music.with_volume_scaled(
        music_volume / 100
    )

    return CompositeAudioClip(
        [
            voice,
            music
        ]
    )
# def build_audio(
#     voice_path,
#     bg_music_path=None,
#     music_volume=20
# ):

#     voice = AudioFileClip(
#         voice_path
#     )

#     final_audio = voice

#     if bg_music_path is not None:

#         try:
#             music = loop_music(
#                 bg_music_path,
#                 voice.duration
#                 )

            # music = AudioFileClip(
            #     bg_music_path
            # )

            # music = music.subclipped(
            #     0,
            #     min(
            #         music.duration,
            #         voice.duration
            #     )
            # )

            # music = music.with_volume_scaled(
            #     music_volume / 10/0
            # # )

            # # final_audio = CompositeAudioClip(
            #     [
            #         voice,
            #         music
            #     ]
            # )

    #     except Exception as e:

    #         print(
    #             "Music Error:",
    #             e
    #         )

    # try:
    #     voice.close()
    # except:
    #     pass
    # return final_audio
    # return final_audio