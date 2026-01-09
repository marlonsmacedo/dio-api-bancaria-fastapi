#!/usr/bin/env python3
"""
Script de exemplo para testar a API bancária.
Demonstra como usar os endpoints da API.
"""

import requests
import json
from typing import Optional

# URL base da API
BASE_URL = "http://localhost:8000"

class BankAPIClient:
    """Cliente para testar a API bancária"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def login(self, cpf: str, senha: str) -> bool:
        """Faz login na API"""
        print(f"\n📝 Fazendo login com CPF {cpf}...")
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"cpf": cpf, "senha": senha},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            print("✅ Login realizado com sucesso!")
            return True
        else:
            print(f"❌ Erro no login: {response.text}")
            return False
    
    def criar_conta(self, cpf: str, titular: str, saldo_inicial: float = 0.0) -> Optional[dict]:
        """Cria uma nova conta"""
        print(f"\n💳 Criando conta para {titular}...")
        response = requests.post(
            f"{self.base_url}/api/v1/contas/",
            json={
                "cpf": cpf,
                "titular": titular,
                "saldo_inicial": saldo_inicial
            },
            headers=self.headers
        )
        
        if response.status_code == 201:
            conta = response.json()
            print(f"✅ Conta criada! ID: {conta['id']}")
            print(f"   CPF: {conta['cpf']}")
            print(f"   Titular: {conta['titular']}")
            print(f"   Saldo: R$ {conta['saldo']:.2f}")
            return conta
        else:
            print(f"❌ Erro ao criar conta: {response.text}")
            return None
    
    def obter_conta(self, conta_id: int) -> Optional[dict]:
        """Obtém informações de uma conta"""
        print(f"\n🔍 Obtendo dados da conta {conta_id}...")
        response = requests.get(
            f"{self.base_url}/api/v1/contas/{conta_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            conta = response.json()
            print(f"✅ Conta encontrada!")
            print(f"   ID: {conta['id']}")
            print(f"   Titular: {conta['titular']}")
            print(f"   Saldo: R$ {conta['saldo']:.2f}")
            return conta
        else:
            print(f"❌ Erro ao obter conta: {response.text}")
            return None
    
    def listar_contas(self) -> Optional[list]:
        """Lista todas as contas"""
        print(f"\n📋 Listando todas as contas...")
        response = requests.get(
            f"{self.base_url}/api/v1/contas/",
            headers=self.headers
        )
        
        if response.status_code == 200:
            contas = response.json()
            print(f"✅ Total de contas: {len(contas)}")
            for conta in contas:
                print(f"   - {conta['id']}: {conta['titular']} (R$ {conta['saldo']:.2f})")
            return contas
        else:
            print(f"❌ Erro ao listar contas: {response.text}")
            return None
    
    def depositar(self, conta_id: int, valor: float, descricao: str = "") -> Optional[dict]:
        """Realiza um depósito"""
        print(f"\n💰 Depositando R$ {valor:.2f} na conta {conta_id}...")
        response = requests.post(
            f"{self.base_url}/api/v1/transacoes/depositar",
            json={
                "conta_id": conta_id,
                "valor": valor,
                "descricao": descricao
            },
            headers=self.headers
        )
        
        if response.status_code == 201:
            transacao = response.json()
            print(f"✅ Depósito realizado!")
            print(f"   Transação ID: {transacao['id']}")
            print(f"   Valor: R$ {transacao['valor']:.2f}")
            print(f"   Data: {transacao['criada_em']}")
            return transacao
        else:
            print(f"❌ Erro no depósito: {response.text}")
            return None
    
    def sacar(self, conta_id: int, valor: float, descricao: str = "") -> Optional[dict]:
        """Realiza um saque"""
        print(f"\n🏧 Sacando R$ {valor:.2f} da conta {conta_id}...")
        response = requests.post(
            f"{self.base_url}/api/v1/transacoes/sacar",
            json={
                "conta_id": conta_id,
                "valor": valor,
                "descricao": descricao
            },
            headers=self.headers
        )
        
        if response.status_code == 201:
            transacao = response.json()
            print(f"✅ Saque realizado!")
            print(f"   Transação ID: {transacao['id']}")
            print(f"   Valor: R$ {transacao['valor']:.2f}")
            print(f"   Data: {transacao['criada_em']}")
            return transacao
        else:
            print(f"❌ Erro no saque: {response.text}")
            return None
    
    def obter_extrato(self, conta_id: int) -> Optional[list]:
        """Obtém o extrato de uma conta"""
        print(f"\n📄 Obtendo extrato da conta {conta_id}...")
        response = requests.get(
            f"{self.base_url}/api/v1/transacoes/extrato/{conta_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            transacoes = response.json()
            print(f"✅ Total de transações: {len(transacoes)}")
            
            for transacao in transacoes:
                tipo_emoji = "➕" if transacao['tipo'] == 'deposito' else "➖"
                print(f"   {tipo_emoji} {transacao['tipo'].upper()}: R$ {transacao['valor']:.2f}")
                print(f"      Data: {transacao['criada_em']}")
                if transacao['descricao']:
                    print(f"      Descrição: {transacao['descricao']}")
            
            return transacoes
        else:
            print(f"❌ Erro ao obter extrato: {response.text}")
            return None


def main():
    """Função principal - demonstra o uso da API"""
    
    print("=" * 60)
    print("🏦 TESTE DA API BANCÁRIA")
    print("=" * 60)
    
    # Criar cliente
    client = BankAPIClient()
    
    # 1. Login
    if not client.login("12345678900", "senha123"):
        print("Não foi possível fazer login. Encerrando...")
        return
    
    # 2. Criar uma conta
    conta1 = client.criar_conta(
        cpf="11122233344",
        titular="João Silva",
        saldo_inicial=1000.00
    )
    
    if not conta1:
        print("Não foi possível criar conta. Encerrando...")
        return
    
    conta_id = conta1["id"]
    
    # 3. Obter dados da conta
    client.obter_conta(conta_id)
    
    # 4. Listar todas as contas
    client.listar_contas()
    
    # 5. Fazer um depósito
    client.depositar(conta_id, 500.00, "Depósito de salário")
    
    # 6. Verificar saldo atualizado
    client.obter_conta(conta_id)
    
    # 7. Fazer um saque
    client.sacar(conta_id, 200.00, "Saque no caixa eletrônico")
    
    # 8. Verificar saldo final
    client.obter_conta(conta_id)
    
    # 9. Obter extrato
    client.obter_extrato(conta_id)
    
    # 10. Tentar saque maior que o saldo
    print("\n⚠️  Testando validação de saldo insuficiente...")
    client.sacar(conta_id, 10000.00, "Saque grande demais")
    
    # 11. Tentar depósito com valor negativo
    print("\n⚠️  Testando validação de valor negativo...")
    client.depositar(conta_id, -100.00, "Valor negativo")
    
    print("\n" + "=" * 60)
    print("✅ TESTE FINALIZADO")
    print("=" * 60)
    print("\nAcesse a documentação interativa em:")
    print("  📖 Swagger: http://localhost:8000/docs")
    print("  📖 ReDoc: http://localhost:8000/redoc")


if __name__ == "__main__":
    main()
