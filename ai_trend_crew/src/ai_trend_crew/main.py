#!/usr/bin/env python
import os
import sys

# This magic block dynamically adds the 'src' folder to Python's search path
# It completely eliminates the 'ModuleNotFoundError' glitch!
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ai_trend_crew.crew import AiTrendCrew

def run():
    """
    Kickoff the AI trend hunting crew execution.
    """
    print("🚀 Initializing your AI Trend Crew...")
    AiTrendCrew().crew().kickoff()

if __name__ == "__main__":
    run()