# Arquitectura del AI Agent Kit

## Visión general

El AI Agent Kit sigue una arquitectura de tres capas separadas por responsabilidades:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   WebUI     │────>│   Gateway   │────>│   Modelo    │
│  (Puerto    │     │  (Puerto    │     │  (Ollama/   │
│   8787)     │     │   8642)     │     │   Cloud)    │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │   Tools     │
                    │  (16+)     │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │  Memoria    │
                    │  SQLite/    │
                    │  JSON       │
                    └─────────────┘
```

## Capas

### 1. WebUI (Frontend)

- **Archivo**: `webui/server.py` + `webui/static/index.html`
- **Puerto**: 8787
- **Responsabilidad**: Interfaz de usuario, STT (speech-to-text), TTS (text-to-speech)
- **Comunicacion**: HTTP REST con el Gateway

### 2. Gateway (Backend)

- **Archivo**: `gateway/server.py`
- **Puerto**: 8642
- **Responsabilidad**: Orquestacion de modelos, ejecucion de tools, gestion de memoria
- **Comunicacion**: HTTP REST con WebUI, HTTP con modelos

### 3. Modelo (IA)

- **Opciones**: Ollama local, OpenRouter, Groq, OpenAI, DeepSeek
- **Responsabilidad**: Inferencia, generacion de respuestas, tool calling

## Memoria persistente

El sistema maneja dos tipos de memoria:

### Memoria simple (JSON)

Archivo: `gateway/memory.json`

```json
[
  {"role": "user", "content": "Hola"},
  {"role": "assistant", "content": "Hola, como estas?"},
  {"role": "user", "content": "Bien, y tu?"},
  {"role": "assistant", "content": "Perfecto, en que te puedo ayudar?"}
]
```

- Guarda las ultimas N conversaciones (configurable via `max_history`)
- Se carga automaticamente al iniciar el Gateway
- Se persiste en disco despues de cada interaccion

### Memoria SQLite (Avanzada)

Para aplicaciones que requieren historial escalable y busqueda:

**Esquema de la tabla messages:**

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,           -- 'user', 'assistant', 'system', 'tool'
    content TEXT NOT NULL,
    tool_call_id TEXT,
    tool_calls TEXT,
    tool_name TEXT,
    timestamp REAL NOT NULL,
    token_count INTEGER,
    finish_reason TEXT,
    reasoning TEXT,
    reasoning_content TEXT,
    reasoning_details TEXT,
    codex_reasoning_items TEXT,
    codex_message_items TEXT,
    platform_message_id TEXT,
    observed INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1,
    compacted INTEGER DEFAULT 0,
    effect_disposition TEXT,
    api_content TEXT,
    display_kind TEXT,
    display_metadata TEXT,
    _compressed_summary INTEGER DEFAULT 0
);
```

**Indice para busquedas rapidas:**

```sql
CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

**Ejemplo de insercion:**

```python
import sqlite3
from datetime import datetime

