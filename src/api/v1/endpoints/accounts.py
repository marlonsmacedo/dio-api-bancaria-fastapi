"""Endpoints de contas bancárias"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.account import AccountCreate, AccountResponse
from services.account_service import AccountService
from api.dependencies import get_current_user

router = APIRouter(prefix="/contas")
account_service = AccountService()


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED,
             summary="Criar nova conta", description="Cria uma nova conta bancária")
async def criar_conta(
    account_data: AccountCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Cria uma nova conta bancária.
    
    - **cpf**: CPF do titular (único)
    - **titular**: Nome completo do titular
    - **saldo_inicial**: Saldo inicial da conta (padrão: 0.0)
    """
    try:
        account = await account_service.criar_conta(account_data)
        return account
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{conta_id}", response_model=AccountResponse,
            summary="Obter conta", description="Retorna os dados de uma conta específica")
async def obter_conta(
    conta_id: int,
    current_user: str = Depends(get_current_user)
):
    """
    Obtém os dados de uma conta específica.
    
    - **conta_id**: ID da conta
    """
    account = await account_service.obter_conta(conta_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    return account


@router.get("/", response_model=List[AccountResponse],
            summary="Listar contas", description="Lista todas as contas bancárias")
async def listar_contas(current_user: str = Depends(get_current_user)):
    """Lista todas as contas cadastradas."""
    contas = await account_service.listar_contas()
    return contas
