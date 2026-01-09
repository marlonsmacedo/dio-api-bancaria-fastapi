"""Serviço de transações bancárias"""
from typing import List
from datetime import datetime
from schemas.transaction import TransactionCreate, TransactionResponse, TransactionType
from db.models.transaction import Transaction, TipoTransacao
from db.repository.transaction_repository import TransactionRepository
from db.repository.account_repository import AccountRepository
from db.session import db


class TransactionService:
    """Serviço para gerenciar transações bancárias"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.repository = TransactionRepository()
        self.account_repository = AccountRepository()
    
    async def criar_transacao(
        self,
        conta_id: int,
        tipo: TransactionType,
        valor: float,
        descricao: str = ""
    ) -> TransactionResponse:
        """
        Cria uma nova transação.
        
        Args:
            conta_id: ID da conta
            tipo: Tipo de transação (deposito ou saque)
            valor: Valor da transação (deve ser positivo)
            descricao: Descrição da transação
            
        Returns:
            TransactionResponse: Dados da transação criada
            
        Raises:
            ValueError: Se a conta não existe, valor inválido ou saldo insuficiente
        """
        # Valida o valor
        if valor <= 0:
            raise ValueError("O valor da transação deve ser positivo")
        
        # Obtém a conta
        account = await self.account_repository.obter_conta(conta_id)
        if not account:
            raise ValueError(f"Conta {conta_id} não encontrada")
        
        # Valida saque
        if tipo == TransactionType.SAQUE:
            if account.saldo < valor:
                raise ValueError(f"Saldo insuficiente. Saldo atual: {account.saldo}")
            # Debita da conta
            account.saldo -= valor
        else:  # Depósito
            # Credita na conta
            account.saldo += valor
        
        # Atualiza o saldo da conta
        account.atualizada_em = datetime.utcnow()
        await self.account_repository.atualizar_conta(account)
        
        # Cria a transação
        transacao_id = db.obter_proximo_transacao_id()
        tipo_enum = TipoTransacao.SAQUE if tipo == TransactionType.SAQUE else TipoTransacao.DEPOSITO
        
        transaction = Transaction(
            id=transacao_id,
            conta_id=conta_id,
            tipo=tipo_enum,
            valor=valor,
            descricao=descricao,
            criada_em=datetime.utcnow()
        )
        
        await self.repository.criar_transacao(transaction)
        return self._to_response(transaction)
    
    async def obter_transacoes_conta(self, conta_id: int) -> List[TransactionResponse]:
        """
        Obtém todas as transações de uma conta.
        
        Args:
            conta_id: ID da conta
            
        Returns:
            Lista de TransactionResponse
            
        Raises:
            ValueError: Se a conta não existe
        """
        # Verifica se a conta existe
        account = await self.account_repository.obter_conta(conta_id)
        if not account:
            raise ValueError(f"Conta {conta_id} não encontrada")
        
        transacoes = await self.repository.obter_transacoes_conta(conta_id)
        return [self._to_response(t) for t in transacoes]
    
    def _to_response(self, transaction: Transaction) -> TransactionResponse:
        """Converte Transaction para TransactionResponse"""
        tipo = TransactionType.SAQUE if transaction.tipo == TipoTransacao.SAQUE else TransactionType.DEPOSITO
        
        return TransactionResponse(
            id=transaction.id,
            conta_id=transaction.conta_id,
            tipo=tipo,
            valor=transaction.valor,
            descricao=transaction.descricao,
            criada_em=transaction.criada_em
        )
