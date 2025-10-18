# mcp_agent.py
from typing import List, Dict, Any
from playwright.sync_api import Page
import time

class MCPExecutor:
    ALLOWED_ACTIONS = {"click", "type", "open_url", "read_text", "navigate", "wait"}

    def __init__(self, page: Page):
        self.page = page

    def validate_plan(self, plan: List[Dict[str, Any]]):
        for step in plan:
            if "action" not in step or step["action"] not in self.ALLOWED_ACTIONS:
                return False, f"Invalid action in step: {step}"
        return True, "ok"

    def execute_plan(self, plan: List[Dict[str, Any]]):
        results = []
        for step in plan:
            try:
                action = step["action"]

                if action in ["open_url", "navigate"]:
                    self.page.goto(step["url"])
                    results.append({"status": "ok", "step": step})

                elif action == "click":
                    sel = step["selector"]
                    idx = step.get("index", 0)
                    self.page.wait_for_selector(sel, timeout=5000)
                    els = self.page.query_selector_all(sel)
                    if len(els) > idx:
                        els[idx].click()
                        results.append({"status": "ok", "step": step})
                    else:
                        results.append({"status": "error", "step": step, "reason": "selector not found"})
                        break

                elif action == "type":
                    sel = step["selector"]
                    value = step.get("value", "")
                    self.page.wait_for_selector(sel, timeout=5000)
                    el = self.page.query_selector(sel)
                    if el:
                        el.fill(value)
                        results.append({"status": "ok", "step": step})
                    else:
                        results.append({"status": "error", "step": step, "reason": "selector not found"})
                        break

                elif action == "read_text":
                    sel = step["selector"]
                    self.page.wait_for_selector(sel, timeout=5000)
                    el = self.page.query_selector(sel)
                    if el:
                        results.append({"status": "ok", "step": step, "value": el.inner_text()})
                    else:
                        results.append({"status": "error", "step": step, "reason": "selector not found"})
                        break

                elif action == "wait":
                    time.sleep(step.get("seconds", 1))
                    results.append({"status": "ok", "step": step})

            except Exception as e:
                results.append({"status": "exception", "error": str(e), "step": step})
                break

        return results

    def auto_login_saucedemo(self, username="standard_user", password="secret_sauce"):
        """Quick helper to login if using saucedemo.com"""
        self.page.goto("https://www.saucedemo.com/")
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        time.sleep(2)  # wait for inventory page to load
