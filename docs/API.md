# API Reference

## Gateway API

El Gateway expone una API REST en el puerto 8642.

### Base URL

```
http://localhost:8642
```

### Endpoints

#### GET /health

Verifica el estado del servidor y retorna informacion del modelo activo.

**Response:**

```json
{
    "status": "ok",
    "model": "qwen3:8b",
    "provider": "ollama"
}
```

**Codigos de respuesta:**

- 200: Servidor funcionando
- 500: Error interno

---

#### GET /tools

Lista todas las herramientas disponibles.

**Response:**

```json
{
    "tools": [
        "terminal",
        "web_search",
        "read_file",
        "write_file",
        "list_files",
        "search_files",
        "read_docx",
        "get_time",
        "system_info",
        "calculator",
        "clipboard",
        "weather",
        "process_list",
        "kill_process",
        "open_url",
        "network_info"
    ]
}
```

---

#### POST /chat

Envia un mensaje al agente y recibe una respuesta.

**Request:**

```json
{
    "message": "Que hora es en Chile?"
}
```

**Response exitosa:**

```json
{
    "response": "Son las 2:30 PM en Chile."
}
```

**Response con tool call:**

```json
{
    "response": "Cree el archivo hello.py con el codigo solicitado."
}
```

**Response con error:**

```json
{
    "error": "Error del modelo: timeout"
}
```

**Codigos de respuesta:**

- 200: Mensaje procesado
- 400: Mensaje no proporcionado
- 500: Error interno

**Ejemplo con curl:**

```bash
curl -X POST http://localhost:8642/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, como estas?"}'
```

**Ejemplo con Python:**

```python
import requests

response = requests.post(
    "http://localhost:8642/chat",
    json={"message": "Hola, como estas?"}
)
data = response.json()
print(data["response"])
```

---

#### GET /history

Obtiene el historial de conversacion.

**Response:**

```json
{
    "history": [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "Hola, como estas?"},
        {"role": "user", "content": "Bien, gracias"}
    ]
}
```

**Parametros query (opcionales):**

- `limit`: Numero maximo de mensajes (default: 50)

---

#### POST /memory/clear

Limpia toda la memoria de conversacion.

**Response:**

```json
{
    "status": "cleared"
}
```

---

#### GET /config

Obtiene la configuracion actual del gateway (sin API keys).

**Response:**

```json
{
    "provider": "ollama",
    "model": "qwen3:8b",
    "host": "127.0.0.1",
    "port": 8642,
    "max_tokens": 500,
    "temperature": 0.7
}
```

---

#### POST /config/update

Actualiza la configuracion del gateway.

**Request:**

```json
{
    "model": "llama3:8b",
    "temperature": 0.8,
    "max_tokens": 1000
}
```

**Response:**

```json
{
    "status": "updated",
    "config": {
        "model": "llama3:8b",
        "temperature": 0.8,
        "max_tokens": 1000
    }
}
```

---

#### GET /memory/stats

Obtiene estadisticas de la memoria.

**Response:**

```json
{
    "total_messages": 1234,
    "total_sessions": 56,
    "avg_messages_per_session": 22.0,
    "oldest_message": "2026-09-01T10:00:00",
    "newest_message": "2026-09-22T14:30:00"
}
```

---

#### POST /session/create

Crea una nueva sesion de conversacion.

**Request:**

```json
{
    "title": "Sesion de prueba"
}
```

**Response:**

```json
{
    "session_id": "20260922_143000_abc123",
    "created_at": "2026-09-22T14:30:00"
}
```

---

#### GET /session/{session_id}

Obtiene informacion de una sesion especifica.

**Response:**

```json
{
    "session_id": "20260922_143000_abc123",
    "title": "Sesion de prueba",
    "created_at": "2026-09-22T14:30:00",
    "message_count": 45,
    "active": true
}
```

---

#### DELETE /session/{session_id}

Elimina una sesion y todos sus mensajes.

**Response:**

```json
{
    "status": "deleted",
    "session_id": "20260922_143000_abc123"
}
```

---

## SQLite API

Para acceso directo a la base de datos SQLite.

### Conexion

```python
import sqlite3

db = sqlite3.connect('memory.db')
cursor = db.cursor()
```

### Tablas principales

#### messages

Almacena todos los mensajes de todas las sesiones.

```sql
-- Insertar mensaje
INSERT INTO messages (session_id, role, content, timestamp, token_count)
VALUES (?, ?, ?, ?, ?);

-- Buscar mensajes por sesion
SELECT role, content, timestamp 
FROM messages 
WHERE session_id = ? 
ORDER BY timestamp DESC 
LIMIT 50;

-- Contar mensajes
SELECT COUNT(*) FROM messages WHERE session_id = ?;

-- Buscar por contenido
SELECT role, content, timestamp 
FROM messages 
WHERE content LIKE '%palabra%' 
ORDER BY timestamp DESC;

-- Eliminar mensajes antiguos
DELETE FROM messages 
WHERE timestamp < ? 
AND session_id = ?;
```

#### sessions

Almacena metadatos de sesiones.

```sql
-- Crear sesion
INSERT INTO sessions (session_id, created_at, updated_at, model, provider, title)
VALUES (?, ?, ?, ?, ?, ?);

-- Listar sesiones activas
SELECT session_id, title, created_at, message_count
FROM sessions 
WHERE active = 1 
ORDER BY updated_at DESC;

-- Actualizar sesion
UPDATE sessions 
SET updated_at = ?, title = ? 
WHERE session_id = ?;
```

#### session_model_usage

Almacena uso de modelos por sesion.

