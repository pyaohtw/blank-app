import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# Hardcoded values
years_to_invest = 10  # Number of years to backtest
initial_investment = 1000  # Initial Investment Amount
investment_frequency = "Monthly"  # Investment frequency (options: "Daily", "Weekly", "Bi-Weekly", "Monthly")
investment_amount = 50  # Monthly Investment Amount

# Frequency options
frequency_options = {"Daily": "D", "Weekly": "W", "Bi-Weekly": "2W", "Monthly": "ME"}

# Stock symbols and their allocation percentages
stock_symbols = ["AAPL", "MSFT", "GOOGL"]  # Example stock symbols
allocation_percentages = [40, 30, 30]  # Example allocation percentages corresponding to the stock symbols

# Ensure the total allocation is 100%
if sum(allocation_percentages) != 100:
    st.error("The total allocation percentage must equal 100%.")

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(weeks=years_to_invest * 52)

total_portfolio_value = pd.Series(dtype=float)

for symbol, percentage in zip(stock_symbols, allocation_percentages):
    try:
        # Download stock data
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            st.warning(f"No data returned for {symbol}.")
            continue

        # Resample and process data
        stock_resampled = stock_data['Close'].resample(frequency_options[investment_frequency]).last().dropna()
        stock_purchases = (percentage / 100 * investment_amount) / stock_resampled
        
        initial_purchase = (percentage / 100 * initial_investment) / stock_resampled.iloc[0]
        stock_purchases.iloc[0] += initial_purchase
        
        total_cost = percentage / 100 * (initial_investment + investment_amount * (len(stock_purchases) - 1))
        accumulated_value = stock_purchases.cumsum() * stock_resampled
        total_portfolio_value = total_portfolio_value.add(accumulated_value, fill_value=0)

    except Exception as e:
        st.error(f"Error processing data for {symbol}: {e}")

# Display final portfolio value and returns
if not total_portfolio_value.empty:
    total_value = total_portfolio_value.iloc[-1]
    total_return = total_value - initial_investment - investment_amount * (len(stock_purchases) - 1)
    total_return_rate = (total_return / (initial_investment + investment_amount * (len(stock_purchases) - 1))) * 100

    st.write(f"Total Value: ${total_value:.2f}")
    st.write(f"Total Return: ${total_return:.2f}")
    st.write(f"Total Return Rate: {total_return_rate:.2f}%")

    # Plot the portfolio growth over time
    st.write("### Growth of Portfolio Over Time")
    plt.figure(figsize=(10, 6))
    plt.plot(total_portfolio_value.index, total_portfolio_value.values, label='Portfolio Value')
    plt.xlabel('Time')
    plt.ylabel('Value ($)')
    plt.title('Growth of Investment Portfolio')
    plt.legend()
    
    # Display the plot in Streamlit
    st.pyplot(plt)
else:
    st.warning("No portfolio data available to display.")
