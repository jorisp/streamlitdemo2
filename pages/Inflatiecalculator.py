import pandas as pd
from pathlib import Path
import streamlit as st

st.header('Inflationcalculator with Belgian CPI data')

CPI_DATA_URL = 'https://raw.githubusercontent.com/jorisp/tradingnotebooks/master/data/static_inflationcalc_be_2025.csv'
#CPI_DATA_SOURCE = Path(__file__).parent/ 'data/static_inflationcalc_be_2025.csv'

st.markdown(
    """
    This tool uses a CSV file with Belgian Consumption Price Index (CPI) data downloaded from
    https://www.github.com/jorisp/tradingnotebooks/blob/master/data/static_inflationcalc_be_2025.csv
    
    For more info see <https://jopxfin.blogspot.com/2025/04/inflatie-in-belgie.html> (Dutch post)
    
    How the calculation works:
    - Amount end year: `Amount end year = amount start year * (HICP2 / HICP1)`
    - Percentage change: `((Amount2 - Amount1) / Amount1) * 100` with Amount1 = amount start year and Amount2 = amount end year
    """
)

# --- Data laden ---
@st.cache_data
def load_cpi_data():
    try:
        df = pd.read_csv(CPI_DATA_URL )
        return df
    except Exception as e:
        st.error(f"Could not load CPI data: {e}")
        st.stop()

    # Validation: Check if required columns are present
    if not {"year", "cpi"}.issubset(df.columns):
        st.error("CSV file needs to contain columns 'year' and 'cpi'.")
        st.stop()

df = load_cpi_data()
df = df.sort_values("year")

st.subheader("Loaded CPI-data")
st.write(df)

# --- Inputvelden ---
amount = st.number_input("Amount in start year", min_value=100, value=100,step=100)
start_year = st.selectbox("Start year", df["year"])
end_year = st.selectbox("End year", df["year"])

# --- Berekening ---
if st.button("Calculate inflation impact"):
    cpi1 = df.loc[df["year"] == start_year, "cpi"].values[0]
    cpi2 = df.loc[df["year"] == end_year, "cpi"].values[0]

    cost2 = amount * (cpi2 / cpi1)
    pct_change = ((cost2 - amount) / amount) * 100
    num_years = end_year - start_year

    if num_years > 0:
        avg_annual = ((cpi2 / cpi1) ** (1 / num_years) - 1) * 100
    else:
        avg_annual = 0

    st.subheader("Results")
    st.write(f"**Amount in {start_year}:** {amount:,.2f}")
    st.write(f"**Amount in {end_year}:** {cost2:,.2f}")
    st.write(f"**Percentage change:** {pct_change:.2f}%")
    st.write(f"**Number of years:** {num_years}")
    st.write(f"**Average annual inflation:** {avg_annual:.2f}%")
    st.write(f"**CPI {start_year}:** {cpi1}")
    st.write(f"**CPI {end_year}:** {cpi2}")