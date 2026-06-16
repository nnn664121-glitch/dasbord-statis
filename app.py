import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Analisis Kopi & Produktivitas",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS KUSTOM ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4A2C2A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD & PREPROCESS DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', sep=';')
    df_clean = df.copy()

    # 1. Konversi Konsumsi Kopi
    df_clean['Kopi_per_Hari'] = df_clean.iloc[:, 4].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

    # 2. Konversi Durasi Belajar
    hours_mapping = {
        '< 2 jam': 1.0,
        '2-4 jam': 3.0,
        '5-7 jam': 6.0,
        '> 7 jam': 8.5
    }
    df_clean['Durasi_Belajar_Num'] = df_clean.iloc[:, 7].map(hours_mapping).fillna(df_clean.iloc[:, 7].mode()[0])

    # 3. Skor Komposit Produktivitas
    likert_cols = [df_clean.columns[9], df_clean.columns[10], df_clean.columns[11], df_clean.columns[12]]
    df_clean['Skor_Produktivitas'] = df_clean[likert_cols].mean(axis=1)

    # 4. Kualitas Tidur
    df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean.iloc[:, 15], errors='coerce').fillna(3)

    # 5. Indikator Fokus Tinggi
    df_clean['Is_Fokus_Tinggi'] = (df_clean['Skor_Produktivitas'] > 3.0).astype(int)
    df_clean['Is_Peminum_Kopi'] = (df_clean['Kopi_per_Hari'] > 0).astype(int)

    return df_clean

# Load data
df = load_data()

# --- HEADER ---
st.markdown('<p class="main-header">☕ Dashboard Analisis Konsumsi Kopi & Produktivitas Mahasiswa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Visualisasi Interaktif Berbasis Data Kuesioner (n=31 Responden)</p>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🎛️ Filter Data")

    kopi_filter = st.multiselect(
        "Jumlah Cangkir Kopi:",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique())
    )

    durasi_options = df['Durasi_Belajar_Num'].unique()
    durasi_range = st.slider(
        "Range Durasi Belajar (jam):",
        min_value=float(min(durasi_options)),
        max_value=float(max(durasi_options)),
        value=(float(min(durasi_options)), float(max(durasi_options)))
    )

    fokus_filter = st.selectbox(
        "Status Fokus:",
        options=["Semua", "Fokus Tinggi (>3.0)", "Fokus Rendah (≤3.0)"]
    )

    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1])
    ]

    if fokus_filter == "Fokus Tinggi (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Fokus Rendah (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]

    st.divider()
    st.metric("Responden Terpilih", f"{len(df_filtered)} / {len(df)}")

# --- METRIK UTAMA ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rata-rata Konsumsi Kopi",
        f"{df_filtered['Kopi_per_Hari'].mean():.2f} cangkir/hari",
        delta=f"{df_filtered['Kopi_per_Hari'].std():.2f} std"
    )

with col2:
    st.metric(
        "Rata-rata Durasi Belajar",
        f"{df_filtered['Durasi_Belajar_Num'].mean():.1f} jam/hari",
        delta=f"{df_filtered['Durasi_Belajar_Num'].std():.1f} std"
    )

with col3:
    st.metric(
        "Skor Produktivitas",
        f"{df_filtered['Skor_Produktivitas'].mean():.2f} / 5.0",
        delta=f"{df_filtered['Skor_Produktivitas'].std():.2f} std"
    )

with col4:
    fokus_pct = df_filtered['Is_Fokus_Tinggi'].mean() * 100
    st.metric(
        "% Fokus Tinggi",
        f"{fokus_pct:.1f}%",
        delta=f"{len(df_filtered[df_filtered['Is_Fokus_Tinggi']==1])} orang"
    )

st.divider()

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analisis Deskriptif",
    "🔗 Analisis Korelasi",
    "🎯 Probabilitas Bersyarat",
    "🎲 Simulasi Monte Carlo"
])

