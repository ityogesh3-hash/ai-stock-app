import streamlit as st
import streamlit.components.v1 as components
import datetime

# Page configuration (Wide layout & collapsed sidebar by default)
st.set_page_config(
    page_title="MarketX — Stock Market Analytics", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Default UI elements (Header, Footer, Menu, Sidebar toggle)
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        .block-container {
            padding: 0px !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 99999;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize Session State for Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("""
    <style>
        .login-box {
            max-width: 420px;
            margin: 120px auto;
            padding: 40px;
            background: #141a29;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f4f7fb;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        }
        .login-heading {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 6px;
            text-align: center;
            background: linear-gradient(100deg, #60a5fa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-heading">MarketX Terminal</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#818ba3; text-align:center; margin-bottom:25px; font-size:13px;">Enter credentials to access cinematic analytics</p>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Secure Login", use_container_width=True):
            if username == "admin" and password == "marketx2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Username or Password!")
        st.markdown('</div>', unsafe_allow_html=True)

# Check Login Status
if not st.session_state.logged_in:
    login_page()
else:
    # Load and Render Full-Screen HTML Dashboard
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Render HTML to occupy full screen viewport
        components.html(html_content, height=1200, scrolling=True)
        
    except FileNotFoundError:
        st.error("⚠️ Error: `dashboard.html` file not found in repository!")
