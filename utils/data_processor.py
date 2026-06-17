# utils/data_processor.py

import pandas as pd


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and engineer features for the hotel booking dataset.
    """

    if df.empty:
        return df

    df = df.copy()

    # -------------------------
    # Missing values
    # -------------------------
    df["children"] = df["children"].fillna(0)
    df["country"] = df["country"].fillna("Unknown")
    df["agent"] = df["agent"].fillna(0)
    df["company"] = df["company"].fillna(0)

    # -------------------------
    # Numeric conversions
    # -------------------------
    numeric_cols = [
        "children",
        "babies",
        "adults",
        "lead_time",
        "adr",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # -------------------------
    # Total guests
    # -------------------------
    df["total_guests"] = (
        df["adults"]
        + df["children"]
        + df["babies"]
    )

    # -------------------------
    # Total nights
    # -------------------------
    df["total_nights"] = (
        df["stays_in_week_nights"]
        + df["stays_in_weekend_nights"]
    )

    # -------------------------
    # Estimated revenue
    # -------------------------
    df["revenue"] = (
        df["adr"]
        * df["total_nights"]
    )

    # -------------------------
    # Arrival date
    # -------------------------
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    df["arrival_month_num"] = (
        df["arrival_date_month"]
        .map(month_map)
    )

    df["arrival_date"] = pd.to_datetime(
        {
            "year": df["arrival_date_year"],
            "month": df["arrival_month_num"],
            "day": df["arrival_date_day_of_month"],
        },
        errors="coerce"
    )

    return df