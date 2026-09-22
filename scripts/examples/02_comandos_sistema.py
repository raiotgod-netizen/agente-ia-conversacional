#!/usr/bin/env python3
"""
Ejemplo 2: Ejecutar comandos del sistema
Demuestra como usar la tool terminal para ejecutar comandos.
"""

import requests
import json

GATEWAY_URL = "http://localhost:8642"

def send_command(message):
    """Envia un mensaje que ejecuta un comando."""
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

def main():
    print("=" * 50)
    print("AI Agent Kit - Ejemplo 2: Comandos del Sistema")
    print("=" * 50)
    
    # Ejemplos de comandos
    ejemplos = [
        "Que archivos hay en el directorio actual?",
        "Cual es la fecha y hora actual?",
        "Que procesos estan corriendo?",
        "Crea un archivo llamado test.txt con el contenido 'Hola mundo'",
        "Lee el contenido del archivo test.txt",
        "Cual es el uso de memoria del sistema?",
        "Busca archivos .py en el directorio",
        "Ejecuta el comando 'ping -c 3 google.com'",
    ]
    
    print("\nEjecutando ejemplos de comandos...\n")
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"[{i}] {ejemplo}")
        print("IA: ", end="", flush=True)
        response = send_command(ejemplo)
        print(response)
        print()
    
    # Ejemplo interactivo
    print("\n" + "=" * 50)
    print("Modo interactivo - Escribe comandos en lenguaje natural")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        try:
            user_input = input("Comando: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit', 'q']:
                print("Hasta luego!")
                break
            
            if not user_input:
                continue
            
            print("Resultado: ", end="", flush=True)
            response = send_command(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrumpido!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
