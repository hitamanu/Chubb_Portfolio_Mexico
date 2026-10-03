
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mexico P&C Portfolio",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/portfolio_mexico_filled.csv")

    df["policy_start_date"] = pd.to_datetime(
        df["policy_start_date"],
        dayfirst=True,
        errors="coerce"
    )

    df["year"] = df["policy_start_date"].dt.year

    return df

df = load_data()


st.title("Mexico P&C Portfolio Dashboard")

st.caption(
    "Written Premium and Year-over-Year Premium Growth "
    "by Industry and Geography"
)


st.sidebar.header("Filters")

available_years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Year",
    available_years
)

industry_options = [
    "All"
] + sorted(
    df["industry_final"]
    .dropna()
    .unique()
    .tolist()
)

selected_industry = st.sidebar.selectbox(
    "Industry",
    industry_options
)

state_options = [
    "All"
] + sorted(
    df["state"]
    .dropna()
    .unique()
    .tolist()
)

selected_state = st.sidebar.selectbox(
    "State",
    state_options
)


filtered = df.copy()

if selected_industry != "All":
    filtered = filtered[
        filtered["industry_final"] == selected_industry
    ]

if selected_state != "All":
    filtered = filtered[
        filtered["state"] == selected_state
    ]

if selected_municipality != "All":
    filtered = filtered[
        filtered["municipality"] == selected_municipality
    ]


current = filtered[
    filtered["year"] == selected_year
]

previous = filtered[
    filtered["year"] == selected_year - 1
]

current_premium = current["premium"].sum()
previous_premium = previous["premium"].sum()

if previous_premium > 0:
    premium_growth = (
        current_premium / previous_premium
    ) - 1
else:
    premium_growth = None

premium_change = (
    current_premium - previous_premium
)

policies = current["policy_id"].nunique()
clients = current["ClientId"].nunique()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Written Premium",
    f"${current_premium / 1_000_000:,.1f}M"
)

col2.metric(
    "Premium Growth YoY",
    f"{premium_growth:.1%}"
    if premium_growth is not None
    else "N/A",
    f"${premium_change / 1_000_000:+,.1f}M"
    if previous_premium > 0
    else None
)

col3.metric(
    "Policies",
    f"{policies:,}"
)

col4.metric(
    "Clients",
    f"{clients:,}"
)


trend = (
    filtered
    .groupby("year", as_index=False)
    .agg(
        premium=("premium", "sum")
    )
)

fig_trend = px.line(
    trend,
    x="year",
    y="premium",
    markers=True,
    title="Written Premium Trend"
)

fig_trend.update_yaxes(
    title="Premium (MXN)"
)

fig_trend.update_xaxes(
    dtick=1
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


industry_current = (
    current
    .groupby(
        "industry_final",
        as_index=False
    )
    .agg(
        premium=("premium", "sum")
    )
    .sort_values(
        "premium",
        ascending=True
    )
)

fig_industry = px.bar(
    industry_current,
    x="premium",
    y="industry_final",
    orientation="h",
    title=f"Written Premium by Industry — {selected_year}"
)

fig_industry.update_xaxes(
    title="Premium (MXN)"
)

fig_industry.update_yaxes(
    title=""
)


industry_year = (
    filtered[
        filtered["year"].isin(
            [selected_year - 1, selected_year]
        )
    ]
    .groupby(
        ["industry_final", "year"],
        as_index=False
    )
    .agg(
        premium=("premium", "sum")
    )
)

industry_pivot = (
    industry_year
    .pivot(
        index="industry_final",
        columns="year",
        values="premium"
    )
    .fillna(0)
)

if selected_year not in industry_pivot.columns:
    industry_pivot[selected_year] = 0

if selected_year - 1 not in industry_pivot.columns:
    industry_pivot[selected_year - 1] = 0

industry_pivot["premium_change"] = (
    industry_pivot[selected_year]
    - industry_pivot[selected_year - 1]
)

industry_change = (
    industry_pivot[
        ["premium_change"]
    ]
    .reset_index()
    .sort_values(
        "premium_change",
        ascending=True
    )
)

fig_change = px.bar(
    industry_change,
    x="premium_change",
    y="industry_final",
    orientation="h",
    title=f"Premium Change by Industry — {selected_year} vs {selected_year - 1}"
)

fig_change.update_xaxes(
    title="Premium Change (MXN)"
)

fig_change.update_yaxes(
    title=""
)


left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_industry,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig_change,
        use_container_width=True
    )


state_current = (
    current
    .groupby(
        "state",
        as_index=False
    )
    .agg(
        premium=("premium", "sum")
    )
    .sort_values(
        "premium",
        ascending=False
    )
)

fig_state = px.bar(
    state_current.head(15),
    x="state",
    y="premium",
    title=f"Top States by Written Premium — {selected_year}"
)

fig_state.update_xaxes(
    title=""
)

fig_state.update_yaxes(
    title="Premium (MXN)"
)

st.plotly_chart(
    fig_state,
    use_container_width=True
)


st.divider()

st.caption(
    "Premium represents written premium grouped by policy inception year. "
    "YoY Growth compares the selected year with the previous inception year. "
    "Unknown industries are retained to preserve transparency regarding "
    "unresolved industry classifications."
)
