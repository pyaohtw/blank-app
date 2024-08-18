import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("Investment Backtesting App")

# User inputs
years_to_invest = st.slider("Select the number of years to backtest", 1, 10, 2)
initial_investment = st.number_input("Initial Investment Amount", value=1000)
bi_weekly_investment = st.number_input("Bi-Weekly Investment Amount", value=50)
stock_symbol = st.text_input("Stock Symbol", value='VOO')

# Calculate the start and end dates
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(weeks=years_to_invest * 52)

# Get historical data
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Resample to bi-weekly frequency
stock_bi_weekly = stock_data['Close'].resample('2W').last().dropna()

# Calculate investments
stock_purchases = bi_weekly_investment / stock_bi_weekly
initial_purchase = initial_investment / stock_bi_weekly.iloc[0]
stock_purchases.iloc[0] += initial_purchase

# Calculate total cost and value
total_cost = initial_investment + bi_weekly_investment * (len(stock_purchases) - 1)
total_stock = stock_purchases.sum()
current_stock_price = stock_data['Close'].iloc[-1]
total_value = total_stock * current_stock_price
total_return = total_value - total_cost
total_return_rate = (total_return / total_cost) * 100

# Display results
st.write(f"### Results for {stock_symbol}")
st.write(f"Investment Period: {years_to_invest} years")
st.write(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
st.write(f"End Date: {end_date.strftime('%Y-%m-%d')}")
st.write(f"Total Cost: ${total_cost:.2f}")
st.write(f"Total {stock_symbol} Purchased: {total_stock:.6f} {stock_symbol}")
st.write(f"Total Value: ${total_value:.2f}")
st.write(f"Total Return: ${total_return:.2f}")
st.write(f"Total Return Rate: {total_return_rate:.2f}%")

# Visualization
st.write("### Growth of Asset Over Time")
accumulated_value = stock_purchases.cumsum() * stock_bi_weekly
plt.figure(figsize=(10, 6))
plt.plot(accumulated_value.index, accumulated_value.values, label='Portfolio Value')
plt.xlabel('Time')
plt.ylabel('Value ($)')
plt.title(f'Growth of Investment in {stock_symbol}')
plt.legend()
st.pyplot(plt)
