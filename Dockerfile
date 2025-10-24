# 1. Base de Python
FROM python:3.11-slim

# 2. Crea y entra al directorio de trabajo
WORKDIR /app

# 3. COPIA SOLO EL ARCHIVO DE REQUERIMIENTOS e instálalos
#    Asegúrate de que este archivo exista exactamente con este nombre en tu GitHub.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia todo lo demás (main.py y Dockerfile mismo)
COPY . .

# 5. Puerto
EXPOSE 8000

# 6. Comando de inicio: NO DEBE LLEVAR .PY
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]