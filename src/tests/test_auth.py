"""Testes para os endpoints de autenticação"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAuth:
    """Testes de autenticação"""
    
    def test_login_success(self):
        """Testa login bem-sucedido"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "cpf": "12345678900",
                "senha": "senha123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_cpf(self):
        """Testa login com CPF inválido"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "cpf": "invalid",
                "senha": "senha123"
            }
        )
        assert response.status_code == 422  # Validação do Pydantic
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "cpf": "12345678900",
                "senha": "senha_errada"
            }
        )
        assert response.status_code == 401
        assert "inválidos" in response.json()["detail"].lower()
    
    def test_login_missing_password(self):
        """Testa login sem senha"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "cpf": "12345678900"
            }
        )
        assert response.status_code == 422  # Validação do Pydantic


@pytest.fixture
def auth_token():
    """Fixture para obter um token válido"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "cpf": "12345678900",
            "senha": "senha123"
        }
    )
    return response.json()["access_token"]
