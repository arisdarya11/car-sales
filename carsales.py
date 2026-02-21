import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight · Car Sales Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Luxury Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --navy:     #0B1622;
    --navy2:    #111E2D;
    --card:     #14243A;
    --border:   #1E3250;
    --teal:     #0EA5C9;
    --teal2:    #06B6D4;
    --gold:     #F59E0B;
    --coral:    #F97316;
    --mint:     #10B981;
    --rose:     #F43F5E;
    --text:     #E2E8F0;
    --muted:    #64748B;
    --white:    #FFFFFF;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy) !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--navy) !important; }

/* ── Hide default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--navy2) !important;
    border-right: 1px solid var(--border);
    padding-top: 1rem;
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'DM Serif Display', serif;
    color: var(--teal) !important;
    font-size: 1.1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, #0B1622 0%, #0A2540 50%, #0B1622 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(14,165,201,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 200px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(245,158,11,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: var(--white);
    margin: 0;
    line-height: 1.15;
}
.hero-title span { color: var(--teal); }
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    margin: 0.5rem 0 0;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(14,165,201,0.15);
    border: 1px solid rgba(14,165,201,0.3);
    color: var(--teal);
    padding: 0.25rem 0.85rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.8rem;
}
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.teal::before  { background: linear-gradient(90deg, var(--teal), var(--teal2)); }
.kpi-card.gold::before  { background: linear-gradient(90deg, var(--gold), var(--coral)); }
.kpi-card.mint::before  { background: linear-gradient(90deg, var(--mint), #34D399); }
.kpi-card.rose::before  { background: linear-gradient(90deg, var(--rose), #FB7185); }
.kpi-label {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    color: var(--white);
    line-height: 1;
    margin-bottom: 0.35rem;
}
.kpi-delta {
    font-size: 0.78rem;
    color: var(--muted);
}
.kpi-delta .up   { color: var(--mint); }
.kpi-delta .down { color: var(--rose); }

/* ── Section Titles ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: var(--white);
    margin: 0 0 0.25rem;
}
.section-sub {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.2rem;
}

/* ── Chart Cards ── */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
}

/* ── Insight Pills ── */
.insight-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(14,165,201,0.1);
    border: 1px solid rgba(14,165,201,0.2);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.82rem;
    color: var(--text);
    margin: 0.3rem 0.3rem 0.3rem 0;
    line-height: 1.4;
}
.insight-pill .icon { font-size: 1rem; }
.insight-pill strong { color: var(--teal); }

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--navy2);
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 1.2rem;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: var(--white) !important;
}

/* ── Filters ── */
.stSelectbox label, .stMultiSelect label, .stSlider label { color: var(--muted) !important; font-size: 0.8rem !important; font-weight: 600 !important; letter-spacing: 0.05em; }
div[data-baseweb="select"] > div { background: var(--card) !important; border-color: var(--border) !important; border-radius: 8px !important; color: var(--text) !important; }
.stSlider .stSlider > div { color: var(--text) !important; }

/* ── Metric overrides ── */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* ── Table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.8rem 0;
}

/* ── Rank badge ── */
.rank-badge {
    display: inline-block;
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--teal);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    text-align: center;
    line-height: 24px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_car_sales_data.csv")
    df["Latest_Launch"] = pd.to_datetime(df["Latest_Launch"], errors="coerce")
    df["Launch_Year"]   = df["Latest_Launch"].dt.year
    df["Launch_Month"]  = df["Latest_Launch"].dt.month
    df["Resale_Ratio"]  = (df["__year_resale_value"] / df["Price_in_thousands"]).round(3)
    df["Price_Segment"] = pd.cut(
        df["Price_in_thousands"],
        bins=[0, 15, 25, 35, 60],
        labels=["Economy (<$15K)", "Mid-Range ($15-25K)", "Premium ($25-35K)", "Luxury ($35K+)"]
    )
    df["HP_Category"] = pd.cut(
        df["Horsepower"],
        bins=[0, 130, 180, 230, 400],
        labels=["Low (<130)", "Mid (130-180)", "High (180-230)", "Sport (230+)"]
    )
    return df

df_raw = load_data()

# ─────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-family: DM Serif Display, serif; font-size: 1.5rem; color: #0EA5C9;'>🚗 AutoInsight</div>
        <div style='font-size: 0.72rem; color: #64748B; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem;'>Car Sales Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🎛️ Filters")

    all_manufacturers = sorted(df_raw["Manufacturer"].unique())
    selected_mfr = st.multiselect(
        "MANUFACTURER",
        options=all_manufacturers,
        default=all_manufacturers,
        placeholder="Select manufacturers..."
    )

    all_types = sorted(df_raw["Vehicle_type"].unique())
    selected_type = st.multiselect(
        "VEHICLE TYPE",
        options=all_types,
        default=all_types,
    )

    price_min, price_max = float(df_raw["Price_in_thousands"].min()), float(df_raw["Price_in_thousands"].max())
    price_range = st.slider(
        "PRICE RANGE ($K)",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
        step=0.5,
    )

    hp_min, hp_max = float(df_raw["Horsepower"].min()), float(df_raw["Horsepower"].max())
    hp_range = st.slider(
        "HORSEPOWER",
        min_value=hp_min,
        max_value=hp_max,
        value=(hp_min, hp_max),
        step=5.0,
    )

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#64748B; text-align:center; line-height:1.8;'>
        📊 Dataset: Cleaned Car Sales<br>
        🗂️ 157 Models · 30 Manufacturers<br>
        🛠️ Built with Streamlit + Plotly<br>
        <span style='color:#0EA5C9;'>Aris Darya Fernanda</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
