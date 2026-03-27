import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Global Literacy Dashboard", layout="wide")

st.title("📊 Global Literacy & Education Trends Dashboard")
st.write("Analyze literacy, illiteracy, GDP, and schooling trends across countries.")

conn = sqlite3.connect("Education.db")

countries_df = pd.read_sql(
    "SELECT COUNT(DISTINCT country) AS total_countries FROM literacy_rates",
    conn
)

years_df = pd.read_sql(
    "SELECT MIN(year) AS min_year, MAX(year) AS max_year FROM literacy_rates",
    conn
)

avg_df = pd.read_sql(
    "SELECT ROUND(AVG(adult_literacy_rate), 2) AS avg_literacy FROM literacy_rates",
    conn
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Countries", int(countries_df.loc[0, "total_countries"]))

with col2:
    st.metric(
        "Year Range",
        f"{int(years_df.loc[0, 'min_year'])} - {int(years_df.loc[0, 'max_year'])}"
    )

with col3:
    st.metric("Average Adult Literacy", f"{avg_df.loc[0, 'avg_literacy']}%")

sample_df = pd.read_sql("""
    SELECT country, country_code, year, adult_literacy_rate,
           youth_literacy_male, youth_literacy_female, region
    FROM literacy_rates
    LIMIT 10
""", conn)

st.subheader("Sample Data")
st.dataframe(sample_df, use_container_width=True)

conn.close()