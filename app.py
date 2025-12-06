import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load dữ liệu ---
@st.cache_data
def load_data():
    df = pd.read_csv("worldbank_full_data.csv")
    return df

df = load_data()

st.title("World Bank Dashboard - Local App")

# --- Chọn quốc gia ---
countries = df['country'].unique()
selected_country = st.selectbox("Chọn quốc gia", countries)

df_country = df[df['country'] == selected_country].sort_values('year')

# --- Hiển thị bảng dữ liệu ---
st.subheader(f"Dữ liệu {selected_country}")
st.dataframe(df_country)

# --- Chọn chỉ số vẽ biểu đồ (CHỈ 1 CHỈ SỐ) ---
indicators = [col for col in df.columns if col not in ['country','year']]

# Giá trị mặc định: chỉ số đầu tiên trong dataset
default_indicator = indicators[0]

selected_indicator = st.selectbox(
    "Chọn chỉ số để vẽ",
    indicators,
    index=indicators.index(default_indicator)
)

# --- Vẽ biểu đồ ---
st.subheader(f"Biểu đồ {selected_indicator} theo năm")

fig = px.line(
    df_country,
    x='year',
    y=selected_indicator,
    markers=True,
    title=f"{selected_country} - {selected_indicator} over years"
)

st.plotly_chart(fig, use_container_width=True)

# --- Load dữ liệu ---
@st.cache_data
def load_data():
    df = pd.read_csv("worldbank_full_data.csv")
    return df

df = load_data()

st.title("World Bank Dashboard - Local App")

# --- Chọn quốc gia ---
countries = df['country'].unique()
selected_country = st.selectbox("Chọn quốc gia", countries)

df_country = df[df['country'] == selected_country].sort_values('year')

# --- Hiển thị bảng dữ liệu ---
st.subheader(f"Dữ liệu {selected_country}")
st.dataframe(df_country)

# --- Chọn chỉ số vẽ biểu đồ ---
indicators = [col for col in df.columns if col not in ['country','year']]
selected_indicators = st.multiselect("Chọn chỉ số để vẽ", indicators, default=indicators[:3])

if selected_indicators:
    st.subheader("Biểu đồ theo năm")
    fig = px.line(df_country, x='year', y=selected_indicators,
                  markers=True, title=f"{selected_country} - Indicators over years")
    st.plotly_chart(fig, use_container_width=True)
