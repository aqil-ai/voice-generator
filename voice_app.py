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
from modules.custom_video import create_custom_video
# from modules.video import create_video, create_custom_video
from modules.captions import get_words
import shutil
from modules.music import get_music

# from utils import split_script_into_chunks

VOICE_SPEED = {
    "YouTube Long": "-5%",
    "Netflix Documentary": "-8%",
    "YouTube Shorts": "+8%",
    "TikTok": "+12%",
    "Instagram Reel": "+10%"
    }
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
try:
    PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
except Exception:
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
# PEXELS_API_KEY = (
#     st.secrets.get("PEXELS_API_KEY")
#     or os.getenv("PEXELS_API_KEY")
# )
# PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
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
    border: 2px solid black !important;
    border-radius: 8px !important;    
    # background-color: white !important;
    # color: black !important;
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
        "🎬 AI Video Generator",
        "🎬 Custom Video Generator"
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
    gender = st.radio(
        "👤 Gender",
        ["Male", "Female"],
        horizontal=True
    )

    filtered_voices = [

        v for v in voice_map

        if (
            search_voice.lower() in v["label"].lower()
            and gender in v["label"]
        )

        # if search_voice.lower()
        # in v["label"].lower()

    ]

    if len(filtered_voices) == 0:

        st.warning("No voice found")

        st.stop()

    # -----------------------------
    # DROPDOWN
    # -----------------------------
    # gender = st.radio(
    #     "👤 Gender",
    #     ["Male", "Female"],
    #     horizontal=True
    # )
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

# 🎬 AI Video Generator
elif page == "🎬 AI Video Generator":

    st.title("🎬 AI Video Generator")

    script = st.text_area(
        "📝 Enter Script",
        height=250
    )
    # script_chunks = split_script_into_chunks(script)
    # -------------------------
