id: 68376488a58eb24bd12e63fc_documentation
summary: Yield-Based Bond Duration Measures and Properties Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# FRN Duration Visualizer Codelab

This codelab provides a comprehensive guide to understanding and utilizing the FRN (Floating Rate Note) Duration Visualizer application built using Streamlit. This application is designed to help developers and finance professionals understand the concept of Macaulay Duration and how it is affected by various FRN parameters.

## Importance of the Application

Understanding the duration of financial instruments is crucial for risk management and investment strategies. This application provides an interactive way to visualize the impact of different FRN parameters on its Macaulay Duration, offering insights into its price sensitivity to interest rate changes.

## Concepts Explained

This codelab and the associated application will help you grasp the following key concepts:

*   **Floating Rate Notes (FRNs):** Understand what FRNs are and how their coupon rates are tied to reference rates.
*   **Macaulay Duration:** Learn about the definition, calculation, and importance of Macaulay Duration as a measure of a bond's price sensitivity to interest rate changes.
*   **Impact of FRN Parameters:** Explore how changes in notional amount, coupon rate, reference rate spread, reset period, maturity date, and start date affect the Macaulay Duration of an FRN.

## Application Architecture

The application follows a simple two-file structure:

1.  `app.py`: This is the main Streamlit application file. It handles the overall layout, title, introduction, and navigation. It also imports and runs the FRN duration calculation page.

2.  `application_pages/frn_duration.py`: This file contains the core logic for the FRN duration calculator, including the `calculate_macaulay_duration` function and the Streamlit components for user interaction.

## Setting up the Environment

Duration: 00:05

To run this application, you'll need Python 3.6 or later and the following libraries:

*   Streamlit
*   Pandas
*   Numpy
*   Plotly

You can install them using pip:

```bash
pip install streamlit pandas numpy plotly
```

## Running the Application

Duration: 00:02

Navigate to the directory containing `app.py` and run the following command:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## Exploring `app.py`

Duration: 00:10

Let's examine the code in `app.py`:

```python
import streamlit as st

st.set_page_config(page_title="FRN Duration Visualizer", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("FRN Duration Visualizer")
st.divider()

st.markdown("""
In this lab, we will explore the concept of Macaulay Duration for Floating Rate Notes (FRNs).
This application allows you to interactively change FRN parameters such as notional amount, coupon rate, reference rate spread, reset period, maturity date, and start date, and observe the impact on Macaulay Duration.

**Macaulay Duration** is a measure of the weighted-average time until an investor receives the bond's cash flows. It's expressed in years and is a crucial indicator of a bond's price sensitivity to changes in interest rates.

**Formula:**

Where:

*   `t` = Time until cash flow
*   `PV(CFt)` = Present value of the cash flow at time `t`
*   `Σ` = Summation
""")

page = st.sidebar.selectbox(label="Navigation", options=["FRN Duration Calculator"])

if page == "FRN Duration Calculator":
    from application_pages.frn_duration import run_frn_duration
    run_frn_duration()

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
```

This code performs the following actions:

*   **Imports Streamlit:**  `import streamlit as st` imports the Streamlit library, aliased as `st`.
*   **Sets Page Configuration:** `st.set_page_config` sets the title and layout of the Streamlit application. The `layout="wide"` argument makes the app use the full width of the browser.
*   **Adds Sidebar Content:** `st.sidebar.image`, `st.sidebar.divider` add an image and a divider to the sidebar.
*   **Sets Title and Introduction:** `st.title` sets the main title of the application, and `st.markdown` displays an introductory text explaining the purpose of the application and the concept of Macaulay Duration.
*   **Creates Navigation:** `st.sidebar.selectbox` creates a dropdown menu in the sidebar, allowing users to select different pages. In this case, there's only one page: "FRN Duration Calculator".
*   **Conditional Page Loading:** The `if page == "FRN Duration Calculator":` block checks which page is selected and then imports and runs the corresponding code. In this case, it imports the `run_frn_duration` function from `application_pages/frn_duration.py` and executes it.
*   **Adds Footer:** `st.divider`, `st.write`, and `st.caption` add a divider and copyright information to the bottom of the page.

## Exploring `application_pages/frn_duration.py`

Duration: 00:20

Now let's dive into `application_pages/frn_duration.py`:

```python
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
```

Here's a breakdown of the code:

