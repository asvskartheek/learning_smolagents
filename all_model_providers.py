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
import os

load_dotenv()
model = LiteLLMModel(
    model_id="anthropic/claude-3-5-sonnet-20241022",
    temperature=0.2,
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

# Gemini
from smolagents import LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    temperature=0.2,
    api_key=os.environ["GEMINI_API_KEY"],
)

# Hf Api model
from smolagents import HfApiModel

model_id = "meta-llama/Llama-3.3-70B-Instruct"
model = HfApiModel(model_id=model_id)

# OpenRouter
from smolagents import LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()
model = LiteLLMModel(
    model_id="openrouter/qwen/qwq-32b:free", api_key=os.environ["OPENROUTER_API_KEY"]
)

# AzureOpenAI
from smolagents import AzureOpenAIServerModel
from dotenv import load_dotenv
import os

load_dotenv()
model = AzureOpenAIServerModel(
    model_id=os.environ.get("AZURE_DEPLOYMENT"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)
