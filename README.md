# AI Agent Kit — Starter Pack para crear tu propio agente de IA

> Creado por Diego Hernandez | Puerto Montt, Chile | 2026

Un kit completo para crear un agente de IA personal con capacidades similares a J.A.R.V.I.S (Iron Man). Incluye gateway multi-provider, webui con voz, tools extensibles y memoria persistente.

## Que es esto?

Un AI Agent Kit completo que incluye:

- **Gateway** -- Servidor que conecta modelos de IA (locales y cloud) con herramientas del sistema
- **WebUI** -- Interfaz web moderna con soporte de voz (STT/TTS)
- **Tools** -- Sistema de 16 herramientas extensibles
- **Memoria** -- Persistencia de conversaciones y aprendizaje
- **Multi-Provider** -- Soporta Ollama, OpenRouter, Groq, OpenAI, DeepSeek

## Instalacion rapida

### Requisitos

- Python 3.10 o superior
- Opcional: Ollama (para modelos locales)
- Opcional: API key de OpenRouter/Groq (para modelos cloud gratuitos)

### Instalacion automatica

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/ai-agent-kit.git
cd ai-agent-kit

# 2. Ejecutar instalador
python scripts/setup.py

# 3. Configurar (el instalador te guia)
#    - Elige provider (Ollama local o cloud)
#    - Ingresa API key si usas cloud
#    - Selecciona modelo

# 4. Iniciar
python gateway/server.py    # Terminal 1: Gateway
python webui/server.py      # Terminal 2: WebUI

# 5. Abrir http://localhost:8787
```

### Instalacion manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar (editar manualmente)
cp gateway/config.example.json gateway/config.json
# Editar config.json con tu configuracion

# Iniciar
python gateway/server.py
python webui/server.py
```

## Estructura del proyecto

```
ai-agent-kit/
├── gateway/
│   ├── server.py          # Servidor principal del gateway
│   ├── config.json        # Configuracion del gateway
│   └── memory.json        # Memoria persistente (auto-generado)
├── webui/
│   ├── server.py          # Servidor web
│   └── static/
│       └── index.html     # Interfaz web
├── scripts/
│   ├── setup.py           # Instalador automatico
│   └── examples/          # Scripts de ejemplo
├── tests/
│   ├── test_gateway.py    # Tests del gateway
│   └── test_tools.py      # Tests de herramientas
├── docs/
│   ├── ARCHITECTURE.md    # Arquitectura del sistema
│   ├── API.md             # Documentacion de la API
│   ├── TOOLS.md           # Lista de herramientas
│   └── PROVIDERS.md       # Providers soportados
├── docker/
│   ├── Dockerfile         # Container del gateway
│   └── docker-compose.yml # Deployment completo
├── requirements.txt       # Dependencias de Python
├── .gitignore             # Archivos ignorados por git
└── README.md              # Este archivo
```

## Providers soportados

### Gratuitos (sin costo)

| Provider | Velocidad | Modelos | API Key |
|----------|-----------|---------|---------|
| **Ollama** | Local | qwen3, llama3, mistral | No requiere |
| **Groq** | Ultra-rapido | llama-3.1-8b, mixtral | Requiere (gratis) |
| **OpenRouter** | Rapido | 200+ modelos | Requiere (gratis) |
| **Together** | Rapido | Llama, Mistral | Requiere (creditos gratis) |

### De pago

| Provider | Velocidad | Modelos | Costo |
|----------|-----------|---------|-------|
| **OpenAI** | Rapido | gpt-4o-mini, gpt-4o | ~$0.15/1M tokens |
| **DeepSeek** | Rapido | deepseek-chat | ~$0.27/1M tokens |
| **Anthropic** | Rapido | claude-3-haiku | ~$0.25/1M tokens |

### Configuracion por provider

#### Ollama (Local - Recomendado para practicar)

```json
{
  "provider": "ollama",
  "model": "qwen3:8b",
  "ollama_url": "http://localhost:11434"
}
```

#### OpenRouter (Cloud gratis)

```json
{
  "provider": "openrouter",
  "api_key": "sk-or-v1-tu-api-key",
  "model": "meta-llama/llama-3.1-8b-instruct:free",
  "base_url": "https://openrouter.ai/api/v1"
}
```

#### Groq (Cloud ultra-rapido)

```json
{
  "provider": "groq",
  "api_key": "gsk_tu-api-key",
  "model": "llama-3.1-8b-instant",
  "base_url": "https://api.groq.com/openai/v1"
}
```

