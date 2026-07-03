from PIL import Image, ImageDraw

for i in range(1,4):

    img = Image.new(
        "RGB",
        (1280,720),
        "white"
    )

    draw = ImageDraw.Draw(img)

    draw.text(
        (500,350),
        f"Scene {i}",
        fill="black"
    )

    img.save(
        f"scene{i}.png"
    )

print("Images created")