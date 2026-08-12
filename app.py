import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# 1. Page Configuration (Wide Layout)
st.set_page_config(page_title="MarketVista Premium AI", page_icon="📈", layout="wide")

# 2. Premium Theme CSS Styling
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e1e2d 0%, #0d0d17 100%); 
        color: white; 
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div.stDataFrame, div[data-testid="stMetric"], div[data-testid="stPlotlyChart"] {
        background-color: white; border-radius: 12px; padding: 15px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 { color: #1e1e2d; }
    .status-card { 
        background: #252538; border-radius: 12px; padding: 15px; 
        margin-top: 50px; border: 1px solid #444; color: white;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Design & Stock Selector (500+ Stocks from CSV)
with st.sidebar:
    st.title("📊 MarketVista")
    st.write("Pro Analytics")
    st.markdown("---")
    
    # Load 500+ stocks dropdown
    try:
        df_stocks = pd.read_csv("stocks.csv")
        selected_stock = st.selectbox("🔍 Search 500+ Stocks:", df_stocks['Symbol'].tolist())
    except:
        selected_stock = "RELIANCE"
        st.warning("stocks.csv not found, using default.")
        
    st.markdown("---")
    
    # Left side keezha picture (Market Status Card like your design)
    st.markdown("""
    <div class="status-card">
        <small style="color: #00CC96;">● Market Status</small><br>
        <b>Market Open</b><br>
        <small>12 Aug 2026, 10:45 AM IST</small><br><br>
        <small>Time to Close</small><br>
        <h3 style="color: white; margin:0;">05:44:12</h3>
        <small>Market Closes: 03:30 PM IST</small>
    </div>
    """, unsafe_allow_html=True)

# 4. Main Dashboard Header & Live Tickers
st.title("📈 Pro AI Stock Screener & Dashboard")

col1, col2, col3, col4 = st.columns(4)
try:
    n_price = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
    s_price = yf.Ticker("^BSESN").history(period="1d")['Close'].iloc[-1]
    b_price = yf.Ticker("^NSEBANK").history(period="1d")['Close'].iloc[-1]
    
    col1.metric("NIFTY 50", f"₹ {n_price:,.2f}", "+0.85%")
    col2.metric("SENSEX", f"₹ {s_price:,.2f}", "+0.74%")
    col3.metric("BANK NIFTY", f"₹ {b_price:,.2f}", "+1.05%")
    col4.metric("INDIA VIX", "12.45", "-2.33%")
except:
    col1.metric("NIFTY 50", "Live Loading...")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Selected Stock Live Screener Details (From 500 Stocks List)
if selected_stock:
    st.subheader(f"📊 Live Data: {selected_stock}")
    try:
        ticker_info = yf.Ticker(f"{selected_stock}.NS").info
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Current Price", f"₹ {ticker_info.get('currentPrice', 'N/A')}")
        sc2.metric("Day High", f"₹ {ticker_info.get('dayHigh', 'N/A')}")
        sc3.metric("52 Week High", f"₹ {ticker_info.get('fiftyTwoWeekHigh', 'N/A')}")
        sc4.metric("Market Cap", f"₹ {ticker_info.get('marketCap', 0)/1e7:,.2f} Cr")
    except:
        st.info("Fetching details for selected stock...")

st.markdown("---")

# 6. Real-Time Nifty 50 Graphic Chart (Nifty keezha chart)
st.subheader("📉 Real-Time Nifty 50 Trend Chart")
chart_col, breadth_col = st.columns([2, 1])

with chart_col:
    try:
        hist = yf.Ticker("^NSEI").history(period="1d", interval="5m")
        if not hist.empty:
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#636EFA', width=2))])
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.write("Chart loading...")

with breadth_col:
    st.subheader("Market Breadth")
    labels = ['Advances', 'Declines']
    values = [35, 15]
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, marker_colors=['#00CC96', '#EF553B'])])
    fig2.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), showlegend=True)
    fig2.add_annotation(text="<b>50</b><br>Nifty Stocks", x=0.5, y=0.5, font_size=18, showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 7. Google Sheets AI Signals (Tabs for Buy, Sell, Hold)
st.subheader("🎯 AI Market Signals (Automated)")

try:
    creds_dict = json.loads(st.secrets["google_credentials"])
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Stock AI Dashboard").sheet1
    df = pd.DataFrame(sheet.get_all_records())
    
    if not df.empty:
        tab1, tab2, tab3, tab4 = st.tabs(["🟢 BUY Signals", "🔴 SELL Signals", "🟡 HOLD Signals", "🌐 ALL Signals"])
        
        with tab1:
            st.dataframe(df[df['Recommendation'] == 'Buy'], hide_index=True, use_container_width=True)
        with tab2:
            st.dataframe(df[df['Recommendation'] == 'Sell'], hide_index=True, use_container_width=True)
        with tab3:
            st.dataframe(df[df['Recommendation'] == 'Hold'], hide_index=True, use_container_width=True)
        with tab4:
            st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("Waiting for data from automation script...")
except Exception as e:
    st.warning("Database connection waiting...")
