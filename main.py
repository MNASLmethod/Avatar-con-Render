import os
import requests

# === CONFIGURACIÓN ===
BEYOND_API_KEY = os.getenv("BEYOND_PRESENCE_API_KEY")

if not BEYOND_API_KEY:
    print("❌ Error: falta la clave de Beyond Presence. Asegúrate de haberla añadido en las variables de entorno.")
    exit()

# === CABECERAS ===
headers = {
    "Authorization": f"Bearer {BEYOND_API_KEY}",
    "Content-Type": "application/json"
}

# === DATOS DEL AGENTE ===
payload = {
    "name": "MNASL Tutor GPT-4o",
    "llm_api_id": "ba46f199-4f70-4729-ae6d-78adb4981890",  # <-- este es tu ID de API
    "llm_model": "gpt-4o",
    "llm_temperature": 0.7,
    "system_prompt": (
        "You are an empathetic AI Language Tutor trained in the MNASL (Methodology for the Natural Acquisition of Second Languages). "
        "Your mission is to foster natural communication by creating a motivating and emotionally safe environment. "
        "You never correct errors directly. Instead, you naturally reformulate the learner’s utterances (motherese style), "
        "providing the correct model in context. You maintain a warm, supportive tone, reduce anxiety, "
        "and encourage intrinsic motivation. Your ultimate goal is to promote natural language acquisition through meaningful feedback and interaction."
    )
}

# === PETICIÓN ===
print("🚀 Creando agente MNASL en Beyond Presence...")
response = requests.post(
    "https://api.beyondpresence.io/v1/agents",
    headers=headers,
    json=payload
)

# === RESULTADO ===
if response.status_code in [200, 201]:
    print("✅ Agente creado correctamente.")
    data = response.json()
    print("🆔 Agent ID:", data.get("id"))
    print("🌐 URL del agente:", data.get("url", "No especificada"))
else:
    print("❌ Error al crear el agente:")
    print(response.status_code, response.text)
