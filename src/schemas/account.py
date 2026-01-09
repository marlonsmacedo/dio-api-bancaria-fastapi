"""Schemas de validação para contas"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class AccountCreate(BaseModel):
    """Schema para criação de conta"""
    cpf: str = Field(..., min_length=11, max_length=11, description="CPF do titular (11 dígitos)")
    titular: str = Field(..., min_length=3, max_length=100, description="Nome completo do titular")
    saldo_inicial: float = Field(default=0.0, ge=0, description="Saldo inicial da conta")
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf(cls, v):
        """Valida o formato do CPF"""
        if not v.isdigit():
            raise ValueError('CPF deve conter apenas dígitos')
        return v
    
    @field_validator('titular')
    @classmethod
    def validar_titular(cls, v):
        """Valida o nome do titular"""
        if not v.isalpha() and ' ' not in v:
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v


class AccountResponse(BaseModel):
    """Schema de resposta para conta"""
    id: int = Field(..., description="ID único da conta")
    cpf: str = Field(..., description="CPF do titular")
    titular: str = Field(..., description="Nome do titular")
    saldo: float = Field(..., description="Saldo atual da conta")
    criada_em: datetime = Field(..., description="Data de criação da conta")
    atualizada_em: datetime = Field(..., description="Data da última atualização")
    
    class Config:
        """Configuração do schema"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "cpf": "12345678900",
                "titular": "João Silva",
                "saldo": 1000.00,
                "criada_em": "2024-01-08T10:30:00",
                "atualizada_em": "2024-01-08T10:30:00"
            }
        }
