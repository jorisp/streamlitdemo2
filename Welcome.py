import streamlit as st

st.set_page_config(page_title="Personal Finance Calculators", layout="wide")

st.title("Personal Finance calculators")

st.write(
    "Use this page to learn what each app page does and quickly jump to the desired tool. "
    "If the links do not jump directly, use the sidebar to select the page."
)

st.markdown(
    "- **Compound Growth Visualizer** — compare the future values of an investment over time for three different annual return rates. \n"
    "- **Inflatiecalculator** — calculate inflation-adjusted values using Belgian CPI data. "
)
