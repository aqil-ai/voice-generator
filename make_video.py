from modules.video import create_video


images = [
    "scene1.png",
    "scene2.png",
    "scene3.png"
]


create_video(
    images,
    "voice.mp3",
    "test_output.mp4"
)

print("Video Done")