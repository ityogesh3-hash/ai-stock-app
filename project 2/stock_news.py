import gspread
from oauth2client.service_account import ServiceAccountCredentials
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. Google Sheets Setup
# Enna ellam access thevai nu solrom
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# JSON file vazhiyaaga login pandrom
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Namma sheet-a open pandrom
sheet = client.open("Stock AI Dashboard").sheet1

# 2. AI & Fetch Setup
analyzer = SentimentIntensityAnalyzer()
rss_url = "https://news.google.com/rss/search?q=wipro+stock"
feed = feedparser.parse(rss_url)

print("Fetching news, analyzing AI sentiment, and saving to Google Sheet...")

for entry in feed.entries[:3]:
    news_title = entry.title
    published_date = entry.published
    
    # AI Sentiment Logic
    scores = analyzer.polarity_scores(news_title)
    compound = scores['compound']
    
    if compound >= 0.05:
        recommendation = "Buy"
    elif compound <= -0.05:
        recommendation = "Sell"
    else:
        recommendation = "Hold"
    
    # 3. Append to Google Sheet (Date, Symbol, Headline, Recommendation)
    row_data = [published_date, "WIPRO", news_title, recommendation]
    sheet.append_row(row_data)
    
    print(f"Success: Added [{recommendation}] - {news_title[:30]}...")

print("Done! Check your Google Sheet Dashboard.")