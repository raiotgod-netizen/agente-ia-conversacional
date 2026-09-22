FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cachear dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente
COPY gateway/ gateway/
COPY webui/ webui/

# Crear directorio de datos
RUN mkdir -p /app/data

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_URL=http://host.docker.internal:11434

# Puertos
EXPOSE 8642 8787

# Comando por defecto: iniciar gateway y webui
CMD ["sh", "-c", "python gateway/server.py & python webui/server.py"]