*   **Imports:** It imports necessary libraries like `streamlit`, `pandas`, `numpy`, `datetime`, and `plotly.express`.
*   **`calculate_macaulay_duration` function:**
    *   This function takes FRN parameters as input and calculates the Macaulay Duration.
    *   It determines the number of payments per year based on the `reset_period`.
    *   It calculates the time to maturity in years.
    *   It calculates the periodic coupon rate.
    *   It calculates the number of periods.
    *   It generates cash flows for each period, adding the notional amount to the last cash flow.
    *   It calculates the present value of each cash flow and multiplies it by the time until the cash flow.
    *   Finally, it calculates the Macaulay Duration using the formula: `sum(weighted_times) / sum(present_values)`.
    *   Error handling is included to return 0.0 in case of any exception.
*   **`run_frn_duration` function:**
    *   This function contains the Streamlit code to create the FRN Duration Calculator interface.
    *   It uses `st.header` to display the title of the calculator.
    *   It uses `st.number_input`, `st.slider`, and `st.selectbox` to create interactive input widgets for the FRN parameters.
    *   It calls the `calculate_macaulay_duration` function with the user-provided inputs.
    *   It displays the calculated Macaulay Duration using `st.metric`.
    *   It creates a Pandas DataFrame to store the Macaulay Duration for different reset periods.
    *   It uses `plotly.express` to create a bar chart visualizing the relationship between reset period and Macaulay Duration.
    *   It displays the chart using `st.plotly_chart`.

## Interacting with the Application

Duration: 00:15

1.  **Notional Amount:** Change the notional amount using the `st.number_input` widget. Observe how it affects the Macaulay Duration.  Increasing the notional amount does not affect the Macaulay Duration directly because it scales all cash flows proportionally.

2.  **Coupon Rate:** Use the `st.slider` to adjust the coupon rate. Notice the inverse relationship between the coupon rate and the Macaulay Duration. Higher coupon rates lead to lower durations because a larger portion of the bond's value is received earlier in the form of coupon payments.

3.  **Reference Rate Spread:** Modify the reference rate spread using the `st.slider`. Similar to the coupon rate, a higher spread reduces the Macaulay Duration.

4.  **Reset Period:** Select different reset periods from the `st.selectbox`.  The shorter the reset period, the closer the FRN's duration is to its time to the next reset, often close to zero.

5.  **Maturity Date:** Experiment with different maturity dates using the `st.date_input`. Longer maturity dates generally increase the Macaulay Duration.

6.  **Start Date:** Modify the start date using the `st.date_input`.  Changing the start date, while keeping the maturity date constant, alters the time to maturity, which impacts the duration.

Observe how the "Macaulay Duration (Years)" metric and the bar chart change in real-time as you adjust the parameters. The bar chart helps visualize the impact of different reset periods on the Macaulay Duration.

## Understanding the Calculation

Duration: 00:10

The `calculate_macaulay_duration` function implements the standard formula for calculating Macaulay Duration. It calculates the present value of each cash flow and weights it by the time until the cash flow is received. The sum of these weighted present values, divided by the sum of all present values, gives the Macaulay Duration.

<aside class="positive">
  Understanding the formula and its implementation is key to interpreting the results of the application. Consider experimenting with different FRN parameters and observing their impact on the calculated duration.
</aside>

## Further Exploration

Duration: 00:08

Here are some suggestions for further exploration:

*   **Add More Sophisticated Discounting:**  Incorporate a more complex yield curve for discounting cash flows instead of using just the coupon rate.
*   **Implement Modified Duration:**  Extend the application to calculate modified duration, which is another important measure of interest rate risk.
*   **Add More Visualizations:**  Create additional charts and graphs to visualize the relationship between FRN parameters and duration. For example, you could create a scatter plot showing the relationship between coupon rate and duration.
*   **Sensitivity Analysis:**  Implement a sensitivity analysis feature to show how the duration changes with small changes in each parameter.

<aside class="negative">
Remember that this application is for educational purposes. The calculations are simplified and may not be accurate for all real-world scenarios.
</aside>

## Conclusion

This codelab has provided a comprehensive guide to understanding and using the FRN Duration Visualizer application. By exploring the code and interacting with the application, you should have gained a better understanding of Macaulay Duration and how it is affected by various FRN parameters. This knowledge is essential for anyone working with fixed-income securities and managing interest rate risk.
