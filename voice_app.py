import streamlit as st
import asyncio
import edge_tts
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import requests
import random
import zipfile
from io import BytesIO
import urllib.parse
from modules.scenes import split_into_scenes
from modules.video import create_video
from modules.captions import get_words

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


@st.cache_data
def load_voices():

    async def get_voices():
        return await edge_tts.list_voices()

    return asyncio.run(get_voices())
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AqilAI Studio",
    page_icon="logo.png.jpeg",
    layout="wide"
)

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
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
# PEXELS FUNCTION
# -----------------------------
def search_images(query):

    headers = {
        "Authorization": PEXELS_API_KEY
    }
    page_no = random.randint(1, 20)

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=10&page={page_no}"

    response = requests.get(
        url,
        headers=headers
    )

    data = response.json()

    images = []

    for photo in data.get("photos", []):
        images.append(photo["src"]["landscape"])

    return images
# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.image("logo.png.jpeg", width=150)
# st.sidebar.title("🎙 AqilAI Studio")

page = st.sidebar.selectbox(
    "Navigate",
    [
        "🏠 Home",
        "🎤 Voice Generator",
        "🖼 Image Generator",
        # "🎨 AI Image Generator",
        # "🎬 AI Video Generator"
    ]
)

# -----------------------------
# HOME PAGE
# -----------------------------
if page == "🏠 Home":
    # st.image("logo.png.jpeg", width=250)

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
#     image_source = st.radio(
#         "Choose Image Source",
#         ["📷 Pexels", "🎨 AI (Pollinations)"]
# )

#     style = st.text_input(
#         "🎨 Image Style",
#         placeholder="Example: white background, realistic, cinematic"
# )
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
    # def get_language_display(locale):

    #     mapping = {
    #         "en": "English",
    #         "de": "German",
    #         "fr": "French",
    #         "es": "Spanish",
    #         "it": "Italian",
    #         "pt": "Portuguese",
    #         "nl": "Dutch",
    #         "pl": "Polish",
    #         "ru": "Russian",
    #         "ja": "Japanese",
    #         "ko": "Korean",
    #         "zh": "Chinese",
    #         "hi": "Hindi",
    #         "ar": "Arabic",
    #         "tr": "Turkish",
    #         "sv": "Swedish",
    #         "da": "Danish",
    #         "fi": "Finnish",
    #         "no": "Norwegian"
    #     }

    #     lang_code = locale.split("-")[0]

    #     return mapping.get(
    #         lang_code,
    #         lang_code
    #     )

    # # -----------------------------
    # # LOAD ALL VOICES
    # # -----------------------------
    # @st.cache_data
    # def load_voices():

    #     async def get_voices():
    #         return await edge_tts.list_voices()

    #     return asyncio.run(get_voices())

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
    st.session_state.voice_id = voice_id

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
        # -----------------------------
# IMAGE GENERATOR
# -----------------------------
elif page == "🖼 Image Generator":

    st.title("🖼 Image Generator")

    script = st.text_area(
        "📝 Paste Your Script Here",
        height=250
    )
    if "images" not in st.session_state:
        st.session_state.images = []
      

    if st.button("🔍 Find Images"):

        if script.strip() == "":
            st.warning("Please paste a script")

        else:

            with st.spinner("Finding images..."):

                st.session_state.images = search_images(script[:100])

    if len(st.session_state.images) > 0:
                st.success(
                    f"Found {len(st.session_state.images)} images"
                )
                #Zip code
                zip_buffer = BytesIO()
                with zipfile.ZipFile(
                    zip_buffer,
                    "a",
                    zipfile.ZIP_DEFLATED,
                    False
                    ) as zip_file:
                    for i, img in enumerate(st.session_state.images):
                        image_data = requests.get(img).content
                        zip_file.writestr(
                             f"image_{i+1}.jpg",
                             image_data
                        )
                zip_buffer.seek(0)
                st.download_button(
                            label="📦 Download All Images ZIP",
                            data=zip_buffer,
                            file_name="all_images.zip",
                             mime="application/zip",
                             key="zip_download"
                        )
                
                


                cols = st.columns(3)
                for i, img in enumerate(st.session_state.images):
                    with cols[i % 3]:
                        st.image(
                        img,
                        use_container_width=True
                    )
                        image_data = requests.get(img).content
                        st.download_button(
                        label="⬇ Download",
                        # label=f"⬇ Download Image {i+1}",
                        data=image_data,
                        file_name=f"image_{i+1}.jpg",
                        mime="image/jpeg",
                        key=f"download_{i}"
                    )
# # XTTS

# elif page == "🎨 AI Image Generator":

#     st.title("🎨 AI Image Generator")

#     prompt = st.text_area(
#         "📝 Describe your image",
#         height=200
#     )

#     if st.button("🚀 Generate AI Images"):

