# utils/metrics.py

import pandas as pd


def total_bookings(df: pd.DataFrame) -> int:
    return len(df)


def cancellation_rate(df: pd.DataFrame) -> float:
    if df.empty:
        return 0

    return (
        df["is_canceled"].mean() * 100
    )


def average_adr(df: pd.DataFrame) -> float:
    return df["adr"].mean()


def total_revenue(df: pd.DataFrame) -> float:
    return df["revenue"].sum()


def average_stay(df: pd.DataFrame) -> float:
    return df["total_nights"].mean()


def kpi_summary(df: pd.DataFrame) -> dict:
    return {
        "bookings": total_bookings(df),
        "cancel_rate": cancellation_rate(df),
        "adr": average_adr(df),
        "revenue": total_revenue(df),
        "avg_stay": average_stay(df),
    }