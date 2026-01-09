"""Repositório de contas bancárias"""
from typing import Optional, List
from db.models.account import Account
from db.session import db


class AccountRepository:
    """Repositório para operações de conta"""
    
    async def criar_conta(self, account: Account) -> Account:
        """Cria uma nova conta"""
        # Verifica se o CPF já existe
        for conta in db.contas.values():
            if conta.cpf == account.cpf:
                raise ValueError(f"Já existe uma conta com o CPF {account.cpf}")
        
        db.contas[account.id] = account
        return account
    
    async def obter_conta(self, conta_id: int) -> Optional[Account]:
        """Obtém uma conta pelo ID"""
        return db.contas.get(conta_id)
    
    async def obter_conta_por_cpf(self, cpf: str) -> Optional[Account]:
        """Obtém uma conta pelo CPF"""
        for conta in db.contas.values():
            if conta.cpf == cpf:
                return conta
        return None
    
    async def atualizar_conta(self, account: Account) -> Account:
        """Atualiza uma conta existente"""
        if account.id not in db.contas:
            raise ValueError(f"Conta {account.id} não encontrada")
        
        db.contas[account.id] = account
        return account
    
    async def listar_contas(self) -> List[Account]:
        """Lista todas as contas"""
        return list(db.contas.values())
    
    async def deletar_conta(self, conta_id: int) -> bool:
        """Deleta uma conta"""
        if conta_id in db.contas:
            del db.contas[conta_id]
            return True
        return False
