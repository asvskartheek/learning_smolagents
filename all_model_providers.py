# Local model - LMStudio
from smolagents import OpenAIServerModel
model = OpenAIServerModel(
    # model_id="qwen2.5-coder-3b-instruct",
    model_id="gemma-3-4b-it",
    api_base="http://127.0.0.1:1234/v1/",
    api_key="none",
)

# Claude
from smolagents import LiteLLMModel
from dotenv import load_dotenv
load_dotenv()
import os
model = LiteLLMModel(
    model_id="anthropic/claude-3-5-sonnet-20241022",
    temperature=0.2,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# Gemini
from smolagents import LiteLLMModel
from dotenv import load_dotenv
load_dotenv()
import os
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash", 
    temperature=0.2,
    api_key=os.environ["GEMINI_API_KEY"]
)