"""Testes para os endpoints de contas"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


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


class TestAccounts:
    """Testes de contas"""
    
    def test_criar_conta_success(self, auth_token):
        """Testa criação de conta bem-sucedida"""
        response = client.post(
            "/api/v1/contas/",
            json={
                "cpf": "98765432100",
                "titular": "Maria Silva",
                "saldo_inicial": 1000.00
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["cpf"] == "98765432100"
        assert data["titular"] == "Maria Silva"
        assert data["saldo"] == 1000.00
    
    def test_criar_conta_sem_autenticacao(self):
        """Testa criação de conta sem autenticação"""
        response = client.post(
            "/api/v1/contas/",
            json={
                "cpf": "98765432100",
                "titular": "Maria Silva",
                "saldo_inicial": 1000.00
            }
        )
        assert response.status_code == 403
    
    def test_criar_conta_cpf_duplicado(self, auth_token):
        """Testa criação de conta com CPF duplicado"""
        # Criar primeira conta
        client.post(
            "/api/v1/contas/",
            json={
                "cpf": "11111111111",
                "titular": "João Silva",
                "saldo_inicial": 500.00
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Tentar criar conta com mesmo CPF
        response = client.post(
            "/api/v1/contas/",
            json={
                "cpf": "11111111111",
                "titular": "João Santos",
                "saldo_inicial": 300.00
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400
    
    def test_obter_conta_success(self, auth_token):
        """Testa obtenção de conta bem-sucedida"""
        # Criar conta
        create_response = client.post(
            "/api/v1/contas/",
            json={
                "cpf": "22222222222",
                "titular": "Ana Costa",
                "saldo_inicial": 2000.00
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        conta_id = create_response.json()["id"]
        
        # Obter conta
        response = client.get(
            f"/api/v1/contas/{conta_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conta_id
        assert data["titular"] == "Ana Costa"
    
    def test_obter_conta_nao_encontrada(self, auth_token):
        """Testa obtenção de conta inexistente"""
        response = client.get(
            "/api/v1/contas/99999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 404
    
    def test_listar_contas(self, auth_token):
        """Testa listagem de contas"""
        response = client.get(
            "/api/v1/contas/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
