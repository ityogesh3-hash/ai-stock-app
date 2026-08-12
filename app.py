import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import yfinance as yf  # <-- PUDHUSA ADD PANNA LIBRARY

# 1. Page Config 
st.set_page_config(page_title="MarketVista AI", page_icon="📈", layout="wide")

# 2. Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #1e1e2d; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    div.stDataFrame, div[data-testid="stMetric"], div[data-testid="stPlotlyChart"] {
        background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3, h4 { color: #1e1e2d; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Fetch LIVE Market Data (Cached to load fast)
@st.cache_data(ttl=60) # Refresh every 1 minute
def get_live_market():
    try:
        # Fetching real Nifty 50 data
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="1d", interval="5m")
        latest_price = hist['Close'].iloc[-1] if not hist.empty else 0
        
        # Sensex & Bank Nifty
        s_price = yf.Ticker("^BSESN").history(period="1d")['Close'].iloc[-1]
        b_price = yf.Ticker("^NSEBANK").history(period="1d")['Close'].iloc[-1]
        return hist, latest_price, s_price, b_price
    except:
        return pd.DataFrame(), 0, 0, 0

nifty_hist, n_price, s_price, b_price = get_live_market()

st.sidebar.title("📊 MarketVista AI")
st.sidebar.markdown("---")
st.sidebar.markdown("🟢 **Market Open/Live**")

# 4. Top Tickers (NOW REAL TIME DATA!)
col1, col2, col3, col4 = st.columns(4)
col1.metric("NIFTY 50", f"₹ {n_price:,.2f}" if n_price else "Loading...")
col2.metric("SENSEX", f"₹ {s_price:,.2f}" if s_price else "Loading...")
col3.metric("BANK NIFTY", f"₹ {b_price:,.2f}" if b_price else "Loading...")
col4.metric("INDIA VIX", "Live") # VIX static for layout

st.markdown("<br>", unsafe_allow_html=True)

# 5. TODAY'S SIGNALS (From Google Sheets)
st.subheader("🎯 AI Signals: Buy, Sell & Hold")
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["google_credentials"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Stock AI Dashboard").sheet1
    data = sheet.get_all_records()
    
    if data:
        df_news = pd.DataFrame(data)
        tab1, tab2, tab3, tab4 = st.tabs(["🟢 BUY Signals", "🔴 SELL Signals", "🟡 HOLD Signals", "🌐 ALL Signals"])
        with tab1:
            buy_stocks = df_news[df_news['Recommendation'] == 'Buy']
            st.dataframe(buy_stocks, hide_index=True, use_container_width=True) if not buy_stocks.empty else st.info("No 'BUY' signals.")
        with tab2:
            sell_stocks = df_news[df_news['Recommendation'] == 'Sell']
            st.dataframe(sell_stocks, hide_index=True, use_container_width=True) if not sell_stocks.empty else st.info("No 'SELL' signals.")
        with tab3:
            hold_stocks = df_news[df_news['Recommendation'] == 'Hold']
            st.dataframe(hold_stocks, hide_index=True, use_container_width=True) if not hold_stocks.empty else st.info("No 'HOLD' signals.")
        with tab4:
            st.dataframe(df_news, hide_index=True, use_container_width=True)
except:
    st.error("Waiting for AI data...")

st.markdown("---")

# 6. Main Chart (REAL NIFTY 50 LIVE CHART)
st.subheader("📉 Real-Time Nifty 50 Trend")
chart_col, breadth_col = st.columns([2, 1])

with chart_col:
    if not nifty_hist.empty:
        df_trend = nifty_hist.reset_index()
        fig = px.area(df_trend, x="Datetime", y="Close", color_discrete_sequence=["#00CC96"])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="Price (₹)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Live chart loading...")

with breadth_col:
    # Market Breadth (Kept static for layout feel, dynamic breadth requires paid APIs)
    labels = ['Advances', 'Declines']
    values = [32, 18] # Example Nifty 50 breadth
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, marker_colors=['#00CC96', '#EF553B'])])
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, showlegend=True)
    fig2.add_annotation(text="<b>50</b><br>Nifty Stocks", x=0.5, y=0.5, font_size=20, showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)
