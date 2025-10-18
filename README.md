# Playwright Robot Driver

## Overview

This project demonstrates an automated browser "robot driver" using Playwright in Python.
It includes:

-   `main.py` — Core automation that logs into https://www.saucedemo.com, finds a product, and prints its price.
-   `api.py` — Flask API wrapper to trigger the automation via HTTP requests.
-   `mcp_agent.py` — Scaffold for integrating an LLM via the MCP pattern (illustrative).
-   `env` — Python virtual environment with dependencies.

## Setup

Run requirements installation:

```bash
python -m venv env
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
python -m playwright install
```

Activate a virtual environment:

```bash
.\env\Scripts\Activate  # Windows
source env/bin/activate  # macOS/Linux
```

To deactivate later:

```bash
deactivate
```

## Run the Core Automation

-   Headless (default):

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
