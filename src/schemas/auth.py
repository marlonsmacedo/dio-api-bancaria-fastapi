"""Schemas de validação para autenticação"""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    cpf: str = Field(..., min_length=11, max_length=11, description="CPF do usuário")
    senha: str = Field(..., min_length=6, description="Senha do usuário")
    
    class Config:
        """Configuração do schema"""
        json_schema_extra = {
            "example": {
                "cpf": "12345678900",
                "senha": "senha123"
            }
        }


class TokenResponse(BaseModel):
    """Schema para resposta de token"""
    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    
    class Config:
        """Configuração do schema"""
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
