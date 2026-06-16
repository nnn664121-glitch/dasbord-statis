import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Coffee Analytics 3D Pro ☕",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM FUTURISTIC EDITION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: radial-gradient(ellipse at top, #0f172a 0%, #020617 50%, #000000 100%);
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }
    
    /* Hide Streamlit Chrome */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {width: 8px;}
    ::-webkit-scrollbar-track {background: #0f172a;}
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #06b6d4, #8b5cf6);
        border-radius: 10px;
    }
    
    /* HERO SECTION */
    .hero-container {
        position: relative;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        margin-bottom: 2.5rem;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(6, 182, 212, 0.1), transparent, rgba(139, 92, 246, 0.1), transparent);
        animation: rotate 15s linear infinite;
        z-index: 0;
    }
    
    @keyframes rotate { 100% { transform: rotate(360deg); } }
    
    .hero-content { position: relative; z-index: 1; }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #22d3ee 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0.8rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* BENTO GRID KPI CARDS */
    .bento-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.2rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #22d3ee, #a78bfa);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-6px);
        border-color: rgba(139, 92, 246, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card:hover::before { opacity: 1; }
    
    .kpi-icon { font-size: 1.8rem; margin-bottom: 0.5rem; display: block; }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.4rem;
        font-weight: 600;
    }
    
    /* SECTION HEADERS */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .section-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #22d3ee, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
    }
    
    /* GLASS CARDS FOR CONTENT */
    .glass-card {
        background: rgba(30, 41, 59, 0.3);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(34, 211, 238, 0.2);
        background: rgba(30, 41, 59, 0.5);
    }
    
    /* SIDEBAR */
    .stSidebar {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
        font-family: 'Outfit', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(139, 92, 246, 0.1);
        color: #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: #fff;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Outfit', sans-serif;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
    }
    
    /* INFO BOX */
    .info-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-left: 3px solid #22d3ee;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* FOOTER */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .footer-text { color: #64748b; font-size: 0.85rem; margin: 0.3rem 0; }
    .footer-brand {
        background: linear-gradient(135deg, #22d3ee, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1rem;
    }
    
    /* Streamlit Elements Override */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; }
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
    hours_mapping = {'< 2 jam': 1.0, '2-4 jam': 3.0, '5-7 jam': 6.0, '> 7 jam': 8.5}
    df_clean['Durasi_Belajar_Num'] = df_clean.iloc[:, 7].map(hours_mapping).fillna(df_clean.iloc[:, 7].mode()[0])

    # 3. Skor Komposit Produktivitas
    likert_cols = [df_clean.columns[9], df_clean.columns[10], df_clean.columns[11], df_clean.columns[12]]
    df_clean['Skor_Produktivitas'] = df_clean[likert_cols].mean(axis=1)

    # 4. Kualitas Tidur
    df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean.iloc[:, 15], errors='coerce').fillna(3)

    # 5. Indikator
    df_clean['Is_Fokus_Tinggi'] = (df_clean['Skor_Produktivitas'] > 3.0).astype(int)
    df_clean['Is_Peminum_Kopi'] = (df_clean['Kopi_per_Hari'] > 0).astype(int)
    df_clean['Fokus_Label'] = df_clean['Is_Fokus_Tinggi'].map({1: 'High Focus', 0: 'Low Focus'})

    return df_clean

df = load_data()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <h1 class="hero-title">☕ Coffee Analytics Pro</h1>
        <p class="hero-subtitle">Advanced 3D Data Visualization & Stochastic Modeling for Academic Productivity</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### ⚙️ **Control Panel**")
    st.markdown("---")

    kopi_filter = st.multiselect(
        "☕ Cangkir per Hari",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique())
    )

    durasi_options = df['Durasi_Belajar_Num'].unique()
    durasi_range = st.slider(
        "⏰ Durasi Belajar (jam)",
        min_value=float(min(durasi_options)),
        max_value=float(max(durasi_options)),
        value=(float(min(durasi_options)), float(max(durasi_options)))
    )

    fokus_filter = st.selectbox(
        "🎯 Status Fokus",
        options=["Semua", "High Focus (>3.0)", "Low Focus (≤3.0)"]
    )

    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1])
    ]

    if fokus_filter == "High Focus (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Low Focus (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]

    st.markdown("---")
    st.markdown(f"""
    <div class="kpi-card" style="text-align: center; border-color: rgba(34, 211, 238, 0.3);">
        <span class="kpi-icon">👥</span>
        <p class="kpi-value">{len(df_filtered)}</p>
        <p class="kpi-label">Responden Aktif</p>
    </div>
    """, unsafe_allow_html=True)

