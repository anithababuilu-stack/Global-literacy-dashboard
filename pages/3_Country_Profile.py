import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Country Profile", layout="wide")
st.title("🌍 Country Profile")

conn = sqlite3.connect("Education.db")

literacy_df = pd.read_sql("""
    SELECT country, country_code, year, adult_literacy_rate,
           youth_literacy_male, youth_literacy_female, region
    FROM literacy_rates
""", conn)

gdp_df = pd.read_sql("""
    SELECT country, country_code, year, gdp_per_capita,
           avg_years_schooling, population, region
    FROM gdp_schooling
""", conn)

illiteracy_df = pd.read_sql("""
    SELECT country, country_code, year, illiteracy_rate, literacy_rate
    FROM illiteracy_population
""", conn)

df = literacy_df.merge(
    gdp_df[["country", "year", "gdp_per_capita", "avg_years_schooling", "population"]],
    on=["country", "year"],
    how="left"
)

df = df.merge(
    illiteracy_df[["country", "year", "illiteracy_rate", "literacy_rate"]],
    on=["country", "year"],
    how="left"
)

country_list = sorted(df["country"].dropna().unique())
selected_country = st.selectbox("Select Country", country_list)

country_df = df[df["country"] == selected_country].sort_values("year")

st.subheader(f"{selected_country} - Full Data")
st.dataframe(country_df, use_container_width=True)

fig1 = px.line(
    country_df,
    x="year",
    y="adult_literacy_rate",
    title="Adult Literacy Rate",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    country_df,
    x="year",
    y="gdp_per_capita",
    title="GDP per Capita",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(
    country_df,
    x="year",
    y="avg_years_schooling",
    title="Average Years of Schooling",
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.line(
    country_df,
    x="year",
    y="illiteracy_rate",
    title="Illiteracy Rate",
    markers=True
)
st.plotly_chart(fig4, use_container_width=True)

gender_df = country_df[["year", "youth_literacy_male", "youth_literacy_female"]].melt(
    id_vars="year",
    var_name="Category",
    value_name="Value"
)

fig5 = px.line(
    gender_df,
    x="year",
    y="Value",
    color="Category",
    title="Youth Literacy Male vs Female",
    markers=True
)
st.plotly_chart(fig5, use_container_width=True)

conn.close()