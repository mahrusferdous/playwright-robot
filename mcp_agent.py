# mcp_agent.py
"""
SCaffold showing how to integrate an LLM with Playwright's MCP Server.
This is an illustrative example (no external LLM calls made).
You would:
- start a Playwright MCP server that exposes page context (aria roles, element list)
- provide that structured context to an LLM with system & user prompts
- LLM returns a JSON plan like:
  [{"action":"click","selector":"#add-to-cart-sauce-labs-backpack"}, {"action":"type","selector":"#zipcode","value":"10001"}, ...]
- The script validates the plan and executes it with Playwright.

This file sketches the validation/execution loop.
"""

import json
from typing import List, Dict, Any

# Example of a plan schema the LLM should return
PLAN_SCHEMA_EXAMPLE = [
    {"action": "click", "selector": ".inventory_item_name", "index": 0},
    {"action": "click", "selector": ".add-to-cart-button", "index": 0},
    {"action": "open_url", "url": "https://www.saucedemo.com/cart.html"},
    {"action": "read_text", "selector": ".cart_item .inventory_item_name"}
]

def validate_plan(plan: List[Dict[str, Any]]):
    allowed_actions = {"click", "type", "open_url", "read_text", "navigate", "wait"}
    for step in plan:
        if "action" not in step or step["action"] not in allowed_actions:
            return False, f"Invalid action in step: {step}"
        # you can add extra schema validation here
    return True, "ok"

def execute_plan_with_playwright(plan, playwright_page):
    """
    Minimal executor: walk steps, mapping them to Playwright calls.
    Must handle exceptions and timeouts robustly.
    """
    results = []
    for step in plan:
        try:
            a = step["action"]
            if a == "open_url" or a == "navigate":
                playwright_page.goto(step["url"])
                results.append({"status":"ok","step":step})
            elif a == "click":
                sel = step["selector"]
                idx = step.get("index", 0)
                els = playwright_page.query_selector_all(sel)
                if len(els) > idx:
                    els[idx].click()
                    results.append({"status":"ok","step":step})
                else:
                    results.append({"status":"error","step":step,"reason":"selector not found"})
                    break
            elif a == "type":
                sel = step["selector"]
                value = step.get("value","")
                el = playwright_page.query_selector(sel)
                if el:
                    el.fill(value)
                    results.append({"status":"ok","step":step})
                else:
                    results.append({"status":"error","step":step,"reason":"selector not found"})
                    break
            elif a == "read_text":
                sel = step["selector"]
                el = playwright_page.query_selector(sel)
                if el:
                    results.append({"status":"ok","step":step,"value":el.inner_text()})
                else:
                    results.append({"status":"error","step":step,"reason":"selector not found"})
                    break
            elif a == "wait":
                import time
                time.sleep(step.get("seconds", 1))
                results.append({"status":"ok","step":step})
        except Exception as e:
            results.append({"status":"exception","error":str(e),"step":step})
            break
    return results

# NOTE:
# To integrate with a real LLM, you would:
# - fetch structured page context from the MCP server (DOM snapshot with roles/labels)
# - create a system prompt describing allowed actions & schema and an example
# - send (context + prompt) to LLM (e.g., OpenAI) and ask for JSON output only
# - validate the JSON (schema) then execute with execute_plan_with_playwright()
