# =============================================================================
# app.py — Entry Point for the Hotel Booking Analytics Dashboard
# =============================================================================
# This is the first file Streamlit runs when you type:
#   streamlit run app.py
#
# It does three things:
#   1. Configures the overall app (title, icon, layout)
#   2. Loads and caches the dataset so all pages can use it
#   3. Renders the Home page with a welcome message and dataset preview
# =============================================================================

import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.metrics import kpi_summary

# =============================================================================
# SECTION 1: PAGE CONFIGURATION
# =============================================================================
# st.set_page_config() must be the FIRST Streamlit command in the file.
# It controls how the browser tab and overall layout look.

st.set_page_config(
    page_title="Hotel Booking Analytics",   # Text shown in the browser tab
    page_icon="🏨",                         # Emoji or image shown in the browser tab
    layout="wide",                          # "wide" uses the full screen width
    initial_sidebar_state="expanded",       # Sidebar is open by default
)


# =============================================================================
# SECTION 3: SIDEBAR NAVIGATION
# =============================================================================
# Streamlit automatically adds pages from the /pages folder to the sidebar,
# ordered by their filename prefix (1_, 2_, 3_, 4_).
#
# We add extra content below the auto-generated navigation links:
# a dataset summary and a filter reminder.

with st.sidebar:
    st.markdown("---")  # Horizontal divider line

    st.markdown("### 📂 Dataset Info")

    # Load the data here so we can show row/column counts in the sidebar
    df = load_data()

    if not df.empty:
        # Show basic dataset dimensions
        st.metric(label="Total Records", value=f"{len(df):,}")
        st.metric(label="Total Columns", value=len(df.columns))

        # Show the date range covered by the dataset
        if "arrival_date_year" in df.columns:
            min_year = int(df["arrival_date_year"].min())
            max_year = int(df["arrival_date_year"].max())
            st.caption(f"📅 Years covered: {min_year} – {max_year}")

    st.markdown("---")
    st.caption("🎓 University Data Analytics Project")
    st.caption("Built with Streamlit & Plotly")


# =============================================================================
# SECTION 4: HOME PAGE CONTENT
# =============================================================================
# This section renders the main area of the Home page.
# Each page in the /pages folder renders its OWN content when selected.

# --- Header ---
st.title("🏨 Hotel Booking Analytics Dashboard")
st.markdown(
    "Welcome! Use the **sidebar** to navigate between pages. "
    "This dashboard analyses hotel booking patterns, cancellation behaviour, "
    "and revenue trends using the Hotel Booking Demand Dataset."
)

df = load_data()
kpis = kpi_summary(df)

st.markdown("---")

# --- Page Guide ---
st.markdown("### 📋 Pages in this Dashboard")

# Display each page as a card using Streamlit columns
col1, col2 = st.columns(2)

with col1:
    st.info(
        "**📊 1 — Overview**\n\n"
        "High-level KPIs: total bookings, cancellation rate, "
        "average daily rate, and a hotel-type comparison."
    )
    st.info(
        "**📅 2 — Booking Trends**\n\n"
        "Monthly booking volumes, lead time distributions, "
        "and average daily rate (ADR) over time."
    )

with col2:
    st.info(
        "**🌍 3 — Customer Insights**\n\n"
        "Guest country of origin, customer type breakdown, "
        "and average stay duration by market segment."
    )
    st.info(
        "**❌ 4 — Cancellation Analysis**\n\n"
        "Cancellation rates by segment, deposit type, "
        "lead time, and hotel type."
    )

st.markdown("---")

# --- Dataset Preview ---
st.markdown("### 🗂️ Dataset Preview")

# Only show the preview if the data loaded successfully
if not df.empty:
    st.success(f"✅ Dataset loaded — {len(df):,} rows × {len(df.columns)} columns")

    # Let the user choose how many rows to preview using a slider
    num_rows = st.slider(
        label="Rows to preview",
        min_value=5,
        max_value=50,
        value=10,  # Default to showing 10 rows
        step=5,
    )

    # Display the first N rows of the DataFrame as a table
    st.dataframe(
        df.head(num_rows),
        use_container_width=True,  # Table fills the full page width
    )

    # Show column names and data types below the table
    with st.expander("🔍 View column names and data types"):
        # Create a small summary table of columns and their types
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values.astype(str),
            "Non-Null Count": df.notnull().sum().values,
        })
        st.dataframe(col_info, use_container_width=True)

else:
    # If data didn't load, show instructions
    st.error(
        "❌ No data to display. "
        "Please add the dataset to `data/raw/hotel_bookings.csv` and refresh."
    )