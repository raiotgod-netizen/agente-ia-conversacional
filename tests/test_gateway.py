#!/usr/bin/env python3
"""
Tests para el AI Agent Gateway.
Ejecutar: python -m pytest tests/test_gateway.py -v
"""

import pytest
import requests
import json
import time

# Configuracion
GATEWAY_URL = "http://localhost:8642"
TEST_TIMEOUT = 30


class TestHealthEndpoint:
    """Tests para el endpoint /health."""
    
    def test_health_returns_200(self):
        """Verifica que /health retorna 200."""
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        assert resp.status_code == 200
    
    def test_health_returns_status_ok(self):
        """Verifica que el status es 'ok'."""
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        data = resp.json()
        assert data["status"] == "ok"
    
    def test_health_returns_model(self):
        """Verifica que retorna el modelo."""
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        data = resp.json()
        assert "model" in data
        assert len(data["model"]) > 0
    
    def test_health_returns_provider(self):
        """Verifica que retorna el provider."""
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        data = resp.json()
        assert "provider" in data
        assert data["provider"] in ["ollama", "openrouter", "groq", "openai", "deepseek", "anthropic", "together"]


class TestToolsEndpoint:
    """Tests para el endpoint /tools."""
    
    def test_tools_returns_200(self):
        """Verifica que /tools retorna 200."""
        resp = requests.get(f"{GATEWAY_URL}/tools", timeout=5)
        assert resp.status_code == 200
    
    def test_tools_returns_list(self):
        """Verifica que retorna una lista de tools."""
        resp = requests.get(f"{GATEWAY_URL}/tools", timeout=5)
        data = resp.json()
        assert "tools" in data
        assert isinstance(data["tools"], list)
    
    def test_tools_contains_terminal(self):
        """Verifica que la tool 'terminal' existe."""
        resp = requests.get(f"{GATEWAY_URL}/tools", timeout=5)
        data = resp.json()
        assert "terminal" in data["tools"]
    
    def test_tools_contains_web_search(self):
        """Verifica que la tool 'web_search' existe."""
        resp = requests.get(f"{GATEWAY_URL}/tools", timeout=5)
        data = resp.json()
        assert "web_search" in data["tools"]


class TestChatEndpoint:
    """Tests para el endpoint /chat."""
    
    def test_chat_requires_message(self):
        """Verifica que /chat requiere un mensaje."""
        resp = requests.post(f"{GATEWAY_URL}/chat", json={}, timeout=5)
        assert resp.status_code == 400
    
    def test_chat_returns_response(self):
        """Verifica que /chat retorna una respuesta."""
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Hola"},
            timeout=TEST_TIMEOUT
        )
        data = resp.json()
        assert "response" in data
        assert len(data["response"]) > 0
    
    def test_chat_handles_simple_question(self):
        """Verifica que maneja preguntas simples."""
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Que dia es hoy?"},
            timeout=TEST_TIMEOUT
        )
        data = resp.json()
        assert "response" in data
    
    def test_chat_handles_get_time(self):
        """Verifica que puede ejecutar la tool get_time."""
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Dime la hora actual"},
            timeout=TEST_TIMEOUT
        )
        data = resp.json()
        assert "response" in data


class TestHistoryEndpoint:
    """Tests para el endpoint /history."""
    
    def test_history_returns_200(self):
        """Verifica que /history retorna 200."""
        resp = requests.get(f"{GATEWAY_URL}/history", timeout=5)
        assert resp.status_code == 200
    
    def test_history_returns_list(self):
        """Verifica que retorna una lista."""
        resp = requests.get(f"{GATEWAY_URL}/history", timeout=5)
        data = resp.json()
        assert "history" in data
        assert isinstance(data["history"], list)


class TestMemoryClearEndpoint:
    """Tests para el endpoint /memory/clear."""
    
    def test_clear_returns_200(self):
        """Verifica que /memory/clear retorna 200."""
        resp = requests.post(f"{GATEWAY_URL}/memory/clear", timeout=5)
        assert resp.status_code == 200
    
    def test_clear_returns_status(self):
        """Verifica que retorna status 'cleared'."""
        resp = requests.post(f"{GATEWAY_URL}/memory/clear", timeout=5)
        data = resp.json()
        assert data["status"] == "cleared"


class TestNotFoundEndpoint:
    """Tests para endpoints inexistentes."""
    
    def test_unknown_endpoint_returns_404(self):
        """Verifica que endpoints inexistentes retornan 404."""
        resp = requests.get(f"{GATEWAY_URL}/nonexistent", timeout=5)
        assert resp.status_code == 404
    
    def test_unknown_post_returns_404(self):
        """Verifica que POST a endpoint inexistente retorna 404."""
        resp = requests.post(f"{GATEWAY_URL}/nonexistent", timeout=5)
        assert resp.status_code == 404


class TestIntegration:
    """Tests de integracion."""
    
    def test_full_conversation_flow(self):
        """Test de flujo completo de conversacion."""
        # 1. Verificar salud
        health = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        assert health.status_code == 200
        
        # 2. Enviar mensaje
        chat_resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Hola, que herramientas tienes?"},
            timeout=TEST_TIMEOUT
        )
        assert chat_resp.status_code == 200
        
        # 3. Verificar historial
        history = requests.get(f"{GATEWAY_URL}/history", timeout=5)
        assert history.status_code == 200
        data = history.json()
        assert len(data["history"]) >= 2  # Al menos el mensaje del usuario y la respuesta
    
    def test_tool_call_execution(self):
        """Test de ejecucion de tool call."""
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Dime que hora es usando get_time"},
            timeout=TEST_TIMEOUT
        )
        data = resp.json()
        assert "response" in data


# Tests de rendimiento
class TestPerformance:
    """Tests de rendimiento."""
    
    def test_health_response_time(self):
        """Verifica que /health responde rapido."""
        start = time.time()
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        elapsed = time.time() - start
        assert resp.status_code == 200
        assert elapsed < 1.0  # Debe responder en menos de 1 segundo
    
    def test_chat_response_time(self):
        """Verifica que /chat responde en tiempo razonable."""
        start = time.time()
        resp = requests.post(
            f"{GATEWAY_URL}/chat",
            json={"message": "Hola"},
            timeout=TEST_TIMEOUT
        )
        elapsed = time.time() - start
        assert resp.status_code == 200
        assert elapsed < 30.0  # Debe responder en menos de 30 segundos


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
