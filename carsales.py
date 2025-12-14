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
# JUDUL
# =====================================================
st.title("🚗 Dashboard Analisis Penjualan Mobil")
st.caption("Portofolio Profesional Data Analyst")

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

filtered_df = df[
    (df["Vehicle_type"].isin(jenis_kendaraan)) &
    (df["Manufacturer"].isin(manufacturer))
]

# =====================================================
# RINGKASAN EKSEKUTIF
# =====================================================
st.subheader("📢 Ringkasan Eksekutif")

if not filtered_df.empty:
    brand_terlaris = (
        filtered_df.groupby("Manufacturer")["Sales_in_thousands"]
        .sum()
        .idxmax()
    )

    jenis_kendaraan_terlaris = (
        filtered_df.groupby("Vehicle_type")["Sales_in_thousands"]
        .sum()
        .idxmax()
    )

    total_unit = filtered_df["Sales_in_thousands"].sum()
    total_penjualan_juta = (
        filtered_df["Sales_in_thousands"] *
        filtered_df["Price_in_thousands"]
    ).sum()

    st.success(
        f"""
        ✔ **Total unit terjual:** {total_unit:,.0f} ribu unit  
        ✔ **Total penjualan:** {total_penjualan_juta:,.2f} juta USD  
        ✔ **Manufacturer terlaris:** {brand_terlaris}  
        ✔ **Jenis kendaraan terlaris:** {jenis_kendaraan_terlaris}  
        """
    )

# =====================================================
# KPI
# =====================================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Unit Terjual (Ribuan)", f"{total_unit:,.0f}")
col2.metric("Total Penjualan (Juta USD)", f"{total_penjualan_juta:,.2f}")
col3.metric("Jumlah Model", filtered_df["Model"].nunique())

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3 = st.tabs(
    ["🏆 Top Model", "🏭 Manufacturer", "📋 Data"]
)

# =====================================================
# TAB 1 — TOP 10 MODEL TERLARIS
# =====================================================
with tab1:
    st.subheader("🏆 10 Model Terlaris")

    df_top = filtered_df.copy()
    df_top["Total_Penjualan_Juta_USD"] = (
        df_top["Sales_in_thousands"] *
        df_top["Price_in_thousands"]
    )

    top_10 = (
        df_top.sort_values("Sales_in_thousands", ascending=False)
        .head(10)
    )

    # BAR PLOT
    fig = px.bar(
        top_10,
        x="Sales_in_thousands",
        y="Model",
        orientation="h",
        color="Manufacturer",
        title="10 Model Terlaris Berdasarkan Unit Terjual",
        labels={
            "Sales_in_thousands": "Unit Terjual (Ribuan)",
            "Model": "Model"
        }
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig, use_container_width=True)

    # TABEL
    st.dataframe(
        top_10[[
            "Manufacturer",
            "Model",
            "Sales_in_thousands",
            "Total_Penjualan_Juta_USD"
        ]].rename(columns={
            "Sales_in_thousands": "Unit Terjual (Ribuan)",
            "Total_Penjualan_Juta_USD": "Total Penjualan (Juta USD)"
        })
    )

    # INSIGHT OTOMATIS
    st.info(
        "📌 **Insight:** Model dengan unit terjual tertinggi "
        "belum tentu menghasilkan penjualan terbesar secara nilai."
    )

# =====================================================
# TAB 2 — MANUFACTURER
# =====================================================
with tab2:
    st.subheader("🏭 Penjualan per Manufacturer")

    manuf_table = (
        filtered_df
        .groupby("Manufacturer")
        .agg(
            Unit_Terjual_Ribuan=("Sales_in_thousands", "sum"),
            Total_Penjualan_Juta_USD=(
                "Sales_in_thousands",
                lambda x: (x * filtered_df.loc[x.index, "Price_in_thousands"]).sum()
            )
        )
        .reset_index()
        .sort_values("Unit_Terjual_Ribuan", ascending=False)
    )

    st.plotly_chart(
        px.bar(
            manuf_table,
            x="Manufacturer",
            y="Unit_Terjual_Ribuan",
            title="Total Unit Terjual per Manufacturer"
        ),
        use_container_width=True
    )

    st.dataframe(manuf_table)

    st.info(
        "📌 **Insight:** Manufacturer dengan volume tinggi "
        "belum tentu memiliki total penjualan tertinggi."
    )

# =====================================================
# TAB 3 — DATA
# =====================================================
with tab3:
    st.subheader("📋 Data Setelah Filter")
    st.dataframe(filtered_df)

    st.subheader("🧪 Kualitas Data")
    st.dataframe(filtered_df.isnull().sum())

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© Portofolio Data Analyst | Streamlit Dashboard")
