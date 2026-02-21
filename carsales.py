import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight · Car Sales Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────
BG       = "#F5F3EE"
SURFACE  = "#FFFFFF"
BORDER   = "#E5E0D8"
INK      = "#1A1714"
INK2     = "#6B6560"
ACCENT   = "#C8430A"
GREEN    = "#1A6B4A"
BLUE     = "#1A4A6B"
GOLD     = "#C8890A"
CHIP_BG  = "#F0EBE3"
GRID_CLR = "rgba(229,224,216,0.7)"

SEG_COLORS  = [BLUE, GOLD, ACCENT, GREEN]
MFR_PALETTE = [ACCENT, BLUE, GREEN, GOLD, "#6B1A4A", "#4A6B1A",
               "#1A6B6B", "#6B4A1A", "#4A1A6B", "#6B1A1A",
               "#C8430A", "#1A4A6B", "#1A6B4A", "#C8890A"]

def plot_layout(height=300, margin=None, **kw):
    m = margin or dict(l=8, r=8, t=32, b=8)
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color=INK2, size=11),
        height=height,
        margin=m,
        showlegend=kw.pop("showlegend", False),
        **kw,
    )

def style_axes(fig, x_title="", y_title="", show_xgrid=True, show_ygrid=True):
    fig.update_xaxes(
        title_text=x_title, title_font=dict(size=10, color=INK2),
        gridcolor=GRID_CLR, gridwidth=0.5, zeroline=False,
        tickfont=dict(size=10, color=INK2), linecolor=BORDER,
        showgrid=show_xgrid,
    )
    fig.update_yaxes(
        title_text=y_title, title_font=dict(size=10, color=INK2),
        gridcolor=GRID_CLR, gridwidth=0.5, zeroline=False,
        tickfont=dict(size=10, color=INK2), linecolor=BORDER,
        showgrid=show_ygrid,
    )
    return fig

def ols_line(x, y):
    arr_x, arr_y = np.array(x, float), np.array(y, float)
    mask = ~(np.isnan(arr_x) | np.isnan(arr_y))
    xc, yc = arr_x[mask], arr_y[mask]
    if len(xc) < 2:
        return [], []
    m, b = np.polyfit(xc, yc, 1)
    x_line = np.array([xc.min(), xc.max()])
    return x_line.tolist(), (m * x_line + b).tolist()

def hex_to_rgba(hex_color, alpha=1.0):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif !important;
    background-color: {BG} !important;
    color: {INK} !important;
}}
.stApp {{ background-color: {BG} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 2rem 3rem !important; max-width: 1400px; }}

section[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label {{
    font-size: 0.72rem !important;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {INK2} !important;
}}

.kpi-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(26,23,20,0.05), 0 4px 16px rgba(26,23,20,0.03);
    transition: box-shadow 0.2s;
}}
.kpi-card:hover {{ box-shadow: 0 4px 12px rgba(26,23,20,0.09), 0 12px 28px rgba(26,23,20,0.05); }}
.kpi-card::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 12px 12px;
}}
.kpi-card.accent::after  {{ background: {ACCENT}; }}
.kpi-card.green::after   {{ background: {GREEN}; }}
.kpi-card.blue::after    {{ background: {BLUE}; }}
.kpi-card.gold::after    {{ background: {GOLD}; }}
.kpi-label {{
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {INK2};
    margin-bottom: 6px;
}}
.kpi-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 500;
    color: {INK};
    line-height: 1;
    margin-bottom: 4px;
}}
.kpi-sub {{ font-size: 0.7rem; color: {INK2}; }}
.kpi-sub b {{ color: {INK}; font-weight: 600; }}

.insight-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem; }}
.insight-pill {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 9px 14px;
    font-size: 0.74rem;
    color: {INK2};
    flex: 1;
    min-width: 170px;
    line-height: 1.5;
    box-shadow: 0 1px 3px rgba(26,23,20,0.04);
}}
.insight-pill b {{ color: {INK}; }}
.insight-pill.accent {{ border-left: 3px solid {ACCENT}; }}
.insight-pill.green  {{ border-left: 3px solid {GREEN}; }}
.insight-pill.blue   {{ border-left: 3px solid {BLUE}; }}
.insight-pill.gold   {{ border-left: 3px solid {GOLD}; }}