# Script Statistics
# -------------------------

    char_count = len(script)
    word_count = len(script.split())

    estimated_minutes = round(word_count / 150, 1)

    st.caption(
        f"📝 Characters: {char_count:,} / 30,000   |   "
        f"📖 Words: {word_count:,}   |   "
        f"⏱ Estimated Duration: {estimated_minutes} min"
    )
    if char_count > 30000:
        st.error("❌ Maximum 30,000 characters allowed.")
    
    col1, col2 = st.columns(2)
    with col1:
        video_type = st.selectbox(
            "📱 Video Type",
        [
                "YouTube Long",
                "YouTube Shorts",
                "TikTok",
                "Instagram Reel",
                "Netflix Documentary"
        ]
    )
        voice_speed = VOICE_SPEED[video_type]
        with col2:
            animation_style = st.selectbox(
                "🎥 Animation Style",
        [
                    "None",
                    "Random",
                    "Zoom In",
                    "Zoom Out",
                    "Ken Burns",
            # "Pan Left",
            # "Pan Right",
            # "Pan Up",
            # "Pan Down",
            # "Rotate",
            # "Flip Horizontal",
            # "Flip Vertical"
        ]
    )
        col3, col4 = st.columns(2)
        with col3:
            animation_speed = st.selectbox(
                "⚡ Animation Speed",
        [
                    "Slow",
                    "Normal",
                    "Fast"
        ]
    )
        with col4:
            caption_style = st.selectbox(
                "🎨 Caption Style",
        [
                "Yellow",
                "White",
                "TikTok",
                "YouTube Shorts",
                "Neon Green"
        ]
    )
    
    all_voices = load_voices()
    col5, col6 = st.columns(2)

    with col5:
        language = st.selectbox(
            "🌍 Language",
            sorted(
                list(
                set(
                    get_language_display(v["Locale"])
                    for v in all_voices
                )
            )
        )
    )

    with col6:
        gender = st.selectbox(
        "👤 Gender",
        [
            "Male",
            "Female"
        ]
    )
    voice_map = []
    for v in all_voices:
        if (
            get_language_display(v["Locale"]) == language
            and v["Gender"] == gender
        ):
            voice_map.append({
                "label": v["ShortName"],
                "value": v["ShortName"]
        })
        # voice_map.append({
        #     "label":
        #     f"{get_language_display(v['Locale'])} | "
        #     f"{v['Gender']} | "
        #     f"{v['ShortName']}",
        #      "value":
        #      v["ShortName"]
        # })
    voice_label = st.selectbox(
        "🎤 Select Voice",
        options=[
            v["label"]
            for v in voice_map
        ]
    )
    selected_voice = next(
        v for v in voice_map
        if v["label"] == voice_label
    )
    voice_id = selected_voice["value"]
    st.divider()
    st.subheader("🎵 Background Music")
    music_style = st.selectbox(
        "Select Music Style",
    [
        "None",
        "Cinematic",
        "Documentary",
        "Corporate",
        "Technology",
        "Motivational",
        "Emotional",
        "Epic",
        "Travel",
        "News"
    ],
    key="music_style"
    )
    music_files = []
    if music_style != "None":
        folder = os.path.join(
            "music",
            music_style.lower()
        )
        if os.path.exists(folder):
            music_files = sorted([
                f for f in os.listdir(folder)
                if f.endswith(".mp3")
                ])
    selected_music = None
    if len(music_files) > 0:
        selected_music = st.selectbox(
            "🎵 Select Music Track",
            music_files,
            key="music_track"
        )
    
    music_volume = st.slider(
        "Music Volume",
        min_value=0,
        max_value=100,
        value=20,
        step=5,
        key="music_volume"
    )
    preview_music = st.button(
        "▶ Preview Music",
        use_container_width=True,
        key="preview_music_btn"
    )
    uploaded_music = st.file_uploader(
        "Or Upload Your Own Music (Optional)",
        type=["mp3", "wav"],
        key="uploaded_music"
    )
    bg_music_path = None
    if uploaded_music is not None:
        os.makedirs("temp", exist_ok=True)
        bg_music_path = "temp/custom_music.mp3"
        with open(bg_music_path, "wb") as f:
            f.write(uploaded_music.read())

    else:
        if selected_music:
            bg_music_path = os.path.join(
                "music",
                music_style.lower(),
                selected_music
            )

        else:
            bg_music_path = None
        # bg_music_path = get_music(music_style)
    if preview_music and bg_music_path is not None:
        with open(bg_music_path, "rb") as f:
            
            st.session_state.music_preview = f.read()
    # st.write(bg_music_path)   
    if "music_preview" in st.session_state:
        st.audio(
            st.session_state.music_preview,
            format="audio/mp3"
        )
    if "video_bytes" not in st.session_state:
        st.session_state.video_bytes = None
    # if "video_path" not in st.session_state:
        # st.session_state.video_path = None


    if "image_files" not in st.session_state:
        st.session_state.image_files = []
        if "scenes" not in st.session_state:
            st.session_state.scenes = []
