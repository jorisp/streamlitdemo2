import pandas as pd
from pathlib import Path
import streamlit as st

st.header('Inflatiecalculator met Belgische CPI gegevens')

CPI_DATA_URL = 'https://raw.githubusercontent.com/jorisp/tradingnotebooks/master/data/static_inflationcalc_be_2025.csv'
#CPI_DATA_SOURCE = Path(__file__).parent/ 'data/static_inflationcalc_be_2025.csv'

st.markdown(
    """
    Deze tool gebruikt een csv bestand met de CPI-dataset die automatisch wordt ingeladen van mijn GitHub repo.
    https://www.github.com/jorisp/tradingnotebooks/blob/master/data/static_inflationcalc_be_2025.csv
    De berekening is als volgt:
    - Nieuwe kost eind jaar: `Bedrag eind jaar = bedrag start jaar * (HICP2 / HICP1)`
    - Procentuele verandering: `((Cost2 - Cost1) / Cost1) * 100`
    """
)

# --- Data laden ---
try:
    df = pd.read_csv(CPI_DATA_URL )
except Exception as e:
    st.error(f"Kon de CPI-data niet laden: {e}")
    st.stop()

# Validatie
if not {"year", "cpi"}.issubset(df.columns):
    st.error("CSV moet kolommen 'year' en 'cpi' bevatten.")
    st.stop()

df = df.sort_values("year")

st.subheader("Ingeladen CPI-data")
st.write(df)

# --- Inputvelden ---
amount = st.number_input("Bedrag in startjaar", min_value=100, value=100,step=100)
start_year = st.selectbox("Startjaar", df["year"])
end_year = st.selectbox("Eindjaar", df["year"])

# --- Berekening ---
if st.button("Bereken inflatie"):
    cpi1 = df.loc[df["year"] == start_year, "cpi"].values[0]
    cpi2 = df.loc[df["year"] == end_year, "cpi"].values[0]

    cost2 = amount * (cpi2 / cpi1)
    pct_change = ((cost2 - amount) / amount) * 100
    num_years = end_year - start_year

    if num_years > 0:
        avg_annual = ((cpi2 / cpi1) ** (1 / num_years) - 1) * 100
    else:
        avg_annual = 0

    st.subheader("Resultaten")
    st.write(f"**Bedrag in {start_year}:** {amount:,.2f}")
    st.write(f"**Bedrag in {end_year}:** {cost2:,.2f}")
    st.write(f"**Procentuele verandering:** {pct_change:.2f}%")
    st.write(f"**Aantal jaren:** {num_years}")
    st.write(f"**Gemiddelde jaarlijkse inflatie:** {avg_annual:.2f}%")
    st.write(f"**CPI {start_year}:** {cpi1}")
    st.write(f"**CPI {end_year}:** {cpi2}")