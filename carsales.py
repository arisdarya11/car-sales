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
    df = pd.read_csv("cleaned_car_sales_data.csv")
    df["Latest_Launch"] = pd.to_datetime(df["Latest_Launch"], errors="coerce")
    df["Launch_Year"] = df["Latest_Launch"].dt.year
    return df

df = load_data()

# =====================================================
# JUDUL DASHBOARD
# =====================================================
st.title("🚗 Dashboard Analisis Penjualan Mobil")
st.caption("Car Sales Analytics & Visualization | Powered by Streamlit")

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

filtered_df = df.loc[
    (df["Vehicle_type"].isin(jenis_kendaraan)) &
    (df["Manufacturer"].isin(manufacturer)) &
    (df["Price_in_thousands"] >= harga_min) &
    (df["Price_in_thousands"] <= harga_max)
].copy()

# =====================================================
# HITUNG TOTAL PENDAPATAN
# =====================================================
filtered_df["Total_Revenue_USD"] = (
    filtered_df["Price_in_thousands"]
    * filtered_df["Sales_in_thousands"]
    * 1_000_000
)

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

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Unit Terjual",
            f"{filtered_df['Sales_in_thousands'].sum():,.0f} Unit")

col2.metric("Total Pendapatan",
            f"${filtered_df['Total_Revenue_USD'].sum()/1_000_000_000:,.2f} B")

col3.metric("Rata-rata Harga",
            f"${filtered_df['Price_in_thousands'].mean():,.2f}K")

col4.metric("Jumlah Model",
            filtered_df["Model"].nunique())

col5.metric("Rata-rata Horsepower",
            f"{filtered_df['Horsepower'].mean():.0f} HP")

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

    # =========================
    # TREND 2008–2012
    # =========================
    st.subheader("📈 Tren Penjualan Berdasarkan Tahun Launch (2008–2012)")

    sales_launch_trend = (
        filtered_df[
            (filtered_df["Launch_Year"] >= 2008) &
            (filtered_df["Launch_Year"] <= 2012)
        ]
        .groupby("Launch_Year")["Sales_in_thousands"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.line(
            sales_launch_trend,
            x="Launch_Year",
            y="Sales_in_thousands",
            markers=True,
            title="Tren Penjualan Mobil Tahun 2008–2012"
        ),
        use_container_width=True
    )

    # =========================
    # MODEL BARU VS LAMA
    # =========================
    latest_year = int(filtered_df["Launch_Year"].max())

    filtered_df["Kategori_Model"] = filtered_df["Launch_Year"].apply(
        lambda x: "Model Baru (≤3 Tahun)"
        if pd.notna(x) and x >= latest_year - 3
        else "Model Lama (>3 Tahun)"
        if pd.notna(x)
        else "Unknown"
    )

    penjualan_model = (
        filtered_df.groupby("Kategori_Model")["Sales_in_thousands"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.bar(
            penjualan_model,
            x="Kategori_Model",
            y="Sales_in_thousands",
            title="Perbandingan Penjualan Model Baru vs Model Lama"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 2 — ANALISIS
# =====================================================
with tab2:
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

# =====================================================
# TAB 3 — INSIGHT
# =====================================================
with tab3:
    filtered_df["Segmen_Harga"] = pd.cut(
        filtered_df["Price_in_thousands"],
        bins=[0, 20, 40, 100],
        labels=["Murah", "Menengah", "Premium"]
    )

    segmen_penjualan = (
        filtered_df.groupby("Segmen_Harga")["Sales_in_thousands"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.bar(
            segmen_penjualan,
            x="Segmen_Harga",
            y="Sales_in_thousands",
            title="Penjualan Berdasarkan Segmen Harga"
        ),
        use_container_width=True
    )

# =====================================================
# TAB 4 — SIMULASI
# =====================================================
with tab4:
    harga_simulasi = st.slider("Simulasi Harga (K USD)", 10, 60, 30)
    hp_simulasi = st.slider("Simulasi Horsepower", 80, 400, 150)

    estimasi_penjualan = (
        filtered_df["Sales_in_thousands"].mean()
        - (harga_simulasi - filtered_df["Price_in_thousands"].mean()) * 0.5
        + (hp_simulasi - filtered_df["Horsepower"].mean()) * 0.02
    )

    st.success(f"Estimasi penjualan ≈ **{estimasi_penjualan:.2f} ribu unit**")

# =====================================================
# TAB 5 — DATA
# =====================================================
with tab5:
    st.dataframe(filtered_df)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© Portfolio Data Analyst | Dashboard built with Streamlit")
