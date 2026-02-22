import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ---- LOAD DATA ----
df = pd.read_csv("data/processed/engineered_features.csv")

# ---- SIDEBAR ----
st.sidebar.title("Filters")

# YEAR FILTER
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2024)
)

# STATE SELECTOR
states = sorted(df["State_y"].dropna().unique())

selected_state = st.sidebar.selectbox(
    "Select Region / State",
    states
)

# FILTER DATA
filtered = df[
    (df["Year"].between(year_range[0], year_range[1])) &
    (df["State_y"] == selected_state)
]

# ---- TITLE ----
st.title("🌡 Climate Change Impact Analyzer")
st.caption("Exploring climate trends across India")

# ---- KPI ----
c1, c2, c3 = st.columns(3)

c1.metric("Avg Temperature", f"{filtered['Avg_Temperature'].mean():.2f} °C")
c2.metric("Avg Rainfall", f"{filtered['Annual_Rainfall'].mean():.0f} mm")
c3.metric("Records Selected", len(filtered))

st.write("---")

# ---- GRAPHS ----
g1, g2 = st.columns(2)

with g1:
    st.subheader("Temperature Trend")
    temp = filtered.groupby("Year")["Avg_Temperature"].mean().reset_index()
    fig1 = px.line(temp, x="Year", y="Avg_Temperature", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    st.subheader("Rainfall Trend")
    rain = filtered.groupby("Year")["Annual_Rainfall"].mean().reset_index()
    fig2 = px.area(rain, x="Year", y="Annual_Rainfall")
    st.plotly_chart(fig2, use_container_width=True)

st.write("---")

# ---- RAW DATA ----
if st.checkbox("View Raw Data"):
    st.dataframe(filtered)