# 👇 Buttons yahan
    st.divider()
    # col_btn1, col_btn2 = st.columns(2)
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

    with col_btn1:
        generate_btn = st.button(
            "🚀 Generate Scenes",
            use_container_width=True
        )
    with col_btn2:
        create_btn = st.button(
            "🎥 Create Video",
            use_container_width=True
            )
    # if st.button("🚀 Generate Scenes"):
    if generate_btn:
        st.session_state.image_files = []

        scenes = split_into_scenes(script)
        st.session_state.scenes = scenes

        st.success(
            f"{len(scenes)} scenes created"
        )

        cols = st.columns(2)

        for i, scene in enumerate(scenes):

            with cols[i % 2]:

                st.subheader(
                    f"Scene {i+1}"
                )

                st.write(scene)

                images = search_images(scene)

                if len(images) > 0:
                    os.makedirs("temp", exist_ok=True)
                    image_path = f"temp/scene_{i}.jpg"

                    # image_path = f"/scene_{i}.jpg"

                    image_data = requests.get(
                        images[0]
                    ).content

                    with open(
                        image_path,
                        "wb"
                    ) as f:
                        f.write(image_data)


                    st.session_state.image_files.append(
                        image_path
                    )


                    st.image(
                        images[0],
                        width="stretch"
                    )

                else:
                    st.warning(
                        "No image found"
                    )


    # if st.button("🎥 Create Video"):
    # if generate_btn:
    if create_btn:
        if len(st.session_state.image_files) == 0:

            st.warning(
                "First generate scenes"
            )

        else:
            os.makedirs("temp", exist_ok=True)
            audio_file = "temp/video_voice.mp3"

            # audio_file = "/video_voice.mp3"


            async def generate_voice():

                communicate = edge_tts.Communicate(
                    script,
                    voice_id,
                    rate=voice_speed
                )

                await communicate.save(
                    audio_file
                )


            with st.spinner("Creating voice..."):

                asyncio.run(
                    generate_voice()
                )


            output_video = "temp/final_video.mp4"
            # output_video = "downloads/final_video.mp4"


            with st.spinner("Making video..."):
                words = get_words(audio_file)

                create_video(
                    st.session_state.image_files,
                    st.session_state.scenes,
                     words,
                    audio_file,
                    output_video,
                    caption_style,
                    video_type,
                    animation_style,
                    animation_speed,
                    bg_music_path,
                    music_volume
                )


            st.success(
                "Video Created Successfully 🎉"
            )

           
            # )
            with open(output_video, "rb") as f:
                st.session_state.video_bytes = f.read()
            # st.session_state.video_path = output_video
           
    if st.session_state.video_bytes is not None:
    # if st.session_state.video_path:
            st.success("Your video is ready 🎬")
            st.video(
                st.session_state.video_bytes
                # st.session_state.video_path
            )
            # with open(
            #     st.session_state.video_path,
            #     "rb"
            #      ) as f:
            st.download_button(
                "⬇ Download Video",
                 data=st.session_state.video_bytes,
                #  data=f.read(),
                 file_name="AqilAI_video.mp4",
                 mime="video/mp4",
                 on_click="ignore"
            )
        

# # Delete temporary scene images
# for image_path in st.session_state.image_files:
#     if os.path.exists(image_path):
#         os.remove(image_path)

# # Clear list
# st.session_state.image_files = []
# Delete temp folder after video creation
    # if create_btn and st.session_state.video_path:
    #     if os.path.exists("temp"):
    #         shutil.rmtree("temp")
    #         st.session_state.image_files = []
    if create_btn:
        if os.path.exists("temp"):
            # shutil.rmtree("temp")
            os.makedirs("temp", exist_ok=True)
# Custom Video Generator       
elif page == "🎬 Custom Video Generator":

    st.title("🎬 Custom Video Generator")
    if "custom_image_files" not in st.session_state:
        st.session_state.custom_image_files = []
    if "custom_scenes" not in st.session_state:
        st.session_state.custom_scenes = []
    if "preview_video_bytes" not in st.session_state:
        st.session_state.preview_video_bytes = None
    if "final_video_bytes" not in st.session_state:
        st.session_state.final_video_bytes = None
    st.info("Create videos using your own scenes and images.")

    scene_count = st.number_input(
        "🎬 Number of Scenes",
        min_value=1,
        max_value=90,
        value=3,
        step=1
    )

    uploaded_images = []
    scene_texts = []

    for i in range(scene_count):

        st.divider()

        st.subheader(f"🎬 Scene {i+1}")

        scene = st.text_area(
            f"Scene {i+1}",
            key=f"scene_{i}"
        )
        images = st.file_uploader(
            f"🖼 Upload Images for Scene {i+1} (Maximum 3)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key=f"images_{i}"
        )
        if len(images) > 3:
            st.error("Maximum 3 images allowed.")
        else:
            cols = st.columns(3)
            for j, img in enumerate(images):
                with cols[j]:
                    st.image(
                    img,
                    width="stretch"
                )
            scene_texts.append(scene)
            uploaded_images.append(images) 
    # Video Type + Animation
    col1, col2 = st.columns(2)

    with col1:
        video_type = st.selectbox(
            "📱 Video Type",
        [
            "YouTube Long",
            "YouTube Shorts",
            "TikTok",
            "Instagram Reel",
            "Netflix Documentary"
        ],
        key="custom_video_type"
    )
        voice_speed = VOICE_SPEED[video_type]
    with col2:
        animation_style = st.selectbox(
            "🎥 Animation Style",
        [
            "None",
            "Random",
            "Zoom In",
            "Zoom Out",
            "Ken Burns"
        ],
        key="custom_animation"
    )
    # Animation Speed + Caption Style
    col3, col4 = st.columns(2)
    with col3:
        animation_speed = st.selectbox(
            "⚡ Animation Speed",
        [
            "Slow",
            "Normal",
            "Fast"
        ],
        key="custom_speed"
    )

    with col4:
        caption_style = st.selectbox(
            "🎨 Caption Style",
        [
            "Yellow",
            "White",
            "TikTok",
            "YouTube Shorts",
            "Neon Green"
        ],
        key="custom_caption"
    )
    # Voice Selection
    all_voices = load_voices()
    col5, col6 = st.columns(2)
    with col5:
        language = st.selectbox(
            "🌍 Language",
            sorted(
                list(
                    set(
                    get_language_display(v["Locale"])
                    for v in all_voices
                )
            )
        ),
        key="custom_language"
    )

    with col6:
        gender = st.selectbox(
            "👤 Gender",
        [
            "Male",
            "Female"
        ],
        key="custom_gender"
    )
    voice_map = []
    for v in all_voices:
        if (
        get_language_display(v["Locale"]) == language
        and v["Gender"] == gender
    ):
            voice_map.append({
                "label": v["ShortName"],
                "value": v["ShortName"]

        })
    voice_label = st.selectbox(
        "🎤 Select Voice",
        options=[
        v["label"]
        for v in voice_map
    ],

    key="custom_voice"
    )
    selected_voice = next(
        v
        for v in voice_map
        if v["label"] == voice_label
    )

    voice_id = selected_voice["value"]

    st.divider()
    st.subheader("🎵 Background Music")
    music_style = st.selectbox(
        "Select Music Style",
    [
        "None",
        "Cinematic",
        "Documentary",
        "Corporate",
        "Technology",
        "Motivational",
        "Emotional",
        "Epic",
        "Travel",
        "News"
    ],
    key="music_style"
    )
    music_files = []
    if music_style != "None":
        folder = os.path.join(
            "music",
            music_style.lower()
        )
        if os.path.exists(folder):
            music_files = sorted([
                f for f in os.listdir(folder)
                if f.endswith(".mp3")
                ])
    selected_music = None
    if len(music_files) > 0:
        selected_music = st.selectbox(
            "🎵 Select Music Track",
            music_files,
            key="music_track"
        )
    
    music_volume = st.slider(
        "Music Volume",
        min_value=0,
        max_value=100,
        value=20,
        step=5,
        key="music_volume"
    )
    preview_music = st.button(
        "▶ Preview Music",
        use_container_width=True,
        key="preview_music_btn"
    )
    uploaded_music = st.file_uploader(
        "Or Upload Your Own Music (Optional)",
        type=["mp3", "wav"],
        key="uploaded_music"
    )
    bg_music_path = None
    if uploaded_music is not None:
        os.makedirs("temp", exist_ok=True)
        bg_music_path = "temp/custom_music.mp3"
        with open(bg_music_path, "wb") as f:
            f.write(uploaded_music.read())

    else:
        if selected_music:
            bg_music_path = os.path.join(
                "music",
                music_style.lower(),
                selected_music
            )

        else:
            bg_music_path = None
        # bg_music_path = get_music(music_style)
    if preview_music and bg_music_path is not None:
        with open(bg_music_path, "rb") as f:
            
            st.session_state.music_preview = f.read()
    # st.write(bg_music_path)   
    if "music_preview" in st.session_state:
        st.audio(
            st.session_state.music_preview,
            format="audio/mp3"
        )
    st.divider()
    preview_video = st.button(
        "👁 Preview Video",
        use_container_width=True,
        key="preview_custom_video_btn"
    )
    generate_video = st.button(
        "🎥 Generate Custom Video",
        use_container_width=True,
        key="custom_video_btn"
    )

    if preview_video or generate_video:
        progress_bar = st.progress(0)
        progress_text = st.empty()
    # if generate_video:
        os.makedirs("temp", exist_ok=True)
        st.session_state.custom_image_files = []
        st.session_state.custom_scenes = []
        
        for scene_index, images in enumerate(uploaded_images):
            current_scene = scene_texts[scene_index]
            if current_scene.strip() == "":
                continue

            scene_images = []

            for image_index, image in enumerate(images):
                image_path = (
                f"temp/scene_{scene_index}_{image_index}.jpg"
                )

                with open(image_path, "wb") as f:
                    f.write(image.read())

                scene_images.append(image_path)

            st.session_state.custom_scenes.append(
                {
                    "text": current_scene,
                    "images": scene_images
                    }
            )
            progress_bar.progress(10)
            progress_text.info("📂 Images Saved (10%)")
        
        # for scene_index, images in enumerate(uploaded_images):
        #     current_scene = scene_texts[scene_index]
        #     if current_scene.strip() == "":
        #         continue
        #     st.session_state.custom_scenes.append(current_scene)
        #     for image_index, image in enumerate(images):
        #         image_path = (
        #             f"temp/"
        #             f"scene_{scene_index}_{image_index}.jpg"
        #         )
        #         with open(image_path, "wb") as f:
        #             f.write(image.read())

        #         st.session_state.custom_image_files.append(image_path)

        audio_file = "temp/custom_voice.mp3"
        full_script = " ".join(
            scene["text"]
            for scene in st.session_state.custom_scenes
            # st.session_state.custom_scenes
        )
        async def generate_voice():
            communicate = edge_tts.Communicate(
            full_script,
            voice_id,
            rate=voice_speed
            )
            await communicate.save(audio_file)
        with st.spinner("Generating Voice..."):
            asyncio.run(generate_voice())
        progress_bar.progress(35)
        progress_text.info("🎤 Voice Generated (35%)")
        words = get_words(audio_file)
        progress_bar.progress(50)
        progress_text.info("📝 Captions Ready (50%)")
        if preview_video:
            output_video = "temp/preview_video.mp4"
        else:
            output_video = "temp/custom_video.mp4"
        progress_bar.progress(60)
        progress_text.info("🎬 Creating Video... (60%)")
        create_custom_video(
            # st.session_state.custom_image_files,
            st.session_state.custom_scenes,
            words,
            audio_file,
            output_video,
            caption_style,
            video_type,
            animation_style,
            animation_speed,
            bg_music_path,
            music_volume
        )
        progress_bar.progress(100)
        progress_text.success("✅ Video Generated Successfully (100%)")
        # Save Preview
        if preview_video:
            # st.session_state.preview_video_path = output_video
            with open(output_video, "rb") as f:
                st.session_state.preview_video_bytes = f.read()

