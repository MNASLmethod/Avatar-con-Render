from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    try:
        if not OPENAI_API_KEY:
            return jsonify({"error": "Missing OPENAI_API_KEY"}), 500

        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        # Llama directamente al endpoint de OpenAI
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(OPENAI_URL, headers=headers, json=data)

        if response.status_code != 200:
            return jsonify({
                "error": "OpenAI API error",
                "status_code": response.status_code,
                "response_text": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500








