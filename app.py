import streamlit as st
import pandas as pd
import requests # Advanced API-a call panna use aagum (No extra installation needed)

# Page Configuration
st.set_page_config(page_title="MarketX Terminal", layout="wide")

# Authentication State
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# ==========================================
# ADVANCED API ENGINE (Alpha Vantage)
# ==========================================
API_KEY = 'M3IETCMSKK9NI07U' # <-- Neenga vanguana Alpha vantage API key-a inga 'demo' ku badhila podanum

def get_pro_data(symbol):
    # Professional-grade Live Price Fetcher
    try:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
        r = requests.get(url)
        data = r.json()
        price = float(data['Global Quote']['05. price'])
        return price
    except:
        return "Fetching API..."

# ==========================================
# MAIN DASHBOARD UI
# ==========================================
def main_dashboard():
    st.title("🚀 MarketX Institutional Terminal v2.0")
    
    # ==========================================
    # SEARCH BOX & MARKET PULSE SECTION
    # ==========================================
    st.markdown("<p style='color:#22d3ee; font-family:monospace; font-size:12px; letter-spacing:2px;'>— SECTION 01 — LIVE DATA</p>", unsafe_allow_html=True)
    st.markdown("<h2>Market Pulse</h2>", unsafe_allow_html=True)
    st.write("Every major index and asset, streaming in real time. Search any stock below.")
    
    # 1. Search Box
    search_col1, search_col2 = st.columns([1, 2])
    with search_col1:
        # Ippo demo-kku sila top stocks list panrom. Pindadi idhai Google Sheets-la irundhu eduypom.
        stock_list = ["RELIANCE.BSE", "TCS.BSE", "INFY.BSE", "HDFCBANK.BSE", "TATAMOTORS.BSE"]
        selected_stock = st.selectbox("🔍 Search 1000+ Stocks", stock_list)
        
    # 2. Fetch Live Data for Searched Stock
    if selected_stock:
        live_price = get_pro_data(selected_stock)
        
        # Design exactly like your picture
        if isinstance(live_price, float):
            price_display = f"{live_price:,.2f}"
            color = "#34d399" # Green
            arrow = "▲"
            change = "+1.24%" # Mock change percentage for UI
        else:
            price_display = "Fetching..."
            color = "#818ba3" # Grey
            arrow = "⏱"
            change = "..."

        # CSS for the Exact Market Pulse Card
        pulse_card_html = f"""
        <div style="background-color: #1a2033; padding: 24px; border-radius: 16px; width: 280px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <span style="color: #818ba3; font-size: 13px; font-weight: 600; letter-spacing: 1px;">{selected_stock.split('.')[0]}</span>
                <span style="background: rgba(255,255,255,0.1); color: #c3cbdc; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: bold;">₹</span>
            </div>
            <div style="color: #f4f7fb; font-size: 32px; font-weight: bold; margin-bottom: 10px; font-family: 'Inter', sans-serif;">
                {price_display}
            </div>
            <div style="color: {color}; font-size: 14px; font-weight: bold; margin-bottom: 25px;">
                {arrow} {change}
            </div>
            <div style="height: 2px; width: 100%; background: linear-gradient(90deg, {color}, transparent); border-radius: 2px;"></div>
        </div>
        """
        st.markdown(pulse_card_html, unsafe_allow_html=True)
    
    st.markdown("---") # Divider

    # ==========================================
    # PORTFOLIO & SIGNALS (Pazhaiya code apdiye irukku)
    # ==========================================
    st.subheader("📊 AI Actionable Signals & Recommendations")
    df_signals = pd.DataFrame({
        "Stock / Asset": ["RELIANCE.BSE", "TCS.BSE"],
        "Signal": ["🟢 BUY", "🔴 SELL / EXIT"],
        "Confidence": ["84 / 100", "78 / 100"],
        "Entry Zone": ["₹1,475 - ₹1,490", "₹3,850"],
        "Target / Exit": ["T1: ₹1,535", "Exit at Resistance"]
    })
    st.table(df_signals)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
# ==========================================
# SECURE LOGIN SYSTEM
# ==========================================
if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("MarketX Terminal Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Secure Login"):
            if user == "admin" and pwd == "marketx2026":
                st.session_state.logged_in = True
                st.rerun()
            else: 
                st.error("Invalid Username or Password!")
else:
    main_dashboard()
