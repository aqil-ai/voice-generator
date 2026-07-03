def split_into_scenes(text):

    scenes = []

    lines = text.split(".")

    for line in lines:

        line = line.strip()

        if line:
            scenes.append(line)

    return scenes