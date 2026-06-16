import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr, ttest_ind, chi2_contingency, shapiro, kstest, norm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import warnings
import io
import base64
from datetime import datetime
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Coffee Analytics 3D Pro ☕",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM 3D EDITION V2.0 ---
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
    
    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #06ffa5, #3a86ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(6, 255, 165, 0.4);
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
    
    /* LOADING SPINNER */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-top: 4px solid #8338ec;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    /* CONFETTI ANIMATION */
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #ff006e;
        animation: confetti-fall 3s linear;
    }
    
    /* STATUS INDICATOR */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-active {
        background: #06ffa5;
        box-shadow: 0 0 10px #06ffa5;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* PROGRESS BAR */
    .progress-container {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff);
        border-radius: 10px;
        animation: progress-fill 2s ease-out;
    }
    
    @keyframes progress-fill {
        from { width: 0%; }
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
    
    # Outlier detection (IQR method)
    Q1 = df_clean['Skor_Produktivitas'].quantile(0.25)
    Q3 = df_clean['Skor_Produktivitas'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean['Is_Outlier'] = ((df_clean['Skor_Produktivitas'] < lower_bound) | 
                               (df_clean['Skor_Produktivitas'] > upper_bound)).astype(int)

    return df_clean

df = load_data()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <span class="hero-emoji">☕</span>
        <h1 class="hero-title">Coffee Analytics Pro</h1>
        <p class="hero-subtitle">Advanced Neuroscience of Caffeine Through Data Science & Machine Learning</p>
        <span class="hero-badge">◆ INTERACTIVE 3D VISUALIZATION ◆ ML PREDICTIONS ◆ EXPORT REPORTS ◆</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🎛️ **Control Panel**")
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
    
    outlier_filter = st.checkbox("🚫 Exclude Outliers", value=False)

    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1])
    ]

    if fokus_filter == "High Focus (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Low Focus (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]
    
    if outlier_filter:
        df_filtered = df_filtered[df_filtered['Is_Outlier'] == 0]

    st.markdown("---")
    st.markdown(f"""
    <div class="glass-card pulse-card" style="text-align: center;">
        <span class="kpi-icon">👥</span>
        <p class="kpi-value">{len(df_filtered)}</p>
        <p class="kpi-label">Responden Aktif</p>
        <span class="status-indicator status-active"></span>
        <span style="font-size: 0.75rem; color: #06ffa5;">LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📥 **Export Data**")
    
    # Download filtered data
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📊 Download Filtered Data (CSV)",
        data=csv,
        file_name=f"coffee_analytics_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Download full dataset
    csv_full = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📁 Download Full Dataset (CSV)",
        data=csv_full,
        file_name=f"coffee_analytics_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

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

col1, col2, col3, col4 = st.columns(4)

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

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌐 3D Visualization",
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎯 Conditional Probability",
    "🎲 Monte Carlo Simulation",
    "🤖 ML Prediction",
    "🧪 Hypothesis Testing",
    "📈 Advanced Analytics"
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
            'Fokus_Label': True
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
                      'Kopi: %{x} cangkir<br>' +
                      'Durasi: %{y:.1f} jam<br>' +
                      'Produktivitas: %{z:.2f}<br>' +
                      'Tidur: %{customdata[3]:.0f}<extra></extra>'
    )
    
    st.plotly_chart(fig_3d_scatter, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # 3D BAR CHART
    st.markdown("### 📊 **3D Bar Chart: Distribusi 3D**")
    
    # Group data for 3D bar
    bar_data = df_filtered.groupby(['Kopi_per_Hari', 'Is_Fokus_Tinggi']).size().reset_index(name='Count')
    
    fig_3d_bar = go.Figure(data=[
        go.Bar3d(
            x=bar_data['Kopi_per_Hari'],
            y=bar_data['Is_Fokus_Tinggi'].map({0: 'Low Focus', 1: 'High Focus'}),
            z=bar_data['Count'],
            color=bar_data['Count'],
            colorscale='Viridis',
            opacity=0.9
        )
    ])
    
    fig_3d_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Space Grotesk'),
        scene=dict(
            xaxis=dict(title='☕ Cangkir Kopi', backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(title='🎯 Status Fokus', backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(title='👥 Jumlah', backgroundcolor='rgba(0,0,0,0)'),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=500,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_3d_bar, use_container_width=True)
    
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
    
    # 3D INSIGHTS
    st.markdown("### 💎 **3D Insights & Pattern Discovery**")
    
    ins_col1, ins_col2, ins_col3 = st.columns(3)
    
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
    
    st.markdown("#### 📋 **Statistical Summary**")
    stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
    st.dataframe(
        stats_df.style.background_gradient(cmap='viridis', axis=1),
        use_container_width=True
    )
    
    # Normality Test
    st.markdown("#### 🧪 **Normality Test (Shapiro-Wilk)**")
    stat, p_value = shapiro(df_filtered['Skor_Produktivitas'])
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown(f"""
        <div class="info-box">
            📊 <strong>Shapiro-Wilk Test</strong><br>
            Test Statistic: <span class="metric-highlight">{stat:.4f}</span><br>
            P-Value: <span class="metric-highlight">{p_value:.4f}</span><br>
            <br>
            {"✅ Data terdistribusi normal (p > 0.05)" if p_value > 0.05 else "❌ Data tidak terdistribusi normal (p ≤ 0.05)"}
        </div>
        """, unsafe_allow_html=True)
    
    with col_n2:
        # Q-Q Plot
        from scipy import stats
        fig_qq = go.Figure()
        fig_qq.add_trace(go.Scatter(
            x=stats.probplot(df_filtered['Skor_Produktivitas'], dist="norm")[0][0],
            y=stats.probplot(df_filtered['Skor_Produktivitas'], dist="norm")[0][1],
            mode='markers',
            marker=dict(color='#8338ec', size=8),
            name='Data'
        ))
        
        # Add reference line
        min_val = min(stats.probplot(df_filtered['Skor_Produktivitas'], dist="norm")[0][0])
        max_val = max(stats.probplot(df_filtered['Skor_Produktivitas'], dist="norm")[0][0])
        fig_qq.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(color='#ff006e', width=2, dash='dash'),
            name='Reference'
        ))
        
        fig_qq.update_layout(
            title='Q-Q Plot',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Theoretical Quantiles', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Sample Quantiles', gridcolor='rgba(255,255,255,0.1)'),
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_qq, use_container_width=True)

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
            hover_data=['Fokus_Label']
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
        
        # Bayes Theorem
        st.markdown("#### 🔢 **Bayes' Theorem Application**")
        
        # P(High Focus | Coffee) = P(Coffee | High Focus) * P(High Focus) / P(Coffee)
        p_high_focus = df_filtered['Is_Fokus_Tinggi'].mean()
        p_coffee = df_filtered['Is_Peminum_Kopi'].mean()
        
        coffee_and_high = len(df_filtered[(df_filtered['Is_Peminum_Kopi'] == 1) & 
                                          (df_filtered['Is_Fokus_Tinggi'] == 1)]) / len(df_filtered)
        
        p_coffee_given_high = coffee_and_high / p_high_focus if p_high_focus > 0 else 0
        
        st.markdown(f"""
        <div class="info-box">
            <strong>P(High Focus | Coffee):</strong> <span class="metric-highlight">{p_kopi/100:.4f}</span><br>
            <strong>P(Coffee | High Focus):</strong> <span class="metric-highlight">{p_coffee_given_high:.4f}</span><br>
            <strong>P(High Focus):</strong> <span class="metric-highlight">{p_high_focus:.4f}</span><br>
            <strong>P(Coffee):</strong> <span class="metric-highlight">{p_coffee:.4f}</span>
        </div>
        """, unsafe_allow_html=True)

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
            
            # Download MC results
            mc_df = pd.DataFrame({'Iteration': range(1, len(hasil)+1), 'Mean_Score': hasil})
            mc_csv = mc_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Monte Carlo Results",
                data=mc_csv,
                file_name=f"monte_carlo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# ===================== TAB 6: ML PREDICTION =====================
with tab6:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">06</span>
        <div>
            <h2 class="section-title">Machine Learning Prediction <span class="badge-3d">✦ AI</span></h2>
            <p class="section-subtitle">Predict productivity based on coffee consumption and study duration</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤖 **Linear Regression Model**")
    st.markdown("""
    <div class="info-box">
        🧠 Model ini menggunakan <b>Linear Regression</b> untuk memprediksi skor produktivitas berdasarkan 
        konsumsi kopi dan durasi belajar. Model dilatih menggunakan data yang sedang difilter.
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare data for ML
    X = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num']]
    y = df_filtered['Skor_Produktivitas']
    
    if len(X) > 10:
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📊</span>
                <p class="kpi-value">{r2:.3f}</p>
                <p class="kpi-label">R² Score</p>
                <span class="kpi-delta">Model Fit</span>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📉</span>
                <p class="kpi-value">{rmse:.3f}</p>
                <p class="kpi-label">RMSE</p>
                <span class="kpi-delta">Error Rate</span>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🎯</span>
                <p class="kpi-value">{model.score(X, y):.3f}</p>
                <p class="kpi-label">Training Score</p>
                <span class="kpi-delta">Accuracy</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Model coefficients
        st.markdown("#### 📐 **Model Coefficients**")
        coef_df = pd.DataFrame({
            'Feature': ['Intercept', 'Kopi_per_Hari', 'Durasi_Belajar_Num'],
            'Coefficient': [model.intercept_, model.coef_[0], model.coef_[1]]
        })
        st.dataframe(coef_df.style.background_gradient(cmap='coolwarm', axis=0), use_container_width=True)
        
        st.markdown(f"""
        <div class="info-box">
            <strong>Prediction Formula:</strong><br>
            Produktivitas = {model.intercept_:.4f} + ({model.coef_[0]:.4f} × Kopi) + ({model.coef_[1]:.4f} × Durasi)
        </div>
        """, unsafe_allow_html=True)
        
        # Actual vs Predicted
        st.markdown("#### 📈 **Actual vs Predicted**")
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(
            x=y_test,
            y=y_pred,
            mode='markers',
            marker=dict(color='#8338ec', size=10, opacity=0.7),
            name='Predictions'
        ))
        
        # Add reference line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        fig_pred.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(color='#ff006e', width=2, dash='dash'),
            name='Perfect Prediction'
        ))
        
        fig_pred.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Actual Productivity', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Predicted Productivity', gridcolor='rgba(255,255,255,0.1)'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Interactive prediction
        st.markdown("#### 🎮 **Try It Yourself!**")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            input_kopi = st.slider("☕ Cangkir Kopi:", 0, 5, 1)
        with col_p2:
            input_durasi = st.slider("📚 Durasi Belajar (jam):", 1.0, 10.0, 5.0, 0.5)
        
        prediction = model.predict([[input_kopi, input_durasi]])[0]
        prediction = np.clip(prediction, 1.0, 5.0)
        
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: #06ffa5; margin: 0;">🎯 Predicted Productivity Score</h3>
            <p style="font-size: 3rem; font-weight: 700; color: #fff; margin: 1rem 0; font-family: 'JetBrains Mono', monospace;">
                {prediction:.3f}
            </p>
            <p style="color: rgba(255,255,255,0.6); margin: 0;">
                Based on {input_kopi} cups of coffee and {input_durasi}h study duration
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Not enough data to train model. Please adjust filters to include more respondents.")

