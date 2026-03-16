import streamlit as st
import requests
import os
import urllib.parse
import time
import sys
import plotly.graph_objects as go
import pandas as pd

# Core Configuration
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from backend.gemini_agent import analyze_idea
except ImportError:
    from gemini_agent import analyze_idea

st.set_page_config(
    page_title="DeadIdea AI | The Phoenix Protocol",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- THEME TOKENS ---
ACCENT_MINT = "#00FFD2"
ACCENT_ROSE = "#FF006E"
UI_BG = "#030303"
UI_GLASS = "rgba(10, 10, 10, 0.75)"
UI_BORDER = "rgba(0, 255, 210, 0.15)"

API_URL = os.environ.get("API_URL", "http://localhost:8000")

# --- PREMIUM STYLING ENGINE ---
st.markdown(f"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

<style>
    /* Fixed Immersive Background */
    [data-testid="stAppViewContainer"] {{
        background: url('https://raw.githubusercontent.com/yuktha2005/DeadIdea-AI/main/deadidea_ui_background_1773671993980.png'), linear-gradient(135deg, #050505 0%, #0a0a0c 100%);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at center, transparent 0%, {UI_BG} 90%);
        z-index: -1;
    }}

    /* Global Typography */
    * {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .tag-font {{ font-family: 'Outfit', sans-serif !important; letter-spacing: -0.02em; }}

    /* Glass Container */
    .glass-box {{
        background: {UI_GLASS};
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid {UI_BORDER};
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
    }}
    
    .glass-box:hover {{
        border-color: rgba(0, 255, 210, 0.4);
        transform: translateY(-5px);
    }}

    /* Hero Branding */
    .brand-hero {{
        text-align: center;
        padding: 4rem 0 2rem 0;
    }}
    
    .main-title {{
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: 800;
        line-height: 0.9;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #FFF 40%, {ACCENT_MINT} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        filter: drop-shadow(0 15px 15px rgba(0, 255, 210, 0.2));
    }}

    .tagline {{
        color: rgba(255, 255, 255, 0.6);
        font-size: 1.2rem;
        letter-spacing: 0.2rem;
        text-transform: uppercase;
        margin-bottom: 3rem;
    }}

    /* Search Control */
    .stTextInput input {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {UI_BORDER} !important;
        border-radius: 100px !important;
        padding: 20px 40px !important;
        color: white !important;
        font-size: 1.2rem !important;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .stTextInput input:focus {{
        background: rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 0 30px rgba(0, 255, 210, 0.2) !important;
    }}

    /* Futuristic Button */
    .stButton>button {{
        background: {ACCENT_MINT} !important;
        color: {UI_BG} !important;
        border-radius: 100px !important;
        padding: 1rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        letter-spacing: 0.1rem !important;
        text-transform: uppercase !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(0, 255, 210, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        margin: 0 auto;
        display: block;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(0, 255, 210, 0.5) !important;
    }}

    /* Result Panels */
    .metric-card {{
        text-align: center;
        padding: 1.5rem;
    }}
    
    .metric-value {{
        font-size: 3.5rem;
        font-weight: 800;
        color: {ACCENT_MINT};
        line-height: 1;
    }}
    
    /* Radar Chart Overrides */
    div.stPlotlyChart {{
        background: transparent !important;
        border-radius: 20px;
    }}

    /* Scanning Effect Overlay */
    .scan-container {{
        position: relative;
        overflow: hidden;
        border-radius: 20px;
    }}
    .scan-line {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: {ACCENT_MINT};
        box-shadow: 0 0 15px {ACCENT_MINT};
        opacity: 0.5;
        z-index: 10;
        animation: scanLines 4s linear infinite;
    }}
    @keyframes scanLines {{
        0% {{ top: -10%; }}
        100% {{ top: 110%; }}
    }}
    
    .scan-grid {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 210, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 210, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: 5;
        pointer-events: none;
    }}

    /* Animations */
    @keyframes fadeInUp {{
        0% {{ opacity: 0; transform: translateY(30px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .animate-in {{ animation: fadeInUp 1s cubic-bezier(0.19, 1, 0.22, 1) forwards; }}

    /* Sidebar Polishing */
    [data-testid="stSidebar"] {{
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid {UI_BORDER};
    }}
</style>
""", unsafe_allow_html=True)

# --- HEADER / HERO ---
st.markdown("""
<div class="brand-hero">
    <p class="tagline animate-in">The Phoenix Protocol</p>
    <h1 class="main-title animate-in">DEADIDEA AI</h1>
</div>
""", unsafe_allow_html=True)

# --- SEARCH PANEL ---
col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    st.markdown('<div class="glass-box animate-in" style="padding: 2rem;">', unsafe_allow_html=True)
    idea_input = st.text_input("Enter a discarded vision", placeholder="e.g. Quibi, Google Glass, Vine...", label_visibility="collapsed")
    submit_btn = st.button("INITIATE REVIVAL RECON")
    st.markdown('</div>', unsafe_allow_html=True)

# API Key Check (Server Side Only)
user_api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

# --- APPLICATION LOGIC ---
if submit_btn:
    if idea_input.strip():
        # Premium Loading Montage
        status_bar = st.progress(0)
        status_log = st.empty()
        
        sequence = [
            ("Accessing Historical Data Banks...", 20),
            ("Engaging Gemini-Pro Neural Matrix...", 50),
            ("Synthesizing 2026 Technological Delta...", 80),
            ("Finalizing Post-Mortem Reconstruction...", 100)
        ]
        
        for msg, prog in sequence:
            status_log.markdown(f'<p style="text-align:center; color:{ACCENT_MINT}; font-weight:600;">{msg}</p>', unsafe_allow_html=True)
            status_bar.progress(prog)
            time.sleep(0.6)
        
        try:
            # Attempt API hit
            try:
                payload = {"idea_name": idea_input}
                response = requests.post(f"{API_URL}/analyze", json=payload, timeout=12)
                response.raise_for_status()
                data = response.json()
            except:
                data = analyze_idea(idea_input, api_key=user_api_key)
            
            status_bar.empty()
            status_log.empty()

            # --- DISPLAY RESULTS ---
            score = data.get("Revival Potential Score", 50)
            
            # Row 1: High Level Strategy
            st.markdown(f"""
            <div class="glass-box animate-in" style="border-left: 5px solid {ACCENT_MINT};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 class="tag-font" style="color: {ACCENT_MINT}; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 2px;">Blueprint Re-Engineered</h4>
                        <h2 class="tag-font" style="font-size: 3rem; margin-top: 0;">{idea_input.upper()}</h2>
                    </div>
                    <div style="text-align: right;">
                        <div class="metric-card" style="padding: 0;">
                            <div class="metric-value">{score}%</div>
                            <div class="metric-label">Viability Index</div>
                        </div>
                        {f'<p style="color:{ACCENT_ROSE}; font-size:0.65rem; font-weight:800; letter-spacing:1px; margin-top:5px;">SIMULATION ACTIVE</p>' if data.get("INTELLIGENCE_LAYER") else ''}
                    </div>
                </div>
                <div style="margin-top: 2rem;">
                    <p style="font-size: 1.5rem; font-style: italic; color: #FFF; line-height: 1.4;">"{data.get('Elevator Pitch', 'A legacy idea reborn for the modern age.')}"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Row 2: Deep Dive + Full Visualization
            col_res1, col_res2 = st.columns([1, 1])
            
            with col_res1:
                # DATA VISUALIZATION: Radar Chart
                st.markdown(f"""
                <div class="glass-box animate-in" style="padding-bottom: 10px;">
                    <h4 class="tag-font" style="color: {ACCENT_MINT}; font-size: 0.8rem; letter-spacing: 2px;">NEURAL MARKET DYNAMICS</h4>
                """, unsafe_allow_html=True)
                
                # Robust Metric Validation
                raw_metrics = data.get("Market Metrics", {})
                if not isinstance(raw_metrics, dict):
                    # Fallback for unexpected AI formats
                    raw_metrics = {"Scale": 60, "Impact": 70, "Innovation": 80, "Risk": 40, "Speed": 50}
                
                categories = [str(k) for k in raw_metrics.keys()]
                values = [float(v) if str(v).replace('.','',1).isdigit() else 50 for v in raw_metrics.values()]
                
                # Minimum 3 points for a radar chart to look decent
                if len(categories) < 3:
                     categories += ["Stability", "Global Demand"][:3-len(categories)]
                     values += [50] * (3-len(values))

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(0, 255, 210, 0.2)',
                    line=dict(color=ACCENT_MINT, width=3),
                    marker=dict(size=8, color=ACCENT_MINT)
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="grey")),
                        angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#FFF", size=10)),
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=20, b=20),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

                # Summary Text
                st.markdown(f"""
                <div class="glass-box animate-in">
                    <h3 class="tag-font"><i class="fas fa-bolt" style="color:{ACCENT_MINT}; margin-right: 15px;"></i> Strategic Concept</h3>
                    <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;">{data.get('Revived Startup Concept', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_res2:
                # VISUAL SYNTHESIS: Scanning Feed
                st.markdown(f"""
                <div class="glass-box animate-in" style="padding: 0;">
                    <div style="padding: 1.5rem; border-bottom: 1px solid {UI_BORDER};">
                        <h4 class="tag-font" style="margin:0; font-size: 0.9rem; letter-spacing: 1px; color: {ACCENT_MINT};">
                            <i class="fas fa-video fa-pulse" style="margin-right: 10px;"></i> SYS_VISUAL_RECON_FEED_v4.0
                        </h4>
                    </div>
                    <div class="scan-container">
                        <div class="scan-line"></div>
                        <div class="scan-grid"></div>
                """, unsafe_allow_html=True)
                
                visual_prompt = data.get("Visual Concept Prompt", "")
                if visual_prompt:
                    clean_prompt = visual_prompt.replace("\n", " ").strip()
                    encoded_prompt = urllib.parse.quote(clean_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
                    st.image(image_url, width='stretch')
                
                st.markdown("""
                    </div>
                    <div style="padding: 1.2rem; background: rgba(0,0,0,0.5); font-family: monospace; font-size: 0.7rem; color: #00FFD2; opacity: 0.7;">
                        > RENDER_STATE: ACTIVE<br>
                        > NEURAL_RECON: 100% COMPLETE<br>
                        > PHOENIX_PROTOCOL: ENGAGED
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Market Context
                st.markdown(f"""
                <div class="glass-box animate-in" style="margin-top: 1rem; text-align: center; border-color: {ACCENT_ROSE}33; padding: 1.5rem;">
                    <h4 class="tag-font" style="font-size: 0.7rem; color: rgba(255,255,255,0.4); letter-spacing: 2px;">PRIMARY SECTOR</h4>
                    <p style="font-size: 1.2rem; font-weight: 700; margin: 0.5rem 0;">{data.get('Target Audience', 'Mass Market')}</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            err_msg = str(e)
            if "exhausted" in err_msg.lower() or "quota" in err_msg.lower():
                st.error("🚨 NEURAL NETWORK CONGESTED: Gemini API Quota exceeded. Please wait 60 seconds and try again, or use a different API key.")
            else:
                st.error(f"Neural Connection Terminated: {e}")

# --- FOOTER ---
st.markdown(f"""
<div style="text-align: center; padding: 5rem 0; color: rgba(255,255,255,0.2); font-size: 0.8rem;">
    <p>VERSION 4.0 // POWERED BY GOOGLE GEMINI PRO // G-STUDIO HACKATHON 2026</p>
    <div style="font-size: 1.5rem; margin-top: 1rem;">
        <i class="fab fa-github" style="margin: 0 10px;"></i>
        <i class="fab fa-google" style="margin: 0 10px;"></i>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for History (Simplified)
with st.sidebar:
    st.markdown(f'<h2 class="tag-font" style="color:{ACCENT_MINT};">Archives</h2>', unsafe_allow_html=True)
    st.info("The Graveyard keeps track of all past resurrections locally.")
    if st.button("CLEAR LOCAL PERSISTENCE"):
        st.cache_data.clear()
        st.success("Buffer Cleared.")
