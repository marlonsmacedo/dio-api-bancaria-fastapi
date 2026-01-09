# Documentação da Implementação

## Visão Geral

Esta é uma API RESTful completa implementada com FastAPI que gerencia operações bancárias assíncronas. A aplicação foi desenvolvida seguindo as melhores práticas de arquitetura de software, incluindo separação de responsabilidades, padrões de design e segurança.

## Arquitetura

### Camadas da Aplicação

#### 1. **Camada de Apresentação (API)**
- **Localização**: `src/api/v1/endpoints/`
- **Responsabilidade**: Expor endpoints HTTP
- **Componentes**:
  - `auth.py`: Autenticação (login)
  - `accounts.py`: Gerenciamento de contas
  - `transactions.py`: Gerenciamento de transações

#### 2. **Camada de Negócio (Services)**
- **Localização**: `src/services/`
- **Responsabilidade**: Lógica de negócio e validações
- **Componentes**:
  - `account_service.py`: Serviço de contas
  - `transaction_service.py`: Serviço de transações

#### 3. **Camada de Dados (Repository)**
- **Localização**: `src/db/repository/`
- **Responsabilidade**: Acesso e manipulação de dados
- **Componentes**:
  - `account_repository.py`: CRUD de contas
  - `transaction_repository.py`: CRUD de transações

#### 4. **Modelos de Dados**
- **Localização**: `src/db/models/`
- **Responsabilidade**: Definição das entidades
- **Componentes**:
  - `account.py`: Modelo de Conta
  - `transaction.py`: Modelo de Transação

#### 5. **Validação de Dados (Schemas)**
- **Localização**: `src/schemas/`
- **Responsabilidade**: Validação de entrada/saída
- **Componentes**:
  - `account.py`: Schemas de conta
  - `transaction.py`: Schemas de transação
  - `auth.py`: Schemas de autenticação

#### 6. **Segurança (Core)**
- **Localização**: `src/core/`
- **Responsabilidade**: Autenticação e criptografia
- **Componentes**:
  - `security.py`: JWT e hashing
  - `config.py`: Configurações da aplicação

## Fluxo de Requisição

```
Requisição HTTP
    ↓
Endpoint (api/v1/endpoints/*.py)
    ↓
Schema Validation (schemas/*.py)
    ↓
Service Logic (services/*.py)
    ↓
Repository CRUD (db/repository/*.py)
    ↓
Database (db/session.py - em memória)
    ↓
Response JSON
```

## Padrões Implementados

### 1. Dependency Injection
```python
# Em dependencies.py
async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Valida o token JWT"""
    
# Uso em endpoints
async def criar_conta(
    account_data: AccountCreate,
    current_user: str = Depends(get_current_user)
):
```

### 2. Repository Pattern
```python
# Abstração de acesso a dados
class AccountRepository:
    async def criar_conta(self, account: Account)
    async def obter_conta(self, conta_id: int)
    async def atualizar_conta(self, account: Account)
```

### 3. Service Layer
```python
# Lógica de negócio isolada
class AccountService:
    def __init__(self):
        self.repository = AccountRepository()
    
    async def criar_conta(self, account_data: AccountCreate)
```

### 4. Async/Await
```python
# Operações assíncronas
async def depositar(...):
    transaction = await transaction_service.criar_transacao(...)
    return transaction
```

## Segurança Implementada

### Autenticação JWT
- **Algoritmo**: HS256
- **Expiração**: 24 horas
- **Implementação**: `core/security.py`

```python
def create_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT com expiração"""
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[str]:
    """Verifica e decodifica token JWT"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
```

### Hashing de Senha
- **Algoritmo**: bcrypt
- **Contexto**: passlib

```python
def criar_hash_senha(senha: str) -> str:
    """Cria hash bcrypt da senha"""
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return pwd_context.verify(senha, hash_senha)
```

### Validação de Dados
- **Framework**: Pydantic
- **Localização**: `src/schemas/`

```python
class AccountCreate(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    titular: str = Field(..., min_length=3, max_length=100)
    saldo_inicial: float = Field(default=0.0, ge=0)
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf(cls, v):
        if not v.isdigit():
            raise ValueError('CPF deve conter apenas dígitos')
        return v
```

## Validações de Negócio

### Conta
- ✓ CPF único por conta
- ✓ Nome do titular validado (letras e espaços)
- ✓ Saldo inicial não pode ser negativo

### Transação
- ✓ Valor sempre positivo
- ✓ Saque não pode exceder saldo disponível
- ✓ Valores negativos são rejeitados
- ✓ Conta deve existir antes de transacionar
- ✓ Saldo é atualizado automaticamente

## Banco de Dados

### Armazenamento em Memória
Para simplificar o desafio, o banco de dados foi implementado em memória usando dicionários Python:

