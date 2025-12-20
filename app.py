import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="World Bank Dashboard", layout="wide")

# ======================
# Load data
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("worldbank_full_data.csv")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df

df = load_data()

st.title("🌍 World Bank Dashboard – Life Expectancy Analysis")

# ======================
# Sidebar
# ======================
st.sidebar.header("🎛 Bộ lọc")

countries = sorted(df["country"].dropna().unique())
countries = ["🌍 World (Average)"] + countries

selected_country = st.sidebar.selectbox("Chọn quốc gia", countries)

if selected_country == "🌍 World (Average)":
    df_country = (
        df
        .groupby("year", as_index=False)
        .mean(numeric_only=True)
    )
else:
    df_country = df[df["country"] == selected_country]


min_year = int(df_country["year"].min())
max_year = int(df_country["year"].max())

year_range = st.sidebar.slider(
    "Chọn khoảng năm",
    min_year,
    max_year,
    (min_year, max_year)
)

df_country = df_country[
    (df_country["year"] >= year_range[0]) &
    (df_country["year"] <= year_range[1])
].sort_values("year")

indicators = [
    c for c in df.columns if c not in ["country", "year"]
]

selected_indicators = st.sidebar.multiselect(
    "Chọn chỉ số",
    indicators,
    default=["life_expectancy"]
)

# ======================
# Tabs
# ======================
tab1, tab2, tab3 = st.tabs(
    ["📈 Time Series", "🔁 Life Expectancy Relationship", "📊 Correlation"]
)

# ----- TAB 1 -----
with tab1:
    st.subheader(f"{selected_country} – Chỉ số theo năm")

    for ind in selected_indicators:
        fig = px.line(
            df_country,
            x="year",
            y=ind,
            markers=True,
            title=f"{ind} over time"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_country)

# ----- TAB 2 -----
with tab2:
    st.subheader("Life Expectancy vs các biến khác")

    other_vars = [v for v in indicators if v != "life_expectancy"]
    x_var = st.selectbox("Chọn biến giải thích", other_vars)

    plot_df = df_country[["life_expectancy", x_var]].dropna()

    fig = px.scatter(
        plot_df,
        x=x_var,
        y="life_expectancy",
        trendline="ols",
        title=f"Life Expectancy vs {x_var}"
    )

    if x_var == "gdp_per_capita":
        fig.update_xaxes(type="log")

    st.plotly_chart(fig, use_container_width=True)

# ----- TAB 3 -----
with tab3:
    st.subheader("Correlation Matrix")

    corr_df = df_country[selected_indicators].dropna()

    if len(selected_indicators) >= 2:
        corr = corr_df.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chọn ít nhất 2 chỉ số để xem correlation.")
