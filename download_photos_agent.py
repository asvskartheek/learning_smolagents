# WORK IN PROGRESS - So far works only with Claude and a detailed prompt.
# This agent is designed to download photos from the internet. It uses the download_image tool to download images from the internet.
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



# model = OpenAIServerModel(
#     # model_id="qwen2.5-coder-3b-instruct",
#     model_id="gemma-3-4b-it",
#     api_base="http://127.0.0.1:1234/v1/",
#     api_key="none",
# )
model = LiteLLMModel(
    model_id="anthropic/claude-3-5-sonnet-20241022",
    temperature=0.2,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

agent = CodeAgent(
    tools=[download_image],model=model, add_base_tools=True, planning_interval=5, max_steps=10, additional_authorized_imports=["bs4", "requests", "PIL", "io"]
)


if __name__ == "__main__":
    # download_image('https://www.newindian.in/wp-content/uploads/2025/03/1-24.webp', 'aimplb_waqf_protest_jantar_mantar.jpg')
    agent.run("Websearch protest at Jantar Mantar by the All India Muslim Personal Law Board (AIMPLB) against Waqf Ammendment bill, Visit a news article with potential of having a photograph. Look at the entire source code and scrape the appropriate image link. Download the photograph.")