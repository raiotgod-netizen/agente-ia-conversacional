#!/usr/bin/env python3
"""
Tests para las herramientas del AI Agent.
Ejecutar: python -m pytest tests/test_tools.py -v
"""

import pytest
import sys
import os
import json
import tempfile

# Agregar directorio del gateway al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gateway'))


class TestToolTerminal:
    """Tests para la tool terminal."""
    
    def test_terminal_executes_command(self):
        """Verifica que puede ejecutar comandos basicos."""
        from server import tool_terminal
        result = tool_terminal("echo hola")
        assert "hola" in result
    
    def test_terminal_handles_error(self):
        """Verifica que maneja comandos invalidos."""
        from server import tool_terminal
        result = tool_terminal("comando_que_no_existe_12345")
        # Deberia retornar algun tipo de error o salida
        assert isinstance(result, str)
    
    def test_terminal_returns_string(self):
        """Verifica que retorna un string."""
        from server import tool_terminal
        result = tool_terminal("echo test")
        assert isinstance(result, str)


class TestToolWebSearch:
    """Tests para la tool web_search."""
    
    def test_web_search_returns_results(self):
        """Verifica que retorna resultados de busqueda."""
        from server import tool_web_search
        result = tool_web_search("python programming")
        assert isinstance(result, str)
        # Puede fallar si no hay conexion, pero no debe crashear
        assert len(result) > 0


class TestToolReadFile:
    """Tests para la tool read_file."""
    
    def test_read_file_reads_content(self):
        """Verifica que lee el contenido de un archivo."""
        from server import tool_read_file
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("contenido de prueba")
            temp_path = f.name
        
        try:
            result = tool_read_file(temp_path)
            assert "contenido de prueba" in result
        finally:
            os.unlink(temp_path)
    
    def test_read_file_handles_nonexistent(self):
        """Verifica que maneja archivos inexistentes."""
        from server import tool_read_file
        result = tool_read_file("/nonexistent/file/path.txt")
        assert "ERROR" in result or "error" in result.lower()


class TestToolWriteFile:
    """Tests para la tool write_file."""
    
    def test_write_file_creates_file(self):
        """Verifica que crea un archivo."""
        from server import tool_write_file
        
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        test_file = os.path.join(temp_dir, "test_write.txt")
        
        try:
            result = tool_write_file(test_file, "contenido de prueba")
            assert "OK" in result
            
            # Verificar que el archivo se creo
            assert os.path.exists(test_file)
            
            # Verificar contenido
            with open(test_file, 'r') as f:
                content = f.read()
            assert content == "contenido de prueba"
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)
            os.rmdir(temp_dir)
    
    def test_write_file_creates_directories(self):
        """Verifica que crea directorios automaticamente."""
        from server import tool_write_file
        
        # Crear ruta con directorios nuevos
        temp_dir = tempfile.mkdtemp()
        nested_file = os.path.join(temp_dir, "subdir", "test.txt")
        
        try:
            result = tool_write_file(nested_file, "test")
            assert "OK" in result
            assert os.path.exists(nested_file)
        finally:
            if os.path.exists(nested_file):
                os.unlink(nested_file)
            # Limpiar directorios
            os.rmdir(os.path.dirname(nested_file))
            os.rmdir(temp_dir)


class TestToolListFiles:
    """Tests para la tool list_files."""
    
    def test_list_files_returns_list(self):
        """Verifica que retorna una lista de archivos."""
        from server import tool_list_files
        result = tool_list_files(".")
        assert isinstance(result, str)
        # Deberia contener archivos del directorio actual
        assert len(result) > 0
    
    def test_list_files_handles_nonexistent(self):
        """Verifica que maneja directorios inexistentes."""
        from server import tool_list_files
        result = tool_list_files("/nonexistent/directory")
        # Deberia retornar error o lista vacia
        assert isinstance(result, str)


class TestToolSearchFiles:
    """Tests para la tool search_files."""
    
    def test_search_files_finds_files(self):
        """Verifica que busca archivos por patron."""
        from server import tool_search_files
        result = tool_search_files("*.py", ".")
        assert isinstance(result, str)


class TestToolReadDocx:
    """Tests para la tool read_docx."""
    
    def test_read_docx_handles_nonexistent(self):
        """Verifica que maneja archivos inexistentes."""
        from server import tool_read_docx
        result = tool_read_docx("/nonexistent/file.docx")
        # Deberia retornar error
        assert isinstance(result, str)


class TestToolGetTime:
    """Tests para la tool get_time."""
    
    def test_get_time_returns_time(self):
        """Verifica que retorna la hora actual."""
        from server import tool_get_time
        result = tool_get_time()
        assert isinstance(result, str)
        # Deberia contener fecha/hora
        assert len(result) > 0


