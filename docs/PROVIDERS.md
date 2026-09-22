# Providers Reference

## Que es un provider?

Un provider es el servicio que provee la capacidad de inferencia de IA. Puede ser local (Ollama) o cloud (OpenRouter, Groq, etc.).

## Providers soportados

### Ollama (Local)

**Descripcion:** Corre modelos de IA directamente en tu computadora. Sin costo, sin internet, sin limites.

**Ventajas:**
- Gratis para siempre
- Sin limite de requests
- Privacidad total (datos no salen de tu PC)
- Sin necesidad de API key

**Desventajas:**
- Requiere GPU con suficiente VRAM
- Mas lento que cloud
- Modelos limitados por hardware

**Configuracion:**

```json
{
    "provider": "ollama",
    "model": "qwen3:8b",
    "ollama_url": "http://localhost:11434"
}
```

**Modelos recomendados:**

| Modelo | Tamaño | VRAM | Calidad |
|--------|--------|------|---------|
| qwen3:8b | 8B | 6GB | Buena |
| llama3:8b | 8B | 6GB | Buena |
| mistral:7b | 7B | 5GB | Buena |
| qwen3:4b | 4B | 3GB | Regular |
| phi3:mini | 3.8B | 3GB | Regular |

**Instalacion:**

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo
ollama pull qwen3:8b

