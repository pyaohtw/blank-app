import yfinance as yf
import streamlit as st

# Streamlit app title
st.title("Simple Stock Price Fetcher")

# Input field for the stock symbol
symbol = st.text_input("Enter the stock symbol:", value="AAPL").upper()

# Button to fetch the latest stock price
if st.button("Fetch Latest Price"):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")  # Get the last day's data

        if not stock_info.empty:
            latest_price = stock_info['Close'].iloc[-1]  # Get the last closing price
            st.success(f"The latest closing price for {symbol} is: ${latest_price:.2f}")
        else:
            st.warning(f"No data available for symbol: {symbol}")

    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")

# Additional info (optional)
st.write("Enter a valid stock symbol and click 'Fetch Latest Price' to see the latest closing price.")
