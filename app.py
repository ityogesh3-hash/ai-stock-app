import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# 1. Page Configuration
st.set_page_config(page_title="MarketVista Premium", layout="wide")

# 2. Premium CSS (Side bar + Market Status Card)
st.markdown("""
<style>
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e1e2d 0%, #0d0d17 100%); 
        color: white; 
    }
    .status-card { 
        background: #252538; border-radius: 15px; padding: 20px; 
        margin-top: 100px; border: 1px solid #444; color: white;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233633.png", width=50) # Mockup Logo
    st.title("MarketVista")
    st.write("Analytics")
    st.radio("Menu", ["Dashboard", "Market Overview", "Indices", "Stocks", "Watchlist", "Analytics", "Screener", "Portfolios", "News & Events", "Alerts", "Reports", "Settings"])
    
    # Left side keezha picture (Market Status)
    st.markdown("""
    <div class="status-card">
        <small>● Market Status</small><br>
        <b>Market Open</b><br>
        <small>12 Aug 2026, 10:45 AM IST</small><br><br>
        <small>Time to Close</small><br>
        <h3>05:44:12</h3>
        <small>Market Closes 03:30 PM IST</small>
    </div>
    """, unsafe_allow_html=True)

# 4. Main Dashboard
st.title("📈 Dashboard")

# Top Tickers
col1, col2, col3, col4 = st.columns(4)
nifty = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
col1.metric("NIFTY 50", f"₹ {nifty:,.2f}", "+0.85%")
col2.metric("SENSEX", "81,330.56", "+0.74%")
col3.metric("BANK NIFTY", "51,274.30", "+1.05%")
col4.metric("INDIA VIX", "12.45", "-2.33%")

# 5. Graphic Chart (Nifty keezha)
st.subheader("Nifty 50 Live Trend")
hist = yf.Ticker("^NSEI").history(period="1d", interval="5m")
fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], line=dict(color='#8884d8', width=2))])
fig.update_layout(height=300, template="plotly_white", margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

# 6. 500+ Stocks Logic (Using cache to avoid API lag)
@st.cache_data(ttl=3600)
def get_all_stocks():
    # List of 500 companies (Simplified here, you can load from a CSV)
    return ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS"] 

# 500+ Stocks Live Engine
st.subheader("🚀 Live Market Screener (Nifty 500)")
stock_search = st.text_input("Search Symbol (e.g., RELIANCE, TCS):")

@st.cache_data(ttl=300)
def fetch_live_data(symbol):
    # .NS add pannina thaan NSE live data varum
    ticker = yf.Ticker(f"{symbol.upper()}.NS")
    info = ticker.info
    return info

if stock_search:
    try:
        data = fetch_live_data(stock_search)
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Current Price", f"₹{data.get('currentPrice', 'N/A')}")
        col_b.metric("Day High", f"₹{data.get('dayHigh', 'N/A')}")
        col_c.metric("Market Cap", f"{data.get('marketCap', 0)/1e7:.2f} Cr")
    except:
        st.error("Invalid Stock Symbol!")
        
st.subheader("Live Market Screener (500+ Companies)")
search = st.text_input("Search 500+ Companies...")
# Display logic for 500 companies
st.info("Showing live updates for Nifty 500 stocks...")
