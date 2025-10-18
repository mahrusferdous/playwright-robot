"""
MCP Agent Executor Module
Handles validation and execution of action plans on web pages using Playwright.
"""

from typing import List, Dict, Any
from playwright.sync_api import Page
import time

class MCPExecutor:
    ALLOWED_ACTIONS = {"click", "read_text", "wait"}

    def __init__(self, page: Page):
        self.page = page

    def validate_plan(self, plan: List[Dict[str, Any]]):
        for step in plan:
            action = step.get("action")

            # Check if action exists and is allowed
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

                # Handle click action
                if action == "click":
                    selector = step["selector"]
                    index = step.get("index", 0) # default to first element

                    self.page.wait_for_selector(selector, timeout=5000) # Wait for element(s) to appear
                    elements = self.page.query_selector_all(selector) # Get all matching elements

                    if index < len(elements):
                        elements[index].click()
                        results.append({"status": "ok", "step": step})
                    else:
                        results.append({
                            "status": "error",
                            "step": step,
                            "reason": f"Element not found at index {index} for selector '{selector}'"
                        })
                        break

                # handle read_text action
                elif action == "read_text":
                    selector = step["selector"]
                    index = step.get("index", 0) # default to first element

                    self.page.wait_for_selector(selector, timeout=5000) # Wait for element(s) to appear
                    elements = self.page.query_selector_all(selector) # Get all matching elements

                    if elements:
                        text_value = elements[index].inner_text()
                        results.append({
                            "status": "ok",
                            "step": step,
                            "value": text_value
                        })
                    else:
                        results.append({
                            "status": "error",
                            "step": step,
                            "reason": f"Element not found for selector '{selector}'"
                        })
                        break

                elif action == "wait":
                    time.sleep(step.get("seconds", 1))
                    results.append({"status": "ok", "step": step})

            except Exception as e:
                results.append({"status": "exception", "error": str(e), "step": step})
                break

        return results

    def auto_login_sauce(self, username="standard_user", password="secret_sauce"):
        self.page.goto("https://www.saucedemo.com/")
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        time.sleep(2)  # wait for inventory page to load
