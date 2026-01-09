"""Agregador de routers da API v1"""
from fastapi import APIRouter
from api.v1.endpoints import auth, accounts, transactions

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, tags=["Autenticação"])
router.include_router(accounts.router, tags=["Contas"])
router.include_router(transactions.router, tags=["Transações"])
