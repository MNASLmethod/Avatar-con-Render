import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

# Configuración base
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com"

if not OPENAI_API_KEY:
    raise ValueError("❌ Falta la variable de entorno OPENAI_API_KEY")

# Ruta principal: proxy a /v1/chat/completions
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_openai_endpoint(request: Request):
    # Tomar el cuerpo y los encabezados de la petición original
    body = await request.body()
    headers = dict(request.headers)
    headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

    # Quitar encabezados problemáticos (evita errores CORS)
    headers.pop("host", None)
    headers.pop("content-length", None)

    # Construir URL destino
    target_url = f"{OPENAI_BASE_URL}{request.url.path}"

    # Reenviar la solicitud a OpenAI
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body
        )

    # Si la respuesta es streaming (por ejemplo, cuando Beyond Presence lo pide)
    if response.headers.get("content-type", "").startswith("text/event-stream"):
        return StreamingResponse(
            response.aiter_raw(),
            media_type="text/event-stream"
        )

    # Devolver respuesta normal
    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )


@app.get("/")
async def root():
    return {"status": "✅ MNASL Agent running on Render"}