class TestToolSystemInfo:
    """Tests para la tool system_info."""
    
    def test_system_info_returns_info(self):
        """Verifica que retorna informacion del sistema."""
        from server import tool_system_info
        result = tool_system_info()
        assert isinstance(result, str)
        # Deberia contener info del SO
        assert len(result) > 0


class TestToolCalculator:
    """Tests para la tool calculator."""
    
    def test_calculator_basic_math(self):
        """Verifica que puede hacer operaciones basicas."""
        from server import tool_calculator
        result = tool_calculator("2 + 2")
        assert "4" in result
    
    def test_calculator_complex_expression(self):
        """Verifica que puede evaluar expresiones complejas."""
        from server import tool_calculator
        result = tool_calculator("(2 + 3) * 4")
        assert "20" in result
    
    def test_calculator_handles_invalid(self):
        """Verifica que maneja expresiones invalidas."""
        from server import tool_calculator
        result = tool_calculator("esto no es math")
        # Deberia retornar error
        assert isinstance(result, str)


class TestToolClipboard:
    """Tests para la tool clipboard."""
    
    def test_clipboard_get(self):
        """Verifica que puede obtener el clipboard."""
        from server import tool_clipboard
        result = tool_clipboard("get")
        # Puede fallar si no hay contenido, pero no debe crashear
        assert isinstance(result, str)
    
    def test_clipboard_set(self):
        """Verifica que puede setear el clipboard."""
        from server import tool_clipboard
        result = tool_clipboard("set", "texto de prueba")
        # Deberia funcionar en la mayoria de sistemas
        assert isinstance(result, str)


class TestToolWeather:
    """Tests para la tool weather."""
    
    def test_weather_returns_weather(self):
        """Verifica que retorna informacion del clima."""
        from server import tool_weather
        result = tool_weather("Santiago")
        assert isinstance(result, str)
        # Puede fallar si no hay conexion
        assert len(result) > 0
    
    def test_weather_default_city(self):
        """Verifica que usa ciudad por defecto."""
        from server import tool_weather
        result = tool_weather()
        assert isinstance(result, str)


class TestToolProcessList:
    """Tests para la tool process_list."""
    
    def test_process_list_returns_processes(self):
        """Verifica que retorna una lista de procesos."""
        from server import tool_process_list
        result = tool_process_list()
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_process_list_with_filter(self):
        """Verifica que puede filtrar por nombre."""
        from server import tool_process_list
        result = tool_process_list("python")
        assert isinstance(result, str)


class TestToolKillProcess:
    """Tests para la tool kill_process."""
    
    def test_kill_process_handles_nonexistent(self):
        """Verifica que maneja procesos inexistentes."""
        from server import tool_kill_process
        result = tool_kill_process("nonexistent_process_12345")
        # Deberia retornar algun tipo de respuesta
        assert isinstance(result, str)


class TestToolOpenUrl:
    """Tests para la tool open_url."""
    
    def test_open_url_returns_status(self):
        """Verifica que retorna estado de la operacion."""
        from server import tool_open_url
        # No abrimos URL real para evitar efectos secundarios
        # Solo verificamos que la funcion existe
        assert callable(tool_open_url)


class TestToolNetworkInfo:
    """Tests para la tool network_info."""
    
    def test_network_info_returns_info(self):
        """Verifica que retorna informacion de red."""
        from server import tool_network_info
        result = tool_network_info()
        assert isinstance(result, str)
        assert len(result) > 0


class TestExtractToolCall:
    """Tests para la funcion extract_tool_call."""
    
    def test_extract_valid_tool_call(self):
        """Verifica que extrae tool calls validos."""
        from server import extract_tool_call
        
        response = '{"tool_call": {"name": "terminal", "args": {"command": "ls"}}}'
        result = extract_tool_call(response)
        
        assert result is not None
        assert result["name"] == "terminal"
        assert result["args"]["command"] == "ls"
    
    def test_extract_tool_call_with_text(self):
        """Verifica que extrae tool calls con texto adicional."""
        from server import extract_tool_call
        
        response = 'Voy a ejecutar esto: {"tool_call": {"name": "terminal", "args": {"command": "pwd"}}}'
        result = extract_tool_call(response)
        
        assert result is not None
        assert result["name"] == "terminal"
    
    def test_extract_no_tool_call(self):
        """Verifica que retorna None cuando no hay tool call."""
        from server import extract_tool_call
        
        response = "Esta es una respuesta normal sin tool calls"
        result = extract_tool_call(response)
        
        assert result is None
    
    def test_extract_invalid_json(self):
        """Verifica que maneja JSON invalido."""
        from server import extract_tool_call
        
        response = '{"tool_call": {"name": "terminal", args: invalid}}'
        result = extract_tool_call(response)
        
        # Deberia retornar None o manejar el error
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
