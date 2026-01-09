"""Endpoints de transações bancárias"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from schemas.transaction import TransactionCreate, TransactionResponse, TransactionType
from services.transaction_service import TransactionService
from api.dependencies import get_current_user

router = APIRouter(prefix="/transacoes")
transaction_service = TransactionService()


@router.post("/depositar", response_model=TransactionResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Realizar depósito", description="Realiza um depósito em uma conta")
async def depositar(
    transaction_data: TransactionCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Realiza um depósito em uma conta.
    
    - **conta_id**: ID da conta
    - **valor**: Valor do depósito (deve ser positivo)
    - **descricao**: Descrição opcional do depósito
    """
    try:
        transaction = await transaction_service.criar_transacao(
            conta_id=transaction_data.conta_id,
            tipo=TransactionType.DEPOSITO,
            valor=transaction_data.valor,
            descricao=transaction_data.descricao
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/sacar", response_model=TransactionResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Realizar saque", description="Realiza um saque em uma conta")
async def sacar(
    transaction_data: TransactionCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Realiza um saque em uma conta.
    
    - **conta_id**: ID da conta
    - **valor**: Valor do saque (deve ser positivo)
    - **descricao**: Descrição opcional do saque
    """
    try:
        transaction = await transaction_service.criar_transacao(
            conta_id=transaction_data.conta_id,
            tipo=TransactionType.SAQUE,
            valor=transaction_data.valor,
            descricao=transaction_data.descricao
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/extrato/{conta_id}", response_model=List[TransactionResponse],
            summary="Obter extrato", 
            description="Retorna todas as transações de uma conta")
async def obter_extrato(
    conta_id: int,
    current_user: str = Depends(get_current_user)
):
    """
    Obtém o extrato de uma conta (todas as transações).
    
    - **conta_id**: ID da conta
    """
    try:
        transacoes = await transaction_service.obter_transacoes_conta(conta_id)
        return transacoes
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
