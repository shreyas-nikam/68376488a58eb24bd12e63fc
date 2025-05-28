id: 68376488a58eb24bd12e63fc_user_guide
summary: Yield-Based Bond Duration Measures and Properties User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# FRN Duration Visualizer: A Codelab

This codelab will guide you through using the FRN (Floating Rate Note) Duration Visualizer application. This tool is designed to help you understand the key concept of Macaulay Duration, a critical measure for assessing a bond's sensitivity to interest rate changes. By interactively adjusting the parameters of an FRN, such as the notional amount, coupon rate, and maturity date, you'll gain valuable insights into how these factors influence its duration. This understanding is crucial for anyone involved in fixed income investments and risk management.

## Understanding the Interface

Duration: 00:03

The application interface is designed to be intuitive and user-friendly. Let's break down the main components:

*   **Sidebar:** Located on the left, the sidebar contains the application logo and a navigation menu. Currently, it allows you to select the "FRN Duration Calculator" page.
*   **Main Panel:** This is where you'll find the interactive FRN Duration Calculator. It's divided into two main sections:
    *   **Input Parameters:** This section contains several input widgets (number input, sliders, date pickers, and selectbox) that allow you to define the characteristics of the FRN. These parameters include:
        *   Notional Amount: The face value of the FRN.
        *   Coupon Rate: The base interest rate of the FRN.
        *   Reference Rate Spread: The additional spread added to the coupon rate.
        *   Reset Period: How frequently the coupon rate is adjusted (Monthly, Quarterly, Semi-Annually, Annually).
        *   Maturity Date: The date when the FRN matures and the principal is repaid.
        *   Start Date: The date the FRN was issued.
    *   **Output & Visualization:** This section displays the calculated Macaulay Duration and a visualization of how the duration changes with different reset periods.

## Calculating the Macaulay Duration

Duration: 00:05

This is the core functionality of the application. Follow these steps to calculate and interpret the Macaulay Duration:

1.  **Input the FRN Parameters:** Use the input widgets in the "FRN Duration Calculator" section to define the characteristics of your FRN. For example, you can set the "Notional Amount" to $1000, the "Coupon Rate" to 5%, the "Reference Rate Spread" to 1%, the "Reset Period" to "Quarterly", "Maturity Date" to Dec 31, 2030 and "Start Date" to Jan 1, 2024.

2.  **Observe the Calculated Duration:** The calculated Macaulay Duration, in years, will be displayed as a metric right below the input parameters. This value represents the weighted-average time until you receive the FRN's cash flows.

3.  **Interpret the Results:** A higher Macaulay Duration indicates that the FRN's price is more sensitive to changes in interest rates. Conversely, a lower duration suggests lower sensitivity.

<aside class="positive">
Experiment with different FRN parameters to see how they impact the Macaulay Duration. Pay close attention to the effect of the maturity date and reset period.
</aside>

## Visualizing the Impact of Reset Period

Duration: 00:05

The application provides a bar chart to visualize how the Macaulay Duration changes with different reset periods.

1.  **Observe the Bar Chart:** The bar chart displays the Macaulay Duration for four different reset periods: Monthly, Quarterly, Semi-Annually, and Annually. The x-axis represents the reset period, and the y-axis represents the Macaulay Duration in years.

2.  **Analyze the Trend:** Examine the chart to see how the reset period affects the duration.  A shorter reset period generally leads to a lower duration because the coupon rate is adjusted more frequently to reflect changes in market interest rates.

<aside class="negative">
The application uses a simplified discount rate for the purpose of demonstration. In real-world scenarios, a more sophisticated yield curve should be used to discount the cash flows.
</aside>

## Exploring Different Scenarios

Duration: 00:07

The true power of this application lies in its ability to allow you to explore different scenarios. Try these experiments to deepen your understanding:

*   **Impact of Maturity Date:** Keep all other parameters constant and vary the "Maturity Date". Observe how extending the maturity date increases the Macaulay Duration, making the FRN more sensitive to interest rate changes.

*   **Impact of Coupon Rate:** Adjust the "Coupon Rate" and "Reference Rate Spread" while keeping other parameters constant. Notice how changes in the coupon rate can slightly affect the duration, as the present values of the cash flows are impacted.

*   **Impact of Reset Period:** Switch between different "Reset Periods" (Monthly, Quarterly, Semi-Annually, Annually). See how more frequent resets generally decrease the Macaulay Duration. This is because the FRN's coupon rate adjusts more quickly to market rates, reducing its price sensitivity.

By experimenting with these scenarios, you'll develop a more intuitive understanding of the factors that influence the Macaulay Duration of an FRN. This knowledge is essential for making informed investment decisions and managing interest rate risk.
