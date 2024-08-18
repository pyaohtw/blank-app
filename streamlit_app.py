import yfinance as yf
import streamlit as st
import time
import datetime  # Add this import

def download_with_retries(symbol, start_date, end_date, max_retries=5, base_delay=2):
    for attempt in range(max_retries):
        try:
            st.write(f"Attempting to download data for {symbol} (Attempt {attempt + 1})...")
            stock_data = yf.download(symbol, start=start_date, end=end_date, timeout=60)  # Increase timeout
            return stock_data
        except Exception as e:
            st.error(f"Error downloading {symbol}: {e}")
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * 2 ** attempt
            st.write(f"Retrying in {delay} seconds...")
            time.sleep(delay)

# Simplified for one stock symbol
st.title("Debugging Multi-Stock Investment Backtesting")

symbol = st.text_input("Enter Stock Symbol", "AAPL")
years_to_invest = 2

if st.button("Start Backtest"):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(weeks=years_to_invest * 52)

    try:
        stock_data = download_with_retries(symbol, start_date, end_date)
        st.write(f"Data fetched for {symbol}:")
        st.write(stock_data.head())
    except Exception as e:
        st.error(f"Failed after multiple attempts: {e}")
