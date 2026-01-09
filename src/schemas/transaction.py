"""Schemas de validação para transações"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Tipos de transação"""
    DEPOSITO = "deposito"
    SAQUE = "saque"


class TransactionCreate(BaseModel):
    """Schema para criação de transação"""
    conta_id: int = Field(..., gt=0, description="ID da conta")
    valor: float = Field(..., gt=0, description="Valor da transação (deve ser positivo)")
    descricao: str = Field(default="", max_length=200, description="Descrição da transação")
    
    class Config:
        """Configuração do schema"""
        json_schema_extra = {
            "example": {
                "conta_id": 1,
                "valor": 100.50,
                "descricao": "Depósito referente a salário"
            }
        }


class TransactionResponse(BaseModel):
    """Schema de resposta para transação"""
    id: int = Field(..., description="ID único da transação")
    conta_id: int = Field(..., description="ID da conta")
    tipo: TransactionType = Field(..., description="Tipo de transação (deposito ou saque)")
    valor: float = Field(..., description="Valor da transação")
    descricao: str = Field(..., description="Descrição da transação")
    criada_em: datetime = Field(..., description="Data e hora da transação")
    
    class Config:
        """Configuração do schema"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "conta_id": 1,
                "tipo": "deposito",
                "valor": 100.50,
                "descricao": "Depósito referente a salário",
                "criada_em": "2024-01-08T10:30:00"
            }
        }
