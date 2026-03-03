import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Tourism Data Insight", layout="wide")

# Veriyi Yükle
@st.cache_data
def load_data():
    df = pd.read_csv('data_warehouse_segmented.csv')
    return df

df = load_data()

# --- SIDEBAR (Filtreleme Alanı) ---
st.sidebar.header("Filter Options")
hotel_type = st.sidebar.multiselect("Select Hotel Type", 
                                    options=df["hotel"].unique(), 
                                    default=df["hotel"].unique())

segment_type = st.sidebar.multiselect("Select Customer Segments", 
                                      options=df["customer_segment"].unique(), 
                                      default=df["customer_segment"].unique())

filtered_df = df[(df["hotel"].isin(hotel_type)) & (df["customer_segment"].isin(segment_type))]

# --- ANA BAŞLIK ---
st.title("🏨 Tourism Data Warehouse & Customer Analytics")
st.markdown("From Scattered Data to **Gold Mine** - *Executive Dashboard*")

# --- KPI METRIKLERI (Üst Bant) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Bookings", len(filtered_df))
with col2:
    st.metric("Avg Price (ADR)", f"${filtered_df['adr'].mean():.2f}")
with col3:
    st.metric("Cancellation Rate", f"{filtered_df['is_canceled'].mean()*100:.1f}%")
with col4:
    st.metric("Repeated Guests", f"{filtered_df['is_repeated_guest'].mean()*100:.1f}%")

st.divider()

# --- GRAFİKLER ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Revenue by Segment")
    fig_rev = px.bar(filtered_df.groupby("customer_segment")["adr"].mean().reset_index(), 
                     x="customer_segment", y="adr", color="customer_segment",
                     color_continuous_scale="Blues")
    st.plotly_chart(fig_rev, use_container_width=True)

with row1_col2:
    st.subheader("Lead Time vs. Cancellation")
    fig_lead = px.box(filtered_df, x="customer_segment", y="lead_time", color="is_canceled")
    st.plotly_chart(fig_lead, use_container_width=True)

# --- STRATEJİK ÖNERİLER (İş Zekası) ---
st.divider()
st.header("💡 Strategic Recommendations")

# Burada dün yaptığın analizleri yazabilirsin
st.info("""
- **Segment 1 (High Value):** These are our VIPs. Focus on personalized services to maintain high ADR.
- **Segment 0 (Early Birds):** High cancellation risk. Implement a strict deposit policy for bookings made >200 days in advance.
- **Loyalty Program:** Segment 3 shows a high repeat rate; target them with exclusive member-only discounts.
""")

# --- VERİ TABLOSU ---
if st.checkbox("Show Raw Segmented Data"):
    st.write(filtered_df.head(100))