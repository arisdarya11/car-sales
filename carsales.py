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
st.title("🚗 Dashboard Analisis Penjualan Mobil (Cleaned Data)")
st.write("Dashboard ini menggunakan dataset yang telah dibersihkan.")

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔍 Filter Data")

vehicle_type = st.sidebar.multiselect(
    "Pilih Jenis Kendaraan",
    df["Vehicle_type"].unique(),
    default=df["Vehicle_type"].unique()
)

manufacturer = st.sidebar.multiselect(
    "Pilih Manufacturer",
    df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

filtered_df = df[
    (df["Vehicle_type"].isin(vehicle_type)) &
    (df["Manufacturer"].isin(manufacturer))
]

# =========================
# KPI METRICS
# =========================
st.subheader("📌 Ringkasan Utama")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penjualan",
    f"{filtered_df['Sales_in_thousands'].sum():,.0f} K Unit"
)

col2.metric(
    "Rata-rata Harga",
    f"${filtered_df['Price_in_thousands'].mean():,.2f} K"
)

col3.metric(
    "Jumlah Model",
    filtered_df["Model"].nunique()
)

# =========================
# VISUALISASI
# =========================
st.subheader("🏭 Total Penjualan per Manufacturer")

sales_brand = (
    filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.plotly_chart(
    px.bar(
        sales_brand,
        x="Manufacturer",
        y="Sales_in_thousands",
        title="Total Penjualan per Manufacturer"
    ),
    use_container_width=True
)

st.subheader("💰 Harga vs Penjualan")

st.plotly_chart(
    px.scatter(
        filtered_df,
        x="Price_in_thousands",
        y="Sales_in_thousands",
        color="Vehicle_type",
        size="Horsepower",
        hover_name="Model"
    ),
    use_container_width=True
)

st.subheader("⛽ Horsepower vs Fuel Efficiency")

st.plotly_chart(
    px.scatter(
        filtered_df,
        x="Horsepower",
        y="Fuel_efficiency",
        hover_name="Model"
    ),
    use_container_width=True
)

# =========================
# TABEL DATA
# =========================
st.subheader("📋 Data Setelah Filter")
st.dataframe(filtered_df)

st.caption("Dashboard Streamlit – Cleaned Car Sales Data")
