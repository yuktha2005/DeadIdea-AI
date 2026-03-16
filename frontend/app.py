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
    /* Global Styles */
    :root {
        --primary-mint: #00FFC2;
        --secondary-rose: #FF2D55;
        --bg-dark: #0B0B0C;
        --card-bg: rgba(28, 29, 31, 0.7);
        --text-muted: #8E9196;
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-dark);
        color: white;
    }

    h1, h2, h3, h4, .outfit-font {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Glass Panels */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 194, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }

    /* Luxury Header */
    .hero-title {
        background: linear-gradient(135deg, #FFFFFF 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.8rem;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    
    .hero-subtitle {
        color: var(--primary-mint);
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: -10px;
    }

    /* Metric Overrides */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: white !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* Button Styling */
    .stButton>button {
        background: white !important;
        color: black !important;
        border: none !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.2) !important;
    }

    /* Input Field Styling */
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: white !important;
    }

    /* Sidebar Branding */
    .sidebar-branding {
        padding: 1.5rem;
        text-align: center;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 2rem;
    }

    /* Custom Divider */
    .premium-hr {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        margin: 3rem 0;
        border: none;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.8s ease forwards;
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
    
    st.markdown("### ⚙️ Engine Settings")
    
    # Try to get key from secrets first (Streamlit Cloud)
    env_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    
    user_api_key = st.text_input("Gemini API Key", type="password", value=env_key, help="Enter your Google Gemini API key.")
    
    if not user_api_key:
        st.warning("⚠️ API Key is missing.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Developer Mode")
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
        
        status_text.markdown("#### 🔍 Querying historical archives...")
        time.sleep(0.5)
        progress_bar.progress(20)
        
        status_text.markdown("#### 🧠 Activating Gemini... Identifying failure points...")
        time.sleep(0.5)
        progress_bar.progress(40)
        
        try:
            # We fetch while leaving the user in suspense
            # First attempt: Local/Container Backend
            try:
                payload = {"idea_name": idea_input}
                if user_api_key:
                    payload["api_key"] = user_api_key
                    
                response = requests.post(f"{API_URL}/analyze", json=payload, timeout=5)
                response.raise_for_status()
                data = response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                # Second attempt: Direct call (Standalone Mode for Streamlit Cloud)
                data = analyze_idea(idea_input, api_key=user_api_key)
            
            if "error" in data and data["error"] == "MISSING_API_KEY":
                progress_bar.empty()
                status_text.empty()
                st.error("🔑 **GEMINI_API_KEY is missing!**")
                st.info("To fix this, set your API key in your terminal environment before running the app. \n\n **Windows:** `set GEMINI_API_KEY=your_key_here` \n\n **Mac/Linux:** `export GEMINI_API_KEY=your_key_here` \n\n Then restart the server.")
                st.stop()
            
            progress_bar.progress(70)
            status_text.markdown("#### 🌐 Mapping to current technological ecosystem...")
            time.sleep(1)
            
            progress_bar.progress(90)
            status_text.markdown("#### 🎨 Generating visual concept render...")
            time.sleep(1.5)
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            score = data.get("Revival Potential Score", 0)
            if score >= 80:
                st.balloons()
            
            # Result Header
            st.markdown(f'<p class="outfit-font animate-in" style="font-size: 2rem; font-weight: 800; margin-bottom: 2rem;">⚡ Revival Protocol: {idea_input.upper()}</p>', unsafe_allow_html=True)
            
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
            <div class="glass-card" style="border-left: 4px solid var(--primary-mint); border-radius: 0 20px 20px 0;">
                <p style="color: var(--primary-mint); font-weight: 600; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 10px;">THE VISION</p>
                <p style="font-size: 1.5rem; font-family: 'Outfit'; font-weight: 500; font-style: italic;">"{pitch}"</p>
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