.chart-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px 10px;
    box-shadow: 0 1px 3px rgba(26,23,20,0.05), 0 4px 16px rgba(26,23,20,0.03);
    margin-bottom: 14px;
    transition: box-shadow 0.2s;
}}
.chart-card:hover {{ box-shadow: 0 4px 12px rgba(26,23,20,0.09); }}
.chart-title {{
    font-size: 0.8rem;
    font-weight: 600;
    color: {INK};
    margin-bottom: 2px;
    letter-spacing: -0.01em;
}}
.chart-sub {{
    font-size: 0.68rem;
    color: {INK2};
    margin-bottom: 10px;
}}

.rank-row {{
    display: grid;
    grid-template-columns: 110px 1fr 55px;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 0.74rem;
}}
.rank-name {{ color: {INK}; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.rank-bar-bg {{ background: {CHIP_BG}; border-radius: 3px; height: 7px; overflow: hidden; }}
.rank-bar {{ height: 100%; border-radius: 3px; }}
.rank-val {{ font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: {INK2}; text-align: right; }}

.dash-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid {BORDER};
}}
.logo-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {ACCENT};
    margin-bottom: 3px;
}}
.logo-title {{
    font-size: 1.6rem;
    font-weight: 700;
    color: {INK};
    letter-spacing: -0.03em;
    line-height: 1;
}}
.logo-title span {{ color: {ACCENT}; }}
.logo-sub {{ font-size: 0.76rem; color: {INK2}; margin-top: 3px; }}
.hstats {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }}
.hstat-val {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    font-weight: 500;
    color: {INK};
}}
.hstat-label {{ font-size: 0.64rem; color: {INK2}; text-transform: uppercase; letter-spacing: 0.08em; }}

.stDataFrame {{ border-radius: 10px; overflow: hidden; }}

div[data-baseweb="select"] > div {{
    background: {SURFACE} !important;
    border-color: {BORDER} !important;
    border-radius: 8px !important;
}}

