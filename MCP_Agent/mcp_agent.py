"""
MCP Agent Executor Module
Handles validation and execution of action plans on web pages using Playwright.
"""

from typing import List, Dict, Any
from playwright.sync_api import Page
import time

class MCPExecutor:
    ALLOWED_ACTIONS = {"goto", "click", "fill", "read_text", "wait"}

    def __init__(self, page: Page):
        self.page = page

    def validate_plan(self, plan: List[Dict[str, Any]]):
        for step in plan:
            if not isinstance(step, dict):
                return False, f"Step is not a dict: {step}"
            action = step.get("action")
            if not action:
                return False, f"Missing 'action' key in step: {step}"
            if action not in self.ALLOWED_ACTIONS:
                return False, f"Invalid action '{action}' in step: {step}"
        return True, "ok"

    def execute_plan(self, plan: List[Dict[str, Any]]):
        results = []
        for step in plan:
            try:
                action = step["action"]

                if action == "goto":
                    self.page.goto(step["url"])
                    results.append({"status": "ok", "step": step})

                elif action == "click":
                    selector = step["selector"]
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    results.append({"status": "ok", "step": step})

                elif action == "fill":
                    selector = step["selector"]
                    value = step.get("value", "")
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.fill(selector, value)
                    results.append({"status": "ok", "step": step})

                elif action == "read_text":
                    selector = step["selector"]
                    self.page.wait_for_selector(selector, timeout=5000)
                    text_value = self.page.inner_text(selector)
                    results.append({"status": "ok", "step": step, "value": text_value})

                elif action == "wait":
                    seconds = step.get("seconds", 1)
                    time.sleep(seconds)
                    results.append({"status": "ok", "step": step})

            except Exception as e:
                results.append({"status": "exception", "error": str(e), "step": step})
                break
        return results
