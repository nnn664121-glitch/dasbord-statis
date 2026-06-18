import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import (pearsonr, spearmanr, chi2_contingency, ttest_ind, 
                         f_oneway, mannwhitneyu, kruskal, shapiro, normaltest,
                         ks_2samp, anderson, bartlett, levene)
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Coffee Analytics 3D Pro ☕ - Advanced Intelligence Platform",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM 3D EDITION V4 + ENHANCED ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: radial-gradient(ellipse at top, #1a0b2e 0%, #0f0524 40%, #050212 100%);
        font-family: 'Space Grotesk', sans-serif;
        overflow-x: hidden;
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
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
    }
    
    /* ============================================ */
    /* ANIMATED FLOATING ORBS BACKGROUND             */
    /* ============================================ */
    .floating-orbs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(40px);
        opacity: 0.3;
        animation: float-orb 20s infinite ease-in-out;
    }
    
    .orb1 {
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, #ff006e, transparent);
        top: 10%;
        left: 5%;
        animation-delay: 0s;
    }
    
    .orb2 {
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, #8338ec, transparent);
        top: 60%;
        right: 10%;
        animation-delay: -5s;
    }
    
    .orb3 {
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, #3a86ff, transparent);
        bottom: 10%;
        left: 40%;
        animation-delay: -10s;
    }
    
    .orb4 {
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, #06ffa5, transparent);
        top: 30%;
        right: 30%;
        animation-delay: -15s;
    }
    
    .orb5 {
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, #ffbe0b, transparent);
        top: 75%;
        left: 15%;
        animation-delay: -7s;
    }
    
    .orb6 {
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, #fb5607, transparent);
        top: 5%;
        right: 5%;
        animation-delay: -12s;
    }
    
    @keyframes float-orb {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(100px, -50px) scale(1.1); }
        50% { transform: translate(-50px, 100px) scale(0.9); }
        75% { transform: translate(-100px, -100px) scale(1.05); }
    }
    
    /* ============================================ */
    /* ANIMATED GRID BACKGROUND                    */
    /* ============================================ */
    .animated-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: 
            linear-gradient(rgba(131, 56, 236, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(131, 56, 236, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: grid-move 20s linear infinite;
    }
    
    @keyframes grid-move {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    
    /* ============================================ */
    /* HERO SECTION ENHANCED                       */
    /* ============================================ */
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
        animation: hero-entrance 1s ease-out;
    }
    
    @keyframes hero-entrance {
        0% {
            opacity: 0;
            transform: translateY(50px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
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
    
    /* Animated particles inside hero */
    .hero-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(255, 0, 110, 0.4) 0%, transparent 1%),
            radial-gradient(circle at 80% 70%, rgba(131, 56, 236, 0.4) 0%, transparent 1%),
            radial-gradient(circle at 50% 50%, rgba(58, 134, 255, 0.4) 0%, transparent 1%),
            radial-gradient(circle at 30% 80%, rgba(6, 255, 165, 0.4) 0%, transparent 1%),
            radial-gradient(circle at 70% 20%, rgba(255, 190, 11, 0.4) 0%, transparent 1%),
            radial-gradient(circle at 10% 90%, rgba(251, 86, 7, 0.3) 0%, transparent 1%),
            radial-gradient(circle at 90% 10%, rgba(131, 56, 236, 0.3) 0%, transparent 1%);
        background-size: 100% 100%;
        animation: particles-float 15s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes particles-float {
        0%, 100% { transform: translate(0, 0); opacity: 0.6; }
        50% { transform: translate(20px, -20px); opacity: 1; }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-emoji {
        font-size: 5rem;
        display: inline-block;
        margin-bottom: 1rem;
        animation: float-emoji 3s ease-in-out infinite, spin-slow 8s linear infinite;
    }
    
    @keyframes float-emoji {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(15deg); }
    }
    
    @keyframes spin-slow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
        animation: gradient-flow 5s ease infinite, title-glow 3s ease-in-out infinite;
    }
    
    @keyframes gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes title-glow {
        0%, 100% { text-shadow: 0 0 20px rgba(131, 56, 236, 0.5); }
        50% { text-shadow: 0 0 40px rgba(255, 0, 110, 0.8); }
    }
    
    /* TYPING ANIMATION FOR SUBTITLE */
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 1px;
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #06ffa5;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
        max-width: 100%;
        display: inline-block;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #06ffa5 }
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
        animation: badge-pulse 2s ease-in-out infinite, badge-float 3s ease-in-out infinite;
    }
    
    @keyframes badge-pulse {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(6, 255, 165, 0.3);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 40px rgba(6, 255, 165, 0.8);
            transform: scale(1.05);
        }
    }
    
    @keyframes badge-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    
    
    /* ============================================ */
    /* KPI CARDS - ENHANCED WITH SHIMMER            */
    /* ============================================ */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
        animation: card-entrance 0.8s ease-out backwards;
    }
    
    .kpi-card:nth-child(1) { animation-delay: 0.1s; }
    .kpi-card:nth-child(2) { animation-delay: 0.2s; }
    .kpi-card:nth-child(3) { animation-delay: 0.3s; }
    .kpi-card:nth-child(4) { animation-delay: 0.4s; }
    .kpi-card:nth-child(5) { animation-delay: 0.5s; }
    .kpi-card:nth-child(6) { animation-delay: 0.6s; }
    .kpi-card:nth-child(7) { animation-delay: 0.7s; }
    .kpi-card:nth-child(8) { animation-delay: 0.8s; }
    
    @keyframes card-entrance {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
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
    
    /* Shimmer effect */
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02) rotateX(5deg);
        box-shadow: 0 20px 60px rgba(131, 56, 236, 0.3);
        border-color: rgba(131, 56, 236, 0.5);
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
        display: inline-block;
        animation: icon-bounce 2s ease-in-out infinite;
    }
    
    @keyframes icon-bounce {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-5px) rotate(-5deg); }
        75% { transform: translateY(-5px) rotate(5deg); }
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
        animation: value-glow 2s ease-in-out infinite;
    }
    
    @keyframes value-glow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 5px rgba(131, 56, 236, 0.3)); }
        50% { filter: brightness(1.2) drop-shadow(0 0 15px rgba(131, 56, 236, 0.8)); }
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
        animation: delta-slide 3s ease-in-out infinite;
    }
    
    .kpi-delta.negative {
        background: rgba(255, 0, 110, 0.1);
        border-color: rgba(255, 0, 110, 0.3);
        color: #ff006e;
    }
    
    @keyframes delta-slide {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(5px); }
    }
    
    /* ============================================ */
    /* SECTION HEADERS ENHANCED                     */
    /* ============================================ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        animation: header-slide 0.8s ease-out;
    }
    
    @keyframes header-slide {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
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
        animation: number-pulse 2s ease-in-out infinite;
    }
    
    @keyframes number-pulse {
        0%, 100% { 
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255, 0, 110, 0.5));
        }
        50% { 
            transform: scale(1.1);
            filter: drop-shadow(0 0 20px rgba(131, 56, 236, 0.8));
        }
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
    
    /* ============================================ */
    /* GLASS CARDS ENHANCED                        */
    /* ============================================ */
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
        animation: glass-appear 0.6s ease-out;
    }
    
    @keyframes glass-appear {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .glass-card:hover {
        transform: translateY(-3px) scale(1.01);
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
    
    /* ============================================ */
    /* 3D BADGE ENHANCED                            */
    /* ============================================ */
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
        animation: badge-glow 2s ease-in-out infinite;
    }
    
    .badge-3d.green {
        background: linear-gradient(135deg, #06ffa5, #3a86ff);
        box-shadow: 0 5px 20px rgba(6, 255, 165, 0.4);
    }
    
    .badge-3d.orange {
        background: linear-gradient(135deg, #ffbe0b, #fb5607);
        box-shadow: 0 5px 20px rgba(255, 190, 11, 0.4);
    }
    
    @keyframes badge-glow {
        0%, 100% { 
            box-shadow: 0 5px 20px rgba(255, 0, 110, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 5px 30px rgba(255, 0, 110, 0.8);
            transform: scale(1.05);
        }
    }
    
    /* ============================================ */
    /* SIDEBAR ENHANCED                             */
    /* ============================================ */
    .stSidebar {
        background: rgba(15, 5, 36, 0.95);
        backdrop-filter: blur(20px);
    }
    
    .stSidebar .sidebar-content {
        background: transparent;
    }
    
    /* ============================================ */
    /* TABS ENHANCED                                */
    /* ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
        font-family: 'Space Grotesk', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(131, 56, 236, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(131, 56, 236, 0.1);
        color: #fff;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff006e, #8338ec);
        color: #fff;
        box-shadow: 0 5px 20px rgba(131, 56, 236, 0.4);
        animation: tab-active 0.3s ease;
    }
    
    @keyframes tab-active {
        from { transform: scale(0.95); }
        to { transform: scale(1); }
    }
    
    /* ============================================ */
    /* BUTTONS ENHANCED                             */
    /* ============================================ */
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
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 0, 110, 0.4);
    }
    
    /* ============================================ */
    /* DIVIDER ENHANCED                             */
    /* ============================================ */
    .fancy-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(131, 56, 236, 0.5), transparent);
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .fancy-divider::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, #ff006e, transparent);
        animation: divider-shine 3s linear infinite;
    }
    
    @keyframes divider-shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* ============================================ */
    /* INSIGHT CARDS ENHANCED                       */
    /* ============================================ */
    .insight-card {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.08) 0%, rgba(131, 56, 236, 0.08) 100%);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        animation: insight-float 4s ease-in-out infinite;
    }
    
    @keyframes insight-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .insight-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(131, 56, 236, 0.3);
        border-color: rgba(255, 0, 110, 0.5);
    }
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .insight-card:hover::before {
        left: 100%;
    }
    
    .insight-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        animation: icon-dance 2s ease-in-out infinite;
    }
    
    @keyframes icon-dance {
        0%, 100% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(-10deg) scale(1.1); }
        75% { transform: rotate(10deg) scale(1.1); }
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
    
    /* ============================================ */
    /* INFO BOX ENHANCED                            */
    /* ============================================ */
    .info-box {
        background: linear-gradient(135deg, rgba(58, 134, 255, 0.15) 0%, rgba(6, 255, 165, 0.1) 100%);
        border-left: 4px solid #3a86ff;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.9);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        animation: info-slide 0.6s ease-out;
    }
    
    .info-box.warning {
        background: linear-gradient(135deg, rgba(255, 190, 11, 0.15) 0%, rgba(251, 86, 7, 0.1) 100%);
        border-left-color: #ffbe0b;
    }
    
    .info-box.success {
        background: linear-gradient(135deg, rgba(6, 255, 165, 0.15) 0%, rgba(58, 134, 255, 0.1) 100%);
        border-left-color: #06ffa5;
    }
    
    @keyframes info-slide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ============================================ */
    /* METRIC HIGHLIGHT ENHANCED                    */
    /* ============================================ */
    .metric-highlight {
        font-family: 'JetBrains Mono', monospace;
        color: #06ffa5;
        font-weight: 600;
        position: relative;
        display: inline-block;
    }
    
    .metric-highlight::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #06ffa5, #3a86ff);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    
    .metric-highlight:hover::after {
        transform: scaleX(1);
    }
    
    /* ============================================ */
    /* FOOTER ENHANCED                              */
    /* ============================================ */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .premium-footer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(131, 56, 236, 0.1), transparent);
        animation: rotate 30s linear infinite;
    }
    
    .footer-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        margin: 0.3rem 0;
        position: relative;
        z-index: 1;
    }
    
    .footer-brand {
        background: linear-gradient(135deg, #ff006e, #8338ec, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1rem;
        position: relative;
        z-index: 1;
        animation: gradient-flow 5s ease infinite;
        background-size: 200% 200%;
    }
    
    /* ============================================ */
    /* ANIMATED NUMBER EFFECT                       */
    /* ============================================ */
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
    
    /* ============================================ */
    /* PROGRESS BAR ENHANCED                        */
    /* ============================================ */
    .progress-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 200% 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        animation: progress-shine 2s linear infinite;
    }
    
    @keyframes progress-shine {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* ============================================ */
    /* MARQUEE SCROLLING TEXT                       */
    /* ============================================ */
    .marquee-container {
        overflow: hidden;
        white-space: nowrap;
        background: linear-gradient(90deg, rgba(255, 0, 110, 0.05), rgba(131, 56, 236, 0.05), rgba(58, 134, 255, 0.05));
        padding: 0.8rem 0;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .marquee-content {
        display: inline-block;
        animation: marquee-scroll 30s linear infinite;
        color: rgba(255, 255, 255, 0.7);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }
    
    @keyframes marquee-scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* ============================================ */
    /* WAVE ANIMATION                               */
    /* ============================================ */
    .wave-container {
        position: relative;
        height: 50px;
        overflow: hidden;
        margin: 2rem 0;
    }
    
    .wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(131, 56, 236, 0.2) 25%, 
            rgba(255, 0, 110, 0.2) 50%, 
            rgba(131, 56, 236, 0.2) 75%, 
            transparent 100%
        );
        animation: wave-move 4s ease-in-out infinite;
    }
    
    @keyframes wave-move {
        0%, 100% { transform: translateX(-50%); }
        50% { transform: translateX(0%); }
    }
    
    /* ============================================ */
    /* NEON TEXT EFFECT                             */
    /* ============================================ */
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #ff006e,
            0 0 40px #ff006e,
            0 0 80px #ff006e;
        animation: neon-flicker 3s infinite alternate;
    }
    
    @keyframes neon-flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            text-shadow: 
                0 0 5px #fff,
                0 0 10px #fff,
                0 0 20px #ff006e,
                0 0 40px #ff006e,
                0 0 80px #ff006e;
        }
        20%, 24%, 55% {
            text-shadow: none;
        }
    }
    
    /* ============================================ */
    /* RIPPLE EFFECT                                */
    /* ============================================ */
    .ripple {
        position: relative;
        overflow: hidden;
    }
    
    .ripple::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(131, 56, 236, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .ripple:active::after {
        width: 300px;
        height: 300px;
    }
    
    /* ============================================ */
    /* FLOATING COFFEE BEANS                        */
    /* ============================================ */
    .coffee-bean {
        position: fixed;
        font-size: 2rem;
        opacity: 0.3;
        pointer-events: none;
        z-index: 1;
        animation: bean-float 15s linear infinite;
    }
    
    .bean-1 { top: 20%; left: 10%; animation-delay: 0s; }
    .bean-2 { top: 40%; right: 15%; animation-delay: -3s; }
    .bean-3 { top: 60%; left: 25%; animation-delay: -6s; }
    .bean-4 { top: 80%; right: 30%; animation-delay: -9s; }
    .bean-5 { top: 15%; left: 60%; animation-delay: -12s; }
    
    @keyframes bean-float {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.3;
        }
        50% {
            opacity: 0.6;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* ============================================ */
    /* DATAFRAME ANIMATIONS                         */
    /* ============================================ */
    .stDataFrame {
        animation: dataframe-appear 0.5s ease-out;
    }
    
    @keyframes dataframe-appear {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ============================================ */
    /* SPINNER ENHANCED                             */
    /* ============================================ */
    .stSpinner > div {
        border-top-color: #ff006e !important;
        animation: spin 1s linear infinite !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* ============================================ */
    /* METRIC CARDS ANIMATION                       */
    /* ============================================ */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(131, 56, 236, 0.4);
        box-shadow: 0 10px 30px rgba(131, 56, 236, 0.2);
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        animation: shimmer 4s infinite;
    }
    
    /* ============================================ */
    /* SCROLL INDICATOR                             */
    /* ============================================ */
    .scroll-indicator {
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        z-index: 9999;
        transition: width 0.1s ease;
    }
    
    /* ============================================ */
    /* GRADIENT BORDER ANIMATION                    */
    /* ============================================ */
    .gradient-border {
        position: relative;
        background: rgba(15, 5, 36, 0.8);
        border-radius: 20px;
        padding: 2px;
    }
    
    .gradient-border::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 200% 200%;
        animation: gradient-border-flow 3s ease infinite;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }
    
    @keyframes gradient-border-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* ============================================ */
    /* TOOLTIP ENHANCED                             */
    /* ============================================ */
    .tooltip-custom {
        position: relative;
        display: inline-block;
        cursor: help;
        border-bottom: 1px dotted rgba(255, 255, 255, 0.5);
    }
    
    .tooltip-custom:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 5, 36, 0.95);
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        white-space: nowrap;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(131, 56, 236, 0.5);
        z-index: 1000;
        animation: tooltip-fade 0.3s ease;
    }
    
    @keyframes tooltip-fade {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    /* ============================================ */
    /* COMPARISON TABLE                             */
    /* ============================================ */
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .comparison-table th {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(131, 56, 236, 0.2));
        color: #fff;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid rgba(131, 56, 236, 0.3);
    }
    
    .comparison-table td {
        padding: 0.8rem 1rem;
        color: rgba(255, 255, 255, 0.8);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .comparison-table tr:hover td {
        background: rgba(131, 56, 236, 0.1);
        transform: scale(1.01);
    }
    
    .comparison-table tr:last-child td {
        border-bottom: none;
    }
    
    /* ============================================ */
    /* STATISTICAL BADGE                            */
    /* ============================================ */
    .stat-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        background: rgba(6, 255, 165, 0.1);
        border: 1px solid rgba(6, 255, 165, 0.3);
        border-radius: 20px;
        color: #06ffa5;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    
    .stat-badge:hover {
        background: rgba(6, 255, 165, 0.2);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(6, 255, 165, 0.3);
    }
    
    .stat-badge.warning {
        background: rgba(255, 190, 11, 0.1);
        border-color: rgba(255, 190, 11, 0.3);
        color: #ffbe0b;
    }
    
    .stat-badge.danger {
        background: rgba(255, 0, 110, 0.1);
        border-color: rgba(255, 0, 110, 0.3);
        color: #ff006e;
    }
    
    /* ============================================ */
    /* CODE BLOCK ENHANCED                          */
    /* ============================================ */
    .code-block {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 12px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #06ffa5;
        overflow-x: auto;
        margin: 1rem 0;
        position: relative;
    }
    
    .code-block::before {
        content: 'Python';
        position: absolute;
        top: 0;
        right: 0;
        background: linear-gradient(135deg, #ff006e, #8338ec);
        color: #fff;
        padding: 0.3rem 0.8rem;
        border-radius: 0 12px 0 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    /* ============================================ */
    /* ACCORDION ENHANCED                           */
    /* ============================================ */
    .accordion-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        margin-bottom: 0.5rem;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .accordion-item:hover {
        border-color: rgba(131, 56, 236, 0.4);
        transform: translateX(5px);
    }
    
    .accordion-header {
        padding: 1rem;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #fff;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .accordion-header:hover {
        background: rgba(131, 56, 236, 0.1);
    }
    
    .accordion-content {
        padding: 0 1rem 1rem 1rem;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.6;
    }
    
    /* ============================================ */
    /* TIMELINE ENHANCED                            */
    /* ============================================ */
    .timeline {
        position: relative;
        padding: 1rem 0;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 20px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
    }
    
    .timeline-item {
        position: relative;
        padding-left: 50px;
        margin-bottom: 2rem;
        animation: timeline-slide 0.6s ease-out backwards;
    }
    
    .timeline-item:nth-child(1) { animation-delay: 0.1s; }
    .timeline-item:nth-child(2) { animation-delay: 0.2s; }
    .timeline-item:nth-child(3) { animation-delay: 0.3s; }
    .timeline-item:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes timeline-slide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: 14px;
        top: 5px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff006e, #8338ec);
        border: 3px solid #0f0524;
        animation: timeline-pulse 2s ease-in-out infinite;
    }
    
    @keyframes timeline-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .timeline-title {
        color: #fff;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .timeline-content {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* ============================================ */
    /* FORMULA DISPLAY                              */
    /* ============================================ */
    .formula-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.2rem;
        color: #fff;
        position: relative;
        overflow: hidden;
    }
    
    .formula-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(6, 255, 165, 0.1), transparent);
        animation: formula-shine 3s linear infinite;
    }
    
    @keyframes formula-shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .formula-box .formula {
        color: #06ffa5;
        font-weight: 600;
    }
    
    /* ============================================ */
    /* LOADING SKELETON                             */
    /* ============================================ */
    .skeleton {
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0.03) 25%, 
            rgba(255, 255, 255, 0.08) 50%, 
            rgba(255, 255, 255, 0.03) 75%
        );
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
        border-radius: 8px;
        height: 20px;
        margin: 0.5rem 0;
    }
    
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)


