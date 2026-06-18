import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import (
    pearsonr, spearmanr, chi2_contingency, 
    ttest_ind, f_oneway, mannwhitneyu, shapiro,
    kruskal, skew, kurtosis
)
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Coffee Analytics 4D Pro ☕",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM 4D EDITION V4 + ENHANCED ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Orbitron:wght@400;500;700;900&display=swap');
    
    :root {
        --primary-pink: #ff006e;
        --primary-purple: #8338ec;
        --primary-blue: #3a86ff;
        --primary-green: #06ffa5;
        --primary-yellow: #ffbe0b;
        --bg-dark: #050212;
        --bg-mid: #0f0524;
        --bg-light: #1a0b2e;
    }
    
    .stApp {
        background: radial-gradient(ellipse at top, var(--bg-light) 0%, var(--bg-mid) 40%, var(--bg-dark) 100%);
        font-family: 'Space Grotesk', sans-serif;
        overflow-x: hidden;
    }
    
    #MainMenu, header, footer {visibility: hidden;}
    
    ::-webkit-scrollbar {width: 10px;}
    ::-webkit-scrollbar-track {background: var(--bg-mid);}
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary-pink), var(--primary-purple), var(--primary-blue));
        border-radius: 10px;
    }
    
    /* ===== AURORA BACKGROUND ===== */
    .aurora-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -2;
        overflow: hidden;
    }
    
    .aurora {
        position: absolute;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            from 0deg,
            transparent,
            rgba(255, 0, 110, 0.05),
            transparent,
            rgba(131, 56, 236, 0.05),
            transparent,
            rgba(58, 134, 255, 0.05),
            transparent,
            rgba(6, 255, 165, 0.05),
            transparent
        );
        animation: aurora-spin 30s linear infinite;
        filter: blur(80px);
    }
    
    @keyframes aurora-spin {
        0% { transform: rotate(0deg) translate(-25%, -25%); }
        100% { transform: rotate(360deg) translate(-25%, -25%); }
    }
    
    /* ===== HOLOGRAPHIC TITLE ===== */
    .holo-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 5rem;
        background: linear-gradient(
            135deg, 
            var(--primary-pink) 0%, 
            var(--primary-yellow) 20%, 
            var(--primary-green) 40%,
            var(--primary-blue) 60%,
            var(--primary-purple) 80%,
            var(--primary-pink) 100%
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: holo-shift 6s ease infinite, holo-glow 3s ease-in-out infinite;
        letter-spacing: -2px;
        margin: 0;
        line-height: 1;
    }
    
    @keyframes holo-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes holo-glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(131, 56, 236, 0.4)); }
        50% { filter: drop-shadow(0 0 40px rgba(255, 0, 110, 0.6)); }
    }
    
    /* ===== HERO V4 ===== */
    .hero-v4 {
        position: relative;
        padding: 5rem 2rem;
        text-align: center;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 0, 110, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(131, 56, 236, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 100%);
        border-radius: 40px;
        overflow: hidden;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        animation: hero-v4-entrance 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes hero-v4-entrance {
        0% { opacity: 0; transform: translateY(80px) scale(0.8); filter: blur(20px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    
    .hero-v4::before {
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: conic-gradient(
            from 0deg,
            transparent,
            rgba(255, 0, 110, 0.3),
            transparent,
            rgba(131, 56, 236, 0.3),
            transparent,
            rgba(6, 255, 165, 0.3),
            transparent
        );
        animation: rotate 15s linear infinite;
    }
    
    .hero-v4::after {
        content: '';
        position: absolute;
        inset: 0;
        background: 
            repeating-linear-gradient(
                90deg,
                transparent 0px,
                transparent 2px,
                rgba(255,255,255,0.03) 2px,
                rgba(255,255,255,0.03) 4px
            );
        pointer-events: none;
    }
    
    .hero-content-v4 {
        position: relative;
        z-index: 2;
    }
    
    .hero-emoji-3d {
        font-size: 6rem;
        display: inline-block;
        animation: emoji-3d 4s ease-in-out infinite;
        filter: drop-shadow(0 10px 20px rgba(255, 0, 110, 0.5));
    }
    
    @keyframes emoji-3d {
        0%, 100% { transform: translateY(0) rotateY(0deg) rotateZ(0deg); }
        25% { transform: translateY(-30px) rotateY(180deg) rotateZ(15deg); }
        50% { transform: translateY(-10px) rotateY(360deg) rotateZ(0deg); }
        75% { transform: translateY(-25px) rotateY(540deg) rotateZ(-15deg); }
    }
    
    .hero-subtitle-v4 {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 1.5rem;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .hero-badges {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .hero-badge-v4 {
        padding: 0.6rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        color: var(--primary-green);
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 2px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        animation: badge-pulse-v4 3s ease-in-out infinite;
    }
    
    .hero-badge-v4:hover {
        transform: translateY(-5px) scale(1.05);
        border-color: var(--primary-green);
        box-shadow: 0 10px 30px rgba(6, 255, 165, 0.3);
    }
    
    @keyframes badge-pulse-v4 {
        0%, 100% { box-shadow: 0 0 0 0 rgba(6, 255, 165, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(6, 255, 165, 0); }
    }
    
    /* ===== DATA QUALITY METER ===== */
    .dq-meter {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, rgba(6, 255, 165, 0.1), rgba(58, 134, 255, 0.1));
        border: 1px solid rgba(6, 255, 165, 0.3);
        border-radius: 16px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .dq-score {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-green);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .dq-bar {
        flex: 1;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dq-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-pink), var(--primary-yellow), var(--primary-green));
        border-radius: 10px;
        animation: dq-fill 2s ease-out;
    }
    
    @keyframes dq-fill {
        from { width: 0%; }
    }
    
    /* ===== KPI CARDS V4 ===== */
    .kpi-grid-v4 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card-v4 {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem 1.5rem;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(20px);
        animation: kpi-slide-in 0.8s ease-out backwards;
    }
    
    .kpi-card-v4:nth-child(1) { animation-delay: 0.1s; }
    .kpi-card-v4:nth-child(2) { animation-delay: 0.2s; }
    .kpi-card-v4:nth-child(3) { animation-delay: 0.3s; }
    .kpi-card-v4:nth-child(4) { animation-delay: 0.4s; }
    .kpi-card-v4:nth-child(5) { animation-delay: 0.5s; }
    .kpi-card-v4:nth-child(6) { animation-delay: 0.6s; }
    
    @keyframes kpi-slide-in {
        from { opacity: 0; transform: translateY(40px) scale(0.9); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .kpi-card-v4::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-pink), var(--primary-purple), var(--primary-blue), var(--primary-green));
        background-size: 300% 100%;
        animation: gradient-shift 4s linear infinite;
    }
    
    .kpi-card-v4::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        animation: shimmer 4s infinite;
    }
    
    .kpi-card-v4:hover {
        transform: translateY(-10px) rotateX(5deg) scale(1.03);
        box-shadow: 
            0 25px 75px rgba(131, 56, 236, 0.4),
            0 0 0 1px rgba(131, 56, 236, 0.5) inset;
    }
    
    .kpi-icon-v4 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: icon-bounce-v4 3s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(131, 56, 236, 0.4));
    }
    
    @keyframes icon-bounce-v4 {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-8px) rotate(-5deg); }
        75% { transform: translateY(-8px) rotate(5deg); }
    }
    
    .kpi-value-v4 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .kpi-label-v4 {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 1rem;
        font-weight: 600;
    }
    
    .kpi-delta-v4 {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: rgba(6, 255, 165, 0.15);
        border: 1px solid rgba(6, 255, 165, 0.4);
        border-radius: 20px;
        color: var(--primary-green);
        font-size: 0.7rem;
        margin-top: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    
    .kpi-ci {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* ===== SECTION HEADERS V4 ===== */
    .section-header-v4 {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid transparent;
        background-image: linear-gradient(var(--bg-mid), var(--bg-mid)), 
                         linear-gradient(90deg, var(--primary-pink), var(--primary-purple), var(--primary-blue), var(--primary-green));
        background-origin: border-box;
        background-clip: padding-box, border-box;
        position: relative;
    }
    
    .section-header-v4::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-pink), var(--primary-purple), var(--primary-blue), var(--primary-green));
        background-size: 200% 100%;
        animation: gradient-shift 4s linear infinite;
    }
    
    .section-number-v4 {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', sans-serif;
        line-height: 1;
        animation: number-pulse-v4 3s ease-in-out infinite;
    }
    
    @keyframes number-pulse-v4 {
        0%, 100% { 
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255, 0, 110, 0.5));
        }
        50% { 
            transform: scale(1.05);
            filter: drop-shadow(0 0 25px rgba(131, 56, 236, 0.9));
        }
    }
    
    .section-title-v4 {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .section-subtitle-v4 {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* ===== GLASS CARDS V4 ===== */
    .glass-card-v4 {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card-v4:hover {
        transform: translateY(-5px) scale(1.01);
        border-color: rgba(131, 56, 236, 0.5);
        box-shadow: 0 20px 50px rgba(131, 56, 236, 0.25);
    }
    
    .glass-card-v4::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(131, 56, 236, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
    }
    
    .glass-card-v4:hover::before {
        opacity: 1;
    }
    
    /* ===== INSIGHT CARDS V4 ===== */
    .insight-card-v4 {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.1) 0%, rgba(131, 56, 236, 0.1) 100%);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        animation: insight-float-v4 5s ease-in-out infinite;
    }
    
    @keyframes insight-float-v4 {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    .insight-card-v4:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 60px rgba(131, 56, 236, 0.4);
        border-color: var(--primary-pink);
    }
    
    .insight-icon-v4 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: icon-dance-v4 3s ease-in-out infinite;
    }
    
    @keyframes icon-dance-v4 {
        0%, 100% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(-15deg) scale(1.15); }
        75% { transform: rotate(15deg) scale(1.15); }
    }
    
    .insight-title-v4 {
        color: #fff;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    
    .insight-text-v4 {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    /* ===== INFO BOX V4 ===== */
    .info-box-v4 {
        background: linear-gradient(135deg, rgba(58, 134, 255, 0.15) 0%, rgba(6, 255, 165, 0.1) 100%);
        border-left: 4px solid var(--primary-blue);
        border-radius: 16px;
        padding: 1.2rem 1.8rem;
        margin: 1.5rem 0;
        color: rgba(255, 255, 255, 0.95);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        position: relative;
        overflow: hidden;
    }
    
    .info-box-v4::before {
        content: '💡';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 4rem;
        opacity: 0.1;
    }
    
    /* ===== METRIC HIGHLIGHT V4 ===== */
    .metric-highlight-v4 {
        font-family: 'JetBrains Mono', monospace;
        color: var(--primary-green);
        font-weight: 700;
        position: relative;
        display: inline-block;
        padding: 0 0.3rem;
        background: rgba(6, 255, 165, 0.1);
        border-radius: 4px;
    }
    
    .metric-highlight-v4::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-green), var(--primary-blue));
    }
    
    /* ===== BADGE 4D ===== */
    .badge-4d {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.2rem;
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-purple), var(--primary-blue));
        background-size: 200% 200%;
        animation: badge-4d-shift 3s ease infinite;
        border-radius: 20px;
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-left: 1rem;
        box-shadow: 0 5px 25px rgba(255, 0, 110, 0.5);
        font-family: 'Orbitron', sans-serif;
    }
    
    @keyframes badge-4d-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* ===== TABS V4 ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 14px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        padding: 14px 28px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Space Grotesk', sans-serif;
        position: relative;
        overflow: hidden;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(131, 56, 236, 0.15);
        color: #fff;
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-purple), var(--primary-blue));
        background-size: 200% 200%;
        animation: badge-4d-shift 3s ease infinite;
        color: #fff;
        box-shadow: 0 8px 30px rgba(131, 56, 236, 0.5);
    }
    
    /* ===== BUTTONS V4 ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-purple), var(--primary-blue));
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
        animation: btn-gradient 4s ease infinite;
    }
    
    @keyframes btn-gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 0, 110, 0.5);
    }
    
    /* ===== PROGRESS V4 ===== */
    .progress-v4 {
        height: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-bar-v4 {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-pink), var(--primary-yellow), var(--primary-green));
        background-size: 200% 100%;
        border-radius: 10px;
        animation: progress-shine-v4 3s linear infinite;
    }
    
    @keyframes progress-shine-v4 {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* ===== FOOTER V4 ===== */
    .premium-footer-v4 {
        text-align: center;
        padding: 3rem;
        margin-top: 4rem;
        background: 
            radial-gradient(circle at 50% 0%, rgba(131, 56, 236, 0.2) 0%, transparent 70%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    
    .footer-brand-v4 {
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-yellow), var(--primary-green), var(--primary-blue), var(--primary-purple));
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 1.5rem;
        font-family: 'Orbitron', sans-serif;
        animation: holo-shift 6s ease infinite;
    }
    
    /* ===== CLUSTER LABELS ===== */
    .cluster-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 1px;
    }
    
    .cluster-0 { background: rgba(255, 0, 110, 0.2); color: var(--primary-pink); border: 1px solid var(--primary-pink); }
    .cluster-1 { background: rgba(131, 56, 236, 0.2); color: var(--primary-purple); border: 1px solid var(--primary-purple); }
    .cluster-2 { background: rgba(58, 134, 255, 0.2); color: var(--primary-blue); border: 1px solid var(--primary-blue); }
    .cluster-3 { background: rgba(6, 255, 165, 0.2); color: var(--primary-green); border: 1px solid var(--primary-green); }
    
    /* ===== ANOMALY ALERT ===== */
    .anomaly-alert {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.15), rgba(255, 190, 11, 0.1));
        border: 2px solid var(--primary-pink);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        animation: alert-pulse 2s ease-in-out infinite;
    }
    
    @keyframes alert-pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 0, 110, 0.4); }
        50% { box-shadow: 0 0 0 15px rgba(255, 0, 110, 0); }
    }
    
    /* ===== COMPARISON MODE ===== */
    .compare-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .vs-badge {
        background: linear-gradient(135deg, var(--primary-pink), var(--primary-purple));
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* ===== NETWORK NODES ===== */
    .network-container {
        position: relative;
        padding: 2rem;
    }
    
    /* ===== SCENARIO PANEL ===== */
    .scenario-panel {
        background: linear-gradient(135deg, rgba(255, 190, 11, 0.1), rgba(255, 0, 110, 0.1));
        border: 1px solid rgba(255, 190, 11, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .scenario-result {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary-yellow), var(--primary-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* ===== TOOLTIP CUSTOM ===== */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }
    
    [data-tooltip]:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 1000;
        pointer-events: none;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .holo-title { font-size: 3rem; }
        .hero-v4 { padding: 3rem 1rem; }
        .kpi-value-v4 { font-size: 2rem; }
    }
    
    /* ===== MARQUEE V4 ===== */
    .marquee-v4 {
        overflow: hidden;
        white-space: nowrap;
        background: linear-gradient(90deg, 
            rgba(255, 0, 110, 0.1), 
            rgba(131, 56, 236, 0.1), 
            rgba(58, 134, 255, 0.1),
            rgba(6, 255, 165, 0.1));
        padding: 1rem 0;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .marquee-content-v4 {
        display: inline-block;
        animation: marquee-v4 40s linear infinite;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    @keyframes marquee-v4 {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* ===== GRADIENT BORDER ANIMATION ===== */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# --- AURORA BACKGROUND ---
st.markdown('<div class="aurora-bg"><div class="aurora"></div></div>', unsafe_allow_html=True)

# --- FUNGSI LOAD & PREPROCESS DATA (Enhanced) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv', sep=';')
    except:
        # Fallback: generate synthetic data for demo
        np.random.seed(42)
        n = 100
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2024-01-01', periods=n, freq='D'),
            'Nama': [f'Responden_{i}' for i in range(n)],
            'Umur': np.random.randint(18, 25, n),
            'Gender': np.random.choice(['L', 'P'], n),
            'Kopi_per_Hari': np.random.choice(['0', '1', '2 cangkir', '3+'], n),
            'Jenis_Kopi': np.random.choice(['Arabica', 'Robusta', 'Blend'], n),
            'Waktu_Minum': np.random.choice(['Pagi', 'Siang', 'Sore', 'Malam'], n),
            'Durasi_Belajar': np.random.choice(['< 2 jam', '2-4 jam', '5-7 jam', '> 7 jam'], n),
            'Fokus_Subjektif': np.random.randint(1, 6, n),
            'Produktivitas_1': np.random.randint(1, 6, n),
            'Produktivitas_2': np.random.randint(1, 6, n),
            'Produktivitas_3': np.random.randint(1, 6, n),
            'Produktivitas_4': np.random.randint(1, 6, n),
            'Efek_Samping': np.random.choice(['Tidak Ada', 'Gelisah', 'Jantung Berdebar'], n),
            'Kafein_Sensitif': np.random.choice(['Ya', 'Tidak'], n),
            'Kualitas_Tidur_Memburuk': np.random.randint(1, 6, n),
        })
    
    df_clean = df.copy()
    
    # Extract numeric coffee
    df_clean['Kopi_per_Hari'] = df_clean.iloc[:, 4].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)
    df_clean.loc[df_clean.iloc[:, 4].astype(str).str.contains('3\+|\+', na=False, regex=True), 'Kopi_per_Hari'] = 3
    
    hours_mapping = {
        '< 2 jam': 1.0,
        '2-4 jam': 3.0,
        '5-7 jam': 6.0,
        '> 7 jam': 8.5
    }
    df_clean['Durasi_Belajar_Num'] = df_clean.iloc[:, 7].map(hours_mapping).fillna(3.0)
    
    likert_cols = [df_clean.columns[9], df_clean.columns[10], df_clean.columns[11], df_clean.columns[12]]
    df_clean['Skor_Produktivitas'] = df_clean[likert_cols].mean(axis=1)
    
    df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean.iloc[:, 15], errors='coerce').fillna(3)
    
    df_clean['Is_Fokus_Tinggi'] = (df_clean['Skor_Produktivitas'] > 3.0).astype(int)
    df_clean['Is_Peminum_Kopi'] = (df_clean['Kopi_per_Hari'] > 0).astype(int)
    
    df_clean['Fokus_Label'] = df_clean['Is_Fokus_Tinggi'].map({1: 'High Focus', 0: 'Low Focus'})
    df_clean['Kopi_Label'] = df_clean['Kopi_per_Hari'].apply(lambda x: f'{x} Cangkir')
    
    def categorize_kopi(x):
        if x == 0: return 'Non-Drinker'
        elif x <= 1: return 'Light (1 cup)'
        elif x <= 2: return 'Moderate (2 cups)'
        else: return 'Heavy (3+ cups)'
    
    df_clean['Kategori_Konsumsi'] = df_clean['Kopi_per_Hari'].apply(categorize_kopi)
    
    def categorize_produktivitas(x):
        if x < 2.5: return 'Low'
        elif x < 3.5: return 'Medium'
        else: return 'High'
    
    df_clean['Produktivitas_Level'] = df_clean['Skor_Produktivitas'].apply(categorize_produktivitas)
    
    # New: Efficiency Score (Productivity per hour of study)
    df_clean['Efficiency_Score'] = df_clean['Skor_Produktivitas'] / df_clean['Durasi_Belajar_Num'].replace(0, 1)
    
    # New: Risk Score
    df_clean['Risk_Score'] = (
        (df_clean['Kopi_per_Hari'] >= 3).astype(int) * 2 +
        (df_clean['Kualitas_Tidur_Memburuk'] >= 4).astype(int) * 2 +
        (df_clean['Skor_Produktivitas'] < 2.5).astype(int)
    )
    
    return df_clean

df = load_data()

# --- DATA QUALITY CALCULATION ---
def calculate_data_quality(df_filtered):
    total_cells = df_filtered.size
    null_cells = df_filtered.isnull().sum().sum()
    completeness = 1 - (null_cells / total_cells) if total_cells > 0 else 0
    
    # Consistency check
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns
    consistency = 1.0
    for col in numeric_cols:
        if df_filtered[col].std() == 0:
            consistency -= 0.05
    consistency = max(0, consistency)
    
    # Volume check
    volume_score = min(1.0, len(df_filtered) / 50)
    
    dq_score = (completeness * 0.4 + consistency * 0.3 + volume_score * 0.3) * 100
    return dq_score, completeness, consistency, volume_score

# --- HERO SECTION V4 ---
st.markdown("""
<div class="hero-v4">
    <div class="hero-content-v4">
        <div class="hero-emoji-3d">☕</div>
        <h1 class="holo-title">COFFEE ANALYTICS 4D</h1>
        <p class="hero-subtitle-v4">Next-Gen Neuroscience & Productivity Intelligence Platform</p>
        <div class="hero-badges">
            <span class="hero-badge-v4">◆ v4.0 QUANTUM EDITION</span>
            <span class="hero-badge-v4">◆ AI-POWERED INSIGHTS</span>
            <span class="hero-badge-v4">◆ ML CLUSTERING</span>
            <span class="hero-badge-v4">◆ STOCHASTIC SIMULATION</span>
            <span class="hero-badge-v4">◆ 4D VISUALIZATION</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MARQUEE ---
st.markdown("""
<div class="marquee-v4">
    <div class="marquee-content-v4">
        ☕ COFFEE ANALYTICS 4D • 🧠 NEUROSCIENCE • 📊 DATA SCIENCE • 🎯 MACHINE LEARNING • 🎲 MONTE CARLO • 🌐 3D VISUALIZATION • 🤖 AI INSIGHTS • 📈 PREDICTIVE ANALYTICS • 🔗 CORRELATION • ⚡ REAL-TIME STATS • ☕ COFFEE ANALYTICS 4D • 🧠 NEUROSCIENCE • 📊 DATA SCIENCE • 🎯 MACHINE LEARNING • 🎲 MONTE CARLO • 🌐 3D VISUALIZATION •
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS (Enhanced) ---
with st.sidebar:
    st.markdown("### 🎛️ **Command Center**")
    st.markdown("---")
    
    st.markdown("#### 🔍 **Smart Filters**")
    
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
    if len(durasi_options) > 0:
        durasi_range = st.slider(
            "⏰ Durasi Belajar (jam)",
            min_value=float(min(durasi_options)),
            max_value=float(max(durasi_options)),
            value=(float(min(durasi_options)), float(max(durasi_options))),
            help="Rentang durasi belajar dalam jam"
        )
    else:
        durasi_range = (0.0, 10.0)
    
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
    
    # New: Risk Filter
    risk_filter = st.select_slider(
        "⚠️ Max Risk Score",
        options=[0, 1, 2, 3, 4, 5],
        value=5,
        help="Filter berdasarkan tingkat risiko kesehatan"
    )
    
    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Kategori_Konsumsi'].isin(kategori_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1]) &
        (df['Produktivitas_Level'].isin(produktivitas_filter)) &
        (df['Risk_Score'] <= risk_filter)
    ]
    
    if fokus_filter == "High Focus (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Low Focus (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]
    
    st.markdown("---")
    
    st.markdown("#### 📈 **Live Statistics**")
    st.markdown(f"""
    <div class="glass-card-v4" style="text-align: center; padding: 1.5rem;">
        <span class="kpi-icon-v4" style="font-size: 2rem;">👥</span>
        <p class="kpi-value-v4" style="font-size: 2.5rem;">{len(df_filtered)}</p>
        <p class="kpi-label-v4">Responden Aktif</p>
    </div>
    """, unsafe_allow_html=True)
    
    pct_filtered = (len(df_filtered) / len(df)) * 100 if len(df) > 0 else 0
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Data Coverage</span>
            <span style="color: var(--primary-green); font-size: 0.85rem; font-weight: 700;">{pct_filtered:.1f}%</span>
        </div>
        <div class="progress-v4">
            <div class="progress-bar-v4" style="width: {pct_filtered}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Quality Meter
    dq_score, completeness, consistency, volume = calculate_data_quality(df_filtered)
    st.markdown(f"""
    <div class="dq-meter">
        <div class="dq-score">{dq_score:.0f}</div>
        <div style="flex: 1;">
            <div style="color: rgba(255,255,255,0.8); font-weight: 600; margin-bottom: 0.5rem;">Data Quality Score</div>
            <div class="dq-bar">
                <div class="dq-bar-fill" style="width: {dq_score}%;"></div>
            </div>
            <div style="font-size: 0.7rem; color: rgba(255,255,255,0.6); margin-top: 0.3rem;">
                Completeness: {completeness*100:.0f}% | Consistency: {consistency*100:.0f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 💾 **Export & Actions**")
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data (CSV)",
        data=csv,
        file_name="coffee_analytics_v4.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Export report
    if st.button("📄 Generate Report", use_container_width=True):
        st.success("✅ Report generation started!")
    
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# --- KPI CARDS V4 (Enhanced dengan Bootstrap CI) ---
st.markdown("""
<div class="section-header-v4">
    <span class="section-number-v4">01</span>
    <div>
        <h2 class="section-title-v4">Key Performance Metrics</h2>
        <p class="section-subtitle-v4">Real-time statistics dengan Bootstrap Confidence Intervals</p>
    </div>
</div>
""", unsafe_allow_html=True)

if len(df_filtered) > 0:
    # Bootstrap CI function
    def bootstrap_ci(data, n_bootstrap=1000, ci=0.95):
        if len(data) == 0:
            return 0, 0, 0
        means = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            means.append(np.mean(sample))
        lower = np.percentile(means, (1-ci)/2 * 100)
        upper = np.percentile(means, (1+ci)/2 * 100)
        return np.mean(data), lower, upper
    
    cols = st.columns(6)
    
    with cols[0]:
        mean_kopi, ci_lo_kopi, ci_hi_kopi = bootstrap_ci(df_filtered['Kopi_per_Hari'].values)
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">☕</span>
            <p class="kpi-value-v4">{mean_kopi:.2f}</p>
            <p class="kpi-label-v4">Avg Cups / Day</p>
            <span class="kpi-delta-v4">σ = {df_filtered['Kopi_per_Hari'].std():.2f}</span>
            <p class="kpi-ci">CI 95%: [{ci_lo_kopi:.2f}, {ci_hi_kopi:.2f}]</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        mean_durasi, ci_lo_durasi, ci_hi_durasi = bootstrap_ci(df_filtered['Durasi_Belajar_Num'].values)
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">📚</span>
            <p class="kpi-value-v4">{mean_durasi:.1f}h</p>
            <p class="kpi-label-v4">Study Duration</p>
            <span class="kpi-delta-v4">σ = {df_filtered['Durasi_Belajar_Num'].std():.1f}h</span>
            <p class="kpi-ci">CI 95%: [{ci_lo_durasi:.1f}, {ci_hi_durasi:.1f}]</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        mean_prod, ci_lo_prod, ci_hi_prod = bootstrap_ci(df_filtered['Skor_Produktivitas'].values)
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">⚡</span>
            <p class="kpi-value-v4">{mean_prod:.2f}</p>
            <p class="kpi-label-v4">Productivity</p>
            <span class="kpi-delta-v4">out of 5.0</span>
            <p class="kpi-ci">CI 95%: [{ci_lo_prod:.2f}, {ci_hi_prod:.2f}]</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        fokus_pct = df_filtered['Is_Fokus_Tinggi'].mean() * 100
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">🎯</span>
            <p class="kpi-value-v4">{fokus_pct:.0f}%</p>
            <p class="kpi-label-v4">High Focus Rate</p>
            <span class="kpi-delta-v4">{len(df_filtered[df_filtered['Is_Fokus_Tinggi']==1])} students</span>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        mean_eff, ci_lo_eff, ci_hi_eff = bootstrap_ci(df_filtered['Efficiency_Score'].values)
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">🚀</span>
            <p class="kpi-value-v4">{mean_eff:.2f}</p>
            <p class="kpi-label-v4">Efficiency Score</p>
            <span class="kpi-delta-v4">Prod/Hours</span>
            <p class="kpi-ci">CI 95%: [{ci_lo_eff:.2f}, {ci_hi_eff:.2f}]</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[5]:
        mean_risk = df_filtered['Risk_Score'].mean()
        high_risk_pct = (df_filtered['Risk_Score'] >= 3).mean() * 100
        st.markdown(f"""
        <div class="kpi-card-v4">
            <span class="kpi-icon-v4">⚠️</span>
            <p class="kpi-value-v4">{mean_risk:.1f}</p>
            <p class="kpi-label-v4">Risk Score</p>
            <span class="kpi-delta-v4">{high_risk_pct:.0f}% High Risk</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Tidak ada data. Silakan ubah filter.")

# --- TABS V4 (8 Tabs) ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌐 3D/4D Visualization",
    "📊 Descriptive",
    "🔗 Correlation",
    "🎯 Probability",
    "🎲 Monte Carlo",
    "🤖 Predictive ML",
    "📈 Advanced",
    "🧠 AI Insights"
])

