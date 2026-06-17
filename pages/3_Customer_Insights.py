# Imports
import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.metrics import kpi_summary

# Load data
df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()

#Header
st.title("🌍 Customer Insights")

# Top Countries
country_df = (
    df["country"]
    .value_counts()
    .head(10)
    .reset_index()
)

country_df.columns = [
    "country",
    "bookings"
]

fig = px.bar(
    country_df,
    x="country",
    y="bookings",
    title="Top 10 Countries"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Market Segment
segment_df = (
    df["market_segment"]
    .value_counts()
    .reset_index()
)

segment_df.columns = [
    "segment",
    "bookings"
]

fig = px.pie(
    segment_df,
    names="segment",
    values="bookings",
    title="Market Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Stay Duration
stay_df = (
    df.groupby("market_segment")
      ["total_nights"]
      .mean()
      .reset_index()
)

fig = px.bar(
    stay_df,
    x="market_segment",
    y="total_nights",
    title="Average Stay Duration"
)

st.plotly_chart(
    fig,
    use_container_width=True
)