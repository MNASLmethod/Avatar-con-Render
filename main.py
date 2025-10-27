import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# 1. Inicializar la aplicación FastAPI
app = FastAPI()
OPENAI_BASE_URL = "https://api.openai.com"

# 3. La única ruta que necesitamos: /v1/chat/completions
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_openai_endpoint(request: Request):
    # ... [Todo el código que reenvía la solicitud a OPENAI_BASE_URL/v1/chat/completions] ...
    pass