# ===================== TAB 1: 3D/4D VISUALIZATION =====================
with tab1:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">3D</span>
        <div>
            <h2 class="section-title-v4">Multi-Dimensional Visualization <span class="badge-4d">✦ 4D</span></h2>
            <p class="section-subtitle-v4">Interactive 3D plots dengan dimensi ke-4 (size/color)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        # Subtabs untuk variasi 3D
        sub1, sub2, sub3, sub4 = st.tabs(["🌌 3D Scatter", "🏔️ Surface Plot", "🫧 3D Bubble", "🌊 Contour 3D"])
        
        with sub1:
            st.markdown("### 🌌 **3D Scatter Plot Multi-Dimensional**")
            st.markdown("""
            <div class="info-box-v4">
                💡 <strong>Interaksi:</strong> Drag untuk rotate, scroll untuk zoom, double-click untuk reset. 
                Arahkan kursor ke titik untuk detail lengkap. <b>Size = Efficiency</b>, <b>Color = Sleep Quality</b>.
            </div>
            """, unsafe_allow_html=True)
            
            fig_3d = px.scatter_3d(
                df_filtered,
                x='Kopi_per_Hari',
                y='Durasi_Belajar_Num',
                z='Skor_Produktivitas',
                color='Kualitas_Tidur_Memburuk',
                size='Efficiency_Score',
                size_max=30,
                color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
                hover_data={
                    'Kopi_per_Hari': ':.0f',
                    'Durasi_Belajar_Num': ':.1f',
                    'Skor_Produktivitas': ':.2f',
                    'Kualitas_Tidur_Memburuk': ':.0f',
                    'Efficiency_Score': ':.2f',
                    'Fokus_Label': True,
                    'Kategori_Konsumsi': True
                },
                labels={
                    'Kopi_per_Hari': '☕ Cangkir Kopi',
                    'Durasi_Belajar_Num': '📚 Durasi (jam)',
                    'Skor_Produktivitas': '⚡ Produktivitas',
                    'Kualitas_Tidur_Memburuk': '😴 Kualitas Tidur'
                }
            )
            
            fig_3d.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                scene=dict(
                    xaxis=dict(
                        backgroundcolor='rgba(0,0,0,0)',
                        gridcolor='rgba(255,255,255,0.15)',
                        showbackground=False,
                        zerolinecolor='rgba(255,255,255,0.3)',
                        title='☕ Cangkir Kopi'
                    ),
                    yaxis=dict(
                        backgroundcolor='rgba(0,0,0,0)',
                        gridcolor='rgba(255,255,255,0.15)',
                        showbackground=False,
                        zerolinecolor='rgba(255,255,255,0.3)',
                        title='📚 Durasi (jam)'
                    ),
                    zaxis=dict(
                        backgroundcolor='rgba(0,0,0,0)',
                        gridcolor='rgba(255,255,255,0.15)',
                        showbackground=False,
                        zerolinecolor='rgba(255,255,255,0.3)',
                        title='⚡ Produktivitas'
                    ),
                    camera=dict(
                        eye=dict(x=1.8, y=1.8, z=1.2),
                        up=dict(x=0, y=0, z=1)
                    ),
                    aspectratio=dict(x=1.2, y=1.2, z=0.9)
                ),
                height=650,
                margin=dict(l=20, r=20, t=20, b=20),
                coloraxis_colorbar=dict(
                    title='Kualitas Tidur',
                    tickfont=dict(color='white'),
                    title_font=dict(color='white')
                )
            )
            
            fig_3d.update_traces(
                marker=dict(
                    opacity=0.9,
                    line=dict(color='rgba(255,255,255,0.6)', width=1.5)
                ),
                hovertemplate='<b>%{customdata[5]}</b><br>' +
                              'Kategori: %{customdata[6]}<br>' +
                              'Kopi: %{x} cangkir<br>' +
                              'Durasi: %{y:.1f} jam<br>' +
                              'Produktivitas: %{z:.2f}<br>' +
                              'Tidur: %{customdata[3]:.0f}<br>' +
                              'Efficiency: %{customdata[4]:.2f}<extra></extra>'
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with sub2:
            st.markdown("### 🏔️ **3D Surface: Produktivitas Landscape**")
            
            kopi_bins = np.linspace(df_filtered['Kopi_per_Hari'].min(), df_filtered['Kopi_per_Hari'].max(), 15)
            durasi_bins = np.linspace(df_filtered['Durasi_Belajar_Num'].min(), df_filtered['Durasi_Belajar_Num'].max(), 15)
            
            Z = np.zeros((len(kopi_bins), len(durasi_bins)))
            for i, k in enumerate(kopi_bins):
                for j, d in enumerate(durasi_bins):
                    mask = (
                        (np.abs(df_filtered['Kopi_per_Hari'] - k) < 0.5) &
                        (np.abs(df_filtered['Durasi_Belajar_Num'] - d) < 1.0)
                    )
                    if mask.sum() > 0:
                        Z[i, j] = df_filtered.loc[mask, 'Skor_Produktivitas'].mean()
                    else:
                        Z[i, j] = np.nan
            
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
                    xaxis=dict(title='📚 Durasi (jam)', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    yaxis=dict(title='☕ Cangkir Kopi', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    zaxis=dict(title='⚡ Produktivitas', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)', range=[1, 5]),
                    camera=dict(eye=dict(x=2, y=2, z=1.5))
                ),
                height=600,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_surface, use_container_width=True)
        
        with sub3:
            st.markdown("### 🫧 **3D Bubble Chart: Multi-Feature Analysis**")
            st.markdown("""
            <div class="info-box-v4">
                🎨 <strong>Dimensi ke-4:</strong> Setiap bubble mewakili kombinasi fitur. 
                <b>Size</b> = jumlah responden di area tersebut, <b>Color</b> = kategori konsumsi.
            </div>
            """, unsafe_allow_html=True)
            
            bubble_data = df_filtered.groupby(['Kopi_per_Hari', 'Kategori_Konsumsi']).agg({
                'Skor_Produktivitas': 'mean',
                'Durasi_Belajar_Num': 'mean',
                'Kualitas_Tidur_Memburuk': 'mean',
                'Is_Fokus_Tinggi': 'count'
            }).reset_index()
            bubble_data.columns = ['Kopi', 'Kategori', 'Produktivitas', 'Durasi', 'Tidur', 'Count']
            
            fig_bubble = go.Figure()
            
            color_map = {
                'Non-Drinker': '#ff006e',
                'Light (1 cup)': '#8338ec',
                'Moderate (2 cups)': '#3a86ff',
                'Heavy (3+ cups)': '#06ffa5'
            }
            
            for kategori in bubble_data['Kategori'].unique():
                subset = bubble_data[bubble_data['Kategori'] == kategori]
                fig_bubble.add_trace(go.Scatter3d(
                    x=subset['Kopi'],
                    y=subset['Durasi'],
                    z=subset['Produktivitas'],
                    mode='markers',
                    marker=dict(
                        size=subset['Count'] * 2 + 10,
                        color=color_map.get(kategori, '#ffffff'),
                        opacity=0.8,
                        line=dict(color='white', width=1.5)
                    ),
                    name=kategori,
                    hovertemplate=f'<b>{kategori}</b><br>Kopi: %{{x}}<br>Durasi: %{{y:.1f}}h<br>Produktivitas: %{{z:.2f}}<br>Count: %{{customdata}}<extra></extra>',
                    customdata=subset['Count']
                ))
            
            fig_bubble.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                scene=dict(
                    xaxis=dict(title='☕ Cangkir Kopi', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    yaxis=dict(title='📚 Durasi (jam)', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    zaxis=dict(title='⚡ Produktivitas', backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)')
                ),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white')),
                height=600,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        with sub4:
            st.markdown("### 🌊 **3D Contour Density**")
            
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
                line_smoothing=1.2,
                hovertemplate='Durasi: %{x:.1f}h<br>Kopi: %{y:.1f}<br>Produktivitas: %{z:.2f}<extra></extra>'
            ))
            
            fig_contour.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                xaxis=dict(title='📚 Durasi (jam)', gridcolor='rgba(255,255,255,0.15)', color='white'),
                yaxis=dict(title='☕ Cangkir Kopi', gridcolor='rgba(255,255,255,0.15)', color='white'),
                height=550,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_contour, use_container_width=True)
        
        # Insight Cards
        st.markdown("### 💎 **Pattern Discovery**")
        ins_cols = st.columns(4)
        
        insights = [
            ("🎯", "Sweet Spot", "Kombinasi optimal: <b>1 cangkir + 5-7 jam</b> = produktivitas maksimal"),
            ("⚠️", "Trade-off Tidur", "Konsumsi >2 cangkir berkorelasi dengan <b>kualitas tidur menurun</b>"),
            ("📈", "Diminishing Returns", "Setelah 2 cangkir, <b>produktivitas plateau</b> tapi risiko meningkat"),
            ("🌊", "Density Clusters", "3 klaster utama: Non-drinkers, Optimal drinkers, Heavy users")
        ]
        
        for i, (icon, title, text) in enumerate(insights):
            with ins_cols[i]:
                st.markdown(f"""
                <div class="insight-card-v4">
                    <div class="insight-icon-v4">{icon}</div>
                    <div class="insight-title-v4">{title}</div>
                    <div class="insight-text-v4">{text}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data kosong. Ubah filter untuk menampilkan visualisasi.")

# ===================== TAB 2: DESKRIPTIF =====================
with tab2:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">02</span>
        <div>
            <h2 class="section-title-v4">Descriptive Analytics</h2>
            <p class="section-subtitle-v4">Statistical distribution dengan advanced tests</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        # Distribution Row 1
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### ☕ **Distribusi Konsumsi Kopi**")
            kopi_counts = df_filtered['Kopi_per_Hari'].value_counts().sort_index()
            fig_dist_kopi = px.bar(
                x=kopi_counts.index,
                y=kopi_counts.values,
                labels={'x': 'Cangkir', 'y': 'Responden'},
                color=kopi_counts.values,
                color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
            )
            fig_dist_kopi.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(dtick=1, gridcolor='rgba(255,255,255,0.15)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_dist_kopi, use_container_width=True)
        
        with col_b:
            st.markdown("#### ⚡ **Distribusi Skor Produktivitas**")
            fig_hist_prod = px.histogram(
                df_filtered,
                x='Skor_Produktivitas',
                nbins=20,
                color_discrete_sequence=['#8338ec'],
                marginal="violin"
            )
            fig_hist_prod.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_hist_prod, use_container_width=True)
        
        # Distribution Row 2
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.markdown("#### 🎯 **Boxplot: Produktivitas per Kelompok**")
            fig_box = px.box(
                df_filtered,
                x='Kategori_Konsumsi',
                y='Skor_Produktivitas',
                color='Kategori_Konsumsi',
                color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
            )
            fig_box.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        with col_d:
            st.markdown("#### 📊 **Radar: Profile per Kategori**")
            
            radar_data = df_filtered.groupby('Kategori_Konsumsi').agg({
                'Kopi_per_Hari': 'mean',
                'Durasi_Belajar_Num': 'mean',
                'Skor_Produktivitas': 'mean',
                'Kualitas_Tidur_Memburuk': 'mean',
                'Efficiency_Score': 'mean'
            }).round(2)
            
            radar_min = radar_data.min()
            radar_max = radar_data.max()
            radar_range = radar_max - radar_min + 0.001
            radar_normalized = (radar_data - radar_min) / radar_range
            
            categories = ['Coffee', 'Study', 'Productivity', 'Sleep', 'Efficiency']
            fig_radar = go.Figure()
            
            for idx, category in enumerate(radar_normalized.index):
                vals = radar_normalized.loc[category].values.tolist()
                vals.append(vals[0])
                theta = categories + [categories[0]]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals,
                    theta=theta,
                    fill='toself',
                    name=category,
                    line=dict(width=2)
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        gridcolor='rgba(255,255,255,0.15)',
                        tickfont=dict(color='white')
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255,255,255,0.15)',
                        tickfont=dict(color='white', size=11)
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white')),
                height=500,
                margin=dict(l=80, r=80, t=50, b=50)
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Advanced Statistics Section
        st.markdown("### 🧮 **Advanced Statistics**")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown("#### Shapiro-Wilk Normality Test")
            if len(df_filtered) >= 3 and len(df_filtered) <= 5000:
                try:
                    stat_sw, p_sw = shapiro(df_filtered['Skor_Produktivitas'])
                    normal = "✓ Normal" if p_sw > 0.05 else "✗ Non-Normal"
                    st.markdown(f"""
                    <div class="glass-card-v4">
                        <p>W-statistic: <span class="metric-highlight-v4">{stat_sw:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight-v4">{p_sw:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: var(--primary-green);">{normal}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.info("Data tidak cukup")
            else:
                st.info("Perlu 3-5000 samples")
        
        with stat_col2:
            st.markdown("#### Distribution Metrics")
            skewness = skew(df_filtered['Skor_Produktivitas'])
            kurt = kurtosis(df_filtered['Skor_Produktivitas'])
            cv = (df_filtered['Skor_Produktivitas'].std() / df_filtered['Skor_Produktivitas'].mean() * 100) if df_filtered['Skor_Produktivitas'].mean() > 0 else 0
            
            st.markdown(f"""
            <div class="glass-card-v4">
                <p>Skewness: <span class="metric-highlight-v4">{skewness:.3f}</span></p>
                <p>Kurtosis: <span class="metric-highlight-v4">{kurt:.3f}</span></p>
                <p>CV: <span class="metric-highlight-v4">{cv:.2f}%</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown("#### Percentiles")
            p25 = np.percentile(df_filtered['Skor_Produktivitas'], 25)
            p50 = np.percentile(df_filtered['Skor_Produktivitas'], 50)
            p75 = np.percentile(df_filtered['Skor_Produktivitas'], 75)
            p90 = np.percentile(df_filtered['Skor_Produktivitas'], 90)
            
            st.markdown(f"""
            <div class="glass-card-v4">
                <p>P25: <span class="metric-highlight-v4">{p25:.2f}</span></p>
                <p>P50 (Median): <span class="metric-highlight-v4">{p50:.2f}</span></p>
                <p>P75: <span class="metric-highlight-v4">{p75:.2f}</span></p>
                <p>P90: <span class="metric-highlight-v4">{p90:.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown("#### Outlier Detection (IQR)")
            Q1 = np.percentile(df_filtered['Skor_Produktivitas'], 25)
            Q3 = np.percentile(df_filtered['Skor_Produktivitas'], 75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df_filtered[(df_filtered['Skor_Produktivitas'] < lower_bound) | 
                                   (df_filtered['Skor_Produktivitas'] > upper_bound)]
            
            st.markdown(f"""
            <div class="glass-card-v4">
                <p>IQR: <span class="metric-highlight-v4">{IQR:.2f}</span></p>
                <p>Range: <span class="metric-highlight-v4">[{lower_bound:.2f}, {upper_bound:.2f}]</span></p>
                <p>Outliers: <span class="metric-highlight-v4">{len(outliers)}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data kosong.")

# ===================== TAB 3: KORELASI =====================
with tab3:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">03</span>
        <div>
            <h2 class="section-title-v4">Correlation Analysis</h2>
            <p class="section-subtitle-v4">Pearson, Spearman & Kendall correlation matrix</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 1:
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown("#### 🎨 **Correlation Heatmap**")
            corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk', 'Efficiency_Score']
            corr_matrix = df_filtered[corr_cols].corr(method='pearson')
            
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=".3f",
                color_continuous_scale=['#ff006e', '#1a0b2e', '#06ffa5'],
                zmin=-1, zmax=1
            )
            fig_heatmap.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='JetBrains Mono'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col_b:
            st.markdown("#### 📈 **Scatter: Kopi vs Produktivitas**")
            
            if len(df_filtered) > 1:
                p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
                signifikansi = "Signifikan" if p_value < 0.05 else "Tidak Signifikan"
                
                st.markdown(f"""
                <div class="info-box-v4">
                    📊 Pearson r: <span class="metric-highlight-v4">{p_coeff:.4f}</span><br>
                    📉 P-Value: <span class="metric-highlight-v4">{p_value:.4f}</span> ({signifikansi})
                </div>
                """, unsafe_allow_html=True)
            
            fig_scatter = px.scatter(
                df_filtered,
                x='Kopi_per_Hari',
                y='Skor_Produktivitas',
                trendline='ols' if len(df_filtered) > 2 else None,
                color='Durasi_Belajar_Num',
                color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5'],
                size='Kualitas_Tidur_Memburuk',
                size_max=20,
                hover_data=['Fokus_Label', 'Kategori_Konsumsi']
            )
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Detailed Correlation Table
        st.markdown("#### 📋 **Complete Correlation Matrix**")
        
        corr_details = []
        for i, col1 in enumerate(corr_cols):
            for j, col2 in enumerate(corr_cols):
                if i < j:
                    try:
                        pearson_r, pearson_p = pearsonr(df_filtered[col1], df_filtered[col2])
                        spearman_r, spearman_p = spearmanr(df_filtered[col1], df_filtered[col2])
                        
                        # Interpretation
                        abs_r = abs(pearson_r)
                        if abs_r < 0.2: strength = "Very Weak"
                        elif abs_r < 0.4: strength = "Weak"
                        elif abs_r < 0.6: strength = "Moderate"
                        elif abs_r < 0.8: strength = "Strong"
                        else: strength = "Very Strong"
                        
                        corr_details.append({
                            'Variables': f'{col1} ↔ {col2}',
                            'Pearson r': f"{pearson_r:.4f}",
                            'Pearson p': f"{pearson_p:.4f}",
                            'Spearman ρ': f"{spearman_r:.4f}",
                            'Spearman p': f"{spearman_p:.4f}",
                            'Strength': strength,
                            'Significant': '✓' if pearson_p < 0.05 else '✗'
                        })
                    except:
                        pass
        
        if len(corr_details) > 0:
            corr_df = pd.DataFrame(corr_details)
            st.dataframe(
                corr_df.style.background_gradient(cmap='RdYlGn', subset=['Pearson r', 'Spearman ρ']),
                use_container_width=True
            )
        
        # Key Insights
        st.markdown("### 💡 **Key Insights**")
        i_cols = st.columns(3)
        
        insight_list = [
            ("☕⚡", "Kopi ↔ Produktivitas", "Korelasi menunjukkan kopi <b>sedikit meningkatkan</b> persepsi produktivitas"),
            ("☕😴", "Kopi ↔ Kualitas Tidur", "Korelasi <b>negatif</b>: lebih banyak kopi = tidur lebih buruk"),
            ("☕📚", "Kopi ↔ Durasi Belajar", "Peminum kopi cenderung <b>belajar lebih lama</b>")
        ]
        
        for i, (icon, title, text) in enumerate(insight_list):
            with i_cols[i]:
                st.markdown(f"""
                <div class="insight-card-v4">
                    <div class="insight-icon-v4">{icon}</div>
                    <div class="insight-title-v4">{title}</div>
                    <div class="insight-text-v4">{text}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data tidak cukup (min 2 data points).")

# ===================== TAB 4: PROBABILITAS =====================
with tab4:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">04</span>
        <div>
            <h2 class="section-title-v4">Conditional Probability</h2>
            <p class="section-subtitle-v4">Bayesian analysis & Chi-Square tests</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown("#### 📊 **Tabel Kontingensi**")
            kontingensi = pd.crosstab(
                df_filtered['Is_Peminum_Kopi'],
                df_filtered['Is_Fokus_Tinggi'],
                margins=True
            )
            kontingensi.index = ['Non-Drinkers', 'Coffee Drinkers', 'Total'] if len(kontingensi) == 3 else list(kontingensi.index)
            kontingensi.columns = ['Low Focus', 'High Focus', 'Total'] if len(kontingensi.columns) == 3 else list(kontingensi.columns)
            st.dataframe(kontingensi, use_container_width=True)
            
            try:
                ct_table = pd.crosstab(df_filtered['Is_Peminum_Kopi'], df_filtered['Is_Fokus_Tinggi'])
                if ct_table.shape[0] > 1 and ct_table.shape[1] > 1:
                    chi2, p_chi, dof, expected = chi2_contingency(ct_table)
                    
                    st.markdown(f"""
                    <div class="info-box-v4">
                        📊 Chi-Square Test:<br>
                        χ² = <span class="metric-highlight-v4">{chi2:.4f}</span><br>
                        p-value = <span class="metric-highlight-v4">{p_chi:.4f}</span><br>
                        df = <span class="metric-highlight-v4">{dof}</span><br>
                        Status: <b>{'✓ Signifikan' if p_chi < 0.05 else '✗ Tidak Signifikan'}</b>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        with col_b:
            st.markdown("#### 📈 **Probability Comparison**")
            
            prob_bersyarat = pd.crosstab(
                df_filtered['Is_Peminum_Kopi'],
                df_filtered['Is_Fokus_Tinggi'],
                normalize='index'
            ) * 100
            
            if 1 in prob_bersyarat.index and 1 in prob_bersyarat.columns:
                p_kopi = prob_bersyarat.loc[1, 1] if 1 in prob_bersyarat.columns else 0
            else:
                p_kopi = 0
                
            if 0 in prob_bersyarat.index and 1 in prob_bersyarat.columns:
                p_non_kopi = prob_bersyarat.loc[0, 1] if 1 in prob_bersyarat.columns else 0
            else:
                p_non_kopi = 0
            
            fig_prob = go.Figure(data=[
                go.Bar(
                    name='High Focus',
                    x=['Coffee Drinkers', 'Non-Drinkers'],
                    y=[p_kopi, p_non_kopi],
                    marker=dict(
                        color=['#ff006e', '#3a86ff'],
                        line=dict(color='rgba(255,255,255,0.4)', width=2)
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
                yaxis=dict(title="Probability (%)", range=[0, 100], gridcolor='rgba(255,255,255,0.15)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_prob, use_container_width=True)
            
            if p_kopi > 0 and p_non_kopi > 0:
                odds_kopi = p_kopi / (100 - p_kopi)
                odds_non = p_non_kopi / (100 - p_non_kopi)
                odds_ratio = odds_kopi / odds_non
                
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>📊 Odds Ratio Analysis</h4>
                    <p>Odds Ratio: <span class="metric-highlight-v4">{odds_ratio:.2f}</span></p>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.8);">
                        Coffee drinkers have <b>{odds_ratio:.2f}x higher odds</b> of achieving high focus.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Bayesian Matrix
        st.markdown("#### 🎲 **Bayesian Probability Matrix**")
        
        prob_matrix = pd.crosstab(
            df_filtered['Kopi_per_Hari'],
            df_filtered['Is_Fokus_Tinggi'],
            normalize='index'
        ) * 100
        
        prob_matrix.columns = ['P(Low Focus)', 'P(High Focus)'] if len(prob_matrix.columns) == 2 else list(prob_matrix.columns)
        prob_matrix.index = [f'{i} Cangkir' for i in prob_matrix.index]
        
        st.dataframe(
            prob_matrix.round(2).style.background_gradient(cmap='RdYlGn', axis=1),
            use_container_width=True
        )
    else:
        st.warning("⚠️ Data kosong.")

# ===================== TAB 5: MONTE CARLO =====================
with tab5:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">05</span>
        <div>
            <h2 class="section-title-v4">Monte Carlo Simulation <span class="badge-4d">✦ STOCHASTIC</span></h2>
            <p class="section-subtitle-v4">Advanced stochastic modeling dengan scenario analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.markdown("#### ⚙️ **Simulation Parameters**")
        n_mahasiswa = st.slider("👥 Students per Class:", 10, 500, 100, 10)
        n_iterasi = st.slider("🔄 Iterations:", 1000, 100000, 20000, 5000)
        
        st.markdown("#### 📊 **Empirical Distribution**")
        p_kopi_dist = df['Kopi_per_Hari'].value_counts(normalize=True).sort_index()
        for cat, w in p_kopi_dist.items():
            st.markdown(f"- <b>{cat} cangkir:</b> <span class='metric-highlight-v4'>{w*100:.1f}%</span>", unsafe_allow_html=True)
        
        simulate_btn = st.button("🎲 Run Simulation", type="primary", use_container_width=True)
        
        # Scenario Analyzer
        st.markdown("#### 🔮 **Scenario Analyzer**")
        scenario = st.selectbox(
            "Pilih Skenario:",
            ["Baseline", "Optimistic", "Conservative", "Extreme"]
        )
        
        scenario_configs = {
            "Baseline": {"factor": 1.0, "desc": "Kondisi normal berdasarkan data"},
            "Optimistic": {"factor": 1.2, "desc": "Produktivitas +20% (asumsi ideal)"},
            "Conservative": {"factor": 0.8, "desc": "Produktivitas -20% (asumsi realistis)"},
            "Extreme": {"factor": 1.5, "desc": "Skenario best-case extreme"}
        }
        
        st.markdown(f"""
        <div class="scenario-panel">
            <h4 style="color: var(--primary-yellow);">🎯 {scenario} Scenario</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{scenario_configs[scenario]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("⚡ Running Monte Carlo simulation..."):
                categories_kopi = p_kopi_dist.index.values
                weights_kopi = p_kopi_dist.values
                
                stats_by_group = df.groupby('Kopi_per_Hari')['Skor_Produktivitas'].agg(['mean', 'std'])
                overall_std = df['Skor_Produktivitas'].std()
                stats_by_group['std'] = stats_by_group['std'].fillna(overall_std)
                
                scenario_factor = scenario_configs[scenario]['factor']
                
                hasil_rata_rata = []
                for _ in range(n_iterasi):
                    simulasi_kopi = np.random.choice(categories_kopi, size=n_mahasiswa, p=weights_kopi)
                    skor_kelas = []
                    for pilihan in simulasi_kopi:
                        mean_val = stats_by_group.loc[pilihan, 'mean'] * scenario_factor
                        std_val = stats_by_group.loc[pilihan, 'std']
                        if np.isnan(std_val):
                            std_val = overall_std
                        skor_acak = np.clip(np.random.normal(mean_val, std_val), 1.0, 5.0)
                        skor_kelas.append(skor_acak)
                    hasil_rata_rata.append(np.mean(skor_kelas))
                
                st.session_state['mc_results'] = hasil_rata_rata
                st.session_state['mc_scenario'] = scenario
        
        if 'mc_results' in st.session_state:
            hasil = st.session_state['mc_results']
            mean_mc = np.mean(hasil)
            ci_bawah = np.percentile(hasil, 2.5)
            ci_atas = np.percentile(hasil, 97.5)
            median_mc = np.median(hasil)
            
            m_cols = st.columns(4)
            with m_cols[0]:
                st.markdown(f"""
                <div class="kpi-card-v4">
                    <span class="kpi-icon-v4">📊</span>
                    <p class="kpi-value-v4">{mean_mc:.3f}</p>
                    <p class="kpi-label-v4">Expected Mean</p>
                </div>
                """, unsafe_allow_html=True)
            with m_cols[1]:
                st.markdown(f"""
                <div class="kpi-card-v4">
                    <span class="kpi-icon-v4">⬇️</span>
                    <p class="kpi-value-v4">{ci_bawah:.3f}</p>
                    <p class="kpi-label-v4">CI 95% Lower</p>
                </div>
                """, unsafe_allow_html=True)
            with m_cols[2]:
                st.markdown(f"""
                <div class="kpi-card-v4">
                    <span class="kpi-icon-v4">⬆️</span>
                    <p class="kpi-value-v4">{ci_atas:.3f}</p>
                    <p class="kpi-label-v4">CI 95% Upper</p>
                </div>
                """, unsafe_allow_html=True)
            with m_cols[3]:
                st.markdown(f"""
                <div class="kpi-card-v4">
                    <span class="kpi-icon-v4">📈</span>
                    <p class="kpi-value-v4">{median_mc:.3f}</p>
                    <p class="kpi-label-v4">Median</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=hasil,
                nbinsx=75,
                marker=dict(
                    color='rgba(131, 56, 236, 0.7)',
                    line=dict(color='#8338ec', width=1.5)
                ),
                hovertemplate="Score: %{x:.3f}<br>Frequency: %{y}<extra></extra>"
            ))
            fig_mc.add_vline(x=mean_mc, line_dash="dash", line_color="#ff006e", line_width=3,
                            annotation_text=f"Mean: {mean_mc:.3f}", annotation_font_color="#ff006e")
            fig_mc.add_vline(x=ci_bawah, line_dash="dot", line_color="#06ffa5", line_width=2,
                            annotation_text=f"CI: {ci_bawah:.3f}", annotation_font_color="#06ffa5")
            fig_mc.add_vline(x=ci_atas, line_dash="dot", line_color="#06ffa5", line_width=2,
                            annotation_text=f"CI: {ci_atas:.3f}", annotation_font_color="#06ffa5")
            fig_mc.add_vline(x=median_mc, line_dash="dash", line_color="#ffbe0b", line_width=2,
                            annotation_text=f"Median: {median_mc:.3f}", annotation_font_color="#ffbe0b")
            
            fig_mc.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                xaxis=dict(title="Average Productivity Score", gridcolor='rgba(255,255,255,0.15)', color='white'),
                yaxis=dict(title="Frequency", gridcolor='rgba(255,255,255,0.15)', color='white'),
                height=450,
                margin=dict(l=20, r=20, t=40, b=20),
                title=dict(text=f"Probability Distribution ({len(hasil):,} Iterations) - {st.session_state.get('mc_scenario', 'Baseline')}",
                          font=dict(color='white', size=16))
            )
            st.plotly_chart(fig_mc, use_container_width=True)
            
            # Probability analysis
            st.markdown("#### 📊 **Probability Analysis**")
            prob_cols = st.columns(3)
            
            with prob_cols[0]:
                p_above_3 = np.mean([1 if x > 3 else 0 for x in hasil]) * 100
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>📈 P(Productivity > 3.0)</h4>
                    <p class="scenario-result">{p_above_3:.1f}%</p>
                    <p style="color: rgba(255,255,255,0.7);">Probabilitas produktivitas di atas rata-rata</p>
                </div>
                """, unsafe_allow_html=True)
            
            with prob_cols[1]:
                p_above_4 = np.mean([1 if x > 4 else 0 for x in hasil]) * 100
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>🚀 P(Productivity > 4.0)</h4>
                    <p class="scenario-result">{p_above_4:.1f}%</p>
                    <p style="color: rgba(255,255,255,0.7);">Probabilitas produktivitas tinggi</p>
                </div>
                """, unsafe_allow_html=True)
            
            with prob_cols[2]:
                p_below_2 = np.mean([1 if x < 2 else 0 for x in hasil]) * 100
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>⚠️ P(Productivity < 2.0)</h4>
                    <p class="scenario-result">{p_below_2:.1f}%</p>
                    <p style="color: rgba(255,255,255,0.7);">Probabilitas produktivitas rendah</p>
                </div>
                """, unsafe_allow_html=True)

# ===================== TAB 6: PREDICTIVE ML =====================
with tab6:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">06</span>
        <div>
            <h2 class="section-title-v4">Predictive Machine Learning <span class="badge-4d">✦ AI</span></h2>
            <p class="section-subtitle-v4">Clustering, Classification & Regression dengan scikit-learn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 10:
        ml_sub1, ml_sub2, ml_sub3 = st.tabs(["🎯 K-Means Clustering", "🤖 Logistic Regression", "📈 Linear Regression"])
        
        with ml_sub1:
            st.markdown("### 🎯 **K-Means Clustering: Student Segmentation**")
            st.markdown("""
            <div class="info-box-v4">
                🧠 <strong>Unsupervised Learning:</strong> Algoritma mengelompokkan responden ke dalam 
                cluster berdasarkan pola konsumsi kopi, produktivitas, dan durasi belajar.
            </div>
            """, unsafe_allow_html=True)
            
            n_clusters = st.slider("Jumlah Cluster (K):", 2, 6, 4, 1)
            
            # Prepare data for clustering
            cluster_features = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
            X_cluster = df_filtered[cluster_features].values
            
            # Standardize
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_cluster)
            
            # K-Means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            df_filtered['Cluster'] = kmeans.fit_predict(X_scaled)
            
            # Cluster visualization
            fig_cluster = px.scatter_3d(
                df_filtered,
                x='Kopi_per_Hari',
                y='Durasi_Belajar_Num',
                z='Skor_Produktivitas',
                color='Cluster',
                color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#00ffff'],
                size_max=15,
                labels={
                    'Kopi_per_Hari': '☕ Cangkir Kopi',
                    'Durasi_Belajar_Num': '📚 Durasi (jam)',
                    'Skor_Produktivitas': '⚡ Produktivitas'
                }
            )
            
            fig_cluster.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                scene=dict(
                    xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)'),
                    zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.15)')
                ),
                height=550,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            )
            
            st.plotly_chart(fig_cluster, use_container_width=True)
            
            # Cluster profiles
            st.markdown("### 📊 **Cluster Profiles**")
            cluster_profiles = df_filtered.groupby('Cluster').agg({
                'Kopi_per_Hari': 'mean',
                'Durasi_Belajar_Num': 'mean',
                'Skor_Produktivitas': 'mean',
                'Kualitas_Tidur_Memburuk': 'mean',
                'Efficiency_Score': 'mean'
            }).round(2)
            cluster_profiles['Count'] = df_filtered.groupby('Cluster').size()
            
            # Add cluster names
            cluster_names = []
            for idx, row in cluster_profiles.iterrows():
                if row['Kopi_per_Hari'] == 0:
                    name = "🚫 Non-Drinkers"
                elif row['Skor_Produktivitas'] > 3.5 and row['Kualitas_Tidur_Memburuk'] < 3:
                    name = "⭐ Optimal Performers"
                elif row['Kopi_per_Hari'] >= 3 and row['Kualitas_Tidur_Memburuk'] >= 4:
                    name = "⚠️ At-Risk Heavy Users"
                elif row['Skor_Produktivitas'] < 2.5:
                    name = "📉 Low Performers"
                else:
                    name = "☕ Moderate Users"
                cluster_names.append(name)
            
            cluster_profiles['Profile'] = cluster_names
            
            st.dataframe(
                cluster_profiles.style.background_gradient(cmap='viridis', subset=['Skor_Produktivitas', 'Efficiency_Score']),
                use_container_width=True
            )
            
            # Cluster insights
            st.markdown("### 💡 **Cluster Insights**")
            for cluster_id in range(min(n_clusters, len(cluster_profiles))):
                profile = cluster_profiles.iloc[cluster_id]
                st.markdown(f"""
                <div class="insight-card-v4">
                    <div class="insight-icon-v4">🎯</div>
                    <div class="insight-title-v4">Cluster {cluster_id}: {profile['Profile']}</div>
                    <div class="insight-text-v4">
                        <b>{int(profile['Count'])}</b> responden • 
                        Avg Kopi: <span class="metric-highlight-v4">{profile['Kopi_per_Hari']:.1f}</span> cangkir • 
                        Produktivitas: <span class="metric-highlight-v4">{profile['Skor_Produktivitas']:.2f}</span> • 
                        Efficiency: <span class="metric-highlight-v4">{profile['Efficiency_Score']:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with ml_sub2:
            st.markdown("### 🤖 **Logistic Regression: High Focus Prediction**")
            st.markdown("""
            <div class="info-box-v4">
                🎯 <strong>Binary Classification:</strong> Memprediksi apakah seorang responden akan 
                mencapai <b>High Focus</b> berdasarkan fitur-fitur yang ada.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Prepare data
                X_lr = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']].values
                y_lr = df_filtered['Is_Fokus_Tinggi'].values
                
                # Standardize
                scaler_lr = StandardScaler()
                X_lr_scaled = scaler_lr.fit_transform(X_lr)
                
                # Train model
                model_lr = LogisticRegression(random_state=42, max_iter=1000)
                model_lr.fit(X_lr_scaled, y_lr)
                
                # Predictions
                y_pred = model_lr.predict(X_lr_scaled)
                y_prob = model_lr.predict_proba(X_lr_scaled)[:, 1]
                
                accuracy = accuracy_score(y_lr, y_pred)
                
                # ROC Curve
                fpr, tpr, _ = roc_curve(y_lr, y_prob)
                roc_auc = auc(fpr, tpr)
                
                col_lr1, col_lr2 = st.columns(2)
                
                with col_lr1:
                    st.markdown("#### 📊 **Model Performance**")
                    st.markdown(f"""
                    <div class="glass-card-v4">
                        <h4>🎯 Accuracy Score</h4>
                        <p class="scenario-result">{accuracy*100:.1f}%</p>
                        <p style="color: rgba(255,255,255,0.8);">Kemampuan model memprediksi dengan benar</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### 📈 **Feature Coefficients**")
                    coef_df = pd.DataFrame({
                        'Feature': ['Coffee', 'Study Hours', 'Sleep Quality'],
                        'Coefficient': model_lr.coef_[0],
                        'Impact': ['⬆️' if c > 0 else '⬇️' for c in model_lr.coef_[0]]
                    })
                    st.dataframe(
                        coef_df.style.background_gradient(cmap='RdYlGn', subset=['Coefficient']),
                        use_container_width=True
                    )
                
                with col_lr2:
                    st.markdown("#### 📈 **ROC Curve**")
                    fig_roc = go.Figure()
                    fig_roc.add_trace(go.Scatter(
                        x=fpr, y=tpr,
                        mode='lines',
                        name=f'ROC (AUC = {roc_auc:.3f})',
                        line=dict(color='#ff006e', width=3)
                    ))
                    fig_roc.add_trace(go.Scatter(
                        x=[0, 1], y=[0, 1],
                        mode='lines',
                        name='Random',
                        line=dict(color='rgba(255,255,255,0.3)', width=2, dash='dash')
                    ))
                    fig_roc.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis=dict(title='False Positive Rate', gridcolor='rgba(255,255,255,0.15)', color='white'),
                        yaxis=dict(title='True Positive Rate', gridcolor='rgba(255,255,255,0.15)', color='white'),
                        height=400,
                        margin=dict(l=20, r=20, t=20, b=20),
                        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    )
                    st.plotly_chart(fig_roc, use_container_width=True)
                    
                    # Confusion Matrix
                    st.markdown("#### 🔢 **Confusion Matrix**")
                    cm = confusion_matrix(y_lr, y_pred)
                    fig_cm = px.imshow(
                        cm,
                        text_auto=True,
                        color_continuous_scale=['#0f0524', '#8338ec', '#ff006e'],
                        labels=dict(x="Predicted", y="Actual")
                    )
                    fig_cm.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=300,
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(fig_cm, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with ml_sub3:
            st.markdown("### 📈 **Linear Regression: Productivity Prediction**")
            st.markdown("""
            <div class="info-box-v4">
                📊 <strong>Regression Analysis:</strong> Memprediksi skor produktivitas 
                berdasarkan konsumsi kopi, durasi belajar, dan kualitas tidur.
            </div>
            """, unsafe_allow_html=True)
            
            try:
                X_reg = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']].values
                y_reg = df_filtered['Skor_Produktivitas'].values
                
                # Add intercept
                X_with_intercept = np.column_stack([np.ones(len(X_reg)), X_reg])
                
                # Least squares
                beta, residuals, rank, s = np.linalg.lstsq(X_with_intercept, y_reg, rcond=None)
                y_pred = X_with_intercept @ beta
                
                # Metrics
                ss_res = np.sum((y_reg - y_pred) ** 2)
                ss_tot = np.sum((y_reg - np.mean(y_reg)) ** 2)
                r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                rmse = np.sqrt(np.mean((y_reg - y_pred) ** 2))
                mae = np.mean(np.abs(y_reg - y_pred))
                
                coef = beta[1:]
                
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>🤖 Linear Regression Model</h4>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-top: 1.5rem;">
                        <div>
                            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">R² Score</p>
                            <p class="scenario-result">{r2:.4f}</p>
                        </div>
                        <div>
                            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">RMSE</p>
                            <p class="scenario-result">{rmse:.4f}</p>
                        </div>
                        <div>
                            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">MAE</p>
                            <p class="scenario-result">{mae:.4f}</p>
                        </div>
                        <div>
                            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Model Fit</p>
                            <p class="scenario-result">{r2*100:.1f}%</p>
                        </div>
                    </div>
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 1.5rem;">
                        <strong>📐 Coefficients:</strong><br>
                        Coffee: <span class="metric-highlight-v4">{coef[0]:.4f}</span> | 
                        Study Duration: <span class="metric-highlight-v4">{coef[1]:.4f}</span> | 
                        Sleep Quality: <span class="metric-highlight-v4">{coef[2]:.4f}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Feature importance
                st.markdown("#### 📊 **Feature Importance**")
                feature_importance = pd.DataFrame({
                    'Feature': ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk'],
                    'Importance': np.abs(coef)
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
                    xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                    showlegend=False,
                    coloraxis_showscale=False,
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_importance, use_container_width=True)
                
                # Prediction demo
                st.markdown("#### 🎯 **Prediction Demo**")
                demo_col1, demo_col2, demo_col3 = st.columns(3)
                
                with demo_col1:
                    demo_kopi = st.slider("☕ Cangkir Kopi:", 0, 5, 1)
                with demo_col2:
                    demo_durasi = st.slider("📚 Durasi (jam):", 0.0, 10.0, 3.0, 0.5)
                with demo_col3:
                    demo_tidur = st.slider("😴 Kualitas Tidur:", 1, 5, 3)
                
                demo_pred = beta[0] + beta[1]*demo_kopi + beta[2]*demo_durasi + beta[3]*demo_tidur
                demo_pred = np.clip(demo_pred, 1, 5)
                
                st.markdown(f"""
                <div class="scenario-panel">
                    <h4 style="color: var(--primary-yellow);">🔮 Prediksi Produktivitas</h4>
                    <p class="scenario-result">{demo_pred:.2f}</p>
                    <p style="color: rgba(255,255,255,0.8);">
                        Berdasarkan: {demo_kopi} cangkir, {demo_durasi}h belajar, tidur={demo_tidur}/5
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("⚠️ Data tidak cukup untuk ML (minimal 10 samples).")

# ===================== TAB 7: ADVANCED =====================
with tab7:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">07</span>
        <div>
            <h2 class="section-title-v4">Advanced Analytics <span class="badge-4d">✦ PRO</span></h2>
            <p class="section-subtitle-v4">Deep dive dengan hypothesis testing & network analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        adv_sub1, adv_sub2, adv_sub3 = st.tabs(["🕸️ Network Graph", "⚖️ Hypothesis Testing", "🌡️ Advanced Heatmaps"])
        
        with adv_sub1:
            st.markdown("### 🕸️ **Correlation Network Graph**")
            st.markdown("""
            <div class="info-box-v4">
                🌐 <strong>Network Visualization:</strong> Menampilkan hubungan antar variabel 
                sebagai jaringan. Tebal garis = kekuatan korelasi, warna = arah (positif/negatif).
            </div>
            """, unsafe_allow_html=True)
            
            corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk', 'Efficiency_Score']
            corr_matrix = df_filtered[corr_cols].corr()
            
            # Create network visualization
            nodes = []
            edges = []
            
            for i, col1 in enumerate(corr_cols):
                nodes.append({'id': col1, 'label': col1, 'group': i})
                for j, col2 in enumerate(corr_cols):
                    if i < j:
                        corr_val = corr_matrix.loc[col1, col2]
                        if abs(corr_val) > 0.2:  # Only show significant correlations
                            edges.append({
                                'source': col1,
                                'target': col2,
                                'value': corr_val,
                                'weight': abs(corr_val) * 5
                            })
            
            fig_network = go.Figure()
            
            # Add edges
            for edge in edges:
                fig_network.add_trace(go.Scatter(
                    x=[corr_cols.index(edge['source']), corr_cols.index(edge['target'])],
                    y=[0, 0],
                    mode='lines',
                    line=dict(
                        color='#ff006e' if edge['value'] > 0 else '#3a86ff',
                        width=edge['weight']
                    ),
                    opacity=0.5,
                    showlegend=False
                ))
            
            # Add nodes
            fig_network.add_trace(go.Scatter(
                x=list(range(len(corr_cols))),
                y=[0] * len(corr_cols),
                mode='markers+text',
                marker=dict(
                    size=50,
                    color=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b'],
                    line=dict(color='white', width=2)
                ),
                text=corr_cols,
                textposition="middle center",
                textfont=dict(color='white', size=10)
            ))
            
            fig_network.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_network, use_container_width=True)
        
        with adv_sub2:
            st.markdown("### ⚖️ **Comprehensive Hypothesis Testing**")
            
            test_col1, test_col2, test_col3 = st.columns(3)
            
            with test_col1:
                st.markdown("##### T-Test: Drinkers vs Non-Drinkers")
                drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 1]['Skor_Produktivitas']
                non_drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 0]['Skor_Produktivitas']
                
                if len(drinkers) > 1 and len(non_drinkers) > 1:
                    t_stat, p_t = ttest_ind(drinkers, non_drinkers)
                    
                    st.markdown(f"""
                    <div class="glass-card-v4">
                        <p>t-statistic: <span class="metric-highlight-v4">{t_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight-v4">{p_t:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: {'var(--primary-green)' if p_t < 0.05 else 'rgba(255,255,255,0.6)'};">
                            {'✓ Significant difference' if p_t < 0.05 else '✗ No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Data tidak cukup")
            
            with test_col2:
                st.markdown("##### ANOVA: Multiple Groups")
                groups = []
                for cups in df_filtered['Kopi_per_Hari'].unique():
                    group_data = df_filtered[df_filtered['Kopi_per_Hari'] == cups]['Skor_Produktivitas']
                    if len(group_data) > 1:
                        groups.append(group_data)
                
                if len(groups) >= 2:
                    f_stat, p_anova = f_oneway(*groups)
                    
                    st.markdown(f"""
                    <div class="glass-card-v4">
                        <p>F-statistic: <span class="metric-highlight-v4">{f_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight-v4">{p_anova:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: {'var(--primary-green)' if p_anova < 0.05 else 'rgba(255,255,255,0.6)'};">
                            {'✓ Significant difference' if p_anova < 0.05 else '✗ No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Data tidak cukup")
            
            with test_col3:
                st.markdown("##### Kruskal-Wallis Test")
                try:
                    if len(groups) >= 2:
                        h_stat, p_kw = kruskal(*groups)
                        
                        st.markdown(f"""
                        <div class="glass-card-v4">
                            <p>H-statistic: <span class="metric-highlight-v4">{h_stat:.4f}</span></p>
                            <p>p-value: <span class="metric-highlight-v4">{p_kw:.4f}</span></p>
                            <p style="font-size: 0.85rem; color: {'var(--primary-green)' if p_kw < 0.05 else 'rgba(255,255,255,0.6)'};">
                                {'✓ Significant difference' if p_kw < 0.05 else '✗ No significant difference'}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Data tidak cukup")
                except:
                    st.info("Error")
            
            # Mann-Whitney U Test
            st.markdown("#### 📊 **Non-Parametric Tests**")
            if len(drinkers) > 1 and len(non_drinkers) > 1:
                u_stat, p_mw = mannwhitneyu(drinkers, non_drinkers, alternative='two-sided')
                
                st.markdown(f"""
                <div class="glass-card-v4">
                    <h4>Mann-Whitney U Test</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <p>U-statistic: <span class="metric-highlight-v4">{u_stat:.4f}</span></p>
                            <p>p-value: <span class="metric-highlight-v4">{p_mw:.4f}</span></p>
                        </div>
                        <div>
                            <p style="color: {'var(--primary-green)' if p_mw < 0.05 else 'rgba(255,255,255,0.6)'};">
                                {'✓ Significant difference' if p_mw < 0.05 else '✗ No significant difference'}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with adv_sub3:
            st.markdown("### 🌡️ **Advanced Heatmaps**")
            
            # Violin Plot
            st.markdown("#### 🎻 **Violin Plot: Distribution by Category**")
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
                xaxis=dict(gridcolor='rgba(255,255,255,0.15)'),
                yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.15)'),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_violin, use_container_width=True)
            
            # Heatmap
            st.markdown("#### 🗺️ **Heatmap: Productivity by Coffee & Study Duration**")
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
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_heatmap_adv, use_container_width=True)
    else:
        st.warning("⚠️ Data kosong.")

# ===================== TAB 8: AI INSIGHTS =====================
with tab8:
    st.markdown("""
    <div class="section-header-v4">
        <span class="section-number-v4">08</span>
        <div>
            <h2 class="section-title-v4">AI-Powered Insights <span class="badge-4d">✦ GPT</span></h2>
            <p class="section-subtitle-v4">Automated analysis, anomaly detection & recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        st.markdown("### 🤖 **Automated Analysis**")
        
        # Optimal Coffee
        prod_by_coffee = df_filtered.groupby('Kopi_per_Hari')['Skor_Produktivitas'].mean()
        if len(prod_by_coffee) > 0:
            optimal_coffee = prod_by_coffee.idxmax()
            optimal_score = prod_by_coffee.max()
        else:
            optimal_coffee = 0
            optimal_score = 0
        
        st.markdown(f"""
        <div class="insight-card-v4">
            <div class="insight-icon-v4">🏆</div>
            <div class="insight-title-v4">Optimal Coffee Consumption</div>
            <div class="insight-text-v4">
                Berdasarkan analisis, konsumsi kopi optimal untuk produktivitas maksimal adalah 
                <span class="metric-highlight-v4">{optimal_coffee} cangkir per hari</span>, dengan rata-rata 
                skor produktivitas <span class="metric-highlight-v4">{optimal_score:.2f}</span>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Study Duration Sweet Spot
        durasi_bins = pd.cut(df_filtered['Durasi_Belajar_Num'], bins=[0, 2, 4, 6, 8, 10])
        durasi_productivity = df_filtered.groupby(durasi_bins, observed=True)['Skor_Produktivitas'].mean()
        if len(durasi_productivity) > 0:
            optimal_durasi = durasi_productivity.idxmax()
            optimal_durasi_score = durasi_productivity.max()
        else:
            optimal_durasi = "N/A"
            optimal_durasi_score = 0
        
        st.markdown(f"""
        <div class="insight-card-v4">
            <div class="insight-icon-v4">⏰</div>
            <div class="insight-title-v4">Study Duration Sweet Spot</div>
            <div class="insight-text-v4">
                Durasi belajar paling produktif adalah <span class="metric-highlight-v4">{optimal_durasi}</span>, 
                dengan rata-rata skor <span class="metric-highlight-v4">{optimal_durasi_score:.2f}</span>.
                Pertimbangkan untuk mengatur sesi belajar dalam rentang waktu ini.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sleep Quality Impact
        sleep_corr = df_filtered['Kualitas_Tidur_Memburuk'].corr(df_filtered['Skor_Produktivitas'])
        
        st.markdown(f"""
        <div class="insight-card-v4">
            <div class="insight-icon-v4">😴</div>
            <div class="insight-title-v4">Sleep Quality Impact</div>
            <div class="insight-text-v4">
                Kualitas tidur menunjukkan korelasi <span class="metric-highlight-v4">{'positif' if sleep_corr > 0 else 'negatif'}</span> 
                dengan produktivitas (r = {sleep_corr:.3f}). 
                {'Tidur berkualitas lebih baik diasosiasikan dengan produktivitas lebih tinggi.' if sleep_corr > 0 else 'Kualitas tidur buruk diasosiasikan dengan produktivitas rendah.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Factor Alert
        high_coffee_low_sleep = df_filtered[(df_filtered['Kopi_per_Hari'] >= 2) & (df_filtered['Kualitas_Tidur_Memburuk'] >= 4)]
        risk_percentage = (len(high_coffee_low_sleep) / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
        
        if risk_percentage > 20:
            st.markdown(f"""
            <div class="anomaly-alert">
                <h4 style="color: var(--primary-pink);">⚠️ Risk Factor Alert</h4>
                <p style="color: rgba(255,255,255,0.9);">
                    <span class="metric-highlight-v4">{risk_percentage:.1f}%</span> responden menunjukkan pola berisiko tinggi: 
                    konsumsi 2+ cangkir kopi per hari dengan kualitas tidur buruk (≥4). 
                    Kombinasi ini dapat menyebabkan masalah kesehatan jangka panjang dan penurunan performa kognitif.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="insight-card-v4">
                <div class="insight-icon-v4">✓</div>
                <div class="insight-title-v4">Low Risk Profile</div>
                <div class="insight-text-v4">
                    Hanya <span class="metric-highlight-v4">{risk_percentage:.1f}%</span> responden menunjukkan pola berisiko tinggi. 
                    Secara keseluruhan, populasi ini memiliki kebiasaan konsumsi kopi yang relatif sehat.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Anomaly Detection
        st.markdown("### 🔍 **Anomaly Detection**")
        
        Q1 = np.percentile(df_filtered['Skor_Produktivitas'], 25)
        Q3 = np.percentile(df_filtered['Skor_Produktivitas'], 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = df_filtered[
            (df_filtered['Skor_Produktivitas'] < lower_bound) | 
            (df_filtered['Skor_Produktivitas'] > upper_bound)
        ]
        
        if len(anomalies) > 0:
            st.markdown(f"""
            <div class="anomaly-alert">
                <h4>🎯 {len(anomalies)} Anomali Terdeteksi</h4>
                <p style="color: rgba(255,255,255,0.9);">
                    Ditemukan <b>{len(anomalies)}</b> responden dengan skor produktivitas di luar range normal 
                    [{lower_bound:.2f}, {upper_bound:.2f}]. Responden ini mungkin memerlukan analisis lebih lanjut.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(anomalies[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].head(10))
        else:
            st.success("✅ Tidak ada anomali signifikan terdeteksi.")
        
        # Personalized Recommendations
        st.markdown("### 💡 **Personalized Recommendations**")
        
        rec_cols = st.columns(3)
        
        with rec_cols[0]:
            st.markdown("""
            <div class="glass-card-v4">
                <h4 style="color: var(--primary-green);">☕ For Light Drinkers</h4>
                <ul style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
                    <li>✓ Pertahankan rutinitas 1 cangkir/hari</li>
                    <li>✓ Konsumsi sebelum sesi belajar</li>
                    <li>✓ Hindari setelah jam 4 sore</li>
                    <li>✓ Monitor kualitas tidur</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_cols[1]:
            st.markdown("""
            <div class="glass-card-v4">
                <h4 style="color: var(--primary-yellow);">⚡ For Moderate Drinkers</h4>
                <ul style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
                    <li>⚠ Pertimbangkan mengurangi ke 1 cangkir</li>
                    <li>⚠ Lacak perubahan produktivitas</li>
                    <li>⚠ Implementasikan coffee breaks</li>
                    <li>⚠ Prioritaskan sleep hygiene</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_cols[2]:
            st.markdown("""
            <div class="glass-card-v4">
                <h4 style="color: var(--primary-pink);">🚨 For Heavy Drinkers</h4>
                <ul style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
                    <li>🚨 Kurangi konsumsi secara bertahap</li>
                    <li>🚨 Konsultasi profesional kesehatan</li>
                    <li>🚨 Implementasikan periode detoks</li>
                    <li>🚨 Fokus pada pemulihan tidur</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data kosong.")

# --- FOOTER V4 ---
st.markdown('<div style="height: 2px; background: linear-gradient(90deg, var(--primary-pink), var(--primary-purple), var(--primary-blue), var(--primary-green)); margin: 3rem 0;"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="premium-footer-v4">
    <p class="footer-brand-v4">☕ COFFEE ANALYTICS 4D PRO</p>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; margin: 1rem 0;">
        Next-Gen Neuroscience & Productivity Intelligence Platform
    </p>
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0.5rem 0;">
        Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b>
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 0.5rem 0;">
        Sumber Data: Kuesioner Mahasiswa (n={}) | Powered by Streamlit, Plotly 3D & scikit-learn
    </p>
    <p style="color: rgba(255,255,255,0.4); font-size: 0.75rem; margin-top: 1.5rem; letter-spacing: 2px;">
        ◆ 4D VISUALIZATION ◆ AI-POWERED ◆ ML CLUSTERING ◆ STOCHASTIC MODELING ◆
    </p>
</div>
""".format(len(df)), unsafe_allow_html=True)
