# Finally fucking works! With Gemini-2.0-Flash model.
from io import BytesIO
from time import sleep

import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from smolagents import CodeAgent, tool
from smolagents.agents import ActionStep

# Load environment variables
load_dotenv()

# Model - Gemini
from smolagents import LiteLLMModel
from dotenv import load_dotenv

load_dotenv()
import os

model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    temperature=0.2,
    api_key=os.environ["GEMINI_API_KEY"],
)

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1350")
chrome_options.add_argument("--disable-pdf-viewer")
chrome_options.add_argument("--window-position=0,0")

# Initialize the browser
driver = helium.start_chrome(headless=False, options=chrome_options)


@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(
            f"Match n°{nth_result} not found (only {len(elements)} matches found)"
        )
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result


@tool
def go_back() -> None:
    """Goes back to previous page."""
    driver.back()


@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    This does not work on cookie consent banners.
    """
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


@tool
def click(element: str) -> None:
    """
    Clicks on the element with the given text.
    Args:
        element: The text of the element to click.
    """
    driver.find_element(By.XPATH, f"//*[contains(text(), '{element}')]").click()


@tool
def right_click(element: str) -> None:
    """
    Right clicks on the element with the given text. Use right click on an image, to download it.
    Args:
        element: The text of the element to click.
    NOTE: TOOL IS WORK IN PROGRESS, CODE IS CORRECT BUT WE CANNOT USE TEXT FOR RIGHT CLICKING ON IMAGES.
    """
    from selenium.webdriver.common.action_chains import ActionChains

    element = driver.find_element(By.XPATH, f"//*[contains(text(), '{element}')]")
    ActionChains(driver).context_click(element).perform()


# Set up screenshot callback
def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    driver = helium.get_driver()
    current_step = memory_step.step_number
    if driver is not None:
        for (
            previous_memory_step
        ) in agent.memory.steps:  # Remove previous screenshots for lean processing
            if (
                isinstance(previous_memory_step, ActionStep)
                and previous_memory_step.step_number <= current_step - 2
            ):
                previous_memory_step.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        memory_step.observations_images = [
            image.copy()
        ]  # Create a copy to ensure it persists

    # Update observations with current URL
    url_info = f"Current url: {driver.current_url}"
    memory_step.observations = (
        url_info
        if memory_step.observations is None
        else memory_step.observations + "\n" + url_info
    )


# Download the image
@tool
def download_image(url: str, filename: str) -> None:
    """
    Given a URL of an image on the internet, download it, convert it to standard jpeg format, then saves to the local file system.

    Args:
        url: The URL of the image to download.
        filename: The name of the file to save the image to.
    """
    import requests
    from PIL import Image
    from io import BytesIO

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save("photos/" + filename, "jpeg")


# Create the agent
agent = CodeAgent(
    tools=[go_back, close_popups, search_item_ctrl_f],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    max_steps=20,
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
"""

search_request = """
Please navigate to https://en.wikipedia.org/wiki/Chicago and give me a sentence containing the word "1992" that mentions a construction accident.
"""
# search_request = """
# Navigate to https://google.com run a search on the recent protests against Waqf ammendment bill in India by AIMPLB. Navigate to one of the search results and download an image of the protest.
# """

agent_output = agent.run(search_request + helium_instructions)
print("Final output:")
print(agent_output)
