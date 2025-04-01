# NOTE: QUESTIONABLE RESULTS [WIP]
model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    HfApiModel,
    GoogleSearchTool,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
)
from dotenv import load_dotenv

load_dotenv()

model = HfApiModel(model_id)

web_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches for you.",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent],
    additional_authorized_imports=["time", "numpy", "pandas"],
)

answer = manager_agent.run(
    "If LLM training continues to scale up at the current rhythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What would that correspond to, compared to some countries? Please provide a source for any numbers used."
)
