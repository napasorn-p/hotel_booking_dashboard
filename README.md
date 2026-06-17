# Hotel Booking Analytics Dashboard

A Streamlit multi-page analytics dashboard built on the Hotel Booking Demand Dataset (Kaggle).

## Project Structure

```
hotel_booking_dashboard/
│
├── app.py                          # Entry point — Streamlit app config & home page
├── config.py                       # Global constants (file paths, color palette, chart defaults)
├── requirements.txt                # Python dependencies (streamlit, pandas, plotly, etc.)
├── README.md                       # This file
├── .gitignore                      # Excludes raw data, __pycache__, .env
│
├── data/
│   ├── raw/
│   │   └── hotel_bookings.csv      # Original dataset downloaded from Kaggle (DO NOT EDIT)
│   └── processed/
│       └── hotel_bookings_clean.csv  # Cleaned dataset produced by data_processor.py
│
├── pages/                          # Streamlit auto-discovers these as navigation pages
│   ├── 1_Overview.py               # Page 1: KPI cards, summary charts, hotel comparison
│   ├── 2_Booking_Trends.py         # Page 2: Monthly trends, lead time, ADR over time
│   ├── 3_Customer_Insights.py      # Page 3: Country map, guest type, stay duration, segments
│   └── 4_Cancellation_Analysis.py  # Page 4: Cancellation rate by segment, deposit, lead time
│
├── components/                     # Reusable UI building blocks shared across pages
│   ├── kpi_cards.py                # Metric cards (Total Bookings, Cancellation Rate, ADR, etc.)
│   ├── charts.py                   # Chart factory functions (bar, line, donut, heatmap, map)
│   ├── filters.py                  # Sidebar filter widgets (hotel type, year, month, segment)
│   └── sidebar.py                  # Sidebar layout wrapper and filter orchestration
│
├── utils/                          # Backend logic — no Streamlit UI code here
│   ├── data_loader.py              # Reads CSV into a DataFrame with caching (@st.cache_data)
│   ├── data_processor.py           # Cleans raw data, engineers features (revenue, total nights)
│   ├── metrics.py                  # Computes aggregated metrics used by KPI cards and charts
│   └── theme.py                    # Color palette, font settings, Plotly layout defaults
│
└── assets/
    └── style.css                   # Custom CSS injected via st.markdown for styling overrides
```

## How the layers connect

```
CSV File
  └── data_loader.py      (load & cache)
        └── data_processor.py   (clean & engineer features)
              └── metrics.py          (aggregate for charts)
                    └── components/         (render UI)
                          └── pages/              (compose full pages)
                                └── app.py              (entry point)
```

## Getting Started

1. Download `hotel_bookings.csv` from Kaggle and place it in `data/raw/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