# ===================== TAB 1: DESKRIPTIF =====================
with tab1:
    st.header("Analisis Statistika Deskriptif")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribusi Konsumsi Kopi")
        kopi_counts = df_filtered['Kopi_per_Hari'].value_counts().sort_index()
        fig_dist_kopi = px.bar(
            x=kopi_counts.index,
            y=kopi_counts.values,
            labels={'x': 'Jumlah Cangkir Kopi', 'y': 'Jumlah Responden'},
            color_discrete_sequence=['#6F4E37']
        )
        fig_dist_kopi.update_layout(xaxis=dict(dtick=1))
        fig_dist_kopi.update_traces(
            hovertemplate="<b>%{x} cangkir</b><br>Responden: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_dist_kopi, use_container_width=True)

    with col_b:
        st.subheader("Distribusi Skor Produktivitas")
        fig_hist_prod = px.histogram(
            df_filtered,
            x='Skor_Produktivitas',
            nbins=15,
            color_discrete_sequence=['#2E86AB'],
            labels={'Skor_Produktivitas': 'Skor Produktivitas'}
        )
        fig_hist_prod.update_traces(
            hovertemplate="<b>Skor: %{x:.2f}</b><br>Frekuensi: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_hist_prod, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Skor Produktivitas per Kelompok Kopi")
        fig_box = px.box(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            color='Kopi_per_Hari',
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                'Kopi_per_Hari': 'Cangkir/Hari',
                'Skor_Produktivitas': 'Skor Produktivitas (1-5)'
            }
        )
        fig_box.update_layout(showlegend=False)
        fig_box.update_traces(
            hovertemplate="<b>%{x} cangkir</b><br>Skor: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_d:
        st.subheader("Rata-rata Durasi Belajar per Kelompok Kopi")
        durasi_mean = df_filtered.groupby('Kopi_per_Hari')['Durasi_Belajar_Num'].mean().reset_index()
        fig_bar_durasi = px.bar(
            durasi_mean,
            x='Kopi_per_Hari',
            y='Durasi_Belajar_Num',
            color='Durasi_Belajar_Num',
            color_continuous_scale='Oranges',
            labels={
                'Kopi_per_Hari': 'Cangkir/Hari',
                'Durasi_Belajar_Num': 'Rata-rata Jam Belajar'
            }
        )
        fig_bar_durasi.update_layout(coloraxis_showscale=False)
        fig_bar_durasi.update_traces(
            hovertemplate="<b>%{x} cangkir</b><br>Durasi: %{y:.1f} jam<extra></extra>"
        )
        st.plotly_chart(fig_bar_durasi, use_container_width=True)

    st.subheader("Ringkasan Statistik")
    stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
    st.dataframe(stats_df, use_container_width=True)

# ===================== TAB 2: KORELASI =====================
with tab2:
    st.header("Analisis Korelasi Antar Variabel")

    col_e, col_f = st.columns([1, 1])

    with col_e:
        st.subheader("Heatmap Matriks Korelasi (Pearson)")
        corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
        corr_matrix = df_filtered[corr_cols].corr(method='pearson')

        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".3f",
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            labels={'color': 'Korelasi'}
        )
        fig_heatmap.update_layout(height=450)
        fig_heatmap.update_traces(
            hovertemplate="<b>%{y} vs %{x}</b><br>Korelasi: %{z:.3f}<extra></extra>"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col_f:
        st.subheader("Scatter: Kopi vs Produktivitas")

        if len(df_filtered) > 1:
            p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
            signifikansi = "Signifikan" if p_value < 0.05 else "Tidak Signifikan"

            st.info(f"""
            **Koefisien Korelasi (r):** {p_coeff:.4f}  
            **P-Value:** {p_value:.4f}  
            **Status:** {signifikansi} (α = 0.05)
            """)

        fig_scatter = px.scatter(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            trendline='ols' if len(df_filtered) > 2 else None,
            color='Durasi_Belajar_Num',
            color_continuous_scale='viridis',
            size='Kualitas_Tidur_Memburuk',
            size_max=20,
            labels={
                'Kopi_per_Hari': 'Cangkir Kopi/Hari',
                'Skor_Produktivitas': 'Skor Produktivitas',
                'Durasi_Belajar_Num': 'Durasi Belajar (jam)',
                'Kualitas_Tidur_Memburuk': 'Kualitas Tidur'
            },
            hover_data=['Is_Fokus_Tinggi']
        )
        fig_scatter.update_traces(
            hovertemplate="<b>%{x} cangkir</b><br>Produktivitas: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("💡 Insight Korelasi")
    insight_cols = st.columns(3)

    with insight_cols[0]:
        st.markdown("""
        **Kopi ↔ Produktivitas**  
        Korelasi positif lemah menunjukkan tren bahwa konsumsi kopi sedikit meningkatkan persepsi produktivitas.
        """)

    with insight_cols[1]:
        st.markdown("""
        **Kopi ↔ Kualitas Tidur**  
        Korelasi negatif moderat membuktikan trade-off: semakin banyak kopi, semakin buruk kualitas tidur.
        """)

    with insight_cols[2]:
        st.markdown("""
        **Kopi ↔ Durasi Belajar**  
        Korelasi positif menunjukkan peminum kopi cenderung belajar lebih lama.
        """)

# ===================== TAB 3: PROBABILITAS =====================
with tab3:
    st.header("Analisis Probabilitas Bersyarat")
    st.markdown("Menghitung peluang mahasiswa memiliki **Fokus Tinggi** (Skor > 3.0) berdasarkan status konsumsi kopi.")

    col_g, col_h = st.columns([1, 1])

    with col_g:
        st.subheader("Tabel Kontingensi")
        kontingensi = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            margins=True
        )
        kontingensi.index = ['Tidak Minum (0)', 'Minum Kopi (≥1)', 'Total']
        kontingensi.columns = ['Fokus Rendah', 'Fokus Tinggi', 'Total']
        st.dataframe(kontingensi, use_container_width=True)

        st.subheader("Matriks Probabilitas Bersyarat")
        prob_bersyarat = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            normalize='index'
        ) * 100
        prob_bersyarat.index = ['Tidak Minum Kopi', 'Minum Kopi']
        prob_bersyarat.columns = ['Fokus Rendah (%)', 'Fokus Tinggi (%)']
        st.dataframe(prob_bersyarat.round(2), use_container_width=True)

    with col_h:
        st.subheader("Perbandingan Probabilitas")

        if 1 in df_filtered['Is_Peminum_Kopi'].values:
            p_kopi = prob_bersyarat.loc['Minum Kopi', 'Fokus Tinggi (%)']
        else:
            p_kopi = 0

        if 0 in df_filtered['Is_Peminum_Kopi'].values:
            p_non_kopi = prob_bersyarat.loc['Tidak Minum Kopi', 'Fokus Tinggi (%)']
        else:
            p_non_kopi = 0

        fig_prob = go.Figure(data=[
            go.Bar(
                name='Fokus Tinggi',
                x=['Minum Kopi', 'Tidak Minum'],
                y=[p_kopi, p_non_kopi],
                marker_color=['#2E8B57', '#CD5C5C'],
                text=[f'{p_kopi:.1f}%', f'{p_non_kopi:.1f}%'],
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>Peluang Fokus Tinggi: %{y:.1f}%<extra></extra>"
            )
        ])
        fig_prob.update_layout(
            yaxis_title="Probabilitas (%)",
            yaxis_range=[0, 100],
            title="P(Fokus Tinggi | Konsumsi Kopi)"
        )
        st.plotly_chart(fig_prob, use_container_width=True)

        if p_kopi > p_non_kopi and p_non_kopi > 0:
            st.success(f"📈 Mahasiswa yang minum kopi memiliki peluang **{p_kopi/p_non_kopi:.1f}x lebih besar** untuk mencapai fokus tinggi!")
        elif p_kopi > 0 and p_non_kopi == 0:
            st.success("📈 Hanya peminum kopi yang mencapai fokus tinggi!")
        else:
            st.warning("Data tidak cukup untuk membandingkan probabilitas.")

