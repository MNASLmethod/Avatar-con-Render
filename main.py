import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# 1. Inicializar la aplicación FastAPI
app = FastAPI()

# 2. Configuración para el reenvío (Cambia la URL por la real de OpenAI)
OPENAI_BASE_URL = "https://api.openai.com"

# 3. La única ruta que necesitamos: /v1/chat/completions (el endpoint de chat)
@app.api_route("/v1/chat/completions", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_openai_endpoint(request: Request):
    
    # 3.1. Leer el método y la ruta
    method = request.method
    path = request.url.path
    
    # 3.2. Obtener el cuerpo de la solicitud si existe
    try:
        data = await request.json()
    except:
        data = None

    # 3.3. Crear la URL final hacia OpenAI
    url = f"{OPENAI_BASE_URL}{path}"
    
    # 3.4. Obtener las cabeceras (headers)
    # Incluimos solo las cabeceras relevantes (Authorization, Content-Type, etc.)
    headers = {
        key: value for key, value in request.headers.items() 
        if key.lower() in ["authorization", "content-type"]
    }

    # 3.5. Enviar la solicitud a OpenAI usando httpx (un cliente HTTP asíncrono)
    async with httpx.AsyncClient() as client:
        
        # 3.6. Ejecutar la solicitud (POST, GET, etc.)
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            # Importante: Desactivar seguimiento de redirecciones para Streaming
            follow_redirects=False, 
            # Timeout (tiempo de espera) alto para que el LLM tenga tiempo de responder
            timeout=300.0 
        )

        # 3.7. Si la respuesta es Streaming (típico de Beyond Presence), devolvemos el stream.
        if "text/event-stream" in response.headers.get("content-type", ""):
            # Función generadora para transmitir la respuesta línea por línea
            async def generate():
                async for chunk in response.aiter_bytes():
                    yield chunk
            
            # Devolver la respuesta en streaming
            return StreamingResponse(
                generate(), 
                status_code=response.status_code, 
                headers=response.headers
            )
        
        # 3.8. Si no es Streaming, devolvemos la respuesta JSON normal.
        return response