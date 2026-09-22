# Tools Reference

## Lista de herramientas

El AI Agent Kit incluye 16 herramientas organizadas en 4 categorias.

## Herramientas de terminal

### terminal

Ejecuta comandos del sistema operativo.

**Parametros:**

- `command` (string, requerido): Comando a ejecutar

**Ejemplo:**

```json
{"tool_call": {"name": "terminal", "args": {"command": "ls -la"}}}
```

**Respuesta:**

```
total 48
drwxr-xr-x 5 user user 4096 Sep 22 14:30 .
drwxr-xr-x 3 user user 4096 Sep 22 14:00 ..
-rw-r--r-- 1 user user  220 Sep 22 14:00 README.md
```

**Limitaciones:**

- Timeout de 30 segundos
- Output maximo de 3000 caracteres

---

### process_list

Lista procesos en ejecucion.

**Parametros:**

- `filter_name` (string, opcional): Filtrar por nombre de proceso

**Ejemplo:**

```json
{"tool_call": {"name": "process_list", "args": {"filter_name": "python"}}}
```

**Respuesta:**

```
python.exe,12345,Console,1,15,45678,0,2026/09/22 14:30,0:00:05,0.5,234
python.exe,12346,Console,1,12,34567,0,2026/09/22 14:31,0:00:03,0.3,189
```

---

### kill_process

Mata un proceso por nombre.

**Parametros:**

- `name` (string, requerido): Nombre del proceso a matar

**Ejemplo:**

```json
{"tool_call": {"name": "kill_process", "args": {"name": "notepad.exe"}}}
```

**Respuesta:**

```
Exito: Proceso notepad.exe terminado
```

**Advertencia:** Use con cuidado. No mate procesos criticos del sistema.

---

## Herramientas de archivos

### read_file

Lee el contenido de archivos de texto.

**Parametros:**

- `path` (string, requerido): Ruta del archivo

**Ejemplo:**

```json
{"tool_call": {"name": "read_file", "args": {"path": "mi_archivo.txt"}}}
```

**Respuesta:**

```
Este es el contenido del archivo...
 linea 2
 linea 3
```

**Formatos soportados:**

- .txt
- .py
- .js
- .json
- .md
- .csv
- Cualquier archivo de texto plano

**Limitaciones:**

- Maximo 5000 caracteres por lectura
- No lee archivos binarios

---

### write_file

Crea o modifica archivos de texto.

**Parametros:**

- `path` (string, requerido): Ruta del archivo
- `content` (string, requerido): Contenido a escribir

**Ejemplo:**

```json
{"tool_call": {"name": "write_file", "args": {"path": "mi_archivo.txt", "content": "Hola mundo"}}}
```

**Respuesta:**

```
OK: mi_archivo.txt
```

**Comportamiento:**

- Crea el archivo si no existe
- Sobreescribe si ya existe
- Crea directorios automaticamente

---

### list_files

Lista archivos en un directorio.

**Parametros:**

- `path` (string, opcional): Directorio a listar (default: directorio actual)

**Ejemplo:**

```json
{"tool_call": {"name": "list_files", "args": {"path": "src"}}}
```

**Respuesta:**

```
__init__.py
main.py
utils.py
models/
templates/
```

---

### search_files

Busca archivos por nombre o patron.

**Parametros:**

- `pattern` (string, requerido): Patron de busqueda (puede incluir * y ?)
- `path` (string, opcional): Directorio donde buscar

**Ejemplo:**

```json
{"tool_call": {"name": "search_files", "args": {"pattern": "*.py", "path": "."}}}
```

**Respuesta:**

```
src/main.py
src/utils.py
tests/test_main.py
```

---

### read_docx

Lee archivos Word (.docx) y extrae el texto.

**Parametros:**

- `path` (string, requerido): Ruta del archivo .docx

**Ejemplo:**

```json
{"tool_call": {"name": "read_docx", "args": {"path": "documento.docx"}}}
```

**Respuesta:**

```
Titulo del documento
Primer parrafo del documento.
Segundo parrafo...
Tabla: Columna1 | Columna2 | Columna3
```

**Requisito:** pip install python-docx

---

## Herramientas de internet

### web_search

Busca en internet usando DuckDuckGo.

**Parametros:**

- `query` (string, requerido): Termino de busqueda

**Ejemplo:**

```json
{"tool_call": {"name": "web_search", "args": {"query": "python tutorial principiantes"}}}
```

**Respuesta:**

```
- Python Tutorial - Python.org: Learn Python programming step by step...
- Tutorial Python Basico -不明: Guia completa para empezar con Python...
- Python para Principiantes -不明: Curso gratis de Python desde cero...
```

**Limitaciones:**

- Maximo 3 resultados por busqueda
- Requiere: pip install duckduckgo-search

---

### open_url

Abre una URL en el navegador predeterminado.

**Parametros:**

- `url` (string, requerido): URL a abrir

**Ejemplo:**

```json
{"tool_call": {"name": "open_url", "args": {"url": "https://google.com"}}}
```

**Respuesta:**

```
Abierto: https://google.com
```

---

### weather

Obtiene el clima de una ciudad.

**Parametros:**

- `city` (string, opcional): Ciudad a consultar (default: "Puerto Montt")

**Ejemplo:**

```json
{"tool_call": {"name": "weather", "args": {"city": "Santiago"}}}
```

**Respuesta:**

```
Santiago: nublado 18C
```

---

## Herramientas del sistema

### get_time

Obtiene la fecha y hora actual.

**Parametros:** Ninguno

**Ejemplo:**

```json
{"tool_call": {"name": "get_time", "args": {}}}
```

**Respuesta:**

