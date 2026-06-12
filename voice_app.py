import streamlit as st
import asyncio
import edge_tts
from deep_translator import GoogleTranslator

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AqilAI Studio",
    page_icon="🎙️",
    layout="wide"
)

# -----------------------------
# PROFESSIONAL UI
# -----------------------------
st.markdown("""
<style>

/* White Background */
.stApp {
    background-color: white;
}

/* White Sidebar */
[data-testid="stSidebar"] {
    background-color: white;
}

/* Black Text */
h1, h2, h3, h4, h5, h6,
p, li, label, span, div {
    color: black !important;
}

/* Text Area */
textarea {
    background-color: white !important;
    color: black !important;
}

/* Input Fields */
input {
    color: black !important;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

/* Cards */
.glass-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🎙 AqilAI Studio")

page = st.sidebar.selectbox(
    "Navigate",
    [
        "🏠 Home",
        "🎤 Voice Generator"
    ]
)

# -----------------------------
# HOME PAGE
# -----------------------------
if page == "🏠 Home":

    st.markdown("""
<div class="glass-card">

<h1>🎙 AqilAI Studio</h1>

<h3>Professional AI Voice Generation & Translation Platform</h3>

<hr>

<h3>🚀 Features</h3>

<ul>
<li>🎤 100+ Natural AI Voices</li>
<li>🌍 Multi-Language Translation</li>
<li>⚡ Instant Voice Generation</li>
<li>⬇ High Quality MP3 Download</li>
<li>🔍 Smart Voice Search</li>
</ul>

<hr>

<h3>⚡ How It Works</h3>

<ol>
<li>Enter your script</li>
<li>Select an AI voice</li>
<li>Generate realistic speech</li>
<li>Preview and download MP3</li>
</ol>

<hr>

<h3>👨‍💻 Developer</h3>

<b>Muhammad Aqil</b>

<p>
AI Tools Creator & Automation Developer
</p>

</div>
""", unsafe_allow_html=True)

    st.success(
        "Open Voice Generator from sidebar 👈"
    )

# -----------------------------
# VOICE GENERATOR
# -----------------------------
elif page == "🎤 Voice Generator":

    st.title("🎤 AI Voice Generator")
    st.caption(
    "Generate natural sounding AI voiceovers in multiple languages."
)

    text = st.text_area(
    "📝 Enter Your Script",
    placeholder="Type or paste your content here...",
    height=220
)
     # Counter
    char_count = len(text)
    word_count = len(text.split())

    st.caption(
    f"Words: {word_count} | Characters: {char_count} / 10000"
)
    # File Name
    file_name = st.text_input(
    "📁 File Name",
    value="voice"
)
    
    # -----------------------------
    # LANGUAGE DISPLAY
    # -----------------------------
    def get_language_display(locale):

        mapping = {
            "en": "English",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "pl": "Polish",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "hi": "Hindi",
            "ar": "Arabic",
            "tr": "Turkish",
            "sv": "Swedish",
            "da": "Danish",
            "fi": "Finnish",
            "no": "Norwegian"
        }

        lang_code = locale.split("-")[0]

        return mapping.get(
            lang_code,
            lang_code
        )

    # -----------------------------
    # LOAD ALL VOICES
    # -----------------------------
    @st.cache_data
    def load_voices():

        async def get_voices():
            return await edge_tts.list_voices()

        return asyncio.run(get_voices())

    all_voices = load_voices()

    # -----------------------------
    # BUILD VOICE LIST
    # -----------------------------
    voice_map = []

    for v in all_voices:

        voice_map.append({
            "label":
            f"{get_language_display(v['Locale'])} | "
            f"{v['Gender']} | "
            f"{v['ShortName']}",

            "value":
            v["ShortName"],

            "locale":
            v["Locale"]
        })

    # -----------------------------
    # SEARCH VOICES
    # -----------------------------
    search_voice = st.text_input(
    "🔍 Search Voice",
    placeholder="Example: English, Hindi, Arabic, German..."
)

    filtered_voices = [

        v for v in voice_map

        if search_voice.lower()
        in v["label"].lower()

    ]

    if len(filtered_voices) == 0:

        st.warning("No voice found")

        st.stop()

    # -----------------------------
    # DROPDOWN
    # -----------------------------
    voice_label = st.selectbox(
        "Choose Voice",
        options=[
            v["label"]
            for v in filtered_voices
        ]
    )

    selected_voice = next(
        v for v in filtered_voices
        if v["label"] == voice_label
    )

    voice_id = selected_voice["value"]

    locale = selected_voice["locale"]
    voice_style = st.selectbox(
    "🎭 Voice Style",
    [
        "Custom",
        "YouTube Narration",
        "Storytelling",
        "News Reporter",
        "Documentary",
        "YouTube Shorts"
    ]
)

speed = 0
pitch = 0

if voice_style == "Storytelling":
    speed = -15
    pitch = -10

elif voice_style == "News Reporter":
    speed = 10

elif voice_style == "Documentary":
    speed = -10
    pitch = -15

elif voice_style == "YouTube Shorts":
    speed = 25
    pitch = 10

if voice_style == "Custom":
    speed = st.slider(
        "⚡ Voice Speed (%)",
        -50, 50, 0, 5
    )

    pitch = st.slider(
        "🎵 Voice Pitch (Hz)",
        -50, 50, 0, 5
    )

st.info(
    f"Speed: {speed}% | Pitch: {pitch}Hz"
)

# -----------------------------
# LANGUAGE CODE
# -----------------------------
def get_lang_code(locale):
    return locale.split("-")[0]

# -----------------------------
# PREVIEW BUTTON
# -----------------------------
preview_btn = st.button(
    "🔊 Preview Voice",
    key="preview_voice_btn"
)

if preview_btn:

    if text.strip() == "":
        st.warning("Please enter text first")

    else:

        preview_text = text[:150]

        preview_file = "preview.mp3"

        with st.spinner("Generating preview..."):

            async def preview_voice():

                communicate = edge_tts.Communicate(
                    preview_text,
                    voice_id,
                    rate=f"{speed:+d}%"
                )

                await communicate.save(preview_file)

            asyncio.run(preview_voice())

        with open(preview_file, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

# -----------------------------
# GENERATE BUTTON
# -----------------------------
st.write("Current filename:", file_name)
generate_btn = st.button(
    "🚀 Generate Voice",
    key="generate_voice_btn"
)

if generate_btn:

    if text.strip() == "":
        st.error("Please enter text")
        st.stop()

    if len(text) > 10000:
        st.error("Maximum 10000 characters allowed")
        st.stop()

    lang_code = get_lang_code(locale)

    translated_text = text

    if lang_code != "en":

        try:
            translated_text = GoogleTranslator(
                source="auto",
                target=lang_code
            ).translate(text)

        except Exception:
            st.warning(
                "Translation failed. Using original text."
            )

    output_file = f"{file_name}.mp3"

    with st.spinner(
        "🤖 AI is generating your voice..."
    ):

        async def generate_voice():

            communicate = edge_tts.Communicate(
                translated_text,
                voice_id,
                rate=f"{speed:+d}%"
            )

            await communicate.save(output_file)

        asyncio.run(generate_voice())

    st.success("Voice Generated Successfully 🎉")

    with open(output_file, "rb") as f:
        audio_bytes = f.read()

    st.audio(audio_bytes, format="audio/mp3")

    st.download_button(
    "⬇ Download Audio",
    data=audio_bytes,
    file_name=f"{file_name}.mp3",
    mime="audio/mp3"
)