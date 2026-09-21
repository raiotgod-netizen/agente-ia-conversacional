"""
AI Agent Kit — Script de instalacion automatica.
Ejecutar: python scripts/setup.py
"""
import subprocess
import sys
import os
import json

def run(cmd, desc):
    print(f"  {desc}...", end=" ")
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            print("OK")
            return True
        else:
            print(f"ERROR: {r.stderr[:100]}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("="*50)
    print("  AI Agent Kit — Instalacion")
    print("="*50)
    
    # 1. Verificar Python
    print("\n[1/4] Verificando Python...")
    run(f"{sys.executable} --version", "Python")
    
    # 2. Instalar dependencias
    print("\n[2/4] Instalando dependencias...")
    req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
    run(f"{sys.executable} -m pip install -r {req_file}", "pip install")
    
    # 3. Verificar Ollama
    print("\n[3/4] Verificando Ollama...")
    if run("ollama --version", "Ollama"):
        # Verificar si hay modelos
        r = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        if "qwen" not in r.stdout.lower():
            print("  Descargando modelo qwen3:8b...")
            run("ollama pull qwen3:8b", "Descargando modelo")
        else:
            print("  Modelos ya instalados")
    else:
        print("  Ollama no encontrado. Instalar desde https://ollama.com")
    
    # 4. Verificar config
    print("\n[4/4] Verificando configuracion...")
    config_file = os.path.join(os.path.dirname(__file__), "..", "gateway", "config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"  Modelo: {config.get('model', 'no definido')}")
        print(f"  Gateway: {config.get('host')}:{config.get('port')}")
    else:
        print("  Archivo de configuracion no encontrado")
    
    print("\n" + "="*50)
    print("  Instalacion completada!")
    print("")
    print("  Para iniciar:")
    print("  Terminal 1: python gateway/server.py")
    print("  Terminal 2: python webui/server.py")
    print("  Abrir: http://localhost:8787")
    print("="*50)

if __name__ == "__main__":
    main()
