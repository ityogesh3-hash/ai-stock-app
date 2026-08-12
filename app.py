import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 1. Pro UI Design Settings
st.set_page_config(page_title="Pro Stock AI", page_icon="📈", layout="wide")

# Sidebar - Filter Menu
st.sidebar.title("⚙️ AI Settings")
st.sidebar.markdown("Filter your stock signals here:")

# 2. Google Sheets Setup 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["google_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Stock AI Dashboard").sheet1
data = sheet.get_all_records()

# Main Title
st.title("📈 Pro AI Stock Screener")
st.markdown("---")

# 3. Dashboard UI Elements
if data:
    df = pd.DataFrame(data)
    
    # Sidebar Stock Filter Logic
    stock_list = ["All Stocks"] + list(df['Stock Symbol'].unique())
    selected_stock = st.sidebar.selectbox("🔍 Select a Stock to Analyze:", stock_list)
    
    if selected_stock != "All Stocks":
        # Filter data only for selected stock
        df = df[df['Stock Symbol'] == selected_stock]
        st.subheader(f"📊 Dashboard for {selected_stock}")
    else:
        st.subheader("🌐 Overall Market Overview")
    
    # Calculate totals based on filter
    buy_count = len(df[df['Recommendation'] == 'Buy'])
    sell_count = len(df[df['Recommendation'] == 'Sell'])
    hold_count = len(df[df['Recommendation'] == 'Hold'])
    
    # Show Top Metric Boxes in 4 Columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📰 Total News", len(df))
    col2.metric("🟢 BUY Signals", buy_count)
    col3.metric("🔴 SELL Signals", sell_count)
    col4.metric("🟡 HOLD Signals", hold_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Pro Tabs Layout
    tab1, tab2 = st.tabs(["📰 AI News Signals", "📈 Live Charts & Fundamentals (Next Step)"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    with tab2:
        st.info("Ippo varai namma app-la AI News mattum thaan irukku. Adutha step-la inga Unmaiyana Live Share Price, P/E Ratio, mariyum Charts varum!")
    
else:
    st.warning("Waiting for data... Please run stock_news.py first!")
