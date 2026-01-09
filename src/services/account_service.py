"""Serviço de contas bancárias"""
from typing import List, Optional
from datetime import datetime
from schemas.account import AccountCreate, AccountResponse
from db.models.account import Account
from db.repository.account_repository import AccountRepository
from db.session import db


class AccountService:
    """Serviço para gerenciar contas bancárias"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.repository = AccountRepository()
    
    async def criar_conta(self, account_data: AccountCreate) -> AccountResponse:
        """
        Cria uma nova conta bancária.
        
        Args:
            account_data: Dados da conta a ser criada
            
        Returns:
            AccountResponse: Dados da conta criada
            
        Raises:
            ValueError: Se o CPF já existe
        """
        # Verifica se CPF já existe
        existente = await self.repository.obter_conta_por_cpf(account_data.cpf)
        if existente:
            raise ValueError(f"Já existe uma conta com o CPF {account_data.cpf}")
        
        # Cria a conta
        conta_id = db.obter_proximo_conta_id()
        account = Account(
            id=conta_id,
            cpf=account_data.cpf,
            titular=account_data.titular,
            saldo=account_data.saldo_inicial,
            criada_em=datetime.utcnow(),
            atualizada_em=datetime.utcnow()
        )
        
        await self.repository.criar_conta(account)
        return self._to_response(account)
    
    async def obter_conta(self, conta_id: int) -> Optional[AccountResponse]:
        """
        Obtém uma conta pelo ID.
        
        Args:
            conta_id: ID da conta
            
        Returns:
            AccountResponse ou None se não encontrada
        """
        account = await self.repository.obter_conta(conta_id)
        if account:
            return self._to_response(account)
        return None
    
    async def listar_contas(self) -> List[AccountResponse]:
        """
        Lista todas as contas.
        
        Returns:
            Lista de AccountResponse
        """
        contas = await self.repository.listar_contas()
        return [self._to_response(c) for c in contas]
    
    async def atualizar_saldo(self, conta_id: int, novo_saldo: float) -> AccountResponse:
        """
        Atualiza o saldo de uma conta.
        
        Args:
            conta_id: ID da conta
            novo_saldo: Novo saldo
            
        Returns:
            AccountResponse atualizada
            
        Raises:
            ValueError: Se a conta não existe
        """
        account = await self.repository.obter_conta(conta_id)
        if not account:
            raise ValueError(f"Conta {conta_id} não encontrada")
        
        account.saldo = novo_saldo
        account.atualizada_em = datetime.utcnow()
        await self.repository.atualizar_conta(account)
        
        return self._to_response(account)
    
    def _to_response(self, account: Account) -> AccountResponse:
        """Converte Account para AccountResponse"""
        return AccountResponse(
            id=account.id,
            cpf=account.cpf,
            titular=account.titular,
            saldo=account.saldo,
            criada_em=account.criada_em,
            atualizada_em=account.atualizada_em
        )
