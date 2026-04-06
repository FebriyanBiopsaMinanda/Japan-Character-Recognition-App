import os
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_drawable_canvas import st_canvas
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
        raise FileNotFoundError(f"File class names tidak ditemukan: {CLASS_NAMES_PATH}")

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
    default_index=4,
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
# PARSE LABEL
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
# PREPROCESS CANVAS IMAGE
# =========================
def preprocess_canvas_image(canvas_image_rgba):
    image = canvas_image_rgba[:, :, :3].astype("uint8")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # canvas putih + coretan hitam -> langsung resize
    gray = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))

    preview = gray.copy()

    image_input = gray.astype("float32") / 255.0
    image_input = np.expand_dims(image_input, axis=-1)
    image_input = np.expand_dims(image_input, axis=0)

    return preview, image_input

# =========================
# CEK APAKAH CANVAS KOSONG
# =========================
def is_canvas_blank(canvas_rgba):
    rgb = canvas_rgba[:, :, :3]
    return np.all(rgb == 255)

# =========================
# AMBIL SAMPEL
# =========================
HIRAGANA_DIR = "../Dataset/Hiragana Images"
KATAKANA_DIR = "../Dataset/Katakana Images"

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
def show_prediction_popup(canvas_rgba, script_type, romaji, char_jp, confidence):

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        preview_canvas = canvas_rgba[:, :, :3].astype("uint8")
        st.image(preview_canvas, use_container_width=True)

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
# LOAD MODEL
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
# SESSION STATE
# =========================
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

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
    st.switch_page("pages/prediksi.py")

elif page == "Canvas":
    left_col, right_col = st.columns([1.15, 1], gap="large")

    with left_col:

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=12,
            stroke_color="#000000",
            background_color="#FFFFFF",
            width=800,
            height=500,
            drawing_mode="freedraw",
            update_streamlit=True,
            key=f"canvas_{st.session_state.canvas_key}",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4, gap="medium")

        with btn_col1:
            if st.button("Reset (リセット)", use_container_width=True):
                st.session_state.canvas_key += 1
                st.rerun()

    with right_col:

        st.markdown(
            """
            <div class='predict-card'>
                <h3>Prediction Info (予測情報)</h3>
                <p>Gambar huruf Hiragana atau Katakana pada canvas, lalu klik tombol prediksi untuk melihat hasilnya.</p><br>
                <p>キャンバスにひらがなまたはカタカナの文字を描き、予測ボタンをクリックすると結果が表示されます。</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if not model_ready:
            st.error("Model belum siap digunakan. Periksa file model dan class names.")
        elif canvas_result.image_data is None or is_canvas_blank(canvas_result.image_data):
            st.info("""Canvas masih kosong. Silakan gambar huruf terlebih dahulu.
                    \nキャンバスはまだ真っ白です。まずは文字を描いてください。""")
        else:
            st.success("""Canvas siap diprediksi. Klik tombol Prediksi Sekarang.
                       \n予測の準備ができました。「今すぐ予測」ボタンをクリックしてください。""")

        btn_col1, btn_col2, btn_col3 = st.columns(3, gap="medium")

        with btn_col3:
            predict_clicked = st.button("Predict (予測) ", use_container_width=True)
            
        if predict_clicked:
            if not model_ready:
                st.error("""Model belum siap digunakan. Periksa file model dan class names.
                         \nモデルはまだ使用できる状態ではありません。モデルファイルとクラス名を確認してください。""")
                
            elif canvas_result.image_data is None or is_canvas_blank(canvas_result.image_data):
                st.error("""Canvas masih kosong. Gambar huruf terlebih dahulu.
                         \nキャンバスはまだ真っ白です。まずは文字を描きましょう。""")
            else:
                _, image_input = preprocess_canvas_image(canvas_result.image_data)
                prediction = model.predict(image_input, verbose=0)[0]

                pred_index = int(np.argmax(prediction))
                pred_label = class_names[pred_index]
                confidence = float(prediction[pred_index])

                script_type, romaji, char_jp = parse_prediction_label(pred_label)

                show_prediction_popup(
                    canvas_result.image_data,
                    script_type,
                    romaji,
                    char_jp,
                    confidence
                )

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

    .canvas-card,
    .predict-card {
        background: #ffffff;
        border: 1px solid #fecaca;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.08);
        margin-bottom: 20px;
    }

    .canvas-card h3,
    .predict-card h3 {
        margin: 0 0 8px 0;
        color: #991b1b;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .canvas-card p,
    .predict-card p {
        margin: 0;
        color: #4b5563;
        font-size: 1rem;
        line-height: 1.8;
    }

    .canvas-wrap {
        background: #ffffff;
        border: 2px solid #ef4444;
        border-radius: 22px;
        padding: 14px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.08);
        margin-bottom: 16px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #b91c1c 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        font-size: 1.05rem !important;
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
    .stSuccess
    .stErorr{
        border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