# --- BENTO GRID KPI ---
st.markdown("""
<div class="section-header">
    <span class="section-number">01</span>
    <div><h2 class="section-title">Key Performance Metrics</h2></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">☕</span>
        <p class="kpi-value">{df_filtered['Kopi_per_Hari'].mean():.2f}</p>
        <p class="kpi-label">Avg Cups / Day</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📚</span>
        <p class="kpi-value">{df_filtered['Durasi_Belajar_Num'].mean():.1f}h</p>
        <p class="kpi-label">Study Duration</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚡</span>
        <p class="kpi-value">{df_filtered['Skor_Produktivitas'].mean():.2f}</p>
        <p class="kpi-label">Productivity Score</p>
    </div>""", unsafe_allow_html=True)
with col4:
    fokus_pct = df_filtered['Is_Fokus_Tinggi'].mean() * 100
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <p class="kpi-value">{fokus_pct:.0f}%</p>
        <p class="kpi-label">High Focus Rate</p>
    </div>""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 3D Visualization",
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎲 Monte Carlo Simulation"
])

# ===================== TAB 1: 3D VISUALIZATION =====================
with tab1:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">3D</span>
        <div><h2 class="section-title">Interactive 3D Data Space</h2></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">💡 <strong>Tip:</strong> Klik & drag untuk memutar, scroll untuk zoom, hover pada titik untuk melihat detail responden.</div>', unsafe_allow_html=True)
    
    fig_3d = px.scatter_3d(
        df_filtered,
        x='Kopi_per_Hari',
        y='Durasi_Belajar_Num',
        z='Skor_Produktivitas',
        color='Kualitas_Tidur_Memburuk',
        size=df_filtered['Is_Fokus_Tinggi'].apply(lambda x: 12 if x == 1 else 6),
        color_continuous_scale=['#06b6d4', '#8b5cf6', '#f472b6'],
        hover_data={'Kopi_per_Hari': ':.0f', 'Durasi_Belajar_Num': ':.1f', 'Skor_Produktivitas': ':.2f', 'Fokus_Label': True},
        labels={'Kopi_per_Hari': 'Cangkir Kopi', 'Durasi_Belajar_Num': 'Durasi Belajar (jam)', 'Skor_Produktivitas': 'Produktivitas', 'Kualitas_Tidur_Memburuk': 'Kualitas Tidur'}
    )
    
    fig_3d.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Outfit'),
        scene=dict(
            xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.2)', title='☕ Cangkir'),
            yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.2)', title='📚 Durasi'),
            zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.2)', title='⚡ Produktivitas'),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title='Tidur', tickfont=dict(color='#94a3b8'), title_font=dict(color='#94a3b8'))
    )
    fig_3d.update_traces(marker=dict(opacity=0.85, line=dict(color='rgba(255,255,255,0.3)', width=0.5)))
    st.plotly_chart(fig_3d, use_container_width=True)

# ===================== TAB 2: DESKRIPTIF =====================
with tab2:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">02</span>
        <div><h2 class="section-title">Descriptive Analytics</h2></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_dist = px.histogram(df_filtered, x='Kopi_per_Hari', nbins=5, color_discrete_sequence=['#8b5cf6'])
        fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col_b:
        fig_hist = px.histogram(df_filtered, x='Skor_Produktivitas', nbins=15, color_discrete_sequence=['#06b6d4'])
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("#### 📋 **Statistical Summary**")
    stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
    st.dataframe(stats_df.style.background_gradient(cmap='Blues', axis=1), use_container_width=True)

# ===================== TAB 3: KORELASI =====================
with tab3:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">03</span>
        <div><h2 class="section-title">Correlation Analysis</h2></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_e, col_f = st.columns([1, 1])
    with col_e:
        corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
        corr_matrix = df_filtered[corr_cols].corr(method='pearson')
        fig_heat = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale=['#0f172a', '#8b5cf6', '#f472b6'], zmin=-1, zmax=1)
        fig_heat.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_heat, use_container_width=True)
    
    with col_f:
        if len(df_filtered) > 1:
            p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
            st.markdown(f"""
            <div class="info-box">
                📊 <strong>Koefisien Pearson (r):</strong> {p_coeff:.4f}<br>
                📉 <strong>P-Value:</strong> {p_value:.4f} ({'Signifikan' if p_value < 0.05 else 'Tidak Signifikan'})
            </div>""", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(df_filtered, x='Kopi_per_Hari', y='Skor_Produktivitas', trendline='ols', color='Durasi_Belajar_Num', color_continuous_scale=['#06b6d4', '#f472b6'])
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_scatter, use_container_width=True)

