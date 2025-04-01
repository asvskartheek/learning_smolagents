from smolagents import (
    CodeAgent,
    HfApiModel,
    GoogleSearchTool,
    VisitWebpageTool,
    PythonInterpreterTool,
)
from huggingface_hub import login, HfFolder

# Only login if not already authenticated
if not HfFolder.get_token():
    login()

task = """
Plan a trip to Belgium for 2 weeks.
- Make the plan detailed, with specific activities, with time slots and which places to visit, along with their ratings.
- I have tickets for the f1 2025 in Spa-Francorchamps. This is the mid-point of my trip, only going on Sunday to the race.
- I am doing WFH those 2 weeks from 6AM to 2PM. I only work 5 days a week.
- I will be living with my girlfriend in Knokke-Heist. She doesnt have a car.
- Her parents live in Ham. Her father does have a car
- I love cycling, I definitely want to see Netherlands some point of the time.
- Don't have budget to do overnight stay anywhere other their houses.
"""
model = HfApiModel()
# model = LiteLLMModel(
#     model_id="anthropic/claude-3-5-sonnet-20241022",
#     temperature=0.2,
#     api_key=os.environ["ANTHROPIC_API_KEY"]
# )
agent = CodeAgent(
    tools=[
        GoogleSearchTool(),
        VisitWebpageTool(),
        PythonInterpreterTool(),
    ],
    model=model,
    add_base_tools=False,
    additional_authorized_imports=["numpy"],
    planning_interval=5,
    max_steps=15,
)

agent.run(task)
