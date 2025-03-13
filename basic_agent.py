from smolagents import CodeAgent, HfApiModel
from dotenv import load_dotenv
load_dotenv()

model = HfApiModel()

agent = CodeAgent(
    tools=[],model=model, add_base_tools=True
)

agent.run("Who is the CEO of Hugging Face?")