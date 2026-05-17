import warnings
warnings.filterwarnings("ignore")

import sys
import os
import datetime
sys.path.append(os.path.dirname(__file__))

import streamlit as st

from modules.gaussian import gaussian_page
from modules.laser_simulation import laser_page
from modules.cavity_losses import cavity_page
from modules.navier_stokes import navier_stokes_page
from modules.data_science import data_science_page
from modules.energy import energy_page
from modules.numerisation_hub import numerisation_hub_page
from modules.integration import integration_page
from modules.interpolation import interpolation_page
from modules.equ_diff import equ_diff_page
from modules.signal_analysis import signal_page
from modules.optimisation import optimisation_page
from modules.automatique import automatique_page

st.set_page_config(
    page_title="SciPRO — Calcul Scientifique",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Page background ── */
    .stApp {
        background: #f0f4f8;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0a1628 !important;
        border-right: 1px solid #1e3a5f;
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        transition: background 0.15s ease !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(248, 250, 252, 0.07) !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
        color: #64748b !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        margin-top: 12px !important;
        margin-bottom: 4px !important;
    }

    /* ── Main content area ── */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* ── Header bar ── */
    .sci-header {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .sci-header-left { display: flex; align-items: center; gap: 14px; }
    .sci-logo {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        border-radius: 9px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px; flex-shrink: 0;
    }
    .sci-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; line-height: 1.2; }
    .sci-subtitle { font-size: 0.75rem; color: #64748b; }
    .sci-badge {
        background: #eff6ff; color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 4px 10px; border-radius: 99px;
        font-size: 0.72rem; font-weight: 600;
    }
    .sci-status {
        display: flex; align-items: center; gap: 6px;
        font-size: 0.78rem; color: #16a34a;
    }
    .sci-status-dot {
        width: 7px; height: 7px;
        background: #22c55e; border-radius: 50%;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0%, 100% { opacity: 1; } 50% { opacity: 0.4; }
    }

    /* ── Metric cards ── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }
    .metric-card.blue::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .metric-card.indigo::before { background: linear-gradient(90deg, #6366f1, #818cf8); }
    .metric-card.amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .metric-card.emerald::before{ background: linear-gradient(90deg, #10b981, #34d399); }
    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 500;
    }
    .metric-sub {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* ── Module cards grid ── */
    .modules-section-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin: 24px 0 12px 0;
    }
    .module-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
    }
    .module-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.15s ease;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .module-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59,130,246,0.12);
        transform: translateY(-1px);
    }
    .module-card-icon {
        width: 36px; height: 36px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .module-card-icon.physics  { background: #eff6ff; }
    .module-card-icon.math     { background: #f5f3ff; }
    .module-card-icon.data     { background: #ecfdf5; }
    .module-card-name {
        font-size: 0.82rem;
        font-weight: 600;
        color: #1e293b;
    }
    .module-card-desc {
        font-size: 0.71rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* ── Recent activity ── */
    .activity-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .activity-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .activity-item:last-child { border-bottom: none; }
    .activity-dot {
        width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }
    .activity-text { font-size: 0.82rem; color: #334155; }
    .activity-time { font-size: 0.72rem; color: #94a3b8; margin-left: auto; }

    /* ── Page content titles ── */
    .page-title-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .page-title-icon { font-size: 1.2rem; }
    .page-title-text { font-size: 1rem; font-weight: 700; color: #0f172a; }
    .page-breadcrumb { font-size: 0.75rem; color: #94a3b8; margin-left: auto; }

    /* ── Streamlit widget overrides ── */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stButton button {
        background: #1d4ed8 !important;
        color: white !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 8px 18px !important;
        transition: background 0.15s ease !important;
    }
    .stButton button:hover {
        background: #1e40af !important;
    }
    .stSelectbox select, .stNumberInput input, .stTextInput input {
        border-radius: 7px !important;
        border-color: #e2e8f0 !important;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Inter', sans-serif !important;
    }
    h1 { font-size: 1.4rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.15rem !important; font-weight: 600 !important; }
    h3 { font-size: 1rem !important; font-weight: 600 !important; }

    /* ── Expander styling ── */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ── Divider ── */
    hr { border-color: #e2e8f0 !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 8px !important;
        padding: 3px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        color: #1d4ed8 !important;
    }

    /* ── Info / warning / error boxes ── */
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        font-size: 0.85rem !important;
    }

    /* ── Sidebar logo area ── */
    .sidebar-logo {
        padding: 0 0 20px 0;
        border-bottom: 1px solid #1e3a5f;
        margin-bottom: 16px;
    }
    .sidebar-logo-icon {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 6px;
    }
    .sidebar-logo-name {
        font-size: 1rem;
        font-weight: 700;
        color: #f1f5f9 !important;
    }
    .sidebar-logo-sub {
        font-size: 0.7rem;
        color: #64748b !important;
        margin-top: 2px;
    }
    .sidebar-section-label {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #475569 !important;
        padding: 14px 0 4px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header():
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">🔬</span>
        <div class="sidebar-logo-name">SciPRO</div>
        <div class="sidebar-logo-sub">Calcul Scientifique v2.0</div>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(icon, title, module_group=""):
    st.markdown(f"""
    <div class="page-title-bar">
        <span class="page-title-icon">{icon}</span>
        <span class="page-title-text">{title}</span>
        <span class="page-breadcrumb">SciPRO › {module_group or title}</span>
    </div>
    """, unsafe_allow_html=True)

def show_home():
    now = datetime.datetime.now()

    if "session_start" not in st.session_state:
        st.session_state["session_start"] = now
    if "sim_count" not in st.session_state:
        st.session_state["sim_count"] = 0
    if "last_module" not in st.session_state:
        st.session_state["last_module"] = "—"
    if "visited_modules" not in st.session_state:
        st.session_state["visited_modules"] = []

    session_duration = int((now - st.session_state["session_start"]).total_seconds() / 60)

    st.markdown(f"""
    <div class="sci-header">
        <div class="sci-header-left">
            <div class="sci-logo">🔬</div>
            <div>
                <div class="sci-title">Application de Calcul Scientifique PRO</div>
                <div class="sci-subtitle">Plateforme de simulation et d'analyse numérique</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:12px;">
            <span class="sci-badge">v2.0</span>
            <div class="sci-status">
                <div class="sci-status-dot"></div>
                Système opérationnel
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card blue">
            <div class="metric-icon">📦</div>
            <div class="metric-value">13</div>
            <div class="metric-label">Modules disponibles</div>
            <div class="metric-sub">Physique · Maths · Data</div>
        </div>
        <div class="metric-card indigo">
            <div class="metric-icon">⚡</div>
            <div class="metric-value">{st.session_state['sim_count']}</div>
            <div class="metric-label">Simulations cette session</div>
            <div class="metric-sub">Depuis {st.session_state['session_start'].strftime('%H:%M')}</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-icon">🕐</div>
            <div class="metric-value">{session_duration}<span style="font-size:1rem;font-weight:400;color:#64748b">min</span></div>
            <div class="metric-label">Durée de session</div>
            <div class="metric-sub">{now.strftime('%d %b %Y, %H:%M')}</div>
        </div>
        <div class="metric-card emerald">
            <div class="metric-icon">🗂️</div>
            <div class="metric-value">{max(len(st.session_state['visited_modules']), 0)}</div>
            <div class="metric-label">Modules visités</div>
            <div class="metric-sub">Dernier : {st.session_state['last_module']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modules-section-title">⚛️ Physique & Simulation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="module-grid">
        <div class="module-card">
            <div class="module-card-icon physics">📈</div>
            <div>
                <div class="module-card-name">Profil Gaussien</div>
                <div class="module-card-desc">Distribution gaussienne, μ, σ</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon physics">🔦</div>
            <div>
                <div class="module-card-name">Simulation Laser</div>
                <div class="module-card-desc">Modes TEM, cavité optique</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon physics">🪞</div>
            <div>
                <div class="module-card-name">Pertes de Cavité</div>
                <div class="module-card-desc">Transmission, absorption</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon physics">🌊</div>
            <div>
                <div class="module-card-name">Navier-Stokes</div>
                <div class="module-card-desc">Mécanique des fluides</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modules-section-title">📐 Mathématiques Numériques</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="module-grid">
        <div class="module-card">
            <div class="module-card-icon math">∫</div>
            <div>
                <div class="module-card-name">Intégration</div>
                <div class="module-card-desc">Simpson, Gauss, Trapèzes</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon math">〜</div>
            <div>
                <div class="module-card-name">Interpolation</div>
                <div class="module-card-desc">Lagrange, Newton, Splines</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon math">∂</div>
            <div>
                <div class="module-card-name">Éq. Différentielles</div>
                <div class="module-card-desc">RK4, Euler, Midpoint</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon math">⚙️</div>
            <div>
                <div class="module-card-name">Optimisation</div>
                <div class="module-card-desc">Gradient, PuLP, linéaire</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon math">🔢</div>
            <div>
                <div class="module-card-name">Hub Numérisation</div>
                <div class="module-card-desc">Algorithmes numériques</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modules-section-title">📊 Data Science & Signal</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="module-grid">
        <div class="module-card">
            <div class="module-card-icon data">📊</div>
            <div>
                <div class="module-card-name">Data Science</div>
                <div class="module-card-desc">ML, régression, clustering</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon data">⚡</div>
            <div>
                <div class="module-card-name">Énergie</div>
                <div class="module-card-desc">Analyse données énergétiques</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon data">〰️</div>
            <div>
                <div class="module-card-name">Analyse Signal</div>
                <div class="module-card-desc">FFT, filtres, spectre</div>
            </div>
        </div>
        <div class="module-card">
            <div class="module-card-icon data">🤖</div>
            <div>
                <div class="module-card-name">Automatique</div>
                <div class="module-card-desc">Systèmes, Bode, Nyquist</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["visited_modules"]:
        st.markdown('<div class="modules-section-title">🕐 Activité récente</div>', unsafe_allow_html=True)
        items_html = ""
        colors = ["#3b82f6", "#6366f1", "#f59e0b", "#10b981", "#ef4444"]
        for i, (mod, ts) in enumerate(reversed(st.session_state["visited_modules"][-5:])):
            color = colors[i % len(colors)]
            items_html += f"""
            <div class="activity-item">
                <div class="activity-dot" style="background:{color}"></div>
                <div class="activity-text">{mod}</div>
                <div class="activity-time">{ts}</div>
            </div>"""
        st.markdown(f'<div class="activity-card">{items_html}</div>', unsafe_allow_html=True)

def show_about():
    st.markdown("""
    <style>
    .about-hero {
        background: linear-gradient(135deg, #0a1628 0%, #0f2040 60%, #0d2a5e 100%);
        border-radius: 16px; padding: 48px 40px; margin-bottom: 24px;
        position: relative; overflow: hidden;
    }
    .about-hero::before {
        content: '';
        position: absolute; inset: 0; border-radius: 16px;
        background: radial-gradient(ellipse 70% 50% at 50% 0%, rgba(59,130,246,0.2) 0%, transparent 70%);
    }
    .about-hero-content { position: relative; }
    .about-avatar {
        width: 80px; height: 80px; border-radius: 50%;
        background: linear-gradient(135deg, #1d4ed8, #6366f1);
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(29,78,216,0.4);
    }
    .about-name { font-size: 1.8rem; font-weight: 800; color: #fff; margin-bottom: 6px; }
    .about-role { font-size: 1rem; color: #60a5fa; font-weight: 600; margin-bottom: 20px; }
    .about-contacts { display: flex; gap: 16px; flex-wrap: wrap; }
    .about-contact {
        display: flex; align-items: center; gap: 8px;
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px; padding: 8px 14px;
        font-size: 0.85rem; color: #94a3b8; text-decoration: none;
        transition: background .15s;
    }
    .about-contact:hover { background: rgba(255,255,255,0.1); color: #e2e8f0; }
    .about-section-title {
        font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.1em; color: #64748b; margin-bottom: 16px; margin-top: 8px;
    }
    .about-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 24px; margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .about-module-chip {
        display: inline-flex; align-items: center; gap: 6px;
        background: #f1f5f9; border: 1px solid #e2e8f0;
        border-radius: 6px; padding: 5px 12px;
        font-size: 0.78rem; font-weight: 500; color: #334155;
        margin: 4px;
    }
    .about-tech-chip {
        display: inline-flex; align-items: center; gap: 6px;
        background: #eff6ff; border: 1px solid #bfdbfe;
        border-radius: 6px; padding: 5px 12px;
        font-size: 0.78rem; font-weight: 600; color: #1d4ed8;
        margin: 4px;
    }
    .about-stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 24px; }
    .about-stat {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
        padding: 16px; text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .about-stat-val { font-size: 1.8rem; font-weight: 800; color: #0f172a; line-height: 1; }
    .about-stat-label { font-size: 0.72rem; color: #64748b; margin-top: 4px; }
    </style>
    <div class="about-hero">
      <div class="about-hero-content">
        <div class="about-avatar">👨‍💻</div>
        <div class="about-name">Adama Gueye</div>
        <div class="about-role">Ingénieur Calcul Scientifique &amp; Data Science</div>
        <div class="about-contacts">
          <span class="about-contact">✉️&nbsp; adama.gueye.3304@gmail.com</span>
          <span class="about-contact">📱&nbsp; +221 77 780 41 63</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-section-title">📊 En chiffres</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-stat-grid">
      <div class="about-stat"><div class="about-stat-val">13</div><div class="about-stat-label">Modules</div></div>
      <div class="about-stat"><div class="about-stat-val">3</div><div class="about-stat-label">Domaines</div></div>
      <div class="about-stat"><div class="about-stat-val">8</div><div class="about-stat-label">Librairies</div></div>
      <div class="about-stat"><div class="about-stat-val">v2.0</div><div class="about-stat-label">Version</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="about-section-title">🔬 À propos de l\'application</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
          <p style="font-size:0.88rem;color:#334155;line-height:1.7;margin-bottom:14px;">
            <strong>SciPRO</strong> est une plateforme de calcul scientifique professionnelle développée en Python avec Streamlit.
            Elle réunit 13 modules spécialisés couvrant la physique, les mathématiques numériques et la data science dans une interface moderne et intuitive.
          </p>
          <p style="font-size:0.88rem;color:#64748b;line-height:1.7;">
            Chaque module propose des paramètres interactifs, des visualisations en temps réel et des algorithmes de référence — 
            sans nécessiter aucune installation ni connaissance en programmation.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="about-section-title">⚙️ Stack technologique</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
          <span class="about-tech-chip">🐍 Python 3</span>
          <span class="about-tech-chip">🎈 Streamlit</span>
          <span class="about-tech-chip">📐 NumPy</span>
          <span class="about-tech-chip">📉 SciPy</span>
          <span class="about-tech-chip">📊 Matplotlib</span>
          <span class="about-tech-chip">🤖 Scikit-learn</span>
          <span class="about-tech-chip">🐼 Pandas</span>
          <span class="about-tech-chip">🎨 Seaborn</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="about-section-title">📦 Modules disponibles</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="about-card">
          <div style="margin-bottom:10px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;">⚛️ Physique</div>
          <span class="about-module-chip">📈 Profil Gaussien</span>
          <span class="about-module-chip">🔦 Simulation Laser</span>
          <span class="about-module-chip">🪞 Pertes de Cavité</span>
          <span class="about-module-chip">🌊 Navier-Stokes</span>
          <div style="margin:14px 0 10px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;">📐 Mathématiques</div>
          <span class="about-module-chip">∫ Intégration</span>
          <span class="about-module-chip">〜 Interpolation</span>
          <span class="about-module-chip">∂ Éq. Différentielles</span>
          <span class="about-module-chip">⚙️ Optimisation</span>
          <span class="about-module-chip">🔢 Hub Numérisation</span>
          <div style="margin:14px 0 10px;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;">📊 Data & Signal</div>
          <span class="about-module-chip">📊 Data Science</span>
          <span class="about-module-chip">⚡ Énergie</span>
          <span class="about-module-chip">〰️ Signal</span>
          <span class="about-module-chip">🤖 Automatique</span>
        </div>
        """, unsafe_allow_html=True)

def track_module(name):
    if "visited_modules" not in st.session_state:
        st.session_state["visited_modules"] = []
    if "sim_count" not in st.session_state:
        st.session_state["sim_count"] = 0
    ts = datetime.datetime.now().strftime("%H:%M")
    if not st.session_state["visited_modules"] or st.session_state["visited_modules"][-1][0] != name:
        st.session_state["visited_modules"].append((name, ts))
    st.session_state["last_module"] = name
    st.session_state["sim_count"] += 1

def main():
    inject_css()

    if "page" not in st.session_state:
        st.session_state["page"] = "🏠 Accueil"

    render_sidebar_header()

    st.sidebar.markdown('<div class="sidebar-section-label">Physique</div>', unsafe_allow_html=True)
    physics_menu = [
        "📈 Profil Gaussien",
        "🔦 Simulation Laser",
        "🪞 Pertes de Cavité",
        "🌊 Navier-Stokes",
    ]

    st.sidebar.markdown('<div class="sidebar-section-label">Mathématiques</div>', unsafe_allow_html=True)
    math_menu = [
        "Intégration",
        "Interpolation",
        "Éq. Diff",
        "⚙️ Optimisation",
        "🔢 Hub Numérisation",
    ]

    st.sidebar.markdown('<div class="sidebar-section-label">Data & Signal</div>', unsafe_allow_html=True)
    data_menu = [
        "📊 Data Science",
        "⚡ Énergie",
        "Signal",
        "🤖 Automatique",
    ]

    st.sidebar.markdown('<div class="sidebar-section-label">Projet</div>', unsafe_allow_html=True)

    full_menu = ["🏠 Accueil"] + physics_menu + math_menu + data_menu + ["👤 À propos"]

    current_idx = full_menu.index(st.session_state["page"]) if st.session_state["page"] in full_menu else 0

    page = st.sidebar.radio(
        "Navigation",
        full_menu,
        index=current_idx,
        label_visibility="collapsed"
    )

    st.session_state["page"] = page

    page_map = {
        "🏠 Accueil": ("🏠", "Accueil", "", show_home, None),
        "📈 Profil Gaussien": ("📈", "Profil Gaussien", "Physique", gaussian_page, "Profil Gaussien"),
        "🔦 Simulation Laser": ("🔦", "Simulation Laser", "Physique", laser_page, "Simulation Laser"),
        "🪞 Pertes de Cavité": ("🪞", "Pertes de Cavité", "Physique", cavity_page, "Pertes de Cavité"),
        "🌊 Navier-Stokes": ("🌊", "Navier-Stokes", "Physique", navier_stokes_page, "Navier-Stokes"),
        "📊 Data Science": ("📊", "Data Science", "Data & Signal", data_science_page, "Data Science"),
        "⚡ Énergie": ("⚡", "Énergie", "Data & Signal", energy_page, "Énergie"),
        "🔢 Hub Numérisation": ("🔢", "Hub Numérisation", "Mathématiques", numerisation_hub_page, "Hub Numérisation"),
        "⚙️ Optimisation": ("⚙️", "Optimisation", "Mathématiques", optimisation_page, "Optimisation"),
        "🤖 Automatique": ("🤖", "Automatique", "Data & Signal", automatique_page, "Automatique"),
        "Intégration": ("∫", "Intégration", "Mathématiques", integration_page, "Intégration"),
        "Interpolation": ("〜", "Interpolation", "Mathématiques", interpolation_page, "Interpolation"),
        "Éq. Diff": ("∂", "Équations Différentielles", "Mathématiques", equ_diff_page, "Éq. Diff"),
        "Signal": ("〰️", "Analyse du Signal", "Data & Signal", signal_page, "Signal"),
        "👤 À propos": ("👤", "À propos", "Projet", show_about, None),
    }

    if page in page_map:
        icon, title, group, func, tracker_name = page_map[page]
        if page != "🏠 Accueil":
            render_page_header(icon, title, group)
            if tracker_name:
                track_module(tracker_name)
        func()

if __name__ == "__main__":
    main()
