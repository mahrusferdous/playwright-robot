# main.py
# Entry point for the MCP Agent — generates a test plan using Cohere and executes it using Playwright.

from playwright.sync_api import sync_playwright
from mcp_agent import MCPExecutor
from llm_cohere import LLMPlanner

def main():
    # 🧠 Initialize LLM Planner (Cohere)
    planner = LLMPlanner(api_key="YOUR_VALID_COHERE_API_KEY_HERE")

    # 🧩 User prompt for the LLM
    user_prompt = "Login to saucedemo.com and read the name of the first product."

    # 🔮 Generate automation plan
    plan = planner.generate_plan(user_prompt)
    print("\n=== 🧠 Generated Plan ===")
    print(plan)

    # 🧪 Execute plan using Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        executor = MCPExecutor(page)

        print("\n=== ⚙️ Validating Plan ===")
        valid, msg = executor.validate_plan(plan)
        if not valid:
            print(f"❌ Invalid plan: {msg}")
            browser.close()
            return

        print("✅ Plan valid — executing...")
        results = executor.execute_plan(plan)
        print("\n=== 📊 Execution Results ===")
        print(results)

        browser.close()

if __name__ == "__main__":
    main()
