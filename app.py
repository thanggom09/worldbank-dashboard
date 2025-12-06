import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("worldbank_full_data.csv")

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