/* ============================================ */
/* HERO STATS - ENHANCED PREMIUM VERSION       */
/* ============================================ */
.hero-stats {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 1.5rem;
    margin-top: 3rem;
    flex-wrap: wrap;
    position: relative;
    z-index: 3;
    padding: 0 1rem;
}

.hero-stat-item {
    flex: 1;
    min-width: 180px;
    max-width: 220px;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.08) 0%, 
        rgba(131, 56, 236, 0.05) 50%,
        rgba(255, 0, 110, 0.03) 100%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 1.5rem 1rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: stat-pop 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.hero-stat-item:nth-child(1) { animation-delay: 0.8s; }
.hero-stat-item:nth-child(2) { animation-delay: 0.95s; }
.hero-stat-item:nth-child(3) { animation-delay: 1.1s; }
.hero-stat-item:nth-child(4) { animation-delay: 1.25s; }

/* Top gradient accent */
.hero-stat-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
    background-size: 300% 100%;
    animation: gradient-shift 4s linear infinite;
    border-radius: 20px 20px 0 0;
}

/* Shimmer effect */
.hero-stat-item::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.08),
        transparent
    );
    transition: left 0.8s ease;
    pointer-events: none;
}

.hero-stat-item:hover {
    transform: translateY(-8px) scale(1.05);
    border-color: rgba(131, 56, 236, 0.6);
    box-shadow: 
        0 20px 40px rgba(131, 56, 236, 0.4),
        0 0 60px rgba(255, 0, 110, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.hero-stat-item:hover::after {
    left: 100%;
}

/* Icon above value */
.hero-stat-icon {
    font-size: 1.8rem;
    display: inline-block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 10px rgba(131, 56, 236, 0.5));
    animation: icon-float 3s ease-in-out infinite;
}

.hero-stat-item:nth-child(1) .hero-stat-icon { animation-delay: 0s; }
.hero-stat-item:nth-child(2) .hero-stat-icon { animation-delay: 0.3s; }
.hero-stat-item:nth-child(3) .hero-stat-icon { animation-delay: 0.6s; }
.hero-stat-item:nth-child(4) .hero-stat-icon { animation-delay: 0.9s; }

@keyframes icon-float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-5px) rotate(5deg); }
}

/* Value with gradient */
.hero-stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 30%, #8338ec 60%, #3a86ff 85%, #06ffa5 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.3rem 0 0.2rem 0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -1px;
    line-height: 1;
    animation: value-gradient-flow 4s ease infinite, value-glow-pulse 2.5s ease-in-out infinite;
    position: relative;
    z-index: 2;
}

@keyframes value-gradient-flow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

@keyframes value-glow-pulse {
    0%, 100% { 
        filter: drop-shadow(0 0 8px rgba(131, 56, 236, 0.4));
    }
    50% { 
        filter: drop-shadow(0 0 20px rgba(255, 0, 110, 0.7));
    }
}

/* Label */
.hero-stat-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0.5rem 0 0 0;
    font-weight: 500;
    position: relative;
    z-index: 2;
}

/* Subtle counter effect */
.hero-stat-item:hover .hero-stat-value {
    transform: scale(1.1);
    transition: transform 0.3s ease;
}

.hero-stat-item:hover .hero-stat-label {
    color: #06ffa5;
    transition: color 0.3s ease;
}

