# jarvis project
Personal Assistant for the AI &amp; Robotics Club
# AI Intent-Based Browser Agent

An end-to-end system that **automatically performs web tasks** based on **user intent classification**. The system combines **NLP-based intent classification** with an **AI-driven browser agent**, enabling hands-free automation of tasks like searching, clicking, filling forms, and extracting data.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Example Workflow](#example-workflow)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project integrates two main components:

1. **Intent Classification**
   - Understands the user's goal from natural language input.
   - Produces structured output (JSON) containing `intent` and `entities`.

2. **AI Browser Agent**
   - Maps intents to browser actions automatically.
   - Executes tasks on the web without manual intervention.

This combination allows **automated execution of complex web tasks** triggered by natural language commands.

---

## Features

- Accepts natural language commands
- Automatic intent classification
- Entity extraction for parameterized actions
- Browser automation using Playwright or Selenium
- Supports multi-step task execution
- Modular architecture for easy extension
- Optional feedback or result extraction

---

## Architecture
```
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
Task Execution / Feedback
```

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/username/intent-agent.git
cd intent-agent
```

Install dependencies
```
pip install -r requirements.txt
```

Install Playwright browsers
```
playwright install
```

Set API keys (if using GPT API) in .env file:
```
OPENAI_API_KEY=your_api_key_here
```
Usage
Run the agent with a sample intent JSON:

```
python run_agent.py
```

Sample intent JSON input

```
{
  "intent": "add_to_cart",
  "entities": {"product": "milk"}
}
```
Agent automatically performs the task in the browser.

```
Example Workflow
User Input:
"Add milk to my shopping cart"
```

Intent Classifier Output:
```
{
  "intent": "add_to_cart",
  "entities": {"product": "milk"}
}
```

Action Planner Maps Intent → Actions:
```
[
  {"action": "open_page", "url": "https://www.example.com/shop"},
  {"action": "search", "product": "milk"},
  {"action": "click", "selector": ".add-to-cart-btn"}
]
```

- AI Browser Agent Executes Actions Automatically

- Task Completed / Feedback Provided

- Contributing
```
Fork the repository

Create a new branch: git checkout -b feature/your-feature

Commit changes: git commit -m "Add new feature"

Push branch: git push origin feature/your-feature

Open a Pull Request
```

License
This project is licensed under the MIT License – see the LICENSE file for details.


