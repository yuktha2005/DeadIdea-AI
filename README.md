# DeadIdea AI 

DeadIdea AI is a multimodal AI agent that analyzes failed startups, discontinued products, and abandoned innovations to determine whether they could succeed today. It fulfills the requirements for the **Gemini Live Agent Challenge Hackathon**, competing in the **Creative Storyteller** category.

## Project Overview
Historically, many brilliant ideas failed purely because the timing was wrong—the technology wasn't there, internet speeds were too slow, or the market wasn't ready. This app uses the **Google Gemini Model** to step thoughtfully into the "idea graveyard", dig up discarded ideas, and reimagine them for the modern technological landscape.

## Features
1. **Idea Input Interface**: Enter any failed product (e.g., Google Glass, Vine).
2. **Failure Analysis**: AI analyzes the historical failure reasons.
3. **Modern Technology Mapping**: AI identifies what has changed (AI, 5G, AR/VR, shifting user habits).
4. **Revived Startup Concept**: AI proposes a completely modernized startup pitch.
5. **Revival Potential Score**: Rates the new concept from 0-100.
6. **Multimodal Output**: Not only generates text analysis, but produces an AI-image prompt and dynamically displays a generated visual of the new concept!
7. **Idea Database**: Connects to Google Cloud Firestore to save historical analyses.

##  Tech Stack
- **AI**: Google Gemini (via `google-generativeai` SDK)
- **Backend API**: Python FastAPI
- **Frontend**: Streamlit
- **Database**: Google Cloud Firestore
- **Deployment**: Google Cloud Run / Docker

## 🏗️ System Architecture

![System Architecture Preview](https://raw.githubusercontent.com/yuktha2005/DeadIdea-AI/main/system_architecture_preview.png)

The **Phoenix Protocol** architecture is designed for high-performance scale and seamless Google Cloud integration.

```mermaid
graph TD
    User([User Entity]) <--> Frontend[Cinematic Streamlit Dashboard]
    Frontend <--> Backend[FastAPI / Phoenix Intelligence Layer]
    Backend <--> Gemini[Google Gemini v1.5/2.0 Models]
    Backend <--> Firestore[GCP Firestore / Long-term Memory]
    Frontend <--> Visual[Plotly & Conceptual Render Feed]
    
    subgraph "Google Cloud Infrastructure"
        Gemini
        Firestore
        CloudRun[Cloud Run Orchestration]
    end
    
    style Frontend fill:#00FFD211,stroke:#00FFD2,stroke-width:2px
    style Backend fill:#FF006E11,stroke:#FF006E,stroke-width:2px
    style Gemini fill:#4285F411,stroke:#4285F4,stroke-width:2px
    style User color:#FFF,stroke:#FFF
```

### 🧠 The Intelligence Flow
1. **Frontend**: Captures discarded visions through a 30px-blur glassmorphism interface.
2. **Intelligence Layer**: Managed by `gemini_agent.py`, it orchestrates multiple Gemini model tiers for maximum resilience.
3. **AI Core**: Google Gemini extracts failure vectors and synthesizes a 2026 technical delta.
4. **Analytics**: Plotly renders **Neural Market Dynamics** (radar charts) while the conceptual engine produces visual recon feeds.
5. **Persistence**: Analyzed ideas are archived via high-performance JSON-Firestore sync.

##  Setup Instructions (Local)

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key:
   - On Windows: `set GEMINI_API_KEY=your_key_here`
   - On Mac/Linux: `export GEMINI_API_KEY=your_key_here`
4. (Optional) Set up Google Cloud Credentials locally for Firestore:
   ```bash
   gcloud auth application-default login
   ```
5. Run the services using the start script:
   - Command: `bash start.sh`
   - Or run separately:
     - Term 1: `uvicorn backend.main:app --reload`
     - Term 2: `streamlit run frontend/app.py`

---

## ⚡ Automated Cloud Deployment

This project demonstrates professional DevOps practices through Infrastructure-as-Code (IaC) and automated shell scripting for Google Cloud Platform.

*   **[deploy_gcp.sh](https://github.com/yuktha2005/DeadIdea-AI/blob/main/deploy_gcp.sh)**: A comprehensive bash script that automates API enabling, container building via **Google Cloud Build**, and orchestration to **Google Cloud Run**.
*   **[cloud_run_service.yaml](https://github.com/yuktha2005/DeadIdea-AI/blob/main/cloud_run_service.yaml)**: A formal Knative-based Service Specification that represents the infrastructure-as-code for the entire Phoenix Protocol service.
*   **[Dockerfile](https://github.com/yuktha2005/DeadIdea-AI/blob/main/Dockerfile)**: The immutable container specification used for consistent deployment across Google Cloud environments.

---

##  Demo Instructions

For your 4-minute demo capability, try the following scenario:

1. **Introduction (1 min)**: Explain the concept of DeadIdea. Open the hosted web interface.
2. **First Example - Google Glass (1.5 min)**:
   - Enter `Google Glass` and click Analyze.
   - Show the summary and the AI’s explanation of why it failed (poor battery, weird social acceptance, lack of use-cases).
   - Show how Gemini maps it to today: lightweight AR, Ray-Ban Meta glasses, AI-agent integrations.
   - Show the generated Revived Concept and the generated **Multimodal image visualization**! Review the Score.
3. **Second Example - Vine (1 min)**:
   - Enter `Vine`.
   - Show the output where it talks about TikTok and Short-form video domination, and propose how a modernized Vine might thrive right now on highly curated AI-edited micro-content.
4. **Architecture & Stack (0.5 min)**: Show the DB history expanding via the History accordion at the bottom, proving Firestore integration. Highlight Cloud Run scaling and Gemini API structured JSON mode.