# ===================== TAB 4: MONTE CARLO =====================
with tab4:
    st.header("Simulasi Monte Carlo")
    st.markdown("Proyeksi rata-rata skor produktivitas ke populasi 100 mahasiswa melalui 10.000 iterasi stokastik.")

    col_i, col_j = st.columns([1, 2])

    with col_i:
        st.subheader("Parameter Simulasi")
        n_mahasiswa = st.slider("Jumlah Mahasiswa per Kelas:", 10, 500, 100, 10)
        n_iterasi = st.slider("Jumlah Iterasi:", 1000, 50000, 10000, 1000)

        st.markdown("**Distribusi Empiris Kopi:**")
        p_kopi_dist = df['Kopi_per_Hari'].value_counts(normalize=True).sort_index()
        for cat, w in p_kopi_dist.items():
            st.markdown(f"- {cat} cangkir: **{w*100:.1f}%**")

        simulate_btn = st.button("🎲 Jalankan Simulasi", type="primary")

    with col_j:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("Menjalankan simulasi Monte Carlo..."):
                categories_kopi = p_kopi_dist.index.values
                weights_kopi = p_kopi_dist.values

                stats_by_group = df.groupby('Kopi_per_Hari')['Skor_Produktivitas'].agg(['mean', 'std'])
                overall_std = df['Skor_Produktivitas'].std()
                stats_by_group['std'] = stats_by_group['std'].fillna(overall_std)

                hasil_rata_rata = []
                for _ in range(n_iterasi):
                    simulasi_kopi = np.random.choice(categories_kopi, size=n_mahasiswa, p=weights_kopi)
                    skor_kelas = []
                    for pilihan in simulasi_kopi:
                        mean_val = stats_by_group.loc[pilihan, 'mean']
                        std_val = stats_by_group.loc[pilihan, 'std']
                        skor_acak = np.clip(np.random.normal(mean_val, std_val), 1.0, 5.0)
                        skor_kelas.append(skor_acak)
                    hasil_rata_rata.append(np.mean(skor_kelas))

                st.session_state['mc_results'] = hasil_rata_rata

        if 'mc_results' in st.session_state:
            hasil = st.session_state['mc_results']
            mean_mc = np.mean(hasil)
            ci_bawah = np.percentile(hasil, 2.5)
            ci_atas = np.percentile(hasil, 97.5)

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Rata-rata Ekspektasi", f"{mean_mc:.4f}")
            with m2:
                st.metric("Batas Bawah CI 95%", f"{ci_bawah:.4f}")
            with m3:
                st.metric("Batas Atas CI 95%", f"{ci_atas:.4f}")

            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=hasil,
                nbinsx=50,
                name='Distribusi Monte Carlo',
                marker_color='#E63946',
                opacity=0.75,
                hovertemplate="Skor: %{x:.3f}<br>Frekuensi: %{y}<extra></extra>"
            ))
            fig_mc.add_vline(
                x=mean_mc, line_dash="dash", line_color="blue",
                annotation_text=f"Mean: {mean_mc:.3f}"
            )
            fig_mc.add_vline(
                x=ci_bawah, line_dash="dot", line_color="purple",
                annotation_text=f"CI Bawah: {ci_bawah:.3f}"
            )
            fig_mc.add_vline(
                x=ci_atas, line_dash="dot", line_color="purple",
                annotation_text=f"CI Atas: {ci_atas:.3f}"
            )
            fig_mc.update_layout(
                title=f"Distribusi Probabilitas Rata-rata Skor ({len(hasil)} Iterasi)",
                xaxis_title="Rata-rata Skor Produktivitas Kelas",
                yaxis_title="Frekuensi",
                height=400
            )
            st.plotly_chart(fig_mc, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 Dashboard dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p>Sumber Data: Kuesioner Mahasiswa (n=31) | Tools: Python, Streamlit, Plotly</p>
</div>
""", unsafe_allow_html=True)
