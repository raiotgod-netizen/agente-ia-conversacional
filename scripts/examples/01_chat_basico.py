#!/usr/bin/env python3
"""
Ejemplo 1: Chat basico con el AI Agent
Demuestra como enviar mensajes y recibir respuestas.
"""

import requests
import json

# Configuracion
GATEWAY_URL = "http://localhost:8642"

def check_health():
    """Verifica que el gateway este funcionando."""
    try:
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        data = resp.json()
        print(f"Gateway: {data['status']}")
        print(f"Modelo: {data['model']}")
        print(f"Provider: {data['provider']}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_message(message):
    """Envia un mensaje y retorna la respuesta."""
    try:
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": message},
            timeout=120
        )
        data = resp.json()
        return data.get("response", data.get("error", "Sin respuesta"))
    except Exception as e:
        return f"Error: {e}"

def list_tools():
    """Lista las herramientas disponibles."""
    try:
        resp = requests.get(f"{GATEWAY_URL}/tools", timeout=5)
        data = resp.json()
        return data.get("tools", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_history():
    """Obtiene el historial de conversacion."""
    try:
        resp = requests.get(f"{GATEWAY_URL}/history", timeout=5)
        data = resp.json()
        return data.get("history", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def clear_memory():
    """Limpia la memoria de conversacion."""
    try:
        resp = requests.post(f"{GATEWAY_URL}/memory/clear", timeout=5)
        data = resp.json()
        return data.get("status") == "cleared"
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 50)
    print("AI Agent Kit - Ejemplo 1: Chat Basico")
    print("=" * 50)
    
    # Verificar conexion
    print("\n[1] Verificando conexion...")
    if not check_health():
        print("No se pudo conectar al gateway. Asegurate de que este corriendo.")
        return
    
    # Listar tools
    print("\n[2] Herramientas disponibles:")
    tools = list_tools()
    for tool in tools:
        print(f"  - {tool}")
    
    # Chat basico
    print("\n[3] Iniciando chat...")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            user_input = input("Tu: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit', 'q']:
                print("Hasta luego!")
                break
            
            if not user_input:
                continue
            
            print("IA: ", end="", flush=True)
            response = send_message(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrumpido. Hasta luego!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
