# jarvis
Personal Assistant for the AI &amp; Robotics Club

AI Intent-Based Browser Agent

An end-to-end system that automatically performs tasks on the web based on user intent classification. The system combines NLP-based intent classification with an AI-driven browser agent, allowing users to execute complex web tasks without manual input.

Table of Contents

Overview

Features

Architecture

Technologies Used

Setup & Installation

Usage

Example Workflow

Contributing

License

Overview

This project integrates two main components:

Intent Classification:

Identifies the user's goal from natural language input.

Output: structured JSON containing intent and entities.

AI Browser Agent:

Automatically maps intents to browser actions.

Performs tasks like searching, clicking, typing, and extracting data without manual intervention.

This combination allows hands-free automation of web tasks triggered by natural language commands.

Features

Natural language input support

Automatic intent classification

Entity extraction for parameterized actions

Browser automation using Playwright or Selenium

Multi-step task execution

Modular architecture (easy to extend with new intents)

Optional feedback or result extraction

Architecture
User Input (Natural Language)
            ↓
Intent Classifier (NLP Model)
            ↓
Intent + Entities (JSON)
            ↓
Action Planner / Task Mapper
            ↓
AI Browser Agent (Playwright / Selenium)
            ↓
Task Execution / Result

Technologies Used

Python 3.10+

Playwright – browser automation

OpenAI GPT-5-mini API – intent classification & entity extraction (optional)

JSON – structured data exchange

Optional: HuggingFace Transformers for local intent classification

Setup & Installation

Clone the repository:

git clone https://github.com/username/intent-agent.git
cd intent-agent


Install dependencies:

pip install -r requirements.txt


Install Playwright browsers:

playwright install


Set API keys (if using GPT API) in .env:

OPENAI_API_KEY=your_api_key_here

Usage

Run the agent with a sample intent JSON:

python run_agent.py


Provide sample input (for testing):

{
  "intent": "add_to_cart",
  "entities": {"product": "milk"}
}


Agent automatically performs the task in the browser.

Example Workflow

User Input: "Add milk to my shopping cart"

Intent Classifier Output:

{
  "intent": "add_to_cart",
  "entities": {"product": "milk"}
}


Action Planner Maps Intent → Actions:

[
  {"action": "open_page", "url": "https://www.example.com/shop"},
  {"action": "search", "product": "milk"},
  {"action": "click", "selector": ".add-to-cart-btn"}
]


AI Browser Agent Executes Actions Automatically

Task Completed / Feedback Provided

Contributing

Fork the repository

Create a new branch: git checkout -b feature/intent-agent

Commit changes: git commit -m "Add new feature"

Push branch: git push origin feature/intent-agent

Open a Pull Request

License

This project is licensed under the MIT License – see the LICENSE
 file for details.
