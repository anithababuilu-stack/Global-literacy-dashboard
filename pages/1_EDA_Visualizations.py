import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Visualizations", layout="wide")
st.title("📈 EDA Visualizations")

conn = sqlite3.connect("Education.db")

df = pd.read_sql("""
SELECT country, year, adult_literacy_rate
FROM literacy_rates
WHERE adult_literacy_rate IS NOT NULL
""", conn)

st.write("Rows loaded:", len(df))

country_list = sorted(df["country"].dropna().unique())

selected_country = st.selectbox("Select Country", country_list)

filtered_df = df[df["country"] == selected_country].sort_values("year")

st.subheader(f"Adult Literacy Trend - {selected_country}")

fig = px.line(
    filtered_df,
    x="year",
    y="adult_literacy_rate",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered_df, use_container_width=True)

conn.close()