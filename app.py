# ==============================================================================
# 1. CRITICAL DATABASE HOTFIX (Must run BEFORE any other package imports)
# ==============================================================================
import os
import sys

if os.name != 'nt':  
    try:
        __import__('pysqlite3')
        sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    except ImportError:
        pass

# ==============================================================================
# 2. IMMEDIATE STREAMLIT PAGE INITIALIZATION (Guarantees Fast Render)
# ==============================================================================
import streamlit as st

logo_file = "vaixus_logo.png"
page_icon_asset = logo_file if os.path.exists(logo_file) else "⚡"

st.set_page_config(
    page_title="VAIXUS Trend Intelligence",
    page_icon=page_icon_asset,
    layout="wide"
)

# ==============================================================================
# 3. VISUAL LAUNCH PROGRESS BAR & HEAVY FRAMEWORK LOADING
# ==============================================================================
with st.spinner("⚡ Initializing VAIXUS Core AI Framework Assets... Please wait."):
    from crewai import Agent, Crew, Process, Task, LLM
    # Upgraded Search Tool: Swapped DuckDuckGo for Enterprise Google Search
    from crewai.tools import SerperDevTool 

# ==============================================================================
# 4. USER INTERACTION INTERFACE LAYOUT (Streamlit UI)
# ==============================================================================
st.title("AI Trend Systems")
st.caption("Autonomous 7-day trend intelligence and creative pipeline scriptwriter.")

st.subheader("⚡ Operational Control")

# Secure retrieval of environment API key routing
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

if not groq_api_key:
    st.error("Authentication Missing: Please configure your 'GROQ_API_KEY' inside your environment dashboard settings.")
elif not serper_api_key:
    st.error("Authentication Missing: Please configure your 'SERPER_API_KEY' inside your environment dashboard settings to unlock Google Search.")
else:
    if st.button("Launch Autonomous Discovery", type="primary"):
        st.info("Orchestrating agent network loops. Running real-time Google queries...")
        
        # Initialize Google Serper Tool natively
        google_search_tool = SerperDevTool()
        
        # Configure stable Groq LLM instance with cache flag disabled
        groq_llm = LLM(
            model="groq/llama-3.3-70b-versatile", 
            api_key=groq_api_key,
            use_cache=False  # Explicitly fixes the 'cache_breakpoint' crash
        )
        
        # ─── AGENT ENGINE DEFINITIONS ─────────────────────────────────────────
        researcher = Agent(
            role="Lead Trend Research Analyst",
            goal="Scrape the internet to uncover accelerating breakthroughs and consumer paradigm shifts.",
            backstory="An elite data-scraping intelligence programmed to look past surface noise and identify high-velocity global trends using actual Google data indexes.",
            verbose=True,
            allow_delegation=False,
            tools=[google_search_tool],  # Uses Google now!
            llm=groq_llm
        )

        writer = Agent(
            role="Chief Creative Copywriter",
            goal="Synthesize raw market data into high-retention, viral educational script frameworks.",
            backstory="A master content architect specialized in packaging dense technical metrics into simple, fascinating narratives.",
            verbose=True,
            allow_delegation=False,
            llm=groq_llm
        )

        # ─── OPERATIONAL TASK SPECIFICATIONS ──────────────────────────────────
        research_task = Task(
            description="Identify the top 3 high-velocity trends taking place in AI automation this week. Analyze what makes them significant.",
            expected_output="A structured markdown intelligence briefing detailing the 3 trends, target demographics, and primary market signals.",
            agent=researcher
        )

        write_task = Task(
            description="Using the intelligence briefing, craft an ultra-engaging, curious LinkedIn hook and short text script breakdown.",
            expected_output="A complete, professional social post copy optimized for technical readers, ready to deploy.",
            agent=writer
        )

        # ─── MULTI-AGENT LOOP ORCHESTRATION ───────────────────────────────────
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, write_task],
            process=Process.sequential,
            verbose=True
        )

        with st.status("Agents are collaborating...", expanded=True) as status:
            try:
                raw_result = crew.kickoff()
                status.update(label="Analysis Finished Successfully!", state="complete", expanded=False)
                
                # ─── VISUAL DISPLAY OF GENERATED ASSETS ─────────────────────────
                st.subheader("📊 Generated Assets")
                tab1, tab2 = st.tabs(["Weekly Intelligence Briefing", "Viral Social Script"])
                
                with tab1:
                    st.markdown("### Core Trend Diagnostics")
                    st.write(str(raw_result))
                with tab2:
                    st.markdown("### Distribution-Ready Media Copy")
                    st.info("Copy and paste the framework below straight onto your social feed.")
                    st.code(str(raw_result), language="markdown")
                    
            except Exception as loop_error:
                status.update(label="Pipeline Failed", state="error")
                st.error(f"Orchestration runtime exception: {str(loop_error)}")

# Fallback UI state display container
if "raw_result" not in locals():
    st.markdown("---")
    st.info("No active trend reports found. Click 'Launch Autonomous Discovery' above to generate one.")