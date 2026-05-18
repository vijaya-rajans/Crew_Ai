# --- CRITICAL CLOUD DATABASE HOTFIX ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS
import streamlit as st
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS

# --- 1. FREE SEARCH TOOL ---
@tool("DuckDuckGo Search")
def free_search_tool(query: str) -> str:
    """Search the web for real-time information regarding a given query."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            return str(results)
    except Exception as e:
        return f"Search error occurred: {str(e)}"

# --- 2. CONFIGURE GROQ LLM ---
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.4
)

# --- 3. APPLE-LIKE MINIMALIST AESTHETIC CSS STYLING ---
st.set_page_config(page_title="VAIXUS Trend Intelligence", page_icon="", layout="wide")

# Fixed: changed unsafe_allow_html to unsafe_allow_html
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #f5f5f7 !important;
    }
    
    .block-container {
        padding-top: 3rem !important;
        max-width: 900px !important;
    }
    
    .apple-title {
        font-weight: 600;
        font-size: 2.8rem;
        letter-spacing: -0.03em;
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1A6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .apple-subtitle {
        color: #86868b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }
    
    div.stButton > button:first-child {
        background-color: #f5f5f7 !important;
        color: #1d1d1f !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:first-child:hover {
        background-color: #ffffff !important;
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.2);
    }
    
    .output-card {
        background-color: #1c1c1e;
        border: 1px solid #2c2c2e;
        border-radius: 14px;
        padding: 24px;
        margin-top: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #86868b !important;
        font-size: 16px !important;
        padding-bottom: 8px !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI HEADER LAYOUT ---
st.markdown('<h1 class="apple-title">AI Trend Systems</h1>', unsafe_allow_html=True)
st.markdown('<p class="apple-subtitle">Autonomous 7-day trend intelligence and creative pipeline scriptwriter.</p>', unsafe_allow_html=True)

# --- ACTION SECTION ---
st.markdown("### ⚡ Operational Control")

if st.button("Launch Autonomous Discovery"):
    with st.spinner("🤖 Crew is currently online. Syncing with Groq and scouring the web..."):
        try:
            # --- DEFINE AGENTS DIRECTLY INSIDE UI ---
            trend_hunter = Agent(
                role='Senior AI Trend and News Hunter',
                goal='Find the absolute latest AI news updates, major model releases, and trends in image and video generation tools.',
                backstory='World-class tech scout specializing in AI. You aggressively ignore anything older than 7 days.',
                tools=[free_search_tool],
                llm=groq_llm,
                verbose=True
            )

            social_monitor = Agent(
                role='Social Media and Creator Content Monitor',
                goal='Identify the exact topics, updates, and video themes that top AI creators are publishing right now.',
                backstory='Creator economy expert tracking top AI YouTubers. You filter out anything older than 7 days.',
                tools=[free_search_tool],
                llm=groq_llm,
                verbose=True
            )

            chief_editor = Agent(
                role='Chief AI Intelligence Editor',
                goal='Consolidate messy research data into a polished, high-signal, hyper-focused weekly AI intelligence briefing.',
                backstory='Meticulous editor with an uncompromised standard for clarity and freshness.',
                llm=groq_llm,
                verbose=True
            )

            content_scriptwriter = Agent(
                role='Viral AI Content Scriptwriter',
                goal='Convert raw tech intelligence reports into short-form video scripts (Instagram Reels, YouTube Shorts) that generate high curiosity and engagement.',
                backstory='Expert social media strategist. You create powerful hooks and conversational scripts.',
                llm=groq_llm,
                verbose=True
            )

            # --- DEFINE TASKS DIRECTLY INSIDE UI ---
            task1 = Task(
                description='Scour the web for core model updates, trending features in AI image tools, and video engines from the last 7 days.',
                expected_output='A structured list of raw breakthrough AI news from the last week.',
                agent=trend_hunter
            )

            task2 = Task(
                description='Investigate what experienced AI creators and YouTubers are talking about in their uploads from the last 7 days.',
                expected_output='A bulleted summary showing what top creators are focusing on this week.',
                agent=social_monitor
            )

            task3 = Task(
                description='Review data from task 1 and 2, remove duplicates, filter out anything older than 7 days, and format a beautiful markdown digest.',
                expected_output='A clean markdown report with sections for updates, trends, and creator summaries.',
                output_file='weekly_ai_trend_report.md',
                agent=chief_editor
            )

            task4 = Task(
                description='Take the editor report and convert the top 2-3 trends into a short form video script with a 3-second hook, visual cues, and a solid CTA.',
                expected_output='A beautifully formatted production short video script.',
                output_file='viral_ai_video_script.md',
                agent=content_scriptwriter
            )

            # --- RUN THE APP CREW ---
            ui_crew = Crew(
                agents=[trend_hunter, social_monitor, chief_editor, content_scriptwriter],
                tasks=[task1, task2, task3, task4],
                process=Process.sequential,
                verbose=True
            )

            ui_crew.kickoff()
            st.success("✨ Execution Complete. Intelligence logs successfully built.")
            st.rerun()
            
        except Exception as e:
            st.error(f"Operational Glitch Encountered: {str(e)}")

st.markdown("---")

# --- DATA DISPLAY LAYER ---
st.markdown("### 📊 Generated Assets")

tab1, tab2 = st.tabs(["🚀 Weekly Intelligence Briefing", "🎥 Viral Social Script"])

with tab1:
    report_file = "weekly_ai_trend_report.md"
    if os.path.exists(report_file):
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No active trend reports found. Click 'Launch Autonomous Discovery' above to generate one.")

with tab2:
    script_file = "viral_ai_video_script.md"
    if os.path.exists(script_file):
        with open(script_file, "r", encoding="utf-8") as f:
            script_content = f.read()
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.markdown(script_content)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No viral social production scripts found. Run the engine to compile your next short-form video assets.")