import os
import streamlit as st
from streamlit_option_menu import option_menu

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
    default_index=1,
    orientation="horizontal"
)
st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)

# =========================
# DATA HURUF
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
# FOLDER DATASET
# =========================
HIRAGANA_DIR = "../Dataset/Hiragana Images"
KATAKANA_DIR = "../Dataset/Katakana Images"

# =========================
# FUNGSI AMBIL GAMBAR
# =========================
def get_sample_images(base_dir, char_key, max_images=6):
    folder_path = os.path.join(base_dir, char_key)

    if not os.path.exists(folder_path):
        return []

    valid_ext = (".png", ".jpg", ".jpeg", ".webp")
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(valid_ext)
    ]

    files.sort()
    return files[:max_images]

# =========================
# POPUP SAMPLE
# =========================
@st.dialog("Character Samples (キャラクターサンプル)", width="large")
def show_sample_popup(title, selected_roman, selected_char, base_dir):
    st.markdown(
        f"""
        <div class='popup-char-info'>
            <h3>{title} - {selected_roman.lower()}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    sample_images = get_sample_images(base_dir, selected_roman, max_images=6)

    if sample_images:
        cols = st.columns(3)
        for i, img_path in enumerate(sample_images):
            with cols[i % 3]:
                st.image(img_path, use_container_width=True, caption=f"Sample {i+1}")
    else:
        st.warning(f"Gambar sample untuk huruf '{selected_roman}' belum ditemukan di folder {base_dir}")

# =========================
# TAMPILKAN HURUF
# =========================
def show_character_samples(title, data_map, base_dir, key_prefix):
    with st.expander(title, expanded=False):
        st.markdown(
            f"<div class='table-title'>List of {title} Character</div>",
            unsafe_allow_html=True
        )

        items = list(data_map.items())
        cols_per_row = 5

        for i in range(0, len(items), cols_per_row):
            row_items = items[i:i + cols_per_row]
            cols = st.columns(cols_per_row)

            for j, (roman, jp_char) in enumerate(row_items):
                label = f"{jp_char}\n{roman}"
                if cols[j].button(label, key=f"{key_prefix}_{roman}", use_container_width=True):
                    show_sample_popup(title, roman, jp_char, base_dir)

# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.switch_page(".../dashboard.py")

elif page == "Data":
    show_character_samples("Hiragana (ひらがな) ", hiragana_map, HIRAGANA_DIR, "hiragana")
    show_character_samples("Katakana (カタカナ) ", katakana_map, KATAKANA_DIR, "katakana")

elif page == "Technology":
    st.switch_page('Pages/teknologi.py')

elif page == "Predict":
    st.switch_page('Pages/prediksi.py')

elif page == "Drawing":
    st.switch_page('Pages/drawing.py')

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

    .element-container, .stMarkdown {
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

    /* EXPANDER RINGKAS */
    div[data-testid="stExpander"] {
        border: 1.5px solid #d1d5db !important;
        border-radius: 18px !important;
        overflow: hidden;
        box-shadow: 0 8px 18px rgba(127, 29, 29, 0.06);
        margin-bottom: 18px;
        background: #ffffff !important;
    }

    div[data-testid="stExpander"] details {
        background: #ffffff !important;
    }

    div[data-testid="stExpander"] details summary {
        background: #ffffff !important;
        color: #b91c1c !important;
        font-weight: 900 !important;
        font-size: 1.35rem !important;
        padding: 12px 18px !important;
        min-height: auto !important;
        line-height: 1.3 !important;
        border-radius: 18px !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        background: #fff5f5 !important;
    }

    div[data-testid="stExpander"] details[open] summary {
        border-bottom: 1px solid #e5e7eb !important;
        margin-bottom: 10px !important;
    }

    .table-title {
        font-size: 1.7rem;
        font-weight: 900;
        color: #b91c1c;
        margin-bottom: 18px;
        line-height: 1.3;
    }

    /* TOMBOL HURUF */
    div.stButton > button {
        background: #ffffff !important;
        color: #b91c1c !important;
        border: 2px solid #dc2626 !important;
        border-radius: 16px !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        min-height: 78px !important;
        white-space: pre-line !important;
        line-height: 1.45 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(220, 38, 38, 0.05) !important;
    }

    div.stButton > button:hover {
        background: #fee2e2 !important;
        color: #991b1b !important;
        border-color: #b91c1c !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(220, 38, 38, 0.12) !important;
    }

    div.stButton > button:focus:not(:active) {
        border-color: #991b1b !important;
        color: #991b1b !important;
        box-shadow: 0 0 0 0.15rem rgba(220, 38, 38, 0.15) !important;
    }


    /* HEADER POPUP (judul + tombol X) */
    div[data-testid="stDialog"] h2 {
        color: #b91c1c !important;
        font-weight: 900 !important;
    }

    /* tombol close (X) */
    div[data-testid="stDialog"] button {
        font-size: 50px;
        color: #b91c1c !important;
    }

    /* biar bagian dalam popup lebih nyatu */
    div[data-testid="stDialog"] .stMarkdown {
        background: transparent !important;
    }

    /* efek hover tombol X */
    div[data-testid="stDialog"] button:hover {
        background: #fee2e2 !important;
        border-radius: 8px !important;
    }
    /* POPUP INFO */
    .popup-char-info {
        background: #ffffff;
        border: 2px solid #dc2626;
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(220, 38, 38, 0.08);
    }

    .popup-char-info h3 {
        margin: 0 0 8px 0;
        color: #b91c1c;
        font-size: 1.9rem;
        font-weight: 900;
        line-height: 1.2;
    }

    .popup-char-info p {
        margin: 0;
        color: #991b1b;
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.6;
    }

    [data-testid="stImage"] img {
        border-radius: 14px !important;
        background: #ffffff;
        padding: 6px;
        border: 2px solid #dc2626;
    }

    [data-testid="stCaptionContainer"] {
        text-align: center;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .stAlert, .stWarning {
        border-radius: 16px !important;
    }
    
    div[data-testid="stExpander"] details summary {
        font-size: 1.8rem !important;   /* BESARKAN DI SINI */
        font-weight: 900 !important;
        color: #b91c1c !important;
        padding: 16px 20px !important;
        line-height: 1.4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)