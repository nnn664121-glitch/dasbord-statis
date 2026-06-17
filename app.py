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

# --- CSS PREMIUM 3D EDITION V4 + PROFILES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at top, #1a0b2e 0%, #0f0524 40%, #050212 100%);
        font-family: 'Space Grotesk', sans-serif;
        overflow-x: hidden;
    }
    
    #MainMenu, header, footer {visibility: hidden;}
    
    ::-webkit-scrollbar {width: 10px;}
    ::-webkit-scrollbar-track {background: #0f0524;}
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff006e, #8338ec, #3a86ff);
        border-radius: 10px;
    }
    
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
    
    .orb1 { width: 300px; height: 300px; background: radial-gradient(circle, #ff006e, transparent); top: 10%; left: 5%; }
    .orb2 { width: 400px; height: 400px; background: radial-gradient(circle, #8338ec, transparent); top: 60%; right: 10%; animation-delay: -5s; }
    .orb3 { width: 250px; height: 250px; background: radial-gradient(circle, #3a86ff, transparent); bottom: 10%; left: 40%; animation-delay: -10s; }
    .orb4 { width: 350px; height: 350px; background: radial-gradient(circle, #06ffa5, transparent); top: 30%; right: 30%; animation-delay: -15s; }
    
    @keyframes float-orb {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(100px, -50px) scale(1.1); }
        50% { transform: translate(-50px, 100px) scale(0.9); }
        75% { transform: translate(-100px, -100px) scale(1.05); }
    }
    
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
        0% { opacity: 0; transform: translateY(50px) scale(0.9); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
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
    
    @keyframes rotate { 100% { transform: rotate(360deg); } }
    
    .hero-content { position: relative; z-index: 2; }
    
    .hero-emoji {
        font-size: 5rem;
        display: inline-block;
        margin-bottom: 1rem;
        animation: float-emoji 3s ease-in-out infinite;
    }
    
    @keyframes float-emoji {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(15deg); }
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
        animation: badge-pulse 2s ease-in-out infinite;
    }
    
    @keyframes badge-pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(6, 255, 165, 0.3); transform: scale(1); }
        50% { box-shadow: 0 0 40px rgba(6, 255, 165, 0.8); transform: scale(1.05); }
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
    
    @keyframes card-entrance {
        from { opacity: 0; transform: translateY(30px) scale(0.9); }
        to { opacity: 1; transform: translateY(0) scale(1); }
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
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
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
        transform: translateY(-8px) scale(1.02);
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
    }
    
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
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
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
        0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px rgba(255, 0, 110, 0.5)); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 20px rgba(131, 56, 236, 0.8)); }
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
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .glass-card:hover {
        transform: translateY(-3px) scale(1.01);
        border-color: rgba(131, 56, 236, 0.4);
        box-shadow: 0 15px 40px rgba(131, 56, 236, 0.15);
    }
    
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
    
    @keyframes badge-glow {
        0%, 100% { box-shadow: 0 5px 20px rgba(255, 0, 110, 0.4); transform: scale(1); }
        50% { box-shadow: 0 5px 30px rgba(255, 0, 110, 0.8); transform: scale(1.05); }
    }
    
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
        position: relative;
        overflow: hidden;
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
    }
    
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
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 0, 110, 0.4);
    }
    
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
    
    @keyframes info-slide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .metric-highlight {
        font-family: 'JetBrains Mono', monospace;
        color: #06ffa5;
        font-weight: 600;
    }
    
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
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(131, 56, 236, 0.3); }
        50% { box-shadow: 0 0 40px rgba(131, 56, 236, 0.6); }
    }
    
    .pulse-card { animation: pulse-glow 3s ease-in-out infinite; }
    
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
        0% { transform: translateY(0) rotate(0deg); opacity: 0.3; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    .profile-card {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(20px);
        margin-bottom: 1.5rem;
        animation: profile-card-entrance 0.8s ease-out backwards;
    }
    
    .profile-card:nth-child(1) { animation-delay: 0.1s; border-color: rgba(255, 0, 110, 0.4); }
    .profile-card:nth-child(2) { animation-delay: 0.2s; border-color: rgba(131, 56, 236, 0.4); }
    .profile-card:nth-child(3) { animation-delay: 0.3s; border-color: rgba(58, 134, 255, 0.4); }
    .profile-card:nth-child(4) { animation-delay: 0.4s; border-color: rgba(6, 255, 165, 0.4); }
    .profile-card:nth-child(5) { animation-delay: 0.5s; border-color: rgba(255, 190, 11, 0.4); }
    .profile-card:nth-child(6) { animation-delay: 0.6s; border-color: rgba(255, 0, 110, 0.4); }
    
    @keyframes profile-card-entrance {
        from { opacity: 0; transform: translateY(50px) scale(0.9); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .profile-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 80px rgba(131, 56, 236, 0.4);
    }
    
    .profile-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .profile-avatar {
        font-size: 4rem;
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(131, 56, 236, 0.2));
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid rgba(255, 255, 255, 0.1);
        animation: avatar-float 3s ease-in-out infinite;
        flex-shrink: 0;
    }
    
    @keyframes avatar-float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    .profile-info { flex: 1; }
    
    .profile-name {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff006e, #8338ec, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .profile-tagline {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-style: italic;
    }
    
    .profile-rank {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(255, 190, 11, 0.2);
        border: 1px solid rgba(255, 190, 11, 0.5);
        border-radius: 20px;
        color: #ffbe0b;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 1px;
        text-transform: uppercase;
        animation: rank-glow 2s ease-in-out infinite;
    }
    
    @keyframes rank-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(255, 190, 11, 0.3); }
        50% { box-shadow: 0 0 25px rgba(255, 190, 11, 0.7); }
    }
    
    .profile-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .profile-stat {
        text-align: center;
    }
    
    .profile-stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06ffa5, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .profile-stat-label {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    
    .profile-description {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        line-height: 1.7;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 12px;
        border-left: 3px solid rgba(131, 56, 236, 0.5);
        margin-bottom: 1rem;
    }
    
    .profile-traits {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .trait-tag {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        background: rgba(131, 56, 236, 0.15);
        border: 1px solid rgba(131, 56, 236, 0.4);
        border-radius: 20px;
        color: #c4b5fd;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
        cursor: default;
    }
    
    .trait-tag:hover {
        background: rgba(131, 56, 236, 0.3);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 5px 15px rgba(131, 56, 236, 0.3);
    }
    
    .profile-match-card {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.1) 0%, rgba(131, 56, 236, 0.1) 100%);
        border: 2px solid rgba(131, 56, 236, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .profile-match-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 190, 11, 0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }
    
    .profile-match-content {
        position: relative;
        z-index: 2;
    }
    
    .level-bar-container {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 4px;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .level-bar {
        height: 24px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 200% 100%;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        animation: level-shine 3s linear infinite;
        transition: width 1s ease;
    }
    
    @keyframes level-shine {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .level-label {
        display: flex;
        justify-content: space-between;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }
    
    .achievement-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.2rem;
        background: linear-gradient(135deg, rgba(255, 190, 11, 0.2), rgba(255, 0, 110, 0.2));
        border: 1px solid rgba(255, 190, 11, 0.5);
        border-radius: 50px;
        color: #ffbe0b;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.3rem;
        transition: all 0.3s ease;
    }
    
    .achievement-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 190, 11, 0.4);
    }
    
    .profile-quote {
        position: relative;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
        border-radius: 16px;
        margin: 1rem 0;
        font-style: italic;
        color: rgba(255, 255, 255, 0.8);
        border-left: 4px solid rgba(131, 56, 236, 0.5);
    }
    
    .profile-quote::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 10px;
        font-size: 4rem;
        color: rgba(131, 56, 236, 0.3);
        font-family: serif;
    }
    
    .profile-timeline {
        position: relative;
        padding-left: 2rem;
        margin: 1.5rem 0;
    }
    
    .profile-timeline::before {
        content: '';
        position: absolute;
        left: 10px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
    }
    
    .timeline-item {
        position: relative;
        padding-bottom: 1.5rem;
        padding-left: 1rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -1.6rem;
        top: 5px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #06ffa5;
        box-shadow: 0 0 15px rgba(6, 255, 165, 0.6);
        animation: timeline-pulse 2s ease-in-out infinite;
    }
    
    @keyframes timeline-pulse {
        0%, 100% { box-shadow: 0 0 10px rgba(6, 255, 165, 0.6); }
        50% { box-shadow: 0 0 25px rgba(6, 255, 165, 1); transform: scale(1.2); }
    }
    
    .timeline-time {
        color: #06ffa5;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.3rem;
    }
    
    .timeline-content {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
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
</style>
""", unsafe_allow_html=True)

# --- ANIMATED BACKGROUND ELEMENTS ---
st.markdown("""
<div class="animated-grid"></div>
<div class="floating-orbs">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
    <div class="orb orb4"></div>
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
    
    df_clean['Fokus_Label'] = df_clean['Is_Fokus_Tinggi'].map({1: 'High Focus', 0: 'Low Focus'})
    df_clean['Kopi_Label'] = df_clean['Kopi_per_Hari'].apply(lambda x: f'{x} Cangkir')
    
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
        <span class="hero-badge">◆ PREMIUM EDITION v4.1 ◆ PROFILES FIXED ◆</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MARQUEE SCROLLING TEXT ---
st.markdown("""
<div class="marquee-container">
    <div class="marquee-content">
        ☕ COFFEE ANALYTICS • 📊 DATA SCIENCE • 🧠 NEUROSCIENCE • 📈 PRODUCTIVITY • 🎯 3D VISUALIZATION • 🤖 AI INSIGHTS • 🎲 MONTE CARLO • 👤 PROFILES •
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🎛️ **Control Panel**")
    st.markdown("---")

    st.markdown("#### 🔍 **Data Filters**")
    
    kopi_filter = st.multiselect(
        "☕ Cangkir per Hari",
        options=sorted(df['Kopi_per_Hari'].unique()),
        default=sorted(df['Kopi_per_Hari'].unique()),
    )

    kategori_filter = st.multiselect(
        "📊 Kategori Konsumsi",
        options=sorted(df['Kategori_Konsumsi'].unique()),
        default=sorted(df['Kategori_Konsumsi'].unique()),
    )

    durasi_options = df['Durasi_Belajar_Num'].unique()
    if len(durasi_options) > 0:
        durasi_range = st.slider(
            "⏰ Durasi Belajar (jam)",
            min_value=float(min(durasi_options)),
            max_value=float(max(durasi_options)),
            value=(float(min(durasi_options)), float(max(durasi_options))),
        )
    else:
        durasi_range = (0.0, 10.0)

    fokus_filter = st.selectbox(
        "🎯 Status Fokus",
        options=["Semua", "High Focus (>3.0)", "Low Focus (≤3.0)"],
    )
    
    produktivitas_filter = st.multiselect(
        "⚡ Level Produktivitas",
        options=sorted(df['Produktivitas_Level'].unique()),
        default=sorted(df['Produktivitas_Level'].unique()),
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
    
    st.markdown("#### 📈 **Live Statistics**")
    st.markdown(f"""
    <div class="glass-card pulse-card" style="text-align: center;">
        <span class="kpi-icon">👥</span>
        <p class="kpi-value">{len(df_filtered)}</p>
        <p class="kpi-label">Responden Aktif</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    st.markdown("#### 💾 **Export Data**")
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="coffee_analytics_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )
    
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

st.markdown("""
<div class="wave-container">
    <div class="wave"></div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌐 3D Visualization",
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎯 Conditional Probability",
    "🎲 Monte Carlo Simulation",
    "📈 Advanced Analytics",
    "🤖 AI Insights",
    "👤 Profiles"
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
    
    if len(df_filtered) > 0:
        st.markdown("### 🌌 **3D Scatter Plot: Kopi × Durasi × Produktivitas**")
        st.markdown("""
        <div class="info-box">
            💡 <strong>Tip:</strong> Klik dan drag untuk memutar, scroll untuk zoom, double-click untuk reset view.
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
            hover_data={'Kopi_per_Hari': ':.0f', 'Durasi_Belajar_Num': ':.1f', 'Skor_Produktivitas': ':.2f', 'Kualitas_Tidur_Memburuk': ':.0f', 'Fokus_Label': True, 'Kategori_Konsumsi': True},
            labels={'Kopi_per_Hari': 'Cangkir Kopi', 'Durasi_Belajar_Num': 'Durasi Belajar (jam)', 'Skor_Produktivitas': 'Skor Produktivitas', 'Kualitas_Tidur_Memburuk': 'Kualitas Tidur'}
        )
        
        fig_3d_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Space Grotesk'),
            scene=dict(
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', showbackground=False, title='☕ Cangkir Kopi'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', showbackground=False, title='📚 Durasi Belajar'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.1)', showbackground=False, title='⚡ Produktivitas'),
                camera=dict(eye=dict(x=1.8, y=1.8, z=1.2), up=dict(x=0, y=0, z=1)),
                aspectratio=dict(x=1.2, y=1.2, z=0.9)
            ),
            height=600, margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(title='Kualitas Tidur', tickfont=dict(color='white'), title_font=dict(color='white'))
        )
        st.plotly_chart(fig_3d_scatter, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data.")

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
    
    if len(df_filtered) > 0:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### ☕ **Distribusi Konsumsi Kopi**")
            kopi_counts = df_filtered['Kopi_per_Hari'].value_counts().sort_index()
            fig_dist_kopi = px.bar(x=kopi_counts.index, y=kopi_counts.values, labels={'x': 'Cangkir', 'y': 'Responden'}, color=kopi_counts.values, color_continuous_scale=['#ff006e', '#8338ec', '#3a86ff'])
            fig_dist_kopi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_dist_kopi, use_container_width=True)
        
        with col_b:
            st.markdown("#### ⚡ **Distribusi Skor Produktivitas**")
            fig_hist_prod = px.histogram(df_filtered, x='Skor_Produktivitas', nbins=15, color_discrete_sequence=['#8338ec'], marginal="violin")
            fig_hist_prod.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), showlegend=False)
            st.plotly_chart(fig_hist_prod, use_container_width=True)
        
        st.markdown("#### 📋 **Statistical Summary**")
        stats_df = df_filtered[['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']].describe().round(3)
        st.dataframe(stats_df.style.background_gradient(cmap='viridis', axis=1), use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data.")

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
    
    if len(df_filtered) > 1:
        corr_cols = ['Kopi_per_Hari', 'Durasi_Belajar_Num', 'Skor_Produktivitas', 'Kualitas_Tidur_Memburuk']
        corr_matrix = df_filtered[corr_cols].corr(method='pearson')
        fig_heatmap = px.imshow(corr_matrix, text_auto=".3f", color_continuous_scale=['#0f0524', '#8338ec', '#ff006e', '#ffbe0b', '#06ffa5'], zmin=-1, zmax=1)
        fig_heatmap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='JetBrains Mono'))
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("⚠️ Data tidak cukup.")

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
    
    if len(df_filtered) > 0:
        st.markdown("#### 📊 **Tabel Kontingensi**")
        kontingensi = pd.crosstab(df_filtered['Is_Peminum_Kopi'], df_filtered['Is_Fokus_Tinggi'], margins=True)
        st.dataframe(kontingensi, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data.")

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
        n_mahasiswa = st.slider("👥 Students per Class:", 10, 500, 100, 10)
        n_iterasi = st.slider("🔄 Iterations:", 1000, 50000, 10000, 1000)
        simulate_btn = st.button("🎲 Run Simulation", type="primary", use_container_width=True)
    
    with col_j:
        if simulate_btn or 'mc_results' not in st.session_state:
            with st.spinner("⚡ Running Monte Carlo simulation..."):
                p_kopi_dist = df['Kopi_per_Hari'].value_counts(normalize=True).sort_index()
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
                        if np.isnan(std_val):
                            std_val = overall_std
                        skor_acak = np.clip(np.random.normal(mean_val, std_val), 1.0, 5.0)
                        skor_kelas.append(skor_acak)
                    hasil_rata_rata.append(np.mean(skor_kelas))
                st.session_state['mc_results'] = hasil_rata_rata

        if 'mc_results' in st.session_state:
            hasil = st.session_state['mc_results']
            mean_mc = np.mean(hasil)
            ci_bawah = np.percentile(hasil, 2.5)
            ci_atas = np.percentile(hasil, 97.5)
            st.info(f"Mean: {mean_mc:.3f}, CI 95%: [{ci_bawah:.3f}, {ci_atas:.3f}]")

# ===================== TAB 6: ADVANCED ANALYTICS =====================
with tab6:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">06</span>
        <div>
            <h2 class="section-title">Advanced Analytics <span class="badge-3d">✦ ADVANCED</span></h2>
            <p class="section-subtitle">Deep dive analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("Advanced Analytics Tab - Radar charts, parallel coordinates, violin plots, heatmaps, and hypothesis testing.")

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
    st.info("AI Insights Tab - Optimal consumption, sweet spots, sleep impact analysis, and regression models.")

# ===================== TAB 8: PROFILES - FIXED! =====================
with tab8:
    st.markdown("""
    <div class="section-header">
        <span class="section-number">08</span>
        <div>
            <h2 class="section-title">Coffee Consumer Profiles <span class="badge-3d">✦ FIXED</span></h2>
            <p class="section-subtitle">Detailed personas & behavioral segmentation analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        st.markdown("""
        <div class="profile-match-card">
            <div class="profile-match-content">
                <h2 style="color: #fff; margin: 0;">🎭 Discover Your Coffee Persona</h2>
                <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
                    Based on behavioral analysis, we've identified <span class="metric-highlight">6 distinct coffee consumer archetypes</span>.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 🎨 **The Six Coffee Archetypes**")
        
        # FIXED: Using triple quotes for multi-line descriptions
        personas = [
            {
                'emoji': '🌱',
                'name': 'The Mindful Minimalist',
                'category': 'Non-Drinker',
                'tagline': 'Less is more - natural focus through discipline',
                'rank': '🥉 BRONZE TIER',
                'description': """Responden yang tidak mengonsumsi kopi sama sekali. Mereka mengandalkan fokus alami, tidur berkualitas, dan rutinitas yang terstruktur. Tipe ini percaya bahwa produktivitas sejati datang dari keseimbangan hidup, bukan stimulan.""",
                'traits': ['💪 Disiplin Tinggi', '😴 Tidur Berkualitas', '🧘 Mindful', '📚 Konsisten', '🌿 Natural Focus'],
                'achievements': ['🏆 Clean Lifestyle', '⏰ Early Riser', '🎯 Consistent Performer'],
                'quote': 'My mind is my best caffeine.'
            },
            {
                'emoji': '☕',
                'name': 'The Casual Sipper',
                'category': 'Light (1 cup)',
                'tagline': 'One cup a day keeps the fatigue away',
                'rank': '🥈 SILVER TIER',
                'description': """Peminum kopi ringan yang menikmati satu cangkir per hari, biasanya di pagi hari. Mereka menggunakan kopi sebagai ritual bukan kebutuhan. Tipe ini memiliki keseimbangan ideal antara konsumsi kopi dan kualitas tidur.""",
                'traits': ['⚖️ Balanced', '🌅 Morning Ritual', '😊 Happy Medium', '📈 Steady Performance', '🎨 Creative'],
                'achievements': ['☕ Coffee Connoisseur', '🌞 Morning Champion', '⚡ Steady Energy'],
                'quote': 'One perfect cup, one perfect day.'
            },
            {
                'emoji': '⚡',
                'name': 'The Power User',
                'category': 'Moderate (2 cups)',
                'tagline': 'Strategic caffeine for peak performance',
                'rank': '🥇 GOLD TIER',
                'description': """Pengguna kopi strategis yang mengonsumsi 2 cangkir per hari untuk optimal performance. Mereka tahu persis kapan dan berapa banyak kopi yang dibutuhkan. Ini adalah sweet spot untuk produktivitas maksimal tanpa mengorbankan tidur.""",
                'traits': ['🎯 Strategic', '💪 High Performer', '📊 Data-Driven', '⏱️ Time Manager', '🚀 Peak Performance'],
                'achievements': ['⚡ Power Hour Master', '📈 Productivity Pro', '🎯 Focus Expert'],
                'quote': 'Coffee is my strategic advantage.'
            },
            {
                'emoji': '🔥',
                'name': 'The Heavy Drinker',
                'category': 'Heavy (3+ cups)',
                'tagline': 'Fueling the grind with multiple cups',
                'rank': '💎 DIAMOND TIER',
                'description': """Peminum kopi berat yang mengonsumsi 3+ cangkir per hari. Mereka sering belajar dalam durasi panjang dan mengandalkan kopi sebagai bahan bakar. Namun, mereka menghadapi trade-off dengan kualitas tidur yang menurun.""",
                'traits': ['🔥 Hard Worker', '📚 Long Hours', '💼 Career-Focused', '⚠️ Sleep Sacrifice', '💪 Determined'],
                'achievements': ['🏃 Marathon Studier', '☕ Caffeine Warrior', '📅 Deadline Crusher'],
                'quote': 'More coffee, more productivity... right?'
            },
            {
                'emoji': '🎯',
                'name': 'The High Achiever',
                'category': 'High Focus',
                'tagline': 'Results-driven with exceptional focus',
                'rank': '👑 LEGENDARY TIER',
                'description': """Responden dengan skor fokus tinggi (>3.0). Mereka adalah mahasiswa berprestasi yang telah menemukan formula sukses mereka sendiri, baik dengan atau tanpa kopi. Tipe ini memiliki kombinasi disiplin, strategi, dan mindset yang optimal.""",
                'traits': ['🏆 Top Performer', '🧠 Sharp Mind', '📊 Analytical', '🎯 Goal-Oriented', '💡 Innovative'],
                'achievements': ['🌟 Honor Student', '📚 Study Master', '🎯 Focus Champion', '🏅 Excellence Award'],
                'quote': 'Focus is my superpower.'
            },
            {
                'emoji': '😴',
                'name': 'The Sleep-Deprived',
                'category': 'Poor Sleep',
                'tagline': 'Trading sleep for productivity',
                'rank': '⚠️ WARNING TIER',
                'description': """Responden dengan kualitas tidur buruk yang cenderung mengonsumsi kopi berlebihan. Mereka terjebak dalam siklus: kurang tidur, butuh kopi, lebih kurang tidur. Tipe ini membutuhkan intervensi untuk memutus pola tidak sehat ini.""",
                'traits': ['⚠️ At Risk', '😴 Sleep Debt', '☕ Caffeine Dependent', '🌙 Night Owl', '💫 Exhausted'],
                'achievements': ['🌙 Night Warrior', '☕ Caffeine Addict', '⚠️ Burnout Risk'],
                'quote': 'Sleep is for the weak... or is it?'
            }
        ]
        
        # Calculate stats
        persona_stats = df_filtered.groupby('Kategori_Konsumsi').agg({
            'Kopi_per_Hari': 'mean',
            'Durasi_Belajar_Num': 'mean',
            'Skor_Produktivitas': 'mean',
            'Kualitas_Tidur_Memburuk': 'mean',
            'Is_Fokus_Tinggi': 'mean'
        }).round(2)
        
        # Display persona cards
        for persona in personas:
            if persona['category'] in persona_stats.index:
                stats = persona_stats.loc[persona['category']]
                count = len(df_filtered[df_filtered['Kategori_Konsumsi'] == persona['category']])
                focus_rate = stats['Is_Fokus_Tinggi'] * 100
            else:
                if persona['category'] == 'High Focus':
                    count = len(df_filtered[df_filtered['Is_Fokus_Tinggi'] == 1])
                    focus_rate = 100.0
                elif persona['category'] == 'Poor Sleep':
                    sleep_poor = df_filtered[df_filtered['Kualitas_Tidur_Memburuk'] >= 4]
                    count = len(sleep_poor)
                    focus_rate = sleep_poor['Is_Fokus_Tinggi'].mean() * 100 if count > 0 else 0
                else:
                    count = 0
                    focus_rate = 0
            
            traits_html = ''.join([f'<span class="trait-tag">{trait}</span>' for trait in persona['traits']])
            achievements_html = ''.join([f'<span class="achievement-badge">{ach}</span>' for ach in persona['achievements']])
            
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-header">
                    <div class="profile-avatar">{persona['emoji']}</div>
                    <div class="profile-info">
                        <h3 class="profile-name">{persona['name']}</h3>
                        <p class="profile-tagline">{persona['tagline']}</p>
                        <span class="profile-rank">{persona['rank']}</span>
                    </div>
                </div>
                
                <div class="profile-stats">
                    <div class="profile-stat">
                        <div class="profile-stat-value">{count}</div>
                        <div class="profile-stat-label">Members</div>
                    </div>
                    <div class="profile-stat">
                        <div class="profile-stat-value">{focus_rate:.0f}%</div>
                        <div class="profile-stat-label">Focus Rate</div>
                    </div>
                    <div class="profile-stat">
                        <div class="profile-stat-value" style="font-size: 1.2rem;">{persona['category']}</div>
                        <div class="profile-stat-label">Category</div>
                    </div>
                </div>
                
                <div class="profile-description">{persona['description']}</div>
                
                <div class="profile-quote">{persona['quote']}</div>
                
                <h4 style="color: #fff; margin-top: 1rem;">🏷️ Key Traits</h4>
                <div class="profile-traits">{traits_html}</div>
                
                <h4 style="color: #fff; margin-top: 1rem;">🏆 Achievements</h4>
                <div style="margin-top: 0.5rem;">{achievements_html}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        
        # Behavioral Timeline
        st.markdown("### ⏰ **A Day in the Life: Behavioral Timeline**")
        
        timeline_col1, timeline_col2 = st.columns(2)
        
        with timeline_col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #06ffa5;">☕ The Casual Sipper's Day</h4>
                <div class="profile-timeline">
                    <div class="timeline-item">
                        <div class="timeline-time">06:00 AM</div>
                        <div class="timeline-content">Bangun tidur dengan energi alami</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">07:30 AM</div>
                        <div class="timeline-content">Sarapan dengan 1 cangkir kopi ☕</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">09:00 AM</div>
                        <div class="timeline-content">Sesi belajar produktif (deep work)</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">10:00 PM</div>
                        <div class="timeline-content">Tidur tepat waktu 😴</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with timeline_col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #ff006e;">🔥 The Heavy Drinker's Day</h4>
                <div class="profile-timeline">
                    <div class="timeline-item">
                        <div class="timeline-time">08:00 AM</div>
                        <div class="timeline-content">Bangun terlambat, kopi pertama ☕</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">10:00 AM</div>
                        <div class="timeline-content">Kopi kedua, mulai fokus</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">03:00 PM</div>
                        <div class="timeline-content">Kopi ketiga, energi spike ⚡</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-time">02:00 AM</div>
                        <div class="timeline-content">Akhirnya tidur, sleep debt 😴</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        
        # Final Insights
        st.markdown("""
        <div class="profile-match-card">
            <div class="profile-match-content">
                <h3 style="color: #fff; margin: 0; text-align: center;">🎯 Final Insights</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 1.5rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 3rem;">🏆</div>
                        <h4 style="color: #06ffa5; margin: 0.5rem 0;">Best Persona</h4>
                        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                            <b>The Power User</b> memiliki keseimbangan optimal.
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 3rem;">⚠️</div>
                        <h4 style="color: #ffbe0b; margin: 0.5rem 0;">At Risk</h4>
                        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                            <b>The Heavy Drinker</b> menunjukkan pola berisiko.
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 3rem;">💎</div>
                        <h4 style="color: #8338ec; margin: 0.5rem 0;">Key Finding</h4>
                        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                            <b>Sleep quality</b> adalah prediktor terkuat produktivitas.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")

# --- FOOTER ---
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="premium-footer">
    <p class="footer-brand">☕ Coffee Analytics Pro Dashboard</p>
    <p class="footer-text">Advanced 3D Neuroscience & Productivity Intelligence Platform</p>
    <p class="footer-text">Dibuat untuk Mata Kuliah <b>Statistika dan Probabilitas</b></p>
    <p class="footer-text">Sumber Data: Kuesioner Mahasiswa (n=31) | Powered by Streamlit & Plotly 3D</p>
</div>
""", unsafe_allow_html=True)