def save_message(session_id, role, content, tool_name=None):
    db = sqlite3.connect('memory.db')
    cursor = db.cursor()
    timestamp = datetime.now().timestamp()
    
    cursor.execute("""
        INSERT INTO messages (session_id, role, content, timestamp, tool_name, token_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, role, content, timestamp, tool_name, len(content.split())))
    
    db.commit()
    db.close()
```

**Ejemplo de busqueda:**

```python
def get_conversation_history(session_id, limit=50):
    db = sqlite3.connect('memory.db')
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT role, content, timestamp 
        FROM messages 
        WHERE session_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (session_id, limit))
    
    messages = cursor.fetchall()
    db.close()
    return messages
```

**Ventajas de SQLite sobre JSON:**

- Maneja millones de mensajes sin problemas
- Permite busquedas por session_id, timestamp, role
- Soporta concurrent access
- Permite compactacion de conversaciones largas
- Facil export/import de datos

### Esquema completo de sesiones

```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    model TEXT,
    provider TEXT,
    title TEXT,
    active INTEGER DEFAULT 1
);
```

### Tabla de uso de modelos

```sql
CREATE TABLE session_model_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    model TEXT NOT NULL,
    provider TEXT,
    tokens_used INTEGER,
    cost_usd REAL,
    timestamp REAL NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

## Tools (Herramientas)

Cada tool es una funcion Python que recibe parametros y retorna un string:

```python
TOOLS = {
    "tool_name": tool_function,
    "otra_tool": otra_function,
}

def tool_function(param1, param2):
    """Descripcion de la tool."""
    # Logica de la tool
    return "resultado como string"
```

### Flujo de ejecucion de tools

```
1. Usuario envia mensaje
2. Gateway envia mensaje + tools disponibles al modelo
3. Modelo responde con tool_call (JSON)
4. Gateway extrae tool_call del response
5. Gateway ejecuta la tool
6. Gateway envia resultado de vuelta al modelo
7. Modelo genera respuesta final
8. Gateway retorna respuesta al usuario
```

### Ejemplo de tool call

```python
# Modelo responde:
{
    "tool_call": {
        "name": "terminal",
        "args": {
            "command": "ls -la"
        }
    }
}

# Gateway ejecuta:
result = tool_terminal("ls -la")

# Resultado:
"total 48
drwxr-xr-x 5 user user 4096 Sep 22 14:30 .
drwxr-xr-x 3 user user 4096 Sep 22 14:00 ..
..."
```

## Providers

### Ollama (Local)

```python
def call_ollama(messages, model, options):
    resp = requests.post(
        f"{ollama_url}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options
        },
        timeout=120
    )
    return resp.json()["message"]["content"]
```

### OpenAI Compatible (Cloud)

```python
def call_openai_compat(messages, model, options):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": options["num_predict"],
        "temperature": options["temperature"]
    }
    resp = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120
    )
    return resp.json()["choices"][0]["message"]["content"]
```

## Endpoints del Gateway

### GET /health

Retorna estado del servidor y modelo activo.

```json
{
    "status": "ok",
    "model": "qwen3:8b",
    "provider": "ollama"
}
```

### GET /tools

Lista de herramientas disponibles.

```json
{
    "tools": ["terminal", "web_search", "read_file", "write_file", ...]
}
```

### POST /chat

Enviar mensaje y recibir respuesta.

**Request:**
```json
{
    "message": "Que hora es?"
}
```

**Response:**
```json
{
    "response": "Son las 2:30 PM en Chile."
}
```

### GET /history

Obtener historial de conversacion.

```json
{
    "history": [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "Hola, como estas?"}
    ]
}
```

### POST /memory/clear

Limpiar memoria de conversacion.

```json
{
    "status": "cleared"
}
```

## Flujo completo de una interaccion

```
1. Usuario escribe "Que tiempo hace en Santiago?"
2. WebUI envia POST /chat con el mensaje
3. Gateway recibe el mensaje
4. Gateway agrega mensaje a memoria
5. Gateway construye contexto:
   - System prompt
   - Historial reciente (20 ultimos mensajes)
   - Mensaje actual del usuario
6. Gateway envia contexto al modelo
7. Modelo responde con tool_call:
   {"tool_call": {"name": "weather", "args": {"city": "Santiago"}}}
8. Gateway ejecuta tool_weather("Santiago")
9. Gateway agrega resultado al contexto
10. Gateway envia contexto actualizado al modelo
11. Modelo genera respuesta final:
    "En Santiago esta nublado con 18 grados."
12. Gateway guarda respuesta en memoria
13. Gateway retorna respuesta al WebUI
14. WebUI muestra respuesta y ejecuta TTS
```

## Seguridad

### Rate Limiting

Implementar rate limiting por IP:

```python
from collections import defaultdict
import time

rate_limit = defaultdict(list)

def check_rate_limit(ip, max_requests=60, window=60):
    now = time.time()
    rate_limit[ip] = [t for t in rate_limit[ip] if now - t < window]
    if len(rate_limit[ip]) >= max_requests:
        return False
    rate_limit[ip].append(now)
    return True
```

### Sanitizacion de inputs

```python
import re

def sanitize_input(text):
    # Remover caracteres peligrosos
    text = re.sub(r'[<>"\']', '', text)
    # Limitar longitud
    return text[:1000]
```

### Proteccion de archivos

```python
ALLOWED_PATHS = ['/tmp', '/home/user/documents']
BLOCKED_PATTERNS = ['..', '~', '/etc', '/proc']

def is_safe_path(path):
    for pattern in BLOCKED_PATTERNS:
        if pattern in path:
            return False
    return any(path.startswith(p) for p in ALLOWED_PATHS)
```

## Rendimiento

### Caching de respuestas

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_weather(city):
    return fetch_weather(city)
```

### Connection pooling

```python
import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=10
)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### Async processing

```python
import asyncio
import aiohttp

async def async_chat(message):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{gateway_url}/chat', json={'message': message}) as resp:
            return await resp.json()
```

## Escalabilidad

### Multi-Gateway

```python
GATEWAYS = [
    {"host": "127.0.0.1", "port": 8642},
    {"host": "127.0.0.1", "port": 8643},
    {"host": "127.0.0.1", "port": 8644},
]

def get_available_gateway():
    for gw in GATEWAYS:
        if check_health(gw):
            return gw
    return None
```

### Load Balancing

```python
import random

def balance_request(message):
    gw = get_available_gateway()
    if gw:
        return forward_request(gw, message)
    return {"error": "No gateways available"}
```

## Monitoring

### Metrics Endpoint

```python
@app.route('/metrics')
def metrics():
    return {
        "total_requests": total_requests,
        "active_sessions": active_sessions,
        "avg_response_time": avg_response_time,
        "error_rate": error_rate,
        "model_usage": model_usage_stats
    }
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gateway.log'),
        logging.StreamHandler()
    ]
)
```