#         if prompt.strip() == "":
#             st.warning("Please enter a prompt.")

#         else:

#             cols = st.columns(2)

#             for i in range(2):

#                 seed = random.randint(1, 1000000)

#                 encoded_prompt = urllib.parse.quote(
#                     f"{prompt} seed:{seed}"
#                 )

#                 image_url = (
#                     f"https://image.pollinations.ai/prompt/{encoded_prompt}"
#                 )

#                 with cols[i]:

#                     st.image(
#                         image_url,
#                         use_container_width=True
#                     )

#                     image_data = requests.get(image_url).content

#                     st.download_button(
#                         label=f"⬇ Download Image {i+1}",
#                         data=image_data,
#                         file_name=f"ai_image_{i+1}.jpg",
#                         mime="image/jpeg",
#                         key=f"ai_download_{i}"
#                     )

# # 🎬 AI Video Generator
# elif page == "🎬 AI Video Generator":

#     st.title("🎬 AI Video Generator")

#     script = st.text_area(
#         "📝 Enter Script",
#         height=250
#     )

#     video_type = st.selectbox(
#         "📱 Video Type",
#         [
#             "YouTube Long",
#             "YouTube Shorts",
#             "TikTok",
#             "Instagram Reel",
#             "Netflix Documentary"
#         ]
#     )
#     caption_style = st.selectbox(
#         "🎨 Caption Style",
#         [
#             "Yellow",
#             "White",
#             "TikTok",
#             "YouTube Shorts",
#             "Neon Green"
#         ]
#     )
#     all_voices = load_voices()
#     voice_map = []
#     for v in all_voices:
#         voice_map.append({
#             "label":
#             f"{get_language_display(v['Locale'])} | "
#             f"{v['Gender']} | "
#             f"{v['ShortName']}",
#              "value":
#              v["ShortName"]
#         })
#     voice_label = st.selectbox(
#         "🎤 Select Voice",
#         options=[
#             v["label"]
#             for v in voice_map
#         ]
#     )
#     selected_voice = next(
#         v for v in voice_map
#         if v["label"] == voice_label
#     )
#     voice_id = selected_voice["value"]
#     if "video_path" not in st.session_state:
#         st.session_state.video_path = None


#     if "image_files" not in st.session_state:
#         st.session_state.image_files = []
#         if "scenes" not in st.session_state:
#             st.session_state.scenes = []


#     if st.button("🚀 Generate Scenes"):

#         st.session_state.image_files = []

#         scenes = split_into_scenes(script)
#         st.session_state.scenes = scenes

#         st.success(
#             f"{len(scenes)} scenes created"
#         )

#         cols = st.columns(2)

#         for i, scene in enumerate(scenes):

#             with cols[i % 2]:

#                 st.subheader(
#                     f"Scene {i+1}"
#                 )

#                 st.write(scene)

#                 images = search_images(scene)

#                 if len(images) > 0:

#                     image_path = f"downloads/scene_{i}.jpg"

#                     image_data = requests.get(
#                         images[0]
#                     ).content

#                     with open(
#                         image_path,
#                         "wb"
#                     ) as f:
#                         f.write(image_data)


#                     st.session_state.image_files.append(
#                         image_path
#                     )


#                     st.image(
#                         images[0],
#                         width="stretch"
#                     )

#                 else:
#                     st.warning(
#                         "No image found"
#                     )


#     if st.button("🎥 Create Video"):

#         if len(st.session_state.image_files) == 0:

#             st.warning(
#                 "First generate scenes"
#             )

#         else:

#             audio_file = "downloads/video_voice.mp3"


#             async def generate_voice():

#                 communicate = edge_tts.Communicate(
#                     script,
#                     voice_id
#                 )

#                 await communicate.save(
#                     audio_file
#                 )


#             with st.spinner("Creating voice..."):

#                 asyncio.run(
#                     generate_voice()
#                 )


#             output_video = "downloads/final_video.mp4"


#             with st.spinner("Making video..."):
#                 words = get_words(audio_file)

#                 create_video(
#                     st.session_state.image_files,
#                     st.session_state.scenes,
#                      words,
#                     audio_file,
#                     output_video,
#                     caption_style,
#                     video_type
#                 )


#             st.success(
#                 "Video Created Successfully 🎉"
#             )

           
#             # )
#             st.session_state.video_path = output_video
           
#     if st.session_state.video_path:
#             st.success("Your video is ready 🎬")
#             st.video(
#                 st.session_state.video_path
#             )
#             with open(
#                 st.session_state.video_path,
#                 "rb"
#                  ) as f:
#                 st.download_button(
#                 "⬇ Download Video",
#                  data=f.read(),
#                  file_name="AqilAI_video.mp4",
#                  mime="video/mp4"
#             )
        
            


            