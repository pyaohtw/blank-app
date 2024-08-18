import streamlit as st
import yfinance as yf
from datetime import datetime

st.title("Simple Stock Price Fetcher")

symbol = st.text_input("Enter a stock symbol:", "AAPL")
start_date = st.date_input("Start date:", datetime(2022, 1, 1))
end_date = st.date_input("End date:", datetime(2022, 12, 31))

if st.button("Get Stock Data"):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        st.write(stock_data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
