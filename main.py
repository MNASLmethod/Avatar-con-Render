import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # tu clave de OpenAI
OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"

@app.post("/v1/chat/completions")
async def proxy_openai_endpoint(request: Request):
    try:
        # Obtener el cuerpo de la solicitud que viene de Beyond Presence o de curl
        body = await request.json()

        # Enviar la solicitud a la API de OpenAI
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_BASE_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=body,
            )

        # Devolver exactamente lo que responde OpenAI
        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


