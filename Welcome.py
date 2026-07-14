import streamlit as st

st.set_page_config(page_title="Personal Finance Calculators", layout="wide")

st.title("Personal Finance calculators")

st.write(
    "Use this page to learn what each app page does and quickly jump to the desired tool. "
    "Use the sidebar to navigate between the different tools. "
)

st.markdown(
    "- **Compounding** — compound growth visualiser, which compares the future values of an investment over time for three different annual return rates. \n"
    "- **Inflatiecalculator** — calculates the impact of  inflation in Belgium based on the Belgian Consumption Price Index (CPI) data. For more info see <https://jopxfin.blogspot.com/2025/04/inflatie-in-belgie.html> (Dutch post) \n "
    "- **Compounding with periodic contributions** — similar to the compound growth visualiser, but allows for periodic contributions (monthly, quarterly, yearly) and different contribution timings (beginning or end of period). \n"
)