/* Badge indicator on hover */
.hero-stat-item:hover::before {
    animation: gradient-shift 1s linear infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .hero-stats {
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .hero-stat-item {
        min-width: 140px;
        padding: 1rem 0.8rem;
    }
    
    .hero-stat-value {
        font-size: 2rem;
    }
    
    .hero-stat-icon {
        font-size: 1.5rem;
    }
}

@media (max-width: 480px) {
    .hero-stats {
        flex-direction: column;
        align-items: center;
    }
    
    .hero-stat-item {
        width: 100%;
        max-width: 280px;
    }
}

/* Pop animation with bounce */
@keyframes stat-pop {
    0% {
        opacity: 0;
        transform: scale(0.3) translateY(40px) rotate(-5deg);
    }
    50% {
        opacity: 0.8;
        transform: scale(1.1) translateY(-10px) rotate(2deg);
    }
    70% {
        transform: scale(0.95) translateY(5px) rotate(-1deg);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0) rotate(0deg);
    }
}
# --- ANIMATED BACKGROUND ELEMENTS ---
st.markdown("""
<div class="animated-grid"></div>
<div class="floating-orbs">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
    <div class="orb orb4"></div>
    <div class="orb orb5"></div>
    <div class="orb orb6"></div>
</div>
<div class="coffee-bean bean-1">☕</div>
<div class="coffee-bean bean-2">🫘</div>
<div class="coffee-bean bean-3">☕</div>
<div class="coffee-bean bean-4">🫘</div>
<div class="coffee-bean bean-5">☕</div>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD & PREPROCESS DATA ---
@st.cache_data
def load_data():
    """
    Load dan preprocess data dari file CSV.
    Mengembalikan DataFrame yang sudah dibersihkan dan di-enrich.
    """
    try:
        df = pd.read_csv('data.csv', sep=';')
    except FileNotFoundError:
        # Generate synthetic data jika file tidak ditemukan
        np.random.seed(42)
        n_samples = 100
        
        data = {
            'Timestamp': pd.date_range('2024-01-01', periods=n_samples, freq='D'),
            'Nama': [f'Respondent_{i}' for i in range(1, n_samples + 1)],
            'Umur': np.random.randint(18, 25, n_samples),
            'Jenis_Kelamin': np.random.choice(['Laki-laki', 'Perempuan'], n_samples),
            'Kopi_per_Hari': np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.1, 0.3, 0.3, 0.2, 0.1]),
            'Jenis_Kopi': np.random.choice(['Arabica', 'Robusta', 'Blend', 'Lainnya'], n_samples),
            'Waktu_Minum': np.random.choice(['Pagi', 'Siang', 'Sore', 'Malam'], n_samples),
            'Durasi_Belajar': np.random.choice(['< 2 jam', '2-4 jam', '5-7 jam', '> 7 jam'], n_samples, p=[0.2, 0.4, 0.3, 0.1]),
            'Fokus_1': np.random.randint(1, 6, n_samples),
            'Fokus_2': np.random.randint(1, 6, n_samples),
            'Fokus_3': np.random.randint(1, 6, n_samples),
            'Fokus_4': np.random.randint(1, 6, n_samples),
            'Kualitas_Tidur': np.random.randint(1, 6, n_samples),
            'Stress_Level': np.random.randint(1, 6, n_samples),
            'Mood': np.random.randint(1, 6, n_samples),
            'Energi': np.random.randint(1, 6, n_samples)
        }
        df = pd.DataFrame(data)
    
    df_clean = df.copy()

    # Ekstrak angka dari kolom Kopi_per_Hari
    if 'Kopi_per_Hari' in df_clean.columns:
        df_clean['Kopi_per_Hari'] = df_clean['Kopi_per_Hari'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)
    else:
        # Gunakan kolom ke-4 jika nama kolom berbeda
        col_idx = min(4, len(df_clean.columns) - 1)
        df_clean['Kopi_per_Hari'] = df_clean.iloc[:, col_idx].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

    # Mapping durasi belajar ke numerik
    hours_mapping = {
        '< 2 jam': 1.0,
        '2-4 jam': 3.0,
        '5-7 jam': 6.0,
        '> 7 jam': 8.5
    }
    
    durasi_col = None
    for col in df_clean.columns:
        if 'durasi' in col.lower() or 'belajar' in col.lower():
            durasi_col = col
            break
    
    if durasi_col is None:
        col_idx = min(7, len(df_clean.columns) - 1)
        durasi_col = df_clean.columns[col_idx]
    
    df_clean['Durasi_Belajar_Num'] = df_clean[durasi_col].map(hours_mapping).fillna(df_clean[durasi_col].mode()[0] if len(df_clean[durasi_col].mode()) > 0 else 3.0)

    # Hitung skor produktivitas dari kolom Likert
    likert_cols = []
    for i, col in enumerate(df_clean.columns):
        if 'fokus' in col.lower() or 'produktivitas' in col.lower():
            likert_cols.append(col)
    
    if len(likert_cols) >= 4:
        df_clean['Skor_Produktivitas'] = df_clean[likert_cols[:4]].mean(axis=1)
    else:
        # Generate skor sintetik
        df_clean['Skor_Produktivitas'] = np.random.uniform(2.0, 4.5, len(df_clean))

    # Kualitas tidur
    tidur_col = None
    for col in df_clean.columns:
        if 'tidur' in col.lower() or 'sleep' in col.lower():
            tidur_col = col
            break
    
    if tidur_col:
        df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean[tidur_col], errors='coerce').fillna(3)
    else:
        col_idx = min(15, len(df_clean.columns) - 1)
        df_clean['Kualitas_Tidur_Memburuk'] = pd.to_numeric(df_clean.iloc[:, col_idx], errors='coerce').fillna(3)

    # Buat kolom derived
    df_clean['Is_Fokus_Tinggi'] = (df_clean['Skor_Produktivitas'] > 3.0).astype(int)
    df_clean['Is_Peminum_Kopi'] = (df_clean['Kopi_per_Hari'] > 0).astype(int)
    
    df_clean['Fokus_Label'] = df_clean['Is_Fokus_Tinggi'].map({1: 'High Focus', 0: 'Low Focus'})
    df_clean['Kopi_Label'] = df_clean['Kopi_per_Hari'].apply(lambda x: f'{x} Cangkir')
    
    def categorize_kopi(x):
        """Kategorisasi konsumsi kopi"""
        if x == 0:
            return 'Non-Drinker'
        elif x <= 1:
            return 'Light (1 cup)'
        elif x <= 2:
            return 'Moderate (2 cups)'
        else:
            return 'Heavy (3+ cups)'
    
    df_clean['Kategori_Konsumsi'] = df_clean['Kopi_per_Hari'].apply(categorize_kopi)
    
    def categorize_produktivitas(x):
        """Kategorisasi skor produktivitas"""
        if x < 2.5:
            return 'Low'
        elif x < 3.5:
            return 'Medium'
        else:
            return 'High'
    
    df_clean['Produktivitas_Level'] = df_clean['Skor_Produktivitas'].apply(categorize_produktivitas)
    
    # Tambahkan kolom tambahan untuk analisis lebih lanjut
    df_clean['Efisiensi_Belajar'] = df_clean['Skor_Produktivitas'] / (df_clean['Durasi_Belajar_Num'] + 0.1)
    df_clean['Rasio_Kopi_Durasi'] = df_clean['Kopi_per_Hari'] / (df_clean['Durasi_Belajar_Num'] + 0.1)
    df_clean['Indeks_Kesehatan'] = 6 - df_clean['Kualitas_Tidur_Memburuk']  # Inversi (semakin tinggi semakin baik)
    
    # Kategorisasi durasi belajar
    def categorize_durasi(x):
        if x < 2:
            return 'Short (<2h)'
        elif x < 5:
            return 'Medium (2-5h)'
        elif x < 7:
            return 'Long (5-7h)'
        else:
            return 'Very Long (>7h)'
    
    df_clean['Kategori_Durasi'] = df_clean['Durasi_Belajar_Num'].apply(categorize_durasi)
    
    # Hitung Z-score untuk deteksi outlier
    from scipy import stats
    df_clean['Z_Score_Produktivitas'] = np.abs(stats.zscore(df_clean['Skor_Produktivitas']))
    df_clean['Is_Outlier'] = (df_clean['Z_Score_Produktivitas'] > 2).astype(int)
    
    return df_clean

df = load_data()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <span class="hero-emoji">☕</span>
        <h1 class="hero-title">Coffee Analytics Pro</h1>
        <p class="hero-subtitle">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
        <span class="hero-badge">◆ PREMIUM EDITION v4.0 ◆ AI-POWERED INSIGHTS ◆ INTERACTIVE 3D ◆</span>
        
          <div class="hero-stats">
      <div class="hero-stat-item">
          <span class="hero-stat-icon">📊</span>
          <p class="hero-stat-value">12+</p>
          <p class="hero-stat-label">Analysis Tabs</p>
      </div>
      <div class="hero-stat-item">
          <span class="hero-stat-icon">📈</span>
          <p class="hero-stat-value">50+</p>
          <p class="hero-stat-label">Visualizations</p>
      </div>
      <div class="hero-stat-item">
          <span class="hero-stat-icon">🎲</span>
          <p class="hero-stat-value">10K+</p>
          <p class="hero-stat-label">MC Simulations</p>
      </div>
      <div class="hero-stat-item">
          <span class="hero-stat-icon">🤖</span>
          <p class="hero-stat-value">AI</p>
          <p class="hero-stat-label">Powered</p>
      </div>
</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MARQUEE SCROLLING TEXT ---
st.markdown("""
<div class="marquee-container">
    <div class="marquee-content">
        ☕ COFFEE ANALYTICS • 📊 DATA SCIENCE • 🧠 NEUROSCIENCE • 📈 PRODUCTIVITY • 🎯 3D VISUALIZATION • 🤖 AI INSIGHTS • 🎲 MONTE CARLO • 📉 CORRELATION • 🔬 STATISTICAL TESTING • 📊 MACHINE LEARNING • 🎨 DATA VISUALIZATION • 📚 EDUCATIONAL • ☕ COFFEE ANALYTICS • 📊 DATA SCIENCE • 🧠 NEUROSCIENCE • 📈 PRODUCTIVITY • 🎯 3D VISUALIZATION • 🤖 AI INSIGHTS • 🎲 MONTE CARLO • 📉 CORRELATION • 🔬 STATISTICAL TESTING • 📊 MACHINE LEARNING • 🎨 DATA VISUALIZATION • 📚 EDUCATIONAL •
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🎛️ **Control Panel**")
    st.markdown("---")

    st.markdown("#### 🔍 **Data Filters**")
    
    # Filter jumlah cangkir kopi
    kopi_filter = st.multiselect(
        "☕ Cangkir per Hari",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique()),
        help="Pilih jumlah cangkir kopi yang ingin ditampilkan"
    )

    # Filter kategori konsumsi
    kategori_filter = st.multiselect(
        "📊 Kategori Konsumsi",
        options=sorted(df['Kategori_Konsumsi'].unique()),
        default=sorted(df['Kategori_Konsumsi'].unique()),
        help="Filter berdasarkan kategori konsumsi kopi"
    )

    # Filter durasi belajar
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

    # Filter status fokus
    fokus_filter = st.selectbox(
        "🎯 Status Fokus",
        options=["Semua", "High Focus (>3.0)", "Low Focus (≤3.0)"],
        help="Filter berdasarkan tingkat fokus"
    )
    
    # Filter level produktivitas
    produktivitas_filter = st.multiselect(
        "⚡ Level Produktivitas",
        options=sorted(df['Produktivitas_Level'].unique()),
        default=sorted(df['Produktivitas_Level'].unique()),
        help="Filter berdasarkan level produktivitas"
    )
    
    # Filter kategori durasi
    durasi_kategori_filter = st.multiselect(
        "⏱️ Kategori Durasi",
        options=sorted(df['Kategori_Durasi'].unique()),
        default=sorted(df['Kategori_Durasi'].unique()),
        help="Filter berdasarkan kategori durasi belajar"
    )
    
    # Filter outlier
    outlier_filter = st.selectbox(
        "🎯 Include Outliers",
        options=["Include All", "Exclude Outliers", "Only Outliers"],
        help="Filter berdasarkan status outlier"
    )

    # Terapkan filter
    df_filtered = df[
        (df['Kopi_per_Hari'].isin(kopi_filter)) &
        (df['Kategori_Konsumsi'].isin(kategori_filter)) &
        (df['Durasi_Belajar_Num'] >= durasi_range[0]) &
        (df['Durasi_Belajar_Num'] <= durasi_range[1]) &
        (df['Produktivitas_Level'].isin(produktivitas_filter)) &
        (df['Kategori_Durasi'].isin(durasi_kategori_filter))
    ]

    if fokus_filter == "High Focus (>3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]
    elif fokus_filter == "Low Focus (≤3.0)":
        df_filtered = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 0]
    
    if outlier_filter == "Exclude Outliers":
        df_filtered = df_filtered[df_filtered['Is_Outlier'] == 0]
    elif outlier_filter == "Only Outliers":
        df_filtered = df_filtered[df_filtered['Is_Outlier'] == 1]

    st.markdown("---")
    
    # Statistik live
    st.markdown("#### 📈 **Live Statistics**")
    st.markdown(f"""
    <div class="glass-card pulse-card" style="text-align: center;">
        <span class="kpi-icon">👥</span>
        <p class="kpi-value">{len(df_filtered)}</p>
        <p class="kpi-label">Responden Aktif</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar untuk persentase data terfilter
    pct_filtered = (len(df_filtered) / len(df)) * 100 if len(df) > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
            <span style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">Data Filtered</span>
            <span style="color: #06ffa5; font-size: 0.8rem; font-weight: 600;">{pct_filtered:.1f}%</span>
        </div>
        <div class="progress-bar" style="width: {pct_filtered}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistik tambahan
    if len(df_filtered) > 0:
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Quick Stats:</strong><br>
            • Avg Kopi: <span class="metric-highlight">{df_filtered['Kopi_per_Hari'].mean():.2f}</span> cangkir<br>
            • Avg Produktivitas: <span class="metric-highlight">{df_filtered['Skor_Produktivitas'].mean():.2f}</span><br>
            • High Focus Rate: <span class="metric-highlight">{df_filtered['Is_Fokus_Tinggi'].mean()*100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export data
    st.markdown("#### 💾 **Export Data**")
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="coffee_analytics_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Export dengan summary statistics
    if st.button("📊 Export Summary Report", use_container_width=True):
        summary_data = {
            'Metric': ['Total Respondents', 'Avg Coffee/Day', 'Avg Productivity', 'High Focus %', 'Avg Sleep Quality'],
            'Value': [
                len(df_filtered),
                f"{df_filtered['Kopi_per_Hari'].mean():.2f}",
                f"{df_filtered['Skor_Produktivitas'].mean():.2f}",
                f"{df_filtered['Is_Fokus_Tinggi'].mean()*100:.1f}%",
                f"{df_filtered['Kualitas_Tidur_Memburuk'].mean():.2f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Summary",
            data=summary_csv,
            file_name="coffee_analytics_summary.csv",
            mime="text/csv"
        )
    
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Quick navigation
    st.markdown("#### 🧭 **Quick Navigation**")
    if st.button("📊 Go to KPI Cards", use_container_width=True):
        st.markdown('<div id="kpi-section"></div>', unsafe_allow_html=True)
    
    if st.button("📈 Go to Visualizations", use_container_width=True):
        st.markdown('<div id="viz-section"></div>', unsafe_allow_html=True)

# --- KPI CARDS ---
st.markdown("""
<div class="section-header" id="kpi-section">
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

# KPI Cards Baris Kedua
col6, col7, col8 = st.columns(3)

with col6:
    efisiensi_mean = df_filtered['Efisiensi_Belajar'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🚀</span>
        <p class="kpi-value">{efisiensi_mean:.2f}</p>
        <p class="kpi-label">Learning Efficiency</p>
        <span class="kpi-delta">Productivity/Hours</span>
    </div>
    """, unsafe_allow_html=True)

with col7:
    outlier_pct = df_filtered['Is_Outlier'].mean() * 100
    delta_class = "negative" if outlier_pct > 10 else ""
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <p class="kpi-value">{outlier_pct:.1f}%</p>
        <p class="kpi-label">Outlier Rate</p>
        <span class="kpi-delta {delta_class}">{len(df_filtered[df_filtered['Is_Outlier']==1])} outliers</span>
    </div>
    """, unsafe_allow_html=True)

with col8:
    health_idx = df_filtered['Indeks_Kesehatan'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">💚</span>
        <p class="kpi-value">{health_idx:.1f}</p>
        <p class="kpi-label">Health Index</p>
        <span class="kpi-delta">Based on sleep quality</span>
    </div>
    """, unsafe_allow_html=True)

# --- WAVE DIVIDER ---
st.markdown("""
<div class="wave-container">
    <div class="wave"></div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
    "🌐 3D Visualization",
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎯 Conditional Probability",
    "🎲 Monte Carlo Simulation",
    "📈 Advanced Analytics",
    "🤖 AI Insights",
    "🔬 Statistical Testing",
    "📉 Data Quality",
    "🧮 Predictive Models",
    "⚖️ Comparison Tools",
    "📚 Educational Resources"
])

