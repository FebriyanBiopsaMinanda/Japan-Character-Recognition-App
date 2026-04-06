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
    default_index=2,
    orientation="horizontal"
)
st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)

# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.switch_page("dashboard.py")

elif page == "Data":
    st.switch_page('pages/data.py')

elif page == "Technology":

    st.markdown("<div class='tech-grid'>", unsafe_allow_html=True)

    
    col1, col2, col3, col4, col5 = st.columns(5, gap="large")
    with col1:
        st.markdown(
        """
        <div class='tech-card numpy'>
            <img src='https://numpy.org/images/logo.svg' class='tech-logo'>
            <h4>NumPy</h4>
            <p>
                NumPy digunakan untuk mengelola array dan operasi numerik yang dibutuhkan
                dalam proses pengolahan data citra serta komputasi matriks.
            </p>
            <br>
            <p>NumPyは、画像データ処理や行列計算に必要な配列や数値演算を管理するために使用されます。</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    with col2:
        st.markdown(
        """
        <div class='tech-card opencv'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/3/32/OpenCV_Logo_with_text_svg_version.svg' class='tech-logo'>
            <h4>OpenCV</h4>
            <p>
                OpenCV dimanfaatkan untuk membaca, memproses, dan memanipulasi gambar
                karakter agar siap digunakan pada tahap prediksi.
            </p>
            <br>
            <p>OpenCVは、文字画像を読み込み、処理し、操作して、予測段階で使用できる状態にするために使用されます。</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    with col3:
        st.markdown(
        """
        <div class='tech-card tensorflow'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg' class='tech-logo'>
            <h4>TensorFlow</h4>
            <p>
                TensorFlow berperan sebagai framework utama dalam membangun,
                melatih, dan menjalankan model deep learning.
            </p>
            <br>
            <p>TensorFlowは、深層学習モデルの構築、トレーニング、実行のための主要なフレームワークとして機能します。</p>
        </div>
        """,
        unsafe_allow_html=True
        )
        
        

    with col4:
        st.markdown(
        """
        <div class='tech-card keras'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/a/ae/Keras_logo.svg' class='tech-logo'>
            <h4>Keras</h4>
            <p>
                Keras digunakan untuk mempermudah perancangan arsitektur model,
                sehingga proses pengembangan jaringan saraf menjadi lebih sederhana.
            </p>
            <br>
            <p>Kerasはモデルアーキテクチャの設計を簡素化するために使用され、それによってニューラルネットワークの開発プロセスが簡素化されます。</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    with col5:
        st.markdown(
        """
        <div class='tech-card cnn'>
            <img src='https://cdn-icons-png.flaticon.com/256/6461/6461928.png' class='tech-logo'>
            <h4>Convolutional Neural Network (CNN)</h4>
            <p>
                CNN merupakan metode utama yang digunakan untuk mengenali pola visual
                pada citra huruf Hiragana dan Katakana secara otomatis.
            </p>
            <br>
            <p>CNNは、ひらがなとカタカナの文字画像における視覚パターンを自動的に認識するために用いられる主要な手法である。</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    
elif page == "Predict":
    st.switch_page('pages/prediksi.py')

elif page == "Canvas":
    st.switch_page('pages/drawing.py')


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
        background: #;
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

    .section-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(127, 29, 29, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.15);
    }

    .feature-box {
        background: linear-gradient(180deg, #ffffff 0%, #fff7f7 100%);
        border: 1px solid #fecaca;
        border-radius: 18px;
        padding: 20px;
        min-height: 150px;
        height: 100%;
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.06);
    }

    .feature-box h4 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #7f1d1d;
        font-size: 1.12rem;
    }

    .feature-box p {
        margin-bottom: 0;
        color: #4b5563;
        font-size: 0.98rem;
        line-height: 1.7;
    }

    .stInfo {
        border-radius: 16px;
    }
    
    .tech-intro {
        background: linear-gradient(180deg, #fff1f2 0%, #ffe4e6 100%);
        border: 1px solid #fecdd3;
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(244, 114, 182, 0.08);
        }

    .tech-intro h3 {
        margin: 0 0 8px 0;
        color: #9f1239;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .tech-intro p {
        margin: 0;
        color: #4b5563;
        font-size: 1rem;
        line-height: 1.8;
    }

    .tech-card {
        background: linear-gradient(180deg, #fffafb 0%, #ffecef 100%);
        border: 1px solid #fbcfe8;
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 22px;
        min-height: 270px;
        text-align: center;
        box-shadow: 0 10px 24px rgba(244, 114, 182, 0.10);
        transition: all 0.3s ease;
    }

    .tech-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 28px rgba(244, 114, 182, 0.16);
    }

    .tech-logo {
        width: 90px;
        height: 90px;
        object-fit: contain;
        margin-bottom: 14px;
    }

    .tech-card h4 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #9f1239;
        font-size: 1.18rem;
        font-weight: 800;
    }

    .tech-card p {
        margin-bottom: 0;
        color: #4b5563;
        font-size: 0.97rem;
        line-height: 1.75;
    }
    
    /* DEFAULT tetap */
.tech-card {
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 22px;
    min-height: 270px;
    text-align: center;
    box-shadow: 0 10px 24px rgba(244, 114, 182, 0.10);
    transition: all 0.3s ease;
}

    /* WARNA BORDER PER TEKNOLOGI */
    .tech-card.numpy {
        border: 2px solid #fda4af; /* pink soft */
    }

    .tech-card.opencv {
        border: 2px solid #fb7185; /* merah muda */
    }

    .tech-card.tensorflow {
        border: 2px solid #f97316; /* orange kemerahan */
    }

    .tech-card.keras {
        border: 2px solid #f43f5e; /* merah kuat */
    }

    .tech-card.cnn {
        border: 2px solid #be123c; /* merah tua */
    }
    
    .tech-card.numpy:hover {
    box-shadow: 0 10px 25px rgba(253, 164, 175, 0.4);
}

    .tech-card.opencv:hover {
        box-shadow: 0 10px 25px rgba(251, 113, 133, 0.4);
    }

    .tech-card.tensorflow:hover {
        box-shadow: 0 10px 25px rgba(249, 115, 22, 0.4);
    }

    .tech-card.keras:hover {
        box-shadow: 0 10px 25px rgba(244, 63, 94, 0.4);
    }

    .tech-card.cnn:hover {
        box-shadow: 0 10px 25px rgba(190, 18, 60, 0.4);
    }
        </style>
    """,
    unsafe_allow_html=True
)
