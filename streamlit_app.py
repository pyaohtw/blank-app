import streamlit as st
import yfinance as yf
import logging
from datetime import datetime

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This will send logs to the Streamlit interface
    ]
)

# Optional: Write logs to a file
logger = logging.getLogger()
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

st.title("Simple Stock Price Fetcher")

symbol = st.text_input("Enter a stock symbol:", "AAPL")
start_date = st.date_input("Start date:", datetime(2022, 1, 1))
end_date = st.date_input("End date:", datetime(2022, 12, 31))

if st.button("Get Stock Data"):
    try:
        logger.info(f"Fetching data for {symbol} from {start_date} to {end_date}")
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        st.write(stock_data)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        st.error(f"Error fetching data: {e}")
