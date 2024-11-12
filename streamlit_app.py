import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("Single Stock Investment Backtesting with Expense Deduction")

# User inputs
years_to_invest = st.slider("Select the number of years to backtest", 1, 30, 2)
initial_investment = st.number_input("Initial Investment Amount", value=1000)
investment_frequency = st.selectbox("Select Investment Frequency", ["Daily", "Weekly", "Bi-Weekly", "Monthly"], index=2)
investment_amount = st.number_input(f"{investment_frequency} Investment Amount", value=50)
annual_expense_ratio = st.number_input("Annual ETF Expense Ratio (%)", min_value=0.0, max_value=10.0, value=0.5)

# Stock symbol input
stock_symbol = st.text_input("Stock Symbol", value="AAPL")

# Ensure valid stock symbol
if stock_symbol:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(weeks=years_to_invest * 52)

    # Download stock data
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    if not stock_data.empty:
        # Resampling frequency mapping
        resample_map = {"Daily": 'D', "Weekly": 'W', "Bi-Weekly": '2W', "Monthly": 'M'}
        resample_frequency = resample_map[investment_frequency]

        # Resample and process stock data
        stock_resampled = stock_data['Close'].resample(resample_frequency).last().dropna()
        stock_purchases = investment_amount / stock_resampled
        initial_purchase = initial_investment / stock_resampled.iloc[0]
        stock_purchases.iloc[0] += initial_purchase
        accumulated_value = stock_purchases.cumsum() * stock_resampled

        # Deduct annual expense from accumulated value at each year mark
        for i in range(1, years_to_invest + 1):
            year_end_index = i * 12  # Adjust for monthly data; modify if frequency is different
            if year_end_index < len(accumulated_value):
                expense_factor = (1 - annual_expense_ratio / 100) ** i  # Compound effect for each year
                accumulated_value.iloc[year_end_index:] *= expense_factor  # Apply expense deduction

        # Extract the final scalar value of the accumulated portfolio
        final_value = accumulated_value.iloc[-1]

        # Ensure that final_value is a scalar and format it
        final_value = final_value.item()  # This ensures it's a scalar (not a Series)


        # Calculate total invested and return
        total_invested = initial_investment + investment_amount * (len(stock_purchases) - 1)
        total_return = final_value - total_invested
        total_return_rate = (total_return / total_invested) * 100

        # Display results
        st.write(f"Final Value: ${final_value:.2f}")
        st.write(f"Total Return: ${total_return:.2f}")
        st.write(f"Total Return Rate: {total_return_rate:.2f}%")

        # Plot portfolio growth over time
        st.write("### Growth of Investment Portfolio Over Time")
        plt.figure(figsize=(10, 6))
        plt.plot(accumulated_value.index, accumulated_value.values, label='Portfolio Value')
        plt.xlabel('Time')
        plt.ylabel('Value ($)')
        plt.title('Growth of Investment Portfolio with Annual Expense Deduction')
        plt.legend()
        st.pyplot(plt)
    else:
        st.warning("No data found for the stock symbol provided.")