```sql
-- Registrar uso
INSERT INTO session_model_usage (session_id, model, provider, tokens_used, cost_usd, timestamp)
VALUES (?, ?, ?, ?, ?, ?);

-- Estadisticas de uso
SELECT model, SUM(tokens_used) as total_tokens, SUM(cost_usd) as total_cost
FROM session_model_usage
GROUP BY model
ORDER BY total_tokens DESC;
```

### Ejemplo completo de uso

```python
import sqlite3
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path='memory.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializa la base de datos con las tablas necesarias."""
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        # Tabla de mensajes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                token_count INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        # Tabla de sesiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                model TEXT,
                provider TEXT,
                title TEXT,
                active INTEGER DEFAULT 1
            )
        ''')
        
        # Indices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_active ON sessions(active)')
        
        db.commit()
        db.close()
    
    def create_session(self, title=None):
        """Crea una nueva sesion."""
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        timestamp = datetime.now().timestamp()
        
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (session_id, created_at, updated_at, title)
            VALUES (?, ?, ?, ?)
        ''', (session_id, timestamp, timestamp, title))
        
        db.commit()
        db.close()
        return session_id
    
    def save_message(self, session_id, role, content):
        """Guarda un mensaje en la sesion."""
        timestamp = datetime.now().timestamp()
        token_count = len(content.split())
        
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('''
            INSERT INTO messages (session_id, role, content, timestamp, token_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, role, content, timestamp, token_count))
        
        # Actualizar timestamp de sesion
        cursor.execute('''
            UPDATE sessions SET updated_at = ? WHERE session_id = ?
        ''', (timestamp, session_id))
        
        db.commit()
        db.close()
    
    def get_history(self, session_id, limit=50):
        """Obtiene el historial de una sesion."""
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT role, content, timestamp 
            FROM messages 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        messages = cursor.fetchall()
        db.close()
        return messages
    
    def search(self, query, limit=20):
        """Busca en todos los mensajes."""
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT session_id, role, content, timestamp 
            FROM messages 
            WHERE content LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = cursor.fetchall()
        db.close()
        return results
    
    def get_stats(self):
        """Obtiene estadisticas de la memoria."""
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM sessions')
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM messages')
        oldest, newest = cursor.fetchone()
        
        db.close()
        
        return {
            'total_messages': total_messages,
            'total_sessions': total_sessions,
            'avg_messages_per_session': total_messages / total_sessions if total_sessions > 0 else 0,
            'oldest_message': datetime.fromtimestamp(oldest).isoformat() if oldest else None,
            'newest_message': datetime.fromtimestamp(newest).isoformat() if newest else None
        }
    
    def cleanup(self, days=30):
        """Elimina mensajes antiguos."""
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        
        cursor.execute('DELETE FROM messages WHERE timestamp < ?', (cutoff,))
        deleted = cursor.rowcount
        
        db.commit()
        db.close()
        
        return deleted

# Ejemplo de uso
if __name__ == '__main__':
    memory = MemoryManager()
    
    # Crear sesion
    session_id = memory.create_session(title='Sesion de prueba')
    print(f'Sesion creada: {session_id}')
    
    # Guardar mensajes
    memory.save_message(session_id, 'user', 'Hola, como estas?')
    memory.save_message(session_id, 'assistant', 'Hola! Estoy bien, gracias por preguntar.')
    
    # Obtener historial
    history = memory.get_history(session_id)
    print(f'Historial: {len(history)} mensajes')
    
    # Buscar
    results = memory.search('hola')
    print(f'Resultados de busqueda: {len(results)}')
    
    # Estadisticas
    stats = memory.get_stats()
    print(f'Estadisticas: {stats}')
```

## WebUI API

La WebUI es un cliente que consume la API del Gateway.

### Endpoints internos

La WebUI no expone API propia, pero genera requests al Gateway.

### Ejemplo de integracion

```javascript
// Enviar mensaje
async function sendMessage(message) {
    const response = await fetch('http://localhost:8642/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    });
    const data = await response.json();
    return data.response;
}

// Obtener historial
async function getHistory() {
    const response = await fetch('http://localhost:8642/history');
    const data = await response.json();
    return data.history;
}

// Verificar salud
async function checkHealth() {
    const response = await fetch('http://localhost:8642/health');
    const data = await response.json();
    return data;
}
```

## Error Handling

### Codigos de error

| Codigo | Significado |
|--------|-------------|
| 200 | Exito |
| 400 | Bad Request (parametros incorrectos) |
| 404 | Endpoint no encontrado |
| 429 | Rate limit excedido |
| 500 | Error interno del servidor |

### Formato de error

```json
{
    "error": "Mensaje descriptivo del error",
    "code": "ERROR_CODE",
    "details": {}
}
```

### Ejemplo de manejo de errores

```python
import requests

def safe_request(url, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        return {"error": "Timeout del servidor"}
    except requests.exceptions.ConnectionError:
        return {"error": "Error de conexion"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}
```

## Rate Limiting

### Implementacion basica

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests=60, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        self.requests[client_id] = [
            t for t in self.requests[client_id] 
            if now - t < self.window
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True

# Uso
limiter = RateLimiter(max_requests=60, window=60)

if not limiter.is_allowed(client_ip):
    return {"error": "Rate limit exceeded"}, 429
```

## Autenticacion

### API Key basica

```python
def verify_api_key(request):
    api_key = request.headers.get('X-API-Key')
    if api_key != EXPECTED_API_KEY:
        return {"error": "Invalid API key"}, 401
    return None
```

### Bearer token

```python
def verify_bearer(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return {"error": "Missing authorization"}, 401
    
    token = auth_header.split(' ')[1]
    if token != EXPECTED_TOKEN:
        return {"error": "Invalid token"}, 401
    
    return None
```
