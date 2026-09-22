# AI Agent Kit — Starter Pack para crear tu propio agente de IA

Un kit completo para hablar con tu agente IA:
- **Gateway** — servidor que conecta el modelo con el mundo exterior
- **WebUI** — interfaz web para interactuar por voz y texto
- **Tools** — sistema de herramientas extensible

## Instalacion rapida


# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/ai-agent-kit.git
cd ai-agent-kit

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar (editar config.json con tu API key)

# 4. Iniciar
python gateway/server.py
python webui/server.py

# 5. Abrir http://localhost:8787
```

## Multi Modelo soporta: 
- **Groq** (gratis, ultra-rapido)
- **OpenRouter** (gratis, modelos open source)
- **OpenAI** (pago, gpt-4o-mini)
- **Ollama** (local, requiere GPU)

## Licencia
MIT
