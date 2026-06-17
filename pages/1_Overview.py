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

# Header
st.title("📊 Overview")

# KPI Cards
kpis = kpi_summary(df)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Bookings",
        f"{kpis['bookings']:,}"
    )

with c2:
    st.metric(
        "Cancellation Rate",
        f"{kpis['cancel_rate']:.1f}%"
    )

with c3:
    st.metric(
        "Average ADR",
        f"${kpis['adr']:.2f}"
    )

with c4:
    st.metric(
        "Revenue",
        f"${kpis['revenue']:,.0f}"
    )

# Bookings by Hotel Type
hotel_df = (
    df.groupby("hotel")
      .size()
      .reset_index(name="bookings")
)

fig = px.bar(
    hotel_df,
    x="hotel",
    y="bookings",
    title="Bookings by Hotel Type"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Cancellation by Hotel
cancel_df = (
    df.groupby("hotel")["is_canceled"]
      .mean()
      .mul(100)
      .reset_index()
)

fig = px.pie(
    cancel_df,
    names="hotel",
    values="is_canceled",
    title="Cancellation Rate by Hotel"
)

st.plotly_chart(
    fig,
    use_container_width=True
)