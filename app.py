import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Profil Mahasiswa - Bedah Kasus 2",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('dataset_profil_mahasiswa.csv')

df = load_data()

st.title("🎓 Dashboard Analisis Profil Mahasiswa")
st.markdown("Eksplorasi dan Analisis Mendalam Dataset Profil Mahasiswa (Bedah Kasus 2)")

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
selected_jurusan = st.sidebar.multiselect(
    "Pilih Jurusan:",
    options=df['Jurusan'].unique(),
    default=df['Jurusan'].unique()
)

selected_semester = st.sidebar.multiselect(
    "Pilih Semester:",
    options=sorted(df['Semester'].unique()),
    default=sorted(df['Semester'].unique())
)

filtered_df = df[
    (df['Jurusan'].isin(selected_jurusan)) & 
    (df['Semester'].isin(selected_semester))
]

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Mahasiswa", f"{len(filtered_df):,}")
with col2:
    avg_ipk = filtered_df['IPK'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata IPK", f"{avg_ipk:.2f}")
with col3:
    avg_usia = filtered_df['Usia'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Usia", f"{avg_usia:.1f} Tahun")
with col4:
    max_ipk = filtered_df['IPK'].max() if len(filtered_df) > 0 else 0
    st.metric("IPK Tertinggi", f"{max_ipk:.2f}")

st.markdown("---")

# Layout Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Ringkasan & Distribusi", "📈 Analisis Jurusan & Semester", "👥 Hubungan & Korelasi", "📋 Data Tabel"])

with tab1:
    st.subheader("Distribusi Variabel Numerik (IPK & Usia)")
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_ipk = px.histogram(filtered_df, x='IPK', nbins=20, title='Histogram Distribusi IPK',
                               color_discrete_sequence=['#4e79a7'], marginal='box')
        fig_ipk.update_layout(bargap=0.1)
        st.plotly_chart(fig_ipk, use_container_width=True)
        st.info("💡 **Insight IPK:** Sebaran IPK menyerupai distribusi normal dengan mayoritas mahasiswa berada di kisaran 3.00 - 3.60.")
        
    with col_b:
        fig_usia = px.histogram(filtered_df, x='Usia', nbins=10, title='Histogram Distribusi Usia',
                                color_discrete_sequence=['#f28e2b'], marginal='box')
        fig_usia.update_layout(bargap=0.1)
        st.plotly_chart(fig_usia, use_container_width=True)
        st.info("💡 **Insight Usia:** Usia mahasiswa mayoritas berada pada rentang 19 hingga 22 tahun sesuai dengan jenjang kuliah.")

with tab2:
    st.subheader("Analisis Berdasarkan Jurusan & Semester")
    col_c, col_d = st.columns(2)
    
    with col_c:
        jurusan_count = filtered_df['Jurusan'].value_counts().reset_index()
        jurusan_count.columns = ['Jurusan', 'Jumlah']
        fig_jurusan = px.bar(jurusan_count, x='Jurusan', y='Jumlah', title='Jumlah Mahasiswa per Jurusan (Kategorik Nominal)',
                             color='Jurusan', text='Jumlah')
        st.plotly_chart(fig_jurusan, use_container_width=True)
        
    with col_d:
        semester_order = filtered_df.sort_values('Semester')
        fig_semester = px.histogram(semester_order, x='Semester', title='Distribusi Mahasiswa per Semester (Kategorik Ordinal)',
                                   color='Semester', text_auto=True)
        fig_semester.update_layout(xaxis=dict(type='category'))
        st.plotly_chart(fig_semester, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Rata-rata IPK per Jurusan")
    avg_ipk_jurusan = filtered_df.groupby('Jurusan')['IPK'].mean().reset_index()
    fig_avg_ipk = px.bar(avg_ipk_jurusan, x='Jurusan', y='IPK', title='Perbandingan Rata-rata IPK antar Jurusan',
                         color='Jurusan', text_auto='.2f')
    st.plotly_chart(fig_avg_ipk, use_container_width=True)

with tab3:
    st.subheader("Analisis Hubungan Antar Variabel (Bivariate)")
    
    col_e, col_f = st.columns(2)
    with col_e:
        fig_box = px.box(filtered_df, x='Semester', y='IPK', title='Box Plot: IPK berdasarkan Semester',
                         color='Semester')
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_f:
        fig_scatter = px.scatter(filtered_df, x='Usia', y='IPK', color='Jurusan', 
                                 title='Scatter Plot: Hubungan Usia dan IPK',
                                 opacity=0.7, trendline='ols')
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.info("📊 **Analisis Mendalam:** Box plot menunjukkan sebaran IPK di tiap semester beserta outlier (nilai pencilan). Scatter plot membantu melihat apakah usia memengaruhi performa akademik (IPK).")

with tab4:
    st.subheader("Eksplorasi Data Mentah (1,000 Data Sintetis)")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv_download = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data yang Difilter (CSV)",
        data=csv_download,
        file_name='filtered_profil_mahasiswa.csv',
        mime='text/csv'
    )
