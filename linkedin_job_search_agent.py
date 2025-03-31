from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import helium
from helium import *
from smolagents import CodeAgent, tool, ActionStep
from time import sleep
from io import BytesIO
from PIL import Image
import undetected_chromedriver as uc

# Load environment variables
load_dotenv()

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

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_profile = "/Users/asvs/Library/Application Support/Google/Chrome"
chrome_options.add_argument(f"--user-data-dir={chrome_profile}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--password-store=basic")
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1350")
chrome_options.add_argument("--disable-pdf-viewer")
chrome_options.add_argument("--window-position=0,0")

driver = uc.Chrome(options=chrome_options)
set_driver(driver)

def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    driver = helium.get_driver()
    current_step = memory_step.step_number
    if driver is not None:
        for previous_memory_step in agent.memory.steps:  # Remove previous screenshots for lean processing
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                previous_memory_step.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists

    # Update observations with current URL
    url_info = f"Current url: {driver.current_url}"
    memory_step.observations = (
        url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
    )

@tool
def click(element: str) -> None:
    """
    Clicks on the element with the given text.
    Args:
        element: The text of the element to click.
    """
    driver.find_element(By.XPATH, f"//*[contains(text(), '{element}')]").click()

@tool
def get_page_source() -> None:
    """
    Get the current page's full HTML code, useful for getting the exact elements to interact with.
    """
    return driver.page_source

from smolagents import Tool

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

agent = CodeAgent(
    tools=[HumanInterventionTool()],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    planning_interval=10,
    max_steps=25,
    verbosity_level=2,
)

# Import helium for the agent
agent.python_executor("from helium import *")

helium_instructions = """
You can use helium to access websites. Don't bother about the helium driver, it's already managed.
We've already ran "from helium import *"
Then you can go to pages!
Code:
go_to('github.com/trending')
```<end_code>

You can directly click clickable elements by inputting the text that appears on them.
Code:
click("Top products")
```<end_code>

If it's a link:
Code:
click(Link("Top products"))
```<end_code>

If you try to interact with an element and it's not found, you'll get a LookupError.
In general stop your action after each button click to see what happens on your screenshot.
Never try to login in a page.

To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
Code:
scroll_down(num_pixels=1200) # This will scroll one viewport down
```<end_code>

When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
Just use your built-in tool `close_popups` to close them:
Code:
close_popups()
```<end_code>

You can use .exists() to check for the existence of an element. For example:
Code:
if Text('Accept cookies?').exists():
    click('I accept')
```<end_code>

To fill in a form or use a search bar, use the `write` function. For example, to use search bar:
Code:
import helium
write("AI engineer jobs", into="Search")
press(helium.ENTER)
```<end_code>
"""

agent_request = """Open LinkedIn and login with Gmail, if not already logged in. Then search for AI engineer jobs in Switzerland. If you need any help, ask me. I can do those steps for you. See if any of those have easy apply and apply to one job, by submitting the application with any details that are already there, dont change anything. If you are confused at any point, ask me."""

agent_output = agent.run(agent_request + helium_instructions)