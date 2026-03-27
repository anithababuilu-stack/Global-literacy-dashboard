import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SQL Query Runner", layout="wide")
st.title("🧮 SQL Query Runner")

conn = sqlite3.connect("Education.db")

queries = {
    "1.Get top 5 countries with highest adult literacy in 2020": """
        SELECT country, adult_literacy_rate
        FROM literacy_rates
        WHERE year = 2020
        ORDER BY adult_literacy_rate DESC
        LIMIT 5;
    """,

    "2.Find countries where female youth literacy < 80%": """
        SELECT country, year,youth_literacy_female
        FROM literacy_rates
        WHERE youth_literacy_female < 80
        ORDER BY youth_literacy_female ASC;
    """,

    "3.Average adult literacy per continent (owid region": """
        SELECT region, AVG(adult_literacy_rate) AS avg_literacy
        FROM literacy_rates
        GROUP BY region
        ORDER BY avg_literacy DESC;
    """,

    "4. Countries with illiteracy % > 20% in 2000.": """
        SELECT country , illiteracy_rate
        FROM illiteracy_population
        WHERE year = 2000 AND illiteracy_rate   >20
        ORDER BY illiteracy_rate   DESC
    """,

    "5. Trend of illiteracy % for India (2000–2020)": """
        SELECT year, illiteracy_rate
        FROM illiteracy_population
        WHERE country ='india' AND year BETWEEN 2000 AND 2020
        ORDER BY year ASC
        LIMIT 5;
    """,

    "6. Top 10 countries with largest illiterate population in the last year": """
       SELECT  country,illiteracy_rate
       FROM illiteracy_population
       WHERE year = 2023
       ORDER BY country DESC
       LIMIT 10;
    """,

    "7.Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.": """
        SELECT  country,year,avg_years_schooling,gdp_per_capita
        FROM gdp_schooling
        WHERE avg_years_schooling >7 AND gdp_per_capita <5000
        ORDER BY avg_years_schooling DESC;
    """,

    "8.Rank countries by GDP per schooling for the year 2020": """
        SELECT  country,avg_years_schooling,gdp_per_capita,
        (gdp_per_capita / avg_years_schooling) AS gdp_per_schooling
        FROM gdp_schooling
        WHERE year=2020
        ORDER BY gdp_per_capita DESC;
    """,

    "9.Find global average schooling years per year": """
        SELECT  year,AVG(avg_years_schooling) AS Avg_SChooling
        from gdp_schooling
        GROUP BY year
        ORDER BY year;
    """,

    " 10. List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling(less than 6).": """
        SELECT country,gdp_per_capita ,avg_years_schooling
        from gdp_schooling
        WHERE year=2020 AND avg_years_schooling <6
        ORDER BY gdp_per_capita DESC
        LIMIT 10;
    """,

    "11. Show countries where the illiterate population is high despite having more than 10 average years of schooling.": """
        SELECT g.country,g.year,g.avg_years_schooling,i.illiteracy_rate
        from gdp_schooling g
        JOIN illiteracy_population i
        ON g.country = i.country AND g.year = i.year
        WHERE g.avg_years_schooling > 10
        AND i.illiteracy_rate > 10
        ORDER BY i.illiteracy_rate DESC;
    """,

    "12. Compare literacy rates and GDP per capita growth for a selected country over the last 20 years.": """
        SELECT
        l.year,
        l.adult_literacy_rate,
        g.gdp_per_capita
        FROM literacy_rates l
        JOIN gdp_schooling g
        ON l.country = g.country AND l.year = g.year
        WHERE l.country = 'india'
        AND l.year >= 2003
        ORDER BY l.year;
    """,

    "13.Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.": """
        SELECT
        l.country,
        l.youth_literacy_male,
        l.youth_literacy_female,
        (l.youth_literacy_male - l.youth_literacy_female) AS literacy_gap,
        g.gdp_per_capita
        FROM literacy_rates l
        JOIN gdp_schooling g
        ON l.country = g.country AND l.year = g.year
        WHERE l.year = 2020
        AND g.gdp_per_capita > 30000
        ORDER BY literacy_gap DESC;
    """
}

selected_query = st.selectbox("Select a Query", list(queries.keys()))

if st.button("Run Query"):
    result_df = pd.read_sql(queries[selected_query], conn)

    st.subheader("Query Result")
    st.dataframe(result_df, use_container_width=True)

    numeric_cols = result_df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) > 0:
        x_col = result_df.columns[0]
        y_col = numeric_cols[-1]

        fig = px.bar(result_df, x=x_col, y=y_col, title=selected_query)
        st.plotly_chart(fig, use_container_width=True)

conn.close()