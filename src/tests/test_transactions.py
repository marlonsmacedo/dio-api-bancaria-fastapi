"""Testes para os endpoints de transações"""
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


@pytest.fixture
def conta_id(auth_token):
    """Fixture para criar uma conta de teste"""
    response = client.post(
        "/api/v1/contas/",
        json={
            "cpf": "55555555555",
            "titular": "Test User",
            "saldo_inicial": 5000.00
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()["id"]


class TestTransactions:
    """Testes de transações"""
    
    def test_depositar_success(self, auth_token, conta_id):
        """Testa depósito bem-sucedido"""
        response = client.post(
            "/api/v1/transacoes/depositar",
            json={
                "conta_id": conta_id,
                "valor": 500.00,
                "descricao": "Depósito de teste"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["tipo"] == "deposito"
        assert data["valor"] == 500.00
        assert data["conta_id"] == conta_id
    
    def test_depositar_valor_negativo(self, auth_token, conta_id):
        """Testa depósito com valor negativo"""
        response = client.post(
            "/api/v1/transacoes/depositar",
            json={
                "conta_id": conta_id,
                "valor": -100.00,
                "descricao": "Depósito inválido"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 422
    
    def test_sacar_success(self, auth_token, conta_id):
        """Testa saque bem-sucedido"""
        response = client.post(
            "/api/v1/transacoes/sacar",
            json={
                "conta_id": conta_id,
                "valor": 100.00,
                "descricao": "Saque de teste"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["tipo"] == "saque"
        assert data["valor"] == 100.00
        assert data["conta_id"] == conta_id
    
    def test_sacar_saldo_insuficiente(self, auth_token, conta_id):
        """Testa saque sem saldo suficiente"""
        response = client.post(
            "/api/v1/transacoes/sacar",
            json={
                "conta_id": conta_id,
                "valor": 10000.00,
                "descricao": "Saque grande"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400
        assert "insuficiente" in response.json()["detail"].lower()
    
    def test_sacar_valor_negativo(self, auth_token, conta_id):
        """Testa saque com valor negativo"""
        response = client.post(
            "/api/v1/transacoes/sacar",
            json={
                "conta_id": conta_id,
                "valor": -50.00,
                "descricao": "Saque inválido"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 422
    
    def test_obter_extrato_success(self, auth_token, conta_id):
        """Testa obtenção de extrato"""
        # Fazer algumas transações
        client.post(
            "/api/v1/transacoes/depositar",
            json={
                "conta_id": conta_id,
                "valor": 200.00,
                "descricao": "Depósito 1"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        client.post(
            "/api/v1/transacoes/sacar",
            json={
                "conta_id": conta_id,
                "valor": 50.00,
                "descricao": "Saque 1"
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Obter extrato
        response = client.get(
            f"/api/v1/transacoes/extrato/{conta_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_obter_extrato_conta_inexistente(self, auth_token):
        """Testa obtenção de extrato de conta inexistente"""
        response = client.get(
            "/api/v1/transacoes/extrato/99999",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 404
    
    def test_transacao_sem_autenticacao(self, conta_id):
        """Testa transação sem autenticação"""
        response = client.post(
            "/api/v1/transacoes/depositar",
            json={
                "conta_id": conta_id,
                "valor": 100.00,
                "descricao": "Sem autenticação"
            }
        )
        assert response.status_code == 403
