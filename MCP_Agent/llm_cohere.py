# llm_cohere.py
# Handles communication with Cohere's LLM for task planning

import cohere
import os
import json

# ✅ Safe import for errors
try:
    from cohere.errors import CohereError
except ImportError:
    CohereError = Exception  # fallback


class LLMPlanner:
    def __init__(self, api_key=None):
        """
        Initialize the Cohere client.
        The API key can be passed directly or loaded from environment variables.
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Missing Cohere API key. Set COHERE_API_KEY in your environment variables."
            )

        self.co = cohere.Client(self.api_key)

    def generate_plan(self, user_prompt: str):
        """
        Generate a structured automation plan using Cohere's LLM.
        Returns a list of dictionaries with 'action' keys.
        """
        try:
            print("🧠 Generating plan using Cohere (command-a-03-2025)...")

            # Prompt enforces strict JSON with "action"
            llm_prompt = f"""
Generate a JSON array ONLY, where each object is a step for Playwright automation.
Each object MUST have an "action" key with one of these: "goto", "click", "fill", "read_text", "wait".
Use "url" for goto, "selector" for click/fill/read_text, "value" for fill, "seconds" for wait.
Do NOT include any descriptive text or code, just pure JSON.

User request: {user_prompt}
"""
            response = self.co.chat(
                model="command-a-03-2025",
                message=llm_prompt,
                temperature=0.2
            )

            # Extract response text
            plan_text = response.text.strip() if hasattr(response, "text") else str(response)

            # Parse JSON safely
            plan_json = json.loads(plan_text)
            if not isinstance(plan_json, list):
                raise ValueError("LLM did not return a list of steps.")

            return plan_json

        except (CohereError, ValueError, json.JSONDecodeError) as e:
            print(f"❌ Cohere API / JSON parsing error: {e}")
            return [
                # fallback plan
                {"action": "goto", "url": "https://www.saucedemo.com/"},
                {"action": "wait", "seconds": 2},
                {"action": "click", "selector": "#login-button"},
            ]

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return [
                {"action": "goto", "url": "https://www.saucedemo.com/"},
                {"action": "wait", "seconds": 2},
                {"action": "click", "selector": "#login-button"},
            ]