df = df_raw.copy()
if selected_mfr:
    df = df[df["Manufacturer"].isin(selected_mfr)]
if selected_type:
    df = df[df["Vehicle_type"].isin(selected_type)]
df = df[
    (df["Price_in_thousands"] >= price_range[0]) &
    (df["Price_in_thousands"] <= price_range[1]) &
    (df["Horsepower"] >= hp_range[0]) &
    (df["Horsepower"] <= hp_range[1])
]

n_filtered  = len(df)
n_total     = len(df_raw)
pct_showing = round(n_filtered / n_total * 100, 1) if n_total > 0 else 0

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT_CLR  = "#94A3B8"
GRID_CLR  = "rgba(30,50,80,0.6)"
TEAL      = "#0EA5C9"
GOLD      = "#F59E0B"
CORAL     = "#F97316"
MINT      = "#10B981"
ROSE      = "#F43F5E"
PURPLE    = "#8B5CF6"

PALETTE = [TEAL, GOLD, CORAL, MINT, ROSE, PURPLE,
           "#06B6D4", "#FBBF24", "#FB923C", "#34D399",
           "#FB7185", "#A78BFA", "#38BDF8", "#FCD34D"]

def base_layout(**kwargs):
    # Pop overridable defaults to prevent duplicate-key errors when
    # callers pass the same key both inside base_layout() AND to update_layout().
    margin = kwargs.pop("margin", dict(l=10, r=10, t=40, b=10))
    legend = kwargs.pop("legend", dict(
        bgcolor="rgba(14,36,58,0.8)",
        bordercolor=GRID_CLR,
        borderwidth=1,
        font=dict(size=11),
    ))
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color=FONT_CLR, size=12),
        margin=margin,
        legend=legend,
        **kwargs
    )

def style_axes(fig, showgrid_x=True, showgrid_y=True):
    fig.update_xaxes(
        gridcolor=GRID_CLR, gridwidth=0.5,
        showgrid=showgrid_x, zeroline=False,
        tickfont=dict(color=FONT_CLR, size=11),
        linecolor=GRID_CLR,
    )
    fig.update_yaxes(
        gridcolor=GRID_CLR, gridwidth=0.5,
        showgrid=showgrid_y, zeroline=False,
        tickfont=dict(color=FONT_CLR, size=11),
        linecolor=GRID_CLR,
    )
    return fig

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
    <div class="hero-badge">📊 Data Analytics Portfolio</div>
    <h1 class="hero-title">Auto<span>Insight</span> Dashboard</h1>
    <p class="hero-sub">Interactive Intelligence Platform · Car Sales & Market Analysis · {n_filtered} of {n_total} models displayed ({pct_showing}%)</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
total_sales    = df["Sales_in_thousands"].sum()
avg_price      = df["Price_in_thousands"].mean()
avg_hp         = df["Horsepower"].mean()
avg_efficiency = df["Fuel_efficiency"].mean()
avg_resale     = df["Resale_Ratio"].mean()

# Compare to full dataset
delta_sales = ((total_sales - df_raw["Sales_in_thousands"].sum()) / df_raw["Sales_in_thousands"].sum() * 100)
delta_price = avg_price - df_raw["Price_in_thousands"].mean()

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card teal">
        <div class="kpi-label">Total Sales Volume</div>
        <div class="kpi-value">{total_sales/1000:,.1f}M</div>
        <div class="kpi-delta">units sold across <strong style='color:#E2E8F0'>{df['Manufacturer'].nunique()}</strong> brands</div>
    </div>
    <div class="kpi-card gold">
        <div class="kpi-label">Avg. Sticker Price</div>
        <div class="kpi-value">${avg_price:,.1f}K</div>
        <div class="kpi-delta"><span class="{'up' if delta_price >= 0 else 'down'}">{'▲' if delta_price >= 0 else '▼'} ${abs(delta_price):.1f}K</span> vs all models</div>
    </div>
    <div class="kpi-card mint">
        <div class="kpi-label">Avg. Horsepower</div>
        <div class="kpi-value">{avg_hp:,.0f} hp</div>
        <div class="kpi-delta">across <strong style='color:#E2E8F0'>{n_filtered}</strong> filtered models</div>
    </div>
    <div class="kpi-card rose">
        <div class="kpi-label">Avg. Fuel Efficiency</div>
        <div class="kpi-value">{avg_efficiency:.1f} mpg</div>
        <div class="kpi-delta">resale ratio avg: <strong style='color:#E2E8F0'>{avg_resale:.2f}x</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Market Overview",
    "🔍 Model Explorer",
    "⚡ Performance Analysis",
    "💰 Price & Value",
    "📋 Data Table",
])

