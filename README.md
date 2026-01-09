# API Bancária Assíncrona com FastAPI

Uma API RESTful assíncrona completa para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Desenvolvida com FastAPI, implementa autenticação JWT e segue práticas recomendadas de design de APIs.

## 🎯 Funcionalidades

### ✅ Autenticação
- **JWT (JSON Web Tokens)**: Autenticação segura de usuários
- **Endpoints protegidos**: Apenas usuários autenticados podem acessar recursos
- **Token com expiração**: Tokens JWT com 24 horas de validade

### 💳 Gerenciamento de Contas
- **Cadastro de contas**: Criar novas contas bancárias
- **Listagem de contas**: Visualizar todas as contas cadastradas
- **Consulta de conta**: Obter detalhes de uma conta específica
- **Validação de CPF**: Garante CPF único por conta

### 💰 Transações Bancárias
- **Depósitos**: Adicionar fundos à conta
- **Saques**: Remover fundos da conta
- **Validação**: 
  - ✗ Valores negativos não são permitidos
  - ✗ Saques sem saldo insuficiente são rejeitados
  - ✓ Valores positivos obrigatórios
- **Extrato**: Visualizar todas as transações de uma conta

### 📚 Documentação
- **OpenAPI/Swagger**: Documentação interativa em `/docs`
- **ReDoc**: Documentação alternativa em `/redoc`
- **Descrições detalhadas**: Cada endpoint tem documentação clara

## 📁 Estrutura do Projeto

```
src/
├── main.py                          # Ponto de entrada da FastAPI
├── api/
│   ├── dependencies.py              # Dependências compartilhadas (autenticação)
│   └── v1/
│       ├── api.py                   # Agregador de routers
│       └── endpoints/
│           ├── auth.py              # Endpoints de autenticação
│           ├── accounts.py          # Endpoints de contas
│           └── transactions.py      # Endpoints de transações
├── core/
│   ├── config.py                    # Configurações da aplicação
│   └── security.py                  # Funções de JWT e hashing
├── db/
│   ├── session.py                   # Gerenciador de banco de dados
│   ├── models/
│   │   ├── account.py               # Modelo Account
│   │   └── transaction.py           # Modelo Transaction
│   └── repository/
│       ├── account_repository.py    # CRUD de contas
│       └── transaction_repository.py # CRUD de transações
├── schemas/
│   ├── account.py                   # Validação de contas
│   ├── transaction.py               # Validação de transações
│   └── auth.py                      # Validação de autenticação
├── services/
│   ├── account_service.py           # Lógica de negócio de contas
│   └── transaction_service.py       # Lógica de negócio de transações
└── tests/
    ├── test_auth.py                 # Testes de autenticação
    ├── test_accounts.py             # Testes de contas
    └── test_transactions.py         # Testes de transações
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.9+
- pip ou poetry

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a API
```bash
cd src
python -m uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### 3. Acessar documentação
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 Endpoints da API

### Autenticação

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "cpf": "12345678900",
    "senha": "senha123"
}
```

**Resposta (201):**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Contas

#### Criar conta
```http
POST /api/v1/contas/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "98765432100",
    "titular": "Maria Silva",
    "saldo_inicial": 1000.00
}
```

**Resposta (201):**
```json
{
    "id": 1,
    "cpf": "98765432100",
    "titular": "Maria Silva",
    "saldo": 1000.00,
    "criada_em": "2024-01-08T10:30:00",
    "atualizada_em": "2024-01-08T10:30:00"
}
```

#### Obter conta
```http
GET /api/v1/contas/{conta_id}
Authorization: Bearer {token}
```

#### Listar todas as contas
```http
GET /api/v1/contas/
Authorization: Bearer {token}
```

### Transações

#### Realizar depósito
```http
POST /api/v1/transacoes/depositar
Authorization: Bearer {token}
Content-Type: application/json

{
    "conta_id": 1,
    "valor": 500.00,
    "descricao": "Depósito de salário"
}
```

**Resposta (201):**
```json
{
    "id": 1,
    "conta_id": 1,
    "tipo": "deposito",
    "valor": 500.00,
    "descricao": "Depósito de salário",
    "criada_em": "2024-01-08T10:35:00"
}
```

#### Realizar saque
```http
POST /api/v1/transacoes/sacar
Authorization: Bearer {token}
Content-Type: application/json

{
    "conta_id": 1,
    "valor": 100.00,
    "descricao": "Saque no caixa"
}
```

#### Obter extrato
```http
GET /api/v1/transacoes/extrato/{conta_id}
Authorization: Bearer {token}
```

**Resposta (200):**
```json
[
    {
        "id": 2,
        "conta_id": 1,
        "tipo": "saque",
        "valor": 100.00,
        "descricao": "Saque no caixa",
        "criada_em": "2024-01-08T10:40:00"
    },
    {
        "id": 1,
        "conta_id": 1,
        "tipo": "deposito",
        "valor": 500.00,
        "descricao": "Depósito de salário",
        "criada_em": "2024-01-08T10:35:00"
    }
]
```

## 🧪 Testes

Executar todos os testes:
```bash
pytest src/tests/ -v
```

Executar testes específicos:
```bash
# Testes de autenticação
pytest src/tests/test_auth.py -v

# Testes de contas
pytest src/tests/test_accounts.py -v

# Testes de transações
pytest src/tests/test_transactions.py -v
```

Com cobertura:
```bash
pytest src/tests/ --cov=src --cov-report=html
```

## 🔐 Segurança

### Autenticação JWT
- Implementa JWT com algoritmo HS256
- Tokens expiram em 24 horas
- Dependência de autenticação em todos os endpoints que exigem

### Validação de Dados
- Pydantic para validação automática
- CPF validado e único por conta
- Valores de transação sempre positivos
- Saldo insuficiente é verificado antes de saques

### Hashing de Senha
- Usa bcrypt para hash seguro de senhas
- Implementado no módulo de segurança

## 🎨 Recursos do FastAPI

### Assincronismo
- Todos os endpoints são async
- Operações de I/O não bloqueantes
- Melhor performance e escalabilidade

### Documentação Automática
- OpenAPI 3.0 completo
- Swagger UI em `/docs`
- ReDoc em `/redoc`
- Exemplos em cada schema

### Validação Automática
- Pydantic models para validação
- Erros informativos (422 Unprocessable Entity)
- Conversão automática de tipos

## 📝 Dados de Teste

### Credenciais para login
```
CPF: 12345678900
Senha: senha123
```

Você pode criar novas contas e realizar transações após fazer login.

## 🛠️ Desenvolvimento

### Padrões Utilizados
- **Layered Architecture**: Separação clara entre camadas
- **Repository Pattern**: Abstração de acesso a dados
- **Service Layer**: Lógica de negócio isolada
- **Dependency Injection**: Via FastAPI Depends
- **OpenAPI-First**: Documentação como parte do código

### Extensões Futuras
- [ ] Integração com banco de dados real (PostgreSQL/MongoDB)
- [ ] Autenticação com múltiplos tipos de usuário (Admin, User)
- [ ] Sistemas de limite de transação
- [ ] Auditoria e logs detalhados
- [ ] Paginação para listagens
- [ ] Filtros e busca avançada
- [ ] Integração com serviços de pagamento
- [ ] Rate limiting
- [ ] Cache com Redis

## 📄 Licença

Este projeto é fornecido como material de aprendizado da DIO.

## 👨‍💻 Autor

Desenvolvido como desafio de API Bancária com FastAPI - DIO (Digital Innovation One)
