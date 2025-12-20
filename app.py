import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("worldbank_full_data.csv")import streamlit as st
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
# Sidebar controls
# ======================
st.sidebar.header("🎛 Bộ lọc dữ liệu")

# --- Country selector ---
countries = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox("Chọn quốc gia", countries)

df_country = df[df['country'] == selected_country]

# --- Year range ---
min_year = int(df_country['year'].min())
max_year = int(df_country['year'].max())

year_range = st.sidebar.slider(
    "Chọn khoảng năm",
    min_year,
    max_year,
    (min_year, max_year)
)

df_country = df_country[
    (df_country['year'] >= year_range[0]) &
    (df_country['year'] <= year_range[1])
].sort_values("year")

# --- Indicators ---
indicators = [
    col for col in df.columns
    if col not in ['country', 'year']
]

selected_indicators = st.sidebar.multiselect(
    "Chọn chỉ số",
    indicators,
    default=["life_expectancy"]
)

# ======================
# Main layout
# ======================
tab1, tab2, tab3 = st.tabs(
    ["📈 Time Series", "🔁 Quan hệ với Life Expectancy", "📊 Correlation"]
)

# ======================
# TAB 1 – Time Series
# ======================
with tab1:
    st.subheader(f"📈 Chỉ số theo năm – {selected_country}")

    for indicator in selected_indicators:
        fig = px.line(
            df_country,
            x="year",
            y=indicator,
            markers=True,
            title=f"{indicator} over time"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_country)

# ======================
# TAB 2 – Life Expectancy Relationship
# ======================
with tab2:
    st.subheader("🔁 Quan hệ với Life Expectancy")

    other_vars = [v for v in indicators if v != "life_expectancy"]

    x_var = st.selectbox(
        "Chọn biến giải thích",
        other_vars
    )

    plot_df = df_country[['life_expectancy', x_var]].dropna()

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

# ======================
# TAB 3 – Correlation
# ======================
with tab3:
    st.subheader("📊 Correlation Matrix")

    corr_df = df_country[selected_indicators].dropna()

    if len(selected_indicators) >= 2:
        corr = corr_df.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu",
            title="Correlation Matrix"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chọn ít nhất 2 chỉ số để xem correlation.")


df = load_data()

st.title("World Bank Dashboard - Local App")

# --- Chọn quốc gia ---
countries = df['country'].unique()
selected_country = st.selectbox(
    "Chọn quốc gia",
    countries,
    key="country_selector"
)

df_country = df[df['country'] == selected_country].sort_values("year")

# --- Hiển thị bảng dữ liệu ---
st.subheader(f"Dữ liệu {selected_country}")
st.dataframe(df_country)

# --- Chọn chỉ số vẽ (1 chỉ số duy nhất) ---
indicators = [col for col in df.columns if col not in ['country', 'year']]
default_indicator = indicators[0]

selected_indicator = st.selectbox(
    "Chọn chỉ số để vẽ",
    indicators,
    index=indicators.index(default_indicator),
    key="indicator_selector"
)

# --- Vẽ biểu đồ ---
st.subheader(f"Biểu đồ {selected_indicator} theo năm")

fig = px.line(
    df_country,
    x="year",
    y=selected_indicator,
    markers=True,
    title=f"{selected_country} - {selected_indicator} over years"
)
st.plotly_chart(fig, use_container_width=True)
