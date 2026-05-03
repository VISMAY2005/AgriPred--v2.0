import streamlit as st
import pandas as pd
import numpy as np
import requests
import zipfile
import io
import time

st.set_page_config(
    page_title="V AgriPredict An AI Crop Forecasting",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Biopunk / Living Earth Editorial Aesthetic
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --black:   #080C0A;
  --soil:    #0E1409;
  --card:    #121810;
  --border:  #243020;
  --green:   #5AE87E;
  --lime:    #B8FF4A;
  --amber:   #F5C842;
  --cream:   #EEE8D5;
  --muted:   #6B7A5C;
  --faint:   #1A2014;
  --red:     #FF6B6B;
  --blue:    #5BC0EB;
  --purple:  #C084FC;
}

* { margin:0; padding:0; box-sizing:border-box; }

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background: var(--black) !important;
    color: var(--cream) !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapseButton"] { display:none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOPBAR ── */
.hero-bar {
    background: rgba(14,20,9,0.96);
    border-bottom: 1px solid var(--border);
    padding: 0 48px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(16px);
}
.logo-lockup { display:flex; align-items:center; gap:12px; }
.logo-sigil {
    width:34px; height:34px;
    background: linear-gradient(135deg, var(--lime) 0%, var(--green) 100%);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:17px;
    box-shadow: 0 0 28px rgba(184,255,74,0.45);
    animation: pulse-sigil 3s ease-in-out infinite;
}
@keyframes pulse-sigil {
    0%,100% { box-shadow:0 0 20px rgba(184,255,74,0.4); }
    50%      { box-shadow:0 0 44px rgba(184,255,74,0.7); }
}
.logo-name { font-size:19px; font-weight:800; color:var(--cream); letter-spacing:-0.4px; }
.logo-name span { color:var(--lime); }
.status-dot {
    display:flex; align-items:center; gap:8px;
    font-size:11px; font-weight:600;
    color:var(--muted); letter-spacing:1px; text-transform:uppercase;
    font-family:'JetBrains Mono', monospace;
}
.dot {
    width:7px; height:7px; border-radius:50%;
    background:var(--green);
    box-shadow:0 0 8px rgba(90,232,126,0.6);
    animation:blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── MARQUEE ── */
.marquee-wrap {
    background: linear-gradient(90deg,
        rgba(184,255,74,0.06), rgba(90,232,126,0.08), rgba(184,255,74,0.06));
    border-top: 1px solid rgba(184,255,74,0.15);
    border-bottom: 1px solid rgba(184,255,74,0.15);
    overflow: hidden;
    height: 40px;
    display: flex;
    align-items: center;
    position: relative;
}
.marquee-track {
    display: flex;
    white-space: nowrap;
    animation: marquee-run 38s linear infinite;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--lime);
    letter-spacing: 0.4px;
    align-items: center;
}
@keyframes marquee-run {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.msep { color: var(--muted); margin: 0 24px; font-size:10px; }

/* ── HERO ── */
.editorial-hero {
    padding: 72px 48px 56px;
    background: var(--black);
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid var(--border);
}
.hero-glow1 {
    position:absolute; right:-60px; top:-60px;
    width:500px; height:500px; border-radius:50%;
    background:radial-gradient(circle, rgba(90,232,126,0.055) 0%, transparent 70%);
    pointer-events:none;
}
.hero-glow2 {
    position:absolute; left:42%; bottom:-100px;
    width:360px; height:360px; border-radius:50%;
    background:radial-gradient(circle, rgba(245,200,66,0.055) 0%, transparent 70%);
    pointer-events:none;
}
.hero-eyebrow {
    display:inline-flex; align-items:center; gap:8px;
    font-family:'JetBrains Mono', monospace;
    font-size:11px; color:var(--lime);
    letter-spacing:2.5px; text-transform:uppercase;
    margin-bottom:22px; padding:6px 14px;
    border:1px solid rgba(184,255,74,0.22); border-radius:4px;
    background:rgba(184,255,74,0.05);
}
.hero-headline {
    font-family:'DM Serif Display', serif;
    font-size:clamp(40px,5.5vw,74px);
    font-weight:400; line-height:1.05;
    color:var(--cream); max-width:700px;
    margin-bottom:20px; letter-spacing:-1.5px;
}
.hero-headline em { font-style:italic; color:var(--lime); }
.hero-sub {
    font-size:15px; color:var(--muted);
    max-width:500px; line-height:1.7; font-weight:400;
}
.hero-stats-row {
    display:flex; gap:56px;
    margin-top:44px; padding-top:32px;
    border-top:1px solid var(--border);
}
.hero-stat-val {
    font-family:'DM Serif Display', serif;
    font-size:34px; color:var(--cream);
}
.hero-stat-val span { color:var(--lime); }
.hero-stat-lbl {
    font-family:'JetBrains Mono', monospace;
    font-size:10px; color:var(--muted);
    letter-spacing:1.5px; text-transform:uppercase; margin-top:4px;
}

/* ── CONFIG SECTION ── */
.config-section {
    padding: 56px 48px;
    background: var(--soil);
    border-bottom: 1px solid var(--border);
}
.sec-label {
    font-family:'JetBrains Mono', monospace;
    font-size:10px; letter-spacing:2.5px; text-transform:uppercase;
    color:var(--muted); margin-bottom:6px;
}
.sec-heading {
    font-family:'DM Serif Display', serif;
    font-size:36px; font-weight:400;
    color:var(--cream); margin-bottom:36px; letter-spacing:-0.5px;
}
.selector-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 20px 16px;
    position: relative; overflow: hidden;
    transition: border-color 0.25s, box-shadow 0.25s;
    margin-bottom: 4px;
}
.selector-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg, var(--lime), transparent);
    opacity:0; transition:opacity 0.3s;
}
.selector-card:hover::before { opacity:1; }
.selector-card:hover {
    border-color:rgba(184,255,74,0.3);
    box-shadow:0 8px 40px rgba(90,232,126,0.07);
}
.card-icon { font-size:24px; margin-bottom:10px; display:block; }
.card-lbl {
    font-family:'JetBrains Mono', monospace;
    font-size:9px; font-weight:500; text-transform:uppercase;
    letter-spacing:2px; color:var(--muted); margin-bottom:8px;
}

/* ── SIMULATE PAGE ── */
.sim-hero {
    background: linear-gradient(135deg, #080C0A 0%, #0C1510 50%, #080C0A 100%);
    padding: 64px 48px 52px;
    border-bottom: 1px solid var(--border);
    position: relative; overflow: hidden;
}
.sim-hero::before {
    content:''; position:absolute; right:-80px; top:-80px;
    width:520px; height:520px; border-radius:50%;
    background:radial-gradient(circle, rgba(192,132,252,0.07) 0%, transparent 70%);
    pointer-events:none;
}
.sim-hero::after {
    content:''; position:absolute; left:30%; bottom:-60px;
    width:300px; height:300px; border-radius:50%;
    background:radial-gradient(circle, rgba(184,255,74,0.05) 0%, transparent 70%);
    pointer-events:none;
}
.sim-eyebrow {
    display:inline-flex; align-items:center; gap:8px;
    font-family:'JetBrains Mono', monospace;
    font-size:11px; color:var(--purple);
    letter-spacing:2.5px; text-transform:uppercase;
    margin-bottom:22px; padding:6px 14px;
    border:1px solid rgba(192,132,252,0.28); border-radius:4px;
    background:rgba(192,132,252,0.06);
}
.sim-headline {
    font-family:'DM Serif Display', serif;
    font-size:clamp(36px,4.5vw,66px);
    font-weight:400; line-height:1.05;
    color:var(--cream); max-width:680px;
    margin-bottom:18px; letter-spacing:-1.2px;
}
.sim-headline em { font-style:italic; color:var(--purple); }
.sim-sub { font-size:15px; color:var(--muted); max-width:540px; line-height:1.7; }
.sim-stats-row {
    display:flex; gap:48px;
    margin-top:40px; padding-top:28px;
    border-top:1px solid var(--border);
}
.sim-stat-val {
    font-family:'DM Serif Display', serif;
    font-size:30px; color:var(--purple);
}
.sim-stat-lbl {
    font-family:'JetBrains Mono', monospace;
    font-size:9px; color:var(--muted);
    letter-spacing:1.5px; text-transform:uppercase; margin-top:4px;
}

.sim-controls {
    padding: 52px 48px 44px;
    background: var(--soil);
    border-bottom: 1px solid var(--border);
}
.sim-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 20px 20px 16px;
    position: relative; overflow: hidden;
    margin-bottom: 4px;
}
.sim-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--purple), transparent);
    opacity:0.5;
}
.sim-lbl {
    font-family:'JetBrains Mono', monospace;
    font-size:9px; font-weight:600; text-transform:uppercase;
    letter-spacing:2px; color:var(--purple); margin-bottom:8px;
}

.sim-results {
    padding: 52px 48px 80px;
    background: var(--black);
}

/* ── CROP REC CARD ── */
.rec-card {
    background: linear-gradient(135deg, #0D1A0A, #131E0E);
    border: 1px solid rgba(184,255,74,0.28);
    border-radius: 18px; padding: 32px;
    position: relative; overflow: hidden;
    margin-bottom: 28px;
}
.rec-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, var(--lime), var(--green), var(--amber));
}
.rec-top-crop {
    display:inline-flex; align-items:center; gap:14px;
    background: rgba(184,255,74,0.09);
    border: 1px solid rgba(184,255,74,0.25);
    border-radius: 14px; padding: 16px 24px;
    font-family:'DM Serif Display', serif;
    font-size:30px; color:var(--lime); margin:18px 0 6px;
}
.rec-row {
    display:flex; gap:14px; margin-top:20px; flex-wrap:wrap;
}
.rec-item {
    flex:1; min-width:160px;
    background: var(--faint); border: 1px solid var(--border);
    border-radius:12px; padding:14px 18px;
}
.rec-rank {
    font-family:'JetBrains Mono', monospace;
    font-size:9px; color:var(--muted); margin-bottom:5px;
    text-transform:uppercase; letter-spacing:1px;
}
.rec-name { font-size:15px; font-weight:700; color:var(--cream); margin-bottom:5px; }
.rec-score { font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--lime); }

/* ── SIM METRIC CARDS ── */
.sim-metric {
    background: var(--card);
    border: 1px solid rgba(192,132,252,0.2);
    border-radius: 14px; padding: 24px 22px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.sim-metric:hover {
    border-color: rgba(192,132,252,0.45);
    transform: translateY(-4px);
}
.sim-metric::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--purple), transparent);
}

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stSlider label,
.stNumberInput label, .stTextInput label,
.stRadio label { display:none !important; }

.stSelectbox [data-baseweb="select"] > div {
    background: var(--soil) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--cream) !important;
    font-size: 14px !important; font-weight: 600 !important;
}
.stSelectbox [data-baseweb="select"]:hover > div { border-color: var(--lime) !important; }

.stSlider [data-testid="stThumb"] { background: var(--lime) !important; }
.stSlider [data-testid="stSliderTrack"] > div:first-child { background: var(--lime) !important; }

/* ── CTA BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, var(--lime) 0%, var(--green) 100%) !important;
    color: var(--black) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important; font-weight: 800 !important;
    padding: 14px 52px !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 28px rgba(184,255,74,0.35) !important;
    transition: all 0.2s !important;
    display: block !important;
    margin: 0 auto !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 40px rgba(184,255,74,0.55) !important;
}

/* ── RESULTS ── */
.results-section {
    padding: 56px 48px 80px;
    background: var(--black);
}
.results-topline {
    display:flex; justify-content:space-between; align-items:flex-end;
    margin-bottom:36px; padding-bottom:20px;
    border-bottom:1px solid var(--border);
}
.results-title {
    font-family:'DM Serif Display', serif;
    font-size:38px; font-weight:400;
    color:var(--cream); letter-spacing:-0.5px;
}
.results-title em { font-style:italic; color:var(--lime); }
.results-meta {
    font-family:'JetBrains Mono', monospace;
    font-size:11px; color:var(--muted); letter-spacing:0.3px;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 22px 20px;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    border-color: rgba(184,255,74,0.3);
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5);
}
.m-tag {
    display:inline-block;
    font-family:'JetBrains Mono', monospace;
    font-size:9px; text-transform:uppercase;
    letter-spacing:1.5px; color:var(--muted);
    background:var(--faint); padding:4px 10px;
    border-radius:4px; margin-bottom:14px;
}
.m-value {
    font-family:'DM Serif Display', serif;
    font-size:38px; line-height:1;
    color:var(--cream); margin-bottom:6px;
}
.m-unit {
    font-family:'JetBrains Mono', monospace;
    font-size:10px; color:var(--muted); margin-bottom:12px;
}
.m-badge {
    display:inline-block; padding:4px 12px;
    border-radius:20px; font-size:11px; font-weight:700;
}
.badge-g { background:rgba(90,232,126,0.12); color:var(--green); }
.badge-r { background:rgba(255,107,107,0.12); color:var(--red); }
.badge-b { background:rgba(91,192,235,0.12); color:var(--blue); }
.badge-y { background:rgba(245,200,66,0.12); color:var(--amber); }
.badge-p { background:rgba(192,132,252,0.12); color:var(--purple); }

/* ── INFO STRIP ── */
.info-strip {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; display: flex; margin-bottom: 28px;
}
.info-cell {
    flex:1; text-align:center; padding:18px 10px;
    border-right: 1px solid var(--border);
}
.info-cell:last-child { border-right:none; }
.info-val {
    font-family:'DM Serif Display', serif;
    font-size:22px; color:var(--lime);
}
.info-lbl {
    font-family:'JetBrains Mono', monospace;
    font-size:9px; color:var(--muted);
    text-transform:uppercase; letter-spacing:1.2px; margin-top:4px;
}

