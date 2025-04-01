# Model - Gemini
from smolagents import LiteLLMModel
from dotenv import load_dotenv
load_dotenv()
import os
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash", 
    # model_id="gemini/gemini-2.5-pro-exp-03-25",
    temperature=0.2,
    api_key=os.environ["GEMINI_API_KEY"]
)

# AzureOpenAI
from smolagents import AzureOpenAIServerModel
from dotenv import load_dotenv
import os

load_dotenv()
model = AzureOpenAIServerModel(
    model_id = os.environ.get("AZURE_DEPLOYMENT"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION")    
)

# Agent
from smolagents import CodeAgent, GoogleSearchTool, VisitWebpageTool, Tool, tool, GradioUI
class HumanInterventionTool(Tool):
    """
    A universal human-in-the-loop tool.
    
    scenario="clarification":
        Ask an open-ended question and return user’s text.
    scenario="approval":
        Ask for YES/NO confirmation from the user.
    scenario="multiple_choice":
        Present a list of options and return the chosen index (or text).
    """
    name = "human_intervention"
    description = (
        "A single human tool for clarifications, approvals, and multiple-choice decisions. "
        "Call with 'scenario' = one of ['clarification', 'approval', 'multiple_choice']."
    )
    inputs = {
        "scenario": {
            "type": "string",
            "description": "One of: 'clarification', 'approval', 'multiple_choice'."
        },
        "message_for_human": {
            "type": "string",
            "description": "Display text or question for the user."
        },
        "choices": {
            "type": "array",
            "description": "If scenario='multiple_choice', list of option strings. Otherwise can be empty.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, scenario: str, message_for_human: str, choices: list = None) -> str:
        if scenario not in ["clarification", "approval", "multiple_choice"]:
            raise ValueError("Must be 'clarification', 'approval', or 'multiple_choice'.")

        print("\n[HUMAN INTERVENTION]")
        print(f"Scenario: {scenario}")
        print(f"Agent says: {message_for_human}")

        if scenario == "clarification":
            user_input = input("\nType your response: ")
            return user_input

        elif scenario == "approval":
            print("Type 'YES' or 'NO' to proceed:")
            user_input = input("Your decision: ").strip().upper()
            return user_input

        elif scenario == "multiple_choice":
            if not choices:
                return "No choices were provided."
            print("\nAvailable options:")
            for i, choice in enumerate(choices, start=1):
                print(f"{i}. {choice}")
            user_input = input("\nEnter the number of your chosen option: ")
            return user_input

@tool
def read_code(file_path: os.PathLike) -> str:
    """
    Reads the content of a code file and returns it as a string.
    Args:
        file_path: Path to the code file.
    """
    with open(file_path, 'r') as file:
        return file.read()

@tool 
def save_script(script: str, file_path: os.PathLike) -> None:
    """
    Saves the generated script to a text file.
    Args:
        script: The script content to save.
        file_path: Path to the output text file.
    """
    with open(file_path, 'w') as file:
        file.write(script)

agent = CodeAgent(
    tools=[HumanInterventionTool(), GoogleSearchTool(), VisitWebpageTool(), read_code, save_script],
    model=model,
    planning_interval=10,
    max_steps=25,
    verbosity_level=2,
)

GradioUI(agent).launch()

agent.run(
    """
    I want to make a YouTube video on how I made an AI agent that applies for jobs on LinkedIn. Code is in `linkedin_job_search_agent.py`. Your task is to write a script for the video, including:
    1. An introduction to the project.
    2. A high-level overview of how the agent works.
    3. What is a code agent and how it differs from a regular agent, how we made use of it.
    3. Explanation of the smolagents library.
    4. Using several tools, we gave the agent to interact with the web and human.
    5. Detailed explanation of any interesting or complex parts of the code.
    6. Demo of the agent in working.
    7. Conclusion and future improvements.

    Video script should be in a conversational tone, as if you are demonstrating the project to a friend. Use simple language and avoid jargon. The script should be detailed enough for someone to understand the project without looking at the code.
    The script should be divided into sections with clear headings. Use bullet points or numbered lists where appropriate. Include examples or analogies to explain complex concepts. Make it into markdown format for easy readability.

    This script will be directly used for video shooting, editing, voiceover, and subtitles. The script should be formatted in a way that editor knows their job, narrator knows their job, and subtitles are generated correctly. Use clear and concise language, and avoid unnecessary jargon. The script should be easy to read and understand.
    Use headings, bullet points, and numbered lists to organize the content. The script should be detailed enough for someone to understand the project without looking at the code.

    Finally, save the script to a file named `yt_script.md`.
    """
)