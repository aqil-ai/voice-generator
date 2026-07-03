from PIL import Image, ImageFilter, ImageOps

def compose_image(image_path, video_type):

    img = Image.open(image_path).convert("RGB")
    orientation = get_orientation(img)

    if video_type == "YouTube Long":

        return prepare_youtube(img, image_path)

    elif video_type == "YouTube Shorts":

        return prepare_vertical(img, image_path, orientation)

    elif video_type == "TikTok":

        return prepare_vertical(img, image_path, orientation)

    elif video_type == "Instagram Reel":

        return prepare_vertical(img, image_path, orientation)

    elif video_type == "Netflix Documentary":

        return prepare_netflix(img, image_path)
    return image_path
 
def prepare_youtube(img, image_path):

    canvas = ImageOps.fit(
        img,
        (1280,720),
        method=Image.LANCZOS,
        centering=(0.5,0.5)
    )

    output = image_path.replace(
        ".jpg",
        "_yt.jpg"
    )

    canvas.save(output)

    return output
def prepare_vertical(img, image_path, orientation):

    canvas = ImageOps.fit(
        img,
        (1080,1920),
        method=Image.LANCZOS,
        centering=(0.5,0.5)
    )

    output = image_path.replace(
        ".jpg",
        "_vertical.jpg"
    )

    canvas.save(output)

    return output

    # bg = ImageOps.fit(
    #     img,
    #     (1080,1920),
    #     method=Image.LANCZOS
    # )

    # bg = bg.filter(
    #     ImageFilter.GaussianBlur(30)
    # )

    # main = img.copy()

    # if orientation == "portrait":

    #    img_w, img_h = main.size
    #    scale = min(
    #        980 / img_w,
    #        1700 / img_h
    #    )
    #    new_w = int(img_w * scale)
    #    new_h = int(img_h * scale)
    #    main = main.resize(
    #        (new_w, new_h),
    #        Image.LANCZOS
    #    )

    # x = (1080-main.width)//2
    # y = (1920-main.height)//2

    # bg.paste(
    #     main,
    #     (x,y)
    # )

    # output = image_path.replace(
    #     ".jpg",
    #     "_vertical.jpg"
    # )

    # bg.save(output)

    # return output
def prepare_netflix(img, image_path):

    canvas = ImageOps.fit(
        img,
        (1920,1080),
        method=Image.LANCZOS
    )

    output = image_path.replace(
        ".jpg",
        "_netflix.jpg"
    )

    canvas.save(output)

    return output
def get_orientation(img):

    w, h = img.size

    if w > h:
        return "landscape"

    elif h > w:
        return "portrait"

    else:
        return "square"