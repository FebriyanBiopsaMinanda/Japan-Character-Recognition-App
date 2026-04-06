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
            An intelligent application that predicts and recognizes Japanese Hiragana and Katakana characters using CNN.
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
    default_index=0,
    orientation="horizontal"
)
st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)

# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.markdown(
        """
       <div class='section-card'>
            <h2>こんにちは, Selamat Datang</h2>
            <p>
                Aplikasi ini dikembangkan untuk membantu mengenali dan memprediksi
                karakter huruf Jepang, khususnya Hiragana dan Katakana, dengan
                memanfaatkan teknologi <strong style="color: #b91c1c;"> Convolutional Neural Network (CNN) </strong> .
                Melalui aplikasi ini, pengguna dapat memperoleh hasil prediksi
                karakter secara cepat dan akurat.
            </p>
            <br>
            <p>このアプリケーションは、畳み込みニューラルネットワーク（CNN）技術を用いて、日本語の文字、特にひらがなとカタカナを認識・予測するために開発されました。このアプリケーションを使用することで、ユーザーは高速かつ正確な文字予測結果を得ることができます。</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
elif page == "Data":
    st.switch_page('pages/data.py')

elif page == "Technology":
    st.switch_page('pages/teknologi.py')
    
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
    .section-card h2 {
    margin-top: 0;
    color: #1f2937;
    font-size: 2rem;
    font-weight: 800;
    }

    .section-card p {
        color: #374151;
        font-size: 1.25rem;
        line-height: 1.8;
        margin-bottom: 0;
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
    </style>
    """,
    unsafe_allow_html=True
)
