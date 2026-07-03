from faster_whisper import WhisperModel


def get_words(audio_file):

    model = WhisperModel(
        "base",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        audio_file,
        word_timestamps=True
    )


    words = []

    for segment in segments:

        for word in segment.words:

            words.append({
                "text": word.word,
                "start": word.start,
                "end": word.end
            })

    return words