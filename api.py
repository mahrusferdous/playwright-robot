"""
Simple Flask wrapper that exposes /run-task 
which triggers the Playwright automation and returns JSON with status and message.
"""

from flask import Flask, request, jsonify
from main import run_task

app = Flask(__name__)

@app.route("/run-task", methods=["POST"])
def run_task_endpoint():
    try:
        # Parse JSON input (with defaults)
        data = request.get_json(force=True) or {}
        product_keyword = data.get("product_keyword", "backpack")
        headless = data.get("headless", True)

        # Run the Playwright automation
        success, message = run_task(headless=headless, product_keyword=product_keyword)

        return jsonify({"success": success, "message": message})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
