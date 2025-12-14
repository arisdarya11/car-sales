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
# HITUNG TOTAL PENJUALAN (JUTA USD)
# =====================================================
filtered_df["Total_Penjualan_Juta_USD"] = (
    filtered_df["Sales_in_thousands"] *
    filtered_df["Price_in_thousands"]
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
st.subheader("📢 Ringkasan Eksekutif")

if not filtered_df.empty:
    brand_terlaris = (
        filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
        .sum().idxmax()
    )

    model_terlaris = (
        filtered_df.sort_values("Sales_in_thousands", ascending=False)
        .iloc[0]["Model"]
    )

    jenis_terlaris = (
        filtered_df.groupby("Vehicle_type")["Sales_in_thousands"]
        .sum().idxmax()
    )

    st.success(
        f"""
        ✔ **Manufacturer dengan penjualan tertinggi:** {brand_terlaris}  
        ✔ **Jenis kendaraan paling laku:** {jenis_terlaris}  
        ✔ **Model paling laris:** {model_terlaris}  
        ✔ **Harga median pasar:** ${filtered_df['Price_in_thousands'].median():.0f}K  
        """
    )
else:
    st.warning("Data kosong setelah filter diterapkan.")

# =====================================================
# KPI
# =====================================================
st.subheader("📌 Indikator Kinerja Utama (KPI)")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Unit Terjual",
    f"{(filtered_df['Sales_in_thousands'].sum() * 1000):,.0f} Unit"
)
col2.metric(
    "Total Penjualan",
    f"${filtered_df['Total_Penjualan_Juta_USD'].sum():,.2f} Juta"
)
col3.metric(
    "Rata-rata Harga",
    f"${filtered_df['Price_in_thousands'].mean():,.2f}K"
)
col4.metric(
    "Jumlah Model",
    filtered_df["Model"].nunique()
)
col5.metric(
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
        .sum().sort_values(ascending=False).reset_index()
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
# TAB 2 — ANALISIS
# =====================================================
with tab2:
    st.subheader("⛽ Horsepower vs Efisiensi BBM")

    st.plotly_chart(
        px.scatter(
            filtered_df,
            x="Horsepower",
            y="Fuel_efficiency",
            color="Vehicle_type",
            trendline="ols",
            hover_name="Model"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 3 — INSIGHT + KLASTER
# =====================================================
with tab3:
    st.subheader("🧠 Klaster Efisiensi Bahan Bakar")

    def klasifikasi_efisiensi(row):
        if row["Horsepower"] <= 130 and row["Fuel_efficiency"] >= 27:
            return "Low HP - High Efficiency (City Car)"
        elif 130 < row["Horsepower"] <= 220 and 20 <= row["Fuel_efficiency"] < 27:
            return "Medium HP - Medium Efficiency (Sedan/Keluarga)"
        else:
            return "High HP - Low Efficiency (SUV/Premium)"

    filtered_df["Klaster_Efisiensi"] = filtered_df.apply(
        klasifikasi_efisiensi, axis=1
    )

    penjualan_klaster = (
        filtered_df
        .groupby("Klaster_Efisiensi")
        .agg(
            Total_Unit_Ribu=("Sales_in_thousands", "sum"),
            Total_Penjualan_Juta_USD=("Total_Penjualan_Juta_USD", "sum"),
            Jumlah_Model=("Model", "nunique")
        )
        .reset_index()
    )

    st.dataframe(
        penjualan_klaster.rename(columns={
            "Klaster_Efisiensi": "Segmen Kendaraan",
            "Total_Unit_Ribu": "Total Unit Terjual (Ribu)",
            "Total_Penjualan_Juta_USD": "Total Penjualan (Juta USD)",
            "Jumlah_Model": "Jumlah Model"
        })
    )

    st.plotly_chart(
        px.bar(
            penjualan_klaster,
            x="Klaster_Efisiensi",
            y="Total_Penjualan_Juta_USD",
            title="Total Penjualan Berdasarkan Klaster Efisiensi (Juta USD)"
        ),
        use_container_width=True
    )

    klaster_terbaik = penjualan_klaster.sort_values(
        "Total_Penjualan_Juta_USD", ascending=False
    ).iloc[0]["Klaster_Efisiensi"]

    st.info(
        f"🔎 **Insight:** Klaster paling bernilai secara bisnis adalah "
        f"**{klaster_terbaik}**."
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

    st.subheader("🧪 Kualitas Data")
    st.dataframe(filtered_df.isnull().sum())

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© Portfolio Profesional Data Analyst | Streamlit Dashboard")
