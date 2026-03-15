import streamlit as st
import requests
import os
import urllib.parse
import time

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="DeadIdea AI", page_icon="💀", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for a cyberpunk/premium aesthetic
st.markdown("""
<style>
    /* Add gradient headers and glowing metrics */
    .stTextInput input {
        border-radius: 8px;
        padding: 12px;
        font-size: 1.1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff1c1c 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }
    .gradient-text {
        background: linear-gradient(90deg, #ff4b4b, #ff8c42, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 3rem !important;
        color: #00ffcc !important;
    }
    .concept-pitch {
        font-size: 1.4rem;
        font-style: italic;
        color: #ffb86c;
        border-left: 4px solid #ffb86c;
        padding-left: 15px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
col_header1, col_header2 = st.columns([1, 6])
with col_header1:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=💀&backgroundColor=0d0d12", width=120)
with col_header2:
    st.markdown('<p class="gradient-text">DeadIdea AI</p>', unsafe_allow_html=True)
    st.markdown("#### Resurrecting the Graveyard of Innovation ⚰️ ➡️ 🚀")

st.markdown("Many multi-billion dollar ideas naturally fail because they were simply *too early*. Enter the name of an abandoned idea, discontinued product, or failed startup. Gemini will analyze its past and structurally reconstruct it for the present.")

st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    user_api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key if not set in environment variables.")
    if not user_api_key and not os.environ.get("GEMINI_API_KEY"):
        st.warning("⚠️ API Key is missing. Enter it above or set GEMINI_API_KEY in the environment.")
    st.info("Don't have a key? Get one at [Google AI Studio](https://aistudio.google.com/app/apikey)")

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
            payload = {"idea_name": idea_input}
            if user_api_key:
                payload["api_key"] = user_api_key
                
            response = requests.post(f"{API_URL}/analyze", json=payload)
            response.raise_for_status()
            data = response.json()
            
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
            
            st.markdown(f"## 🌟 Revival Protocol Complete: **{idea_input.upper()}**")
            
            # The core storytelling UI
            if data.get("Elevator Pitch"):
                st.markdown(f'<div class="concept-pitch">"{data.get("Elevator Pitch", "An incredible new future.")}"</div>', unsafe_allow_html=True)
            
            # Top metrics
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="Revival Viability %", value=f"{score}%", delta="High Potential" if score > 75 else "- Low Viability")
            with m_col2:
                short_audience = data.get("Target Audience", "Mass Market")
                if len(short_audience) > 25: short_audience = short_audience[:22] + "..."
                st.metric(label="Target Audience", value=short_audience)
            with m_col3:
                st.metric(label="Status", value="SEED READY" if score > 80 else "NEEDS R&D", delta_color="off")
                
            st.divider()
            
            # Visual + Detailed layout
            main_col1, main_col2 = st.columns([1.5, 1])
            
            with main_col1:
                # Use Tabs for a clean, non-overwhelming UI
                tab1, tab2, tab3 = st.tabs(["📉 The Post-Mortem", "🚀 The Revival Plan", "💡 The Concept Details"])
                
                with tab1:
                    st.markdown("### 📝 What It Was")
                    st.write(data.get("Idea Summary", ""))
                    st.markdown("### 💀 Why It Died")
                    st.info(data.get("Failure Analysis", ""))
                    
                with tab2:
                    st.markdown("### ⚡ What Has Changed?")
                    st.success(data.get("What Has Changed Today", ""))
                    st.markdown("### 🎯 Core Demographic")
                    st.write(data.get("Target Audience", ""))
                    
                with tab3:
                    st.markdown("### ✨ Modern Execution")
                    st.write(data.get("Revived Startup Concept", ""))
            
            with main_col2:
                # Show image with a nice styled caption
                st.markdown("### 📸 Generative Concept")
                visual_prompt = data.get("Visual Concept Prompt", "")
                
                if visual_prompt:
                    encoded_prompt = urllib.parse.quote(visual_prompt)
                    # Pollinations API with seed for consistency
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=1337"
                    
                    st.image(image_url, use_container_width=True, caption=f"AI Representation of the New Paradigm")
                    
                    with st.expander("Show Underlying Image Prompt"):
                        st.code(visual_prompt, language="text")
                        
        except Exception as e:
            st.error(f"System Failure: {e}")
            progress_bar.empty()
            status_text.empty()
    else:
        st.warning("Please enter an idea.")

st.divider()

st.subheader("📚 Idea Graveyard (Recent Revivals)")
if st.button("Load History Archive"):
    try:
        res = requests.get(f"{API_URL}/history")
        if res.status_code == 200:
            history = res.json().get("history", [])
            if not history:
                st.info("No history found in the databanks.")
            for item in history:
                score = item.get('Revival Potential Score', 0)
                emoji = "🚀" if score > 80 else "📉"
                with st.expander(f"{emoji} {item.get('original_idea', 'Unknown').upper()} (Viability: {score}%)"):
                    st.write(f"**Pitch:** {item.get('Elevator Pitch', 'N/A')}")
                    st.write(f"**Concept:** {item.get('Revived Startup Concept')}")
        else:
            st.error("Failed to access archives.")
    except Exception as e:
        st.error(f"Failed to fetch history: {e}")
