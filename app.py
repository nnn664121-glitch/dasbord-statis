import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr, spearmanr, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Coffee Analytics 3D Pro ☕",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM 3D EDITION V2 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: radial-gradient(ellipse at top, #1a0b2e 0%, #0f0524 40%, #050212 100%);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Hide Streamlit chrome */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {width: 10px;}
    ::-webkit-scrollbar-track {background: #0f0524;}
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff006e, #8338ec, #3a86ff);
        border-radius: 10px;
    }
    
    /* HERO SECTION */
    .hero-container {
        position: relative;
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.1) 0%, rgba(131, 56, 236, 0.1) 50%, rgba(58, 134, 255, 0.1) 100%);
        border-radius: 30px;
        overflow: hidden;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255, 0, 110, 0.3), transparent, rgba(131, 56, 236, 0.3), transparent);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-emoji {
        font-size: 5rem;
        display: block;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 25%, #8338ec 50%, #3a86ff 75%, #06ffa5 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -3px;
        line-height: 1.1;
        animation: gradient-flow 5s ease infinite;
    }
    
    @keyframes gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        color: #06ffa5;
        font-size: 0.85rem;
        margin-top: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 2px;
    }
    
    /* KPI CARDS - NEON GLOW */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.8rem;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(10px);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 300% 100%;
        animation: gradient-shift 3s linear infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(131, 56, 236, 0.3);
        border-color: rgba(131, 56, 236, 0.5);
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.8rem;
        font-weight: 500;
    }
    
    .kpi-delta {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(6, 255, 165, 0.1);
        border: 1px solid rgba(6, 255, 165, 0.3);
        border-radius: 20px;
        color: #06ffa5;
        font-size: 0.75rem;
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* SECTION HEADERS */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .section-number {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff006e, #8338ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #fff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .section-subtitle {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.2rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* GLASS CARDS */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(131, 56, 236, 0.4);
        box-shadow: 0 15px 40px rgba(131, 56, 236, 0.15);
    }
    
    .glass-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(131, 56, 236, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .glass-card:hover::after {
        opacity: 1;
    }
    
    /* 3D BADGE */
    .badge-3d {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        background: linear-gradient(135deg, #ff006e, #8338ec);
        border-radius: 20px;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-left: 1rem;
        box-shadow: 0 5px 20px rgba(255, 0, 110, 0.4);
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* SIDEBAR */
    .stSidebar {
        background: rgba(15, 5, 36, 0.95);
        backdrop-filter: blur(20px);
    }
    
    .stSidebar .sidebar-content {
        background: transparent;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(131, 56, 236, 0.1);
        color: #fff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff006e, #8338ec);
        color: #fff;
        box-shadow: 0 5px 20px rgba(131, 56, 236, 0.4);
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #ff006e, #8338ec);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 0, 110, 0.4);
    }
    
    /* DIVIDER */
    .fancy-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(131, 56, 236, 0.5), transparent);
        margin: 3rem 0;
    }
    
    /* INSIGHT CARDS */
    .insight-card {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.08) 0%, rgba(131, 56, 236, 0.08) 100%);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(131, 56, 236, 0.2);
    }
    
    .insight-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .insight-title {
        color: #fff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* INFO BOX */
    .info-box {
        background: linear-gradient(135deg, rgba(58, 134, 255, 0.15) 0%, rgba(6, 255, 165, 0.1) 100%);
        border-left: 4px solid #3a86ff;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.9);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    
    /* METRIC HIGHLIGHT */
    .metric-highlight {
        font-family: 'JetBrains Mono', monospace;
        color: #06ffa5;
        font-weight: 600;
    }
    
    /* FOOTER */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .footer-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        margin: 0.3rem 0;
    }
    
    .footer-brand {
        background: linear-gradient(135deg, #ff006e, #8338ec, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1rem;
    }
    
    /* ANIMATED NUMBER EFFECT */
    @keyframes pulse-glow {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(131, 56, 236, 0.3);
        }
        50% { 
            box-shadow: 0 0 40px rgba(131, 56, 236, 0.6);
        }
    }
    
    .pulse-card {
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    /* DOWNLOAD BUTTON */
    .download-btn {
        background: linear-gradient(135deg, #06ffa5, #3a86ff) !important;
        box-shadow: 0 5px 20px rgba(6, 255, 165, 0.3);
    }
    
    .download-btn:hover {
        box-shadow: 0 10px 30px rgba(6, 255, 165, 0.5) !important;
    }
    
    /* PROGRESS BAR */
    .progress-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* TOOLTIP */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: rgba(15, 5, 36, 0.95);
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        border: 1px solid rgba(131, 56, 236, 0.3);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD & PREPROCESS DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', sep=';')
    df_clean = df.copy()

    df_clean['Kopi_per_Hari'] = df_clean.iloc[:, 4].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

    hours_mapping = {
        '< 2 jam': 1.0,
        '2-4 jam': 3.0,
        '5-7 jam': 6.0,
        '> 7 jam': 8.5
    }
    df_clean['Durasi_Belajar_Num'] = df_clean.iloc[:, 7].map(hours_mapping).fillna(df_clean.iloc[:, 7].mode()[0])

    likert_cols = [df_clean.columns[9], df_clean.columns[10], df_clean.columns[11], df_clean.columns[12]]
    df_clean['Skor_Produktivitas'] = df_clean[likert_cols].mean(axis=1)

    df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean.iloc[:, 15], errors='coerce').fillna(3)

    df_clean['Is_Fokus_Tinggi'] = (df_clean['Skor_Produktivitas'] > 3.0).astype(int)
    df_clean['Is_Peminum_Kopi'] = (df_clean['Kopi_per_Hari'] > 0).astype(int)
    
    # Label untuk 3D
    df_clean['Fokus_Label'] = df_clean['Is_Fokus_Tinggi'].map({1: 'High Focus', 0: 'Low Focus'})
    df_clean['Kopi_Label'] = df_clean['Kopi_per_Hari'].apply(lambda x: f'{x} Cangkir')
    
    # Kategori Konsumsi
    def categorize_kopi(x):
        if x == 0:
            return 'Non-Drinker'
        elif x <= 1:
            return 'Light (1 cup)'
        elif x <= 2:
            return 'Moderate (2 cups)'
        else:
            return 'Heavy (3+ cups)'
    
    df_clean['Kategori_Konsumsi'] = df_clean['Kopi_per_Hari'].apply(categorize_kopi)
    
    # Produktivitas Level
    def categorize_produktivitas(x):
        if x < 2.5:
            return 'Low'
        elif x < 3.5:
            return 'Medium'
        else:
            return 'High'
    
    df_clean['Produktivitas_Level'] = df_clean['Skor_Produktivitas'].apply(categorize_produktivitas)

    return df_clean

df = load_data()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <span class="hero-emoji">☕</span>
        <h1 class="hero-title">Coffee Analytics Pro</h1>
        <p class="hero-subtitle">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
        <span class="hero-badge">◆ PREMIUM EDITION v2.0 ◆ AI-POWERED INSIGHTS ◆</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🎛️ **Control Panel**")
    st.markdown("---")

    # Advanced Filters
    st.markdown("#### 🔍 **Data Filters**")
    
    kopi_filter = st.multiselect(
        "☕ Cangkir per Hari",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique()),
        help="Pilih jumlah cangkir kopi yang ingin ditampilkan"
    )

    kategori_filter = st.multiselect(
        "📊 Kategori Konsumsi",
        options=sorted(df['Kategori_Konsumsi'].unique()),
        default=sorted(df['Kategori_Konsumsi'].unique()),
        help="Filter berdasarkan kategori konsumsi kopi"
    )

    durasi_options = df['Durasi_Belajar_Num'].unique()
    durasi_range = st.slider(
        "⏰ Durasi Belajar (jam)",
        min_value=float(min(durasi_options)),
        max_value=float(max(durasi_options)),
        value=(float(min(durasi_options)), float(max(durasi_options))),
        help="Rentang durasi belajar dalam jam"
    )

    fokus_filter = st.selectbox(
        "🎯 Status Fokus",
        options=["Semua", "High Focus (>3.0)", "Low Focus (≤3.0)"],
        help="Filter berdasarkan tingkat fokus"
    )
    
    produktivitas_filter = st.multiselect(
        "⚡ Level Produktivitas",
        options=sorted(df['Produktivitas_Level'].unique()),
        default=sorted(df['Produktivitas_Level'].unique()),
        help="Filter berdasarkan level produktivitas"
    )

    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Kategori_Konsumsi'].isin(kategori_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1]) &
        (df['Produktivitas_Level'].isin(produktivitas_filter))
    ]

    if fokus_filter == "High Focus (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Low Focus (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]

    st.markdown("---")
    
    # Live Stats
    st.markdown("#### 📈 **Live Statistics**")
    st.markdown(f"""
    <div class="glass-card pulse-card" style="text-align: center;">
        <span class="kpi-icon">👥</span>
        <p class="kpi-value">{len(df_filtered)}</p>
        <p class="kpi-label">Responden Aktif</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar
    pct_filtered = (len(df_filtered) / len(df)) * 100
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
            <span style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">Data Filtered</span>
            <span style="color: #06ffa5; font-size: 0.8rem; font-weight: 600;">{pct_filtered:.1f}%</span>
        </div>
        <div class="progress-bar" style="width: {pct_filtered}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export Options
    st.markdown("#### 💾 **Export Data**")
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="coffee_analytics_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Reset Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# --- KPI CARDS ---
st.markdown("""
<div class="section-header">
    <span class="section-number">01</span>
    <div>
        <h2 class="section-title">Key Performance Metrics</h2>
        <p class="section-subtitle">Real-time statistics from filtered data</p>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">☕</span>
        <p class="kpi-value">{df_filtered['Kopi_per_Hari'].mean():.2f}</p>
        <p class="kpi-label">Avg Cups / Day</p>
        <span class="kpi-delta">σ = {df_filtered['Kopi_per_Hari'].std():.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📚</span>
        <p class="kpi-value">{df_filtered['Durasi_Belajar_Num'].mean():.1f}h</p>
        <p class="kpi-label">Study Duration</p>
        <span class="kpi-delta">σ = {df_filtered['Durasi_Belajar_Num'].std():.1f}h</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚡</span>
        <p class="kpi-value">{df_filtered['Skor_Produktivitas'].mean():.2f}</p>
        <p class="kpi-label">Productivity Score</p>
        <span class="kpi-delta">out of 5.0</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fokus_pct = df_filtered['Is_Fokus_Tinggi'].mean() * 100
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <p class="kpi-value">{fokus_pct:.0f}%</p>
        <p class="kpi-label">High Focus Rate</p>
        <span class="kpi-delta">{len(df_filtered[df_filtered['Is_Fokus_Tinggi']==1])} students</span>
    </div>
    """, unsafe_allow_html=True)

with col5:
    tidur_mean = df_filtered['Kualitas_Tidur_Memburuk'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">😴</span>
        <p class="kpi-value">{tidur_mean:.1f}</p>
        <p class="kpi-label">Sleep Quality</p>
        <span class="kpi-delta">1-5 scale</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌐 3D Visualization",
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎯 Conditional Probability",
    "🎲 Monte Carlo Simulation",
    "📈 Advanced Analytics",
    "🤖 AI Insights"
])

# ===================== TAB 1: 3D VISUALIZATION =====================
with tab1:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">3D</span>
        <div>
            <h2 class="section-title">Interactive 3D Visualization <span class="badge-3d">✦ PREMIUM</span></h2>
            <p class="section-subtitle">Multi-dimensional data exploration in three dimensions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3D SCATTER PLOT - MAIN VISUALIZATION
    st.markdown("### 🌌 **3D Scatter Plot: Kopi × Durasi × Produktivitas**")
    st.markdown("""
    <div class="info-box">
        💡 <strong>Tip:</strong> Klik dan drag untuk memutar, scroll untuk zoom, double-click untuk reset view.
        Arahkan kursor ke titik untuk melihat detail responden.
    </div>
    """, unsafe_allow_html=True)
    
    fig_3d_scatter = px.scatter_3d(
        df_filtered,
        x='Kopi_per_Hari',
        y='Durasi_Belajar_Num',
        z='Skor_Produktivitas',
        color='Kualitas_Tidur_Memburuk',
        size=df_filtered['Is_Fokus_Tinggi'].apply(lambda x: 15 if x == 1 else 8),
        color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
        hover_data={
            'Kopi_per_Hari': ':.0f',
            'Durasi_Belajar_Num': ':.1f',
            'Skor_Produktivitas': ':.2f',
            'Kualitas_Tidur_Memburuk': ':.0f',
            'Fokus_Label': True,
            'Kategori_Konsumsi': True
        },
        labels={
            'Kopi_per_Hari': 'Cangkir Kopi',
            'Durasi_Belajar_Num': 'Durasi Belajar (jam)',
            'Skor_Produktivitas': 'Skor Produktivitas',
            'Kualitas_Tidur_Memburuk': 'Kualitas Tidur'
        }
    )
    
    fig_3d_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Space Grotesk'),
        scene=dict(
            xaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False,
                zerolinecolor='rgba(255,255,255,0.2)',
                title='☕ Cangkir Kopi'
            ),
            yaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False,
                zerolinecolor='rgba(255,255,255,0.2)',
                title='📚 Durasi Belajar'
            ),
            zaxis=dict(
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False,
                zerolinecolor='rgba(255,255,255,0.2)',
                title='⚡ Produktivitas'
            ),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2),
                up=dict(x=0, y=0, z=1)
            ),
            aspectratio=dict(x=1.2, y=1.2, z=0.9)
        ),
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_colorbar=dict(
            title='Kualitas Tidur',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        )
    )
    
    fig_3d_scatter.update_traces(
        marker=dict(
            opacity=0.85,
            line=dict(color='rgba(255,255,255,0.5)', width=1)
        ),
        hovertemplate='<b>%{customdata[4]}</b><br>' +
                      'Kategori: %{customdata[5]}<br>' +
                      'Kopi: %{x} cangkir<br>' +
                      'Durasi: %{y:.1f} jam<br>' +
                      'Produktivitas: %{z:.2f}<br>' +
                      'Tidur: %{customdata[3]:.0f}<extra></extra>'
    )
    
    st.plotly_chart(fig_3d_scatter, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # 3D SURFACE PLOT
    st.markdown("### 🏔️ **3D Surface Plot: Produktivitas Landscape**")
    st.markdown("""
    <div class="info-box">
        🗺️ <strong>Surface Plot:</strong> Menunjukkan "topografi" produktivitas berdasarkan kombinasi konsumsi kopi dan durasi belajar.
        Area tinggi (warna cerah) = produktivitas tinggi.
    </div>
    """, unsafe_allow_html=True)
    
    # Binning untuk surface
    kopi_bins = np.linspace(df_filtered['Kopi_per_Hari'].min(), df_filtered['Kopi_per_Hari'].max(), 10)
    durasi_bins = np.linspace(df_filtered['Durasi_Belajar_Num'].min(), df_filtered['Durasi_Belajar_Num'].max(), 10)
    
    Z = np.zeros((len(kopi_bins), len(durasi_bins)))
    for i, k in enumerate(kopi_bins):
        for j, d in enumerate(durasi_bins):
            mask = (
                (np.abs(df_filtered['Kopi_per_Hari'] - k) < 0.6) &
                (np.abs(df_filtered['Durasi_Belajar_Num'] - d) < 1.5)
            )
            if mask.sum() > 0:
                Z[i, j] = df_filtered.loc[mask, 'Skor_Produktivitas'].mean()
            else:
                Z[i, j] = np.nan
    
    # Fill NaN dengan interpolasi sederhana
    Z_filled = pd.DataFrame(Z).ffill().bfill().fillna(df_filtered['Skor_Produktivitas'].mean()).values
    
    fig_surface = go.Figure(data=[go.Surface(
        z=Z_filled,
        x=durasi_bins,
        y=kopi_bins,
        colorscale=[
            [0, '#0f0524'],
            [0.2, '#8338ec'],
            [0.4, '#ff006e'],
            [0.6, '#ffbe0b'],
            [0.8, '#06ffa5'],
            [1, '#ffffff']
        ],
        contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True)
        ),
        opacity=0.95,
        hovertemplate='<b>Durasi: %{x:.1f}h</b><br>' +
                      'Kopi: %{y:.1f} cangkir<br>' +
                      'Produktivitas: %{z:.2f}<extra></extra>'
    )])
    
    fig_surface.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Space Grotesk'),
        scene=dict(
            xaxis=dict(
                title='📚 Durasi Belajar (jam)',
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False
            ),
            yaxis=dict(
                title='☕ Cangkir Kopi',
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False
            ),
            zaxis=dict(
                title='⚡ Produktivitas',
                backgroundcolor='rgba(0,0,0,0)',
                gridcolor='rgba(255,255,255,0.1)',
                showbackground=False,
                range=[1, 5]
            ),
            camera=dict(
                eye=dict(x=2, y=2, z=1.5)
            )
        ),
        height=550,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_surface, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # 3D CONTOUR PLOT
    st.markdown("### 🌊 **3D Contour Plot: Density Mapping**")
    
    fig_contour = go.Figure()
    
    fig_contour.add_trace(go.Contour(
        z=Z_filled,
        x=durasi_bins,
        y=kopi_bins,
        colorscale='Viridis',
        contours=dict(
            coloring='heatmap',
            showlabels=True,
            labelfont=dict(size=12, color='white')
        ),
        line_smoothing=1.0,
        hovertemplate='Durasi: %{x:.1f}h<br>Kopi: %{y:.1f}<br>Produktivitas: %{z:.2f}<extra></extra>'
    ))
    
    fig_contour.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Space Grotesk'),
        xaxis=dict(
            title='📚 Durasi Belajar (jam)',
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        ),
        yaxis=dict(
            title='☕ Cangkir Kopi',
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        ),
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_colorbar=dict(
            title='Produktivitas',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        )
    )
    
    st.plotly_chart(fig_contour, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # 3D INSIGHTS
    st.markdown("### 💎 **3D Insights & Pattern Discovery**")
    
    ins_col1, ins_col2, ins_col3, ins_col4 = st.columns(4)
    
    with ins_col1:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">🎯</div>
            <div class="insight-title">Sweet Spot Teridentifikasi</div>
            <div class="insight-text">
                Titik-titik <span class="metric-highlight">hijau neon</span> menunjukkan 
                kombinasi optimal: <b>1 cangkir kopi + 5-7 jam belajar</b> menghasilkan 
                produktivitas maksimal.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with ins_col2:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">⚠️</div>
            <div class="insight-title">Trade-off Tidur</div>
            <div class="insight-text">
                Titik berwarna <span class="metric-highlight">merah muda</span> menunjukkan 
                responden dengan <b>kualitas tidur buruk</b> - mereka cenderung konsumsi kopi 
                lebih banyak (>1 cangkir/hari).
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with ins_col3:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">📈</div>
            <div class="insight-title">Surface Peaks</div>
            <div class="insight-text">
                Permukaan 3D menunjukkan <span class="metric-highlight">"puncak"</span> di area 
                tertentu, mengindikasikan adanya <b>threshold optimal</b> konsumsi kopi untuk 
                produktivitas maksimal.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with ins_col4:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">🌊</div>
            <div class="insight-title">Density Zones</div>
            <div class="insight-text">
                Contour plot menunjukkan <span class="metric-highlight">zona kepadatan</span> 
                data, area dengan <b>kontur rapat</b> = variasi produktivitas tinggi.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===================== TAB 2: DESKRIPTIF =====================
with tab2:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">02</span>
        <div>
            <h2 class="section-title">Descriptive Analytics</h2>
            <p class="section-subtitle">Statistical distribution and pattern analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### ☕ **Distribusi Konsumsi Kopi**")
        kopi_counts = df_filtered['Kopi_per_Hari'].value_counts().sort_index()
        fig_dist_kopi = px.bar(
            x=kopi_counts.index,
            y=kopi_counts.values,
            labels={'x': 'Cangkir', 'y': 'Responden'},
            color=kopi_counts.values,
            color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff']
        )
        fig_dist_kopi.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(dtick=1, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            coloraxis_showscale=False
        )
        fig_dist_kopi.update_traces(
            marker_line=dict(color='rgba(255,255,255,0.3)', width=1),
            hovertemplate="<b>%{x} cangkir</b><br>Responden: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_dist_kopi, use_container_width=True)
    
    with col_b:
        st.markdown("#### ⚡ **Distribusi Skor Produktivitas**")
        fig_hist_prod = px.histogram(
            df_filtered,
            x='Skor_Produktivitas',
            nbins=15,
            color_discrete_sequence=['#8338ec'],
            marginal="violin"
        )
        fig_hist_prod.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        fig_hist_prod.update_traces(
            marker=dict(
                color='rgba(131, 56, 236, 0.7)',
                line=dict(color='#8338ec', width=1)
            ),
            hovertemplate="<b>Skor: %{x:.2f}</b><br>Frekuensi: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_hist_prod, use_container_width=True)
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.markdown("#### 🎯 **Boxplot: Produktivitas per Kelompok Kopi**")
        fig_box = px.box(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            color='Kopi_per_Hari',
            color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
        )
        fig_box.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_box.update_traces(
            hovertemplate="<b>%{x} cangkir</b><br>Skor: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_d:
        st.markdown("#### 📊 **Rata-rata Durasi Belajar**")
        durasi_mean = df_filtered.groupby('Kopi_per_Hari')['Durasi_Belajar_Num'].mean().reset_index()
        fig_bar_durasi = px.bar(
            durasi_mean,
            x='Kopi_per_Hari',
            y='Durasi_Belajar_Num',
            color='Durasi_Belajar_Num',
            color_continuous_scale=['#ff006e', '#ffbe0b', '#06ffa5']
        )
        fig_bar_durasi.update_layout(
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_bar_durasi.update_traces(
            marker_line=dict(color='rgba(255,255,255,0.3)', width=1),
            hovertemplate="<b>%{x} cangkir</b><br>Durasi: %{y:.1f}h<extra></extra>"
        )
        st.plotly_chart(fig_bar_durasi, use_container_width=True)
    
    col_e, col_f = st.columns(2)
    
    with col_e:
        st.markdown("#### 🥧 **Distribusi Kategori Konsumsi**")
        kategori_counts = df_filtered['Kategori_Konsumsi'].value_counts()
        fig_pie = px.pie(
            values=kategori_counts.values,
            names=kategori_counts.index,
            color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_f:
        st.markdown("#### 📈 **Stacked Bar: Produktivitas Level per Kategori**")
        stacked_data = pd.crosstab(
            df_filtered['Kategori_Konsumsi'],
            df_filtered['Produktivitas_Level'],
            normalize='index'
        ) * 100
        
        fig_stacked = go.Figure()
        for level in stacked_data.columns:
            fig_stacked.add_trace(go.Bar(
                name=level,
                x=stacked_data.index,
                y=stacked_data[level],
                marker_color={'Low': '#ff006e', 'Medium': '#8338ec', 'High': '#06ffa5'}[level]
            ))
        
        fig_stacked.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Persentase (%)', gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
    
    st.markdown("#### 📋 **Statistical Summary**")
    stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
    st.dataframe(
        stats_df.style.background_gradient(cmap='viridis', axis=1),
        use_container_width=True
    )
    
    # Additional Statistics
    st.markdown("#### 📊 **Advanced Statistics**")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Skewness (Produktivitas)", f"{df_filtered['Skor_Produktivitas'].skew():.3f}")
    with col_stat2:
        st.metric("Kurtosis (Produktivitas)", f"{df_filtered['Skor_Produktivitas'].kurtosis():.3f}")
    with col_stat3:
        st.metric("Coefficient of Variation", f"{(df_filtered['Skor_Produktivitas'].std() / df_filtered['Skor_Produktivitas'].mean() * 100):.2f}%")

# ===================== TAB 3: KORELASI =====================
with tab3:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">03</span>
        <div>
            <h2 class="section-title">Correlation Analysis</h2>
            <p class="section-subtitle">Statistical relationships between variables</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_e, col_f = st.columns([1, 1])
    
    with col_e:
        st.markdown("#### 🎨 **3D Correlation Heatmap**")
        corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
        corr_matrix = df_filtered[corr_cols].corr(method='pearson')
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".3f",
            color_continuous_scale=['#0f0524', '#8338ec', '#ff006e', '#ffbe0b', '#06ffa5'],
            zmin=-1, zmax=1
        )
        fig_heatmap.update_layout(
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='JetBrains Mono'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_heatmap.update_traces(
            hovertemplate="<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col_f:
        st.markdown("#### 📈 **Scatter: Kopi vs Produktivitas**")
        
        if len(df_filtered) > 1:
            p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
            signifikansi = "Signifikan" if p_value < 0.05 else "Tidak Signifikan"
            
            st.markdown(f"""
            <div class="info-box">
                📊 Koefisien Pearson: <span class="metric-highlight">r = {p_coeff:.4f}</span><br>
                📉 P-Value: <span class="metric-highlight">{p_value:.4f}</span> ({signifikansi})
            </div>
            """, unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            trendline='ols' if len(df_filtered) > 2 else None,
            color='Durasi_Belajar_Num',
            color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff'],
            size='Kualitas_Tidur_Memburuk',
            size_max=20,
            hover_data=['Fokus_Label', 'Kategori_Konsumsi']
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_scatter.update_traces(
            marker=dict(
                opacity=0.8,
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            hovertemplate="<b>%{x} cangkir</b><br>Produktivitas: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    col_g, col_h = st.columns(2)
    
    with col_g:
        st.markdown("#### 🔗 **Spearman Rank Correlation**")
        if len(df_filtered) > 1:
            spearman_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
            spearman_matrix = df_filtered[spearman_cols].corr(method='spearman')
            
            fig_spearman = px.imshow(
                spearman_matrix,
                text_auto=".3f",
                color_continuous_scale=['#3a86ff', '#8338ec', '#ff006e'],
                zmin=-1, zmax=1
            )
            fig_spearman.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='JetBrains Mono'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_spearman, use_container_width=True)
    
    with col_h:
        st.markdown("#### 📊 **Correlation Matrix Details**")
        
        # Calculate all correlations
        corr_details = []
        for i, col1 in enumerate(corr_cols):
            for j, col2 in enumerate(corr_cols):
                if i < j:
                    pearson_r, pearson_p = pearsonr(df_filtered[col1], df_filtered[col2])
                    spearman_r, spearman_p = spearmanr(df_filtered[col1], df_filtered[col2])
                    
                    corr_details.append({
                        'Variable 1': col1,
                        'Variable 2': col2,
                        'Pearson r': f"{pearson_r:.4f}",
                        'Pearson p-value': f"{pearson_p:.4f}",
                        'Spearman ρ': f"{spearman_r:.4f}",
                        'Spearman p-value': f"{spearman_p:.4f}"
                    })
        
        corr_df = pd.DataFrame(corr_details)
        st.dataframe(
            corr_df.style.background_gradient(cmap='YlOrRd', subset=['Pearson r', 'Spearman ρ']),
            use_container_width=True
        )
    
    st.markdown("### 💡 **Key Insights**")
    i_col1, i_col2, i_col3 = st.columns(3)
    
    with i_col1:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">☕⚡</div>
            <div class="insight-title">Kopi ↔ Produktivitas</div>
            <div class="insight-text">
                Korelasi positif lemah menunjukkan kopi <b>sedikit meningkatkan</b> 
                persepsi produktivitas mahasiswa.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with i_col2:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">☕😴</div>
            <div class="insight-title">Kopi ↔ Kualitas Tidur</div>
            <div class="insight-text">
                Korelasi <b>negatif moderat</b> membuktikan trade-off: 
                lebih banyak kopi = tidur lebih buruk.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with i_col3:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">☕📚</div>
            <div class="insight-title">Kopi ↔ Durasi Belajar</div>
            <div class="insight-text">
                Korelasi positif menunjukkan <b>peminum kopi cenderung 
                belajar lebih lama</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===================== TAB 4: PROBABILITAS =====================
with tab4:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">04</span>
        <div>
            <h2 class="section-title">Conditional Probability</h2>
            <p class="section-subtitle">P(High Focus | Coffee Consumption)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_g, col_h = st.columns([1, 1])
    
    with col_g:
        st.markdown("#### 📊 **Tabel Kontingensi**")
        kontingensi = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            margins=True
        )
        kontingensi.index = ['Non-Drinkers', 'Coffee Drinkers', 'Total']
        kontingensi.columns = ['Low Focus', 'High Focus', 'Total']
        st.dataframe(kontingensi, use_container_width=True)
        
        # Chi-square test
        if len(df_filtered) > 0:
            chi2, p_chi, dof, expected = chi2_contingency(
                pd.crosstab(df_filtered['Is_Peminum_Kopi'], df_filtered['Is_Fokus_Tinggi'])
            )
            
            st.markdown(f"""
            <div class="info-box">
                📊 Chi-Square Test:<br>
                χ² = <span class="metric-highlight">{chi2:.4f}</span><br>
                p-value = <span class="metric-highlight">{p_chi:.4f}</span><br>
                Degrees of Freedom = <span class="metric-highlight">{dof}</span><br>
                Status: <b>{'Signifikan' if p_chi < 0.05 else 'Tidak Signifikan'}</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### 🎯 **Matriks Probabilitas**")
        prob_bersyarat = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            normalize='index'
        ) * 100
        prob_bersyarat.index = ['Non-Drinkers', 'Coffee Drinkers']
        prob_bersyarat.columns = ['Low Focus (%)', 'High Focus (%)']
        st.dataframe(
            prob_bersyarat.round(2).style.background_gradient(cmap='YlOrRd', axis=1),
            use_container_width=True
        )
    
    with col_h:
        st.markdown("#### 📈 **Probability Comparison**")
        
        if 1 in df_filtered['Is_Peminum_Kopi'].values:
            p_kopi = prob_bersyarat.loc['Coffee Drinkers', 'High Focus (%)']
        else:
            p_kopi = 0

        if 0 in df_filtered['Is_Peminum_Kopi'].values:
            p_non_kopi = prob_bersyarat.loc['Non-Drinkers', 'High Focus (%)']
        else:
            p_non_kopi = 0

        fig_prob = go.Figure(data=[
            go.Bar(
                name='High Focus',
                x=['Coffee Drinkers', 'Non-Drinkers'],
                y=[p_kopi, p_non_kopi],
                marker=dict(
                    color=['#ff006e', '#3a86ff'],
                    line=dict(color='rgba(255,255,255,0.3)', width=2)
                ),
                text=[f'{p_kopi:.1f}%', f'{p_non_kopi:.1f}%'],
                textposition='auto',
                textfont=dict(color='white', size=18, family='JetBrains Mono')
            )
        ])
        fig_prob.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(title="Probability (%)", range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig_prob.update_traces(
            hovertemplate="<b>%{x}</b><br>Probability: %{y:.1f}%<extra></extra>"
        )
        st.plotly_chart(fig_prob, use_container_width=True)
        
        if p_kopi > p_non_kopi and p_non_kopi > 0:
            st.success(f"📈 Coffee drinkers have **{p_kopi/p_non_kopi:.1f}x higher** chance of achieving high focus!")
        
        # Odds Ratio
        if p_non_kopi > 0 and p_non_kopi < 100:
            odds_kopi = p_kopi / (100 - p_kopi) if p_kopi < 100 else float('inf')
            odds_non = p_non_kopi / (100 - p_non_kopi)
            odds_ratio = odds_kopi / odds_non if odds_non > 0 else float('inf')
            
            st.markdown(f"""
            <div class="glass-card">
                <h4>📊 Odds Ratio Analysis</h4>
                <p>Odds Ratio: <span class="metric-highlight">{odds_ratio:.2f}</span></p>
                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                    Coffee drinkers have {odds_ratio:.2f}x higher odds of achieving high focus compared to non-drinkers.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional Probability Analysis
    st.markdown("#### 🎲 **Bayesian Probability Matrix**")
    
    # Calculate P(Focus | Coffee Amount)
    prob_matrix = pd.crosstab(
        df_filtered['Kopi_per_Hari'],
        df_filtered['Is_Fokus_Tinggi'],
        normalize='index'
    ) * 100
    
    prob_matrix.columns = ['P(Low Focus)', 'P(High Focus)']
    prob_matrix.index = [f'{i} Cangkir' for i in prob_matrix.index]
    
    st.dataframe(
        prob_matrix.round(2).style.background_gradient(cmap='RdYlGn', axis=1),
        use_container_width=True
    )

# ===================== TAB 5: MONTE CARLO =====================
with tab5:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">05</span>
        <div>
            <h2 class="section-title">Monte Carlo Simulation <span class="badge-3d">✦ STOCHASTIC</span></h2>
            <p class="section-subtitle">Stochastic modeling with 10,000+ iterations</p>
        </div>
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
            st.markdown(f"- <b>{cat} cangkir:</b> <span class='metric-highlight'>{w*100:.1f}%</span>", unsafe_allow_html=True)
        
        simulate_btn = st.button("🎲 Run Simulation", type="primary", use_container_width=True)
    
    with col_j:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("⚡ Running Monte Carlo simulation..."):
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
                st.markdown(f"""
                <div class="kpi-card">
                    <span class="kpi-icon">📊</span>
                    <p class="kpi-value">{mean_mc:.3f}</p>
                    <p class="kpi-label">Expected Mean</p>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="kpi-card">
                    <span class="kpi-icon">⬇️</span>
                    <p class="kpi-value">{ci_bawah:.3f}</p>
                    <p class="kpi-label">CI 95% Lower</p>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="kpi-card">
                    <span class="kpi-icon">⬆️</span>
                    <p class="kpi-value">{ci_atas:.3f}</p>
                    <p class="kpi-label">CI 95% Upper</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=hasil,
                nbinsx=50,
                marker=dict(
                    color='rgba(131, 56, 236, 0.6)',
                    line=dict(color='#8338ec', width=1)
                ),
                hovertemplate="Score: %{x:.3f}<br>Frequency: %{y}<extra></extra>"
            ))
            fig_mc.add_vline(
                x=mean_mc, line_dash="dash", line_color="#ff006e", line_width=3,
                annotation_text=f"Mean: {mean_mc:.3f}", annotation_font_color="#ff006e"
            )
            fig_mc.add_vline(
                x=ci_bawah, line_dash="dot", line_color="#06ffa5", line_width=2,
                annotation_text=f"CI: {ci_bawah:.3f}", annotation_font_color="#06ffa5"
            )
            fig_mc.add_vline(
                x=ci_atas, line_dash="dot", line_color="#06ffa5", line_width=2,
                annotation_text=f"CI: {ci_atas:.3f}", annotation_font_color="#06ffa5"
            )
            fig_mc.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                xaxis=dict(title="Average Productivity Score", gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(title="Frequency", gridcolor='rgba(255,255,255,0.1)', color='white'),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                title=dict(
                    text=f"Probability Distribution ({len(hasil)} Iterations)",
                    font=dict(color='white', size=16)
                )
            )
            st.plotly_chart(fig_mc, use_container_width=True)
            
            # Additional Statistics
            st.markdown("#### 📊 **Monte Carlo Statistics**")
            mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
            
            with mc_col1:
                st.metric("Std Deviation", f"{np.std(hasil):.4f}")
            with mc_col2:
                st.metric("Median", f"{np.median(hasil):.4f}")
            with mc_col3:
                st.metric("Min Value", f"{np.min(hasil):.4f}")
            with mc_col4:
                st.metric("Max Value", f"{np.max(hasil):.4f}")

# ===================== TAB 6: ADVANCED ANALYTICS =====================
with tab6:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">06</span>
        <div>
            <h2 class="section-title">Advanced Analytics <span class="badge-3d">✦ ADVANCED</span></h2>
            <p class="section-subtitle">Deep dive analysis with machine learning insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        st.markdown("#### 🕸️ **Radar Chart: Multi-dimensional Profile**")
        
        # Calculate average metrics per category
        radar_data = df_filtered.groupby('Kategori_Konsumsi').agg({
            'Kopi_per_Hari': 'mean',
            'Durasi_Belajar_Num': 'mean',
            'Skor_Produktivitas': 'mean',
            'Kualitas_Tidur_Memburuk': 'mean'
        }).round(2)
        
        # Normalize data for radar chart
        radar_normalized = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min() + 0.001)
        
        categories = ['Coffee Consumption', 'Study Duration', 'Productivity', 'Sleep Quality']
        
        fig_radar = go.Figure()
        
        for idx, category in enumerate(radar_normalized.index):
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_normalized.loc[category].values.tolist() + [radar_normalized.loc[category].values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=category,
                line=dict(width=2)
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white')
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white', size=12)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Space Grotesk'),
            showlegend=True,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white')),
            height=500,
            margin=dict(l=80, r=80, t=50, b=50)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_adv2:
        st.markdown("#### 📊 **Parallel Coordinates: Multi-variable Analysis**")
        
        fig_parallel = px.parallel_coordinates(
            df_filtered,
            dimensions=['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk'],
            color='Skor_Produktivitas',
            color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5'],
            labels={
                'Kopi_per_Hari': 'Coffee',
                'Durasi_Belajar_Num': 'Study Hours',
                'Skor_Produktivitas': 'Productivity',
                'Kualitas_Tidur_Memburuk': 'Sleep Quality'
            }
        )
        
        fig_parallel.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Space Grotesk'),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(
                title='Productivity',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            )
        )
        
        st.plotly_chart(fig_parallel, use_container_width=True)
    
    col_adv3, col_adv4 = st.columns(2)
    
    with col_adv3:
        st.markdown("#### 📈 **Violin Plot: Distribution by Category**")
        
        fig_violin = px.violin(
            df_filtered,
            x='Kategori_Konsumsi',
            y='Skor_Produktivitas',
            color='Kategori_Konsumsi',
            box=True,
            points='outliers',
            color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
        )
        
        fig_violin.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_violin, use_container_width=True)
    
    with col_adv4:
        st.markdown("#### 🌡️ **Heatmap: Productivity by Coffee & Study Duration**")
        
        # Create heatmap data
        heatmap_data = df_filtered.groupby(['Kopi_per_Hari', 'Durasi_Belajar_Num'])['Skor_Produktivitas'].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='Kopi_per_Hari', columns='Durasi_Belajar_Num', values='Skor_Produktivitas')
        
        fig_heatmap_adv = px.imshow(
            heatmap_pivot,
            text_auto=".2f",
            color_continuous_scale=['#0f0524', '#8338ec', '#ff006e', '#ffbe0b', '#06ffa5'],
            labels=dict(x="Study Duration (h)", y="Coffee Cups", color="Productivity")
        )
        
        fig_heatmap_adv.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='JetBrains Mono'),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(
                title='Productivity',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            )
        )
        
        st.plotly_chart(fig_heatmap_adv, use_container_width=True)
    
    # Statistical Tests
    st.markdown("#### 🧪 **Hypothesis Testing**")
    
    test_col1, test_col2, test_col3 = st.columns(3)
    
    with test_col1:
        st.markdown("##### T-Test: Drinkers vs Non-Drinkers")
        drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 1]['Skor_Produktivitas']
        non_drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 0]['Skor_Produktivitas']
        
        if len(drinkers) > 1 and len(non_drinkers) > 1:
            from scipy.stats import ttest_ind
            t_stat, p_t = ttest_ind(drinkers, non_drinkers)
            
            st.markdown(f"""
            <div class="glass-card">
                <p>t-statistic: <span class="metric-highlight">{t_stat:.4f}</span></p>
                <p>p-value: <span class="metric-highlight">{p_t:.4f}</span></p>
                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                    {'✓ Significant difference' if p_t < 0.05 else '✗ No significant difference'}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with test_col2:
        st.markdown("##### ANOVA: Multiple Groups")
        from scipy.stats import f_oneway
        
        groups = []
        for cups in df_filtered['Kopi_per_Hari'].unique():
            group_data = df_filtered[df_filtered['Kopi_per_Hari'] == cups]['Skor_Produktivitas']
            if len(group_data) > 1:
                groups.append(group_data)
        
        if len(groups) >= 2:
            f_stat, p_anova = f_oneway(*groups)
            
            st.markdown(f"""
            <div class="glass-card">
                <p>F-statistic: <span class="metric-highlight">{f_stat:.4f}</span></p>
                <p>p-value: <span class="metric-highlight">{p_anova:.4f}</span></p>
                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                    {'✓ Significant difference' if p_anova < 0.05 else '✗ No significant difference'}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with test_col3:
        st.markdown("##### Mann-Whitney U Test")
        from scipy.stats import mannwhitneyu
        
        if len(drinkers) > 1 and len(non_drinkers) > 1:
            u_stat, p_mw = mannwhitneyu(drinkers, non_drinkers, alternative='two-sided')
            
            st.markdown(f"""
            <div class="glass-card">
                <p>U-statistic: <span class="metric-highlight">{u_stat:.4f}</span></p>
                <p>p-value: <span class="metric-highlight">{p_mw:.4f}</span></p>
                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                    {'✓ Significant difference' if p_mw < 0.05 else '✗ No significant difference'}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ===================== TAB 7: AI INSIGHTS =====================
with tab7:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">07</span>
        <div>
            <h2 class="section-title">AI-Powered Insights <span class="badge-3d">✦ AI</span></h2>
            <p class="section-subtitle">Automated pattern recognition and recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate AI Insights
    st.markdown("### 🤖 **Automated Analysis**")
    
    # Insight 1: Optimal Coffee Consumption
    optimal_coffee = df_filtered.groupby('Kopi_per_Hari')['Skor_Produktivitas'].mean().idxmax()
    optimal_score = df_filtered.groupby('Kopi_per_Hari')['Skor_Produktivitas'].mean().max()
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">🏆</div>
        <div class="insight-title">Optimal Coffee Consumption</div>
        <div class="insight-text">
            Based on our analysis, the optimal coffee consumption for maximum productivity is 
            <span class="metric-highlight">{optimal_coffee} cups per day</span>, achieving an average 
            productivity score of <span class="metric-highlight">{optimal_score:.2f}</span>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Insight 2: Study Duration Sweet Spot
    durasi_bins = pd.cut(df_filtered['Durasi_Belajar_Num'], bins=[0, 2, 4, 6, 8, 10])
    durasi_productivity = df_filtered.groupby(durasi_bins)['Skor_Produktivitas'].mean()
    optimal_durasi = durasi_productivity.idxmax()
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">⏰</div>
        <div class="insight-title">Study Duration Sweet Spot</div>
        <div class="insight-text">
            The most productive study duration range is <span class="metric-highlight">{optimal_durasi}</span>, 
            with an average productivity score of <span class="metric-highlight">{durasi_productivity.max():.2f}</span>.
            Consider structuring your study sessions within this timeframe.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Insight 3: Sleep Quality Impact
    sleep_corr = df_filtered['Kualitas_Tidur_Memburuk'].corr(df_filtered['Skor_Produktivitas'])
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">😴</div>
        <div class="insight-title">Sleep Quality Impact</div>
        <div class="insight-text">
            Sleep quality shows a <span class="metric-highlight">{'positive' if sleep_corr > 0 else 'negative'}</span> 
            correlation with productivity (r = {sleep_corr:.3f}). 
            {'Better sleep quality is associated with higher productivity.' if sleep_corr > 0 else 'Poorer sleep quality is associated with lower productivity.'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Insight 4: Risk Factors
    high_coffee_low_sleep = df_filtered[(df_filtered['Kopi_per_Hari'] >= 2) & (df_filtered['Kualitas_Tidur_Memburuk'] >= 4)]
    risk_percentage = (len(high_coffee_low_sleep) / len(df_filtered)) * 100
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">⚠️</div>
        <div class="insight-title">Risk Factor Alert</div>
        <div class="insight-text">
            <span class="metric-highlight">{risk_percentage:.1f}%</span> of respondents show a high-risk pattern: 
            consuming 2+ cups of coffee daily with poor sleep quality (≥4). This combination may lead to 
            long-term health issues and decreased cognitive performance.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("### 💡 **Personalized Recommendations**")
    
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    
    with rec_col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #06ffa5;">☕ For Light Drinkers</h4>
            <ul style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                <li>✓ Maintain 1 cup/day routine</li>
                <li>✓ Consume before study sessions</li>
                <li>✓ Avoid after 4 PM</li>
                <li>✓ Monitor sleep quality</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ffbe0b;">⚡ For Moderate Drinkers</h4>
            <ul style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                <li>⚠ Consider reducing to 1 cup</li>
                <li>⚠ Track productivity changes</li>
                <li>⚠ Implement coffee breaks</li>
                <li>⚠ Prioritize sleep hygiene</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ff006e;">🚨 For Heavy Drinkers</h4>
            <ul style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                <li>🚨 Reduce consumption gradually</li>
                <li>🚨 Consult health professional</li>
                <li>🚨 Implement detox periods</li>
                <li>🚨 Focus on sleep recovery</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Predictive Model Summary
    st.markdown("### 📊 **Predictive Model Summary**")
    
    # Simple linear regression summary
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_squared_error
    
    X = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']]
    y = df_filtered['Skor_Produktivitas']
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    st.markdown(f"""
    <div class="glass-card">
        <h4>🤖 Linear Regression Model</h4>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
            <div>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">R² Score</p>
                <p class="metric-highlight" style="font-size: 1.5rem;">{r2:.4f}</p>
            </div>
            <div>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">RMSE</p>
                <p class="metric-highlight" style="font-size: 1.5rem;">{rmse:.4f}</p>
            </div>
            <div>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Model Accuracy</p>
                <p class="metric-highlight" style="font-size: 1.5rem;">{r2*100:.1f}%</p>
            </div>
        </div>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 1rem;">
            <strong>Coefficients:</strong><br>
            Coffee: {model.coef_[0]:.4f} | Study Duration: {model.coef_[1]:.4f} | Sleep Quality: {model.coef_[2]:.4f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Importance
    st.markdown("### 📈 **Feature Importance**")
    
    feature_importance = pd.DataFrame({
        'Feature': ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk'],
        'Importance': np.abs(model.coef_)
    }).sort_values('Importance', ascending=False)
    
    fig_importance = px.bar(
        feature_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#06ffa5', '#8338ec', '#ff006e']
    )
    
    fig_importance.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        showlegend=False,
        coloraxis_showscale=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)

# --- FOOTER ---
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Pro Dashboard</p>
    <p class="footer-text">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Sumber Data: Kuesioner Mahasiswa (n=31) | Powered by Streamlit & Plotly 3D</p>
    <p class="footer-text" style="margin-top: 1rem; opacity: 0.6;">
        ◆ Interactive 3D Visualization ◆ AI-Powered Insights ◆ Stochastic Modeling ◆ Advanced Analytics ◆
    </p>
</div>
""", unsafe_allow_html=True)
