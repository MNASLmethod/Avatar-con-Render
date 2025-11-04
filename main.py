from flask import Flask, request, jsonify
import httpx  # <-- Cambiado a httpx (asíncrono)
import os
import asyncio

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

        # Usa httpx asíncrono con timeout
        async def call_openai():
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    OPENAI_URL,
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json=data,
                )
                response.raise_for_status()
                return response.json()

        # Ejecuta el async en sync
        result = asyncio.run(call_openai())
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e), "traceback": __import__('traceback').format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)






