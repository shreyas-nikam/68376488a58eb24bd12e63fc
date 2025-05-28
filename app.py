
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
