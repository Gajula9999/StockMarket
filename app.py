import streamlit as st
import requests
import pandas as pd
import time

# Set up the page
st.set_page_config(page_title="Stock Price Viewer", layout="wide")
st.title("📈 Stock Price Viewer")

# API Key (Hardcoded for simplicity, but not recommended for security reasons)
API_KEY = "2ASFNWPVYYI4FQ7T"
BASE_URL = "https://www.alphavantage.co/query"

# Function to fetch stock data with caching
@st.cache_data
def get_stock_data(symbol, interval):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    key = f"Time Series ({interval})"
    
    if key in data:
        df = pd.DataFrame.from_dict(data[key], orient='index')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df
    else:
        return None

# Sidebar input
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
interval = st.sidebar.selectbox("Select Interval", ["1min", "5min", "15min", "30min", "60min"], index=1)

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching stock data..."):
        time.sleep(1)  # Simulate loading
        df = get_stock_data(symbol, interval)
        
        if df is not None:
            st.success("Data Loaded Successfully!")
            st.subheader(f"Stock Price Data for {symbol} ({interval} Interval)")
            st.line_chart(df["1. open"], use_container_width=True)
            st.dataframe(df)
        else:
            st.error("Error fetching data. Please check the stock symbol and API limit.")