/* equal-height columns helper */
[data-testid="column"] > div > div > div > div {{
    height: 100%;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_car_sales_data.csv")
    df["Resale_Ratio"]  = df["__year_resale_value"] / df["Price_in_thousands"]
    df["Price_Segment"] = pd.cut(
        df["Price_in_thousands"],
        bins=[0, 15, 25, 35, 100],
        labels=["Economy", "Mid-Range", "Premium", "Luxury"],
    )
    df["Latest_Launch"] = pd.to_datetime(df["Latest_Launch"], errors="coerce")
    return df

df_raw = load_data()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; letter-spacing:0.14em; text-transform:uppercase; color:{ACCENT}; margin-bottom:4px;'>⬡ Portfolio Dashboard</div>
      <div style='font-size:1.3rem; font-weight:700; color:{INK}; letter-spacing:-0.03em;'>Auto<span style="color:{ACCENT}">Insight</span></div>
      <div style='font-size:0.7rem; color:{INK2}; margin-top:3px;'>Car Sales Intelligence</div>
    </div>
    <hr style='border:none; border-top:1px solid {BORDER}; margin-bottom:1rem;'>
    """, unsafe_allow_html=True)

    st.markdown("**SEGMENT**")
    seg_opts  = ["All"] + list(df_raw["Price_Segment"].cat.categories)
    sel_seg   = st.selectbox("", seg_opts, label_visibility="collapsed")

    st.markdown("**VEHICLE TYPE**")
    type_opts = ["All"] + sorted(df_raw["Vehicle_type"].unique())
    sel_type  = st.selectbox(" ", type_opts, label_visibility="collapsed")

    st.markdown("**MAX PRICE ($K)**")
    price_max = st.slider("", 9, 53, 53, label_visibility="collapsed")

    st.markdown("**MIN SALES (K UNITS)**")
    min_sales = st.slider(" ", 0, 150, 0, label_visibility="collapsed")

    st.markdown("**MANUFACTURER**")
    all_mfrs  = sorted(df_raw["Manufacturer"].unique())
    sel_mfrs  = st.multiselect("", all_mfrs, default=all_mfrs, label_visibility="collapsed")

    st.markdown(f"""
    <hr style='border:none; border-top:1px solid {BORDER}; margin-top:1rem;'>
    <div style='font-size:0.65rem; color:{INK2}; text-align:center; line-height:2; margin-top:0.8rem;'>
      📊 157 Models · 30 Manufacturers<br>
      🛠️ Streamlit + Plotly · Pure NumPy<br>
      <span style='color:{ACCENT}; font-family:JetBrains Mono,monospace;'>Aris Darya Fernanda</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_seg  != "All": df = df[df["Price_Segment"] == sel_seg]
if sel_type != "All": df = df[df["Vehicle_type"]  == sel_type]
if sel_mfrs:          df = df[df["Manufacturer"].isin(sel_mfrs)]
df = df[df["Price_in_thousands"] <= price_max]
df = df[df["Sales_in_thousands"] >= min_sales]

n       = len(df)
n_total = len(df_raw)

if n == 0:
    st.warning("⚠️ No data matches the current filters. Try relaxing your selections.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────
total_sales = df["Sales_in_thousands"].sum()
avg_price   = df["Price_in_thousands"].mean()
avg_hp      = df["Horsepower"].mean()
avg_mpg     = df["Fuel_efficiency"].mean()
avg_resale  = df["Resale_Ratio"].mean()
n_brands    = df["Manufacturer"].nunique()

top_brand   = df.groupby("Manufacturer")["Sales_in_thousands"].sum().idxmax()
top_model   = df.loc[df["Sales_in_thousands"].idxmax()]
best_mpg    = df.loc[df["Fuel_efficiency"].idxmax()]
most_hp     = df.loc[df["Horsepower"].idxmax()]

seg_color_map = {"Economy": BLUE, "Mid-Range": GOLD, "Premium": ACCENT, "Luxury": GREEN}

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div>
    <div class="logo-eyebrow">⬡ Portfolio Dashboard</div>
    <div class="logo-title">Auto<span>Insight</span></div>
    <div class="logo-sub">Car Sales Market Intelligence · {n} of {n_total} models · {n_brands} brands</div>
  </div>
  <div class="hstats">
    <div><div class="hstat-val">{total_sales/1000:.1f}M</div><div class="hstat-label">Total Units</div></div>
    <div><div class="hstat-val">${avg_price:.1f}K</div><div class="hstat-label">Avg. Price</div></div>
    <div><div class="hstat-val">{avg_hp:.0f} hp</div><div class="hstat-label">Avg. Power</div></div>
    <div><div class="hstat-val">{avg_mpg:.1f} mpg</div><div class="hstat-label">Avg. MPG</div></div>
    <div><div class="hstat-val">{avg_resale:.2f}x</div><div class="hstat-label">Avg. Resale</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, color_cls, label, value, sub):
    col.markdown(f"""
    <div class="kpi-card {color_cls}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(k1, "accent", "Total Sales Volume",   f"{total_sales/1000:.1f}M",  f"units · <b>{n}</b> models · <b>{n_brands}</b> brands")
kpi_card(k2, "green",  "Models Displayed",      str(n),                       f"of <b>{n_total}</b> total models")
kpi_card(k3, "blue",   "Avg. Sticker Price",    f"${avg_price:.1f}K",         f"avg HP: <b>{avg_hp:.0f}</b>")
kpi_card(k4, "gold",   "Avg. Fuel Efficiency",  f"{avg_mpg:.1f} mpg",         f"resale retention: <b>{avg_resale*100:.1f}%</b>")

st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# INSIGHT PILLS
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="insight-row">
  <div class="insight-pill accent">🏆 <b>Top Brand:</b> {top_brand} — {df.groupby("Manufacturer")["Sales_in_thousands"].sum()[top_brand]:,.0f}K units</div>
  <div class="insight-pill green">⭐ <b>Best Seller:</b> {top_model.Manufacturer} {top_model.Model} ({top_model.Sales_in_thousands:.1f}K)</div>
  <div class="insight-pill blue">🌿 <b>Best MPG:</b> {best_mpg.Manufacturer} {best_mpg.Model} at {best_mpg.Fuel_efficiency:.1f} mpg</div>
  <div class="insight-pill gold">⚡ <b>Most Powerful:</b> {most_hp.Manufacturer} {most_hp.Model} — {most_hp.Horsepower:.0f} hp</div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# ROW 1 — Brand bar (left) + Segment donut (right)
# ═════════════════════════════════════════════════════════════
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Sales by Manufacturer</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Total units sold (K) — top 12 by volume</div>', unsafe_allow_html=True)

    brand_df = (df.groupby("Manufacturer")["Sales_in_thousands"]
                .sum().sort_values().tail(12).reset_index())
    colors_bar = [MFR_PALETTE[i % len(MFR_PALETTE)] for i in range(len(brand_df))]

    fig_brand = go.Figure(go.Bar(
        x=brand_df["Sales_in_thousands"],
        y=brand_df["Manufacturer"],
        orientation="h",
        marker=dict(color=colors_bar, line=dict(width=0)),
        text=[f" {v:,.0f}K" for v in brand_df["Sales_in_thousands"]],
        textposition="outside",
        textfont=dict(size=10, color=INK2),
        hovertemplate="<b>%{y}</b><br>Sales: %{x:,.0f}K units<extra></extra>",
    ))
    fig_brand.update_layout(**plot_layout(height=360, margin=dict(l=8, r=55, t=10, b=8)))
    style_axes(fig_brand, show_xgrid=True, show_ygrid=False)
    st.plotly_chart(fig_brand, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Market by Segment</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Volume share across price tiers</div>', unsafe_allow_html=True)

    segs     = ["Economy", "Mid-Range", "Premium", "Luxury"]
    seg_vals = [df[df["Price_Segment"] == s]["Sales_in_thousands"].sum() for s in segs]
    total_seg = sum(seg_vals)

    fig_seg = go.Figure(go.Pie(
        labels=segs,
        values=seg_vals,
        hole=0.62,
        marker=dict(colors=SEG_COLORS, line=dict(color=SURFACE, width=3)),
        textinfo="label+percent",
        textfont=dict(size=11, color=INK),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}K units<br>%{percent}<extra></extra>",
        sort=False,
    ))
    fig_seg.add_annotation(
        text=f"<b>{total_seg/1000:.1f}M</b><br><span style='font-size:10px'>units</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=INK, size=14), align="center",
    )
    fig_seg.update_layout(
        **plot_layout(height=280, margin=dict(l=8, r=8, t=10, b=8), showlegend=True),
        legend=dict(orientation="v", x=1.02, y=0.5,
                    font=dict(size=10, color=INK2), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})

    # ── Avg Price per Segment mini bar (fills remaining space)
    seg_price = [df[df["Price_Segment"] == s]["Price_in_thousands"].mean() for s in segs]
    fig_sp = go.Figure(go.Bar(
        x=segs,
        y=seg_price,
        marker=dict(color=SEG_COLORS, line=dict(width=0)),
        text=[f"${v:.1f}K" for v in seg_price],
        textposition="outside",
        textfont=dict(size=9, color=INK2),
        hovertemplate="<b>%{x}</b><br>Avg Price: $%{y:.1f}K<extra></extra>",
    ))
    fig_sp.update_layout(**plot_layout(height=140, margin=dict(l=8, r=8, t=28, b=8)),
                         title=dict(text="Avg Price per Segment", font=dict(size=11, color=INK), x=0))
    style_axes(fig_sp, y_title="$K", show_xgrid=False)
    fig_sp.update_yaxes(range=[0, max(seg_price) * 1.3])
    st.plotly_chart(fig_sp, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# ROW 2 — Top Models (left) + Price vs Sales + HP vs MPG (right 2)
# ═════════════════════════════════════════════════════════════
c1, c2, c3 = st.columns(3)

# ── Top Models rank list
with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Top Models by Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Units (K) — top 10</div>', unsafe_allow_html=True)

    top10 = df.nlargest(10, "Sales_in_thousands")
    max_v = top10["Sales_in_thousands"].max()
    rank_colors = [ACCENT, BLUE, GREEN, GOLD, "#6B1A4A", "#4A6B1A", "#1A6B6B", "#6B4A1A", "#4A1A6B", "#6B1A1A"]

    bars_html = ""
    for i, (_, row) in enumerate(top10.iterrows()):
        pct = row["Sales_in_thousands"] / max_v * 100
        clr = rank_colors[i % len(rank_colors)]
        bars_html += f"""
        <div class="rank-row">
          <span class="rank-name" title="{row.Manufacturer} {row.Model}">
            {row.Manufacturer} <span style='color:{INK2};font-weight:400'>{row.Model}</span>
          </span>
          <div class="rank-bar-bg"><div class="rank-bar" style="width:{pct:.1f}%;background:{clr}"></div></div>
          <span class="rank-val">{row.Sales_in_thousands:.1f}</span>
        </div>"""
    st.markdown(bars_html, unsafe_allow_html=True)

    # ── Mini: Vehicle type sales donut
    vtype_sales = df.groupby("Vehicle_type")["Sales_in_thousands"].sum().reset_index()
    vtype_colors = [MFR_PALETTE[i % len(MFR_PALETTE)] for i in range(len(vtype_sales))]
    fig_vt = go.Figure(go.Pie(
        labels=vtype_sales["Vehicle_type"],
        values=vtype_sales["Sales_in_thousands"],
        hole=0.55,
        marker=dict(colors=vtype_colors, line=dict(color=SURFACE, width=2)),
        textinfo="label+percent",
        textfont=dict(size=9),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}K units<extra></extra>",
        sort=True,
    ))
    fig_vt.update_layout(
        **plot_layout(height=160, margin=dict(l=0, r=0, t=28, b=0), showlegend=False),
        title=dict(text="Sales by Vehicle Type", font=dict(size=11, color=INK), x=0),
    )
    st.plotly_chart(fig_vt, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Price vs Sales scatter
with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Price vs Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Bubble size = Horsepower · Color = Tier</div>', unsafe_allow_html=True)

    fig_scat = go.Figure()
    for seg, clr in seg_color_map.items():
        sub = df[df["Price_Segment"] == seg]
        if len(sub) == 0:
            continue
        fig_scat.add_trace(go.Scatter(
            x=sub["Price_in_thousands"],
            y=sub["Sales_in_thousands"],
            mode="markers",
            name=str(seg),
            marker=dict(
                size=np.sqrt(sub["Horsepower"]) * 0.85,
                color=hex_to_rgba(clr, 0.6),
                line=dict(color=clr, width=1),
            ),
            hovertemplate="<b>%{customdata[0]} %{customdata[1]}</b><br>Price: $%{x:.1f}K<br>Sales: %{y:.1f}K<extra></extra>",
            customdata=sub[["Manufacturer", "Model"]].values,
        ))
    xl, yl = ols_line(df["Price_in_thousands"], df["Sales_in_thousands"])
    if xl:
        fig_scat.add_trace(go.Scatter(
            x=xl, y=yl, mode="lines",
            line=dict(color=hex_to_rgba(ACCENT, 0.4), width=1.8, dash="dot"),
            showlegend=False, hoverinfo="skip",
        ))
    fig_scat.update_layout(
        **plot_layout(height=310, margin=dict(l=8, r=8, t=10, b=8), showlegend=True),
        legend=dict(orientation="h", x=0, y=1.08, font=dict(size=9, color=INK2), bgcolor="rgba(0,0,0,0)"),
    )
    style_axes(fig_scat, x_title="Price ($K)", y_title="Sales (K)")
    st.plotly_chart(fig_scat, use_container_width=True, config={"displayModeBar": False})

    # ── Mini: Engine size vs Curb weight
    fig_ew = go.Figure()
    for seg, clr in seg_color_map.items():
        sub = df[df["Price_Segment"] == seg]
        if len(sub) == 0:
            continue
        fig_ew.add_trace(go.Scatter(
            x=sub["Engine_size"],
            y=sub["Curb_weight"],
            mode="markers",
            name=str(seg),
            marker=dict(size=6, color=hex_to_rgba(clr, 0.6), line=dict(color=clr, width=0.7)),
            hovertemplate="<b>%{customdata[0]} %{customdata[1]}</b><br>Engine: %{x:.1f}L · Weight: %{y:.0f}kg<extra></extra>",
            customdata=sub[["Manufacturer", "Model"]].values,
        ))
    fig_ew.update_layout(
        **plot_layout(height=175, margin=dict(l=8, r=8, t=28, b=8), showlegend=False),
        title=dict(text="Engine Size vs Curb Weight", font=dict(size=11, color=INK), x=0),
    )
    style_axes(fig_ew, x_title="Engine (L)", y_title="Weight (kg)")
    st.plotly_chart(fig_ew, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── HP vs MPG
with c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Horsepower vs MPG</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Efficiency tradeoff · Dashed = trend</div>', unsafe_allow_html=True)

    fig_eff = go.Figure()
    for seg, clr in seg_color_map.items():
        sub = df[df["Price_Segment"] == seg]
        if len(sub) == 0:
            continue
        fig_eff.add_trace(go.Scatter(
            x=sub["Horsepower"],
            y=sub["Fuel_efficiency"],
            mode="markers",
            name=str(seg),
            marker=dict(size=7, color=hex_to_rgba(clr, 0.53), line=dict(color=clr, width=0.8)),
            hovertemplate="<b>%{customdata[0]} %{customdata[1]}</b><br>%{x:.0f} hp · %{y:.1f} mpg<extra></extra>",
            customdata=sub[["Manufacturer", "Model"]].values,
        ))
    xl, yl = ols_line(df["Horsepower"], df["Fuel_efficiency"])
    if xl:
        fig_eff.add_trace(go.Scatter(
            x=xl, y=yl, mode="lines",
            line=dict(color=hex_to_rgba(ACCENT, 0.4), width=1.8, dash="dot"),
            showlegend=False, hoverinfo="skip",
        ))
    fig_eff.update_layout(**plot_layout(height=310, margin=dict(l=8, r=8, t=10, b=8)))
    style_axes(fig_eff, x_title="Horsepower", y_title="MPG")
    st.plotly_chart(fig_eff, use_container_width=True, config={"displayModeBar": False})

    # ── Mini: Power Performance Factor by Segment box
    fig_ppf = go.Figure()
    for seg, clr in seg_color_map.items():
        sub = df[df["Price_Segment"] == seg]
        if len(sub) == 0:
            continue
        fig_ppf.add_trace(go.Box(
            y=sub["Power_perf_factor"],
            name=str(seg),
            marker_color=clr,
            line=dict(color=clr, width=1.5),
            fillcolor=hex_to_rgba(clr, 0.15),
            boxmean=True,
            hovertemplate="<b>%{x}</b><br>Perf: %{y:.1f}<extra></extra>",
        ))
    fig_ppf.update_layout(
        **plot_layout(height=175, margin=dict(l=8, r=8, t=28, b=8), showlegend=False),
        title=dict(text="Performance Factor by Tier", font=dict(size=11, color=INK), x=0),
    )
    style_axes(fig_ppf, y_title="Perf Factor", show_xgrid=False)
    st.plotly_chart(fig_ppf, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# ROW 3 — Resale + Correlation heatmap (full)
# ═════════════════════════════════════════════════════════════
r3a, r3b = st.columns([1, 2])

with r3a:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Best Resale Retention</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Resale value / original price — top 10</div>', unsafe_allow_html=True)

    top_resale = df.nlargest(10, "Resale_Ratio").sort_values("Resale_Ratio")
    bar_colors_r = [GREEN if v >= 0.7 else (GOLD if v >= 0.55 else ACCENT)
                    for v in top_resale["Resale_Ratio"]]

    fig_res = go.Figure(go.Bar(
        x=top_resale["Resale_Ratio"] * 100,
        y=top_resale.apply(lambda r: f"{r.Manufacturer} {r.Model}", axis=1),
        orientation="h",
        marker=dict(color=[hex_to_rgba(c, 0.8) for c in bar_colors_r], line=dict(width=0)),
        text=[f" {v*100:.1f}%" for v in top_resale["Resale_Ratio"]],
        textposition="outside",
        textfont=dict(size=9, color=INK2),
        hovertemplate="<b>%{y}</b><br>Retains %{x:.1f}% of value<extra></extra>",
    ))
    fig_res.update_layout(**plot_layout(height=340, margin=dict(l=8, r=55, t=10, b=8)))
    style_axes(fig_res, x_title="Retention (%)", show_ygrid=False)
    fig_res.update_xaxes(range=[0, 115])
    st.plotly_chart(fig_res, use_container_width=True, config={"displayModeBar": False})

    # ── Mini: Avg Resale Ratio per Segment
    seg_resale_avg = [df[df["Price_Segment"] == s]["Resale_Ratio"].mean() * 100 for s in segs]
    fig_sr = go.Figure(go.Bar(
        x=segs,
        y=seg_resale_avg,
        marker=dict(color=SEG_COLORS, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in seg_resale_avg],
        textposition="outside",
        textfont=dict(size=9, color=INK2),
        hovertemplate="<b>%{x}</b><br>Avg Resale: %{y:.1f}%<extra></extra>",
    ))
    fig_sr.update_layout(
        **plot_layout(height=160, margin=dict(l=8, r=8, t=28, b=8)),
        title=dict(text="Avg Resale Rate by Segment", font=dict(size=11, color=INK), x=0),
    )
    style_axes(fig_sr, y_title="%", show_xgrid=False)
    fig_sr.update_yaxes(range=[0, max(seg_resale_avg) * 1.3])
    st.plotly_chart(fig_sr, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with r3b:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Correlation Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Pearson correlations between numeric features · Red = negative, Blue = positive</div>', unsafe_allow_html=True)

    num_cols = ["Sales_in_thousands", "Price_in_thousands", "Horsepower",
                "Fuel_efficiency", "Engine_size", "Curb_weight",
                "Power_perf_factor", "Resale_Ratio"]
    corr_labels = ["Sales", "Price", "Horsepower", "MPG", "Engine", "Weight", "PerfFactor", "Resale"]
    corr_mat = df[num_cols].corr().round(2)

    fig_heat = go.Figure(go.Heatmap(
        z=corr_mat.values,
        x=corr_labels,
        y=corr_labels,
        colorscale=[[0, ACCENT], [0.5, SURFACE], [1, BLUE]],
        zmid=0,
        text=corr_mat.values,
        texttemplate="%{text:.2f}",
        textfont=dict(size=9, color=INK),
        hovertemplate="<b>%{y} × %{x}</b><br>r = %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(thickness=10, len=0.8,
                      tickfont=dict(size=9, color=INK2),
                      title=dict(text="r", font=dict(size=10, color=INK2))),
    ))
    fig_heat.update_layout(**plot_layout(height=340, margin=dict(l=8, r=8, t=10, b=8)))
    fig_heat.update_xaxes(tickangle=-30, tickfont=dict(size=9), gridcolor="rgba(0,0,0,0)")
    fig_heat.update_yaxes(tickfont=dict(size=9), gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    # ── Mini: Top 5 strongest correlations (absolute) with Sales
    corr_with_sales = corr_mat["Sales_in_thousands"].drop("Sales_in_thousands").abs().sort_values(ascending=False)
    top_corr = corr_mat["Sales_in_thousands"].drop("Sales_in_thousands").reindex(corr_with_sales.index)
    corr_colors = [GREEN if v > 0 else ACCENT for v in top_corr.values]
    labels_map  = dict(zip(num_cols[1:], corr_labels[1:]))
    nice_labels = [labels_map.get(i, i) for i in top_corr.index]

    fig_corr_bar = go.Figure(go.Bar(
        x=nice_labels,
        y=top_corr.values,
        marker=dict(color=[hex_to_rgba(c, 0.8) for c in corr_colors], line=dict(width=0)),
        text=[f"{v:+.2f}" for v in top_corr.values],
        textposition="outside",
        textfont=dict(size=9, color=INK2),
        hovertemplate="<b>%{x}</b> ↔ Sales<br>r = %{y:.2f}<extra></extra>",
    ))
    fig_corr_bar.add_hline(y=0, line_color=BORDER, line_width=1)
    fig_corr_bar.update_layout(
        **plot_layout(height=165, margin=dict(l=8, r=8, t=28, b=8)),
        title=dict(text="Feature Correlation with Sales", font=dict(size=11, color=INK), x=0),
    )
    style_axes(fig_corr_bar, y_title="r", show_xgrid=False)
    fig_corr_bar.update_yaxes(range=[min(top_corr.values) * 1.4, max(top_corr.values) * 1.4])
    st.plotly_chart(fig_corr_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# ROW 4 — Data Table (full width)
# ═════════════════════════════════════════════════════════════
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.markdown('<div class="chart-title">Model Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Full filtered dataset — sortable & downloadable</div>', unsafe_allow_html=True)
with t_col2:
    search = st.text_input("", placeholder="🔎 Search brand or model…", label_visibility="collapsed")

tbl = df.copy()
if search:
    mask = (
        tbl["Model"].str.contains(search, case=False, na=False) |
        tbl["Manufacturer"].str.contains(search, case=False, na=False)
    )
    tbl = tbl[mask]

display_cols = {
    "Manufacturer": "Brand", "Model": "Model", "Vehicle_type": "Type",
    "Price_Segment": "Tier", "Sales_in_thousands": "Sales (K)",
    "Price_in_thousands": "Price ($K)", "Horsepower": "HP",
    "Fuel_efficiency": "MPG", "Engine_size": "Engine (L)",
    "Resale_Ratio": "Resale Ratio", "Power_perf_factor": "Perf Factor",
}
tbl_show = tbl[list(display_cols.keys())].rename(columns=display_cols)
tbl_show["Sales (K)"]    = tbl_show["Sales (K)"].round(1)
tbl_show["Price ($K)"]   = tbl_show["Price ($K)"].round(1)
tbl_show["HP"]           = tbl_show["HP"].round(0).astype(int)
tbl_show["MPG"]          = tbl_show["MPG"].round(1)
tbl_show["Engine (L)"]   = tbl_show["Engine (L)"].round(1)
tbl_show["Resale Ratio"] = (tbl_show["Resale Ratio"] * 100).round(1).astype(str) + "%"
tbl_show["Perf Factor"]  = tbl_show["Perf Factor"].round(1)

st.dataframe(
    tbl_show.sort_values("Sales (K)", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=320,
)

dl_col, _ = st.columns([1, 4])
with dl_col:
    st.download_button(
        label="⬇️ Download CSV",
        data=tbl.to_csv(index=False).encode("utf-8"),
        file_name="filtered_car_sales.csv",
        mime="text/csv",
        use_container_width=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='border-top:1px solid {BORDER}; margin-top:2rem; padding-top:1rem;
     text-align:center; font-size:0.68rem; color:{INK2}; font-family:JetBrains Mono,monospace;'>
  AutoInsight · Car Sales Intelligence Dashboard<br>
  Built with <b style='color:{INK}'>Streamlit</b> + <b style='color:{INK}'>Plotly</b> ·
  Dataset: 157 Models · 30 Manufacturers<br>
  <span style='color:{ACCENT}'>Aris Darya Fernanda</span> · Data Analyst & Data Scientist · 2025–2026
</div>
""", unsafe_allow_html=True)
