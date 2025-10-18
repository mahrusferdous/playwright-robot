# Playwright Robot Driver

## Overview

This project demonstrates an automated browser "robot driver" using Playwright in Python.
It includes:

-   `main.py` — Core automation that logs into https://www.saucedemo.com, finds a product, and prints its price.
-   `api.py` — Flask API wrapper to trigger the automation via HTTP requests.
-   `mcp_agent.py` — Class-based implementation of a minimal AI agent (`MCPExecutor`) that executes a predefined plan of web actions using Playwright.
-   `test_mcp_agent.py` — Test script for the `MCPExecutor` class.
-   `requirements.txt` — Python dependencies.

## Setup

Run requirements installation:

```bash
python -m venv env
```

Activate a virtual environment:

```bash
.\env\Scripts\Activate  # Windows
source env/bin/activate  # macOS/Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

To deactivate later:

```bash
deactivate
```

## Run the Core Automation

```bash
python main.py
```

## Run the Flask API (Optional)

```bash
python api.py
```

Then POST to `http://localhost:8000/run-task` with JSON:

```json
{ "product_keyword": "backpack", "headless": false, "delay": 1000 }
```

##

## Playwright AI Agent - MCP Executor

This project demonstrates a **minimal AI-driven web automation agent** using **Playwright**. The agent executes a predefined plan of steps (like clicking, typing, navigating, and reading text) on a web page. It is structured in a class-based format (`MCPExecutor`) and can be extended to integrate with a real LLM for dynamic plan generation.

---

## Features

-   Open URLs and navigate pages
-   Click elements and type into inputs
-   Read text from elements
-   Wait for elements or a specified time
-   Validate action plans before execution
-   Automatic login helper for [Sauce Demo](https://www.saucedemo.com/)
-   Step-by-step execution results with error reporting

---
