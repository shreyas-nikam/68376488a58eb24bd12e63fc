
# Technical Specifications for a Streamlit Application: Floating Rate Note (FRN) Duration Visualizer

## Overview

This Streamlit application aims to visualize and explain the concept of Macaulay Duration for Floating Rate Notes (FRNs). It allows users to interactively change FRN parameters (reset periods) and observe the impact on Macaulay Duration through calculated values and interactive charts. The application directly relates to the concept of Macaulay Duration as described in the provided document (Specifically, the subsection on Duration of Floating-Rate Notes and Loans) by demonstrating how reset frequency influences duration.

## Step-by-Step Generation Process

1.  **Set up the Streamlit environment:**
    *   Install necessary libraries: `streamlit`, `pandas`, `numpy`
    *   Create a new Python file (e.g., `frn_duration.py`).

2.  **Import Libraries:**
    ```python
    import streamlit as st
    import pandas as pd
    import numpy as np
    import datetime
    from typing import Callable, Optional
    ```

3.  **Define Calculation Functions:**
    *   Create a function to calculate the cash flows of an FRN. This will depend on the notional, coupon rate (tied to a reference rate, e.g., LIBOR, plus a spread), and the reset period.
    *   Create a function to calculate the present value (PV) of each cash flow.
    *   Create a function to calculate the Macaulay Duration based on cash flows and their present values.

4.  **Implement the Streamlit User Interface:**
    *   **Title and Description:** Add a title and brief explanation of the app.
    ```python
    st.title("Floating Rate Note (FRN) Duration Visualizer")
    st.write("Explore how the reset period affects the Macaulay Duration of an FRN.")
    ```
    *   **Input Widgets:**  Use `st.number_input`, `st.slider`, `st.date_input` and similar Streamlit features to allow the user to define the FRN's parameters.
    ```python
    notional = st.number_input("Notional Amount", value=1000.0)
    coupon_rate = st.slider("Coupon Rate (%)", min_value=0.0, max_value=10.0, value=5.0) / 100  # Divide by 100 to represent as decimal
    reference_rate_spread = st.slider("Reference Rate Spread (%)", min_value=0.0, max_value=2.0, value=1.0) / 100 # Divide by 100 to represent as decimal
    reset_period = st.selectbox("Reset Period", options=["Monthly", "Quarterly", "Semi-Annually", "Annually"], index=1)
    maturity_date = st.date_input("Maturity Date", value=datetime.date(2030, 12, 31))
    start_date = st.date_input("Start Date", value=datetime.date(2024,1,1))
    ```

5.  **Calculate Macaulay Duration:**
    *   Based on the user inputs, calculate the cash flows, present values, and Macaulay Duration.
    ```python
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

    macaulay_duration = calculate_macaulay_duration(notional, coupon_rate, reference_rate_spread, reset_period, maturity_date, start_date)
    ```

6.  **Display Results:**
    *   Use `st.write` or `st.metric` to display the calculated Macaulay Duration.
    ```python
    st.metric("Macaulay Duration (Years)", value=macaulay_duration)

    ```
    *   Optionally, create a simple DataFrame and chart to visualize how the Macaulay Duration changes over a range of reset periods.  This will require iterating through different values within the function and storing the values.

7.  **Add Explanatory Text:**
    *   Include markdown text using `st.markdown` to explain the concept of Macaulay Duration, how it's calculated, and how the reset period affects it.

## Important Definitions, Examples, and Formulae

### Macaulay Duration

Macaulay Duration is a measure of the weighted-average time until an investor receives the bond's cash flows. It's expressed in years and is a crucial indicator of a bond's price sensitivity to changes in interest rates.

**Formula:**

```
Macaulay Duration =  (Σ (t * PV(CFt))) / (Σ PV(CFt))
```

Where:

*   `t` = Time until cash flow
*   `PV(CFt)` = Present value of the cash flow at time `t`
*   `Σ` = Summation

**Example:**

Consider a bond with two cash flows:

*   Year 1: \$105 (face value + coupon)
*   Yield to Maturity (YTM): 5%

The present values of the cash flows are:

*   PV(Year 1): \$105 / (1 + 0.05)^1 = \$100

Macaulay Duration = (1 * \$100) / \$100 = 1 year

### Cash Flow (CF)

A cash flow represents the payments an investor receives from a bond.  For an FRN, this includes the coupon payments (which reset based on the reference rate) and the return of principal (notional) at maturity.

**Formula (Periodic Coupon Payment):**

```
Periodic Coupon Payment = Notional * (Coupon Rate + Reference Rate Spread) / Payments Per Year
```

Where:

*   *Notional* =  The face value of the bond.
*   *Coupon Rate* = The stated coupon rate of the FRN (linked to a reference rate).
*   *Reference Rate Spread* = The additional spread above the reference rate.
*   *Payments Per Year* = The frequency of coupon payments (e.g., 12 for monthly, 4 for quarterly).

### Present Value (PV)

The present value is the current worth of a future sum of money or stream of cash flows, given a specified rate of return.

**Formula:**

```
PV = CF / (1 + r)^t
```

Where:

*   `PV` = Present Value
*   `CF` = Cash Flow
*   `r` = Discount Rate (typically the Yield-to-Maturity, but for simplicity, can use the coupon rate)
*   `t` = Time until the cash flow is received

## Libraries and Tools

*   **Streamlit:** The core library for building the interactive web application. It provides widgets (number inputs, sliders, selectboxes, date inputs) for user interaction and functions for displaying results (text, metrics, charts).
*   **Pandas:** Primarily used for creating and manipulating data for visualization, especially when generating charts that show the effect of varying reset periods.
*   **Numpy:** Used for numerical calculations, particularly when dealing with arrays of cash flows or present values.
*   **datetime**: Used to handle date inputs from the user related to maturity and start dates, which influence the duration calculation.
