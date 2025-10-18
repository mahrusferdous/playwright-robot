# Playwright Robot Driver

## Overview

This project demonstrates an automated browser "robot driver" using Playwright in Python.
It includes:

-   `main.py` — Core automation that logs into https://www.saucedemo.com, finds a product, and prints its price.
-   `api.py` — Optional FastAPI endpoint to trigger the automation via HTTP.
-   `mcp_agent.py` — Scaffold for integrating an LLM via the MCP pattern (illustrative).
-   `requirements.txt` — Python dependencies.

## Setup

1. Activate a virtual environment:

```bash
.\env\Scripts\Activate  # Windows
source env/bin/activate  # macOS/Linux
```

## Run the Core Automation

-   Headless (default):

```bash
python main.py
```

-   Headed (for debugging):

```bash
python main.py headed
or
python main.py headed backpack 2000
```

## Run the Flask API (Optional)

```bash
python api.py
```

Then POST to `http://localhost:8000/run-task` with JSON:

```json
{ "product_keyword": "backpack", "headless": true }
```
