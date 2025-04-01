model_id = "Qwen/QwQ-32B"
from smolagents import (
    CodeAgent,
    HfApiModel,
    GoogleSearchTool,
    VisitWebpageTool,
    PythonInterpreterTool,
    FinalAnswerTool,
    LiteLLMModel,
)
from huggingface_hub import login, HfFolder
import os

from dotenv import load_dotenv

load_dotenv()

# Only login if not already authenticated
if not HfFolder.get_token():
    login()

task = """
Search the average cost of construction materials (cement, steel, and bricks) in Hyderabad.
Estimate the cost of building a 2,000 square foot house based on these material costs.
Include labor and other costs in the estimate (consider 2.25x the material cost for labor).
Provide a detailed cost breakdown and generate a visualization of the results.
"""
model = HfApiModel(model_id)
# model = LiteLLMModel("openrouter/qwen/qwq-32b:free", api_key=os.environ["OPENROUTER_API_KEY"])
agent = CodeAgent(
    tools=[
        GoogleSearchTool(),
        VisitWebpageTool(),
        PythonInterpreterTool(),
        FinalAnswerTool(),
    ],
    model=model,
    add_base_tools=False,
    additional_authorized_imports=["matplotlib"],
    planning_interval=5,
    max_steps=12,
)

agent.run(task)
