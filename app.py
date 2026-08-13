import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="MarketX Terminal", layout="wide")

# CSS to make it "Cinematic & Clean"
st.markdown("""
<style>
    body { background-color: #0a0e1a; color: #f4f7fb; }
    .card { background: #141a29; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 20px; }
    .stApp { padding: 40px; }
    h2, h3 { color: #22d3ee; }
</style>
""", unsafe_allow_html=True)

# Authentication State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def main_dashboard():
    st.title("🚀 MarketX Terminal v2.0")
    
    # 1. Market Signals Table
    st.subheader("Market Intelligence Signals")
    df_signals = pd.DataFrame({
        "Stock": ["RELIANCE", "TCS", "CRUDE OIL"],
        "Signal": ["BUY", "SELL", "HOLD"],
        "Confidence": ["84/100", "78/100", "65/100"],
        "Entry": ["₹1480", "₹3850", "₹6200"]
    })
    st.table(df_signals)

    # 2. My Stock List (Portfolio)
    st.subheader("My Portfolio List")
    df_portfolio = pd.DataFrame({
        "Stock": ["RELIANCE"],
        "Buy Price": ["₹1400"],
        "Current": ["₹1485"],
        "P/L": ["+6.07%"],
        "Sell Trigger": ["₹1550"]
    })
    st.table(df_portfolio)
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Login Logic
if not st.session_state.logged_in:
    with st.form("login"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if user == "admin" and pwd == "marketx2026":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Login Failed")
else:
    main_dashboard()
