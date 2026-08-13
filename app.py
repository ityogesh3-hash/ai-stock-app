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
    import streamlit as st
import pandas as pd
from nsepython import nse_eq

def get_nse_live_data(symbol):
    try:
        # NSE official live data fetcher
        data = nse_eq(symbol)
        last_price = data['priceInfo']['lastPrice']
        change = data['priceInfo']['pChange']
        return last_price, change
    except:
        return 0.0, 0.0

def main_dashboard():
    st.title("🚀 MarketX Institutional Terminal v2.0")
    
    # 1. Market Intelligence Signals Table
    st.subheader("📊 AI Actionable Signals & Recommendations")
    df_signals = pd.DataFrame({
        "Stock / Asset": ["RELIANCE", "TCS", "CRUDE OIL"],
        "Signal": ["🟢 BUY", "🔴 SELL / EXIT", "🟡 HOLD"],
        "Confidence": ["84 / 100", "78 / 100", "65 / 100"],
        "Entry Zone": ["₹1,475 - ₹1,490", "₹3,850", "₹6,200"],
        "Target / Exit": ["T1: ₹1,535", "Exit at Resistance", "Wait for breakout"],
        "Action Reason": [
            "Breakout confirmed with 2.4x volume spike.", 
            "RSI near overbought zone; momentum fading.", 
            "Consolidating inside range; hold till support holds."
        ]
    })
    st.table(df_signals)

    # 2. My Stock List (Portfolio Tracking with NSE Live Data)
    st.subheader("💼 My Portfolio & Exit Trigger List")
    
    # Sample user holdings (Can be connected to database later)
    portfolio = [
        {"Stock": "RELIANCE", "Buy Price": 1420.0, "Target Sell": 1550.0},
        {"Stock": "TCS", "Buy Price": 3750.0, "Target Sell": 3950.0}
    ]
    
    portfolio_data = []
    for item in portfolio:
        live_price, p_change = get_nse_live_data(item['Stock'])
        if live_price > 0:
            pl_amount = ((live_price - item['BuyPrice']) / item['BuyPrice']) * 100
            # Automatic Recommendation Trigger
            recommendation = "HOLD" if live_price < item['TargetSell'] else "SELL NOW (Target Reached)"
        else:
            live_price = "Fetching..."
            pl_amount = 0.0
            recommendation = "N/A"
            
        portfolio_data.append({
            "Stock": item['Stock'],
            "Buy Price": f"₹{item['BuyPrice']}",
            "Live Price": f"₹{live_price}" if isinstance(live_price, float) else live_price,
            "P/L %": f"{round(pl_amount, 2)}%" if live_price != "Fetching..." else "0%",
            "Recommendation / Exit Trigger": recommendation
        })
    
    st.table(pd.DataFrame(portfolio_data))
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
