import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# 1. Page Config (Wide Layout)
st.set_page_config(page_title="MarketVista AI", page_icon="📈", layout="wide")

# 2. Custom CSS for Premium Theme
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #1e1e2d; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    div.stDataFrame, div[data-testid="stMetric"], div[data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3, h4 { color: #1e1e2d; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Navigation Mockup)
st.sidebar.title("📊 MarketVista AI")
st.sidebar.markdown("---")
st.sidebar.markdown("🟢 **Market Open**\n\n*Time to Close: 05:44:12*")

# 4. Top Tickers (4 in a line)
col1, col2, col3, col4 = st.columns(4)
col1.metric("NIFTY 50", "24,834.85", "+0.85%")
col2.metric("SENSEX", "81,330.56", "+0.74%")
col3.metric("BANK NIFTY", "51,274.30", "+1.05%")
col4.metric("INDIA VIX", "12.45", "-2.33%")

st.markdown("<br>", unsafe_allow_html=True)

# 5. TODAY'S BUY SIGNALS (Line by Line Full Width)
st.subheader("🟢 Today's Action: 'BUY' Signals")

try:
    # Fetch REAL data from Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["google_credentials"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Stock AI Dashboard").sheet1
    data = sheet.get_all_records()
    
    if data:
        df_news = pd.DataFrame(data)
        # Filter strictly for BUY signals
        buy_stocks = df_news[df_news['Recommendation'] == 'Buy']
        
        if not buy_stocks.empty:
            # Display line by line using a full width table
            st.dataframe(buy_stocks[['Date', 'Stock Symbol', 'News Headline']], hide_index=True, use_container_width=True)
        else:
            st.info("No 'BUY' signals generated yet for today.")
    else:
        st.warning("Data not found. Please run stock_news.py")
except Exception as e:
    st.error("Waiting for data connection... Check API keys.")

st.markdown("---")

# 6. Main Chart & Market Breadth Grid (Bottom Section)
st.subheader("📉 Market Trend & Breadth")
chart_col, breadth_col = st.columns([2, 1])

with chart_col:
    # Generate Dummy Trend Data for UI
    dates = pd.date_range(start="2026-08-12 09:15", end="2026-08-12 15:30", freq="5min")
    prices = 24600 + np.cumsum(np.random.randn(len(dates)) * 10)
    df_trend = pd.DataFrame({"Time": dates, "Price": prices})
    
    # Plotly Line Chart
    fig = px.area(df_trend, x="Time", y="Price", color_discrete_sequence=["#636EFA"])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with breadth_col:
    # Plotly Donut Chart
    labels = ['Advances', 'Declines', 'Unchanged']
    values = [1782, 980, 0]
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, marker_colors=['#00CC96', '#EF553B', '#FFA15A'])])
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, showlegend=True)
    fig2.add_annotation(text="<b>2,762</b><br>Total Stocks", x=0.5, y=0.5, font_size=20, showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)