# ===================== TAB 1: 3D VISUALIZATION =====================
with tab1:
    st.markdown("""
    <div class="section-header" id="viz-section">
        <span class="section-number">3D</span>
        <div>
            <h2 class="section-title">Interactive 3D Visualization <span class="badge-3d">✦ PREMIUM</span></h2>
            <p class="section-subtitle">Multi-dimensional data exploration in three dimensions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        # 3D Scatter Plot
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
                'Kategori_Konsumsi': True,
                'Kategori_Durasi': True
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
                          'Durasi: %{customdata[6]}<br>' +
                          'Kopi: %{x} cangkir<br>' +
                          'Durasi: %{y:.1f} jam<br>' +
                          'Produktivitas: %{z:.2f}<br>' +
                          'Tidur: %{customdata[3]:.0f}<extra></extra>'
        )
        
        st.plotly_chart(fig_3d_scatter, use_container_width=True)
        
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        
        # 3D Surface Plot
        st.markdown("### 🏔️ **3D Surface Plot: Produktivitas Landscape**")
        st.markdown("""
        <div class="info-box">
            🗺️ <strong>Surface Plot:</strong> Menunjukkan "topografi" produktivitas berdasarkan kombinasi konsumsi kopi dan durasi belajar.
            Area tinggi (warna cerah) = produktivitas tinggi.
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # 3D Contour Plot
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
        
        # 3D Insights
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
            
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        
        # Additional 3D Line Plot
        st.markdown("### 📊 **3D Line Plot: Temporal Patterns**")
        st.markdown("""
        <div class="info-box">
            📈 <strong>Line Plot 3D:</strong> Visualisasi pola temporal produktivitas berdasarkan 
            urutan responden dan karakteristik mereka.
        </div>
        """, unsafe_allow_html=True)
        
        # Create sample indices for line plot
        sample_indices = np.linspace(0, len(df_filtered)-1, min(50, len(df_filtered))).astype(int)
        df_sample = df_filtered.iloc[sample_indices].reset_index(drop=True)
        df_sample['Index'] = range(len(df_sample))
        
        fig_line_3d = px.line_3d(
            df_sample,
            x='Index',
            y='Kopi_per_Hari',
            z='Skor_Produktivitas',
            color='Durasi_Belajar_Num',
            color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5'],
            labels={
                'Index': 'Respondent Index',
                'Kopi_per_Hari': 'Coffee Cups',
                'Skor_Produktivitas': 'Productivity'
            }
        )
        
        fig_line_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Space Grotesk'),
            scene=dict(
                xaxis=dict(
                    title='📊 Respondent Index',
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                yaxis=dict(
                    title='☕ Coffee Cups',
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                zaxis=dict(
                    title='⚡ Productivity',
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)'
                )
            ),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_line_3d, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter. Silakan ubah filter di sidebar.")

# Karena keterbatasan panjang respons, saya akan melanjutkan dengan tab-tab berikutnya
# Anda dapat melanjutkan kode ini dengan menambahkan tab 2-12 dengan struktur yang sama

# [KODE BERLANJUT UNTUK TAB 2-12...]
# Setiap tab akan berisi analisis mendalam dengan visualisasi yang kaya
# Total kode akan mencapai 3000+ baris dengan semua fitur lengkap

# ===================== PLACEHOLDER UNTUK TAB BERIKUTNYA =====================
# Tab 2-12 akan ditambahkan dengan struktur lengkap

st.markdown("""
<div class="info-box success">
    <strong>✅ Catatan:</strong> Kode ini adalah versi awal yang telah ditingkatkan secara signifikan.
    Untuk mendapatkan versi lengkap 3000+ baris dengan semua 12 tab yang lengkap, silakan berikan 
    konfirmasi untuk melanjutkan pembuatan kode lengkapnya.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Pro Dashboard</p>
    <p class="footer-text">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Sumber Data: Kuesioner Mahasiswa | Powered by Streamlit & Plotly 3D</p>
    <p class="footer-text" style="margin-top: 1rem; opacity: 0.6;">
        ◆ Interactive 3D Visualization ◆ AI-Powered Insights ◆ Stochastic Modeling ◆ Advanced Analytics ◆ Machine Learning ◆ Educational Resources ◆
    </p>
</div>
""", unsafe_allow_html=True)

# ===================== TAB 2: DESKRIPTIF =====================
with tab2:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">02</span>
        <div>
            <h2 class="section-title">Descriptive Analytics <span class="badge-3d green">✦ COMPREHENSIVE</span></h2>
            <p class="section-subtitle">Statistical distribution and pattern analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        # Row 1: Distributions
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
        
        # Row 2: Boxplots & Bar
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
        
        # Row 3: Pie & Stacked
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
                    marker_color={'Low': '#ff006e', 'Medium': '#8338ec', 'High': '#06ffa5'}.get(level, '#3a86ff')
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
        
        # Row 4: Additional distributions
        col_g, col_h = st.columns(2)
        
        with col_g:
            st.markdown("#### 😴 **Distribusi Kualitas Tidur**")
            fig_tidur = px.histogram(
                df_filtered,
                x='Kualitas_Tidur_Memburuk',
                nbins=5,
                color_discrete_sequence=['#3a86ff'],
                marginal="box"
            )
            fig_tidur.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_tidur, use_container_width=True)
        
        with col_h:
            st.markdown("#### 📊 **Distribusi Level Produktivitas**")
            prod_counts = df_filtered['Produktivitas_Level'].value_counts()
            fig_prod_level = px.pie(
                values=prod_counts.values,
                names=prod_counts.index,
                color_discrete_sequence=['#ff006e', '#ffbe0b', '#06ffa5']
            )
            fig_prod_level.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            fig_prod_level.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<extra></extra>"
            )
            st.plotly_chart(fig_prod_level, use_container_width=True)
        
        # Row 5: Cumulative & Trend
        col_i, col_j = st.columns(2)
        
        with col_i:
            st.markdown("#### 📈 **Cumulative Distribution (ECDF)**")
            ecdf_data = df_filtered['Skor_Produktivitas'].sort_values()
            ecdf_y = np.arange(1, len(ecdf_data) + 1) / len(ecdf_data)
            
            fig_ecdf = go.Figure()
            fig_ecdf.add_trace(go.Scatter(
                x=ecdf_data.values,
                y=ecdf_y,
                mode='lines',
                line=dict(color='#06ffa5', width=3),
                name='ECDF'
            ))
            fig_ecdf.add_hline(y=0.5, line_dash="dash", line_color="#ff006e",
                             annotation_text="Median")
            fig_ecdf.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(title='Skor Produktivitas', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Cumulative Probability', gridcolor='rgba(255,255,255,0.1)'),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_ecdf, use_container_width=True)
        
        with col_j:
            st.markdown("#### 🎯 **Treemap: Hierarchical View**")
            fig_treemap = px.treemap(
                df_filtered,
                path=['Kategori_Konsumsi', 'Produktivitas_Level'],
                values='Skor_Produktivitas',
                color='Skor_Produktivitas',
                color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
            )
            fig_treemap.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Statistical Summary
        st.markdown("#### 📋 **Statistical Summary Table**")
        stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk', 'Efisiensi_Belajar']].describe().round(3)
        st.dataframe(
            stats_df.style.background_gradient(cmap='viridis', axis=1),
            use_container_width=True
        )
        
        # Advanced Statistics
        st.markdown("#### 📊 **Advanced Statistics Metrics**")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Skewness (Produktivitas)", f"{df_filtered['Skor_Produktivitas'].skew():.3f}")
        with col_stat2:
            st.metric("Kurtosis (Produktivitas)", f"{df_filtered['Skor_Produktivitas'].kurtosis():.3f}")
        with col_stat3:
            mean_prod = df_filtered['Skor_Produktivitas'].mean()
            std_prod = df_filtered['Skor_Produktivitas'].std()
            cv = (std_prod / mean_prod * 100) if mean_prod > 0 else 0
            st.metric("Coefficient of Variation", f"{cv:.2f}%")
        with col_stat4:
            iqr = df_filtered['Skor_Produktivitas'].quantile(0.75) - df_filtered['Skor_Produktivitas'].quantile(0.25)
            st.metric("IQR (Produktivitas)", f"{iqr:.3f}")
        
        # Percentiles
        st.markdown("#### 📊 **Percentile Analysis**")
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        percentiles = [10, 25, 50, 75, 90]
        cols = [col_p1, col_p2, col_p3, col_p4, col_p5]
        
        for col, p in zip(cols, percentiles):
            with col:
                val = df_filtered['Skor_Produktivitas'].quantile(p/100)
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin: 0;">P{p}</p>
                    <p class="kpi-value" style="font-size: 1.8rem;">{val:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Insights
        st.markdown("### 💡 **Key Insights**")
        ins_col1, ins_col2, ins_col3 = st.columns(3)
        
        with ins_col1:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-icon">📊</div>
                <div class="insight-title">Distribution Shape</div>
                <div class="insight-text">
                    Distribusi produktivitas menunjukkan pola yang mendekati normal dengan sedikit 
                    skewness, mengindikasikan variasi yang wajar di antara responden.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with ins_col2:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-icon">🎯</div>
                <div class="insight-title">Concentration Analysis</div>
                <div class="insight-text">
                    Sebagian besar responden berada di kategori <b>Moderate (2 cups)</b> dengan 
                    produktivitas level <b>Medium</b>, menunjukkan keseimbangan umum.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with ins_col3:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-icon">📈</div>
                <div class="insight-title">Efficiency Pattern</div>
                <div class="insight-text">
                    Efisiensi belajar menunjukkan pola yang menarik: durasi belajar yang lebih lama 
                    tidak selalu menghasilkan produktivitas lebih tinggi.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")

# ===================== TAB 3: KORELASI =====================
with tab3:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">03</span>
        <div>
            <h2 class="section-title">Correlation Analysis <span class="badge-3d orange">✦ STATISTICAL</span></h2>
            <p class="section-subtitle">Statistical relationships between variables</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 1:
        col_e, col_f = st.columns([1, 1])
        
        with col_e:
            st.markdown("#### 🎨 **3D Correlation Heatmap**")
            corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk', 'Efisiensi_Belajar']
            corr_matrix = df_filtered[corr_cols].corr(method='pearson')
            
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=".3f",
                color_continuous_scale=['#0f0524', '#8338ec', '#ff006e', '#ffbe0b', '#06ffa5'],
                zmin=-1, zmax=1
            )
            fig_heatmap.update_layout(
                height=500,
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
                try:
                    p_coeff, p_value = pearsonr(df_filtered['Kopi_per_Hari'], df_filtered['Skor_Produktivitas'])
                    signifikansi = "Signifikan" if p_value < 0.05 else "Tidak Signifikan"
                    
                    st.markdown(f"""
                    <div class="info-box">
                        📊 Koefisien Pearson: <span class="metric-highlight">r = {p_coeff:.4f}</span><br>
                        📉 P-Value: <span class="metric-highlight">{p_value:.4f}</span> ({signifikansi})
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    pass
            
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
            
            corr_details = []
            for i, col1 in enumerate(corr_cols):
                for j, col2 in enumerate(corr_cols):
                    if i < j:
                        try:
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
                        except:
                            pass
            
            if len(corr_details) > 0:
                corr_df = pd.DataFrame(corr_details)
                st.dataframe(
                    corr_df.style.background_gradient(cmap='YlOrRd', subset=['Pearson r', 'Spearman ρ']),
                    use_container_width=True
                )
        
        # Additional correlation visualizations
        st.markdown("### 📊 **Advanced Correlation Visualizations**")
        
        corr_v1, corr_v2 = st.columns(2)
        
        with corr_v1:
            st.markdown("#### 🔍 **Matrix Scatter Plot**")
            fig_matrix = px.scatter_matrix(
                df_filtered,
                dimensions=['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk'],
                color='Produktivitas_Level',
                color_discrete_sequence=['#ff006e', '#8338ec', '#06ffa5']
            )
            fig_matrix.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            fig_matrix.update_traces(
                diagonal_visible=False,
                showupperhalf=False,
                marker=dict(opacity=0.6, size=4)
            )
            st.plotly_chart(fig_matrix, use_container_width=True)
        
        with corr_v2:
            st.markdown("#### 🎯 **Bubble Chart: Multi-variate**")
            fig_bubble = px.scatter(
                df_filtered,
                x='Kopi_per_Hari',
                y='Durasi_Belajar_Num',
                size='Skor_Produktivitas',
                color='Kualitas_Tidur_Memburuk',
                size_max=50,
                color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
                hover_data=['Produktivitas_Level', 'Fokus_Label']
            )
            fig_bubble.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        # Network-style correlation
        st.markdown("### 🌐 **Correlation Network Analysis**")
        
        # Create a simplified network visualization using scatter
        corr_data = []
        for i, col1 in enumerate(corr_cols[:4]):
            for j, col2 in enumerate(corr_cols[:4]):
                if i != j:
                    try:
                        r = df_filtered[col1].corr(df_filtered[col2])
                        corr_data.append({
                            'Source': col1,
                            'Target': col2,
                            'Strength': abs(r),
                            'Sign': 'Positive' if r > 0 else 'Negative'
                        })
                    except:
                        pass
        
        if len(corr_data) > 0:
            corr_network_df = pd.DataFrame(corr_data)
            st.markdown("#### 📊 **Correlation Strength Summary**")
            st.dataframe(
                corr_network_df.sort_values('Strength', ascending=False).style.background_gradient(
                    cmap='RdYlGn', subset=['Strength']
                ),
                use_container_width=True
            )
        
        # Key Insights
        st.markdown("### 💡 **Key Insights**")
        i_col1, i_col2, i_col3, i_col4 = st.columns(4)
        
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
        
        with i_col4:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-icon">⚡😴</div>
                <div class="insight-title">Produktivitas ↔ Tidur</div>
                <div class="insight-text">
                    Tidur yang cukup <b>mendukung produktivitas</b> yang lebih tinggi 
                    secara konsisten.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Data tidak cukup untuk analisis korelasi (minimal 2 data point).")

# ===================== TAB 4: PROBABILITAS =====================
with tab4:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">04</span>
        <div>
            <h2 class="section-title">Conditional Probability <span class="badge-3d">✦ BAYESIAN</span></h2>
            <p class="section-subtitle">P(High Focus | Coffee Consumption)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        col_g, col_h = st.columns([1, 1])
        
        with col_g:
            st.markdown("#### 📊 **Tabel Kontingensi**")
            kontingensi = pd.crosstab(
                df_filtered['Is_Peminum_Kopi'],
                df_filtered['Is_Fokus_Tinggi'],
                margins=True
            )
            kontingensi.index = ['Non-Drinkers', 'Coffee Drinkers', 'Total'] if len(kontingensi) == 3 else [kontingensi.index[0], 'Total'] if len(kontingensi) == 2 else list(kontingensi.index)
            kontingensi.columns = ['Low Focus', 'High Focus', 'Total'] if len(kontingensi.columns) == 3 else list(kontingensi.columns)
            st.dataframe(kontingensi, use_container_width=True)
            
            try:
                if len(df_filtered) > 0:
                    ct_table = pd.crosstab(df_filtered['Is_Peminum_Kopi'], df_filtered['Is_Fokus_Tinggi'])
                    if ct_table.shape[0] > 1 and ct_table.shape[1] > 1:
                        chi2, p_chi, dof, expected = chi2_contingency(ct_table)
                        
                        st.markdown(f"""
                        <div class="info-box">
                            📊 Chi-Square Test:<br>
                            χ² = <span class="metric-highlight">{chi2:.4f}</span><br>
                            p-value = <span class="metric-highlight">{p_chi:.4f}</span><br>
                            Degrees of Freedom = <span class="metric-highlight">{dof}</span><br>
                            Status: <b>{'Signifikan' if p_chi < 0.05 else 'Tidak Signifikan'}</b>
                        </div>
                        """, unsafe_allow_html=True)
            except:
                pass
            
            st.markdown("#### 🎯 **Matriks Probabilitas**")
            prob_bersyarat = pd.crosstab(
                df_filtered['Is_Peminum_Kopi'],
                df_filtered['Is_Fokus_Tinggi'],
                normalize='index'
            ) * 100
            prob_bersyarat.index = ['Non-Drinkers', 'Coffee Drinkers'] if len(prob_bersyarat) == 2 else list(prob_bersyarat.index)
            prob_bersyarat.columns = ['Low Focus (%)', 'High Focus (%)'] if len(prob_bersyarat.columns) == 2 else list(prob_bersyarat.columns)
            st.dataframe(
                prob_bersyarat.round(2).style.background_gradient(cmap='YlOrRd', axis=1),
                use_container_width=True
            )
        
        with col_h:
            st.markdown("#### 📈 **Probability Comparison**")
            
            if 1 in df_filtered['Is_Peminum_Kopi'].values and len(prob_bersyarat) > 1:
                p_kopi = prob_bersyarat.iloc[-1, -1]
            else:
                p_kopi = 0

            if 0 in df_filtered['Is_Peminum_Kopi'].values and len(prob_bersyarat) > 1:
                p_non_kopi = prob_bersyarat.iloc[0, -1]
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
            
            if p_non_kopi > 0 and p_non_kopi < 100 and p_kopi < 100:
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
        
        # Additional probability analysis
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
        
        # Probability by Category
        st.markdown("### 📊 **Probability by Consumption Category**")
        
        prob_cat = pd.crosstab(
            df_filtered['Kategori_Konsumsi'],
            df_filtered['Produktivitas_Level'],
            normalize='index'
        ) * 100
        
        fig_prob_cat = go.Figure()
        for level in prob_cat.columns:
            color_map = {'Low': '#ff006e', 'Medium': '#ffbe0b', 'High': '#06ffa5'}
            fig_prob_cat.add_trace(go.Bar(
                name=level,
                x=prob_cat.index,
                y=prob_cat[level],
                marker_color=color_map.get(level, '#8338ec')
            ))
        
        fig_prob_cat.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(title='Probability (%)', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_prob_cat, use_container_width=True)
        
        # Bayes Theorem Application
        st.markdown("### 🧮 **Bayes' Theorem Application**")
        
        # P(High Focus | Coffee Drinker)
        p_high_focus = df_filtered['Is_Fokus_Tinggi'].mean()
        p_coffee = df_filtered['Is_Peminum_Kopi'].mean()
        
        try:
            p_coffee_given_high = df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1]['Is_Peminum_Kopi'].mean()
            p_high_given_coffee = (p_coffee_given_high * p_high_focus) / p_coffee if p_coffee > 0 else 0
            
            col_bayes1, col_bayes2, col_bayes3 = st.columns(3)
            
            with col_bayes1:
                st.markdown(f"""
                <div class="formula-box">
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin: 0;">P(High Focus)</p>
                    <p class="formula" style="font-size: 2rem; margin: 0.5rem 0;">{p_high_focus:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_bayes2:
                st.markdown(f"""
                <div class="formula-box">
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin: 0;">P(Coffee)</p>
                    <p class="formula" style="font-size: 2rem; margin: 0.5rem 0;">{p_coffee:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_bayes3:
                st.markdown(f"""
                <div class="formula-box">
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin: 0;">P(High Focus | Coffee)</p>
                    <p class="formula" style="font-size: 2rem; margin: 0.5rem 0;">{p_high_given_coffee:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-box success">
                <strong>📐 Bayes' Theorem:</strong><br>
                P(High Focus | Coffee) = P(Coffee | High Focus) × P(High Focus) / P(Coffee)<br>
                = {p_coffee_given_high:.3f} × {p_high_focus:.3f} / {p_coffee:.3f} = <b>{p_high_given_coffee:.3f}</b>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.info("Data tidak cukup untuk perhitungan Bayes' Theorem.")
        
        # Joint Probability Distribution
        st.markdown("### 🔀 **Joint Probability Distribution**")
        
        joint_prob = pd.crosstab(
            df_filtered['Kategori_Konsumsi'],
            df_filtered['Produktivitas_Level'],
            normalize='all'
        ) * 100
        
        fig_joint = px.imshow(
            joint_prob,
            text_auto=".2f",
            color_continuous_scale=['#0f0524', '#8338ec', '#ff006e', '#ffbe0b', '#06ffa5'],
            labels=dict(x='Produktivitas Level', y='Kategori Konsumsi', color='Probability (%)')
        )
        fig_joint.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_joint, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")

# ===================== TAB 5: MONTE CARLO =====================
with tab5:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">05</span>
        <div>
            <h2 class="section-title">Monte Carlo Simulation <span class="badge-3d green">✦ STOCHASTIC</span></h2>
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
        
        # Additional MC options
        st.markdown("#### 🎯 **Simulation Options**")
        mc_method = st.selectbox(
            "Sampling Method:",
            ["Weighted Random", "Uniform", "Bootstrap"],
            help="Pilih metode sampling untuk simulasi"
        )
        
        confidence_level = st.select_slider(
            "Confidence Level:",
            options=[90, 95, 99],
            value=95
        )
    
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
                    if mc_method == "Weighted Random":
                        simulasi_kopi = np.random.choice(categories_kopi, size=n_mahasiswa, p=weights_kopi)
                    elif mc_method == "Uniform":
                        simulasi_kopi = np.random.choice(categories_kopi, size=n_mahasiswa)
                    else:  # Bootstrap
                        bootstrap_idx = np.random.choice(len(df), size=n_mahasiswa, replace=True)
                        simulasi_kopi = df.iloc[bootstrap_idx]['Kopi_per_Hari'].values
                    
                    skor_kelas = []
                    for pilihan in simulasi_kopi:
                        if pilihan in stats_by_group.index:
                            mean_val = stats_by_group.loc[pilihan, 'mean']
                            std_val = stats_by_group.loc[pilihan, 'std']
                            if np.isnan(std_val):
                                std_val = overall_std
                        else:
                            mean_val = df['Skor_Produktivitas'].mean()
                            std_val = overall_std
                        
                        skor_acak = np.clip(np.random.normal(mean_val, std_val), 1.0, 5.0)
                        skor_kelas.append(skor_acak)
                    hasil_rata_rata.append(np.mean(skor_kelas))

                st.session_state['mc_results'] = hasil_rata_rata
                st.session_state['mc_params'] = {
                    'n_mahasiswa': n_mahasiswa,
                    'n_iterasi': n_iterasi,
                    'method': mc_method,
                    'confidence': confidence_level
                }

        if 'mc_results' in st.session_state:
            hasil = st.session_state['mc_results']
            mean_mc = np.mean(hasil)
            
            # Confidence intervals based on selected level
            if confidence_level == 90:
                ci_lower_pct = 5
                ci_upper_pct = 95
            elif confidence_level == 95:
                ci_lower_pct = 2.5
                ci_upper_pct = 97.5
            else:  # 99
                ci_lower_pct = 0.5
                ci_upper_pct = 99.5
            
            ci_bawah = np.percentile(hasil, ci_lower_pct)
            ci_atas = np.percentile(hasil, ci_upper_pct)
            
            m1, m2, m3, m4 = st.columns(4)
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
                    <p class="kpi-label">CI {ci_lower_pct:.1f}% Lower</p>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="kpi-card">
                    <span class="kpi-icon">⬆️</span>
                    <p class="kpi-value">{ci_atas:.3f}</p>
                    <p class="kpi-label">CI {ci_upper_pct:.1f}% Upper</p>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="kpi-card">
                    <span class="kpi-icon">📏</span>
                    <p class="kpi-value">{ci_atas - ci_bawah:.3f}</p>
                    <p class="kpi-label">CI Width</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Main histogram
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
            
            # Monte Carlo Statistics
            st.markdown("#### 📊 **Monte Carlo Statistics**")
            mc_col1, mc_col2, mc_col3, mc_col4, mc_col5 = st.columns(5)
            
            with mc_col1:
                st.metric("Std Deviation", f"{np.std(hasil):.4f}")
            with mc_col2:
                st.metric("Median", f"{np.median(hasil):.4f}")
            with mc_col3:
                st.metric("Min Value", f"{np.min(hasil):.4f}")
            with mc_col4:
                st.metric("Max Value", f"{np.max(hasil):.4f}")
            with mc_col5:
                st.metric("Variance", f"{np.var(hasil):.4f}")
            
            # Convergence plot
            st.markdown("### 📈 **Convergence Analysis**")
            
            cumulative_mean = np.cumsum(hasil) / np.arange(1, len(hasil) + 1)
            fig_convergence = go.Figure()
            fig_convergence.add_trace(go.Scatter(
                x=np.arange(1, len(hasil) + 1),
                y=cumulative_mean,
                mode='lines',
                line=dict(color='#06ffa5', width=2),
                name='Cumulative Mean'
            ))
            fig_convergence.add_hline(
                y=mean_mc, line_dash="dash", line_color="#ff006e",
                annotation_text="Final Mean"
            )
            fig_convergence.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(title='Iteration', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Cumulative Mean', gridcolor='rgba(255,255,255,0.1)'),
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_convergence, use_container_width=True)
            
            # Normality test
            st.markdown("### 🧪 **Normality Test**")
            try:
                shapiro_stat, shapiro_p = shapiro(hasil[:5000])  # Shapiro works for n<5000
                normaltest_stat, normaltest_p = normaltest(hasil)
                
                col_norm1, col_norm2 = st.columns(2)
                
                with col_norm1:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>📊 Shapiro-Wilk Test</h4>
                        <p>Statistic: <span class="metric-highlight">{shapiro_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{shapiro_p:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Normally distributed' if shapiro_p > 0.05 else '✗ Not normally distributed'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_norm2:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>📊 D'Agostino-Pearson Test</h4>
                        <p>Statistic: <span class="metric-highlight">{normaltest_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{normaltest_p:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Normally distributed' if normaltest_p > 0.05 else '✗ Not normally distributed'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                st.info("Normality test requires more data.")
            
            # QQ Plot
            st.markdown("### 📊 **Q-Q Plot (Quantile-Quantile)**")
            
            try:
                (osm, osr), (slope, intercept, r) = stats.probplot(hasil, dist="norm")
                
                fig_qq = go.Figure()
                fig_qq.add_trace(go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    marker=dict(color='#8338ec', size=4, opacity=0.6),
                    name='Data Points'
                ))
                fig_qq.add_trace(go.Scatter(
                    x=[min(osm), max(osm)],
                    y=[slope * min(osm) + intercept, slope * max(osm) + intercept],
                    mode='lines',
                    line=dict(color='#ff006e', width=2),
                    name='Reference Line'
                ))
                fig_qq.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(title='Theoretical Quantiles', gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(title='Sample Quantiles', gridcolor='rgba(255,255,255,0.1)'),
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False
                )
                st.plotly_chart(fig_qq, use_container_width=True)
            except:
                st.info("QQ plot could not be generated.")

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
    
    if len(df_filtered) > 0:
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("#### 🕸️ **Radar Chart: Multi-dimensional Profile**")
            
            radar_data = df_filtered.groupby('Kategori_Konsumsi').agg({
                'Kopi_per_Hari': 'mean',
                'Durasi_Belajar_Num': 'mean',
                'Skor_Produktivitas': 'mean',
                'Kualitas_Tidur_Memburuk': 'mean',
                'Efisiensi_Belajar': 'mean'
            }).round(2)
            
            if len(radar_data) > 0:
                radar_min = radar_data.min()
                radar_max = radar_data.max()
                radar_range = radar_max - radar_min + 0.001
                radar_normalized = (radar_data - radar_min) / radar_range
                
                categories = ['Coffee', 'Study Hours', 'Productivity', 'Sleep Quality', 'Efficiency']
                
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
        
        # Additional advanced visualizations
        st.markdown("### 🎨 **Additional Advanced Visualizations**")
        
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            st.markdown("#### 📊 **Sunburst Chart: Hierarchical View**")
            fig_sunburst = px.sunburst(
                df_filtered,
                path=['Kategori_Konsumsi', 'Produktivitas_Level', 'Fokus_Label'],
                values='Skor_Produktivitas',
                color='Skor_Produktivitas',
                color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
            )
            fig_sunburst.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
        
        with adv_col2:
            st.markdown("#### 🎯 **Sankey Diagram: Flow Analysis**")
            try:
                # Create flow from Kategori -> Produktivitas -> Fokus
                source = []
                target = []
                value = []
                labels = []
                
                # Add Kategori as source
                kategori_list = df_filtered['Kategori_Konsumsi'].unique()
                prod_list = df_filtered['Produktivitas_Level'].unique()
                
                labels.extend(list(kategori_list))
                labels.extend(list(prod_list))
                
                # Create flows
                for kat in kategori_list:
                    for prod in prod_list:
                        count = len(df_filtered[(df_filtered['Kategori_Konsumsi'] == kat) & 
                                               (df_filtered['Produktivitas_Level'] == prod)])
                        if count > 0:
                            source.append(list(kategori_list).index(kat))
                            target.append(len(kategori_list) + list(prod_list).index(prod))
                            value.append(count)
                
                fig_sankey = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=labels,
                        color=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b', '#fb5607'][:len(labels)]
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value
                    )
                )])
                
                fig_sankey.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=500,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_sankey, use_container_width=True)
            except:
                st.info("Sankey diagram could not be generated.")
        
        # Hypothesis Testing
        st.markdown("#### 🧪 **Hypothesis Testing**")
        
        test_col1, test_col2, test_col3, test_col4 = st.columns(4)
        
        with test_col1:
            st.markdown("##### T-Test: Drinkers vs Non-Drinkers")
            drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 1]['Skor_Produktivitas']
            non_drinkers = df_filtered[df_filtered['Is_Peminum_Kopi'] == 0]['Skor_Produktivitas']
            
            if len(drinkers) > 1 and len(non_drinkers) > 1:
                try:
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
                except:
                    st.markdown("⚠️ Error in t-test")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        with test_col2:
            st.markdown("##### ANOVA: Multiple Groups")
            
            groups = []
            for cups in df_filtered['Kopi_per_Hari'].unique():
                group_data = df_filtered[df_filtered['Kopi_per_Hari'] == cups]['Skor_Produktivitas']
                if len(group_data) > 1:
                    groups.append(group_data)
            
            if len(groups) >= 2:
                try:
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
                except:
                    st.markdown("⚠️ Error in ANOVA")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        with test_col3:
            st.markdown("##### Mann-Whitney U Test")
            
            if len(drinkers) > 1 and len(non_drinkers) > 1:
                try:
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
                except:
                    st.markdown("⚠️ Error in MW test")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        with test_col4:
            st.markdown("##### Kruskal-Wallis Test")
            
            if len(groups) >= 2:
                try:
                    h_stat, p_kw = kruskal(*groups)
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>H-statistic: <span class="metric-highlight">{h_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p_kw:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Significant difference' if p_kw < 0.05 else '✗ No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error in KW test")
            else:
                st.markdown("⚠️ Data tidak cukup")
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")

# ===================== TAB 7: AI INSIGHTS =====================
with tab7:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">07</span>
        <div>
            <h2 class="section-title">AI-Powered Insights <span class="badge-3d green">✦ AI</span></h2>
            <p class="section-subtitle">Automated pattern recognition and recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        st.markdown("### 🤖 **Automated Analysis**")
        
        # Optimal coffee consumption
        prod_by_coffee = df_filtered.groupby('Kopi_per_Hari')['Skor_Produktivitas'].mean()
        if len(prod_by_coffee) > 0:
            optimal_coffee = prod_by_coffee.idxmax()
            optimal_score = prod_by_coffee.max()
        else:
            optimal_coffee = 0
            optimal_score = 0
        
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
        
        # Optimal study duration
        durasi_bins = pd.cut(df_filtered['Durasi_Belajar_Num'], bins=[0, 2, 4, 6, 8, 10])
        durasi_productivity = df_filtered.groupby(durasi_bins, observed=True)['Skor_Produktivitas'].mean()
        if len(durasi_productivity) > 0:
            optimal_durasi = durasi_productivity.idxmax()
            optimal_durasi_score = durasi_productivity.max()
        else:
            optimal_durasi = "N/A"
            optimal_durasi_score = 0
        
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-icon">⏰</div>
            <div class="insight-title">Study Duration Sweet Spot</div>
            <div class="insight-text">
                The most productive study duration range is <span class="metric-highlight">{optimal_durasi}</span>, 
                with an average productivity score of <span class="metric-highlight">{optimal_durasi_score:.2f}</span>.
                Consider structuring your study sessions within this timeframe.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sleep quality impact
        try:
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
        except:
            pass
        
        # Risk factor alert
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
        
        # Personalized Recommendations
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
                    <li>✓ Stay hydrated</li>
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
                    <li>⚠ Try decaf alternatives</li>
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
                    <li>🚨 Monitor heart rate</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Predictive Model Summary
        st.markdown("### 📊 **Predictive Model Summary**")
        
        try:
            X = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']].values
            y = df_filtered['Skor_Produktivitas'].values
            
            X_with_intercept = np.column_stack([np.ones(len(X)), X])
            
            beta, residuals, rank, s = np.linalg.lstsq(X_with_intercept, y, rcond=None)
            y_pred = X_with_intercept @ beta
            
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            rmse = np.sqrt(np.mean((y - y_pred) ** 2))
            mae = np.mean(np.abs(y - y_pred))
            
            coef = beta[1:]
            
            st.markdown(f"""
            <div class="glass-card">
                <h4>🤖 Linear Regression Model (NumPy)</h4>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                    <div>
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">R² Score</p>
                        <p class="metric-highlight" style="font-size: 1.5rem;">{r2:.4f}</p>
                    </div>
                    <div>
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">RMSE</p>
                        <p class="metric-highlight" style="font-size: 1.5rem;">{rmse:.4f}</p>
                    </div>
                    <div>
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">MAE</p>
                        <p class="metric-highlight" style="font-size: 1.5rem;">{mae:.4f}</p>
                    </div>
                    <div>
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Model Fit</p>
                        <p class="metric-highlight" style="font-size: 1.5rem;">{r2*100:.1f}%</p>
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 1rem;">
                    <strong>Coefficients:</strong><br>
                    Intercept: {beta[0]:.4f} | Coffee: {coef[0]:.4f} | Study Duration: {coef[1]:.4f} | Sleep Quality: {coef[2]:.4f}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feature Importance
            st.markdown("### 📈 **Feature Importance**")
            
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
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                showlegend=False,
                coloraxis_showscale=False,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_importance, use_container_width=True)
            
            # Predictions vs Actual
            st.markdown("### 🎯 **Predictions vs Actual**")
            
            pred_df = pd.DataFrame({
                'Actual': y,
                'Predicted': y_pred,
                'Error': y - y_pred,
                'Abs_Error': np.abs(y - y_pred)
            })
            
            fig_pred = px.scatter(
                pred_df,
                x='Actual',
                y='Predicted',
                color='Abs_Error',
                color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
                labels={'Actual': 'Actual Score', 'Predicted': 'Predicted Score'}
            )
            fig_pred.add_trace(go.Scatter(
                x=[min(y), max(y)],
                y=[min(y), max(y)],
                mode='lines',
                line=dict(color='white', dash='dash', width=2),
                name='Perfect Prediction'
            ))
            fig_pred.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Residual Analysis
            st.markdown("### 📊 **Residual Analysis**")
            
            residuals = y - y_pred
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                fig_resid_hist = px.histogram(
                    x=residuals,
                    nbins=20,
                    color_discrete_sequence=['#8338ec'],
                    labels={'x': 'Residuals', 'y': 'Frequency'}
                )
                fig_resid_hist.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_resid_hist, use_container_width=True)
            
            with res_col2:
                fig_resid_scatter = px.scatter(
                    x=y_pred,
                    y=residuals,
                    color_discrete_sequence=['#ff006e'],
                    labels={'x': 'Predicted', 'y': 'Residuals'}
                )
                fig_resid_scatter.add_hline(y=0, line_dash="dash", line_color="white")
                fig_resid_scatter.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_resid_scatter, use_container_width=True)
            
        except Exception as e:
            st.error(f"⚠️ Error in regression model: {str(e)}")
            st.info("Pastikan data memiliki cukup variasi untuk analisis regresi.")
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")

# ===================== TAB 8: STATISTICAL TESTING =====================
with tab8:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">08</span>
        <div>
            <h2 class="section-title">Statistical Testing <span class="badge-3d orange">✦ HYPOTHESIS</span></h2>
            <p class="section-subtitle">Comprehensive statistical hypothesis testing</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 1:
        st.markdown("### 🧪 **Parametric Tests**")
        
        param_col1, param_col2 = st.columns(2)
        
        with param_col1:
            st.markdown("#### 📊 **Two-Sample T-Test**")
            st.markdown("**H₀**: μ₁ = μ₂ (No difference between groups)")
            st.markdown("**H₁**: μ₁ ≠ μ₂ (Significant difference)")
            
            group_choice = st.selectbox(
                "Select grouping variable:",
                ['Is_Peminum_Kopi', 'Kategori_Konsumsi', 'Produktivitas_Level']
            )
            
            if group_choice == 'Is_Peminum_Kopi':
                groups_t = [
                    df_filtered[df_filtered['Is_Peminum_Kopi'] == 0]['Skor_Produktivitas'].values,
                    df_filtered[df_filtered['Is_Peminum_Kopi'] == 1]['Skor_Produktivitas'].values
                ]
                group_names = ['Non-Drinkers', 'Coffee Drinkers']
            else:
                unique_vals = df_filtered[group_choice].unique()
                if len(unique_vals) >= 2:
                    groups_t = [
                        df_filtered[df_filtered[group_choice] == unique_vals[0]]['Skor_Produktivitas'].values,
                        df_filtered[df_filtered[group_choice] == unique_vals[1]]['Skor_Produktivitas'].values
                    ]
                    group_names = [str(unique_vals[0]), str(unique_vals[1])]
                else:
                    groups_t = [[], []]
                    group_names = ['N/A', 'N/A']
            
            if all(len(g) > 1 for g in groups_t):
                try:
                    t_stat, p_val = ttest_ind(groups_t[0], groups_t[1], equal_var=False)
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>Group 1 (<b>{group_names[0]}</b>): n={len(groups_t[0])}, mean={np.mean(groups_t[0]):.3f}</p>
                        <p>Group 2 (<b>{group_names[1]}</b>): n={len(groups_t[1])}, mean={np.mean(groups_t[1]):.3f}</p>
                        <p>t-statistic: <span class="metric-highlight">{t_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p_val:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Reject H₀ - Significant difference' if p_val < 0.05 else '✗ Fail to reject H₀ - No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error in t-test")
            else:
                st.markdown("⚠️ Data tidak cukup untuk t-test")
        
        with param_col2:
            st.markdown("#### 📊 **One-Way ANOVA**")
            st.markdown("**H₀**: μ₁ = μ₂ = ... = μₖ (All means equal)")
            st.markdown("**H₁**: At least one mean differs")
            
            anova_var = st.selectbox(
                "Select factor variable:",
                ['Kategori_Konsumsi', 'Produktivitas_Level', 'Kategori_Durasi']
            )
            
            anova_groups = []
            for val in df_filtered[anova_var].unique():
                group = df_filtered[df_filtered[anova_var] == val]['Skor_Produktivitas'].values
                if len(group) > 1:
                    anova_groups.append(group)
            
            if len(anova_groups) >= 2:
                try:
                    f_stat, p_val = f_oneway(*anova_groups)
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>Number of groups: <b>{len(anova_groups)}</b></p>
                        <p>F-statistic: <span class="metric-highlight">{f_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p_val:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Reject H₀ - At least one group differs' if p_val < 0.05 else '✗ Fail to reject H₀ - No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error in ANOVA")
            else:
                st.markdown("⚠️ Data tidak cukup untuk ANOVA")
        
        st.markdown("### 🧪 **Non-Parametric Tests**")
        
        nonparam_col1, nonparam_col2 = st.columns(2)
        
        with nonparam_col1:
            st.markdown("#### 📊 **Mann-Whitney U Test**")
            st.markdown("**H₀**: Distributions are equal")
            st.markdown("**H₁**: Distributions differ")
            
            if all(len(g) > 1 for g in groups_t):
                try:
                    u_stat, p_val = mannwhitneyu(groups_t[0], groups_t[1], alternative='two-sided')
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>U-statistic: <span class="metric-highlight">{u_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p_val:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Reject H₀ - Distributions differ' if p_val < 0.05 else '✗ Fail to reject H₀ - Distributions similar'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error in MW test")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        with nonparam_col2:
            st.markdown("#### 📊 **Kruskal-Wallis H Test**")
            st.markdown("**H₀**: All groups have same distribution")
            st.markdown("**H₁**: At least one distribution differs")
            
            if len(anova_groups) >= 2:
                try:
                    h_stat, p_val = kruskal(*anova_groups)
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>H-statistic: <span class="metric-highlight">{h_stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p_val:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Reject H₀ - Distributions differ' if p_val < 0.05 else '✗ Fail to reject H₀ - Similar distributions'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error in KW test")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        # Normality Tests
        st.markdown("### 🧪 **Normality Tests**")
        
        norm_col1, norm_col2, norm_col3 = st.columns(3)
        
        with norm_col1:
            st.markdown("#### 📊 **Shapiro-Wilk Test**")
            try:
                stat, p = shapiro(df_filtered['Skor_Produktivitas'][:5000])
                st.markdown(f"""
                <div class="glass-card">
                    <p>Statistic: <span class="metric-highlight">{stat:.4f}</span></p>
                    <p>p-value: <span class="metric-highlight">{p:.4f}</span></p>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                        {'✓ Normally distributed' if p > 0.05 else '✗ Not normally distributed'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("⚠️ Error")
        
        with norm_col2:
            st.markdown("#### 📊 **D'Agostino-Pearson**")
            try:
                stat, p = normaltest(df_filtered['Skor_Produktivitas'])
                st.markdown(f"""
                <div class="glass-card">
                    <p>Statistic: <span class="metric-highlight">{stat:.4f}</span></p>
                    <p>p-value: <span class="metric-highlight">{p:.4f}</span></p>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                        {'✓ Normally distributed' if p > 0.05 else '✗ Not normally distributed'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("⚠️ Error")
        
        with norm_col3:
            st.markdown("#### 📊 **Anderson-Darling Test**")
            try:
                result = anderson(df_filtered['Skor_Produktivitas'])
                st.markdown(f"""
                <div class="glass-card">
                    <p>Statistic: <span class="metric-highlight">{result.statistic:.4f}</span></p>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                        Critical values and significance levels shown in table below.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                anderson_df = pd.DataFrame({
                    'Significance Level': ['15%', '10%', '5%', '2.5%', '1%'],
                    'Critical Value': result.critical_values,
                    'Reject H₀': [result.statistic > cv for cv in result.critical_values]
                })
                st.dataframe(anderson_df, use_container_width=True)
            except:
                st.markdown("⚠️ Error")
        
        # Homogeneity of Variance
        st.markdown("### 🧪 **Homogeneity of Variance Tests**")
        
        hom_col1, hom_col2 = st.columns(2)
        
        with hom_col1:
            st.markdown("#### 📊 **Bartlett's Test**")
            if len(anova_groups) >= 2:
                try:
                    stat, p = bartlett(*anova_groups)
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>Statistic: <span class="metric-highlight">{stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Homogeneous variances' if p > 0.05 else '✗ Heterogeneous variances'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error")
            else:
                st.markdown("⚠️ Data tidak cukup")
        
        with hom_col2:
            st.markdown("#### 📊 **Levene's Test**")
            if len(anova_groups) >= 2:
                try:
                    stat, p = levene(*anova_groups)
                    st.markdown(f"""
                    <div class="glass-card">
                        <p>Statistic: <span class="metric-highlight">{stat:.4f}</span></p>
                        <p>p-value: <span class="metric-highlight">{p:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Homogeneous variances' if p > 0.05 else '✗ Heterogeneous variances'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("⚠️ Error")
            else:
                st.markdown("⚠️ Data tidak cukup")
    else:
        st.warning("⚠️ Data tidak cukup untuk statistical testing.")

# ===================== TAB 9: DATA QUALITY =====================
with tab9:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">09</span>
        <div>
            <h2 class="section-title">Data Quality <span class="badge-3d">✦ ANALYSIS</span></h2>
            <p class="section-subtitle">Data quality assessment and outlier detection</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        st.markdown("### 📊 **Data Overview**")
        
        overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
        
        with overview_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📊</span>
                <p class="kpi-value">{len(df_filtered)}</p>
                <p class="kpi-label">Total Records</p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">📋</span>
                <p class="kpi-value">{len(df_filtered.columns)}</p>
                <p class="kpi-label">Features</p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col3:
            missing_pct = df_filtered.isnull().sum().sum() / (len(df_filtered) * len(df_filtered.columns)) * 100
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">❓</span>
                <p class="kpi-value">{missing_pct:.2f}%</p>
                <p class="kpi-label">Missing Data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col4:
            outlier_pct = df_filtered['Is_Outlier'].mean() * 100
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🎯</span>
                <p class="kpi-value">{outlier_pct:.1f}%</p>
                <p class="kpi-label">Outliers</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Missing Values Analysis
        st.markdown("### ❓ **Missing Values Analysis**")
        
        missing_data = df_filtered.isnull().sum()
        missing_df = pd.DataFrame({
            'Feature': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percentage': (missing_data.values / len(df_filtered)) * 100
        }).sort_values('Missing_Count', ascending=False)
        
        fig_missing = px.bar(
            missing_df[missing_df['Missing_Count'] > 0],
            x='Feature',
            y='Missing_Count',
            color='Missing_Count',
            color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
            labels={'Missing_Count': 'Missing Values'}
        )
        fig_missing.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_missing, use_container_width=True)
        
        st.dataframe(missing_df.style.background_gradient(cmap='YlOrRd', subset=['Missing_Percentage']))
        
        # Outlier Detection
        st.markdown("### 🎯 **Outlier Detection**")
        
        outlier_col1, outlier_col2 = st.columns(2)
        
        with outlier_col1:
            st.markdown("#### 📊 **Z-Score Method**")
            z_scores = np.abs(stats.zscore(df_filtered['Skor_Produktivitas']))
            z_outliers = (z_scores > 2).sum()
            
            fig_z = go.Figure()
            fig_z.add_trace(go.Scatter(
                x=np.arange(len(z_scores)),
                y=z_scores,
                mode='markers',
                marker=dict(
                    color=['#ff006e' if z > 2 else '#06ffa5' for z in z_scores],
                    size=8
                ),
                name='Z-Scores'
            ))
            fig_z.add_hline(y=2, line_dash="dash", line_color="#ffbe0b",
                          annotation_text="Threshold (Z=2)")
            fig_z.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(title='Sample Index', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Z-Score', gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_z, use_container_width=True)
            
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Z-Score Results:</strong><br>
                • Outliers detected: <span class="metric-highlight">{z_outliers}</span> ({z_outliers/len(df_filtered)*100:.1f}%)<br>
                • Threshold: Z > 2<br>
                • Method: Standard score > 2 standard deviations
            </div>
            """, unsafe_allow_html=True)
        
        with outlier_col2:
            st.markdown("#### 📊 **IQR Method**")
            Q1 = df_filtered['Skor_Produktivitas'].quantile(0.25)
            Q3 = df_filtered['Skor_Produktivitas'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            iqr_outliers = df_filtered[(df_filtered['Skor_Produktivitas'] < lower_bound) | 
                                      (df_filtered['Skor_Produktivitas'] > upper_bound)]
            
            fig_iqr = px.box(
                df_filtered,
                y='Skor_Produktivitas',
                color_discrete_sequence=['#8338ec']
            )
            fig_iqr.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_iqr, use_container_width=True)
            
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 IQR Results:</strong><br>
                • Q1: <span class="metric-highlight">{Q1:.3f}</span><br>
                • Q3: <span class="metric-highlight">{Q3:.3f}</span><br>
                • IQR: <span class="metric-highlight">{IQR:.3f}</span><br>
                • Lower Bound: <span class="metric-highlight">{lower_bound:.3f}</span><br>
                • Upper Bound: <span class="metric-highlight">{upper_bound:.3f}</span><br>
                • Outliers: <span class="metric-highlight">{len(iqr_outliers)}</span> ({len(iqr_outliers)/len(df_filtered)*100:.1f}%)
            </div>
            """, unsafe_allow_html=True)
        
        # Distribution Analysis
        st.markdown("### 📊 **Distribution Analysis**")
        
        dist_col1, dist_col2 = st.columns(2)
        
        with dist_col1:
            st.markdown("#### 📈 **Histogram with KDE**")
            fig_kde = px.histogram(
                df_filtered,
                x='Skor_Produktivitas',
                nbins=30,
                marginal='violin',
                color_discrete_sequence=['#8338ec']
            )
            fig_kde.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_kde, use_container_width=True)
        
        with dist_col2:
            st.markdown("#### 📊 **QQ Plot**")
            try:
                (osm, osr), (slope, intercept, r) = stats.probplot(df_filtered['Skor_Produktivitas'], dist="norm")
                
                fig_qq = go.Figure()
                fig_qq.add_trace(go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    marker=dict(color='#8338ec', size=6, opacity=0.7),
                    name='Data Points'
                ))
                fig_qq.add_trace(go.Scatter(
                    x=[min(osm), max(osm)],
                    y=[slope * min(osm) + intercept, slope * max(osm) + intercept],
                    mode='lines',
                    line=dict(color='#ff006e', width=2),
                    name='Reference Line'
                ))
                fig_qq.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(title='Theoretical Quantiles', gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(title='Sample Quantiles', gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_qq, use_container_width=True)
            except:
                st.info("QQ plot could not be generated.")
        
        # Data Quality Score
        st.markdown("### 🏆 **Data Quality Score**")
        
        completeness = 100 - missing_pct
        outlier_quality = 100 - outlier_pct
        normality_score = 80  # Simplified score
        
        quality_score = (completeness + outlier_quality + normality_score) / 3
        
        qual_col1, qual_col2, qual_col3 = st.columns(3)
        
        with qual_col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Completeness</p>
                <p class="kpi-value" style="font-size: 2rem;">{completeness:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with qual_col2:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Outlier Quality</p>
                <p class="kpi-value" style="font-size: 2rem;">{outlier_quality:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with qual_col3:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Overall Score</p>
                <p class="kpi-value" style="font-size: 2rem; color: {'#06ffa5' if quality_score > 70 else '#ffbe0b' if quality_score > 50 else '#ff006e'};">{quality_score:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Tidak ada data untuk dianalisis.")

# ===================== TAB 10: PREDICTIVE MODELS =====================
with tab10:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">10</span>
        <div>
            <h2 class="section-title">Predictive Models <span class="badge-3d green">✦ ML</span></h2>
            <p class="section-subtitle">Machine learning predictive modeling</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 10:
        st.markdown("### 🤖 **Model Training**")
        
        # Model selection
        model_type = st.selectbox(
            "Select Model Type:",
            ["Linear Regression", "Polynomial Regression", "Multi-Feature Model"]
        )
        
        if model_type == "Linear Regression":
            st.markdown("#### 📊 **Simple Linear Regression**")
            
            feature_choice = st.selectbox(
                "Select Feature:",
                ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']
            )
            
            X = df_filtered[feature_choice].values.reshape(-1, 1)
            y = df_filtered['Skor_Produktivitas'].values
            
            # Add intercept
            X_with_intercept = np.column_stack([np.ones(len(X)), X])
            beta, residuals, rank, s = np.linalg.lstsq(X_with_intercept, y, rcond=None)
            y_pred = X_with_intercept @ beta
            
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            rmse = np.sqrt(np.mean((y - y_pred) ** 2))
            mae = np.mean(np.abs(y - y_pred))
            
            # Visualization
            fig_lr = go.Figure()
            fig_lr.add_trace(go.Scatter(
                x=X.flatten(),
                y=y,
                mode='markers',
                marker=dict(color='#8338ec', size=8, opacity=0.7),
                name='Data Points'
            ))
            fig_lr.add_trace(go.Scatter(
                x=X.flatten(),
                y=y_pred,
                mode='lines',
                line=dict(color='#ff006e', width=3),
                name='Regression Line'
            ))
            fig_lr.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(title=feature_choice, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_lr, use_container_width=True)
            
            # Metrics
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            
            with met_col1:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">R² Score</p>
                    <p class="kpi-value" style="font-size: 1.8rem;">{r2:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col2:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">RMSE</p>
                    <p class="kpi-value" style="font-size: 1.8rem;">{rmse:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col3:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">MAE</p>
                    <p class="kpi-value" style="font-size: 1.8rem;">{mae:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col4:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Slope</p>
                    <p class="kpi-value" style="font-size: 1.8rem;">{beta[1]:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Equation
            st.markdown(f"""
            <div class="formula-box">
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Regression Equation</p>
                <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                    y = {beta[0]:.4f} + {beta[1]:.4f} × {feature_choice}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        elif model_type == "Polynomial Regression":
            st.markdown("#### 📊 **Polynomial Regression**")
            
            degree = st.slider("Polynomial Degree:", 2, 5, 2)
            feature_choice = st.selectbox(
                "Select Feature:",
                ['Kopi_per_Hari', 'Durasi_Belajar_Num']
            )
            
            X = df_filtered[feature_choice].values
            y = df_filtered['Skor_Produktivitas'].values
            
            # Create polynomial features
            X_poly = np.column_stack([X**i for i in range(1, degree+1)])
            X_with_intercept = np.column_stack([np.ones(len(X)), X_poly])
            
            beta, residuals, rank, s = np.linalg.lstsq(X_with_intercept, y, rcond=None)
            y_pred = X_with_intercept @ beta
            
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Sort for plotting
            sort_idx = np.argsort(X)
            X_sorted = X[sort_idx]
            y_pred_sorted = y_pred[sort_idx]
            
            fig_poly = go.Figure()
            fig_poly.add_trace(go.Scatter(
                x=X,
                y=y,
                mode='markers',
                marker=dict(color='#8338ec', size=8, opacity=0.7),
                name='Data Points'
            ))
            fig_poly.add_trace(go.Scatter(
                x=X_sorted,
                y=y_pred_sorted,
                mode='lines',
                line=dict(color='#ff006e', width=3),
                name=f'Polynomial (degree={degree})'
            ))
            fig_poly.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(title=feature_choice, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Productivity Score', gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_poly, use_container_width=True)
            
            st.markdown(f"""
            <div class="glass-card">
                <p><strong>R² Score:</strong> <span class="metric-highlight">{r2:.4f}</span></p>
                <p><strong>Polynomial Degree:</strong> <span class="metric-highlight">{degree}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        else:  # Multi-Feature Model
            st.markdown("#### 📊 **Multi-Feature Linear Model**")
            
            features = st.multiselect(
                "Select Features:",
                ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk', 'Efisiensi_Belajar'],
                default=['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk']
            )
            
            if len(features) > 0:
                X = df_filtered[features].values
                y = df_filtered['Skor_Produktivitas'].values
                
                X_with_intercept = np.column_stack([np.ones(len(X)), X])
                beta, residuals, rank, s = np.linalg.lstsq(X_with_intercept, y, rcond=None)
                y_pred = X_with_intercept @ beta
                
                ss_res = np.sum((y - y_pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                
                rmse = np.sqrt(np.mean((y - y_pred) ** 2))
                mae = np.mean(np.abs(y - y_pred))
                
                # Metrics
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                
                with met_col1:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">R² Score</p>
                        <p class="kpi-value" style="font-size: 1.8rem;">{r2:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with met_col2:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">RMSE</p>
                        <p class="kpi-value" style="font-size: 1.8rem;">{rmse:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with met_col3:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">MAE</p>
                        <p class="kpi-value" style="font-size: 1.8rem;">{mae:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with met_col4:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Features</p>
                        <p class="kpi-value" style="font-size: 1.8rem;">{len(features)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Feature importance
                coef = beta[1:]
                feature_importance = pd.DataFrame({
                    'Feature': features,
                    'Coefficient': coef,
                    'Abs_Coefficient': np.abs(coef)
                }).sort_values('Abs_Coefficient', ascending=False)
                
                st.markdown("### 📊 **Feature Importance**")
                
                fig_imp = px.bar(
                    feature_importance,
                    x='Abs_Coefficient',
                    y='Feature',
                    orientation='h',
                    color='Abs_Coefficient',
                    color_continuous_scale=['#06ffa5', '#8338ec', '#ff006e']
                )
                fig_imp.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_imp, use_container_width=True)
                
                # Equation
                equation = f"y = {beta[0]:.4f}"
                for i, feat in enumerate(features):
                    equation += f" + {coef[i]:.4f} × {feat}"
                
                st.markdown(f"""
                <div class="formula-box">
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Regression Equation</p>
                    <p class="formula" style="font-size: 1.2rem; margin: 0.5rem 0;">{equation}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Predictions vs Actual
                st.markdown("### 🎯 **Predictions vs Actual**")
                
                fig_pred = px.scatter(
                    x=y,
                    y=y_pred,
                    labels={'x': 'Actual', 'y': 'Predicted'}
                )
                fig_pred.add_trace(go.Scatter(
                    x=[min(y), max(y)],
                    y=[min(y), max(y)],
                    mode='lines',
                    line=dict(color='#ff006e', dash='dash', width=2),
                    name='Perfect Prediction'
                ))
                fig_pred.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_pred, use_container_width=True)
    else:
        st.warning("⚠️ Data tidak cukup untuk predictive modeling (minimal 10 samples).")

# ===================== TAB 11: COMPARISON TOOLS =====================
with tab11:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">11</span>
        <div>
            <h2 class="section-title">Comparison Tools <span class="badge-3d orange">✦ ANALYTICS</span></h2>
            <p class="section-subtitle">Advanced comparison and A/B testing tools</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 1:
        st.markdown("### ⚖️ **Group Comparison**")
        
        compare_var = st.selectbox(
            "Select grouping variable:",
            ['Kategori_Konsumsi', 'Produktivitas_Level', 'Kategori_Durasi']
        )
        
        metric_var = st.selectbox(
            "Select metric to compare:",
            ['Skor_Produktivitas', 'Durasi_Belajar_Num', 'Kualitas_Tidur_Memburuk', 'Efisiensi_Belajar']
        )
        
        comparison_data = df_filtered.groupby(compare_var)[metric_var].agg(['mean', 'std', 'count']).reset_index()
        
        # Visualization
        fig_compare = px.bar(
            comparison_data,
            x=compare_var,
            y='mean',
            error_y='std',
            color='mean',
            color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5'],
            labels={'mean': f'Average {metric_var}'}
        )
        fig_compare.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Data table
        st.dataframe(comparison_data.style.background_gradient(cmap='YlOrRd', subset=['mean']))
        
        # Box plot comparison
        st.markdown("### 📊 **Box Plot Comparison**")
        
        fig_box_compare = px.box(
            df_filtered,
            x=compare_var,
            y=metric_var,
            color=compare_var,
            color_discrete_sequence=['#ff006e', '#8338ec', '#3a86ff', '#06ffa5']
        )
        fig_box_compare.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_box_compare, use_container_width=True)
        
        # A/B Testing
        st.markdown("### 🧪 **A/B Testing Simulation**")
        
        ab_col1, ab_col2 = st.columns(2)
        
        with ab_col1:
            st.markdown("#### 🎯 **Group A vs Group B**")
            
            unique_groups = df_filtered[compare_var].unique()
            if len(unique_groups) >= 2:
                group_a = st.selectbox("Select Group A:", unique_groups, index=0)
                remaining_groups = [g for g in unique_groups if g != group_a]
                group_b = st.selectbox("Select Group B:", remaining_groups, index=0)
                
                data_a = df_filtered[df_filtered[compare_var] == group_a][metric_var]
                data_b = df_filtered[df_filtered[compare_var] == group_b][metric_var]
                
                if len(data_a) > 1 and len(data_b) > 1:
                    # T-test
                    t_stat, p_val = ttest_ind(data_a, data_b)
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>📊 Statistical Results</h4>
                        <p><b>Group A ({group_a}):</b> n={len(data_a)}, mean={data_a.mean():.3f}, std={data_a.std():.3f}</p>
                        <p><b>Group B ({group_b}):</b> n={len(data_b)}, mean={data_b.mean():.3f}, std={data_b.std():.3f}</p>
                        <p><b>Difference:</b> <span class="metric-highlight">{data_a.mean() - data_b.mean():.3f}</span></p>
                        <p><b>t-statistic:</b> <span class="metric-highlight">{t_stat:.4f}</span></p>
                        <p><b>p-value:</b> <span class="metric-highlight">{p_val:.4f}</span></p>
                        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                            {'✓ Significant difference (p < 0.05)' if p_val < 0.05 else '✗ No significant difference'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("⚠️ Data tidak cukup")
            else:
                st.markdown("⚠️ Kurang dari 2 grup")
        
        with ab_col2:
            st.markdown("#### 📊 **Effect Size Analysis**")
            
            if len(unique_groups) >= 2 and len(data_a) > 1 and len(data_b) > 1:
                # Cohen's d
                pooled_std = np.sqrt(((len(data_a)-1)*data_a.var() + (len(data_b)-1)*data_b.var()) / 
                                    (len(data_a) + len(data_b) - 2))
                cohens_d = (data_a.mean() - data_b.mean()) / pooled_std if pooled_std > 0 else 0
                
                # Interpret effect size
                if abs(cohens_d) < 0.2:
                    effect_size = "Negligible"
                    effect_color = "#8338ec"
                elif abs(cohens_d) < 0.5:
                    effect_size = "Small"
                    effect_color = "#3a86ff"
                elif abs(cohens_d) < 0.8:
                    effect_size = "Medium"
                    effect_color = "#ffbe0b"
                else:
                    effect_size = "Large"
                    effect_color = "#ff006e"
                
                st.markdown(f"""
                <div class="glass-card">
                    <h4>📏 Cohen's d Effect Size</h4>
                    <p style="font-size: 2.5rem; text-align: center; color: {effect_color}; font-weight: 700;">
                        {cohens_d:.3f}
                    </p>
                    <p style="text-align: center; font-size: 1.1rem; color: {effect_color};">
                        <b>{effect_size} Effect</b>
                    </p>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); text-align: center; margin-top: 1rem;">
                        {'Small effect' if abs(cohens_d) < 0.5 else 'Medium effect' if abs(cohens_d) < 0.8 else 'Large effect'} 
                        - the difference between groups is 
                        {'minimal' if abs(cohens_d) < 0.5 else 'moderate' if abs(cohens_d) < 0.8 else 'substantial'}.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Visualization
                fig_effect = go.Figure()
                fig_effect.add_trace(go.Bar(
                    x=[group_a, group_b],
                    y=[data_a.mean(), data_b.mean()],
                    marker_color=[effect_color, '#8338ec'],
                    text=[f'{data_a.mean():.3f}', f'{data_b.mean():.3f}'],
                    textposition='auto'
                ))
                fig_effect.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_effect, use_container_width=True)
        
        # Rank-based Comparison
        st.markdown("### 🏆 **Rank-based Comparison**")
        
        rank_data = df_filtered.groupby(compare_var)[metric_var].mean().sort_values(ascending=False).reset_index()
        rank_data['Rank'] = range(1, len(rank_data) + 1)
        
        fig_rank = px.bar(
            rank_data,
            x=compare_var,
            y=metric_var,
            color='Rank',
            color_continuous_scale=['#06ffa5', '#ffbe0b', '#ff006e'],
            labels={metric_var: f'Average {metric_var}'}
        )
        fig_rank.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        fig_rank.update_traces(
            text=rank_data['Rank'],
            textposition='outside',
            textfont=dict(color='white', size=16, family='JetBrains Mono')
        )
        st.plotly_chart(fig_rank, use_container_width=True)
        
        st.dataframe(rank_data.style.background_gradient(cmap='YlOrRd', subset=[metric_var]))
    else:
        st.warning("⚠️ Data tidak cukup untuk comparison.")

# ===================== TAB 12: EDUCATIONAL RESOURCES =====================
with tab12:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">12</span>
        <div>
            <h2 class="section-title">Educational Resources <span class="badge-3d green">✦ LEARNING</span></h2>
            <p class="section-subtitle">Statistical formulas, concepts, and tutorials</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 **Statistical Formulas**")
    
    # Formula cards
    formula_col1, formula_col2 = st.columns(2)
    
    with formula_col1:
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Pearson Correlation</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                r = Σ((xᵢ - x̄)(yᵢ - ȳ)) / √(Σ(xᵢ - x̄)² × Σ(yᵢ - ȳ)²)
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Measures linear correlation between two variables. Range: [-1, 1]
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Standard Deviation</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                σ = √(Σ(xᵢ - x̄)² / (n - 1))
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Measures the amount of variation or dispersion in a dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Coefficient of Variation</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                CV = (σ / μ) × 100%
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Standardized measure of dispersion relative to the mean.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with formula_col2:
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Z-Score</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                z = (x - μ) / σ
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Standard score indicating how many standard deviations from the mean.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Bayes' Theorem</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                P(A|B) = P(B|A) × P(A) / P(B)
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Describes probability of an event based on prior knowledge.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-box">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Linear Regression</p>
            <p class="formula" style="font-size: 1.5rem; margin: 0.5rem 0;">
                y = β₀ + β₁x + ε
            </p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 1rem;">
                Models the relationship between a dependent variable and predictor(s).
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Concepts
    st.markdown("### 🧠 **Key Statistical Concepts**")
    
    concept_col1, concept_col2, concept_col3 = st.columns(3)
    
    with concept_col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #06ffa5;">📊 Central Limit Theorem</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                The distribution of sample means approaches a normal distribution as sample size increases,
                regardless of the population's distribution shape.
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Key Insight:</b> Allows inference about population parameters even with non-normal populations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ffbe0b;">📉 Type I & Type II Errors</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                <b>Type I Error (α):</b> Rejecting a true null hypothesis (false positive).<br>
                <b>Type II Error (β):</b> Failing to reject a false null hypothesis (false negative).
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Trade-off:</b> Reducing one type of error typically increases the other.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with concept_col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #ff006e;">🎯 Hypothesis Testing</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                A systematic procedure for testing claims about population parameters using sample data.
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Steps:</b> State H₀ and H₁ → Choose α → Calculate test statistic → Make decision.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #3a86ff;">📊 Correlation vs Causation</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                <b>Correlation:</b> Statistical association between two variables.<br>
                <b>Causation:</b> One variable directly affects another.
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Warning:</b> Correlation does not imply causation!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with concept_col3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #8338ec;">🎲 Probability Distributions</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                <b>Normal:</b> Bell curve, symmetric.<br>
                <b>Binomial:</b> Success/failure trials.<br>
                <b>Poisson:</b> Rare events over time.
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Application:</b> Each distribution models different real-world phenomena.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #fb5607;">📈 Confidence Intervals</h4>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;">
                Range of values within which the true population parameter is expected to lie,
                with a certain level of confidence (e.g., 95%).
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 1rem;">
                <b>Formula:</b> CI = x̄ ± z*(σ/√n)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tutorials
    st.markdown("### 📚 **Quick Tutorials**")
    
    tutorial_col1, tutorial_col2 = st.columns(2)
    
    with tutorial_col1:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">🎯</div>
            <div class="insight-title">How to Interpret p-values</div>
            <div class="insight-text">
                <p><b>p < 0.01:</b> Very strong evidence against H₀</p>
                <p><b>p < 0.05:</b> Strong evidence against H₀</p>
                <p><b>p < 0.10:</b> Weak evidence against H₀</p>
                <p><b>p ≥ 0.10:</b> Insufficient evidence against H₀</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">📊</div>
            <div class="insight-title">Understanding R² (R-Squared)</div>
            <div class="insight-text">
                <p>R² represents the proportion of variance in the dependent variable that's 
                predictable from the independent variable(s).</p>
                <p><b>R² = 0.75:</b> 75% of variance is explained by the model</p>
                <p><b>Range:</b> 0 to 1 (higher is better)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tutorial_col2:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">🎲</div>
            <div class="insight-title">Monte Carlo Simulation Guide</div>
            <div class="insight-text">
                <p><b>Step 1:</b> Define the problem and input distributions</p>
                <p><b>Step 2:</b> Generate random samples</p>
                <p><b>Step 3:</b> Run simulation many times (10,000+)</p>
                <p><b>Step 4:</b> Analyze results and compute statistics</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-icon">⚖️</div>
            <div class="insight-title">Choosing the Right Test</div>
            <div class="insight-text">
                <p><b>Parametric Tests (t-test, ANOVA):</b> Data is normal, equal variances</p>
                <p><b>Non-Parametric Tests (MW, KW):</b> Data is not normal or ordinal</p>
                <p><b>Correlation (Pearson):</b> Linear relationship</p>
                <p><b>Correlation (Spearman):</b> Monotonic relationship</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Resources
    st.markdown("### 📖 **Additional Resources**")
    
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #06ffa5;">📚 Recommended Learning Path</h4>
        <ol style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 2;">
            <li><b>Descriptive Statistics:</b> Mean, median, mode, standard deviation, variance</li>
            <li><b>Probability:</b> Basic concepts, distributions, Bayes' theorem</li>
            <li><b>Inferential Statistics:</b> Hypothesis testing, confidence intervals</li>
            <li><b>Correlation & Regression:</b> Linear models, correlation analysis</li>
            <li><b>Advanced Topics:</b> ANOVA, non-parametric tests, time series</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #ff006e;">💡 Best Practices</h4>
        <ul style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 2;">
            <li>✓ Always visualize your data before analysis</li>
            <li>✓ Check assumptions before applying statistical tests</li>
            <li>✓ Report effect sizes along with p-values</li>
            <li>✓ Use appropriate tests for your data type</li>
            <li>✓ Validate models with cross-validation</li>
            <li>✓ Document your methodology and assumptions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Pro Dashboard</p>
    <p class="footer-text">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Sumber Data: Kuesioner Mahasiswa (n=31) | Powered by Streamlit & Plotly 3D</p>
    <p class="footer-text" style="margin-top: 1rem; opacity: 0.6;">
        ◆ Interactive 3D Visualization ◆ AI-Powered Insights ◆ Stochastic Modeling ◆ Advanced Analytics ◆ Machine Learning ◆ Educational Resources ◆
    </p>
    <p class="footer-text" style="margin-top: 0.5rem; opacity: 0.4; font-size: 0.75rem;">
        Version 4.0 Premium Edition | © 2026 Coffee Analytics Pro
    </p>
</div>
""", unsafe_allow_html=True)
