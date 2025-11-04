from flask import Flask, request, jsonify
import httpx
import os
import asyncio
import logging

# Configuración básica
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    app.logger.error("OPENAI_API_KEY no configurada")
    raise RuntimeError("OPENAI_API_KEY no encontrada")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/v1/chat/completions", methods=["POST"])
async def chat_completions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido o vacío"}), 400

        model = data.get("model", "gpt-4o-mini")
        messages = data.get("messages", [])
        if not messages:
            return jsonify({"error": "Falta campo 'messages'"}), 400

        # Llamada asíncrona a OpenAI
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENAI_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": model, "messages": messages},
            )

        # Manejo de errores de OpenAI
        if response.status_code != 200:
            error_text = response.text
            app.logger.error(f"OpenAI error {response.status_code}: {error_text}")
            return jsonify({"error": "OpenAI API error", "response_text": error_text}), response.status_code

        return jsonify(response.json())

    except Exception as e:
        app.logger.error(f"Error interno: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Para Gunicorn
def create_app():
    return app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