# ===================== TAB 7: HYPOTHESIS TESTING =====================
with tab7:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">07</span>
        <div>
            <h2 class="section-title">Hypothesis Testing <span class="badge-3d">✦ STATISTICAL</span></h2>
            <p class="section-subtitle">Rigorous statistical tests to validate findings</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧪 **T-Test: Coffee Drinkers vs Non-Drinkers**")
    st.markdown("""
    <div class="info-box">
        <strong>H₀:</strong> Tidak ada perbedaan produktivitas antara peminum kopi dan non-peminum kopi<br>
        <strong>H₁:</strong> Ada perbedaan produktivitas antara peminum kopi dan non-peminum kopi<br>
        <strong>Significance Level:</strong> α = 0.05
    </div>
    """, unsafe_allow_html=True)
    
    coffee_drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 1]['Skor_Produktivitas']
    non_drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 0]['Skor_Produktivitas']
    
    if len(coffee_drinkers) > 1 and len(non_drinkers) > 1:
        t_stat, p_value_t = ttest_ind(coffee_drinkers, non_drinkers)
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">☕</span>
                <p class="kpi-value">{coffee_drinkers.mean():.3f}</p>
                <p class="kpi-label">Coffee Drinkers Mean</p>
                <span class="kpi-delta">n = {len(coffee_drinkers)}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_t2:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🚫</span>
                <p class="kpi-value">{non_drinkers.mean():.3f}</p>
                <p class="kpi-label">Non-Drinkers Mean</p>
                <span class="kpi-delta">n = {len(non_drinkers)}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_t3:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📊</span>
                <p class="kpi-value">{t_stat:.3f}</p>
                <p class="kpi-label">T-Statistic</p>
                <span class="kpi-delta">p = {p_value_t:.4f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value_t < 0.05:
            st.success(f"""
            ✅ **Reject H₀** (p = {p_value_t:.4f} < 0.05)<br>
            Terdapat perbedaan signifikan dalam produktivitas antara peminum kopi dan non-peminum kopi.
            """)
        else:
            st.info(f"""
            ℹ️ **Fail to Reject H₀** (p = {p_value_t:.4f} ≥ 0.05)<br>
            Tidak terdapat perbedaan signifikan dalam produktivitas antara peminum kopi dan non-peminum kopi.
            """)
        
        # Visualization
        fig_ttest = go.Figure()
        fig_ttest.add_trace(go.Box(y=coffee_drinkers, name='Coffee Drinkers', marker_color='#ff006e'))
        fig_ttest.add_trace(go.Box(y=non_drinkers, name='Non-Drinkers', marker_color='#3a86ff'))
        
        fig_ttest.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_ttest, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # Chi-Square Test
    st.markdown("### 🔢 **Chi-Square Test: Independence**")
    st.markdown("""
    <div class="info-box">
        <strong>H₀:</strong> Konsumsi kopi dan status fokus bersifat independen<br>
        <strong>H₁:</strong> Konsumsi kopi dan status fokus bergantung satu sama lain<br>
        <strong>Significance Level:</strong> α = 0.05
    </div>
    """, unsafe_allow_html=True)
    
    contingency_table = pd.crosstab(df_filtered['Is_Peminum_Kopi'], df_filtered['Is_Fokus_Tinggi'])
    
    if contingency_table.shape[0] > 1 and contingency_table.shape[1] > 1:
        chi2, p_value_chi2, dof, expected = chi2_contingency(contingency_table)
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📊</span>
                <p class="kpi-value">{chi2:.3f}</p>
                <p class="kpi-label">Chi-Square Statistic</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🔢</span>
                <p class="kpi-value">{dof}</p>
                <p class="kpi-label">Degrees of Freedom</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📉</span>
                <p class="kpi-value">{p_value_chi2:.4f}</p>
                <p class="kpi-label">P-Value</p>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value_chi2 < 0.05:
            st.success(f"""
            ✅ **Reject H₀** (p = {p_value_chi2:.4f} < 0.05)<br>
            Konsumsi kopi dan status fokus <b>tidak independen</b> - ada hubungan signifikan antara keduanya.
            """)
        else:
            st.info(f"""
            ℹ️ **Fail to Reject H₀** (p = {p_value_chi2:.4f} ≥ 0.05)<br>
            Konsumsi kopi dan status fokus bersifat <b>independen</b> - tidak ada hubungan signifikan.
            """)
        
        # Contingency table display
        st.markdown("#### 📋 **Contingency Table**")
        st.dataframe(contingency_table, use_container_width=True)
        
        st.markdown("#### 📊 **Expected Frequencies**")
        expected_df = pd.DataFrame(expected, 
                                   index=contingency_table.index, 
                                   columns=contingency_table.columns)
        expected_df.index = ['Non-Drinkers', 'Coffee Drinkers']
        expected_df.columns = ['Low Focus', 'High Focus']
        st.dataframe(expected_df.round(2), use_container_width=True)

# ===================== TAB 8: ADVANCED ANALYTICS =====================
with tab8:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">08</span>
        <div>
            <h2 class="section-title">Advanced Analytics <span class="badge-3d">✦ PREMIUM</span></h2>
            <p class="section-subtitle">Outlier detection, distribution fitting, and comparative analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Outlier Detection
    st.markdown("### 🚨 **Outlier Detection**")
    st.markdown("""
    <div class="info-box">
        Outlier dideteksi menggunakan metode <b>IQR (Interquartile Range)</b>. 
        Data points di luar Q1 - 1.5×IQR atau Q3 + 1.5×IQR dianggap sebagai outlier.
    </div>
    """, unsafe_allow_html=True)
    
    outlier_count = df_filtered['Is_Outlier'].sum()
    outlier_pct = (outlier_count / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
    
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🚨</span>
            <p class="kpi-value">{outlier_count}</p>
            <p class="kpi-label">Outliers Detected</p>
            <span class="kpi-delta">{outlier_pct:.1f}% of data</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_o2:
        # Outlier visualization
        fig_outlier = px.scatter(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            color='Is_Outlier',
            color_discrete_map={0: '#8338ec', 1: '#ff006e'},
            size='Kualitas_Tidur_Memburuk',
            size_max=20,
            labels={'Is_Outlier': 'Outlier Status'},
            hover_data=['Durasi_Belajar_Num', 'Fokus_Label']
        )
        fig_outlier.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Cups of Coffee', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_outlier, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # Distribution Fitting
    st.markdown("### 📊 **Distribution Fitting**")
    st.markdown("""
    <div class="info-box">
        Menguji distribusi mana yang paling cocok dengan data produktivitas menggunakan 
        <b>Kolmogorov-Smirnov Test</b>.
    </div>
    """, unsafe_allow_html=True)
    
    productivity_data = df_filtered['Skor_Produktivitas'].dropna()
    
    if len(productivity_data) > 5:
        # Test different distributions
        distributions = {
            'Normal': norm
        }
        
        results = []
        for name, dist in distributions.items():
            # Fit distribution
            params = dist.fit(productivity_data)
            # KS test
            ks_stat, ks_pvalue = kstest(productivity_data, name.lower(), args=params)
            results.append({
                'Distribution': name,
                'KS Statistic': ks_stat,
                'P-Value': ks_pvalue,
                'Fit': 'Good' if ks_pvalue > 0.05 else 'Poor'
            })
        
        results_df = pd.DataFrame(results)
        st.dataframe(
            results_df.style.apply(lambda x: ['background: rgba(6, 255, 165, 0.2)' if v == 'Good' 
                                               else 'background: rgba(255, 0, 110, 0.2)' 
                                               for v in x['Fit']], axis=1),
            use_container_width=True
        )
        
        # Distribution plot
        fig_dist = go.Figure()
        
        # Histogram
        fig_dist.add_trace(go.Histogram(
            x=productivity_data,
            name='Actual Data',
            nbinsx=20,
            marker_color='rgba(131, 56, 236, 0.6)',
            marker_line_color='#8338ec',
            opacity=0.7
        ))
        
        # Fitted normal distribution
        x_range = np.linspace(productivity_data.min(), productivity_data.max(), 100)
        pdf = norm.pdf(x_range, *params)
        fig_dist.add_trace(go.Scatter(
            x=x_range,
            y=pdf * len(productivity_data) * (productivity_data.max() - productivity_data.min()) / 20,
            name='Fitted Normal',
            line=dict(color='#ff006e', width=3),
            mode='lines'
        ))
        
        fig_dist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Frequency', gridcolor='rgba(255,255,255,0.1)'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            barmode='overlay'
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    # Comparative Analysis
    st.markdown("### 📈 **Comparative Analysis by Coffee Consumption**")
    
    comparison_metric = st.selectbox(
        "Select Metric to Compare:",
        ['Skor_Produktivitas', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']
    )
    
    # Group by coffee consumption
    comparison_data = df_filtered.groupby('Kopi_per_Hari')[comparison_metric].agg(['mean', 'std', 'count']).reset_index()
    comparison_data.columns = ['Kopi_per_Hari', 'Mean', 'Std', 'Count']
    
    fig_comp = go.Figure()
    
    # Bar chart with error bars
    fig_comp.add_trace(go.Bar(
        x=comparison_data['Kopi_per_Hari'],
        y=comparison_data['Mean'],
        error_y=dict(type='data', array=comparison_data['Std'], visible=True),
        marker_color='#8338ec',
        name='Mean',
        text=comparison_data['Count'],
        textposition='auto',
        texttemplate='%{text} samples'
    ))
    
    fig_comp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(title='Cups of Coffee per Day', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title=f'Average {comparison_metric}', gridcolor='rgba(255,255,255,0.1)'),
        height=450,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Detailed comparison table
    st.markdown("#### 📋 **Detailed Comparison Table**")
    st.dataframe(
        comparison_data.style.background_gradient(cmap='viridis', subset=['Mean']),
        use_container_width=True
    )

# --- FOOTER ---
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Pro Dashboard</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Sumber Data: Kuesioner Mahasiswa (n=31) | Powered by Streamlit & Plotly 3D</p>
    <p class="footer-text" style="margin-top: 1rem; opacity: 0.6;">
        ◆ Interactive 3D Visualization ◆ Machine Learning ◆ Statistical Testing ◆ Monte Carlo Simulation ◆
    </p>
</div>
""", unsafe_allow_html=True)
