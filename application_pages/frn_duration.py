
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
from typing import Callable, Optional


def calculate_macaulay_duration(notional: float, coupon_rate: float, reference_rate_spread: float, reset_period: str, maturity_date: datetime.date, start_date: datetime.date) -> float:
    """
    Calculates the Macaulay Duration of a Floating Rate Note (FRN).

    Args:
        notional (float): The notional amount of the FRN.
        coupon_rate (float): The base coupon rate of the FRN (e.g., tied to a reference rate).
        reference_rate_spread (float): The spread added to the coupon rate.
        reset_period (str): The reset period of the FRN ("Monthly", "Quarterly", "Semi-Annually", "Annually").
        maturity_date (datetime.date): The maturity date of the FRN.
        start_date (datetime.date): The start date of the FRN.

    Returns:
        float: The Macaulay Duration of the FRN in years. Returns 0 if there is an error.
    """
    try:
        # Determine the number of payments per year based on the reset period
        if reset_period == "Monthly":
            payments_per_year = 12
        elif reset_period == "Quarterly":
            payments_per_year = 4
        elif reset_period == "Semi-Annually":
            payments_per_year = 2
        else:  # Annually
            payments_per_year = 1

        # Calculate the time to maturity in years
        time_to_maturity = (maturity_date - start_date).days / 365.25

        # Calculate the periodic coupon rate
        periodic_coupon_rate = (coupon_rate + reference_rate_spread) / payments_per_year

        # Calculate the number of periods
        number_of_periods = int(time_to_maturity * payments_per_year)

        # Discount rate -  using coupon rate as the discount rate for simplicity
        discount_rate = coupon_rate

        # Generate cash flows
        cash_flows = [notional * periodic_coupon_rate] * number_of_periods
        cash_flows[-1] += notional  # Add notional to the last cash flow

        # Calculate present values and weighted times
        present_values = []
        weighted_times = []
        for i, cf in enumerate(cash_flows):
            t = (i + 1) / payments_per_year  # Time of cash flow
            pv = cf / (1 + discount_rate/payments_per_year)**(i + 1)
            present_values.append(pv)
            weighted_times.append(t * pv)

        # Calculate Macaulay Duration
        macaulay_duration = sum(weighted_times) / sum(present_values)

        return macaulay_duration

    except Exception as e:
        print(f"Error calculating Macaulay Duration: {e}")
        return 0.0


def run_frn_duration():
    st.header("FRN Duration Calculator")

    notional = st.number_input("Notional Amount", value=1000.0)
    coupon_rate = st.slider("Coupon Rate (%)", min_value=0.0, max_value=10.0, value=5.0) / 100  # Divide by 100 to represent as decimal
    reference_rate_spread = st.slider("Reference Rate Spread (%)", min_value=0.0, max_value=2.0, value=1.0) / 100 # Divide by 100 to represent as decimal
    reset_period = st.selectbox("Reset Period", options=["Monthly", "Quarterly", "Semi-Annually", "Annually"], index=1)
    maturity_date = st.date_input("Maturity Date", value=datetime.date(2030, 12, 31))
    start_date = st.date_input("Start Date", value=datetime.date(2024,1,1))

    macaulay_duration = calculate_macaulay_duration(notional, coupon_rate, reference_rate_spread, reset_period, maturity_date, start_date)

    st.metric("Macaulay Duration (Years)", value=round(macaulay_duration, 3))

    # Create a DataFrame for visualization
    reset_periods = ["Monthly", "Quarterly", "Semi-Annually", "Annually"]
    durations = []
    for period in reset_periods:
        duration = calculate_macaulay_duration(notional, coupon_rate, reference_rate_spread, period, maturity_date, start_date)
        durations.append(duration)

    df = pd.DataFrame({"Reset Period": reset_periods, "Macaulay Duration": durations})

    # Create a bar chart using Plotly
    fig = px.bar(df, x="Reset Period", y="Macaulay Duration", title="Macaulay Duration vs. Reset Period")
    st.plotly_chart(fig, use_container_width=True)