# ===================== TAB 4: MONTE CARLO =====================
with tab4:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">04</span>
        <div><h2 class="section-title">Monte Carlo Simulation</h2></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_i, col_j = st.columns([1, 2])
    with col_i:
        st.markdown("#### ⚙️ **Parameters**")
        n_mahasiswa = st.slider("👥 Students per Class:", 10, 500, 100, 10)
        n_iterasi = st.slider("🔄 Iterations:", 1000, 50000, 10000, 1000)
        
        st.markdown("#### 📊 **Empirical Distribution**")
        p_kopi_dist = df['Kopi_per_Hari'].value_counts(normalize=True).sort_index()
        for cat, w in p_kopi_dist.items():
            st.markdown(f"- <b>{cat} cangkir:</b> <span style='color:#22d3ee'>{w*100:.1f}%</span>", unsafe_allow_html=True)
        
        simulate_btn = st.button("🎲 Run Simulation", type="primary", use_container_width=True)
    
    with col_j:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("⚡ Running stochastic simulation..."):
                categories_kopi = p_kopi_dist.index.values
                weights_kopi = p_kopi_dist.values
                stats_by_group = df.groupby('Kopi_per_Hari')['Skor_Produktivitas'].agg(['mean', 'std'])
                overall_std = df['Skor_Produktivitas'].std()
                stats_by_group['std'] = stats_by_group['std'].fillna(overall_std)

                hasil_rata_rata = []
                for _ in range(n_iterasi):
                    simulasi_kopi = np.random.choice(categories_kopi, size=n_mahasiswa, p=weights_kopi)
                    skor_kelas = [np.clip(np.random.normal(stats_by_group.loc[p, 'mean'], stats_by_group.loc[p, 'std']), 1.0, 5.0) for p in simulasi_kopi]
                    hasil_rata_rata.append(np.mean(skor_kelas))
                st.session_state['mc_results'] = hasil_rata_rata

        if 'mc_results' in st.session_state:
            hasil = st.session_state['mc_results']
            mean_mc = np.mean(hasil)
            ci_bawah = np.percentile(hasil, 2.5)
            ci_atas = np.percentile(hasil, 97.5)
            
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"""<div class="kpi-card" style="text-align:center"><p class="kpi-value">{mean_mc:.3f}</p><p class="kpi-label">Expected Mean</p></div>""", unsafe_allow_html=True)
            with m2: st.markdown(f"""<div class="kpi-card" style="text-align:center"><p class="kpi-value">{ci_bawah:.3f}</p><p class="kpi-label">CI 95% Lower</p></div>""", unsafe_allow_html=True)
            with m3: st.markdown(f"""<div class="kpi-card" style="text-align:center"><p class="kpi-value">{ci_atas:.3f}</p><p class="kpi-label">CI 95% Upper</p></div>""", unsafe_allow_html=True)
            
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(x=hasil, nbinsx=50, marker=dict(color='rgba(139, 92, 246, 0.6)', line=dict(color='#8b5cf6', width=1))))
            fig_mc.add_vline(x=mean_mc, line_dash="dash", line_color="#22d3ee", annotation_text=f"Mean: {mean_mc:.3f}", annotation_font_color="#22d3ee")
            fig_mc.add_vline(x=ci_bawah, line_dash="dot", line_color="#f472b6", annotation_text=f"CI: {ci_bawah:.3f}", annotation_font_color="#f472b6")
            fig_mc.add_vline(x=ci_atas, line_dash="dot", line_color="#f472b6", annotation_text=f"CI: {ci_atas:.3f}", annotation_font_color="#f472b6")
            
            fig_mc.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Outfit'),
                xaxis=dict(title="Average Productivity Score", gridcolor='rgba(255,255,255,0.1)', color='#94a3b8'),
                yaxis=dict(title="Frequency", gridcolor='rgba(255,255,255,0.1)', color='#94a3b8'),
                height=400, margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_mc, use_container_width=True)

# --- FOOTER ---
st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Dashboard Pro</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Data Source: Student Questionnaire (n=31) | Powered by Streamlit, Pandas & Plotly 3D</p>
</div>
""", unsafe_allow_html=True)