```python
class DatabaseManager:
    def __init__(self):
        self.contas = {}        # ID -> Account
        self.transacoes = {}    # ID -> Transaction
        self.conta_counter = 1
        self.transacao_counter = 1
```

### Migrando para Banco de Dados Real
Para usar um banco de dados real (PostgreSQL, MySQL, MongoDB):

1. Instale SQLAlchemy: `pip install sqlalchemy`
2. Configure a conexão em `db/session.py`
3. Use modelos SQLAlchemy ao invés de dataclasses
4. Atualize os repositórios para usar Sessions SQLAlchemy

## Testes

### Estrutura de Testes
```
src/tests/
├── conftest.py              # Fixtures e configuração
├── test_auth.py             # Testes de autenticação
├── test_accounts.py         # Testes de contas
└── test_transactions.py     # Testes de transações
```

### Tipos de Teste Implementados

#### Testes de Autenticação (`test_auth.py`)
- Login bem-sucedido
- CPF inválido
- Credenciais inválidas
- Dados faltando

#### Testes de Contas (`test_accounts.py`)
- Criar conta com sucesso
- Verificar autenticação obrigatória
- Evitar CPF duplicado
- Obter conta existente
- Conta não encontrada
- Listar contas

#### Testes de Transações (`test_transactions.py`)
- Depósito bem-sucedido
- Valor negativo rejeitado
- Saque bem-sucedido
- Saldo insuficiente rejeitado
- Obter extrato
- Conta inexistente
- Autenticação obrigatória

### Executar Testes
```bash
# Todos os testes
pytest src/tests/ -v

# Com cobertura
pytest src/tests/ --cov=src --cov-report=html

# Teste específico
pytest src/tests/test_auth.py::TestAuth::test_login_success -v
```

## Documentação OpenAPI

A API gera automaticamente documentação OpenAPI:

### Swagger UI
- **URL**: `http://localhost:8000/docs`
- **Funcionalidades**: 
  - Testar endpoints interativamente
  - Ver modelos e schemas
  - Visualizar respostas de exemplo

### ReDoc
- **URL**: `http://localhost:8000/redoc`
- **Funcionalidades**:
  - Documentação mais limpa
  - Melhor legibilidade
  - Navegação por seções

## Configuração

### Variáveis de Ambiente (`.env`)
```
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
DEBUG=True
```

### Arquivo `conftest.py`
Define fixtures e configuração do pytest:
- Reset do banco de dados antes de cada teste
- Importação correta de módulos

## Performance

### Características Assíncronas
- Endpoints implementados com `async/await`
- Operações não-bloqueantes
- Suporta múltiplas requisições simultâneas

### Middleware
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Extensibilidade

### Como Adicionar um Novo Endpoint

1. **Criar o modelo** (`src/db/models/novo.py`)
```python
@dataclass
class Novo:
    id: int
    dados: str
```

2. **Criar o schema** (`src/schemas/novo.py`)
```python
class NovoCreate(BaseModel):
    dados: str
```

3. **Criar o repositório** (`src/db/repository/novo_repository.py`)
```python
class NovoRepository:
    async def criar(self, obj: Novo)
```

4. **Criar o serviço** (`src/services/novo_service.py`)
```python
class NovoService:
    async def criar(self, data: NovoCreate)
```

5. **Criar o endpoint** (`src/api/v1/endpoints/novo.py`)
```python
@router.post("/novo", response_model=NovoResponse)
async def criar_novo(data: NovoCreate, current_user = Depends(get_current_user)):
    return await novo_service.criar(data)
```

6. **Incluir no agregador** (`src/api/v1/api.py`)
```python
router.include_router(novo.router, tags=["Novo"])
```

## Tratamento de Erros

### Códigos HTTP Utilizados
- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `400 Bad Request`: Validação falhou
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Sem autenticação
- `404 Not Found`: Recurso não existe
- `422 Unprocessable Entity`: Erro de validação Pydantic

### Exemplo de Tratamento
```python
try:
    account = await account_service.criar_conta(account_data)
    return account
except ValueError as e:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
    )
```

## Checklist de Requisitos

✅ **Cadastro de Transações**: Implementado (depósitos e saques)
✅ **Exibição de Extrato**: Implementado (GET /transacoes/extrato/{conta_id})
✅ **Autenticação com JWT**: Implementado (POST /auth/login)
✅ **FastAPI**: Utilizado como framework principal
✅ **Modelagem de Dados**: Contas e transações relacionadas
✅ **Validação de Operações**: Valores positivos, saldo suficiente, CPF único
✅ **Segurança**: JWT, hashing de senha, CORS
✅ **Documentação OpenAPI**: Swagger UI e ReDoc ativados

## Conclusão

Esta implementação fornece uma base sólida para uma API bancária moderna, escalável e segura. Pode ser facilmente estendida com mais funcionalidades e integrada com um banco de dados real.
