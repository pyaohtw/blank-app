import yfinance as yf

# Ask the user to enter a stock symbol
symbol = input("Enter the stock symbol: ").upper()

# Fetch the latest stock data
try:
    stock = yf.Ticker(symbol)
    stock_info = stock.history(period="1d")  # Get the last day's data

    if not stock_info.empty:
        latest_price = stock_info['Close'].iloc[-1]  # Get the last closing price
        print(f"The latest closing price for {symbol} is: ${latest_price:.2f}")
    else:
        print(f"No data available for symbol: {symbol}")

except Exception as e:
    print(f"Error fetching data for {symbol}: {e}")
