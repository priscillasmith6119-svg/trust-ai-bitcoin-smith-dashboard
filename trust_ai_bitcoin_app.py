# trust_ai_bitcoin_app.py

import streamlit as st
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime
from gtts import gTTS
import os

# ----------------------------
# Helper Functions
# ----------------------------
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    return requests.get(url).json()['bitcoin']['usd']

def get_btc_news():
    return [
        "Bitcoin adoption expands globally",
        "Institutions increase BTC holdings",
        "Crypto regulation developments reported",
        "Market correction after strong gains"
    ]

def analyze_sentiment(headlines):
    return sum(TextBlob(h).sentiment.polarity for h in headlines) / len(headlines)

def detect_trend(prices):
    if len(prices) < 2:
        return "stable"
    change = prices[-1] - prices[-2]
    return "rising ↑" if change > 0 else "falling ↓" if change < 0 else "stable →"

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp_btc.mp3"
    tts.save(filename)
    audio_bytes = open(filename, 'rb').read()
    os.remove(filename)
    return audio_bytes

# ----------------------------
# Streamlit UI Setup
# ----------------------------
st.title("🛡️ Trust AI Bitcoin Dashboard")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if "prices" not in st.session_state:
    st.session_state.prices = []

btc_price = get_btc_price()
st.session_state.prices.append(btc_price)
prices = st.session_state.prices

news_list = get_btc_news()
sentiment_score = analyze_sentiment(news_list)
latest_news = news_list[-1] if news_list else "No news available"

trend = detect_trend(prices)
sentiment_string = "Positive 🙂" if sentiment_score > 0 else "Neutral/Negative 😐"

summary_text = f"""
Bitcoin is currently ${btc_price:,.2f} and trending {trend}.
Market sentiment is {sentiment_string}.
Latest news: {latest_news}

Tip: Short-term price swings are normal. Focus on long-term trends.
"""

st.subheader("📊 Market Summary")
st.text(summary_text)

voice_toggle = st.checkbox("🔊 Enable Voice Agent")
if voice_toggle and st.button("👂 Talk to me"):
    audio_bytes = speak_text(summary_text)
    st.audio(audio_bytes, format="audio/mp3")

show_detailed = st.checkbox("📈 Show Detailed Metrics")
if show_detailed:
    st.write(f"24h Volatility: Moderate")
    st.write(f"Sentiment Score (raw): {sentiment_score:.2f}")
    st.write(f"Price history: {prices}")

st.subheader("📉 Price Trend Chart")
fig, ax = plt.subplots()
ax.plot(prices, marker="o", linestyle="-", color="orange")
ax.set_xlabel("Updates")
ax.set_ylabel("Price (USD)")
ax.set_title("Bitcoin Price Trend Over Time")
ax.grid(True)
st.pyplot(fig)

st.subheader("📰 Latest News")
for item in news_list:
    st.write(f"- {item}")

user_question = st.text_input("💬 Ask Trust AI a question about Bitcoin:")

if user_question:
    reply = "Bitcoin markets are driven by global factors and long-term trends."
    if "drop" in user_question.lower():
        reply = "Short-term corrections are normal; don’t panic."
    if "trend" in user_question.lower():
        reply = f"Based on recent prices, the trend is {trend}."
    st.write(f"🤖 Trust AI Answer: {reply}")
    if voice_toggle:
        audio2 = speak_text(reply)
        st.audio(audio2, format="audio/mp3")
