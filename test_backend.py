from modules.avatar.backends import LivePortraitBackend

backend = LivePortraitBackend()

print(backend.info())

backend.generate(
    image_path="person.jpg",
    audio_path="voice.mp3",
    output_path="avatar.mp4"
)