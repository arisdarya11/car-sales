import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Cleaned Car Sales Dashboard",
    page_icon="🚗",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_car_sales_data.csv")

df = load_data()

# =========================
# JUDUL
# =========================
st.title("🚗 Dashboard Analisis Penjualan Mobil")
st.write("Dashboard ini menggunakan dataset **cleaned_car_sales_data** untuk analisis penjualan mobil.")

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔍 Filter Data")

vehicle_type = st.sidebar.multiselect(
    "Jenis Kendaraan",
    df["Vehicle_type"].unique(),
    default=df["Vehicle_type"].unique()
)

manufacturer = st.sidebar.multiselect(
    "Manufacturer",
    df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

min_price, max_price = st.sidebar.slider(
    "Rentang Harga (Ribuan USD)",
    float(df["Price_in_thousands"].min()),
    float(df["Price_in_thousands"].max()),
    (
        float(df["Price_in_thousands"].min()),
        float(df["Price_in_thousands"].max())
    )
)

filtered_df = df[
    (df["Vehicle_type"].isin(vehicle_type)) &
    (df["Manufacturer"].isin(manufacturer)) &
    (df["Price_in_thousands"] >= min_price) &
    (df["Price_in_thousands"] <= max_price)
]

# =========================
# KPI METRICS
# =========================
st.subheader("📌 Ringkasan Utama")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penjualan", f"{filtered_df['Sales_in_thousands'].sum():,.0f} K")
col2.metric("Rata-rata Harga", f"${filtered_df['Price_in_thousands'].mean():,.2f} K")
col3.metric("Jumlah Model", filtered_df["Model"].nunique())
col4.metric("Rata-rata Horsepower", f"{filtered_df['Horsepower'].mean():.0f} HP")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overview", "📈 Analisis Detail", "🧠 Insight", "📋 Data"]
)

# =========================
# TAB 1: OVERVIEW
# =========================
with tab1:
    st.subheader("🏭 Penjualan per Manufacturer")

    sales_brand = (
        filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_brand = px.bar(
        sales_brand,
        x="Manufacturer",
        y="Sales_in_thousands",
        title="Total Penjualan (Ribuan Unit)"
    )
    st.plotly_chart(fig_brand, use_container_width=True)

    st.subheader("📈 Distribusi Harga Mobil")
    fig_price_dist = px.histogram(
        filtered_df,
        x="Price_in_thousands",
        nbins=30
    )
    st.plotly_chart(fig_price_dist, use_container_width=True)

# =========================
# TAB 2: ANALISIS DETAIL
# =========================
with tab2:
    st.subheader("💰 Harga vs Penjualan")
    fig_price_sales = px.scatter(
        filtered_df,
        x="Price_in_thousands",
        y="Sales_in_thousands",
        color="Vehicle_type",
        size="Horsepower",
        hover_name="Model"
    )
    st.plotly_chart(fig_price_sales, use_container_width=True)

    st.subheader("⛽ Horsepower vs Fuel Efficiency")
    fig_fuel = px.scatter(
        filtered_df,
        x="Horsepower",
        y="Fuel_efficiency",
        hover_name="Model"
    )
    st.plotly_chart(fig_fuel, use_container_width=True)

    st.subheader("📊 Correlation Heatmap")
    corr = filtered_df.select_dtypes(include="number").corr()
    fig_corr = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# TAB 3: INSIGHT
# =========================
with tab3:
    st.subheader("🧠 Insight Otomatis")

    if not filtered_df.empty:
        top_brand = (
            filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
            .sum()
            .idxmax()
        )

        top_model = (
            filtered_df.sort_values("Sales_in_thousands", ascending=False)
            .iloc[0]["Model"]
        )

        st.info(
            f"""
            🔹 Manufacturer dengan penjualan tertinggi: **{top_brand}**  
            🔹 Model terlaris: **{top_model}**  
            🔹 Mobil dengan harga menengah cenderung memiliki penjualan lebih tinggi dibandingkan mobil premium.
            """
        )

        st.subheader("🏆 Top 10 Model Terlaris")
        top_models = (
            filtered_df.sort_values("Sales_in_thousands", ascending=False)
            .head(10)
        )
        st.dataframe(top_models[["Manufacturer", "Model", "Sales_in_thousands"]])

    else:
        st.warning("Data kosong setelah filter diterapkan.")

# =========================
# TAB 4: DATA
# =========================
with tab4:
    st.subheader("📋 Data Setelah Filter")
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Data (CSV)",
        csv,
        "filtered_car_sales_data.csv",
        "text/csv"
    )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("📊 Streamlit Dashboard | Cleaned Car Sales Data | Data Analyst Project")
