"""Endpoints de autenticação"""
from fastapi import APIRouter, HTTPException, status
from schemas.auth import LoginRequest, TokenResponse
from core.security import create_token

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=TokenResponse, summary="Fazer login", 
             description="Autentica um usuário e retorna um token JWT")
async def login(login_data: LoginRequest):
    """
    Endpoint para autenticação de usuários.
    
    - **cpf**: CPF do usuário
    - **senha**: Senha do usuário
    
    Retorna um token JWT válido por 24 horas.
    """
    # Simulação simples de autenticação
    # Em produção, você verificaria no banco de dados
    if login_data.cpf == "12345678900" and login_data.senha == "senha123":
        token = create_token(user_id=login_data.cpf)
        return TokenResponse(access_token=token, token_type="bearer")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="CPF ou senha inválidos"
    )
