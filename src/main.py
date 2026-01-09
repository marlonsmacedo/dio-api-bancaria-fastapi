"""
API Bancária Assíncrona com FastAPI

API RESTful para gerenciar operações bancárias de depósitos e saques
vinculadas a contas correntes, com autenticação JWT.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from core.config import (
    CORS_ORIGINS,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION
)
from api.v1.api import router as api_v1_router

# Criar aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_v1_router)


@app.get("/", tags=["Health Check"])
async def root():
    """
    Endpoint raiz da API
    
    Retorna informações sobre a API.
    """
    return {
        "title": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "status": "online"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint
    
    Verifica se a API está funcionando corretamente.
    """
    return {"status": "healthy"}


def custom_openapi():
    """Customiza a documentação OpenAPI"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )