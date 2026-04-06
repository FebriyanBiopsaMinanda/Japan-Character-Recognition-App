import os
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
import random

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="日本語 Character App",
    page_icon="💮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# KONFIGURASI FILE MODEL
# =========================
MODEL_PATH = "../japanese_char.h5"
CLASS_NAMES_PATH = "../class_names.npy"
IMG_SIZE = 64

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model tidak ditemukan: {MODEL_PATH}")
    return tf.keras.models.load_model(MODEL_PATH)

# =========================
# LOAD CLASS NAMES
# =========================
@st.cache_data
def load_class_names():
    if not os.path.exists(CLASS_NAMES_PATH):
        raise FileNotFoundError(
            f"File class names tidak ditemukan: {CLASS_NAMES_PATH}"
        )

    class_names = np.load(CLASS_NAMES_PATH, allow_pickle=True)

    if len(class_names) == 0:
        raise ValueError("class_names.npy kosong.")

    return class_names

# =========================
# HEADER UTAMA
# =========================
st.markdown(
    """
    <div class='navbar-header'>
        <div class='navbar-title'>日本語 Character Recognition App</div>
        <div class='navbar-subtitle'>
            An intelligent application that predicts and recognizes Japanese Hiragana and Katakana characters using CNN
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# NAVBAR STICKY
# =========================
st.markdown("<div class='sticky-nav-wrap'>", unsafe_allow_html=True)
page = option_menu(
    menu_title=None,
    options=["Dashboard", "Data", "Technology", "Predict", "Canvas"],
    icons=["house", "table", "cpu", "graph-up-arrow", "pencil-square"],
    default_index=3,
    orientation="horizontal"
)
st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)

# =========================
# MAPPING LABEL
# =========================
hiragana_map = {
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "ya": "や", "yu": "ゆ", "yo": "よ",
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "wa": "わ", "wo": "を", "n": "ん"
}

katakana_map = {
    "a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
    "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ",
    "sa": "サ", "shi": "シ", "su": "ス", "se": "セ", "so": "ソ",
    "ta": "タ", "chi": "チ", "tsu": "ツ", "te": "テ", "to": "ト",
    "na": "ナ", "ni": "ニ", "nu": "ヌ", "ne": "ネ", "no": "ノ",
    "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ",
    "ma": "マ", "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ",
    "ya": "ヤ", "yu": "ユ", "yo": "ヨ",
    "ra": "ラ", "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ",
    "wa": "ワ", "wo": "ヲ", "n": "ン"
}

# =========================
# FUNGSI PREPROCESS
# =========================
def preprocess_image(uploaded_image):
    image = Image.open(uploaded_image).convert("L")
    image = np.array(image)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

    preview = image.copy()

    image = image.astype("float32") / 255.0
    image_input = np.expand_dims(image, axis=-1)
    image_input = np.expand_dims(image_input, axis=0)

    return preview, image_input

# =========================
# FUNGSI PARSE LABEL
# =========================
def parse_prediction_label(label):
    parts = str(label).split("_", 1)

    if len(parts) != 2:
        return "Unknown", str(label), "-"

    script_type, romaji = parts

    if script_type == "hiragana":
        char_jp = hiragana_map.get(romaji, "-")
    elif script_type == "katakana":
        char_jp = katakana_map.get(romaji, "-")
    else:
        char_jp = "-"

    return script_type.capitalize(), romaji, char_jp

# =========================
# AMBIL SAMPEL
# =========================
st.write("HIRAGANA_DIR:", HIRAGANA_DIR)
st.write("KATAKANA_DIR:", KATAKANA_DIR)
st.write("Hiragana exists:", os.path.exists(HIRAGANA_DIR))
st.write("Katakana exists:", os.path.exists(KATAKANA_DIR))

def get_sample_images(script_type, romaji, max_samples=5):
    if script_type.lower() == "hiragana":
        folder_path = os.path.join(HIRAGANA_DIR, romaji.lower())
    else:
        folder_path = os.path.join(KATAKANA_DIR, romaji.lower())

    if not os.path.exists(folder_path):
        return []

    images = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if len(images) == 0:
        return []

    return random.sample(images, min(max_samples, len(images)))

# =========================
# POPUP HASIL PREDIKSI
# =========================
@st.dialog("Predict Result (予測結果)", width="large")
def show_prediction_popup(uploaded_file, script_type, romaji, char_jp):
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        original_image = Image.open(uploaded_file)
        st.image(original_image, use_container_width=True)

    with col2:
        st.markdown(
            f"""
            <div class='popup-result-box'>
                <h3>Result (結果) : {romaji.lower()}</h3>
                <p>Type (手紙): <b>{script_type}</b></p>
                <p>Japanese Characters (日本の文字): <b>{char_jp}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        sample_images = get_sample_images(script_type, romaji)

        if sample_images:
            st.markdown("<h2 style='color:#991b1b;'>Contoh Dataset</h2>", unsafe_allow_html=True)

            cols = st.columns(5)

            for i, img_path in enumerate(sample_images):
                with cols[i]:
                    st.image(img_path, use_container_width=True)
        else:
            st.info("""Sample dataset tidak ditemukan.
                    \nサンプルデータセットが見つかりませんでした。""")

# =========================
# CEK MODEL
# =========================
model = None
class_names = None
model_ready = False

try:
    model = load_model()
    class_names = load_class_names()

    model_output_classes = model.output_shape[-1]
    if model_output_classes != len(class_names):
        st.error(
            f"Jumlah output model ({model_output_classes}) tidak sama dengan jumlah class names ({len(class_names)})."
        )
    else:
        model_ready = True
except Exception as e:
    st.warning(f"Model belum bisa digunakan: {e}")

# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.switch_page("dashboard.py")

elif page == "Data":
    st.switch_page("pages/data.py")

elif page == "Technology":
    st.switch_page("pages/teknologi.py")

elif page == "Predict":
    left_col, right_col = st.columns([1.1, 1], gap="large")

    with left_col:
        st.markdown(
            """
            <div class='predict-card'>
                <h3>Upload Gambar (画像をアップロードする)</h3>
                <p>Pilih satu file gambar huruf Jepang dengan format PNG, JPG, atau JPEG, lalu klik tombol prediksi.</p>
                <br>
                <p>PNG、JPG、またはJPEG形式の日本語文字画像ファイルを選択し、予測ボタンをクリックしてください。</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right_col:
        st.markdown("<div class='upload-container'>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload gambar",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )

        if uploaded_file is None:
            st.info("""Silakan upload satu gambar huruf Jepang terlebih dahulu.
                    \nまず、日本語の文字の画像を1枚アップロードしてください。""")
            
        else:
            st.success("""Gambar berhasil diupload. Klik tombol prediksi.
                       \n画像のアップロードが完了しました。予測ボタンをクリックしてください。""")

            col1, col2, col3= st.columns(3)
            
            with col3:
                if st.button("Predict (予測)", use_container_width=True):
                    if not model_ready:
                        st.error("""Model belum siap digunakan. Periksa file model dan class names.
                         \nモデルはまだ使用できる状態ではありません。モデルファイルとクラス名を確認してください。""")
                    else:
                        _, image_input = preprocess_image(uploaded_file)
                        prediction = model.predict(image_input, verbose=0)[0]

                        pred_index = int(np.argmax(prediction))
                        pred_label = class_names[pred_index]
                        script_type, romaji, char_jp = parse_prediction_label(pred_label)

                        show_prediction_popup(
                            uploaded_file,
                            script_type,
                            romaji,
                            char_jp
                        )

        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Canvas":
    st.switch_page("pages/drawing.py")

# =========================
# CSS CUSTOM
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #fffafa 45%, #fff1f2 100%);
    }

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .main .block-container {
        padding-top: 0.7rem;
        padding-bottom: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 96% !important;
    }

    .element-container,
    .stMarkdown {
        width: 100% !important;
    }

    .navbar-header {
        background: linear-gradient(90deg, #7f1d1d 0%, #b91c1c 45%, #dc2626 100%);
        padding: 28px 34px 24px 34px;
        border-radius: 24px;
        box-shadow: 0 10px 28px rgba(127, 29, 29, 0.18);
        margin-bottom: 14px;
        width: 100%;
        margin-top: 60px;
    }

    .navbar-title {
        color: white;
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
        line-height: 1.15;
    }

    .navbar-subtitle {
        color: #fee2e2;
        font-size: 1.06rem;
        line-height: 1.75;
        max-width: 1100px;
    }

    .sticky-nav-wrap {
        position: sticky;
        top: 0;
        z-index: 9999;
        padding-top: 12px;
        padding-bottom: 12px;
        margin-bottom: 10px;
        width: 100%;
    }

    .nav-divider {
        width: 100%;
        height: 2px;
        background: #efb1b1;
        margin-top: 10px;
        margin-bottom: 18px;
        border-radius: 999px;
    }

    div[data-testid="stOptionMenu"] {
        background: transparent !important;
        width: 100% !important;
    }

    div[data-testid="stOptionMenu"] > div {
        width: 100% !important;
        background: transparent !important;
    }

    div[data-testid="stOptionMenu"] ul {
        background: #ffffff !important;
        border-radius: 18px !important;
        padding: 10px !important;
        box-shadow: 0 8px 22px rgba(127, 29, 29, 0.08) !important;
        border: 1px solid #fecaca !important;
        gap: 8px;
        width: 100%;
        margin: 0 !important;
    }

    div[data-testid="stOptionMenu"] ul li {
        margin: 0 4px !important;
    }

    div[data-testid="stOptionMenu"] ul li a {
        border-radius: 14px !important;
        padding: 12px 18px !important;
        color: #7f1d1d !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stOptionMenu"] ul li a:hover {
        background: #fee2e2 !important;
        color: #991b1b !important;
    }

    div[data-testid="stOptionMenu"] ul li a.nav-link-active {
        background: linear-gradient(90deg, #b91c1c 0%, #dc2626 100%) !important;
        color: white !important;
        box-shadow: 0 6px 14px rgba(185, 28, 28, 0.22) !important;
    }

    div[data-testid="stOptionMenu"] .icon {
        font-size: 16px !important;
    }

    .top-header {
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 60%, #ef4444 100%);
        padding: 18px 16px;
        border-radius: 24px;
        color: white;
        box-shadow: 0 12px 30px rgba(153, 27, 27, 0.18);
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .predict-card {
        background: #ffffff;
        border: 1px solid #fecaca;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.08);
    }

    .predict-card h3 {
        margin: 0 0 8px 0;
        color: #991b1b;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .predict-card p {
        margin: 0;
        color: #4b5563;
        font-size: 1rem;
        line-height: 1.8;
    }

    .upload-container {
        max-width: 520px;
        margin: 0 auto;
    }

    div[data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1.5px solid #fecaca !important;
        border-radius: 18px !important;
        padding: 14px !important;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.06) !important;
    }

    div[data-testid="stFileUploader"] section {
        background: linear-gradient(90deg, #1f2937 0%, #2b2d42 100%) !important;
        border-radius: 16px !important;
    }

    div[data-testid="stFileUploader"] button {
        border-radius: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #b91c1c 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 18px rgba(185, 28, 28, 0.16) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(185, 28, 28, 0.24) !important;
    }

    div[data-testid="stDialog"] {
        text-align: center !important;
    }

    div[data-testid="stDialog"] h2 {
        font-size: 2.2rem !important;
        text-align: center !important;
        font-weight: 900 !important;
        color: #b91c1c !important;
    }

    div[data-testid="stDialog"] button {
        color: #b91c1c !important;
    }

    div[data-testid="stDialog"] button:hover {
        background: #fee2e2 !important;
        border-radius: 8px !important;
    }

    .popup-result-box {
        background: #ffffff;
        border: 2px solid #ef4444;
        border-radius: 20px;
        padding: 20px 22px;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.08);
    }

    .popup-result-box h3 {
        margin: 0 0 12px 0;
        color: #b91c1c;
        font-size: 1.8rem;
        font-weight: 900;
    }

    .popup-result-box p {
        margin: 6px 0;
        color: #7f1d1d;
        font-size: 1.08rem;
        font-weight: 600;
        line-height: 1.7;
    }

    [data-testid="stImage"] img {
        border-radius: 16px !important;
        border: 2px solid #ef4444;
        background: #ffffff;
        padding: 6px;
    }

    .stInfo,
    .stAlert,
    .stWarning,
    .stSuccess {
        border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
