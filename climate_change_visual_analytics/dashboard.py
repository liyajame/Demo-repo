"""
Climate Change Dashboard — Final Project
========================================
Interactive Streamlit app exploring Berkeley Earth global temperature data.

How to run:
    streamlit run dashboard.py

The app provides:
    • A country selector (dropdown)
    • A year-range slider
    • Four linked visualizations that update together:
        1. Annual temperature trend for the selected country (with global overlay)
        2. Decadal box plot for the selected country
        3. Country-vs-world warming comparison (bar chart)
        4. Seasonal anomaly heatmap for the selected country
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================================================================
# Page config
# =====================================================================
st.set_page_config(
    page_title="Climate Change Dashboard",
    page_icon="🌡️",
    layout="wide",
)

# =====================================================================
# Styling constants (match the notebook's warm-cool palette)
# =====================================================================
ACCENT_COLD = "#2166AC"
ACCENT_WARM = "#B2182B"
ACCENT_NEUT = "#4D4D4D"
WARM_COOL_SCALE = [
    "#2166AC", "#67A9CF", "#D1E5F0",
    "#FDDBC7", "#EF8A62", "#B2182B",
]

# =====================================================================
# Data loading (cached so the 22 MB CSV only loads once)
# =====================================================================
@st.cache_data
def load_data():
    """Load and preprocess the three Berkeley Earth files."""
    global_df = pd.read_csv("data/GlobalTemperatures.csv", parse_dates=["dt"])
    country_df = pd.read_csv(
        "data/GlobalLandTemperaturesByCountry.csv", parse_dates=["dt"]
    )

    # --- clean ---
    global_df = global_df.dropna(subset=["LandAverageTemperature"]).reset_index(drop=True)
    country_df = country_df.dropna(subset=["AverageTemperature"]).reset_index(drop=True)

    # --- remove continental aggregates that appear as "countries" ---
    aggregates = {
        "Africa", "Asia", "Europe", "North America", "South America",
        "Oceania", "Antarctica", "Americas",
        "Europe (non-EU)", "European Union",
        "Denmark (Europe)", "France (Europe)",
        "Netherlands (Europe)", "United Kingdom (Europe)",
    }
    country_df = country_df[~country_df["Country"].isin(aggregates)].reset_index(drop=True)

    # --- feature engineering ---
    for df, tcol in [(global_df, "LandAverageTemperature"), (country_df, "AverageTemperature")]:
        df["Year"] = df["dt"].dt.year
        df["Month"] = df["dt"].dt.month
        df["Decade"] = (df["Year"] // 10) * 10
        season_map = {12: "DJF", 1: "DJF", 2: "DJF",
                      3: "MAM", 4: "MAM", 5: "MAM",
                      6: "JJA", 7: "JJA", 8: "JJA",
                      9: "SON", 10: "SON", 11: "SON"}
        df["Season"] = df["Month"].map(season_map)

        # Anomaly vs 1951-1980 baseline (NASA/NOAA reference period)
        baseline = (
            df[(df["Year"] >= 1951) & (df["Year"] <= 1980)]
            .groupby("Month")[tcol].mean()
        )

        if tcol == "AverageTemperature":
            # Country-specific baseline (per-country, per-month climatology)
            country_baseline = (
                df[(df["Year"] >= 1951) & (df["Year"] <= 1980)]
                .groupby(["Country", "Month"])[tcol].mean()
                .reset_index()
                .rename(columns={tcol: "baseline"})
            )
            df = df.merge(country_baseline, on=["Country", "Month"], how="left")
            df["Anomaly"] = df[tcol] - df["baseline"]
            country_df = df.drop(columns=["baseline"])
        else:
            df["Anomaly"] = df.apply(
                lambda r: r[tcol] - baseline.loc[r["Month"]], axis=1
            )
            global_df = df

    return global_df, country_df


# =====================================================================
# Load data (with spinner)
# =====================================================================
with st.spinner("Loading Berkeley Earth climate data..."):
    global_df, country_df = load_data()

# =====================================================================
# Title & intro
# =====================================================================
st.title("🌡️ Climate Change Dashboard")
st.markdown(
    """
    **Research question:** *In this project, we investigate whether the industrial era
    influences global land surface temperature patterns using real-world data from
    the Berkeley Earth Surface Temperature Study.*

    Use the sidebar controls to explore warming patterns for any country and any
    time window. All four panels below update together.
    """
)
st.divider()

# =====================================================================
# SIDEBAR — interactive controls
# =====================================================================
st.sidebar.header("🎛️ Controls")

# -- Country selector (dropdown) --
all_countries = sorted(country_df["Country"].unique())
default_country = "India" if "India" in all_countries else all_countries[0]
selected_country = st.sidebar.selectbox(
    "Select a country",
    options=all_countries,
    index=all_countries.index(default_country),
    help="All four visualizations will update for the country you choose.",
)

# -- Year range slider --
year_min = int(country_df["Year"].min())
year_max = int(country_df["Year"].max())
year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(1850, year_max),
    step=1,
    help="Drag either end to focus on a time window.",
)

# -- Smoothing slider --
smoothing_years = st.sidebar.slider(
    "Rolling-mean window (years)",
    min_value=1,
    max_value=30,
    value=10,
    step=1,
    help="Larger values produce a smoother trend line.",
)

st.sidebar.divider()
st.sidebar.markdown(
    f"**Selected country:** `{selected_country}`  \n"
    f"**Years:** `{year_range[0]} – {year_range[1]}`  \n"
    f"**Smoothing:** `{smoothing_years}-year rolling mean`"
)

# =====================================================================
# Filter data based on selections
# =====================================================================
country_sel = country_df[
    (country_df["Country"] == selected_country)
    & (country_df["Year"].between(*year_range))
].copy()

global_sel = global_df[global_df["Year"].between(*year_range)].copy()

# =====================================================================
# Headline KPI row
# =====================================================================
if len(country_sel) > 0:
    early_period = country_sel[country_sel["Year"].between(year_range[0], year_range[0] + 30)]
    late_period = country_sel[country_sel["Year"].between(year_range[1] - 30, year_range[1])]

    if len(early_period) > 0 and len(late_period) > 0:
        early_temp = early_period["AverageTemperature"].mean()
        late_temp = late_period["AverageTemperature"].mean()
        warming = late_temp - early_temp

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Country", selected_country)
        col2.metric(
            f"Avg temp ({year_range[0]}s)", f"{early_temp:.2f} °C"
        )
        col3.metric(
            f"Avg temp ({year_range[1]}s)", f"{late_temp:.2f} °C"
        )
        col4.metric(
            "Change",
            f"{warming:+.2f} °C",
            delta=f"{warming:+.2f} °C",
            delta_color="inverse",  # red = warming (bad), blue = cooling
        )

st.divider()

# =====================================================================
# 2×2 chart grid
# =====================================================================
left_col, right_col = st.columns(2)

# --------------------------------------------------
# Chart 1 — Annual trend (country + global overlay)
# --------------------------------------------------
with left_col:
    st.subheader(f"📈 Annual temperature trend — {selected_country}")

    annual_country = country_sel.groupby("Year")["AverageTemperature"].mean().reset_index()
    annual_country["Smoothed"] = (
        annual_country["AverageTemperature"].rolling(smoothing_years, center=True).mean()
    )

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=annual_country["Year"],
            y=annual_country["AverageTemperature"],
            mode="lines", name="Annual mean",
            line=dict(color=ACCENT_NEUT, width=1),
            opacity=0.4,
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=annual_country["Year"],
            y=annual_country["Smoothed"],
            mode="lines",
            name=f"{smoothing_years}-yr rolling mean",
            line=dict(color=ACCENT_WARM, width=3),
        )
    )
    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Annual mean temperature (°C)",
        hovermode="x unified",
        height=380,
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "The thin grey line shows raw annual means; the red line removes year-to-year "
        "noise to reveal the underlying trend."
    )

# --------------------------------------------------
# Chart 2 — Decadal box plot
# --------------------------------------------------
with right_col:
    st.subheader(f"📦 Temperature distribution by decade — {selected_country}")

    box_df = country_sel[country_sel["Decade"] >= (year_range[0] // 10) * 10].copy()

    fig2 = px.box(
        box_df, x="Decade", y="AverageTemperature",
        color="Decade",
        color_discrete_sequence=px.colors.sample_colorscale(
            WARM_COOL_SCALE, [i / max(1, box_df["Decade"].nunique() - 1)
                              for i in range(box_df["Decade"].nunique())]
        ),
    )
    fig2.update_layout(
        xaxis_title="Decade",
        yaxis_title="Monthly temperature (°C)",
        showlegend=False,
        height=380,
        margin=dict(l=20, r=20, t=10, b=20),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "Each box spans the middle 50% of monthly temperatures for that decade. "
        "A rising median and upper whisker indicates warming."
    )

# --------------------------------------------------
# Chart 3 — Warming comparison (country vs global vs neighbours)
# --------------------------------------------------
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("🌍 Warming comparison — top 10 + your country")

    # Warming = mean of second half minus mean of first half of selected window
    midpoint = (year_range[0] + year_range[1]) // 2
    first_half = (
        country_df[country_df["Year"].between(year_range[0], midpoint)]
        .groupby("Country")["AverageTemperature"].mean()
    )
    second_half = (
        country_df[country_df["Year"].between(midpoint, year_range[1])]
        .groupby("Country")["AverageTemperature"].mean()
    )
    warming = (second_half - first_half).dropna().sort_values(ascending=False)

    top10 = warming.head(10)
    if selected_country not in top10.index and selected_country in warming.index:
        sel_value = warming.loc[selected_country]
        bar_data = pd.concat([top10, pd.Series({selected_country: sel_value})])
    else:
        bar_data = top10

    bar_df = bar_data.reset_index()
    bar_df.columns = ["Country", "Warming"]
    bar_df = bar_df.sort_values("Warming", ascending=True)
    bar_df["Color"] = np.where(
        bar_df["Country"] == selected_country, ACCENT_WARM, "#B8B8B8"
    )

    fig3 = go.Figure()
    fig3.add_trace(
        go.Bar(
            x=bar_df["Warming"], y=bar_df["Country"],
            orientation="h",
            marker_color=bar_df["Color"],
            text=[f"+{v:.2f}°C" for v in bar_df["Warming"]],
            textposition="outside",
        )
    )
    fig3.update_layout(
        xaxis_title=f"Temp change ({midpoint}-{year_range[1]} minus {year_range[0]}-{midpoint}), °C",
        yaxis_title="",
        height=420,
        margin=dict(l=20, r=50, t=10, b=40),
        showlegend=False,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        f"Red bar highlights **{selected_country}**. Compares the warming amount "
        f"against the ten countries that warmed the most in this time window."
    )

# --------------------------------------------------
# Chart 4 — Seasonal heatmap (month × decade) for selected country
# --------------------------------------------------
with right_col2:
    st.subheader(f"🔥 Month × decade heatmap — {selected_country}")

    heat_df = (
        country_sel.groupby(["Decade", "Month"])["Anomaly"].mean().unstack("Month")
    )
    if not heat_df.empty:
        heat_df.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        fig4 = px.imshow(
            heat_df,
            color_continuous_scale=WARM_COOL_SCALE,
            color_continuous_midpoint=0,
            labels=dict(x="Month", y="Decade", color="Anomaly (°C)"),
            aspect="auto",
        )
        fig4.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=10, b=20),
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.caption(
            "Each cell = one month's anomaly vs the 1951-1980 baseline. "
            "Blue → colder than baseline. Red → warmer."
        )
    else:
        st.info("Not enough data for a heatmap in this country / year range.")

st.divider()

# =====================================================================
# Footer
# =====================================================================
st.markdown(
    """
    ### How to read this dashboard
    - **Sidebar controls** filter all four charts simultaneously.
    - **Hover** over any chart for exact values.
    - Anomalies are computed against the **1951-1980 baseline**, the standard
      NASA/NOAA reference period.

    **Data source:** Berkeley Earth Surface Temperature Study
    (via Kaggle: *Climate Change: Earth Surface Temperature Data*).
    """
)
