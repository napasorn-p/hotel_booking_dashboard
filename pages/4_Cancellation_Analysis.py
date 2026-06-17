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
st.title("❌ Cancellation Analysis")

# Cancellation by Market Segment
cancel_segment = (
    df.groupby("market_segment")
      ["is_canceled"]
      .mean()
      .mul(100)
      .reset_index()
)

fig = px.bar(
    cancel_segment,
    x="market_segment",
    y="is_canceled",
    title="Cancellation Rate by Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Cancellation by Deposit Type
deposit_df = (
    df.groupby("deposit_type")
      ["is_canceled"]
      .mean()
      .mul(100)
      .reset_index()
)

fig = px.bar(
    deposit_df,
    x="deposit_type",
    y="is_canceled",
    title="Cancellation by Deposit Type"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Lead Time vs Cancellation
fig = px.box(
    df,
    x="is_canceled",
    y="lead_time",
    title="Lead Time vs Cancellation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)