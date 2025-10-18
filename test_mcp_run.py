from mcp_agent import MCPExecutor
from playwright.sync_api import sync_playwright

plan = [
    {"action": "click", "selector": ".inventory_item_name", "index": 0}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    executor = MCPExecutor(page)
    executor.auto_login_saucedemo()  # login first

    valid, msg = executor.validate_plan(plan)
    print("Validation:", valid, msg)

    results = executor.execute_plan(plan)
    print("Execution results:", results)

    browser.close()