# Verificar
ollama list
```

---

### Groq (Cloud ultra-rapido)

**Descripcion:** Servicio cloud con GPUs L40S. La velocidad de inferencia mas rapida del mundo.

**Ventajas:**
- Velocidad extrema (hasta 500 tokens/seg)
- Tier gratis generoso
- Sin setup de GPU local

**Desventajas:**
- Requiere API key
- Tier gratis tiene rate limits
- Modelos limitados

**Configuracion:**

```json
{
    "provider": "groq",
    "api_key": "gsk_tu-api-key-aqui",
    "model": "llama-3.1-8b-instant",
    "base_url": "https://api.groq.com/openai/v1"
}
```

**Modelos disponibles (gratis):**

| Modelo | Velocidad | Contexto |
|--------|-----------|----------|
| llama-3.1-8b-instant | ~500 tok/s | 8K |
| llama-3.1-70b-versatile | ~200 tok/s | 8K |
| mixtral-8x7b-32768 | ~300 tok/s | 32K |
| gemma2-9b-it | ~400 tok/s | 8K |

**Obtener API key:**

1. Ve a https://console.groq.com
2. Crea una cuenta gratis
3. Ve a API Keys
4. Crea una nueva key
5. Copia la key (empieza con gsk_)

**Limites del tier gratis:**

- 30 requests/minuto
- 14,400 requests/dia
- 100,000 tokens/minuto

---

### OpenRouter (Cloud con 200+ modelos)

**Descripcion:** Proxy que da acceso a mas de 200 modelos de diferentes providers. Muchos son gratis.

**Ventajas:**
- Acceso a muchos modelos
- Varios modelos gratis
- Sin compromiso a un solo provider
- Rate limits generosos

**Desventajas:**
- Velocidad variable segun el modelo
- Algunos modelos son de pago
- Latencia adicional por ser proxy

**Configuracion:**

```json
{
    "provider": "openrouter",
    "api_key": "sk-or-v1-tu-api-key-aqui",
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "base_url": "https://openrouter.ai/api/v1"
}
```

**Modelos gratis populares:**

| Modelo | Velocidad | Calidad |
|--------|-----------|---------|
| meta-llama/llama-3.1-8b-instruct:free | Rapida | Buena |
| google/gemma-2-9b-it:free | Rapida | Buena |
| mistralai/mistral-7b-instruct:free | Rapida | Buena |
| qwen/qwen-2.5-7b-instruct:free | Rapida | Buena |
| nvidia/llama-3.1-nemotron-70b-instruct:free | Lenta | Excelente |

**Obtener API key:**

1. Ve a https://openrouter.ai
2. Crea una cuenta
3. Ve a Keys
4. Crea una nueva key
5. Copia la key (empieza con sk-or-v1-)

---

### OpenAI (Cloud premium)

**Descripcion:** Los modelos GPT de OpenAI. La calidad mas alta del mercado.

**Ventajas:**
- Calidad excepcional
- Funciones avanzadas (vision, function calling)
- Documentacion excelente
- Amplio soporte

**Desventajas:**
- De pago
- Mas caro que alternativas
- Requiere tarjeta de credito

**Configuracion:**

```json
{
    "provider": "openai",
    "api_key": "sk-tu-api-key-aqui",
    "model": "gpt-4o-mini",
    "base_url": "https://api.openai.com/v1"
}
```

**Modelos disponibles:**

| Modelo | Costo | Contexto | Calidad |
|--------|-------|----------|---------|
| gpt-4o-mini | $0.15/1M | 128K | Muy buena |
| gpt-4o | $2.50/1M | 128K | Excelente |
| gpt-3.5-turbo | $0.50/1M | 16K | Buena |

**Obtener API key:**

1. Ve a https://platform.openai.com
2. Crea una cuenta
3. Agrega metodo de pago
4. Ve a API Keys
5. Crea una nueva key

---

### DeepSeek (Cloud economico)

**Descripcion:** Modelos chinos de alta calidad a precios muy bajos.

**Ventajas:**
- Muy economico
- Buena calidad
- Modelos de codigo excelente
- Sin|minimo registro

**Desventajas:**
- Servidor en China
- Latencia variable
- Menos documentacion

**Configuracion:**

```json
{
    "provider": "deepseek",
    "api_key": "sk-tu-api-key-aqui",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
}
```

**Modelos disponibles:**

| Modelo | Costo | Contexto | Calidad |
|--------|-------|----------|---------|
| deepseek-chat | $0.27/1M | 64K | Muy buena |
| deepseek-coder | $0.27/1M | 64K | Excelente para codigo |

**Obtener API key:**

1. Ve a https://platform.deepseek.com
2. Crea una cuenta
3. Recarga saldo (minimo $5)
4. Ve a API Keys
5. Crea una nueva key

---

### Together (Cloud con creditos gratis)

**Descripcion:** Plataforma cloud para modelos open source. Ofrece creditos gratis al registrarse.

**Ventajas:**
- Creditos gratis al registrarse
- Modelos open source de alta calidad
- Buena infraestructura

**Desventajas:**
- Creditos se agotan
- Velocidad variable

**Configuracion:**

```json
{
    "provider": "together",
    "api_key": "tu-api-key-aqui",
    "model": "meta-llama/Llama-3-8b-chat-hf",
    "base_url": "https://api.together.xyz/v1"
}
```

**Obtener API key:**

1. Ve a https://api.together.xyz
2. Crea una cuenta
3. Recibe $25 de creditos gratis
4. Ve a Settings > API Keys
5. Crea una nueva key

---

### Anthropic (Cloud premium)

**Descripcion:** Los modelos Claude. Excelente razonamiento y seguridad.

**Ventajas:**
- Razonamiento excepcional
- Seguridad robusta
- Contexto largo (200K)
- Buena Instruction following

**Desventajas:**
- Caro
- Requiere API key
- Sin tier gratis

**Configuracion:**

```json
{
    "provider": "anthropic",
    "api_key": "sk-ant-tu-api-key-aqui",
    "model": "claude-3-haiku-20240307",
    "base_url": "https://api.anthropic.com/v1"
}
```

**Modelos disponibles:**

| Modelo | Costo | Contexto | Calidad |
|--------|-------|----------|---------|
| claude-3-haiku | $0.25/1M | 200K | Buena |
| claude-3-sonnet | $3.00/1M | 200K | Muy buena |
| claude-3-opus | $15.00/1M | 200K | Excelente |

---

## Comparativa de providers

### Velocidad

1. **Groq** (~500 tok/s) - El mas rapido
2. **OpenAI** (~100 tok/s) - Rapido
3. **DeepSeek** (~80 tok/s) - Normal
4. **OpenRouter** (~50-200 tok/s) - Variable
5. **Ollama** (~20-50 tok/s) - Depende del hardware

### Costo

1. **Ollama** (gratis) - Sin costo
2. **Groq** (gratis tier) - Generoso
3. **OpenRouter** (gratis tier) - Varios modelos gratis
4. **DeepSeek** ($0.27/1M) - Muy barato
5. **OpenAI** ($0.15-2.50/1M) - Moderado a caro
6. **Anthropic** ($0.25-15/1M) - Caro

### Calidad

1. **Anthropic Claude-3-opus** - La mejor
2. **OpenAI GPT-4o** - Excelente
3. **DeepSeek-chat** - Muy buena
4. **Groq llama-3.1-70b** - Muy buena
5. **OpenRouter modelos** - Variable

### Facilidad de uso

1. **Ollama** - Instalar y usar
2. **Groq** - API key y listo
3. **OpenRouter** - API key y listo
4. **DeepSeek** - API key y listo
5. **OpenAI** - Requiere tarjeta
6. **Anthropic** - Requiere tarjeta

## Recomendaciones

### Para practicar (gratis)

**Opcion 1: Ollama local**
- Mejor para aprender
- Sin costo
- Sin limite de requests
- Requiere GPU

**Opcion 2: Groq gratis**
- Sin GPU necesaria
- Ultra-rapido
- Tier generoso
- Solo necesitas internet

### Para produccion

**Opcion 1: DeepSeek**
- Calidad excelente
- Muy economico
- Buen para alto volumen

**Opcion 2: OpenAI GPT-4o-mini**
- Calidad muy buena
- Precio moderado
- Amplio soporte

### Para proyectos criticos

**Opcion 1: OpenAI GPT-4o**
- La mejor calidad disponible
- Funciones avanzadas
- Documentacion completa

**Opcion 2: Anthropic Claude-3**
- Excelente razonamiento
- Contexto muy largo
- Seguridad robusta

## Cambiar de provider

### Via config.json

1. Abre `gateway/config.json`
2. Cambia el campo `provider`
3. Actualiza `api_key`, `model` y `base_url`
4. Reinicia el gateway

### Via codigo

```python
# Cambiar provider en runtime
config["provider"] = "groq"
config["api_key"] = "gsk_tu-key"
config["model"] = "llama-3.1-8b-instant"
config["base_url"] = "https://api.groq.com/openai/v1"
```

### Via variables de entorno

```bash
# Linux/Mac
export AI_PROVIDER=groq
export AI_API_KEY=gsk_tu-key
export AI_MODEL=llama-3.1-8b-instant

# Windows
set AI_PROVIDER=groq
set AI_API_KEY=gsk_tu-key
set AI_MODEL=llama-3.1-8b-instant
```

## Troubleshooting

### "API key invalida"

1. Verifica que la key sea correcta (sin espacios)
2. Asegurate de que empiece con el prefijo correcto (sk-, gsk-, sk-or-v1-, etc.)
3. Verifica que no haya expirado
4. Revisa que tengas credito/saldo

### "Modelo no encontrado"

1. Verifica que el nombre del modelo sea exacto
2. Algunos modelos requieren registro previo
3. Revisa la documentacion del provider

### "Rate limit exceeded"

1. Espera 1 minuto y vuelve a intentar
2. Reduce la frecuencia de requests
3. Considera upgradear tu tier
4. Usa un provider diferente

### "Timeout"

1. El modelo puede estar sobrecargado
2. Intenta con un modelo mas pequeno
3. Verifica tu conexion a internet
4. Aumenta el timeout en config

### "Modelo lento"

1. Usa un provider mas rapido (Groq)
2. Usa un modelo mas pequeno
3. Reduce max_tokens
4. Verifica tu conexion a internet
