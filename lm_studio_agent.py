# !pip install smolagents[transformers]
from smolagents import CodeAgent, OpenAIServerModel, GoogleSearchTool
from dotenv import load_dotenv
load_dotenv()

model = OpenAIServerModel(
    # model_id="qwen2.5-coder-3b-instruct",
    model_id="gemma-3-4b-it",
    api_base="http://127.0.0.1:1234/v1/",
    api_key="none",
)

agent = CodeAgent(
    tools=[],model=model, add_base_tools=True
)

agent.run("Who is the CEO of Hugging Face?")