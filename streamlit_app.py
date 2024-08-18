import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("Multi-Stock Investment Backtesting App")

# User inputs
years_to_invest = st.slider("Select the number of years to backtest", 1, 30, 2)
initial_investment = st.number_input("Initial Investment Amount", value=1000)

# Frequency selection for investments
investment_frequency = st.selectbox("Select Investment Frequency", ["Daily", "Weekly", "Bi-Weekly", "Monthly"], index=2)
investment_amount = st.number_input(f"{investment_frequency} Investment Amount", value=50)

# Stock symbol inputs
st.write("### Enter up to 5 stock symbols and their respective allocation percentages:")
stock_symbols = []
allocation_percentages = []

for i in range(1, 6):
    col1, col2 = st.columns([2, 1])
    symbol = col1.text_input(f"Stock Symbol {i}", value="")
    percentage = col2.number_input(f"Allocation % {i}", min_value=0, max_value=100, value=0)

    if symbol and percentage > 0:
        stock_symbols.append(symbol)
        allocation_percentages.append(percentage)

# Ensure the total allocation is 100%
if sum(allocation_percentages) != 100:
    st.error("The total allocation percentage must equal 100%.")
else:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(weeks=years_to_invest * 52)

    total_portfolio_value = pd.Series(dtype=float)

    # Determine resampling frequency based on user selection
    resample_map = {
        "Daily": 'D',
        "Weekly": 'W',
        "Bi-Weekly": '2W',
        "Monthly": 'M'
    }
    resample_frequency = resample_map[investment_frequency]

    # Process each stock
    for symbol, percentage in zip(stock_symbols, allocation_percentages):
        try:
            stock_data = yf.download(symbol, start=start_date, end=end_date, timeout=10)  # Increase timeout to 10 seconds
            if stock_data.empty:
                st.warning(f"No data found for {symbol}. Skipping this stock.")
                continue
            
            stock_resampled = stock_data['Close'].resample(resample_frequency).last().dropna()
            stock_purchases = (percentage / 100 * investment_amount) / stock_resampled

            initial_purchase = (percentage / 100 * initial_investment) / stock_resampled.iloc[0]
            stock_purchases.iloc[0] += initial_purchase

            accumulated_value = stock_purchases.cumsum() * stock_resampled
            total_portfolio_value = total_portfolio_value.add(accumulated_value, fill_value=0)
        except Exception as e:
            st.error(f"Failed to download data for {symbol}: {e}")

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
        st.pyplot(plt)
    else:
        st.warning("No valid data available to display the portfolio growth.")