```
2026-09-22 14:30:00 (Tuesday)
```

---

### system_info

Obtiene informacion del sistema.

**Parametros:** Ninguno

**Ejemplo:**

```json
{"tool_call": {"name": "system_info", "args": {}}}
```

**Respuesta:**

```
SO: Windows 11
CPU: Intel i5-8400 @ 2.80GHz
RAM: 16GB
GPU: NVIDIA RTX 3050
Disco: 463GB SSD + 2 HDD
```

---

### calculator

Realiza calculos matematicos.

**Parametros:**

- `expression` (string, requerido): Expresion matematica a evaluar

**Ejemplo:**

```json
{"tool_call": {"name": "calculator", "args": {"expression": "2 + 2 * 3"}}}
```

**Respuesta:**

```
8
```

**Operaciones soportadas:**

- Aritmetica: +, -, *, /, //, %, **
- Funciones: sin, cos, tan, sqrt, log, etc.
- Parentesis: (2 + 3) * 4

---

### clipboard

Obtiene o modifica el portapapeles del sistema.

**Parametros:**

- `action` (string, requerido): "get" o "set"
- `text` (string, opcional): Texto a copiar (requerido si action es "set")

**Ejemplo obtener:**

```json
{"tool_call": {"name": "clipboard", "args": {"action": "get"}}}
```

**Respuesta:**

```
Texto copiado en el portapapeles...
```

**Ejemplo copiar:**

```json
{"tool_call": {"name": "clipboard", "args": {"action": "set", "text": "Hola mundo"}}}
```

**Respuesta:**

```
Clipboard actualizado
```

---

### network_info

Obtiene informacion de red del sistema.

**Parametros:** Ninguno

**Ejemplo:**

```json
{"tool_call": {"name": "network_info", "args": {}}}
```

**Respuesta:**

```json
{
    "hostname": "JARVIS-PC",
    "ip": "192.168.1.100",
    "tailscale": "100.x.x.x"
}
```

---

## Crear tools nuevas

### Estructura basica

```python
def tool_nombre(param1, param2):
    """Descripcion breve de la tool.
    
    Args:
        param1: Descripcion del primer parametro
        param2: Descripcion del segundo parametro
    
    Returns:
        str: Resultado de la ejecucion
    """
    try:
        # Logica de la tool aqui
        resultado = "algo"
        return resultado
    except Exception as e:
        return f"ERROR: {e}"

# Agregar al diccionario TOOLS
TOOLS["nombre"] = tool_nombre
```

### Ejemplo: tool de API

```python
def tool_weather_api(city):
    """Obtiene el clima de una ciudad usando wttr.in."""
    try:
        import requests
        resp = requests.get(
            f"https://wttr.in/{city}?format=3",
            timeout=10
        )
        return resp.text.strip()
    except Exception as e:
        return f"ERROR: {e}"

TOOLS["weather"] = tool_weather_api
```

### Ejemplo: tool de base de datos

```python
def tool_query_db(query):
    """Ejecuta una consulta SQL en la base de datos."""
    try:
        import sqlite3
        db = sqlite3.connect('memory.db')
        cursor = db.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return str(results[:20])
        else:
            db.commit()
            return f"OK: {cursor.rowcount} filas afectadas"
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        db.close()

TOOLS["query_db"] = tool_query_db
```

### Ejemplo: tool con validacion

```python
import re

def tool_safe_terminal(command):
    """Ejecuta comandos con validacion de seguridad."""
    # Comandos bloqueados
    BLOCKED = ['rm -rf', 'format', 'del /s', 'shutdown']
    
    for blocked in BLOCKED:
        if blocked in command.lower():
            return f"ERROR: Comando bloqueado por seguridad: {blocked}"
    
    # Validar longitud
    if len(command) > 1000:
        return "ERROR: Comando demasiado largo"
    
    # Ejecutar
    return tool_terminal(command)

TOOLS["safe_terminal"] = tool_safe_terminal
```

## Mejores practicas

### 1. Siempre manejar errores

```python
def tool_ejemplo(param):
    try:
        # Logica principal
        return "exito"
    except ValueError as e:
        return f"ERROR de validacion: {e}"
    except Exception as e:
        return f"ERROR inesperado: {e}"
```

### 2. Limitar output

```python
def tool_ejemplo(param):
    resultado = "resultado muy largo..."
    return resultado[:3000]  # Limitar a 3000 caracteres
```

### 3. Usar timeout en requests

```python
def tool_ejemplo(param):
    resp = requests.get(url, timeout=10)  # Siempre usar timeout
    return resp.text
```

### 4. Documentar parametros

```python
def tool_ejemplo(param1, param2):
    """Hace algo util.
    
    Args:
        param1 (str): Descripcion clara
        param2 (int): Descripcion clara con rango si aplica
    
    Returns:
        str: Descripcion del resultado
    """
```

### 5. No mutar estado global

```python
# MAL
global_counter = 0

def tool_malo():
    global global_counter
    global_counter += 1
    return str(global_counter)

# BIEN
def tool_bueno():
    # Usar estado local o persistente
    return "resultado"
```

## debugging

### Logs

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def tool_ejemplo(param):
    logger.debug(f"Ejecutando tool con param: {param}")
    # ...
    logger.debug(f"Resultado: {resultado}")
    return resultado
```

### Test unitario

```python
def test_tool_ejemplo():
    resultado = tool_ejemplo("test")
    assert resultado == "esperado"
    assert "ERROR" not in resultado
```

### Test con mock

```python
from unittest.mock import patch, MagicMock

def test_tool_con_mock():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            text="respuesta mock"
        )
        resultado = tool_web_search("test")
        assert "respuesta mock" in resultado
```
