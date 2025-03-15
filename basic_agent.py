from smolagents import CodeAgent, HfApiModel, LiteLLMModel
from dotenv import load_dotenv
load_dotenv()
import os

# model = HfApiModel()
model = LiteLLMModel("openrouter/deepseek/deepseek-r1-distill-qwen-14b:free", api_key=os.environ["OPENROUTER_API_KEY"])

agent = CodeAgent(
    tools=[],model=model, add_base_tools=True
)

agent.run("Who is the CEO of Hugging Face?")