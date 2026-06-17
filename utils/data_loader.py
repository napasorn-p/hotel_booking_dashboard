# =============================================================================
# utils/data_loader.py — Dataset Loading Utility
# =============================================================================
# This file has ONE job: read the CSV file from disk and return it as a
# pandas DataFrame that every page in the dashboard can use.
#
# Why is this a separate file?
#   Instead of writing the same "read CSV" code in all 4 pages, we write it
#   ONCE here and import it wherever needed. This is called the DRY principle:
#   "Don't Repeat Yourself."
#
# How to use this in any page file:
#   from utils.data_loader import load_data
#   df = load_data()
# =============================================================================

import os                  # For building file paths that work on all operating systems
import pandas as pd        # For reading CSV files into a DataFrame
import streamlit as st     # For @st.cache_data and showing error/warning messages
from utils.data_processor import process_data

# =============================================================================
# CONSTANTS — File Paths
# =============================================================================
# Define the path to the raw dataset as a constant at the top of the file.
# If you ever move the file, you only need to change it here — not everywhere
# it's used.
#
# os.path.join() builds the path correctly for both:
#   Windows  →  data\raw\hotel_bookings.csv
#   Mac/Linux → data/raw/hotel_bookings.csv

RAW_DATA_PATH = os.path.join("data", "raw", "hotel_bookings.csv")


# =============================================================================
# MAIN FUNCTION: load_data()
# =============================================================================
# @st.cache_data is a Streamlit decorator that caches (saves) the result of
# this function after the first time it runs.
#
# Without caching:
#   Every button click or filter change causes Streamlit to re-run the whole
#   script — including reading the CSV file again. For a 119,000-row file,
#   that's slow and wasteful.
#
# With @st.cache_data:
#   The CSV is read ONCE. After that, Streamlit returns the saved DataFrame
#   instantly from memory. All 4 pages share the same cached copy.

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Reads hotel_bookings.csv from data/raw/ and returns it as a DataFrame.

    Returns:
        pd.DataFrame: The full hotel bookings dataset if the file is found.
                      An empty DataFrame if the file is missing, so the app
                      doesn't crash — it just shows a warning instead.

    Usage:
        from utils.data_loader import load_data
        df = load_data()
    """

    # ------------------------------------------------------------------
    # STEP 1: Check that the file actually exists before trying to read it
    # ------------------------------------------------------------------
    # os.path.exists() returns True if the file is found, False if not.
    # Without this check, pandas would raise a hard-to-understand error.

    if not os.path.exists(RAW_DATA_PATH):
        # st.error() shows a red error box in the Streamlit app
        st.error(
            f"❌ Dataset file not found at: `{RAW_DATA_PATH}`\n\n"
            "**What to do:**\n"
            "1. Download `hotel_bookings.csv` from Kaggle.\n"
            "2. Place it inside the `data/raw/` folder.\n"
            "3. Refresh this page."
        )
        # Return an empty DataFrame so pages can still load without crashing.
        # Pages should check:  if df.empty: → show message instead of chart
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # STEP 2: Try to read the CSV file
    # ------------------------------------------------------------------
    # We wrap this in try/except to handle unexpected errors gracefully
    # (e.g. a corrupted file, wrong encoding, or permission issues).

    try:
        # pd.read_csv() reads the file and returns a pandas DataFrame.
        # A DataFrame is like a spreadsheet table in Python — rows and columns.
        df = pd.read_csv(RAW_DATA_PATH)

        # ------------------------------------------------------------------
        # STEP 3: Basic validation — make sure the file isn't empty
        # ------------------------------------------------------------------
        if df.empty:
            st.warning(
                "⚠️ The file was found but contains no data. "
                "Please check that the correct `hotel_bookings.csv` was placed "
                "in `data/raw/`."
            )
            return pd.DataFrame()

        # ------------------------------------------------------------------
        # STEP 4: Confirm expected columns are present
        # ------------------------------------------------------------------
        # These are the minimum columns our dashboard needs to function.
        # If they're missing, the dataset is probably the wrong file.

        required_columns = [
            "hotel",
            "is_canceled",
            "arrival_date_year",
            "arrival_date_month",
            "adr",               # Average Daily Rate (room price per night)
            "market_segment",
            "country",
        ]

        # Find which required columns are missing from the loaded file
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.warning(
                f"⚠️ The dataset is missing expected columns: `{missing}`\n\n"
                "The dashboard may not display correctly. "
                "Make sure you are using the Hotel Booking Demand dataset from Kaggle."
            )
            # We still return the DataFrame — partial data is better than nothing

        # ------------------------------------------------------------------
        # STEP 5: Show a success message and return the DataFrame
        # ------------------------------------------------------------------
        # st.success() shows a green confirmation box in the app
        df = process_data(df)

        return df  # ← This is the DataFrame all pages will use

    except Exception as e:
        # If anything unexpected goes wrong, show the error message
        # and return an empty DataFrame so the app doesn't crash.
        st.error(
            f"❌ An error occurred while reading the file:\n\n`{e}`\n\n"
            "Please check that the file is a valid CSV and try again."
        )
        return pd.DataFrame()


# =============================================================================
# QUICK TEST BLOCK
# =============================================================================
# This block runs ONLY when you execute this file directly with Python:
#   python utils/data_loader.py
#
# It does NOT run when Streamlit imports this file normally.
# Use it to quickly verify that the file loads without opening the full app.

if __name__ == "__main__":
    print(f"Looking for dataset at: {RAW_DATA_PATH}")
    print(f"File exists: {os.path.exists(RAW_DATA_PATH)}")

    if os.path.exists(RAW_DATA_PATH):
        df = pd.read_csv(RAW_DATA_PATH)

        print("\n--- Dataset Summary ---")
        print(f"Rows    : {len(df):,}")
        print(f"Columns : {len(df.columns)}")
        print(f"\nColumn names:\n{list(df.columns)}")
        print(f"\nFirst 3 rows:\n{df.head(3)}")
    else:
        print("File not found. Place hotel_bookings.csv in data/raw/")