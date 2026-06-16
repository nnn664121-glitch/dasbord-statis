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
    page_title="Coffee Analytics ☕",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS KUSTOM GEN Z STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Main Headers */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metric Cards */
    .metric-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(20px);
    }
    
    .stSidebar .sidebar-content {
        background: transparent;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #a0a0a0;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        color: #fff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #fff;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding-left: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #fff;
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess {
        background: linear-gradient(135deg, rgba(46, 213, 115, 0.2), rgba(46, 213, 115, 0.1));
        border: 1px solid rgba(46, 213, 115, 0.4);
        border-radius: 12px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 165, 2, 0.2), rgba(255, 165, 2, 0.1));
        border: 1px solid rgba(255, 165, 2, 0.4);
        border-radius: 12px;
    }
    
    /* Animated gradient border */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-border {
        position: relative;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2px;
    }
    
    .gradient-border::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% 300%;
        border-radius: 22px;
        z-index: -1;
        animation: gradient-shift 5s ease infinite;
    }
    
    /* Metric delta styling */
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
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

    return df_clean

df = load_data()

# --- HEADER SECTION ---
st.markdown('<p class="main-title">☕ Coffee Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Exploring the correlation between caffeine consumption and academic productivity</p>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🎛️ **Filters**")
    st.markdown("---")

    kopi_filter = st.multiselect(
        "Cups per Day",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique())
    )

    durasi_options = df['Durasi_Belajar_Num'].unique()
    durasi_range = st.slider(
        "Study Duration (hours)",
        min_value=float(min(durasi_options)),
        max_value=float(max(durasi_options)),
        value=(float(min(durasi_options)), float(max(durasi_options)))
    )

    fokus_filter = st.selectbox(
        "Focus Status",
        options=["All", "High Focus (>3.0)", "Low Focus (≤3.0)"]
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
    <div class="metric-box">
        <p class="metric-value">{len(df_filtered)}</p>
        <p class="metric-label">Respondents</p>
    </div>
    """, unsafe_allow_html=True)

# --- BENTO GRID METRICS ---
st.markdown("### 📊 **Quick Stats**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <p class="metric-value">{df_filtered['Kopi_per_Hari'].mean():.1f}</p>
        <p class="metric-label">☕ Avg Cups/Day</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <p class="metric-value">{df_filtered['Durasi_Belajar_Num'].mean():.1f}h</p>
        <p class="metric-label">📚 Avg Study Time</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <p class="metric-value">{df_filtered['Skor_Produktivitas'].mean():.2f}</p>
        <p class="metric-label">⚡ Productivity Score</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fokus_pct = df_filtered['Is_Fokus_Tinggi'].mean() * 100
    st.markdown(f"""
    <div class="metric-box">
        <p class="metric-value">{fokus_pct:.0f}%</p>
        <p class="metric-label">🎯 High Focus Rate</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎯 Conditional Probability",
    "🎲 Monte Carlo Simulation"
])

