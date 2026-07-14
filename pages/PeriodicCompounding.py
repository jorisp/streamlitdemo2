import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------
st.title("Compound Growth Visualizer")
st.write(
    "Explore how different annual return rates compound over time — "
    "with optional periodic investments (monthly, quarterly, yearly)."
)

# ---------------------------------------------------------
# User Inputs
# ---------------------------------------------------------
st.subheader("Initial Setup")

initial_investment = st.number_input(
    "Initial investment (€)", min_value=0.0, value=1000.0, step=100.0
)

investment_horizon = st.number_input(
    "Investment horizon (years)", min_value=1, max_value=100, value=40
)

# Return inputs
colors = ["red", "blue", "green"]
labels = ["Return 1", "Return 2", "Return 3"]

col1, col2, col3 = st.columns(3)
r1 = col1.number_input("Return 1 (%)", value=4.0, step=0.5)
r2 = col2.number_input("Return 2 (%)", value=6.0, step=0.5)
r3 = col3.number_input("Return 3 (%)", value=8.0, step=0.5)
rates = [r1, r2, r3]

# ---------------------------------------------------------
# Periodic Contribution Inputs
# ---------------------------------------------------------
st.subheader("Periodic Contributions")

contribution = st.number_input(
    "Periodic contribution (€)", min_value=0.0, value=0.0, step=50.0
)

frequency = st.selectbox(
    "Contribution frequency", ["Monthly", "Quarterly", "Yearly"]
)

timing = st.selectbox(
    "Contribution timing", ["End of period", "Beginning of period"]
)

freq_map = {"Monthly": 12, "Quarterly": 4, "Yearly": 1}
periods_per_year = freq_map[frequency]
total_periods = investment_horizon * periods_per_year

# ---------------------------------------------------------
# Simulation Function
# ---------------------------------------------------------
def simulate_with_contributions(initial, annual_rate, contribution, periods, periods_per_year, timing):
    """Simulates compounding with periodic contributions."""
    periodic_rate = (1 + annual_rate) ** (1 / periods_per_year) - 1

    value = initial
    values = []

    for t in range(periods + 1):
        if timing == "Beginning of period" and t > 0:
            value += contribution

        value *= (1 + periodic_rate)

        if timing == "End of period" and t > 0:
            value += contribution

        values.append(value)

    return values

# ---------------------------------------------------------
# Compute values for each return scenario
# ---------------------------------------------------------
all_values = []
for r in rates:
    annual_rate = r / 100
    vals = simulate_with_contributions(
        initial_investment,
        annual_rate,
        contribution,
        total_periods,
        periods_per_year,
        timing
    )
    all_values.append(vals)

# ---------------------------------------------------------
# Plotting
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

years_axis = np.arange(0, total_periods + 1) / periods_per_year

for vals, label, color in zip(all_values, labels, colors):
    plt.plot(years_axis, vals, label=label, color=color)

plt.title(
    f"Compound Growth of €{initial_investment:,.0f} "
    f"Over {investment_horizon} Years"
)
plt.xlabel("Years")
plt.ylabel("Portfolio Value (€)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# Add final value labels
for vals, color in zip(all_values, colors):
    plt.text(
        years_axis[-1],
        vals[-1],
        f"€{vals[-1]:,.0f}",
        color=color,
        ha="right",
        va="center",
        fontsize=10
    )

st.pyplot(plt)
plt.close()  # Close the plot to free memory

# ---------------------------------------------------------
# Summary Metrics
# ---------------------------------------------------------
st.subheader("Final Portfolio Values")

total_contributions = contribution * total_periods

for rate, vals in zip(rates, all_values):
    final_value = vals[-1]
    growth = final_value - total_contributions - initial_investment

    st.write(
        f"**{rate:.1f}% return:** "
        f"Final value: €{final_value:,.2f} — "
        f"Growth: €{growth:,.2f}"
    )
