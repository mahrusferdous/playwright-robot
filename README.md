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

The MCP Executor is a class-based implementation of a minimal AI agent that executes a predefined plan of web actions using Playwright. It validates the action plan before execution and provides step-by-step results with error reporting.

## Features

-   Validates action plans before execution
-   Executes a series of web actions (click, fill, read text, wait)
-   Provides detailed step-by-step execution results
-   Supports error handling and reporting

## To Use the MCP Executor

Api key Setup:

1. Sign up for a Cohere account at [Cohere](https://cohere.com/).
2. Navigate to the API Keys section in your Cohere dashboard.
3. Generate a new API key and copy it.
4. Replace the placeholder `"YOUR_VALID_COHERE_API_KEY_HERE"` in `MCP_Agent/main.py` with your actual API key.

To use the MCP Executor, run the following command:

```
cd MCP_Agent
python main.py
```

---
