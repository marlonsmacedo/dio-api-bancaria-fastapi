"""Repositório de transações bancárias"""
from typing import Optional, List
from db.models.transaction import Transaction
from db.session import db


class TransactionRepository:
    """Repositório para operações de transação"""
    
    async def criar_transacao(self, transaction: Transaction) -> Transaction:
        """Cria uma nova transação"""
        db.transacoes[transaction.id] = transaction
        return transaction
    
    async def obter_transacao(self, transacao_id: int) -> Optional[Transaction]:
        """Obtém uma transação pelo ID"""
        return db.transacoes.get(transacao_id)
    
    async def obter_transacoes_conta(self, conta_id: int) -> List[Transaction]:
        """Obtém todas as transações de uma conta"""
        transacoes = []
        for transacao in db.transacoes.values():
            if transacao.conta_id == conta_id:
                transacoes.append(transacao)
        # Ordena por data de criação (mais recentes primeiro)
        return sorted(transacoes, key=lambda x: x.criada_em, reverse=True)
    
    async def listar_transacoes(self) -> List[Transaction]:
        """Lista todas as transações"""
        return list(db.transacoes.values())
