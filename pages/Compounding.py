import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Compound Growth Visualizer")

st.write(
    "Explore how different annual return rates compound over time. "
    "Enter an investment horizon and three possible net returns."
)

# --- User Inputs ---
initial_investment = st.number_input(
    "Initial investment (€)", min_value=0.0, value=1000.0, step=100.0
)

years = st.number_input(
    "Investment horizon (years)", min_value=1, max_value=100, value=40
)
colors = ["red", "blue", "green"]
labels = ["Return 1", "Return 2", "Return 3"]

col1, col2, col3 = st.columns(3)
r1 = col1.number_input("Return 1 (%)", value=4.0,step=1.0)
r2 = col2.number_input("Return 2 (%)", value=6.0, step=1.0)
r3 = col3.number_input("Return 3 (%)", value=8.0, step=1.0)

rates = [r1, r2, r3]

# --- Compute compound growth ---
years = np.arange(0, years + 1)

# Compute compound growth for each rate
values = [(initial_investment * (1 + r / 100) ** years) for r in rates]


# --- Plot ---
# Prepare column names for the chart
plt.figure(figsize=(10, 6))

for val, label, color in zip(values, labels, colors):
    plt.plot(years, val, label=label, color=color)

plt.title(f"Compound Growth of €{initial_investment:,.0f} Over {years[-1]} Years")
plt.xlabel("Years")
plt.ylabel("Portfolio Value (€)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Add labels at the end of each line with the final value
for val, color in zip(values, colors):
    plt.text(years[-1], val[-1], f'{val[-1]:,.0f}€', color=color, ha='right', va='center', fontsize=10)

st.pyplot(plt)

# --- Final values ---
st.subheader("Final Portfolio Values")
for rate, val in zip(rates, values):
    final_value = val[-1]
    st.write(f"**{rate:.1f}% return:** €{final_value:,.2f}")
