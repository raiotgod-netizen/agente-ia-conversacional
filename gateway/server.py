"""
AI Agent Gateway — Soporta modelos locales (Ollama) y cloud (API keys).
Providers: Ollama, OpenRouter, OpenAI, Groq, Together, etc.
"""
import json
import os
import subprocess
import sys
import time
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ══════════════════════════════════════════════════════════════
# CONFIGURACION
# ══════════════════════════════════════════════════════════════
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_CONFIG = {
    "provider": "openrouter",
    "api_key": "",
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "base_url": "https://openrouter.ai/api/v1",
    "ollama_url": "http://localhost:11434",
    "host": "127.0.0.1",
    "port": 8642,
    "max_tokens": 500,
    "temperature": 0.7,
    "system_prompt": "Eres un asistente de IA personal. Hablas en español natural, eres directo y util. Tienes acceso a herramientas del sistema.",
    "max_history": 50,
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

CONFIG = load_config()

# ══════════════════════════════════════════════════════════════
# PROVIDERS
# ══════════════════════════════════════════════════════════════
def call_ollama(messages, model, options):
    """Llama a Ollama local."""
    resp = requests.post(
        f"{CONFIG['ollama_url']}/api/chat",
        json={"model": model, "messages": messages, "stream": False, "options": options},
        timeout=120
    )
    if resp.status_code == 200:
        return resp.json().get("message", {}).get("content", "")
    raise Exception(f"Ollama error: {resp.status_code} - {resp.text[:200]}")

def call_openai_compat(messages, model, options):
    """Llama a APIs compatibles con OpenAI (OpenRouter, OpenAI, Groq, Together, etc.)."""
    headers = {"Content-Type": "application/json"}
    if CONFIG.get("api_key"):
        headers["Authorization"] = f"Bearer {CONFIG['api_key']}"
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": options.get("num_predict", 500),
        "temperature": options.get("temperature", 0.7),
    }
    
    resp = requests.post(
        f"{CONFIG['base_url']}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120
    )
    if resp.status_code == 200:
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    raise Exception(f"API error: {resp.status_code} - {resp.text[:200]}")

def call_model(messages):
    """Dispatch al provider correcto."""
    model = CONFIG["model"]
    options = {"temperature": CONFIG["temperature"], "num_predict": CONFIG["max_tokens"]}
    
    provider = CONFIG.get("provider", "ollama").lower()
    
    if provider == "ollama":
        return call_ollama(messages, model, options)
    elif provider in ("openrouter", "openai", "groq", "together", "deepseek", "anthropic"):
        return call_openai_compat(messages, model, options)
    else:
        # Intentar OpenAI compat como fallback
        return call_openai_compat(messages, model, options)

# ══════════════════════════════════════════════════════════════
# TOOLS
# ══════════════════════════════════════════════════════════════
def tool_terminal(command):
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr)[:3000]
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def tool_web_search(query):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return "\n".join([f"- {r['title']}: {r['body'][:100]}" for r in results])
    except:
        return "Instalar: pip install duckduckgo-search"

def tool_read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(5000)
    except Exception as e:
        return f"ERROR: {e}"

def tool_write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"OK: {path}"
    except Exception as e:
        return f"ERROR: {e}"

TOOLS = {
    "terminal": tool_terminal,
    "web_search": tool_web_search,
    "read_file": tool_read_file,
    "write_file": tool_write_file,
}

# ══════════════════════════════════════════════════════════════
# MEMORIA
# ══════════════════════════════════════════════════════════════
class Memory:
    def __init__(self, max_size=50):
        self.history = []
        self.max_size = max_size
        self.file = os.path.join(os.path.dirname(__file__), "memory.json")
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except:
            self.history = []
    
    def save(self):
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-self.max_size:], f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save()
    
    def get_context(self, n=20):
        return self.history[-n:]

memory = Memory()

# ══════════════════════════════════════════════════════════════
# CHAT CON TOOL CALLING
# ══════════════════════════════════════════════════════════════
def chat_with_tools(user_message):
    """Chat con tool calling automatico."""
    memory.add("user", user_message)
    
    messages = [{"role": "system", "content": CONFIG["system_prompt"]}]
    messages.extend(memory.get_context(20))
    
    for _ in range(5):
        try:
            response = call_model(messages)
        except Exception as e:
            return f"Error del modelo: {str(e)[:200]}"
        
        # Buscar tool call
        tool_call = extract_tool_call(response)
        if tool_call:
            name = tool_call["name"]
            args = tool_call["args"]
            if name in TOOLS:
                if name == "write_file":
                    result = TOOLS[name](args.get("path", ""), args.get("content", ""))
                else:
                    result = TOOLS[name](**args)
            else:
                result = f"Tool '{name}' no existe"
            
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"[TOOL RESULT] {result[:2000]}"})
        else:
            memory.add("assistant", response)
            return response
    
    return "Maximo de tool calls alcanzado"

def extract_tool_call(response):
    try:
        idx = response.find('"tool_call"')
        if idx == -1:
            return None
        start = response.rfind('{', 0, idx)
        if start == -1:
            return None
        depth = 0
        end = start
        for i in range(start, len(response)):
            if response[i] == '{': depth += 1
            elif response[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        return json.loads(response[start:end]).get("tool_call")
    except:
        return None

# ══════════════════════════════════════════════════════════════
# HTTP SERVER
# ══════════════════════════════════════════════════════════════
class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Maneja preflight CORS."""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "ok", "model": CONFIG["model"], "provider": CONFIG["provider"]})
        elif self.path == "/tools":
            self._respond(200, {"tools": list(TOOLS.keys())})
        elif self.path == "/history":
            self._respond(200, {"history": memory.get_context(50)})
        else:
            self._respond(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/chat":
            self._handle_chat()
        elif self.path == "/memory/clear":
            memory.history = []
            memory.save()
            self._respond(200, {"status": "cleared"})
        else:
            self._respond(404, {"error": "not found"})
    
    def _handle_chat(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            message = body.get("message", "")
            if not message:
                self._respond(400, {"error": "message required"})
                return
            response = chat_with_tools(message)
            self._respond(200, {"response": response})
        except Exception as e:
            self._respond(500, {"error": str(e)})
    
    def _respond(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0] if args else ''}")

def main():
    server = ThreadingHTTPServer((CONFIG["host"], CONFIG["port"]), Handler)
    print(f"AI Agent Gateway v2.0")
    print(f"Provider: {CONFIG['provider']}")
    print(f"Modelo: {CONFIG['model']}")
    print(f"URL: http://{CONFIG['host']}:{CONFIG['port']}")
    print(f"Tools: {list(TOOLS.keys())}")
    print(f"Ctrl+C para detener")
    server.serve_forever()

if __name__ == "__main__":
    main()
