"""Configurações da aplicação"""
from datetime import timedelta
from typing import Optional

# JWT Configuration
SECRET_KEY = "sua-chave-secreta-muito-segura-mude-isso-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_HOURS * 60

# Banco de dados (simulado com dicionários em memória)
DATABASE_URL = "sqlite:///./test.db"

# CORS
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

# API Info
API_TITLE = "API Bancária"
API_DESCRIPTION = "API RESTful assíncrona para gerenciar operações bancárias"
API_VERSION = "1.0.0"
