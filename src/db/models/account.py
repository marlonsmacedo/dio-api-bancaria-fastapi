"""Modelo de conta bancária"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Account:
    """Modelo de dados para uma conta bancária"""
    id: int
    cpf: str
    titular: str
    saldo: float
    criada_em: datetime = field(default_factory=datetime.utcnow)
    atualizada_em: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self):
        """Converte a conta para dicionário"""
        return {
            "id": self.id,
            "cpf": self.cpf,
            "titular": self.titular,
            "saldo": self.saldo,
            "criada_em": self.criada_em.isoformat(),
            "atualizada_em": self.atualizada_em.isoformat()
        }
