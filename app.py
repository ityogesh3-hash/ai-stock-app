import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import yfinance as yf

# Page Setup
st.set_page_config(page_title="MarketVista AI", page_icon="📈", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #1e1e2d; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .css-1r6slb0 { background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 MarketVista AI")
st.sidebar.markdown("---")

# Data
try:
    nifty = yf.Ticker("^NSEI").history(period="1d")
    n_price = nifty['Close'].iloc[-1]
    col1, col2 = st.columns(2)
    col1.metric("NIFTY 50", f"₹ {n_price:,.2f}")
except:
    col1.metric("NIFTY 50", "Loading...")

# Google Sheet Data
try:
    creds_dict = json.loads(st.secrets["google_credentials"])
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Stock AI Dashboard").sheet1
    df = pd.DataFrame(sheet.get_all_records())
    
    st.subheader("🎯 AI Market Signals")
    tab1, tab2, tab3 = st.tabs(["🟢 BUY", "🔴 SELL", "🟡 HOLD"])
    
    with tab1:
        st.dataframe(df[df['Recommendation'] == 'Buy'], use_container_width=True)
    with tab2:
        st.dataframe(df[df['Recommendation'] == 'Sell'], use_container_width=True)
    with tab3:
        st.dataframe(df[df['Recommendation'] == 'Hold'], use_container_width=True)
except Exception as e:
    st.error(f"Data loading error: {e}")