## Tools (Herramientas)

El agente tiene acceso a 16 herramientas del sistema:

### Herramientas de terminal

- **terminal** -- Ejecutar comandos del sistema operativo
- **process_list** -- Listar procesos en ejecucion
- **kill_process** -- Matar un proceso por nombre

### Herramientas de archivos

- **read_file** -- Leer archivos de texto
- **write_file** -- Crear o modificar archivos
- **list_files** -- Listar archivos en un directorio
- **search_files** -- Buscar archivos por nombre
- **read_docx** -- Leer archivos Word (.docx)

### Herramientas de internet

- **web_search** -- Buscar en internet
- **open_url** -- Abrir URL en navegador
- **weather** -- Consultar clima

### Herramientas del sistema

- **get_time** -- Obtener fecha y hora
- **system_info** -- Informacion del sistema
- **calculator** -- Calculadora
- **clipboard** -- Obtener/modificar portapapeles
- **network_info** -- Informacion de red

### Ejemplo de uso

```
Usuario: "Que hora es en Chile?"
Agente: [get_time] 2026-09-22 14:30:00
        Son las 2:30 PM en Chile.

Usuario: "Crea un archivo hello.py con un print"
Agente: [write_file] hello.py
        Archivo creado.

Usuario: "Ejecuta hello.py"
Agente: [terminal] python hello.py
        Hello World!
```

## WebUI

La interfaz web incluye:

- **Chat de texto** -- Mensajes en tiempo real
- **Voz (STT)** -- Hablar al agente con el microfono
- **TTS** -- El agente responde por voz
- **Panel de tools** -- Ver herramientas en uso
- **Diseno Iron Man** -- Estilo futurista con colores naranja/azul

### Atajos de teclado

- **Enter** -- Enviar mensaje
- **Escape** -- Detener reproduccion de voz
- **Ctrl+L** -- Limpiar chat

## Tests

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar tests especificos
python -m pytest tests/test_gateway.py -v
python -m pytest tests/test_tools.py -v

# Con cobertura
python -m pytest tests/ --cov=gateway --cov=webui
```

## Docker

### Ejecutar con Docker

```bash
# Build y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Dockerfile standalone

```bash
# Build imagen
docker build -t ai-agent-kit -f docker/Dockerfile .

# Ejecutar
docker run -p 8642:8642 -p 8787:8787 ai-agent-kit
```

## Documentacion

- **[Arquitectura](docs/ARCHITECTURE.md)** -- Como funciona el sistema
- **[API](docs/API.md)** -- Endpoints del gateway
- **[Tools](docs/TOOLS.md)** -- Lista completa de herramientas
- **[Providers](docs/PROVIDERS.md)** -- Guia de providers
- **[Despliegue](docs/DEPLOYMENT.md)** -- Opciones de deployment

## Personalizacion

### Agregar una tool nueva

```python
# En gateway/server.py, agregar al diccionario TOOLS:
def tool_mi_nueva_tool(param1, param2):
    """Descripcion de la tool."""
    # Tu logica aqui
    return "resultado"

TOOLS["mi_nueva_tool"] = tool_mi_nueva_tool
```

### Cambiar el system prompt

```json
// En gateway/config.json
{
  "system_prompt": "Eres un experto en programacion. Ayudas a los usuarios con codigo. Hablas en español."
}
```

### Agregar memoria persistente

```python
# La memoria se guarda automaticamente en gateway/memory.json
# Puede ser leida y modificada directamente
```

## Solucion de problemas

### "Ollama no encontrado"

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar un modelo
ollama pull qwen3:8b
```

### "API key invalida"

1. Verifica que la API key sea correcta
2. Asegurate de tener credito (si es provider de pago)
3. Revisa los rate limits del provider

### "Puerto 8642 en uso"

```bash
# En Linux/Mac
lsof -i :8642
kill -9 <PID>

# En Windows
netstat -ano | findstr :8642
taskkill /PID <PID> /F
```

### "WebUI no carga"

1. Verifica que el gateway este corriendo
2. Revisa que el puerto 8787 este libre
3. Abre la consola del navegador (F12) para ver errores

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Haz commit (`git commit -am 'Agregar nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

## Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## Creditos

- **Diego Hernandez** -- Creador original
- **Ollama** -- Modelos locales
- **OpenRouter** -- Acceso a multiples modelos
- **Groq** -- Inferencia ultra-rapida

---

Hecho con dedicacion en Puerto Montt, Chile
