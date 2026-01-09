"""Modelo de transação bancária"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TipoTransacao(str, Enum):
    """Tipos de transação"""
    DEPOSITO = "deposito"
    SAQUE = "saque"


@dataclass
class Transaction:
    """Modelo de dados para uma transação bancária"""
    id: int
    conta_id: int
    tipo: TipoTransacao
    valor: float
    descricao: str = ""
    criada_em: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self):
        """Converte a transação para dicionário"""
        return {
            "id": self.id,
            "conta_id": self.conta_id,
            "tipo": self.tipo.value,
            "valor": self.valor,
            "descricao": self.descricao,
            "criada_em": self.criada_em.isoformat()
        }
