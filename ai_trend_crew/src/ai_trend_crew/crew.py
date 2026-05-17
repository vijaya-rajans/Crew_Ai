from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
from duckduckgo_search import DDGS
import os

@tool("DuckDuckGo Search")
def free_search_tool(query: str) -> str:
    """Search the web for real-time information regarding a given query."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            return str(results)
    except Exception as e:
        return f"Search error occurred: {str(e)}"

groq_llm = LLM(
    model=os.environ.get("MODEL", "groq/llama-3.3-70b-versatile"),
    temperature=0.5 # Slightly higher temperature gives the scriptwriter more creative juice
)

@CrewBase
class AiTrendCrew():
    """Enhanced 4-Agent AI Content Automation Pipeline"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trend_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_hunter'],
            tools=[free_search_tool],
            llm=groq_llm,
            verbose=True
        )

    @agent
    def social_monitor(self) -> Agent:
        return Agent(
            config=self.agents_config['social_monitor'],
            tools=[free_search_tool],
            llm=groq_llm,
            verbose=True
        )

    @agent
    def chief_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_editor'],
            llm=groq_llm,
            verbose=True 
        )

    @agent
    def content_scriptwriter(self) -> Agent:
        return Agent(
            config=self.agents_config['content_scriptwriter'],
            llm=groq_llm,
            verbose=True
        )

    @task
    def trend_hunting_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_hunting_task']
        )

    @task
    def social_monitoring_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_monitoring_task']
        )

    @task
    def editorial_task(self) -> Task:
        return Task(
            config=self.tasks_config['editorial_task'],
            output_file='weekly_ai_trend_report.md' 
        )

    @task
    def scriptwriting_task(self) -> Task:
        return Task(
            config=self.tasks_config['scriptwriting_task'],
            output_file='viral_ai_video_script.md' # Saves your script to a separate ready-to-read file!
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )