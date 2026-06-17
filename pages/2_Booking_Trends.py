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
st.title("📅 Booking Trends")

# Monthly Bookings
monthly = (
    df.groupby(
        ["arrival_date_year",
         "arrival_month_num"]
    )
    .size()
    .reset_index(name="bookings")
)

fig = px.line(
    monthly,
    x="arrival_month_num",
    y="bookings",
    color="arrival_date_year",
    markers=True,
    title="Monthly Bookings"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Lead Time Distribution
fig = px.histogram(
    df,
    x="lead_time",
    nbins=40,
    title="Lead Time Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ADR Distribution
fig = px.box(
    df,
    x="hotel",
    y="adr",
    title="ADR by Hotel"
)

st.plotly_chart(
    fig,
    use_container_width=True
)