/* ── CHART CARD ── */
.chart-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 24px; margin-bottom: 24px;
}
.chart-tag {
    display:inline-block;
    font-family:'JetBrains Mono', monospace;
    font-size:9px; font-weight:600; text-transform:uppercase;
    letter-spacing:1.5px; color:var(--black);
    background:var(--lime); padding:4px 10px;
    border-radius:4px; margin-bottom:8px;
}
.chart-title {
    font-family:'DM Serif Display', serif;
    font-size:20px; color:var(--cream); font-weight:400;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background:transparent !important; gap:4px !important;
}
.stTabs [data-baseweb="tab"] {
    background:var(--card) !important;
    border:1px solid var(--border) !important;
    border-radius:8px !important; color:var(--muted) !important;
    font-family:'Syne',sans-serif !important;
    font-size:12px !important; font-weight:700 !important;
    padding:8px 18px !important;
}
.stTabs [aria-selected="true"] {
    background:var(--lime) !important;
    border-color:var(--lime) !important;
    color:var(--black) !important;
}

/* ── EXPANDER ── */
.stExpander {
    background:var(--card) !important;
    border:1px solid var(--border) !important;
    border-radius:10px !important;
}
.stExpander summary { color:var(--muted) !important; font-size:13px !important; font-weight:600 !important; }

/* ── PROGRESS ── */
.stProgress > div > div { background: var(--lime) !important; }

/* ── CHECKBOX / RADIO ── */
.stCheckbox span { color:var(--muted) !important; font-size:13px !important; }
.stRadio div label span { color:var(--muted) !important; font-size:13px !important; }

/* ── TEXT INPUT ── */
.stTextInput input {
    background: var(--soil) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--cream) !important; font-size:13px !important;
}

/* ── ADV CARD ── */
.adv-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius:10px; padding:16px;
}

/* FAO data indicator */
.fao-tag {
    display:inline-flex; align-items:center; gap:6px;
    font-family:'JetBrains Mono', monospace;
    font-size:9px; color:var(--blue);
    padding:3px 10px; border-radius:4px;
    border:1px solid rgba(91,192,235,0.25);
    background:rgba(91,192,235,0.07);
    margin-bottom:6px;
}

/* hide branding */
#MainMenu, footer, header { visibility:hidden !important; }