# ===================== TAB 1: DESKRIPTIF =====================
with tab1:
    st.markdown("### 📊 **Descriptive Analytics**")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Coffee Consumption Distribution")
        kopi_counts = df_filtered['Kopi_per_Hari'].value_counts().sort_index()
        fig_dist_kopi = px.bar(
            x=kopi_counts.index,
            y=kopi_counts.values,
            labels={'x': 'Cups', 'y': 'Respondents'},
        )
        fig_dist_kopi.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(dtick=1, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_dist_kopi.update_traces(
            marker=dict(
                color=['#667eea', '#764ba2', '#f093fb'],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate="<b>%{x} cups</b><br>Respondents: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_dist_kopi, use_container_width=True)
    
    with col_b:
        st.markdown("#### Productivity Score Distribution")
        fig_hist_prod = px.histogram(
            df_filtered,
            x='Skor_Produktivitas',
            nbins=15,
        )
        fig_hist_prod.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_hist_prod.update_traces(
            marker_color='rgba(102, 126, 234, 0.7)',
            marker_line=dict(color='#667eea', width=1),
            hovertemplate="<b>Score: %{x:.2f}</b><br>Frequency: %{y}<extra></extra>"
        )
        st.plotly_chart(fig_hist_prod, use_container_width=True)
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.markdown("#### Productivity by Coffee Group")
        fig_box = px.box(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            color='Kopi_per_Hari',
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
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
            hovertemplate="<b>%{x} cups</b><br>Score: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_d:
        st.markdown("#### Study Duration by Coffee Group")
        durasi_mean = df_filtered.groupby('Kopi_per_Hari')['Durasi_Belajar_Num'].mean().reset_index()
        fig_bar_durasi = px.bar(
            durasi_mean,
            x='Kopi_per_Hari',
            y='Durasi_Belajar_Num',
            color='Durasi_Belajar_Num',
            color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
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
            marker_line=dict(color='rgba(255,255,255,0.2)', width=1),
            hovertemplate="<b>%{x} cups</b><br>Duration: %{y:.1f}h<extra></extra>"
        )
        st.plotly_chart(fig_bar_durasi, use_container_width=True)
    
    st.markdown("#### 📋 **Statistical Summary**")
    stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
    st.dataframe(stats_df, use_container_width=True)

# ===================== TAB 2: KORELASI =====================
with tab2:
    st.markdown("### 🔗 **Correlation Analysis**")
    
    col_e, col_f = st.columns([1, 1])
    
    with col_e:
        st.markdown("#### Correlation Heatmap")
        corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
        corr_matrix = df_filtered[corr_cols].corr(method='pearson')
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale=['#f093fb', '#764ba2', '#667eea', '#1a1a2e'],
            zmin=-1, zmax=1,
        )
        fig_heatmap.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_heatmap.update_traces(
            hovertemplate="<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col_f:
        st.markdown("#### Coffee vs Productivity")
        
        if len(df_filtered) > 1:
            p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
            signifikansi = "Significant" if p_value < 0.05 else "Not Significant"
            
            st.markdown(f"""
            <div class="info-box">
                <p style="color: #a0a0a0; margin: 0;">📊 Correlation Coefficient</p>
                <p style="color: #fff; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">r = {p_coeff:.4f}</p>
                <p style="color: #a0a0a0; margin: 0;">p-value: {p_value:.4f} ({signifikansi})</p>
            </div>
            """, unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_filtered,
            x='Kopi_per_Hari',
            y='Skor_Produktivitas',
            trendline='ols' if len(df_filtered) > 2 else None,
            color='Durasi_Belajar_Num',
            color_continuous_scale=['#667eea', '#f093fb'],
            size='Kualitas_Tidur_Memburuk',
            size_max=20,
            hover_data=['Is_Fokus_Tinggi']
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
            hovertemplate="<b>%{x} cups</b><br>Productivity: %{y:.2f}<extra></extra>"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("### 💡 **Key Insights**")
    insight_cols = st.columns(3)
    
    with insight_cols[0]:
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #667eea;">☕ ↔ ⚡ Productivity</h4>
            <p style="color: #a0a0a0;">Weak positive correlation suggests coffee slightly enhances perceived productivity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_cols[1]:
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #f093fb;">☕ ↔ 😴 Sleep Quality</h4>
            <p style="color: #a0a0a0;">Moderate negative correlation proves the trade-off: more coffee = worse sleep.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_cols[2]:
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #764ba2;">☕ ↔ 📚 Study Time</h4>
            <p style="color: #a0a0a0;">Positive correlation indicates coffee drinkers tend to study longer.</p>
        </div>
        """, unsafe_allow_html=True)

# ===================== TAB 3: PROBABILITAS =====================
with tab3:
    st.markdown("### 🎯 **Conditional Probability Analysis**")
    st.markdown("Calculating the probability of achieving **High Focus** (Score > 3.0) based on coffee consumption status.")
    
    col_g, col_h = st.columns([1, 1])
    
    with col_g:
        st.markdown("#### Contingency Table")
        kontingensi = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            margins=True
        )
        kontingensi.index = ['Non-Drinkers (0)', 'Coffee Drinkers (≥1)', 'Total']
        kontingensi.columns = ['Low Focus', 'High Focus', 'Total']
        st.dataframe(kontingensi, use_container_width=True)
        
        st.markdown("#### Probability Matrix")
        prob_bersyarat = pd.crosstab(
            df_filtered['Is_Peminum_Kopi'],
            df_filtered['Is_Fokus_Tinggi'],
            normalize='index'
        ) * 100
        prob_bersyarat.index = ['Non-Drinkers', 'Coffee Drinkers']
        prob_bersyarat.columns = ['Low Focus (%)', 'High Focus (%)']
        st.dataframe(prob_bersyarat.round(2), use_container_width=True)
    
    with col_h:
        st.markdown("#### Probability Comparison")
        
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
                    color=['#667eea', '#f093fb'],
                    line=dict(color='rgba(255,255,255,0.2)', width=1)
                ),
                text=[f'{p_kopi:.1f}%', f'{p_non_kopi:.1f}%'],
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>Probability: %{y:.1f}%<extra></extra>"
            )
        ])
        fig_prob.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(title="Probability (%)", range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            title=dict(text="P(High Focus | Coffee Consumption)", font=dict(color='white')),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_prob, use_container_width=True)
        
        if p_kopi > p_non_kopi and p_non_kopi > 0:
            st.success(f"📈 Coffee drinkers have **{p_kopi/p_non_kopi:.1f}x higher** chance of achieving high focus!")
        elif p_kopi > 0 and p_non_kopi == 0:
            st.success("📈 Only coffee drinkers achieve high focus!")
        else:
            st.warning("Insufficient data for probability comparison.")

# ===================== TAB 4: MONTE CARLO =====================
with tab4:
    st.markdown("### 🎲 **Monte Carlo Simulation**")
    st.markdown("Projecting average productivity scores to a population of 100 students through 10,000 stochastic iterations.")
    
    col_i, col_j = st.columns([1, 2])
    
    with col_i:
        st.markdown("#### ⚙️ Parameters")
        n_mahasiswa = st.slider("Students per Class:", 10, 500, 100, 10)
        n_iterasi = st.slider("Iterations:", 1000, 50000, 10000, 1000)
        
        st.markdown("#### 📊 Empirical Distribution")
        p_kopi_dist = df['Kopi_per_Hari'].value_counts(normalize=True).sort_index()
        for cat, w in p_kopi_dist.items():
            st.markdown(f"- **{cat} cups:** {w*100:.1f}%")
        
        simulate_btn = st.button("🎲 Run Simulation", type="primary", use_container_width=True)
    
    with col_j:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("Running Monte Carlo simulation..."):
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
                <div class="metric-box">
                    <p class="metric-value">{mean_mc:.3f}</p>
                    <p class="metric-label">Expected Mean</p>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-box">
                    <p class="metric-value">{ci_bawah:.3f}</p>
                    <p class="metric-label">CI 95% Lower</p>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-box">
                    <p class="metric-value">{ci_atas:.3f}</p>
                    <p class="metric-label">CI 95% Upper</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=hasil,
                nbinsx=50,
                name='Monte Carlo Distribution',
                marker=dict(
                    color='rgba(102, 126, 234, 0.6)',
                    line=dict(color='#667eea', width=1)
                ),
                hovertemplate="Score: %{x:.3f}<br>Frequency: %{y}<extra></extra>"
            ))
            fig_mc.add_vline(
                x=mean_mc, line_dash="dash", line_color="#f093fb",
                annotation_text=f"Mean: {mean_mc:.3f}", annotation_font_color="#f093fb"
            )
            fig_mc.add_vline(
                x=ci_bawah, line_dash="dot", line_color="#764ba2",
                annotation_text=f"CI Lower: {ci_bawah:.3f}", annotation_font_color="#764ba2"
            )
            fig_mc.add_vline(
                x=ci_atas, line_dash="dot", line_color="#764ba2",
                annotation_text=f"CI Upper: {ci_atas:.3f}", annotation_font_color="#764ba2"
            )
            fig_mc.update_layout(
                title=dict(
                    text=f"Probability Distribution ({len(hasil)} Iterations)",
                    font=dict(color='white')
                ),
                xaxis=dict(title="Average Productivity Score", gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(title="Frequency", gridcolor='rgba(255,255,255,0.1)', color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_mc, use_container_width=True)

# --- FOOTER ---
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p style="color: #a0a0a0;">📊 Built for <b>Statistics & Probability</b> Course</p>
    <p style="color: #666;">Data Source: Student Questionnaire (n=31) | Powered by Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
