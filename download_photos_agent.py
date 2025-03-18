# This agent is designed to download photos from the internet. It uses the download_image tool to download images from the internet.
# WORK IN PROGRESS
# - download_image_agent works only with Claude and a detailed prompt.
# - analyze_script_agent works only "kinda" with Claude and a detailed prompt (Did not verify if the output is comprehensive enough)
from smolagents import CodeAgent, OpenAIServerModel, GoogleSearchTool, tool, LiteLLMModel
import os
from dotenv import load_dotenv
load_dotenv()

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
    img.save("photos/"+filename, "jpeg")

@tool
def get_script_content(file_path: str) -> str:
    """
    Given a file path, read the content of the file and return it as a string.
    Args:
        file_path: The path to the file to read.
    Returns:
        The content of the file as a string.
    """
    with open(file_path, "r") as file:
        return file.read()



model = OpenAIServerModel(
    # model_id="qwen2.5-coder-3b-instruct",
    model_id="gemma-3-4b-it",
    api_base="http://127.0.0.1:1234/v1/",
    api_key="none",
)
# model = LiteLLMModel(
#     model_id="anthropic/claude-3-5-sonnet-20241022",
#     temperature=0.2,
#     api_key=os.environ["ANTHROPIC_API_KEY"]
# )
# model = LiteLLMModel(
#     model_id="gemini/gemini-2.0-flash", 
#     temperature=0.2,
#     api_key=os.environ["GEMINI_API_KEY"]
# )

analyze_script_agent = CodeAgent(
    tools=[get_script_content], model=model, add_base_tools=False, planning_interval=5, max_steps=10, additional_authorized_imports=[]
)

# download_image_agent = CodeAgent(
#     tools=[download_image],model=model, add_base_tools=True, planning_interval=5, max_steps=10, additional_authorized_imports=["bs4", "requests", "PIL", "io"]
# )


if __name__ == "__main__":
    # download_image('https://www.newindian.in/wp-content/uploads/2025/03/1-24.webp', 'aimplb_waqf_protest_jantar_mantar.jpg')
    analyze_script_agent.run("Go through the local script file at the path: ./test_script.txt and read the entire script, analyze the script, then create a comprehensive list of all the images that needed to be downloaded, in order to successfully make a video out of the script. Each entry must be atomic, as in only one image per entry. Be very elaborate and descriptive for each image. We would use each entry as a google search query to find an image for that and download it. Do not include any visualisations, that need to be created. An example entry of the list: 'protest at Jantar Mantar by the All India Muslim Personal Law Board (AIMPLB) against Waqf Ammendment bill'")
    # download_image_agent.run("Websearch protest at Jantar Mantar by the All India Muslim Personal Law Board (AIMPLB) against Waqf Ammendment bill, Visit a news article with potential of having a photograph. Look at the entire source code and scrape the appropriate image link. Download the photograph.")