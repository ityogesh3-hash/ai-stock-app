import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

# 1. Page Config (Wide Layout)
st.set_page_config(page_title="MarketVista AI", page_icon="📈", layout="wide")

# 2. Custom CSS for Premium Theme (Dark Sidebar, Light Main, Cards)
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #f4f7f6; }
    /* Sidebar Styling (Dark) */
    [data-testid="stSidebar"] { background-color: #1e1e2d; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    /* Card Styling */
    div.stDataFrame, div[data-testid="stMetric"], div[data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    /* Headers */
    h1, h2, h3 { color: #1e1e2d; }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Navigation Mockup)
st.sidebar.title("📊 MarketVista AI")
menu = ["Dashboard", "Market Overview", "Indices", "Stocks", "Watchlist", "News & Events"]
choice = st.sidebar.radio("Navigation", menu)
st.sidebar.markdown("---")
st.sidebar.markdown("🟢 **Market Open**\n\n*Time to Close: 05:44:12*")

# 4. Top Tickers (Dummy Data for layout)
col1, col2, col3, col4 = st.columns(4)
col1.metric("NIFTY 50", "24,834.85", "+0.85%")
col2.metric("SENSEX", "81,330.56", "+0.74%")
col3.metric("BANK NIFTY", "51,274.30", "+1.05%")
col4.metric("INDIA VIX", "12.45", "-2.33%")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Main Chart & Market Breadth Grid
chart_col, breadth_col = st.columns([2, 1])

with chart_col:
    st.subheader("NIFTY 50 Trend")
    # Generate Dummy Trend Data
    dates = pd.date_range(start="2026-08-12 09:15", end="2026-08-12 15:30", freq="5min")
    prices = 24600 + np.cumsum(np.random.randn(len(dates)) * 10)
    df_trend = pd.DataFrame({"Time": dates, "Price": prices})
    
    # Plotly Line Chart
    fig = px.area(df_trend, x="Time", y="Price", color_discrete_sequence=["#636EFA"])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with breadth_col:
    st.subheader("Market Breadth")
    # Plotly Donut Chart
    labels = ['Advances', 'Declines', 'Unchanged']
    values = [1782, 980, 0]
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, marker_colors=['#00CC96', '#EF553B', '#FFA15A'])])
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, showlegend=True)
    # Add center text
    fig2.add_annotation(text="<b>2,762</b><br>Total Stocks", x=0.5, y=0.5, font_size=20, showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 6. Gainers, Losers, and REAL AI News Grid
st.subheader("Market Action & AI Signals")
grid1, grid2, grid3 = st.columns(3)

with grid1:
    st.markdown("**Top Gainers**")
    gainers = pd.DataFrame({
        "Symbol": ["TATASTEEL", "JSWSTEEL", "BAJFINANCE", "HINDALCO"],
        "LTP": ["163.45", "1,012.30", "7,156.20", "643.80"],
        "Chg%": ["+4.72%", "+4.15%", "+3.21%", "+2.98%"]
    })
    st.dataframe(gainers, hide_index=True, use_container_width=True)

with grid2:
    st.markdown("**Top Losers**")
    losers = pd.DataFrame({
        "Symbol": ["ADANIPORTS", "M&M", "NTPC", "TATAMOTORS"],
        "LTP": ["1,398.50", "2,782.60", "328.65", "1,079.40"],
        "Chg%": ["-3.45%", "-2.98%", "-2.12%", "-1.85%"]
    })
    st.dataframe(losers, hide_index=True, use_container_width=True)

with grid3:
    st.markdown("**Real-Time AI Sentiment (From Google Sheets)**")
    # Fetch REAL data from Google Sheets
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(st.secrets["google_credentials"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Stock AI Dashboard").sheet1
        data = sheet.get_all_records()
        
        if data:
            df_news = pd.DataFrame(data)
            # Show only symbol and AI signal for compact fit
            df_mini_news = df_news[['Stock Symbol', 'Recommendation']].tail(5)
            st.dataframe(df_mini_news, hide_index=True, use_container_width=True)
        else:
            st.write("Run stock_news.py to get live AI signals.")
    except Exception as e:
        st.error("Waiting for data connection...")
