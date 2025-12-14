import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Dashboard Analisis Penjualan Mobil",
    page_icon="🚗",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_car_sales_data.csv")

df = load_data()

# =====================================================
# JUDUL DASHBOARD
# =====================================================
st.title("🚗 Dashboard Analisis Penjualan Mobil")
st.caption("Portfolio Profesional Data Analyst | Dataset Cleaned Car Sales")

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("🔍 Filter Data")

jenis_kendaraan = st.sidebar.multiselect(
    "Jenis Kendaraan",
    df["Vehicle_type"].unique(),
    default=df["Vehicle_type"].unique()
)

manufacturer = st.sidebar.multiselect(
    "Manufacturer",
    df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

harga_min, harga_max = st.sidebar.slider(
    "Rentang Harga (Ribuan USD)",
    float(df["Price_in_thousands"].min()),
    float(df["Price_in_thousands"].max()),
    (
        float(df["Price_in_thousands"].min()),
        float(df["Price_in_thousands"].max())
    )
)

filtered_df = df[
    (df["Vehicle_type"].isin(jenis_kendaraan)) &
    (df["Manufacturer"].isin(manufacturer)) &
    (df["Price_in_thousands"] >= harga_min) &
    (df["Price_in_thousands"] <= harga_max)
]

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
st.subheader("📢 Ringkasan Eksekutif")

if not filtered_df.empty:
    brand_terlaris = (
        filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
        .sum()
        .idxmax()
    )

    model_terlaris = (
        filtered_df.sort_values("Sales_in_thousands", ascending=False)
        .iloc[0]["Model"]
    )

    jenis_terlaris = (
        filtered_df.groupby("Vehicle_type")["Sales_in_thousands"]
        .sum()
        .idxmax()
    )

    st.success(
        f"""
        ✔ **Manufacturer terlaris:** {brand_terlaris}  
        ✔ **Jenis kendaraan terlaris:** {jenis_terlaris}  
        ✔ **Model paling laku:** {model_terlaris}  
        ✔ **Harga median pasar:** ${filtered_df['Price_in_thousands'].median():.0f}K  
        """
    )
else:
    st.warning("Data kosong setelah filter diterapkan.")

# =====================================================
# KPI
# =====================================================
st.subheader("📌 Indikator Kinerja Utama (KPI)")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penjualan",
    f"{filtered_df['Sales_in_thousands'].sum():,.0f} Unit"
)
col2.metric(
    "Rata-rata Harga",
    f"${filtered_df['Price_in_thousands'].mean():,.2f}K"
)
col3.metric(
    "Jumlah Model",
    filtered_df["Model"].nunique()
)
col4.metric(
    "Rata-rata Horsepower",
    f"{filtered_df['Horsepower'].mean():.0f} HP"
)

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Ringkasan", "📈 Analisis", "🧠 Insight", "🔮 Simulasi", "📋 Data"]
)

# =====================================================
# TAB 1 — RINGKASAN
# =====================================================
with tab1:
    st.subheader("🏭 Total Penjualan per Manufacturer")

    penjualan_brand = (
        filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.plotly_chart(
        px.bar(
            penjualan_brand,
            x="Manufacturer",
            y="Sales_in_thousands",
            title="Total Penjualan per Manufacturer (Ribu Unit)"
        ),
        use_container_width=True
    )

    st.subheader("📊 Distribusi Harga Mobil")

    st.plotly_chart(
        px.histogram(
            filtered_df,
            x="Price_in_thousands",
            nbins=30,
            title="Distribusi Harga Mobil (Ribuan USD)"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 2 — ANALISIS (❌ TANPA TRENDLINE)
# =====================================================
with tab2:
    st.subheader("💰 Harga vs Penjualan")

    st.plotly_chart(
        px.scatter(
            filtered_df,
            x="Price_in_thousands",
            y="Sales_in_thousands",
            color="Vehicle_type",
            size="Horsepower",
            hover_name="Model",
            title="Harga vs Penjualan"
        ),
        use_container_width=True
    )

    st.subheader("⛽ Horsepower vs Efisiensi BBM")

    st.plotly_chart(
        px.scatter(
            filtered_df,
            x="Horsepower",
            y="Fuel_efficiency",
            hover_name="Model",
            title="Horsepower vs Efisiensi Bahan Bakar"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 3 — INSIGHT + KLASTER
# =====================================================
with tab3:
    st.subheader("📌 Segmentasi Harga")

    filtered_df["segmen_harga"] = pd.cut(
        filtered_df["Price_in_thousands"],
        bins=[0, 20, 40, 100],
        labels=["Murah", "Menengah", "Premium"]
    )

    penjualan_segmen = (
        filtered_df.groupby("segmen_harga")["Sales_in_thousands"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.bar(
            penjualan_segmen,
            x="segmen_harga",
            y="Sales_in_thousands",
            title="Penjualan berdasarkan Segmen Harga"
        ),
        use_container_width=True
    )

    # ==========================
    # KLASTER EFISIENSI BBM
    # ==========================
    st.subheader("🧠 Klaster Efisiensi Kendaraan")

    def klasifikasi_efisiensi(row):
        if row["Horsepower"] < 120 and row["Fuel_efficiency"] > 25:
            return "Low HP – High Efficiency (City Car)"
        elif row["Horsepower"] <= 200:
            return "Medium HP – Medium Efficiency (Sedan/Keluarga)"
        else:
            return "High HP – Low Efficiency (SUV/Premium)"

    filtered_df["klaster_efisiensi"] = filtered_df.apply(
        klasifikasi_efisiensi, axis=1
    )

    penjualan_klaster = (
        filtered_df.groupby("klaster_efisiensi")["Sales_in_thousands"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.bar(
            penjualan_klaster,
            x="klaster_efisiensi",
            y="Sales_in_thousands",
            title="Penjualan Berdasarkan Klaster Efisiensi BBM"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 4 — SIMULASI
# =====================================================
with tab4:
    st.subheader("🔮 Simulasi What-If Penjualan")

    harga_simulasi = st.slider("Simulasi Harga (K USD)", 10, 60, 30)
    hp_simulasi = st.slider("Simulasi Horsepower", 80, 400, 150)

    estimasi_penjualan = (
        filtered_df["Sales_in_thousands"].mean()
        - (harga_simulasi - filtered_df["Price_in_thousands"].mean()) * 0.5
        + (hp_simulasi - filtered_df["Horsepower"].mean()) * 0.02
    )

    st.success(
        f"Estimasi penjualan ≈ **{estimasi_penjualan:.2f} ribu unit**"
    )

# =====================================================
# TAB 5 — DATA
# =====================================================
with tab5:
    st.subheader("📋 Data Setelah Filter")
    st.dataframe(filtered_df)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© Portfolio Profesional Data Analyst | Streamlit Dashboard")
