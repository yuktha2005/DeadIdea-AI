import streamlit as st
import requests
import os
import urllib.parse
import time
import sys

# Add root directory to path so we can import backend logic directly if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from backend.gemini_agent import analyze_idea
except ImportError:
    # Direct import fallback for different envs
    from gemini_agent import analyze_idea

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="DeadIdea AI | Resurrecting Innovation", 
    page_icon="💀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- ADVANCED DESIGN SYSTEM (CSS) ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@500;800&display=swap" rel="stylesheet">

<style>
    /* Premium Design System Tokens */
    :root {
        --accent-glow: #00FFC2;
        --accent-danger: #FF2D55;
        --rich-black: #050505;
        --card-surface: rgba(20, 20, 22, 0.82);
        --glass-stroke: rgba(255, 255, 255, 0.05);
        --text-primary: #FFFFFF;
        --text-secondary: #94949E;
        --font-outfit: 'Outfit', sans-serif;
    }

    /* Base Reset & Typography */
    body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--rich-black);
        color: var(--text-primary);
        letter-spacing: -0.01em;
    }

    h1, h2, h3, h4, .outfit-font {
        font-family: var(--font-outfit) !important;
        letter-spacing: -0.03em;
    }

    /* High-End Animations */
    @keyframes revealUp {
        0% { opacity: 0; transform: translateY(40px) scale(0.96); filter: blur(10px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    
    @keyframes subtlePulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    .animate-reveal {
        animation: revealUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Engineered Glassmorphism */
    .glass-card {
        background: var(--card-surface);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--glass-stroke);
        border-radius: 28px;
        padding: 2.5rem;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 194, 0.2);
        background: rgba(25, 25, 28, 0.9);
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }

    /* Luxury Scaling Header */
    .hero-title {
        background: linear-gradient(135deg, #FFFFFF 0%, #71717A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: clamp(3rem, 10vw, 5rem);
        line-height: 0.95;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.5));
    }
    
    .hero-subtitle {
        color: var(--accent-glow);
        text-transform: uppercase;
        letter-spacing: 6px;
        font-size: clamp(0.7rem, 2vw, 0.9rem);
        font-weight: 600;
        opacity: 0.9;
    }

    /* Interaction & Feedback UI */
    .stButton>button {
        background: linear-gradient(135deg, #FFFFFF 0%, #D4D4D8 100%) !important;
        color: #000000 !important;
        height: 60px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        border-radius: 16px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem;
    }
    
    .stButton>button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 40px rgba(255, 255, 255, 0.15) !important;
    }

    /* Professional Analytics Styling */
    div[data-testid="stMetricValue"] {
        font-family: var(--font-outfit);
        font-size: clamp(2.5rem, 5vw, 4rem) !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        text-shadow: 0 0 20px rgba(0, 255, 194, 0.3);
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-weight: 600 !important;
    }

    /* Content Hierarchy */
    .concept-title {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 2rem;
    }

    /* Custom Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--accent-glow) !important;
        height: 6px;
        border-radius: 3px;
    }

    /* Input Field Polishing */
    .stTextInput input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--glass-stroke) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: var(--accent-glow) !important;
        background: rgba(255,255,255,0.06) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    # Robust logo path
    logo_path = "deadidea_ai_luxury_logo_1773671009582.png"
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(__file__), "..", logo_path)
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        st.markdown('<div style="font-size: 5rem;">💀</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown('<p class="hero-title animate-in">DeadIdea AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle animate-in">Resurrecting the Graveyard of Innovation</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top: 15px; color: #8E9196; max-width: 600px; line-height: 1.6; font-size: 1.1rem;">
    Deciphering the failure of past visions to engineer the breakthroughs of tomorrow. 
    Powered by <b>Google Gemini Pro</b>.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="premium-hr"></div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.markdown('<div class="sidebar-branding">', unsafe_allow_html=True)
    st.markdown('<p class="outfit-font" style="font-weight: 800; font-size: 1.5rem; color: var(--primary-mint);">DEADIDEA</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("###  Engine Settings")
    
    # Try to get key from secrets first (Streamlit Cloud)
    env_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    
    user_api_key = st.text_input("Gemini API Key", type="password", value=env_key, help="Enter your Google Gemini API key.")
    
    if not user_api_key:
        st.warning("⚠️ API Key is missing.")
    
    st.markdown("---")
    st.markdown("###  Developer Mode")
    st.info("Direct Standalone Link active. Connected to Gemini SDK.")

col_search1, col_search2, col_search3 = st.columns([1, 2, 1])
with col_search2:
    idea_input = st.text_input("Enter a failed idea (e.g., Google Glass, Vine, Segway, Quibi):", placeholder="e.g. Google Plus")
    submit_btn = st.button("Reactivate Idea Timeline ⚡", type="primary")

if submit_btn:
    if idea_input.strip():
        # Cinematic loading sequence
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("####  Accessing historical archives...")
        time.sleep(0.7)
        progress_bar.progress(25)
        
        status_text.markdown("#### Identifying root failure vectors...")
        time.sleep(0.7)
        progress_bar.progress(50)
        
        try:
            # We fetch while leaving the user in suspense
            # First attempt: Local/Container Backend
            try:
                payload = {"idea_name": idea_input}
                if user_api_key:
                    payload["api_key"] = user_api_key
                    
                response = requests.post(f"{API_URL}/analyze", json=payload, timeout=8)
                response.raise_for_status()
                data = response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
                # Second attempt: Direct call (Standalone Mode for Streamlit Cloud)
                data = analyze_idea(idea_input, api_key=user_api_key)
            
            progress_bar.progress(75)
            status_text.markdown("#### 🌐  Mapping to modern ecosystem...")
            time.sleep(0.8)
            
            progress_bar.progress(100)
            status_text.markdown("#### ✨  Re-engineering successful.")
            time.sleep(0.5)
            
            status_text.empty()
            progress_bar.empty()
            if "error" in data and data["error"] == "MISSING_API_KEY":
                progress_bar.empty()
                status_text.empty()
                st.error(" **GEMINI_API_KEY is missing!**")
                st.info("To fix this, set your API key in your terminal environment before running the app. \n\n **Windows:** `set GEMINI_API_KEY=your_key_here` \n\n **Mac/Linux:** `export GEMINI_API_KEY=your_key_here` \n\n Then restart the server.")
            
            progress_bar.progress(70)
            status_text.markdown("#### Mapping to current technological ecosystem...")
            time.sleep(1)
            
            progress_bar.progress(90)
            status_text.markdown("####  Generating visual concept render...")
            time.sleep(1.5)
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            score = data.get("Revival Potential Score", 0)
            if score >= 80:
                st.balloons()
            
            # Result Header
            st.markdown(f'<p class="concept-title animate-reveal">⚡ Revival Protocol: {idea_input.upper()}</p>', unsafe_allow_html=True)
            
            # Metric Row in Glass Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.metric(label="Viability Index", value=f"{score}%", delta="HIGH POTENTIAL" if score > 75 else "LOW")
                st.markdown('</div>', unsafe_allow_html=True)
            with m2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                short_audience = data.get("Target Audience", "Mass Market")
                if len(short_audience) > 20: short_audience = short_audience[:18] + "..."
                st.metric(label="Market Segement", value=short_audience)
                st.markdown('</div>', unsafe_allow_html=True)
            with m3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.metric(label="Investment Status", value="SEED READY" if score > 80 else "R&D")
                st.markdown('</div>', unsafe_allow_html=True)

            # Elevator Pitch Panel
            pitch = data.get("Elevator Pitch", "A bold vision for the future.")
            st.markdown(f"""
            <div class="glass-card animate-reveal" style="border-left: 5px solid var(--accent-glow); border-radius: 0 28px 28px 0; background: linear-gradient(90deg, rgba(0,255,194,0.05) 0%, var(--card-surface) 100%);">
                <p style="color: var(--accent-glow); font-weight: 700; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 12px; text-transform: uppercase;">Executive Vision</p>
                <p style="font-size: 1.6rem; font-family: var(--font-outfit); font-weight: 500; font-style: italic; line-height: 1.4;">"{pitch}"</p>
            </div>
            """, unsafe_allow_html=True)
                
            st.divider()
            
            # Visual + Detailed layout
            main_col1, main_col2 = st.columns([1.5, 1])
            
            with main_col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                # Use Tabs for a clean, non-overwhelming UI
                tab1, tab2, tab3 = st.tabs(["📉 Post-Mortem", "🚀 Revival Plan", "💡 Concept Details"])
                
                with tab1:
                    st.markdown("#### The Idea Summary")
                    st.write(data.get("Idea Summary", ""))
                    st.markdown("#### Failure Vectors")
                    st.warning(data.get("Failure Analysis", ""))
                    
                with tab2:
                    st.markdown("#### Market Evolution")
                    st.success(data.get("What Has Changed Today", ""))
                    st.markdown("#### Primary Demographic")
                    st.write(data.get("Target Audience", ""))
                    
                with tab3:
                    st.markdown("#### High-Level execution")
                    st.write(data.get("Revived Startup Concept", ""))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with main_col2:
                st.markdown('<div class="glass-card" style="padding-top: 1rem;">', unsafe_allow_html=True)
                st.markdown('<p class="outfit-font" style="font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;">📸 GENERATIVE RENDER</p>', unsafe_allow_html=True)
                visual_prompt = data.get("Visual Concept Prompt", "")
                
                if visual_prompt:
                    # Clean prompt for URL
                    clean_prompt = visual_prompt.replace("\n", " ").strip()
                    encoded_prompt = urllib.parse.quote(clean_prompt)
                    # Pollinations API with seed for consistency
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=1337"
                    
                    st.image(image_url, use_container_width=True, caption=f"AI Representation of the New Paradigm")
                    
                    with st.expander("Show AI Parameters"):
                        st.code(visual_prompt, language="text")
                st.markdown('</div>', unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"System Failure: {e}")
            progress_bar.empty()
            status_text.empty()
    else:
        st.warning("Please enter an idea.")

st.markdown('<div class="premium-hr"></div>', unsafe_allow_html=True)

st.markdown('<p class="outfit-font" style="font-size: 1.5rem; font-weight: 700;">📚 Idea Graveyard (Recent Revivals)</p>', unsafe_allow_html=True)
if st.button("Access Historical Archive"):
    try:
        res = requests.get(f"{API_URL}/history")
        if res.status_code == 200:
            history = res.json().get("history", [])
            if not history:
                st.info("The archive is currently empty.")
            
            # Show history in a clean grid
            for item in history:
                score = item.get('Revival Potential Score', 0)
                st.markdown('<div class="glass-card" style="padding: 1.2rem;">', unsafe_allow_html=True)
                with st.expander(f"{item.get('original_idea', 'Unknown').upper()} — Viability: {score}%"):
                    st.write(f"**Concept:** {item.get('Revived Startup Concept')}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Connection to archives failed.")
    except Exception as e:
        st.error(f"Archive retrieval error: {e}")