# ══════════════════════════════════════════════
# TAB 1 — MARKET OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<p class="section-title">Top Manufacturers by Sales Volume</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Total units sold (thousands) — ranked & color-coded by performance tier</p>', unsafe_allow_html=True)

        mfr_sales = (
            df.groupby("Manufacturer")["Sales_in_thousands"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        mfr_sales["rank"] = range(len(mfr_sales), 0, -1)

        fig_mfr = go.Figure()
        colors = [TEAL if v >= mfr_sales["Sales_in_thousands"].quantile(0.75)
                  else (GOLD if v >= mfr_sales["Sales_in_thousands"].median()
                  else FONT_CLR)
                  for v in mfr_sales["Sales_in_thousands"]]

        fig_mfr.add_trace(go.Bar(
            x=mfr_sales["Sales_in_thousands"],
            y=mfr_sales["Manufacturer"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"  {v:,.0f}K" for v in mfr_sales["Sales_in_thousands"]],
            textposition="outside",
            textfont=dict(size=10, color=FONT_CLR),
            hovertemplate="<b>%{y}</b><br>Sales: %{x:,.0f}K units<extra></extra>",
        ))
        fig_mfr.update_layout(
            **base_layout(height=460, title=None),
            xaxis_title="Sales (thousands)",
            yaxis_title=None,
            showlegend=False,
        )
        style_axes(fig_mfr, showgrid_x=True, showgrid_y=False)
        st.plotly_chart(fig_mfr, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Market Share by Price Segment</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Volume distribution across price tiers</p>', unsafe_allow_html=True)

        seg_sales = df.groupby("Price_Segment", observed=True)["Sales_in_thousands"].sum().reset_index()
        seg_sales.columns = ["Segment", "Sales"]

        fig_donut = go.Figure(go.Pie(
            labels=seg_sales["Segment"],
            values=seg_sales["Sales"],
            hole=0.62,
            marker=dict(colors=[TEAL, GOLD, CORAL, ROSE], line=dict(color="rgba(0,0,0,0)", width=0)),
            textinfo="label+percent",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f}K units<br>%{percent}<extra></extra>",
            sort=False,
        ))
        fig_donut.add_annotation(
            text=f"<b style='font-size:18px'>{seg_sales['Sales'].sum()/1000:,.1f}M</b><br><span style='font-size:11px; color:{FONT_CLR}'>Total Units</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#E2E8F0", size=14),
            align="center",
        )
        fig_donut.update_layout(**base_layout(height=240, title=None, margin=dict(t=10, b=10, l=10, r=10)), showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown('<p class="section-title" style="margin-top:0.5rem">Vehicle Type Mix</p>', unsafe_allow_html=True)
        type_sales = df.groupby("Vehicle_type")["Sales_in_thousands"].sum().reset_index()
        fig_type = go.Figure(go.Pie(
            labels=type_sales["Vehicle_type"],
            values=type_sales["Sales_in_thousands"],
            hole=0.55,
            marker=dict(colors=[TEAL, MINT]),
            textinfo="label+percent",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f}K units<extra></extra>",
        ))
        fig_type.update_layout(**base_layout(height=175, title=None, margin=dict(t=5, b=5, l=10, r=10)), showlegend=False)
        st.plotly_chart(fig_type, use_container_width=True)

    # ── Row 2: Sales vs Price Scatter + Monthly Launch
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    col3, col4 = st.columns([3, 2])

    with col3:
        st.markdown('<p class="section-title">Sales Volume vs. Price — Bubble Map</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Bubble size = Horsepower · Color = Manufacturer · Hover for full detail</p>', unsafe_allow_html=True)

        fig_bubble = px.scatter(
            df,
            x="Price_in_thousands",
            y="Sales_in_thousands",
            size="Horsepower",
            color="Manufacturer",
            hover_name="Model",
            hover_data={"Manufacturer": True, "Price_in_thousands": ":.1f",
                        "Sales_in_thousands": ":.1f", "Horsepower": ":.0f",
                        "Fuel_efficiency": ":.1f"},
            color_discrete_sequence=PALETTE,
            size_max=28,
            labels={
                "Price_in_thousands": "Price ($K)",
                "Sales_in_thousands": "Sales (K units)",
                "Horsepower": "HP",
            },
        )
        fig_bubble.update_traces(
            marker=dict(opacity=0.75, line=dict(width=0.5, color="rgba(255,255,255,0.2)")),
        )
        fig_bubble.update_layout(**base_layout(height=380))
        style_axes(fig_bubble)
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col4:
        st.markdown('<p class="section-title">Launch Activity by Year</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Model launches and cumulative sales</p>', unsafe_allow_html=True)

        year_df = df.groupby("Launch_Year").agg(
            Models=("Model", "count"),
            Sales=("Sales_in_thousands", "sum")
        ).reset_index().dropna()

        fig_year = make_subplots(specs=[[{"secondary_y": True}]])
        fig_year.add_trace(go.Bar(
            x=year_df["Launch_Year"], y=year_df["Models"],
            name="# Models", marker_color=TEAL, opacity=0.7,
            hovertemplate="%{x}: %{y} models<extra></extra>",
        ), secondary_y=False)
        fig_year.add_trace(go.Scatter(
            x=year_df["Launch_Year"], y=year_df["Sales"],
            name="Sales (K)", line=dict(color=GOLD, width=2.5),
            mode="lines+markers",
            marker=dict(size=6, color=GOLD),
            hovertemplate="%{x}: %{y:,.0f}K units<extra></extra>",
        ), secondary_y=True)
        fig_year.update_layout(
            **base_layout(height=380, legend=dict(x=0.02, y=0.98, font=dict(size=10))),
        )
        fig_year.update_yaxes(gridcolor=GRID_CLR, zeroline=False, tickfont=dict(color=FONT_CLR, size=11))
        fig_year.update_xaxes(gridcolor=GRID_CLR, zeroline=False, tickfont=dict(color=FONT_CLR, size=11))
        st.plotly_chart(fig_year, use_container_width=True)

    # ── Key Insights
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📌 Auto-Generated Insights</p>', unsafe_allow_html=True)

    top_mfr    = df.groupby("Manufacturer")["Sales_in_thousands"].sum().idxmax()
    top_model  = df.loc[df["Sales_in_thousands"].idxmax(), "Model"]
    top_sales  = df["Sales_in_thousands"].max()
    neg_corr   = round(df["Sales_in_thousands"].corr(df["Price_in_thousands"]), 3)
    best_mpg   = df.loc[df["Fuel_efficiency"].idxmax()]
    top_seg    = seg_sales.loc[seg_sales["Sales"].idxmax(), "Segment"]

    st.markdown(f"""
    <div style='display:flex; flex-wrap:wrap; gap:0.3rem; margin-top:0.5rem;'>
        <div class='insight-pill'><span class='icon'>🏆</span><span><strong>{top_mfr}</strong> leads with the highest total sales volume in the current filter.</span></div>
        <div class='insight-pill'><span class='icon'>⭐</span><span>Best-selling single model: <strong>{top_model}</strong> with <strong>{top_sales:,.1f}K units</strong>.</span></div>
        <div class='insight-pill'><span class='icon'>📉</span><span>Price vs Sales correlation: <strong>{neg_corr}</strong> — higher-priced cars sell significantly fewer units.</span></div>
        <div class='insight-pill'><span class='icon'>🌿</span><span>Most fuel-efficient model: <strong>{best_mpg['Model']}</strong> ({best_mpg['Manufacturer']}) at <strong>{best_mpg['Fuel_efficiency']:.1f} mpg</strong>.</span></div>
        <div class='insight-pill'><span class='icon'>💼</span><span>Dominant segment by volume: <strong>{top_seg}</strong> — where mass-market demand is concentrated.</span></div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — MODEL EXPLORER
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">🔍 Interactive Model Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Drill down into individual models — compare specs, rank by any metric</p>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 3])
    with col_l:
        x_metric = st.selectbox("X-AXIS METRIC", [
            "Price_in_thousands", "Horsepower", "Fuel_efficiency",
            "Engine_size", "Curb_weight", "Power_perf_factor"
        ], index=0, format_func=lambda x: x.replace("_", " ").title())

        y_metric = st.selectbox("Y-AXIS METRIC", [
            "Sales_in_thousands", "Horsepower", "__year_resale_value",
            "Fuel_efficiency", "Power_perf_factor", "Resale_Ratio"
        ], index=0, format_func=lambda x: x.replace("_", " ").replace("__", "").title())

        color_by = st.selectbox("COLOR BY", ["Manufacturer", "Vehicle_type", "Price_Segment", "HP_Category"])
        show_trendline = st.checkbox("Show Trendline", value=True)

    with col_r:
        fig_exp = px.scatter(
            df,
            x=x_metric,
            y=y_metric,
            color=color_by,
            hover_name="Model",
            hover_data={"Manufacturer": True, "Price_in_thousands": ":.1f",
                        "Sales_in_thousands": ":.1f", "Horsepower": ":.0f"},
            color_discrete_sequence=PALETTE,
            trendline="ols" if show_trendline else None,
            labels={
                x_metric: x_metric.replace("_", " ").replace("__", "").title(),
                y_metric: y_metric.replace("_", " ").replace("__", "").title(),
            },
            size_max=12,
        )
        fig_exp.update_traces(
            selector=dict(mode="markers"),
            marker=dict(size=9, opacity=0.8, line=dict(width=0.5, color="rgba(255,255,255,0.2)")),
        )
        fig_exp.update_layout(**base_layout(height=430))
        style_axes(fig_exp)
        st.plotly_chart(fig_exp, use_container_width=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Top / Bottom 10 Rankings
    col_rank1, col_rank2 = st.columns(2)

    with col_rank1:
        st.markdown('<p class="section-title">🥇 Top 10 — Sales Champions</p>', unsafe_allow_html=True)
        top10 = (df.nlargest(10, "Sales_in_thousands")
                 [["Manufacturer","Model","Sales_in_thousands","Price_in_thousands","Horsepower"]]
                 .reset_index(drop=True))
        top10.index += 1
        top10.columns = ["Brand", "Model", "Sales (K)", "Price ($K)", "HP"]
        top10["Sales (K)"] = top10["Sales (K)"].round(1)
        top10["Price ($K)"] = top10["Price ($K)"].round(1)
        top10["HP"] = top10["HP"].round(0).astype(int)

        fig_top = go.Figure(go.Bar(
            x=top10["Sales (K)"][::-1],
            y=[f"{r}. {b} {m}" for r, b, m in zip(top10.index[::-1], top10["Brand"][::-1], top10["Model"][::-1])],
            orientation="h",
            marker=dict(
                color=top10["Sales (K)"][::-1],
                colorscale=[[0, "rgba(14,165,201,0.4)"], [1, TEAL]],
                showscale=False,
            ),
            text=[f"  {v:.1f}K" for v in top10["Sales (K)"][::-1]],
            textposition="outside", textfont=dict(size=10, color=FONT_CLR),
            hovertemplate="<b>%{y}</b><br>Sales: %{x:.1f}K<extra></extra>",
        ))
        fig_top.update_layout(**base_layout(height=320, margin=dict(l=120, r=40, t=15, b=10)), showlegend=False)
        style_axes(fig_top, showgrid_y=False)
        st.plotly_chart(fig_top, use_container_width=True)

    with col_rank2:
        st.markdown('<p class="section-title">💡 Top 10 — Most Powerful</p>', unsafe_allow_html=True)
        top10_hp = (df.nlargest(10, "Horsepower")
                    [["Manufacturer","Model","Horsepower","Price_in_thousands","Sales_in_thousands"]]
                    .reset_index(drop=True))

        fig_hp = go.Figure(go.Bar(
            x=top10_hp["Horsepower"][::-1],
            y=[f"{b} {m}" for b, m in zip(top10_hp["Manufacturer"][::-1], top10_hp["Model"][::-1])],
            orientation="h",
            marker=dict(
                color=top10_hp["Horsepower"][::-1],
                colorscale=[[0, "rgba(249,115,22,0.4)"], [1, CORAL]],
                showscale=False,
            ),
            text=[f"  {v:.0f} hp" for v in top10_hp["Horsepower"][::-1]],
            textposition="outside", textfont=dict(size=10, color=FONT_CLR),
            hovertemplate="<b>%{y}</b><br>HP: %{x:.0f}<extra></extra>",
        ))
        fig_hp.update_layout(**base_layout(height=320, margin=dict(l=120, r=40, t=15, b=10)), showlegend=False)
        style_axes(fig_hp, showgrid_y=False)
        st.plotly_chart(fig_hp, use_container_width=True)

    # Manufacturer deep-dive
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">🏭 Manufacturer Deep-Dive</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Select a manufacturer to explore their full model lineup</p>', unsafe_allow_html=True)

    sel_mfr = st.selectbox("SELECT MANUFACTURER", sorted(df["Manufacturer"].unique()), label_visibility="collapsed")
    mfr_df  = df[df["Manufacturer"] == sel_mfr].sort_values("Sales_in_thousands", ascending=False)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Models in Lineup", len(mfr_df))
    m2.metric("Total Sales (K)", f"{mfr_df['Sales_in_thousands'].sum():,.1f}")
    m3.metric("Avg Price ($K)", f"{mfr_df['Price_in_thousands'].mean():.1f}")
    m4.metric("Avg Horsepower", f"{mfr_df['Horsepower'].mean():.0f} hp")

    fig_mfr_detail = px.bar(
        mfr_df,
        x="Model",
        y="Sales_in_thousands",
        color="Price_Segment",
        color_discrete_map={
            "Economy (<$15K)": TEAL,
            "Mid-Range ($15-25K)": GOLD,
            "Premium ($25-35K)": CORAL,
            "Luxury ($35K+)": ROSE,
        },
        hover_data={"Price_in_thousands":":.1f", "Horsepower":":.0f",
                    "Fuel_efficiency":":.1f", "Sales_in_thousands":":.1f"},
        labels={"Sales_in_thousands": "Sales (K)", "Model": ""},
    )
    fig_mfr_detail.update_layout(**base_layout(height=280), title=None)
    style_axes(fig_mfr_detail, showgrid_x=False)
    st.plotly_chart(fig_mfr_detail, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — PERFORMANCE ANALYSIS
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">⚡ Performance & Engineering Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Horsepower, engine specs, efficiency, and the performance-price tradeoff</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # HP Distribution by Segment
        fig_violin = go.Figure()
        segments = df["Price_Segment"].cat.categories
        colors_v  = [TEAL, GOLD, CORAL, ROSE]
        for seg, clr in zip(segments, colors_v):
            sub = df[df["Price_Segment"] == seg]["Horsepower"].dropna()
            if len(sub) > 0:
                fig_violin.add_trace(go.Violin(
                    y=sub, name=str(seg),
                    line_color=clr, fillcolor=clr.replace(")", ",0.15)").replace("#", "rgba(").replace("rgba(0", "rgba(0"),
                    meanline_visible=True, box_visible=True,
                    hovertemplate=f"<b>{seg}</b><br>HP: %{{y:.0f}}<extra></extra>",
                ))
        fig_violin.update_layout(
            **base_layout(height=360, title="Horsepower Distribution by Price Segment"),
            showlegend=True, violinmode="overlay",
        )
        style_axes(fig_violin, showgrid_x=False)
        st.plotly_chart(fig_violin, use_container_width=True)

    with col2:
        # Engine Size vs HP
        fig_eng = px.scatter(
            df.dropna(subset=["Engine_size","Horsepower"]),
            x="Engine_size", y="Horsepower",
            color="Price_Segment",
            size="Sales_in_thousands",
            hover_name="Model",
            hover_data={"Manufacturer": True, "Engine_size": ":.1f", "Horsepower": ":.0f"},
            color_discrete_map={
                "Economy (<$15K)": TEAL, "Mid-Range ($15-25K)": GOLD,
                "Premium ($25-35K)": CORAL, "Luxury ($35K+)": ROSE,
            },
            labels={"Engine_size": "Engine Size (L)", "Horsepower": "Horsepower"},
            title="Engine Size vs Horsepower",
            trendline="ols",
        )
        fig_eng.update_traces(
            selector=dict(mode="markers"),
            marker=dict(opacity=0.75, line=dict(width=0.5, color="rgba(255,255,255,0.15)"))
        )
        fig_eng.update_layout(**base_layout(height=360))
        style_axes(fig_eng)
        st.plotly_chart(fig_eng, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Fuel Efficiency vs HP colored by price segment
        fig_eff = px.scatter(
            df,
            x="Horsepower", y="Fuel_efficiency",
            color="Manufacturer",
            hover_name="Model",
            color_discrete_sequence=PALETTE,
            labels={"Horsepower": "Horsepower", "Fuel_efficiency": "Fuel Efficiency (mpg)"},
            title="Horsepower vs Fuel Efficiency",
            trendline="lowess",
        )
        fig_eff.update_traces(
            selector=dict(mode="markers"),
            marker=dict(size=8, opacity=0.75, line=dict(width=0.4, color="rgba(255,255,255,0.1)"))
        )
        fig_eff.update_layout(**base_layout(height=340))
        style_axes(fig_eff)
        st.plotly_chart(fig_eff, use_container_width=True)

    with col4:
        # Power-Performance-Factor Ranking — Top 15
        ppf_top = df.nlargest(15, "Power_perf_factor")[["Manufacturer","Model","Power_perf_factor","Price_in_thousands"]].reset_index(drop=True)
        fig_ppf = px.bar(
            ppf_top.sort_values("Power_perf_factor"),
            x="Power_perf_factor",
            y=ppf_top.sort_values("Power_perf_factor").apply(lambda r: f"{r['Manufacturer']} {r['Model']}", axis=1),
            orientation="h",
            color="Price_in_thousands",
            color_continuous_scale=[[0, TEAL], [0.5, GOLD], [1, ROSE]],
            labels={"Power_perf_factor": "Power-Perf Factor", "color": "Price ($K)"},
            title="Top 15 by Power-Performance Factor",
        )
        fig_ppf.update_coloraxes(colorbar=dict(
            thickness=10, len=0.7,
            tickfont=dict(color=FONT_CLR, size=10),
            title=dict(text="Price $K", font=dict(color=FONT_CLR, size=10))
        ))
        fig_ppf.update_layout(**base_layout(height=340, margin=dict(l=140, r=20, t=40, b=10)))
        style_axes(fig_ppf, showgrid_y=False)
        st.plotly_chart(fig_ppf, use_container_width=True)

    # Correlation Heatmap
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">🧮 Correlation Matrix</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Pearson correlations between all numeric features — darker = stronger relationship</p>', unsafe_allow_html=True)

    num_cols = ["Sales_in_thousands","Price_in_thousands","Engine_size","Horsepower",
                "Wheelbase","Width","Length","Curb_weight","Fuel_capacity",
                "Fuel_efficiency","Power_perf_factor","Resale_Ratio"]
    corr_df  = df[num_cols].corr().round(2)
    labels_clean = [c.replace("_in_thousands","").replace("_"," ").title() for c in num_cols]

    fig_heat = go.Figure(go.Heatmap(
        z=corr_df.values,
        x=labels_clean,
        y=labels_clean,
        colorscale=[[0, "#F43F5E"], [0.5, "#0B1622"], [1, "#0EA5C9"]],
        zmid=0,
        text=corr_df.values,
        texttemplate="%{text:.2f}",
        textfont=dict(size=9, color="#E2E8F0"),
        hovertemplate="<b>%{y} × %{x}</b><br>Correlation: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=12, len=0.8,
            tickfont=dict(color=FONT_CLR, size=10),
        ),
    ))
    fig_heat.update_layout(**base_layout(height=420, margin=dict(l=10, r=10, t=10, b=10)))
    fig_heat.update_xaxes(tickangle=-35, tickfont=dict(size=10, color=FONT_CLR))
    fig_heat.update_yaxes(tickfont=dict(size=10, color=FONT_CLR))
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 4 — PRICE & VALUE
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">💰 Price Intelligence & Resale Value</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Where does the money go? Analyze pricing dynamics, depreciation, and value retention</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        # Price vs Resale Ratio scatter
        fig_resale = px.scatter(
            df,
            x="Price_in_thousands",
            y="__year_resale_value",
            color="Manufacturer",
            size="Sales_in_thousands",
            hover_name="Model",
            hover_data={
                "Manufacturer": True,
                "Price_in_thousands": ":.1f",
                "__year_resale_value": ":.2f",
                "Resale_Ratio": ":.2f",
                "Sales_in_thousands": ":.1f"
            },
            color_discrete_sequence=PALETTE,
            labels={
                "Price_in_thousands": "Original Price ($K)",
                "__year_resale_value": "Resale Value ($K)",
            },
            title="Price vs. Resale Value (bubble = sales volume)",
            trendline="ols",
        )
        # Add reference line (resale = price)
        max_p = df["Price_in_thousands"].max()
        fig_resale.add_trace(go.Scatter(
            x=[0, max_p], y=[0, max_p],
            mode="lines",
            line=dict(dash="dot", color=FONT_CLR, width=1),
            name="Resale = Price",
            showlegend=True,
        ))
        fig_resale.update_traces(
            selector=dict(mode="markers"),
            marker=dict(opacity=0.75, line=dict(width=0.5, color="rgba(255,255,255,0.15)"))
        )
        fig_resale.update_layout(**base_layout(height=400))
        style_axes(fig_resale)
        st.plotly_chart(fig_resale, use_container_width=True)

    with col2:
        # Best Resale Ratio Top 10
        st.markdown('<p class="section-title" style="font-size:1.1rem">🔝 Best Value Retention</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Resale / Original Price ratio</p>', unsafe_allow_html=True)

        top_resale = df.nlargest(10, "Resale_Ratio")[["Manufacturer","Model","Resale_Ratio","Price_in_thousands"]].reset_index(drop=True)
        top_resale.index += 1

        for _, row in top_resale.iterrows():
            pct = row["Resale_Ratio"] * 100
            color = MINT if pct >= 70 else (GOLD if pct >= 55 else FONT_CLR)
            st.markdown(f"""
            <div style='display:flex; align-items:center; justify-content:space-between;
                        padding: 0.5rem 0.75rem; margin-bottom: 0.4rem;
                        background: rgba(20,36,58,0.8); border: 1px solid {GRID_CLR};
                        border-radius: 8px;'>
                <div>
                    <div style='font-size:0.85rem; color:#E2E8F0; font-weight:500'>{row['Manufacturer']} {row['Model']}</div>
                    <div style='font-size:0.72rem; color:{FONT_CLR}'>Orig. ${row['Price_in_thousands']:.1f}K</div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:1.0rem; font-weight:700; color:{color}'>{pct:.1f}%</div>
                    <div style='font-size:0.7rem; color:{FONT_CLR}'>retained</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Row 2
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        # Price by Manufacturer — Box Plot
        fig_box = go.Figure()
        mfrs_sorted = df.groupby("Manufacturer")["Price_in_thousands"].median().sort_values(ascending=False).index[:16]
        for i, mfr in enumerate(mfrs_sorted):
            sub = df[df["Manufacturer"] == mfr]["Price_in_thousands"]
            fig_box.add_trace(go.Box(
                y=sub, name=mfr,
                marker_color=PALETTE[i % len(PALETTE)],
                line_color=PALETTE[i % len(PALETTE)],
                fillcolor=f"rgba({int(PALETTE[i % len(PALETTE)][1:3],16)},{int(PALETTE[i % len(PALETTE)][3:5],16)},{int(PALETTE[i % len(PALETTE)][5:7],16)},0.2)",
                boxmean="sd",
                hovertemplate=f"<b>{mfr}</b><br>Price: %{{y:.1f}}K<extra></extra>",
            ))
        fig_box.update_layout(
            **base_layout(height=380, title="Price Range by Manufacturer (Top 16)"),
            showlegend=False,
            xaxis=dict(tickangle=-35, tickfont=dict(size=9, color=FONT_CLR)),
        )
        style_axes(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    with col4:
        # Average price per segment + avg resale
        seg_stats = df.groupby("Price_Segment", observed=True).agg(
            Avg_Price=("Price_in_thousands", "mean"),
            Avg_Resale=("__year_resale_value", "mean"),
            Count=("Model", "count"),
        ).reset_index()

        fig_seg = go.Figure()
        fig_seg.add_trace(go.Bar(
            x=seg_stats["Price_Segment"].astype(str),
            y=seg_stats["Avg_Price"],
            name="Avg Original Price",
            marker_color=TEAL, opacity=0.85,
        ))
        fig_seg.add_trace(go.Bar(
            x=seg_stats["Price_Segment"].astype(str),
            y=seg_stats["Avg_Resale"],
            name="Avg Resale Value",
            marker_color=GOLD, opacity=0.85,
        ))
        fig_seg.update_layout(
            **base_layout(height=380, title="Original vs Resale Value by Segment"),
            barmode="group",
            xaxis=dict(tickangle=-10, tickfont=dict(size=10)),
        )
        style_axes(fig_seg, showgrid_x=False)
        st.plotly_chart(fig_seg, use_container_width=True)

    # ── Fuel efficiency vs Price segments
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    col5, col6 = st.columns([2, 3])

    with col5:
        st.markdown('<p class="section-title">⛽ Efficiency by Segment</p>', unsafe_allow_html=True)
        seg_eff = df.groupby("Price_Segment", observed=True)["Fuel_efficiency"].mean().reset_index()
        fig_eff2 = go.Figure(go.Bar(
            x=seg_eff["Fuel_efficiency"],
            y=seg_eff["Price_Segment"].astype(str),
            orientation="h",
            marker=dict(
                color=[TEAL, GOLD, CORAL, ROSE],
                line=dict(width=0),
            ),
            text=[f"  {v:.1f} mpg" for v in seg_eff["Fuel_efficiency"]],
            textposition="outside",
            textfont=dict(size=11, color=FONT_CLR),
            hovertemplate="<b>%{y}</b><br>Avg Efficiency: %{x:.1f} mpg<extra></extra>",
        ))
        fig_eff2.update_layout(**base_layout(height=250, title=None), showlegend=False)
        style_axes(fig_eff2, showgrid_y=False)
        st.plotly_chart(fig_eff2, use_container_width=True)

    with col6:
        st.markdown('<p class="section-title">🗓️ Price vs Launch Timeline</p>', unsafe_allow_html=True)
        fig_time = px.scatter(
            df.dropna(subset=["Launch_Year"]),
            x="Launch_Year", y="Price_in_thousands",
            color="Price_Segment",
            size="Sales_in_thousands",
            hover_name="Model",
            hover_data={"Manufacturer": True, "Price_in_thousands": ":.1f"},
            color_discrete_map={
                "Economy (<$15K)": TEAL, "Mid-Range ($15-25K)": GOLD,
                "Premium ($25-35K)": CORAL, "Luxury ($35K+)": ROSE,
            },
            labels={"Launch_Year": "Launch Year", "Price_in_thousands": "Price ($K)"},
        )
        fig_time.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color="rgba(255,255,255,0.15)")))
        fig_time.update_layout(**base_layout(height=250))
        style_axes(fig_time)
        st.plotly_chart(fig_time, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 5 — DATA TABLE
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">📋 Raw Data Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Full filtered dataset — searchable, sortable, downloadable</p>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        search_text = st.text_input("🔎 SEARCH MODEL OR BRAND", placeholder="e.g. Accord, Toyota, Mustang...")
    with col_s2:
        sort_col = st.selectbox("SORT BY", [
            "Sales_in_thousands", "Price_in_thousands", "Horsepower",
            "Fuel_efficiency", "Power_perf_factor", "Resale_Ratio"
        ], format_func=lambda x: x.replace("_", " ").replace("__", "").title())
    with col_s3:
        sort_dir = st.radio("ORDER", ["Descending ↓", "Ascending ↑"], horizontal=True)

    # Apply search
    display_df = df.copy()
    if search_text:
        mask = (
            display_df["Model"].str.contains(search_text, case=False, na=False) |
            display_df["Manufacturer"].str.contains(search_text, case=False, na=False)
        )
        display_df = display_df[mask]

    display_df = display_df.sort_values(sort_col, ascending=(sort_dir == "Ascending ↑"))

    # Nice column selection
    show_cols = ["Manufacturer","Model","Vehicle_type","Price_Segment",
                 "Sales_in_thousands","Price_in_thousands","Horsepower",
                 "Fuel_efficiency","Engine_size","Resale_Ratio","Power_perf_factor","Latest_Launch"]
    display_df_show = display_df[[c for c in show_cols if c in display_df.columns]].reset_index(drop=True)
    display_df_show.columns = [c.replace("_in_thousands","").replace("_"," ").replace("__","").title() for c in display_df_show.columns]

    st.markdown(f"<p style='color:{FONT_CLR}; font-size:0.8rem;'>Showing <strong style='color:#E2E8F0'>{len(display_df_show)}</strong> records</p>", unsafe_allow_html=True)
    st.dataframe(
        display_df_show,
        use_container_width=True,
        height=400,
    )

    # ── Download
    col_d1, col_d2 = st.columns([1, 3])
    with col_d1:
        csv_out = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=csv_out,
            file_name="filtered_car_sales.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── Summary Stats
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📊 Descriptive Statistics</p>', unsafe_allow_html=True)
    num_summary_cols = ["Sales_in_thousands","Price_in_thousands","Horsepower","Fuel_efficiency",
                         "Engine_size","Curb_weight","Power_perf_factor","Resale_Ratio"]
    stat_df = display_df[num_summary_cols].describe().round(2)
    stat_df.columns = [c.replace("_in_thousands","").replace("_"," ").title() for c in stat_df.columns]
    st.dataframe(stat_df, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='fancy-divider'></div>
<div style='text-align:center; padding: 1rem 0; color: #475569; font-size: 0.78rem; line-height: 2;'>
    <strong style='color:#0EA5C9; font-family: DM Serif Display, serif; font-size:1rem;'>AutoInsight</strong> · Car Sales Intelligence Dashboard<br>
    Built with <strong style='color:#E2E8F0;'>Streamlit</strong> + <strong style='color:#E2E8F0;'>Plotly</strong> · Dataset: 157 Models · 30 Manufacturers<br>
    <span style='color:#0EA5C9;'>Aris Darya Fernanda</span> · Data Analyst & Data Scientist Portfolio · 2025–2026
</div>
""", unsafe_allow_html=True)
