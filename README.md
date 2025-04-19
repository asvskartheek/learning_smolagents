# Learning SmoLAgents

This repository contains various examples and experiments using the [smolagents](https://github.com/huggingface/smolagents) library to build AI agents for different tasks.

## Overview

SmoLAgents is a lightweight framework for building AI agents that can perform various tasks autonomously. This repository demonstrates different applications of SmoLAgents, including:

- LinkedIn job search automation
- YouTube script generation
- News video creation
- Trip planning
- Text to SQL conversion
- House cost estimation
- And more!

## Project Structure

- `linkedin_job_search_agent.py`: An agent that can search and apply for jobs on LinkedIn
- `yt_script_writer.py`: Generates YouTube video scripts
- `script_to_presentation_agent.py`: Converts scripts to PowerPoint presentations
- `download_photos_agent.py`: Downloads relevant images for presentations
- `browser_automation.py`: Utilities for web browser automation
- `text_to_sql.py`: Converts natural language to SQL queries
- `trip_planner.py`: Plans trips based on user preferences
- `house_cost_estimator.py`: Estimates house costs based on various factors

## Installation

1. Clone this repository:
```bash
git clone https://github.com/asvskartheek/learning_smolagents.git
cd learning_smolagents
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and other configuration
```

## Usage Examples

### LinkedIn Job Search Agent

This agent can autonomously search for jobs on LinkedIn and apply to them using the "Easy Apply" feature.

```python
from linkedin_job_search_agent import LinkedInJobSearchAgent

agent = LinkedInJobSearchAgent()
agent.run(job_title="AI Engineer", location="Switzerland")
```

See [linkedin_job_search_agent.py](./linkedin_job_search_agent.py) for more details.

### YouTube Script Generation

Generate scripts for YouTube videos on various topics:

```python
from yt_script_writer import generate_script

script = generate_script(topic="AI Agents")
print(script)
```

See [yt_script.md](./yt_script.md) for an example output.

### News Video Creation

The process of creating a news video involves several steps as outlined in [news_video.md](./news_video.md):

1. Research a topic using web search
2. Find good source documents
3. Write a YouTube script
4. Download needed images
5. Create a PowerPoint presentation
6. Sync the presentation with audio output

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.