import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

# URL base de OpenAI
OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/v1/chat/completions")
async def proxy_openai_endpoint(request: Request):
    try:
        if not OPENAI_API_KEY:
            return JSONResponse({"error": "Missing OpenAI API key"}, status_code=500)

        body = await request.json()

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OPENAI_BASE_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=body,
            )

        # Devolver directamente la respuesta de OpenAI
        return JSONResponse(response.json(), status_code=response.status_code)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

