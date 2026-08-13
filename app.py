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
    
    # 1. Market Intelligence Signals Table
    st.subheader("📊 AI Actionable Signals & Recommendations")
    df_signals = pd.DataFrame({
        "Stock / Asset": ["RELIANCE.BSE", "TCS.BSE"],
        "Signal": ["🟢 BUY", "🔴 SELL / EXIT"],
        "Confidence": ["84 / 100", "78 / 100"],
        "Entry Zone": ["₹1,475 - ₹1,490", "₹3,850"],
        "Target / Exit": ["T1: ₹1,535", "Exit at Resistance"]
    })
    st.table(df_signals)

    # 2. My Stock List (Portfolio Tracking with Alpha Vantage)
    st.subheader("💼 My Portfolio (Live API Data)")
    
    # Unga own stock list (Target Sell price oda set panirukom)
    portfolio = [
        {"Stock": "RELIANCE.BSE", "Buy Price": 1420.0, "Target Sell": 1550.0},
        {"Stock": "TCS.BSE", "Buy Price": 3750.0, "Target Sell": 3950.0}
    ]
    
    portfolio_data = []
    for item in portfolio:
        live_price = get_pro_data(item['Stock'])
        
        # Calculations based on Live Price
        if isinstance(live_price, float):
            pl_amount = ((live_price - item['Buy Price']) / item['Buy Price']) * 100
            recommendation = "HOLD 🟡" if live_price < item['Target Sell'] else "SELL NOW 🔴"
            live_price_str = f"₹{live_price:.2f}"
            pl_str = f"{pl_amount:.2f}%"
        else:
            live_price_str = live_price
            pl_str = "0.00%"
            recommendation = "Waiting for data..."
            
        portfolio_data.append({
            "Stock Name": item['Stock'],
            "Buy Price": f"₹{item['Buy Price']}",
            "Live Price": live_price_str,
            "P/L %": pl_str,
            "Exit Recommendation": recommendation
        })
    
    st.table(pd.DataFrame(portfolio_data))
    
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