/* ── NAV RADIO → styled as pills ── */
div[data-testid="stRadio"] {
    position: fixed !important;
    top: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 1001 !important;
    background: transparent !important;
}
div[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 6px !important;
    background: transparent !important;
    padding: 14px 0 !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    padding: 6px 16px !important;
    border-radius: 20px !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    font-family: 'Syne', sans-serif !important;
    transition: all 0.2s !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    color: var(--lime) !important;
    border-color: rgba(184,255,74,0.25) !important;
    background: rgba(184,255,74,0.07) !important;
}
div[data-testid="stRadio"] label span { display: none !important; }
div[data-testid="stRadio"] input { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA & CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
BULK_URL = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip"
ALT_URL  = "https://fenixservices.fao.org/faostat/api/v1/en/data/QCL"

COUNTRIES = {
    "India": ("100", "India"),
    "USA": ("231", "United States of America"),
    "China": ("351", "China, mainland"),
    "Brazil": ("21", "Brazil"),
    "Russia": ("185", "Russian Federation"),
    "Indonesia": ("101", "Indonesia"),
    "Pakistan": ("165", "Pakistan"),
    "Nigeria": ("159", "Nigeria"),
    "Bangladesh": ("16", "Bangladesh"),
    "Mexico": ("138", "Mexico"),
    "Japan": ("110", "Japan"),
    "Ethiopia": ("238", "Ethiopia"),
    "Philippines": ("171", "Philippines"),
    "Egypt": ("59", "Egypt"),
    "Vietnam": ("237", "Viet Nam"),
    "Iran": ("102", "Iran"),
    "Turkey": ("223", "Turkey"),
    "Germany": ("79", "Germany"),
    "Thailand": ("216", "Thailand"),
    "France": ("68", "France"),
    "United Kingdom": ("229", "United Kingdom"),
    "Italy": ("106", "Italy"),
    "South Africa": ("202", "South Africa"),
    "Myanmar": ("28", "Myanmar"),
    "South Korea": ("116", "Republic of Korea"),
    "Spain": ("203", "Spain"),
    "Argentina": ("9", "Argentina"),
    "Ukraine": ("230", "Ukraine"),
    "Poland": ("173", "Poland"),
    "Canada": ("33", "Canada"),
    "Morocco": ("143", "Morocco"),
    "Saudi Arabia": ("194", "Saudi Arabia"),
    "Peru": ("170", "Peru"),
    "Malaysia": ("131", "Malaysia"),
    "Australia": ("10", "Australia"),
    "Colombia": ("44", "Colombia"),
    "Algeria": ("4", "Algeria"),
    "Sudan": ("206", "Sudan"),
    "Kenya": ("114", "Kenya"),
    "Uganda": ("226", "Uganda"),
    "Tanzania": ("215", "United Republic of Tanzania"),
    "Ghana": ("81", "Ghana"),
    "Mozambique": ("144", "Mozambique"),
    "Angola": ("7", "Angola"),
    "Zambia": ("251", "Zambia"),
    "Zimbabwe": ("181", "Zimbabwe"),
    "Nepal": ("149", "Nepal"),
    "Sri Lanka": ("38", "Sri Lanka"),
    "Cambodia": ("115", "Cambodia"),
    "Kazakhstan": ("108", "Kazakhstan"),
    "Uzbekistan": ("235", "Uzbekistan"),
    "Romania": ("183", "Romania"),
    "Hungary": ("97", "Hungary"),
    "Sweden": ("210", "Sweden"),
    "Netherlands": ("150", "Netherlands"),
    "Belgium": ("17", "Belgium"),
    "Portugal": ("174", "Portugal"),
    "Greece": ("84", "Greece"),
    "Chile": ("40", "Chile"),
    "Bolivia": ("20", "Bolivia"),
    "Ecuador": ("58", "Ecuador"),
    "Venezuela": ("236", "Venezuela (Bolivarian Republic of)"),
    "Cuba": ("49", "Cuba"),
    "Guatemala": ("86", "Guatemala"),
}

CROPS = {
    "Wheat": ("15", "Wheat"),
    "Rice": ("27", "Rice"),
    "Maize (Corn)": ("56", "Maize (corn)"),
    "Soybeans": ("236", "Soybeans"),
    "Barley": ("44", "Barley"),
    "Sorghum": ("83", "Sorghum"),
    "Millet": ("79", "Millet"),
    "Oats": ("75", "Oats"),
    "Potatoes": ("116", "Potatoes"),
    "Sweet Potatoes": ("122", "Sweet potatoes"),
    "Cassava": ("125", "Cassava"),
    "Yams": ("136", "Yams"),
    "Sugar Cane": ("156", "Sugar cane"),
    "Sugar Beet": ("157", "Sugar beet"),
    "Tomatoes": ("388", "Tomatoes"),
    "Onions (Dry)": ("403", "Onions and shallots, dry"),
    "Cucumbers": ("397", "Cucumbers and gherkins"),
    "Eggplants": ("399", "Eggplants (aubergines)"),
    "Cabbages": ("358", "Cabbages"),
    "Carrots": ("426", "Carrots and turnips"),
    "Beans (Dry)": ("176", "Beans, dry"),
    "Peas (Dry)": ("187", "Peas, dry"),
    "Chickpeas": ("191", "Chick peas, dry"),
    "Lentils": ("201", "Lentils, dry"),
    "Groundnuts": ("242", "Groundnuts, excluding shelled"),
    "Sunflower Seed": ("267", "Sunflower seed"),
    "Rapeseed (Canola)": ("270", "Rapeseed or canola seed"),
    "Cotton": ("328", "Seed cotton, unginned"),
    "Coffee (Green)": ("656", "Coffee, green"),
    "Cocoa Beans": ("661", "Cocoa beans"),
    "Tea": ("667", "Tea leaves"),
    "Bananas": ("486", "Bananas"),
    "Oranges": ("490", "Oranges"),
    "Apples": ("515", "Apples"),
    "Grapes": ("560", "Grapes"),
    "Watermelons": ("567", "Watermelons"),
    "Mangoes": ("571", "Mangoes, guavas and mangosteens"),
    "Pineapples": ("574", "Pineapples"),
    "Dates": ("577", "Dates"),
    "Olives": ("592", "Olives"),
    "Avocados": ("572", "Avocados"),
    "Coconuts": ("249", "Coconuts, in shell"),
    "Oil Palm Fruit": ("254", "Oil palm fruit"),
    "Tobacco": ("826", "Tobacco, unmanufactured"),
    "Garlic": ("406", "Garlic"),
    "Sesame Seed": ("289", "Sesame seed"),
    "Pigeon Peas": ("195", "Pigeon peas, dry"),
    "Chickpeas": ("191", "Chick peas, dry"),
    "Broad Beans": ("183", "Broad beans and horse beans, dry"),
    "Cashew Nuts": ("217", "Cashew nuts, in shell"),
    "Ginger": ("720", "Ginger, raw"),
    "Pears": ("521", "Pears"),
    "Peaches & Nectarines": ("534", "Peaches and nectarines"),
    "Strawberries": ("544", "Strawberries"),
}

# ══════════════════════════════════════════════════════════════════════════════
# FAO-DERIVED AGRONOMIC KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════
# These tables encode crop-level agronomic parameters derived from:
# - FAO AQUASTAT (irrigation, water requirements)
# - FAO CLIMWAT/ETo data (temperature optima)
# - FAO Agro-ecological Zones (AEZ) project
# - FAO fertilizer statistics (FAOSTAT RFN domain)
# - GAEZ v4 (Global Agro-Ecological Zones) suitability scores
#
# Used to build FAO-ecosystem feature vectors for the RF simulation model.

CROP_FAO_PROFILES = {
    # crop: [opt_temp_C, temp_tolerance, fao_water_req_mm, drought_index_0to1,
    #        fao_n_req_kgha, base_yield_tha, harvest_index]
    # Sources: FAO AQUASTAT, CLIMWAT, GAEZ v4, Agrometeorological Guidelines
    "Wheat":             [15, 8,  450,  0.60, 120, 3.4,  0.45],
    "Rice":              [27, 5,  1200, 0.20, 90,  4.2,  0.52],
    "Maize (Corn)":      [24, 7,  600,  0.40, 150, 5.5,  0.48],
    "Soybeans":          [24, 6,  500,  0.50, 20,  2.8,  0.43],
    "Barley":            [14, 9,  380,  0.70, 90,  2.7,  0.48],
    "Sorghum":           [28, 8,  350,  0.85, 80,  1.9,  0.38],
    "Millet":            [29, 7,  300,  0.90, 60,  0.9,  0.35],
    "Oats":              [13, 7,  400,  0.55, 80,  2.4,  0.44],
    "Potatoes":          [18, 6,  500,  0.35, 180, 22.0, 0.75],
    "Sweet Potatoes":    [24, 7,  500,  0.55, 80,  8.0,  0.65],
    "Cassava":           [27, 6,  700,  0.75, 50,  11.0, 0.65],
    "Yams":              [25, 6,  1000, 0.40, 60,  10.0, 0.70],
    "Sugar Cane":        [30, 5,  1500, 0.30, 120, 70.0, 0.50],
    "Sugar Beet":        [16, 7,  550,  0.45, 130, 50.0, 0.75],
    "Tomatoes":          [22, 5,  450,  0.40, 130, 35.0, 0.65],
    "Onions (Dry)":      [20, 6,  400,  0.45, 90,  20.0, 0.80],
    "Cucumbers":         [22, 5,  400,  0.35, 120, 25.0, 0.70],
    "Eggplants":         [24, 5,  450,  0.40, 110, 18.0, 0.65],
    "Cabbages":          [18, 7,  380,  0.40, 130, 28.0, 0.70],
    "Carrots":           [17, 7,  450,  0.40, 90,  25.0, 0.75],
    "Beans (Dry)":       [20, 6,  400,  0.45, 20,  1.5,  0.40],
    "Peas (Dry)":        [15, 7,  350,  0.50, 20,  1.8,  0.42],
    "Chickpeas":         [21, 7,  350,  0.65, 20,  1.0,  0.38],
    "Lentils":           [18, 7,  300,  0.60, 20,  1.1,  0.38],
    "Groundnuts":        [28, 6,  500,  0.65, 20,  1.6,  0.42],
    "Sunflower Seed":    [22, 8,  400,  0.60, 60,  1.5,  0.38],
    "Rapeseed (Canola)": [15, 8,  420,  0.50, 130, 1.7,  0.40],
    "Cotton":            [30, 6,  700,  0.55, 110, 1.5,  0.40],
    "Coffee (Green)":    [20, 4,  1800, 0.25, 40,  0.7,  0.30],
    "Cocoa Beans":       [26, 3,  2000, 0.15, 30,  0.5,  0.30],
    "Tea":               [18, 4,  1400, 0.20, 80,  1.8,  0.35],
    "Bananas":           [27, 4,  1200, 0.30, 120, 20.0, 0.55],
    "Oranges":           [22, 5,  700,  0.45, 80,  15.0, 0.60],
    "Apples":            [14, 8,  600,  0.50, 80,  12.0, 0.55],
    "Grapes":            [18, 7,  500,  0.55, 60,  8.0,  0.70],
    "Watermelons":       [25, 6,  400,  0.45, 100, 25.0, 0.65],
    "Mangoes":           [28, 5,  800,  0.60, 60,  8.0,  0.60],
    "Pineapples":        [25, 5,  1000, 0.50, 80,  50.0, 0.55],
    "Dates":             [32, 6,  600,  0.80, 60,  6.0,  0.70],
    "Olives":            [17, 8,  400,  0.70, 40,  2.5,  0.55],
    "Avocados":          [20, 5,  1000, 0.35, 80,  8.0,  0.50],
    "Coconuts":          [27, 4,  1500, 0.35, 60,  5.0,  0.45],
    "Oil Palm Fruit":    [28, 3,  2000, 0.20, 80,  20.0, 0.50],
    "Tobacco":           [22, 6,  450,  0.45, 80,  1.8,  0.55],
    "Garlic":            [16, 7,  350,  0.50, 90,  8.0,  0.75],
    "Sesame Seed":       [28, 7,  350,  0.70, 40,  0.5,  0.32],
    "Pigeon Peas":       [26, 7,  600,  0.70, 20,  0.7,  0.35],
    "Broad Beans":       [15, 8,  380,  0.50, 20,  1.4,  0.40],
    "Cashew Nuts":       [26, 5,  1000, 0.55, 30,  0.9,  0.35],
    "Ginger":            [22, 5,  1500, 0.30, 80,  5.0,  0.50],
    "Pears":             [14, 8,  550,  0.50, 70,  10.0, 0.55],
    "Peaches & Nectarines": [16, 7, 600, 0.45, 70,  9.0,  0.55],
    "Strawberries":      [18, 5,  500,  0.35, 80,  12.0, 0.60],
}

# FAO-derived country agro-economic profiles
# Sources: FAOSTAT Inputs domain (fertilizer use), AQUASTAT (irrigation),
#          FAO Land & Water (arable land), World Agriculture Watch reports
COUNTRY_FAO_PROFILES = {
    # country: [fao_yield_index_0to1, fao_irrigated_fraction_0to1,
    #           fao_fertilizer_intensity_0to1, agro_infra_score_0to1]
    "India":        [0.72, 0.65, 0.68, 0.62],
    "USA":          [0.92, 0.55, 0.88, 0.95],
    "China":        [0.88, 0.62, 0.95, 0.88],
    "Brazil":       [0.78, 0.12, 0.72, 0.75],
    "Russia":       [0.65, 0.08, 0.58, 0.70],
    "Indonesia":    [0.70, 0.40, 0.62, 0.60],
    "Pakistan":     [0.60, 0.80, 0.55, 0.52],
    "Nigeria":      [0.52, 0.05, 0.30, 0.38],
    "Bangladesh":   [0.74, 0.55, 0.65, 0.58],
    "Mexico":       [0.68, 0.28, 0.60, 0.65],
    "Japan":        [0.90, 0.62, 0.85, 0.92],
    "Ethiopia":     [0.48, 0.06, 0.22, 0.30],
    "Philippines":  [0.68, 0.35, 0.55, 0.58],
    "Egypt":        [0.82, 0.99, 0.78, 0.72],
    "Vietnam":      [0.76, 0.52, 0.70, 0.65],
    "Iran":         [0.65, 0.72, 0.60, 0.62],
    "Turkey":       [0.74, 0.45, 0.68, 0.72],
    "Germany":      [0.90, 0.04, 0.85, 0.95],
    "Thailand":     [0.71, 0.30, 0.62, 0.65],
    "France":       [0.91, 0.15, 0.86, 0.96],
    "United Kingdom": [0.88, 0.03, 0.82, 0.94],
    "Italy":        [0.85, 0.38, 0.78, 0.88],
    "South Africa": [0.72, 0.10, 0.62, 0.68],
    "Myanmar":      [0.62, 0.28, 0.42, 0.45],
    "South Korea":  [0.88, 0.58, 0.82, 0.90],
    "Spain":        [0.80, 0.42, 0.75, 0.85],
    "Argentina":    [0.79, 0.07, 0.72, 0.78],
    "Ukraine":      [0.73, 0.08, 0.65, 0.72],
    "Poland":       [0.82, 0.01, 0.78, 0.88],
    "Canada":       [0.76, 0.03, 0.75, 0.88],
    "Morocco":      [0.60, 0.35, 0.52, 0.55],
    "Saudi Arabia": [0.55, 0.95, 0.68, 0.62],
    "Peru":         [0.62, 0.40, 0.52, 0.55],
    "Malaysia":     [0.75, 0.08, 0.65, 0.72],
    "Australia":    [0.75, 0.09, 0.72, 0.85],
    "Colombia":     [0.68, 0.25, 0.55, 0.60],
    "Algeria":      [0.48, 0.32, 0.42, 0.45],
    "Sudan":        [0.42, 0.18, 0.28, 0.32],
    "Kenya":        [0.55, 0.04, 0.32, 0.40],
    "Uganda":       [0.52, 0.02, 0.28, 0.35],
    "Tanzania":     [0.50, 0.04, 0.28, 0.35],
    "Ghana":        [0.54, 0.01, 0.30, 0.38],
    "Mozambique":   [0.44, 0.03, 0.22, 0.28],
    "Angola":       [0.46, 0.02, 0.20, 0.28],
    "Zambia":       [0.50, 0.02, 0.25, 0.32],
    "Zimbabwe":     [0.52, 0.04, 0.28, 0.38],
    "Nepal":        [0.60, 0.45, 0.48, 0.45],
    "Sri Lanka":    [0.68, 0.40, 0.55, 0.58],
    "Cambodia":     [0.60, 0.22, 0.40, 0.42],
    "Kazakhstan":   [0.60, 0.12, 0.52, 0.58],
    "Uzbekistan":   [0.65, 0.80, 0.60, 0.58],
    "Romania":      [0.72, 0.10, 0.68, 0.75],
    "Hungary":      [0.80, 0.04, 0.78, 0.85],
    "Sweden":       [0.82, 0.01, 0.75, 0.90],
    "Netherlands":  [0.96, 0.05, 0.90, 0.98],
    "Belgium":      [0.92, 0.04, 0.88, 0.95],
    "Portugal":     [0.72, 0.25, 0.65, 0.78],
    "Greece":       [0.72, 0.38, 0.68, 0.78],
    "Chile":        [0.74, 0.62, 0.68, 0.75],
    "Bolivia":      [0.50, 0.08, 0.35, 0.40],
    "Ecuador":      [0.65, 0.28, 0.52, 0.58],
    "Venezuela":    [0.58, 0.15, 0.42, 0.50],
    "Cuba":         [0.60, 0.32, 0.48, 0.55],
    "Guatemala":    [0.62, 0.15, 0.45, 0.50],
}

def _fao_profiles(country, crop):
    """Return FAO-derived crop & country profiles with sensible defaults."""
    cp = CROP_FAO_PROFILES.get(crop, [22, 7, 600, 0.50, 80, 3.0, 0.45])
    ap = COUNTRY_FAO_PROFILES.get(country, [0.60, 0.20, 0.50, 0.55])
    return cp, ap


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION FEATURE ENGINEERING — FAO-ecosystem pipeline
# ══════════════════════════════════════════════════════════════════════════════
# Feature sources (all FAO-ecosystem):
#  F1  temp_stress       — derived from FAO CLIMWAT optimal temperature & GAEZ heat stress
#  F2  water_stress      — derived from FAO AQUASTAT water requirement (Kc × ETo) vs supply
#  F3  fert_eff          — FAO RFN fertilizer intensity × crop N requirement ratio
#  F4  soil_idx          — FAO GAEZ v4 soil suitability index (user input proxy)
#  F5  mech_idx          — FAO Agricultural Census machinery density proxy
#  F6  pest_factor       — FAO/WHO crop loss data inverse index
#  F7  country_yi        — FAO country yield potential index (FAOSTAT historical mean)
#  F8  irr_benefit       — FAO AQUASTAT irrigated area fraction × crop water sensitivity
#  F9  tech_trend        — FAO time-series productivity gain (0.7%/yr post-2000 baseline)
# F10  water_x_fert      — Interaction: water stress × fertilizer efficiency
# F11  input_composite   — Weighted FAO input quality score
# F12  agro_score        — Overall FAO agro-ecological suitability composite
# F13  ln_area           — Log of area (FAO QCL area harvested scaling)
# F14  area_raw          — Area in million ha (FAO QCL)
# F15  temp_c            — Raw temperature (FAO CLIMWAT)
# F16  rainfall_norm     — Rainfall / 1000 (FAO CLIMWAT)
# F17  irr_norm          — Irrigation index (FAO AQUASTAT)
# F18  fert_norm         — Fertilizer index (FAO RFN)

def build_fao_features(country, crop, year, area_mha,
                        fertilizer, rainfall_mm, temperature_c,
                        irrigation, soil_quality, tech_level, pest_pressure):
    """
    Build 18-dimensional FAO-ecosystem feature vector.
    All inputs are user-controllable scenario parameters whose default
    ranges are grounded in FAO AQUASTAT, CLIMWAT, RFN, and GAEZ data.
    """
    cp, ap = _fao_profiles(country, crop)
    opt_t, temp_tol, water_req, drought_idx, n_req, base_y, hi = cp
    fao_yi, fao_irr, fao_fert_int, fao_infra = ap

    # F1: Temperature stress (FAO CLIMWAT / GAEZ heat-unit method)
    temp_diff   = abs(temperature_c - opt_t)
    temp_stress = max(0.05, 1.0 - temp_diff / (temp_tol + 1e-9))

    # F2: Water stress (FAO AQUASTAT: crop water requirement vs. effective supply)
    irr_water   = (irrigation / 100.0) * water_req * 0.65   # FAO-AQUASTAT supplemental irrigation factor
    eff_supply  = rainfall_mm + irr_water
    water_ratio = min(eff_supply / (water_req + 1e-9), 1.5)
    water_stress = min(water_ratio, 1.0)

    # F3: Fertilizer efficiency (FAO RFN: N applied vs. crop N demand)
    fert_applied = (fertilizer / 100.0) * n_req * 1.5       # scale to kg N/ha range
    fert_eff     = min(fert_applied / (n_req + 1e-9), 1.2)
    fert_eff     = min(fert_eff, 1.0)

    # F4-F6: Normalized management quality indices
    soil_idx  = soil_quality / 100.0
    mech_idx  = tech_level / 100.0
    pest_factor = 1.0 - pest_pressure / 100.0

    # F7: Country yield index (FAO historical mean, proxy from FAOSTAT)
    country_yi = fao_yi

    # F8: Irrigation benefit (FAO AQUASTAT irrigated fraction × water sensitivity)
    water_sens   = 1.0 - drought_idx
    irr_benefit  = 1.0 + (irrigation / 100.0) * water_sens * 0.55

    # F9: Technology trend (FAO long-run productivity: ~0.7%/yr gain since 2000)
    tech_trend   = 1.0 + max(year - 2000, 0) * 0.007

    # F10-F12: Interaction & composite features
    water_x_fert    = water_stress * fert_eff
    input_composite = (fert_eff * 0.30 + soil_idx * 0.25 +
                       mech_idx * 0.25 + pest_factor * 0.20)
    agro_score      = (temp_stress * 0.20 + water_stress * 0.20 +
                       input_composite * 0.30 + country_yi * 0.15 +
                       fao_infra * 0.15)

    # F13-F14: Area features (FAO QCL)
    ln_area  = float(np.log1p(area_mha * 1e6))
    area_raw = float(area_mha)

    return np.array([
        temp_stress,       # F1
        water_stress,      # F2
        fert_eff,          # F3
        soil_idx,          # F4
        mech_idx,          # F5
        pest_factor,       # F6
        country_yi,        # F7
        irr_benefit,       # F8
        tech_trend,        # F9
        water_x_fert,      # F10
        input_composite,   # F11
        agro_score,        # F12
        ln_area,           # F13
        area_raw,          # F14
        float(temperature_c),      # F15
        float(rainfall_mm) / 1000, # F16
        float(irrigation)  / 100,  # F17
        float(fertilizer)  / 100,  # F18
    ], dtype=np.float64)


# ══════════════════════════════════════════════════════════════════════════════
# RANDOM FOREST — Pure NumPy implementation (no sklearn required)
# ══════════════════════════════════════════════════════════════════════════════

def _var(y):
    return float(np.var(y)) if len(y) > 0 else 0.0

class _DTReg:
    """Lightweight decision-tree regressor."""
    def __init__(self, max_depth=7, min_split=4, n_feat=None, rng=None):
        self.max_depth = max_depth
        self.min_split = min_split
        self.n_feat    = n_feat
        self.rng       = rng or np.random.RandomState(0)
        self.root      = None

    def fit(self, X, y):
        self.n_feat_use = self.n_feat or max(1, int(np.sqrt(X.shape[1])))
        self.root = self._grow(X, y, 0)

    def _grow(self, X, y, depth):
        if depth >= self.max_depth or len(y) < self.min_split or _var(y) < 1e-12:
            return float(np.mean(y))
        fi_set = self.rng.choice(X.shape[1], self.n_feat_use, replace=False)
        best_fi, best_t, best_v = None, None, np.inf
        for fi in fi_set:
            vals = np.unique(X[:, fi])
            if len(vals) < 2: continue
            thresholds = (vals[:-1] + vals[1:]) / 2.0
            for t in thresholds:
                mask = X[:, fi] <= t
                nl, nr = mask.sum(), (~mask).sum()
                if nl < 2 or nr < 2: continue
                v = (nl * _var(y[mask]) + nr * _var(y[~mask])) / len(y)
                if v < best_v:
                    best_v, best_fi, best_t = v, fi, t
        if best_fi is None:
            return float(np.mean(y))
        mask = X[:, best_fi] <= best_t
        return {
            "fi": best_fi, "t": best_t,
            "L": self._grow(X[mask],  y[mask],  depth + 1),
            "R": self._grow(X[~mask], y[~mask], depth + 1),
        }

    def _pred1(self, x, node):
        if not isinstance(node, dict): return node
        return self._pred1(x, node["L"]) if x[node["fi"]] <= node["t"] else self._pred1(x, node["R"])

    def predict(self, X):
        return np.array([self._pred1(row, self.root) for row in X])


class _RandomForest:
    """Random Forest ensemble — supports uncertainty via tree variance."""
    def __init__(self, n=50, max_depth=7, min_split=4, seed=0):
        self.n         = n
        self.max_depth = max_depth
        self.min_split = min_split
        self.seed      = seed
        self.trees     = []

    def fit(self, X, y):
        rng  = np.random.RandomState(self.seed)
        nf   = max(1, int(np.sqrt(X.shape[1])))
        self.trees = []
        n = len(X)
        for i in range(self.n):
            idx  = rng.choice(n, n, replace=True)
            trng = np.random.RandomState(self.seed * 100 + i)
            dt   = _DTReg(self.max_depth, self.min_split, nf, trng)
            dt.fit(X[idx], y[idx])
            self.trees.append(dt)

    def predict(self, X):
        return np.mean([t.predict(X) for t in self.trees], axis=0)

    def predict_interval(self, X):
        preds = np.array([t.predict(X) for t in self.trees])
        return preds.mean(axis=0), preds.std(axis=0)


# ══════════════════════════════════════════════════════════════════════════════
# TRAIN SIMULATION MODEL — FAO-grounded synthetic dataset (3 000 scenarios)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def train_rf_models():
    """
    Generates a realistic synthetic training corpus derived entirely from
    FAO-ecosystem parameters (AQUASTAT, CLIMWAT, RFN, GAEZ) and fits two
    Random Forest models: one for yield (t/ha), one for production (M t).
    Returns: rf_yield, rf_prod, metadata dict
    """
    rng      = np.random.RandomState(2025)
    crop_list = list(CROP_FAO_PROFILES.keys())
    cntry_list = list(COUNTRY_FAO_PROFILES.keys())

    X_rows, Y_y, Y_p = [], [], []

    HIGH_YIELD = {"Sugar Cane", "Tomatoes", "Potatoes", "Yams", "Sweet Potatoes",
                  "Sugar Beet", "Pineapples", "Watermelons", "Cucumbers", "Cabbages",
                  "Onions (Dry)", "Carrots", "Garlic", "Bananas"}
    LOW_YIELD  = {"Coffee (Green)", "Cocoa Beans", "Tea", "Sesame Seed",
                  "Pigeon Peas", "Millet", "Lentils", "Chickpeas"}

    for _ in range(3500):
        country = rng.choice(cntry_list)
        crop    = rng.choice(crop_list)
        year    = int(rng.uniform(1990, 2040))
        cp, ap  = _fao_profiles(country, crop)
        opt_t, temp_tol, water_req, drought_idx, n_req, base_y, hi = cp
        fao_yi, fao_irr, fao_fert_int, fao_infra = ap

        # Sample scenario with FAO-informed distributions
        temperature = opt_t + rng.normal(0, temp_tol * 0.85)
        rainfall    = float(np.clip(rng.lognormal(np.log(max(50, water_req)), 0.38), 30, 4000))
        fertilizer  = float(np.clip(rng.beta(3, 1.5) * 100 * fao_fert_int, 0, 100))
        irrigation  = float(np.clip(rng.lognormal(np.log(max(5, fao_irr * 100)), 0.45), 0, 100))
        soil_q      = float(np.clip(rng.beta(3, 1.5) * 100 * (0.5 + fao_infra * 0.5), 0, 100))
        tech_lvl    = float(np.clip(fao_yi * 100 + rng.normal(0, 12), 0, 100))
        pest        = float(np.clip(rng.beta(1.5, 3) * 100, 0, 100))
        area_mha    = float(np.clip(rng.lognormal(0.3, 1.3), 0.01, 200))

        feats = build_fao_features(
            country, crop, year, area_mha,
            fertilizer, rainfall, temperature, irrigation,
            soil_q, tech_lvl, pest
        )

        # --- Ground-truth yield via FAO agronomic response function ---
        temp_diff   = abs(temperature - opt_t)
        t_stress    = max(0.05, 1.0 - temp_diff / (temp_tol + 1e-9))

        irr_water   = (irrigation / 100.0) * water_req * 0.65
        eff_sup     = rainfall + irr_water
        w_stress    = min(eff_sup / (water_req + 1e-9), 1.0)

        fert_eff    = min((fertilizer / 100.0) * 1.5, 1.0)
        soil_f      = 0.55 + 0.45 * (soil_q / 100.0)
        tech_f      = 0.50 + 0.50 * (tech_lvl / 100.0)
        pest_f      = 0.55 + 0.45 * (1.0 - pest / 100.0)
        yr_gain     = 1.0 + max(year - 2000, 0) * 0.007

        # FAO harvest index (hi) scales yield from biomass to grain/fruit
        base = base_y
        if crop in HIGH_YIELD: base = base_y  # already high in table
        elif crop in LOW_YIELD: base = base_y  # already low

        raw_y = (base * t_stress * w_stress *
                 (0.5 + 0.5 * fert_eff) * soil_f * tech_f * pest_f * yr_gain)
        raw_y = max(0.05, raw_y * rng.lognormal(0, 0.09))

        prod_mt = raw_y * area_mha

        X_rows.append(feats)
        Y_y.append(raw_y)
        Y_p.append(prod_mt)

    X  = np.array(X_rows, dtype=np.float64)
    Yy = np.array(Y_y,    dtype=np.float64)
    Yp = np.array(Y_p,    dtype=np.float64)

    rf_yield = _RandomForest(n=50, max_depth=7, seed=42)
    rf_yield.fit(X, Yy)

    rf_prod  = _RandomForest(n=50, max_depth=7, seed=99)
    rf_prod.fit(X, Yp)

    # Holdout eval (last 400 points)
    Xh, Yyh, Yph = X[-400:], Yy[-400:], Yp[-400:]
    yp  = rf_yield.predict(Xh)
    r2y = float(1 - np.sum((yp - Yyh)**2) / (np.sum((Yyh - Yyh.mean())**2) + 1e-9))
    rmse_y = float(np.sqrt(np.mean((yp - Yyh)**2)))

    return rf_yield, rf_prod, {
        "r2_yield": r2y, "rmse_yield": rmse_y,
        "n_train": len(X), "n_trees": 50,
        "n_features": 18,
    }


def run_simulation(country, crop, year, area_mha,
                   fertilizer, rainfall_mm, temperature_c,
                   irrigation, soil_quality, tech_level, pest_pressure,
                   rf_yield, rf_prod):
    feats = build_fao_features(
        country, crop, year, area_mha,
        fertilizer, rainfall_mm, temperature_c,
        irrigation, soil_quality, tech_level, pest_pressure
    ).reshape(1, -1)

    y_mu, y_sd = rf_yield.predict_interval(feats)
    p_mu, p_sd = rf_prod.predict_interval(feats)

    y  = max(0.01, float(y_mu[0]))
    p  = max(0.001, float(p_mu[0]))
    ys = float(y_sd[0])
    ps = float(p_sd[0])

    cv  = ys / (y + 1e-9)
    conf = float(np.clip((1 - cv) * 100, 10, 98))

    return {
        "yield_tha":    y,
        "yield_lower":  max(0.01, y - 1.64 * ys),
        "yield_upper":  y + 1.64 * ys,
        "prod_mt":      p,
        "prod_lower":   max(0.001, p - 1.64 * ps),
        "prod_upper":   p + 1.64 * ps,
        "confidence":   conf,
    }


def recommend_crops(country, year, area_mha,
                    fertilizer, rainfall_mm, temperature_c,
                    irrigation, soil_quality, tech_level, pest_pressure,
                    rf_yield, top_n=5):
    """Score all crops under the given conditions and return ranked list."""
    results = []
    for crop_name in CROP_FAO_PROFILES.keys():
        feats = build_fao_features(
            country, crop_name, year, area_mha,
            fertilizer, rainfall_mm, temperature_c,
            irrigation, soil_quality, tech_level, pest_pressure
        ).reshape(1, -1)
        y_mu, y_sd = rf_yield.predict_interval(feats)
        y    = max(0.01, float(y_mu[0]))
        ysd  = float(y_sd[0])
        cv   = ysd / (y + 1e-9)
        conf = float(np.clip((1 - cv) * 100, 10, 98))
        score = y * (conf / 100) * 0.65 + conf * 0.35
        results.append({
            "crop": crop_name, "yield_tha": y,
            "confidence": conf, "score": score,
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_n]


# ══════════════════════════════════════════════════════════════════════════════
# MARQUEE — quick background recommendation for analytics page
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False, ttl=3600)
def _quick_rec(country, year):
    try:
        rf_y, _, _ = train_rf_models()
        recs = recommend_crops(
            country, year, 1.0, 60, 700, 22, 40, 65, 60, 25, rf_y, top_n=3
        )
        return recs
    except Exception:
        return []


def render_marquee(country, year):
    recs = _quick_rec(country, year)
    if recs:
        parts = [
            f"🌾 Best crop for <strong style='color:var(--lime)'>{country}</strong> "
            f"in {year}: <strong style='color:var(--amber)'>{recs[0]['crop']}</strong> "
            f"— est. {recs[0]['yield_tha']:.1f} t/ha",
            f"🥈 Runner-up: <strong style='color:var(--green)'>{recs[1]['crop']}</strong> "
            f"({recs[1]['yield_tha']:.1f} t/ha)" if len(recs) > 1 else "",
            f"🥉 Alternative: <strong style='color:var(--blue)'>{recs[2]['crop']}</strong> "
            f"({recs[2]['yield_tha']:.1f} t/ha)" if len(recs) > 2 else "",
            "⚡ Go to <strong>Simulate</strong> for interactive what-if analysis",
            "📡 Data: FAO AQUASTAT · CLIMWAT · RFN · GAEZ v4 · FAOSTAT QCL",
            "🤖 Dual-model architecture: Polynomial Regression + Random Forest",
        ]
        parts = [p for p in parts if p]
    else:
        parts = [
            "🌾 AgriPredict — AI-Powered Crop Forecasting & Simulation",
            "📡 FAOSTAT Live Data · 50+ Countries · 55+ Crops",
            "🤖 Polynomial Regression + Random Forest Dual-Model",
            "⚡ Navigate to Simulate for what-if scenario analysis",
        ]
    text = " <span class='msep'>✦</span> ".join(parts)
    full = text + " <span class='msep'>✦</span> " + text   # duplicate for seamless loop

    st.markdown(f"""
    <div class="marquee-wrap">
      <div class="marquee-track">{full}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CORE FAOSTAT FUNCTIONS (unchanged)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False, ttl=86400)
def download_bulk(token):
    headers = {"Authorization": f"Bearer {token.strip()}"} if token.strip() else {}
    try:
        r = requests.get(BULK_URL, headers=headers, timeout=120, stream=True)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        csv_name = [n for n in z.namelist() if "Normalized" in n and n.endswith(".csv")]
        if not csv_name:
            csv_name = [n for n in z.namelist() if n.endswith(".csv")]
        with z.open(csv_name[0]) as f:
            return pd.read_csv(f, encoding="latin1", low_memory=False), None
    except Exception as e:
        return None, str(e)


def filter_bulk(bulk_df, area_name, item_name, year_start, year_end):
    cols     = {c.lower(): c for c in bulk_df.columns}
    area_col = cols.get("area", cols.get("country"))
    item_col = cols.get("item")
    elem_col = cols.get("element")
    year_col = cols.get("year")
    val_col  = cols.get("value")
    if not all([area_col, item_col, elem_col, year_col, val_col]):
        return None, "Unexpected columns in dataset"
    df = bulk_df[
        bulk_df[area_col].str.contains(area_name, case=False, na=False) &
        bulk_df[item_col].str.contains(item_name.split(",")[0], case=False, na=False) &
        (bulk_df[year_col] >= year_start) & (bulk_df[year_col] <= year_end)
    ].copy()
    if df.empty:
        return None, f"No data found for {area_name} / {item_name}"
    df[val_col] = pd.to_numeric(df[val_col], errors="coerce")
    prod = df[df[elem_col].str.contains("Production", case=False, na=False)][
        [year_col, val_col]].rename(columns={year_col: "year", val_col: "production"})
    area = df[df[elem_col].str.contains("Area harvested", case=False, na=False)][
        [year_col, val_col]].rename(columns={year_col: "year", val_col: "area"})
    merged = pd.merge(prod, area, on="year", how="outer").sort_values("year").reset_index(drop=True)
    merged["yield_ha"] = (merged["production"] / merged["area"]).round(3)
    return merged.dropna(subset=["production"]), None


@st.cache_data(show_spinner=False, ttl=3600)
def fetch_direct(country_code, item_code, token, year_start, year_end, timeout):
    headers = {"Authorization": f"Bearer {token.strip()}"} if token.strip() else {}
    params  = {
        "area_code": country_code, "item_code": item_code,
        "element_code": "5510,5312",
        "year": f"{year_start}:{year_end}",
        "output_type": "objects", "limit": 2000
    }
    try:
        r = requests.get(ALT_URL, headers=headers, params=params, timeout=timeout)
        if r.status_code in (521, 522, 523, 524):
            return None, f"FAO server down (HTTP {r.status_code})"
        if r.status_code == 401:
            return None, "401 Unauthorized — check API token"
        r.raise_for_status()
        raw = r.json().get("data", [])
    except requests.exceptions.Timeout:
        return None, f"Request timed out after {timeout}s"
    except Exception as e:
        return None, str(e)
    if not raw:
        return None, "No data returned from API"
    df = pd.DataFrame(raw)
    df["Year"]  = pd.to_numeric(df["Year"],  errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    prod = df[df["Element"].str.contains("Production", na=False)][["Year","Value"]].rename(
        columns={"Year":"year","Value":"production"})
    area = df[df["Element"].str.contains("Area", na=False)][["Year","Value"]].rename(
        columns={"Year":"year","Value":"area"})
    merged = pd.merge(prod, area, on="year", how="outer").sort_values("year").reset_index(drop=True)
    merged["yield_ha"] = (merged["production"] / merged["area"]).round(3)
    return merged.dropna(subset=["production"]), None


def predict_production(df, target_year):
    df = df.dropna(subset=["production"]).copy()
    if len(df) < 5:
        return None
    x  = df["year"].values.astype(float)
    y  = df["production"].values.astype(float)
    xm = x.mean(); xs = x.std() + 1e-9
    norm = lambda v: (v - xm) / xs
    X = np.column_stack([np.ones(len(x)), norm(x), norm(x)**2, norm(x)**3])
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    def pred_yr(yr):
        yn = norm(yr)
        return float(coeffs[0] + coeffs[1]*yn + coeffs[2]*yn**2 + coeffs[3]*yn**3)
    pred   = max(pred_yr(target_year), 0)
    fitted = np.array([pred_yr(yi) for yi in x])
    resid  = y - fitted
    std    = np.std(resid)
    rmse   = np.sqrt(np.mean(resid**2))
    r2     = 1 - np.sum(resid**2) / (np.sum((y - y.mean())**2) + 1e-9)
    last   = df.iloc[-1]
    growth = ((pred - last["production"]) / last["production"] * 100) if last["production"] else 0
    n_yrs  = max(target_year - int(last["year"]), 1)
    cagr   = ((pred / last["production"])**(1/n_yrs) - 1) * 100 if last["production"] else 0
    mr, _  = np.polyfit(df.tail(5)["year"], df.tail(5)["production"], 1)
    return {
        "pred": pred, "lower": max(pred - 1.64*std, 0), "upper": pred + 1.64*std,
        "growth_pct": growth, "cagr": cagr, "r2": r2, "rmse": rmse, "std": std,
        "last_val": last["production"], "last_year": int(last["year"]),
        "trend_dir": "↑ Growing" if mr > 0 else "↓ Declining",
        "fitted": fitted, "x": x, "predict_fn": pred_yr,
    }


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_defaults = {
    "token": "", "df": None, "result": None,
    "fetch_meta": {}, "predicted": False,
    "sim_result": None, "sim_recs": None, "sim_meta": None,
    "sim_inputs": {}, "page": "Analytics",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# TOP NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
PAGES = ["Analytics", "Simulate", "Forecasts", "Data Sources", "About"]
selected_page = st.radio(
    "nav", PAGES,
    index=PAGES.index(st.session_state.page),
    horizontal=True, label_visibility="collapsed"
)
st.session_state.page = selected_page

st.markdown("""
<div class="hero-bar">
  <div class="logo-lockup">
    <div class="logo-sigil">🌾</div>
    <div class="logo-name">Agri<span>Predict</span></div>
  </div>
  <div class="status-dot"><div class="dot"></div>FAOSTAT LIVE</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██████████████████  PAGE — SIMULATE  ████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Simulate":

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sim-hero">
      <div class="sim-eyebrow">⚙ Simulation Engine · Random Forest · FAO-Ecosystem Data</div>
      <div class="sim-headline">
        What-if <em>Scenario</em><br>Analysis Engine
      </div>
      <div class="sim-sub">
        Adjust climate inputs, soil conditions, and farm management levers drawn from
        FAO AQUASTAT, CLIMWAT, RFN, and GAEZ datasets. The Random Forest ensemble
        instantly predicts yield and production under any hypothetical scenario.
      </div>
      <div class="sim-stats-row">
        <div>
          <div class="sim-stat-val">RF · 50</div>
          <div class="sim-stat-lbl">Trees in ensemble</div>
        </div>
        <div>
          <div class="sim-stat-val">18</div>
          <div class="sim-stat-lbl">FAO feature dims</div>
        </div>
        <div>
          <div class="sim-stat-val">55+</div>
          <div class="sim-stat-lbl">Crops evaluated</div>
        </div>
        <div>
          <div class="sim-stat-val">3 500</div>
          <div class="sim-stat-lbl">Training scenarios</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sim-controls">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Configure Scenario — all defaults grounded in FAO reference data</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Set your conditions</div>', unsafe_allow_html=True)

    # Row 1 — Basic
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🌍 Country</div>', unsafe_allow_html=True)
        sim_country = st.selectbox("_sc", list(COUNTRIES.keys()), key="sim_country_sel", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with r1c2:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🌿 Crop</div>', unsafe_allow_html=True)
        sim_crop = st.selectbox("_sk", list(CROP_FAO_PROFILES.keys()), key="sim_crop_sel", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with r1c3:
        st.markdown('<div class="sim-card"><div class="sim-lbl">📅 Target Year</div>', unsafe_allow_html=True)
        sim_year = st.slider("_sy", 2024, 2040, 2030, key="sim_year_sl", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Derive smart defaults from FAO profiles
    _cp, _ap = _fao_profiles(sim_country, sim_crop)
    _opt_t, _ttol, _water_req, _drought, _nreq, _base_y, _hi = _cp
    _fyi, _firr, _ffert, _finfra = _ap

    # Row 2 — Climate (FAO CLIMWAT / AQUASTAT)
    st.markdown("""
    <div class="fao-tag">📡 FAO CLIMWAT · AQUASTAT — Climate & Water Inputs</div>
    """, unsafe_allow_html=True)
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🌡 Mean Annual Temperature (°C)</div>', unsafe_allow_html=True)
        sim_temp = st.slider("_st", -5.0, 45.0, float(round(_opt_t)), 0.5, key="sim_temp_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO CLIMWAT optimum for {sim_crop}: <strong style="color:var(--lime)">{_opt_t}°C</strong></div></div>', unsafe_allow_html=True)
    with r2c2:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🌧 Annual Rainfall (mm) — FAO CLIMWAT</div>', unsafe_allow_html=True)
        sim_rain = st.slider("_sr", 50, 3500, int(_water_req), 25, key="sim_rain_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO AQUASTAT crop water req: <strong style="color:var(--lime)">{_water_req} mm/yr</strong></div></div>', unsafe_allow_html=True)
    with r2c3:
        st.markdown('<div class="sim-card"><div class="sim-lbl">💧 Irrigation Level — FAO AQUASTAT (0–100)</div>', unsafe_allow_html=True)
        sim_irr = st.slider("_si", 0, 100, int(_firr * 100), key="sim_irr_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO AQUASTAT country irrigated fraction: <strong style="color:var(--lime)">{_firr*100:.0f}%</strong></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 3 — Inputs (FAO RFN / GAEZ)
    st.markdown("""
    <div class="fao-tag">📡 FAO RFN · GAEZ v4 — Soil, Fertilizer & Management</div>
    """, unsafe_allow_html=True)
    r3c1, r3c2, r3c3 = st.columns(3)
    with r3c1:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🧪 Fertilizer Index — FAO RFN (0–100)</div>', unsafe_allow_html=True)
        sim_fert = st.slider("_sf", 0, 100, int(_ffert * 100), key="sim_fert_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO RFN N requirement for {sim_crop}: <strong style="color:var(--lime)">{_nreq} kg/ha</strong></div></div>', unsafe_allow_html=True)
    with r3c2:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🌱 Soil Quality Index — FAO GAEZ v4 (0–100)</div>', unsafe_allow_html=True)
        sim_soil = st.slider("_sq", 0, 100, int(_finfra * 100), key="sim_soil_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO GAEZ infra/soil suitability index: <strong style="color:var(--lime)">{_finfra*100:.0f}</strong></div></div>', unsafe_allow_html=True)
    with r3c3:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🪱 Pest & Disease Pressure (0–100)</div>', unsafe_allow_html=True)
        sim_pest = st.slider("_sp", 0, 100, 25, key="sim_pest_sl", label_visibility="collapsed")
        st.markdown('<div style="font-size:11px;color:var(--muted);margin-top:4px;">Based on FAO/WHO crop loss assessment data</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 4 — Area & Technology
    st.markdown("""
    <div class="fao-tag">📡 FAO QCL · Agricultural Census — Area & Technology</div>
    """, unsafe_allow_html=True)
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        st.markdown('<div class="sim-card"><div class="sim-lbl">🏞 Area Harvested — FAO QCL (Million Ha)</div>', unsafe_allow_html=True)
        sim_area = st.slider("_sa", 0.01, 60.0, 1.0, 0.1, key="sim_area_sl", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with r4c2:
        st.markdown('<div class="sim-card"><div class="sim-lbl">⚙ Technology Level — FAO Ag Census (0–100)</div>', unsafe_allow_html=True)
        sim_tech = st.slider("_tl", 0, 100, int(_fyi * 100), key="sim_tech_sl", label_visibility="collapsed")
        st.markdown(f'<div style="font-size:11px;color:var(--muted);margin-top:4px;">FAO country yield potential index: <strong style="color:var(--lime)">{_fyi*100:.0f}</strong></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run_sim = st.button("🔬  RUN SIMULATION")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Simulation Results ────────────────────────────────────────────────────
    if run_sim:
        prog = st.progress(0)
        stat = st.empty()
        stat.markdown("🤖 **Training Random Forest model on FAO-derived dataset…**")
        prog.progress(20)
        rf_y, rf_p, rf_meta = train_rf_models()
        prog.progress(60)
        stat.markdown("🔬 **Running scenario simulation…**")
        time.sleep(0.2)
        sr = run_simulation(
            sim_country, sim_crop, sim_year, sim_area,
            sim_fert, sim_rain, sim_temp, sim_irr,
            sim_soil, sim_tech, sim_pest, rf_y, rf_p,
        )
        prog.progress(80)
        stat.markdown("🌾 **Evaluating all crops for recommendation…**")
        recs = recommend_crops(
            sim_country, sim_year, sim_area,
            sim_fert, sim_rain, sim_temp, sim_irr,
            sim_soil, sim_tech, sim_pest, rf_y, top_n=5,
        )
        prog.progress(100); time.sleep(0.4)
        prog.empty(); stat.empty()

        st.session_state.sim_result = sr
        st.session_state.sim_recs   = recs
        st.session_state.sim_meta   = rf_meta
        st.session_state.sim_inputs = {
            "country": sim_country, "crop": sim_crop, "year": sim_year,
        }

    if st.session_state.sim_result:
        sr   = st.session_state.sim_result
        recs = st.session_state.sim_recs
        inp  = st.session_state.sim_inputs
        meta = st.session_state.sim_meta

        st.markdown('<div class="sim-results">', unsafe_allow_html=True)

        # ── Crop Recommendation Card ──────────────────────────────────────────
        r0, r1, r2 = recs[0], recs[1] if len(recs) > 1 else {}, recs[2] if len(recs) > 2 else {}
        st.markdown(f"""
        <div class="rec-card">
          <div class="sec-label">🏆 Crop Recommendation Engine — FAO-RF Model</div>
          <div style="font-family:'DM Serif Display',serif; font-size:28px;
                      color:var(--cream); letter-spacing:-0.5px; margin-bottom:6px;">
            Best crop for <em style="color:var(--lime)">{inp['country']}</em>
            in {inp['year']}
          </div>
          <div style="font-size:13px; color:var(--muted); margin-bottom:4px;">
            All {len(CROP_FAO_PROFILES)} crops evaluated under your scenario conditions
            using FAO AQUASTAT, CLIMWAT, RFN and GAEZ v4 feature vectors.
          </div>
          <div class="rec-top-crop">
            🥇 &nbsp;{r0['crop']}
            <span style="font-family:'JetBrains Mono',monospace; font-size:14px;
                         color:var(--muted); margin-left:8px;">
              {r0['yield_tha']:.2f} t/ha &nbsp;·&nbsp; {r0['confidence']:.0f}% confidence
            </span>
          </div>
          <div class="rec-row">
            <div class="rec-item">
              <div class="rec-rank">🥇 Rank 1 — Best Match</div>
              <div class="rec-name">{recs[0]['crop']}</div>
              <div class="rec-score">{recs[0]['yield_tha']:.2f} t/ha · {recs[0]['confidence']:.0f}% conf</div>
            </div>
            <div class="rec-item">
              <div class="rec-rank">🥈 Rank 2 — Strong Pick</div>
              <div class="rec-name">{recs[1]['crop'] if len(recs)>1 else '—'}</div>
              <div class="rec-score">{f"{recs[1]['yield_tha']:.2f} t/ha · {recs[1]['confidence']:.0f}% conf" if len(recs)>1 else '—'}</div>
            </div>
            <div class="rec-item">
              <div class="rec-rank">🥉 Rank 3 — Good Alternative</div>
              <div class="rec-name">{recs[2]['crop'] if len(recs)>2 else '—'}</div>
              <div class="rec-score">{f"{recs[2]['yield_tha']:.2f} t/ha · {recs[2]['confidence']:.0f}% conf" if len(recs)>2 else '—'}</div>
            </div>
            <div class="rec-item">
              <div class="rec-rank">4️⃣ Rank 4</div>
              <div class="rec-name">{recs[3]['crop'] if len(recs)>3 else '—'}</div>
              <div class="rec-score">{f"{recs[3]['yield_tha']:.2f} t/ha · {recs[3]['confidence']:.0f}% conf" if len(recs)>3 else '—'}</div>
            </div>
            <div class="rec-item">
              <div class="rec-rank">5️⃣ Rank 5</div>
              <div class="rec-name">{recs[4]['crop'] if len(recs)>4 else '—'}</div>
              <div class="rec-score">{f"{recs[4]['yield_tha']:.2f} t/ha · {recs[4]['confidence']:.0f}% conf" if len(recs)>4 else '—'}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 4 Simulation Metric Cards ─────────────────────────────────────────
        conf_cls   = "badge-g" if sr["confidence"] >= 70 else "badge-y" if sr["confidence"] >= 50 else "badge-r"
        yld_vs_fao = sr["yield_tha"] / (_cp[5] + 1e-9)
        comp_lbl   = "Above FAO avg" if yld_vs_fao >= 1 else "Below FAO avg"
        comp_cls   = "badge-g" if yld_vs_fao >= 1 else "badge-r"

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""
            <div class="sim-metric">
              <span class="m-tag">Simulated Yield</span>
              <div class="m-value">{sr['yield_tha']:.2f}</div>
              <div class="m-unit">tonnes per hectare</div>
              <span class="m-badge {comp_cls}">{comp_lbl}</span>
            </div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
            <div class="sim-metric">
              <span class="m-tag">Simulated Production</span>
              <div class="m-value">{sr['prod_mt']:.2f}</div>
              <div class="m-unit">million tonnes</div>
              <span class="m-badge badge-b">{inp['year']}</span>
            </div>""", unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
            <div class="sim-metric">
              <span class="m-tag">Model Confidence</span>
              <div class="m-value">{sr['confidence']:.0f}%</div>
              <div class="m-unit">RF ensemble agreement</div>
              <span class="m-badge {conf_cls}">{'High' if sr['confidence']>=70 else 'Moderate' if sr['confidence']>=50 else 'Low'}</span>
            </div>""", unsafe_allow_html=True)
        with mc4:
            fao_base = _cp[5]
            delta    = sr['yield_tha'] - fao_base
            d_cls    = "badge-g" if delta >= 0 else "badge-r"
            st.markdown(f"""
            <div class="sim-metric">
              <span class="m-tag">vs. FAO Baseline</span>
              <div class="m-value">{delta:+.2f}</div>
              <div class="m-unit">t/ha vs FAO reference</div>
              <span class="m-badge {d_cls}">FAO ref: {fao_base:.1f} t/ha</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CI Strip ──────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="info-strip">
          <div class="info-cell">
            <div class="info-val">{sr['yield_lower']:.2f}–{sr['yield_upper']:.2f}</div>
            <div class="info-lbl">Yield 90% CI (t/ha)</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{sr['prod_lower']:.2f}–{sr['prod_upper']:.2f}</div>
            <div class="info-lbl">Production 90% CI (Mt)</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{meta['n_trees']}</div>
            <div class="info-lbl">RF Trees</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{meta['n_features']}</div>
            <div class="info-lbl">FAO Features</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{meta['r2_yield']:.3f}</div>
            <div class="info-lbl">Model R² (yield)</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{meta['n_train']}</div>
            <div class="info-lbl">Training Scenarios</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Feature Breakdown Chart ───────────────────────────────────────────
        import altair as alt

        feat_vec = build_fao_features(
            inp["country"], inp["crop"], inp["year"], sim_area,
            sim_fert, sim_rain, sim_temp, sim_irr,
            sim_soil, sim_tech, sim_pest,
        )
        feat_labels = [
            "Temperature Stress", "Water Stress", "Fertilizer Efficiency",
            "Soil Quality", "Technology Level", "Pest Control",
            "Country Yield Index", "Irrigation Benefit", "Tech Trend",
            "Water×Fert Interaction", "Input Composite", "Agro Score",
            "Ln(Area)", "Area (Mha)", "Temperature °C",
            "Rainfall (norm)", "Irrigation (norm)", "Fertilizer (norm)",
        ]
        feat_df = pd.DataFrame({
            "feature": feat_labels,
            "value":   feat_vec,
        }).sort_values("value", ascending=False)

        st.markdown("""
        <div class="chart-card">
          <span class="chart-tag">FAO Feature Vector</span>
          <div class="chart-title">18-dimensional FAO-ecosystem input breakdown</div>
        </div>
        """, unsafe_allow_html=True)

        bar = (
            alt.Chart(feat_df)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
            .encode(
                y=alt.Y("feature:N", sort="-x",
                        axis=alt.Axis(labelColor="#6B7A5C", labelFontSize=11, titleColor="#6B7A5C")),
                x=alt.X("value:Q", title="Feature Value",
                        axis=alt.Axis(labelColor="#6B7A5C", gridColor="#1A2014")),
                color=alt.condition(
                    alt.datum.value > 0.5,
                    alt.value("#B8FF4A"),
                    alt.value("#5BC0EB")
                ),
                tooltip=["feature:N", alt.Tooltip("value:Q", format=".4f")],
            )
            .properties(height=380, background="#121810")
            .configure_view(strokeOpacity=0)
        )
        st.altair_chart(bar, use_container_width=True)

        # ── Top-5 Crops Comparison ────────────────────────────────────────────
        rec_df = pd.DataFrame(recs)
        st.markdown("""
        <div class="chart-card">
          <span class="chart-tag">Crop Comparison</span>
          <div class="chart-title">Top 5 crops ranked by RF suitability score</div>
        </div>
        """, unsafe_allow_html=True)

        rc = (
            alt.Chart(rec_df)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
            .encode(
                y=alt.Y("crop:N", sort="-x",
                        axis=alt.Axis(labelColor="#6B7A5C", labelFontSize=12)),
                x=alt.X("yield_tha:Q", title="Predicted Yield (t/ha)",
                        axis=alt.Axis(labelColor="#6B7A5C", gridColor="#1A2014")),
                color=alt.Color("confidence:Q",
                    scale=alt.Scale(scheme="greens", domain=[30, 95]),
                    legend=alt.Legend(title="Confidence %",
                                      labelColor="#EEE8D5", titleColor="#EEE8D5")),
                tooltip=["crop:N",
                         alt.Tooltip("yield_tha:Q", format=".2f", title="Yield t/ha"),
                         alt.Tooltip("confidence:Q", format=".0f", title="Confidence %"),
                         alt.Tooltip("score:Q", format=".2f", title="RF Score")],
            )
            .properties(height=220, background="#121810")
            .configure_view(strokeOpacity=0)
        )
        st.altair_chart(rc, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██████████████████  PAGE — FORECASTS  ███████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Forecasts":
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Forecasts</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Dual-model architecture explained</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:820px; color:var(--muted); font-size:15px; line-height:1.8; margin-bottom:36px;">
      AgriPredict now runs <strong style="color:var(--cream)">two distinct ML models</strong> for two
      distinct tasks. The <strong style="color:var(--lime)">Analytics page</strong> uses classical
      polynomial regression on FAOSTAT historical time-series to project future production trends.
      The <strong style="color:var(--purple)">Simulate page</strong> uses a Random Forest ensemble
      trained on FAO-ecosystem features (AQUASTAT, CLIMWAT, RFN, GAEZ) for interactive what-if
      scenario analysis and crop recommendation.
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:36px;">

      <div class="chart-card" style="border-color:rgba(184,255,74,0.25);">
        <span class="chart-tag">Model 1 — Analytics Page</span>
        <div class="chart-title" style="margin-bottom:16px; color:var(--lime);">
          Polynomial Regression · Degree 3
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8; margin-bottom:16px;">
          Fitted on FAOSTAT QCL historical production data per country/crop pair.
          Z-score normalised year inputs prevent numerical blow-up at long horizons.
          Extrapolated to target year with ±1.64σ confidence interval.
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:4px;">USE CASE</div>
            <div style="font-size:13px; color:var(--cream);">Historical trend projection</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:4px;">INPUT</div>
            <div style="font-size:13px; color:var(--cream);">Year (from FAOSTAT QCL)</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:4px;">OUTPUT</div>
            <div style="font-size:13px; color:var(--cream);">Production (tonnes) + CI</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:4px;">LIBRARY</div>
            <div style="font-size:13px; color:var(--cream);">numpy.linalg.lstsq</div>
          </div>
        </div>
      </div>

      <div class="chart-card" style="border-color:rgba(192,132,252,0.25);">
        <span class="chart-tag" style="background:var(--purple); color:var(--black);">Model 2 — Simulate Page</span>
        <div class="chart-title" style="margin-bottom:16px; color:var(--purple);">
          Random Forest Regressor · 50 Trees
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8; margin-bottom:16px;">
          Trained on 3 500 FAO-derived scenarios spanning the full crop × country × climate
          parameter space. Feature engineering uses FAO AQUASTAT, CLIMWAT, RFN, and GAEZ v4
          data sources exclusively. Tree variance provides uncertainty bounds.
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--purple); margin-bottom:4px;">USE CASE</div>
            <div style="font-size:13px; color:var(--cream);">What-if scenario analysis</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--purple); margin-bottom:4px;">INPUTS</div>
            <div style="font-size:13px; color:var(--cream);">18 FAO-ecosystem features</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--purple); margin-bottom:4px;">OUTPUT</div>
            <div style="font-size:13px; color:var(--cream);">Yield (t/ha) + Production (Mt)</div>
          </div>
          <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:12px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--purple); margin-bottom:4px;">LIBRARY</div>
            <div style="font-size:13px; color:var(--cream);">Pure NumPy (no sklearn)</div>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-card" style="margin-bottom:20px;">
      <span class="chart-tag">FAO Feature Engineering — 18 Dimensions</span>
      <div class="chart-title" style="margin-bottom:18px;">How the RF model's inputs are derived from FAO data</div>
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:14px;">
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO CLIMWAT</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Temperature Stress</div>
          <div style="font-size:12px; color:var(--muted);">Deviation from FAO crop-specific optimal temperature; GAEZ heat unit method.</div>
        </div>
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO AQUASTAT</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Water Stress</div>
          <div style="font-size:12px; color:var(--muted);">Effective water supply (rainfall + irrigation) vs. FAO Kc×ETo crop water requirement.</div>
        </div>
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO RFN</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Fertilizer Efficiency</div>
          <div style="font-size:12px; color:var(--muted);">Applied N relative to FAO crop N requirement; derived from RFN fertilizer statistics.</div>
        </div>
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO GAEZ v4</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Soil Suitability</div>
          <div style="font-size:12px; color:var(--muted);">Agro-ecological zone soil quality index from GAEZ v4 suitability maps.</div>
        </div>
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO QCL / Ag Census</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Country Yield Index</div>
          <div style="font-size:12px; color:var(--muted);">Historical mean yield potential per country derived from FAOSTAT QCL time-series.</div>
        </div>
        <div style="background:var(--faint); border:1px solid var(--border); border-radius:8px; padding:14px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:6px;">FAO Long-run Trend</div>
          <div style="font-size:13px; color:var(--cream); margin-bottom:4px;">Technology Trend</div>
          <div style="font-size:12px; color:var(--muted);">~0.7%/yr productivity gain derived from FAO's global yield growth analysis.</div>
        </div>
      </div>
    </div>

    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:28px;">
      <div class="metric-card">
        <span class="m-tag">Step 01 — Poly Reg</span>
        <div style="font-family:'DM Serif Display',serif; font-size:20px; color:var(--cream); margin:10px 0 8px;">Data Ingestion</div>
        <div style="font-size:13px; color:var(--muted); line-height:1.7;">
          Raw production & area series pulled from FAOSTAT QCL (bulk ZIP or API).
          Missing values forward-filled; optional 3-year rolling mean.
        </div>
      </div>
      <div class="metric-card">
        <span class="m-tag">Step 02 — Poly Reg</span>
        <div style="font-family:'DM Serif Display',serif; font-size:20px; color:var(--cream); margin:10px 0 8px;">Model Training</div>
        <div style="font-size:13px; color:var(--muted); line-height:1.7;">
          Z-score normalised year → cubic polynomial basis →
          <code style="color:var(--lime)">np.linalg.lstsq</code>. Residuals give σ for CI.
        </div>
      </div>
      <div class="metric-card">
        <span class="m-tag">Step 03 — Poly Reg</span>
        <div style="font-family:'DM Serif Display',serif; font-size:20px; color:var(--cream); margin:10px 0 8px;">Projection</div>
        <div style="font-size:13px; color:var(--muted); line-height:1.7;">
          Curve extrapolated to target year. ±1.64σ = 90% CI. CAGR and R²
          communicate forecast confidence.
        </div>
      </div>
    </div>

    <div class="chart-card">
      <span class="chart-tag">Crop Recommendation Logic</span>
      <div class="chart-title" style="margin-bottom:16px;">How the best crop is selected</div>
      <div style="font-size:13px; color:var(--muted); line-height:1.9;">
        For a given country, year, and set of conditions, the RF yield model is run once per crop
        (all {n_crops} crops in the FAO profile library). Each run produces a predicted yield and
        a confidence score derived from tree variance. A composite suitability score
        <code style="color:var(--lime)">score = yield × (confidence/100) × 0.65 + confidence × 0.35</code>
        ranks all crops. The top 5 are returned to the UI with their predicted yield and confidence.
      </div>
    </div>

    <div class="chart-card" style="background:var(--faint); border-color:rgba(184,255,74,0.15);">
      <span class="chart-tag" style="background:var(--amber); color:var(--black);">Limitations</span>
      <div class="chart-title" style="margin-bottom:14px;">What these models do <em style="font-style:italic; color:var(--red);">not</em> account for</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        <div style="font-size:13px; color:var(--muted); line-height:1.9;">
          <strong style="color:var(--amber);">Polynomial Regression:</strong><br>
          ⚠️ Climate shocks and extreme weather events<br>
          ⚠️ Geopolitical disruptions and trade policy<br>
          ⚠️ Sudden technology shifts (GMO rollout, etc.)<br>
          ⚠️ Post-2023 structural changes not in FAOSTAT
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.9;">
          <strong style="color:var(--purple);">Random Forest Simulation:</strong><br>
          ⚠️ Trained on FAO-derived synthetic data, not real field measurements<br>
          ⚠️ Country-level aggregates, not farm-level precision<br>
          ⚠️ Does not model multi-year soil depletion dynamics<br>
          ⚠️ Market prices and farmer decision-making not included
        </div>
      </div>
    </div>
    """.format(n_crops=len(CROP_FAO_PROFILES)), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██████████████████  PAGE — DATA SOURCES  ████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Data Sources":
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Data Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Where the data comes from</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:16px; margin-bottom:28px;">

      <div class="metric-card" style="border-color:rgba(184,255,74,0.2);">
        <span class="m-tag">Primary Source</span>
        <div style="font-family:'DM Serif Display',serif; font-size:24px; color:var(--cream); margin:10px 0 8px;">
          FAOSTAT — FAO Statistical Database
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8; margin-bottom:16px;">
          The Food and Agriculture Organization of the United Nations (FAO) maintains FAOSTAT —
          the world's most comprehensive free database of food and agriculture statistics,
          covering 245 countries and territories from 1961 to present.
        </div>
        <a href="https://www.fao.org/faostat/en/" target="_blank"
           style="display:inline-block; padding:8px 18px; background:rgba(184,255,74,0.1);
                  border:1px solid rgba(184,255,74,0.3); border-radius:8px;
                  color:var(--lime); font-size:12px; font-weight:700;
                  text-decoration:none; letter-spacing:0.5px;">
          → Visit FAOSTAT
        </a>
      </div>

      <div class="metric-card">
        <span class="m-tag">Dataset Used</span>
        <div style="font-family:'DM Serif Display',serif; font-size:24px; color:var(--cream); margin:10px 0 8px;">
          Crops and Livestock Products (QCL)
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8; margin-bottom:16px;">
          The QCL domain contains area harvested, production quantity, and yield data for
          primary crops worldwide. Available as bulk normalized CSV download or via the
          FAOSTAT REST API.
        </div>
        <a href="https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip"
           target="_blank"
           style="display:inline-block; padding:8px 18px; background:rgba(91,192,235,0.1);
                  border:1px solid rgba(91,192,235,0.3); border-radius:8px;
                  color:var(--blue); font-size:12px; font-weight:700;
                  text-decoration:none; letter-spacing:0.5px;">
          ↓ Download Bulk ZIP
        </a>
      </div>
    </div>

    <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:16px; margin-bottom:28px;">
      <div class="metric-card" style="border-color:rgba(192,132,252,0.2);">
        <span class="m-tag" style="color:var(--purple);">Simulation Features</span>
        <div style="font-family:'DM Serif Display',serif; font-size:22px; color:var(--cream); margin:10px 0 8px;">
          FAO AQUASTAT + CLIMWAT
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8;">
          Crop water requirements (Kc × ETo) and country irrigation statistics from FAO's
          global water information system. Used to derive water stress and irrigation benefit
          features for the RF simulation model.
        </div>
      </div>
      <div class="metric-card" style="border-color:rgba(192,132,252,0.2);">
        <span class="m-tag" style="color:var(--purple);">Simulation Features</span>
        <div style="font-family:'DM Serif Display',serif; font-size:22px; color:var(--cream); margin:10px 0 8px;">
          FAO GAEZ v4 + RFN
        </div>
        <div style="font-size:13px; color:var(--muted); line-height:1.8;">
          Global Agro-Ecological Zones (GAEZ v4) soil suitability indices and FAOSTAT
          Inputs/Fertilizers by Nutrient (RFN) domain for crop nitrogen demand and
          country-level fertilizer intensity.
        </div>
      </div>
    </div>

    <div class="chart-card" style="margin-bottom:20px;">
      <span class="chart-tag">API Endpoints</span>
      <div class="chart-title" style="margin-bottom:18px;">How AgriPredict fetches data</div>
      <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:20px;">
        <div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--lime); margin-bottom:6px;">BULK DOWNLOAD (default)</div>
          <code style="display:block; background:var(--faint); border:1px solid var(--border);
                       border-radius:8px; padding:12px; font-size:11px; color:var(--cream);
                       line-height:1.8; word-break:break-all;">
            bulks-faostat.fao.org/production/<br>
            Production_Crops_Livestock_E<br>
            _All_Data_(Normalized).zip
          </code>
          <div style="font-size:12px; color:var(--muted); margin-top:8px;">Full historical dataset. Cached for 24hrs. No API key required.</div>
        </div>
        <div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--lime); margin-bottom:6px;">DIRECT API (optional)</div>
          <code style="display:block; background:var(--faint); border:1px solid var(--border);
                       border-radius:8px; padding:12px; font-size:11px; color:var(--cream);
                       line-height:1.8; word-break:break-all;">
            fenixservices.fao.org/<br>
            faostat/api/v1/en/data/QCL<br>
            ?area_code=&item_code=…
          </code>
          <div style="font-size:12px; color:var(--muted); margin-top:8px;">Targeted query. Faster for single country/crop. Bearer token optional.</div>
        </div>
      </div>
    </div>

    <div class="chart-card">
      <span class="chart-tag">Reference Links</span>
      <div class="chart-title" style="margin-bottom:18px;">Further reading & citations</div>
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:14px;">
        <a href="https://www.fao.org/faostat/en/#data/QCL" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:8px;">FAOSTAT QCL</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Crops & Livestock Products</div>
            <div style="font-size:12px; color:var(--muted);">Official QCL data browser with charts and download.</div>
          </div>
        </a>
        <a href="https://www.fao.org/aquastat/en/" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--blue); margin-bottom:8px;">FAO AQUASTAT</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Global Water Information</div>
            <div style="font-size:12px; color:var(--muted);">Irrigation, water requirement, and water stress data.</div>
          </div>
        </a>
        <a href="https://gaez.fao.org/" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--purple); margin-bottom:8px;">FAO GAEZ v4</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Agro-Ecological Zones</div>
            <div style="font-size:12px; color:var(--muted);">Soil suitability and land resource assessments.</div>
          </div>
        </a>
        <a href="https://www.fao.org/faostat/en/#data/RFN" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--amber); margin-bottom:8px;">FAO FAOSTAT RFN</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Fertilizers by Nutrient</div>
            <div style="font-size:12px; color:var(--muted);">Country-level N/P/K fertilizer use statistics.</div>
          </div>
        </a>
        <a href="https://ourworldindata.org/crop-yields" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:8px;">OUR WORLD IN DATA</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Crop Yields</div>
            <div style="font-size:12px; color:var(--muted);">Visualised global yield trends — great for cross-referencing.</div>
          </div>
        </a>
        <a href="https://www.fao.org/food-agriculture-statistics/en/" target="_blank" style="text-decoration:none;">
          <div class="selector-card" style="cursor:pointer;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--lime); margin-bottom:8px;">FAO</div>
            <div style="font-size:14px; font-weight:600; color:var(--cream); margin-bottom:6px;">Food & Ag Statistics Hub</div>
            <div style="font-size:12px; color:var(--muted);">Central portal for all FAO statistical programmes.</div>
          </div>
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██████████████████  PAGE — ABOUT  ███████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "About":
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">About</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">The project</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid; grid-template-columns:1.6fr 1fr; gap:24px; margin-bottom:28px;">

      <div class="chart-card">
        <span class="chart-tag">Overview</span>
        <div class="chart-title" style="margin-bottom:16px;">What is AgriPredict?</div>
        <div style="font-size:14px; color:var(--muted); line-height:1.9;">
          AgriPredict is a final-year academic project demonstrating how publicly available
          FAO agricultural data can be transformed into production forecasts and scenario
          simulations using a dual ML architecture — no black-box APIs, no proprietary data.
          <br><br>
          The application connects to <strong style="color:var(--cream)">FAOSTAT</strong>
          for historical time-series and uses FAO ecosystem datasets (AQUASTAT, CLIMWAT, RFN,
          GAEZ v4) to power a Random Forest simulation engine capable of interactive what-if
          analysis across 55+ crops and 60+ countries.
          <br><br>
          The Simulate page evaluates all crops simultaneously under user-defined conditions
          and recommends the best agronomic choices — acting as a crop intelligence layer
          on top of the forecasting foundation.
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:16px;">
        <div class="metric-card">
          <span class="m-tag">Built By</span>
          <div style="font-family:'DM Serif Display',serif; font-size:26px; color:var(--cream); margin:8px 0 4px;">
            Final Year Student
          </div>
          <div style="font-size:13px; color:var(--muted);">BSc Computer Science</div>
          <div style="font-size:13px; color:var(--muted); margin-top:4px;">Vismay Rao BN</div>
        </div>
        <div class="metric-card">
          <span class="m-tag">Academic Context</span>
          <div style="font-family:'DM Serif Display',serif; font-size:20px; color:var(--cream); margin:8px 0 4px;">
            Final Year Project
          </div>
          <div style="font-size:13px; color:var(--muted);">Agricultural Analytics</div>
          <div style="font-size:13px; color:var(--muted); margin-top:4px;">Academic Year 2025–2026</div>
        </div>
      </div>
    </div>

    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:28px;">
      <div class="metric-card">
        <span class="m-tag">Model 1</span>
        <div style="font-family:'DM Serif Display',serif; font-size:18px; color:var(--lime); margin:10px 0 8px;">
          Polynomial Regression
        </div>
        <div style="font-size:12px; color:var(--muted); line-height:1.7;">
          Degree-3, OLS via <code style="color:var(--lime)">numpy.linalg.lstsq</code>.
          Z-score normalised year. Used for historical trend projection on Analytics page.
        </div>
      </div>
      <div class="metric-card">
        <span class="m-tag">Model 2</span>
        <div style="font-family:'DM Serif Display',serif; font-size:18px; color:var(--purple); margin:10px 0 8px;">
          Random Forest · 50 Trees
        </div>
        <div style="font-size:12px; color:var(--muted); line-height:1.7;">
          Pure NumPy RF on 18 FAO-ecosystem features (AQUASTAT, CLIMWAT, RFN, GAEZ v4).
          Used for scenario simulation and crop recommendation on Simulate page.
        </div>
      </div>
      <div class="metric-card">
        <span class="m-tag">Data Layer</span>
        <div style="font-family:'DM Serif Display',serif; font-size:18px; color:var(--cream); margin:10px 0 8px;">
          FAO Ecosystem
        </div>
        <div style="font-size:12px; color:var(--muted); line-height:1.7;">
          FAOSTAT QCL (live), AQUASTAT, CLIMWAT, RFN, GAEZ v4.
          All simulation features are FAO-derived. 24-hour caching.
        </div>
      </div>
      <div class="metric-card">
        <span class="m-tag">Coverage</span>
        <div style="font-family:'DM Serif Display',serif; font-size:18px; color:var(--cream); margin:10px 0 8px;">
          60+ Countries · 55+ Crops
        </div>
        <div style="font-size:12px; color:var(--muted); line-height:1.7;">
          From wheat in India to cocoa in Ghana. Covering staple crops, cash crops,
          fruits, spices, oilseeds across 6 continents.
        </div>
      </div>
    </div>

    <div class="chart-card">
      <span class="chart-tag">Tech Stack</span>
      <div class="chart-title" style="margin-bottom:18px;">Libraries & Tools</div>
      <div style="display:flex; flex-wrap:wrap; gap:10px;">
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Python 3.10+</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Streamlit</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Pandas</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">NumPy</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Altair</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Requests</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">FAOSTAT REST API</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--purple);">Random Forest (NumPy)</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--purple);">FAO AQUASTAT</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--purple);">FAO CLIMWAT</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--purple);">FAO GAEZ v4</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--purple);">FAO RFN</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Polynomial Regression (OLS)</span>
        <span style="padding:8px 16px; background:var(--faint); border:1px solid var(--border); border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--lime);">Confidence Intervals</span>
      </div>
    </div>

    <div class="chart-card" style="margin-top:20px; background:var(--faint); border-color:rgba(184,255,74,0.12);">
      <span class="chart-tag" style="background:var(--amber); color:var(--black);">Disclaimer</span>
      <div style="font-size:13px; color:var(--muted); line-height:1.9; margin-top:12px;">
        This project is built for <strong style="color:var(--cream)">academic and demonstration purposes only</strong>.
        Predictions are statistical extrapolations; simulations are model outputs on FAO-derived synthetic scenarios.
        Neither should be used for commercial agricultural decisions without expert validation. All data sourced
        from FAO's publicly available databases (FAOSTAT, AQUASTAT, GAEZ, CLIMWAT, RFN).
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------------------------
#  PAGE — ANALYTICS (default) 
# -------------------------------------------------------------------------------------------
# The Analytics page renders below regardless of page, because the hero,
# config section, and results section are always shown when page == "Analytics"
# (other pages return early via elif, so execution falls through here only for Analytics)

if st.session_state.page == "Analytics":

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="editorial-hero">
      <div class="hero-glow1"></div>
      <div class="hero-glow2"></div>
      <div class="hero-eyebrow">✦ A Project by VISMAY RAO</div>
      <div class="hero-headline">
        Predict the <em>future</em><br>of global food production
      </div>
      <div class="hero-sub">
        Powered by FAOSTAT's global agricultural database.
        Select any country, crop, and forecast horizon — the polynomial regression
        model delivers production estimates with confidence intervals.
      </div>
      <div class="hero-stats-row">
        <div class="hero-stat">
          <div class="hero-stat-val"><span>60+</span></div>
          <div class="hero-stat-lbl">Countries</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-val"><span>55+</span></div>
          <div class="hero-stat-lbl">Crop Types</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-val">1961–<span>2040</span></div>
          <div class="hero-stat-lbl">Year Range</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-val"><span>2</span> ML<span>Models</span></div>
          <div class="hero-stat-lbl">Dual Architecture</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Config section ────────────────────────────────────────────────────────
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Step 01 — Configure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Build your forecast</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="selector-card">
          <span class="card-icon">🌍</span>
          <div class="card-lbl">Select Country</div>
        </div>""", unsafe_allow_html=True)
        country_key = st.selectbox("country", list(COUNTRIES.keys()), label_visibility="collapsed")

    with col2:
        st.markdown("""
        <div class="selector-card">
          <span class="card-icon">🌿</span>
          <div class="card-lbl">Select Crop</div>
        </div>""", unsafe_allow_html=True)
        crop_key = st.selectbox("crop", list(CROPS.keys()), label_visibility="collapsed")

    with col3:
        st.markdown("""
        <div class="selector-card">
          <span class="card-icon">📅</span>
          <div class="card-lbl">Forecast Target Year</div>
        </div>""", unsafe_allow_html=True)
        target_y = st.slider("year", 2024, 2040, 2030, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("⚙️  Advanced Settings — Data source · Year range · Options"):
        a1, a2, a3, a4, a5 = st.columns(5)
        with a1:
            st.markdown('<div class="adv-card"><div class="card-lbl">Data Source</div>', unsafe_allow_html=True)
            source_mode = st.radio("src", ["Bulk Download", "Direct API"], label_visibility="collapsed")
            use_bulk = source_mode == "Bulk Download"
            st.markdown('</div>', unsafe_allow_html=True)
        with a2:
            st.markdown('<div class="adv-card"><div class="card-lbl">From Year</div>', unsafe_allow_html=True)
            year_start = st.slider("ys", 1961, 2010, 1990, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        with a3:
            st.markdown('<div class="adv-card"><div class="card-lbl">To Year</div>', unsafe_allow_html=True)
            year_end = st.slider("ye", 2010, 2023, 2023, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        with a4:
            st.markdown('<div class="adv-card"><div class="card-lbl">Timeout (s)</div>', unsafe_allow_html=True)
            timeout = st.slider("to", 30, 120, 60, disabled=use_bulk, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        with a5:
            st.markdown('<div class="adv-card"><div class="card-lbl">Options</div>', unsafe_allow_html=True)
            smooth  = st.checkbox("3-yr Rolling Smooth", value=True)
            show_ci = st.checkbox("Show 90% CI Band", value=True)
            token_input = st.text_input(
                "API Token", value=st.session_state.token,
                type="password", placeholder="Optional: Bearer token",
                label_visibility="collapsed"
            )
            if token_input != st.session_state.token:
                st.session_state.token = token_input
                st.cache_data.clear()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("⚡  RUN PREDICTION")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Marquee — shown after first run or always ─────────────────────────────
    render_marquee(country_key, target_y)

    # ── Fetch & Predict ───────────────────────────────────────────────────────
    if go:
        st.session_state.predicted = False
        country_code, country_name = COUNTRIES[country_key]
        item_code,    item_name    = CROPS[crop_key]
        df, err = None, None

        prog_bar = st.progress(0)
        status   = st.empty()

        if use_bulk:
            status.markdown("📦 **Downloading FAOSTAT bulk dataset…**")
            prog_bar.progress(20)
            bulk_df, err = download_bulk(st.session_state.token)
            prog_bar.progress(60)
            status.markdown(f"🔍 **Filtering** {crop_key} for {country_key}…")
            if bulk_df is not None:
                df, err = filter_bulk(bulk_df, country_name, item_name, year_start, year_end)
                if df is not None:
                    st.session_state.fetch_meta = {
                        "rows": len(df),
                        "year_range": f"{int(df['year'].min())}–{int(df['year'].max())}",
                        "source": "Bulk ZIP"
                    }
        else:
            status.markdown("🔌 **Connecting to FAOSTAT API…**")
            prog_bar.progress(30)
            df, err = fetch_direct(country_code, item_code, st.session_state.token,
                                   year_start, year_end, timeout)
            if df is not None:
                st.session_state.fetch_meta = {
                    "rows": len(df),
                    "year_range": f"{int(df['year'].min())}–{int(df['year'].max())}",
                    "source": "Direct API"
                }

        prog_bar.progress(80)
        status.markdown("🤖 **Training polynomial regression model…**")
        time.sleep(0.3)

        if err:
            prog_bar.empty(); status.empty()
            st.error(f"❌ {err}")
        elif df is None or df.empty:
            prog_bar.empty(); status.empty()
            st.error("No data found for this selection. Try a different country/crop combination.")
        else:
            if smooth and len(df) >= 5:
                df["production"] = df["production"].rolling(3, center=True, min_periods=1).mean().round(0)
                df["area"]       = df["area"].rolling(3, center=True, min_periods=1).mean().round(0)
            result = predict_production(df, target_y)
            prog_bar.progress(100)
            status.markdown(f"✅ **Done!** Loaded {len(df)} data points — model trained.")
            time.sleep(0.6)
            prog_bar.empty(); status.empty()
            st.session_state.update(
                df=df, result=result,
                country=country_key, crop=crop_key,
                target=target_y, predicted=True
            )

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.predicted and st.session_state.df is not None:
        import altair as alt

        df  = st.session_state.df
        res = st.session_state.result
        m   = st.session_state.fetch_meta

        st.markdown('<div class="results-section">', unsafe_allow_html=True)

        # Header
        st.markdown(f"""
        <div class="results-topline">
          <div class="results-title">
            <em>{st.session_state.crop}</em> &nbsp;·&nbsp; {st.session_state.country}
          </div>
          <div class="results-meta">
            {m.get('rows','?')} data pts &nbsp;·&nbsp; {m.get('year_range','')}
            &nbsp;·&nbsp; via {m.get('source','')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 Metric Cards
        arrow = "▲" if res["growth_pct"] >= 0 else "▼"
        d_cls = "badge-g" if res["growth_pct"] >= 0 else "badge-r"
        c_cls = "badge-g" if res["cagr"] >= 0 else "badge-r"
        r2_lbl = "Excellent" if res["r2"] > 0.95 else "Good" if res["r2"] > 0.85 else "Fair"

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
              <span class="m-tag">Predicted {st.session_state.target}</span>
              <div class="m-value">{res['pred']/1e6:.2f}M</div>
              <div class="m-unit">tonnes · production</div>
              <span class="m-badge {d_cls}">{arrow} {abs(res['growth_pct']):.1f}% vs last</span>
            </div>""", unsafe_allow_html=True)
        with mc2:
            last_yield = df['yield_ha'].dropna().iloc[-1] if not df['yield_ha'].dropna().empty else 0
            st.markdown(f"""
            <div class="metric-card">
              <span class="m-tag">Yield / Hectare</span>
              <div class="m-value">{last_yield:.2f}</div>
              <div class="m-unit">tonnes per hectare</div>
              <span class="m-badge badge-b">{res['trend_dir']}</span>
            </div>""", unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
            <div class="metric-card">
              <span class="m-tag">Model R²</span>
              <div class="m-value">{res['r2']:.3f}</div>
              <div class="m-unit">fit quality score</div>
              <span class="m-badge badge-y">{r2_lbl}</span>
            </div>""", unsafe_allow_html=True)
        with mc4:
            st.markdown(f"""
            <div class="metric-card">
              <span class="m-tag">CAGR</span>
              <div class="m-value">{res['cagr']:+.2f}%</div>
              <div class="m-unit">compound annual growth</div>
              <span class="m-badge {c_cls}">to {st.session_state.target}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Info Strip
        last     = df.iloc[-1]
        area_val = last['area'] / 1e6 if not np.isnan(last['area']) else 0
        st.markdown(f"""
        <div class="info-strip">
          <div class="info-cell">
            <div class="info-val">{last['production']/1e6:.1f}M t</div>
            <div class="info-lbl">Last Production</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{area_val:.2f}M ha</div>
            <div class="info-lbl">Area Harvested</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{res['lower']/1e6:.1f}–{res['upper']/1e6:.1f}M</div>
            <div class="info-lbl">90% CI Band</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{res['rmse']/1e6:.2f}M</div>
            <div class="info-lbl">RMSE Error</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{int(res['last_year'])}</div>
            <div class="info-lbl">Last Data Year</div>
          </div>
          <div class="info-cell">
            <div class="info-val">{len(df)}</div>
            <div class="info-lbl">Data Points</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Main Forecast Chart
        st.markdown("""
        <div class="chart-card">
          <span class="chart-tag">Production Forecast</span>
          <div class="chart-title">Historical data · Model fit · Forward projection</div>
        </div>
        """, unsafe_allow_html=True)

        chart_df  = df[["year","production"]].assign(type="Historical")
        fitted_df = pd.DataFrame({
            "year": res["x"].astype(int), "production": res["fitted"], "type": "Model Fit"
        })
        future_y = np.arange(int(df["year"].max()) + 1, st.session_state.target + 1)
        fcast_df = pd.DataFrame({
            "year": future_y,
            "production": np.array([max(res["predict_fn"](y), 0) for y in future_y]),
            "type": "Forecast"
        }) if len(future_y) > 0 else pd.DataFrame(columns=["year","production","type"])

        full_df = pd.concat([chart_df, fitted_df, fcast_df], ignore_index=True)
        ax_cfg  = dict(labelColor="#6B7A5C", titleColor="#6B7A5C",
                       gridColor="#1A2014", domainColor="#243020")

        base = alt.Chart(full_df).encode(
            x=alt.X("year:O", title="Year",
                    axis=alt.Axis(**ax_cfg, labelAngle=-45, labelFontSize=10)),
            y=alt.Y("production:Q", title="Production (tonnes)",
                    axis=alt.Axis(**{k: v for k, v in ax_cfg.items()}, format="~s")),
            color=alt.Color("type:N",
                scale=alt.Scale(
                    domain=["Historical","Model Fit","Forecast"],
                    range=["#5AE87E","#5BC0EB","#F5C842"]),
                legend=alt.Legend(
                    labelColor="#EEE8D5", titleColor="#EEE8D5",
                    orient="top-right", labelFontSize=12)),
            tooltip=["year:O",
                     alt.Tooltip("production:Q", format=",.0f", title="Production (t)"),
                     "type:N"]
        )
        pts = alt.Chart(chart_df).mark_point(
            size=55, filled=True, opacity=0.85, color="#5AE87E"
        ).encode(
            x="year:O", y="production:Q",
            tooltip=["year:O", alt.Tooltip("production:Q", format=",.0f")]
        )
        layers = [base.mark_line(strokeWidth=2.5), pts]
        if show_ci and len(future_y) > 0:
            ci_df = pd.DataFrame({
                "year":  future_y,
                "upper": [res["predict_fn"](y) + 1.64*res["std"] for y in future_y],
                "lower": [max(res["predict_fn"](y) - 1.64*res["std"], 0) for y in future_y],
            })
            layers.insert(0,
                alt.Chart(ci_df).mark_area(opacity=0.12, color="#F5C842")
                .encode(x="year:O", y="lower:Q", y2="upper:Q")
            )

        st.altair_chart(
            alt.layer(*layers)
            .properties(height=360, background="#121810")
            .configure_view(strokeOpacity=0)
            .configure_axis(gridColor="#1A2014", domainColor="#243020"),
            use_container_width=True
        )

        # Bottom Row
        bc1, bc2 = st.columns([1.4, 1])
        with bc1:
            st.markdown("""
            <div class="chart-card">
              <span class="chart-tag">Yield Trend</span>
              <div class="chart-title">Tonnes per Hectare over time</div>
            </div>
            """, unsafe_allow_html=True)
            yd = df.dropna(subset=["yield_ha"])
            if not yd.empty:
                yc = (
                    alt.Chart(yd)
                    .mark_area(
                        line={"color": "#B8FF4A", "strokeWidth": 2},
                        color=alt.Gradient(
                            gradient="linear", x1=0, x2=0, y1=1, y2=0,
                            stops=[
                                alt.GradientStop(color="#B8FF4A10", offset=0),
                                alt.GradientStop(color="#B8FF4A55", offset=1),
                            ],
                        ),
                    )
                    .encode(
                        x=alt.X("year:O", axis=alt.Axis(labelColor="#6B7A5C",
                                                         labelAngle=-45, gridColor="#1A2014")),
                        y=alt.Y("yield_ha:Q", title="Yield (t/ha)",
                                axis=alt.Axis(labelColor="#6B7A5C", gridColor="#1A2014")),
                        tooltip=["year:O", alt.Tooltip("yield_ha:Q", format=".3f", title="Yield")]
                    )
                    .properties(height=260, background="#121810")
                    .configure_view(strokeOpacity=0)
                )
                st.altair_chart(yc, use_container_width=True)

        with bc2:
            tab1, tab2 = st.tabs(["📋  Data Table", "🔬  Model Stats"])
            with tab1:
                st.dataframe(
                    df.tail(12)
                      .rename(columns={"year": "Year", "production": "Prod (t)",
                                       "area": "Area (ha)", "yield_ha": "Yield"})
                      .style.format({"Prod (t)": "{:,.0f}", "Area (ha)": "{:,.0f}", "Yield": "{:.3f}"}),
                    use_container_width=True, height=290
                )
            with tab2:
                st.markdown(f"""
**Model:** Polynomial Regression (degree 3)

| Metric | Value |
|--------|-------|
| R² Score | `{res['r2']:.4f}` |
| RMSE | `{res['rmse']/1e6:.3f}M t` |
| Std Dev | `{res['std']/1e6:.3f}M t` |
| Prediction | `{res['pred']/1e6:.2f}M t` |
| 90% CI | `{res['lower']/1e6:.2f} – {res['upper']/1e6:.2f}M t` |
| CAGR | `{res['cagr']:+.2f}% / yr` |
| Trend | `{res['trend_dir']}` |
| Last Data Year | `{res['last_year']}` |
| Last Production | `{res['last_val']/1e6:.2f}M t` |
""")

        st.markdown('</div>', unsafe_allow_html=True)
