import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"

@app.post("/v1/chat/completions")
async def proxy_openai_endpoint(request: Request):
    try:
        body = await request.json()

        if not OPENAI_API_KEY:
            return JSONResponse(
                content={"error": "Falta la variable OPENAI_API_KEY en Render."},
                status_code=500
            )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_BASE_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=body,
            )

        # Mostrar la respuesta de OpenAI para depurar
        try:
            data = response.json()
        except Exception:
            data = {"error": "Respuesta no JSON de OpenAI", "text": response.text}

        return JSONResponse(content=data, status_code=response.status_code)

    except Exception as e:
        import traceback
        return JSONResponse(
            content={"error": str(e), "traceback": traceback.format_exc()},
            status_code=500
        )