# Save Final Video
        else:
            # st.session_state.final_video_path = output_video
            with open(output_video, "rb") as f:
                st.session_state.final_video_bytes = f.read()
        # if preview_video:
        #     st.success("👁 Preview Ready!")
        #     st.video(output_video)
        # else:
        #     st.success("✅ Custom Video Created!")
        #     st.video(output_video)
        # # st.success("✅ Custom Video Created!")
        # # st.video(output_video)
        
        # with open(output_video, "rb") as f:
        #     st.download_button(
        #         "⬇ Download Video",
        #         data=f.read(),
        #         file_name="custom_video.mp4",
        #         mime="video/mp4",
        #         key="download_custom_video"
        #     )
    # ==========================
# Preview
# ==========================

    if st.session_state.preview_video_bytes is not None:
    # if "preview_video_bytes" in st.session_state:
        st.subheader("👁 Preview")
        st.video(
            st.session_state.preview_video_bytes
        )
        st.download_button(
            "⬇ Download Preview",
            data=st.session_state.preview_video_bytes,
            file_name="preview_video.mp4",
            mime="video/mp4",
            key="download_preview",
            on_click="ignore"
        )


# ==========================
# Final Video
# ==========================
    if st.session_state.final_video_bytes is not None:
    # if "final_video_bytes" in st.session_state:
        st.subheader("🎬 Final Video")
        st.video(
        st.session_state.final_video_bytes
        )
        st.download_button(
            "⬇ Download Final Video",
            data=st.session_state.final_video_bytes,
            file_name="custom_video.mp4",
            mime="video/mp4",
            key="download_final",
            on_click="ignore"
        )


    
      


            