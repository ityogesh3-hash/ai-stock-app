import streamlit as st
import streamlit.components.v1 as components
import datetime

# Page configuration
st.set_page_config(page_title="MarketX — Stock Market Analytics", page_icon="📈", layout="wide")

# Initialize Session State for Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login Function / Page UI
def login_page():
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: #141a29;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f4f7fb;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }
        .login-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
            text-align: center;
            background: linear-gradient(100deg, #60a5fa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-sub {
            font-size: 13px;
            color: #818ba3;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">MarketX Terminal</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Enter credentials to access analytics</div>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Secure Login", use_container_width=True):
            # Default credentials for demo
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
    # Clean IST Time Display on top bar if needed
    current_ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = current_ist_time.strftime("%d %b %Y, %I:%M:%S %p IST")
    
    st.sidebar.success(f"🟢 Connected | {formatted_time}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Load and Render the Stunning HTML Dashboard via Streamlit Component
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        # Render full screen HTML dashboard component (height set to 1050px for smooth scrolling)
        components.html(html_content, height=1050, scrolling=True)
    except FileNotFoundError:
        st.error("⚠️ Error: `dashboard.html` file not found in your repository! Please upload it.")
