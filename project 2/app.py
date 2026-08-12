import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 1. App Webpage Design Settings
st.set_page_config(page_title="AI Stock App", page_icon="📈", layout="wide")
st.title("📈 AI Stock Market Dashboard")
st.write("Real-time Google News and AI Sentiment Analysis")

# 2. Google Sheets Setup (Using Streamlit Secrets)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["google_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 3. Read Data from Google Sheet
sheet = client.open("Stock AI Dashboard").sheet1
data = sheet.get_all_records()

# 4. Dashboard UI Elements
if data:
    df = pd.DataFrame(data)
    
    # Calculate totals
    buy_count = len(df[df['Recommendation'] == 'Buy'])
    sell_count = len(df[df['Recommendation'] == 'Sell'])
    hold_count = len(df[df['Recommendation'] == 'Hold'])
    
    # Show Top Metric Boxes
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 BUY Signals", buy_count)
    col2.metric("🔴 SELL Signals", sell_count)
    col3.metric("🟡 HOLD Signals", hold_count)
    
    st.divider()
    
    # Show the Table
    st.subheader("📰 Latest News & AI Signals")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
else:
    st.info("Waiting for data... Please run stock_news.py first!")
