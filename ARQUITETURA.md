# Diagrama da Arquitetura

## Fluxo de Requisição

```
┌──────────────────────────────────────────────────────────────────┐
│                       CLIENTE HTTP                               │
│              (Browser, cURL, Postman, etc)                       │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTP Request
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                        │
│                    src/api/v1/endpoints/                         │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  auth.py    │  │ accounts.py  │  │ transactions.py      │   │
│  │             │  │              │  │                      │   │
│  │ POST /login │  │ POST /       │  │ POST /depositar      │   │
│  │             │  │ GET /{id}    │  │ POST /sacar          │   │
│  │             │  │ GET /        │  │ GET /extrato/{id}    │   │
│  └────────┬────┘  └──────┬───────┘  └──────────┬───────────┘   │
└───────────┼───────────────┼──────────────────────┼───────────────┘
            │               │                      │
            │ Valida        │ Valida               │ Valida
            │ schema        │ schema               │ schema
            ▼               ▼                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CAMADA DE VALIDAÇÃO                           │
│                    src/schemas/                                  │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  auth.py    │  │ account.py   │  │ transaction.py       │   │
│  │             │  │              │  │                      │   │
│  │ LoginRequest│  │AccountCreate │  │TransactionCreate     │   │
│  │TokenResponse│  │AccountResponse  │TransactionResponse   │   │
│  └────────┬────┘  └──────┬───────┘  └──────────┬───────────┘   │
└───────────┼───────────────┼──────────────────────┼───────────────┘
            │               │                      │
            │ Pydantic      │ Pydantic            │ Pydantic
            │ Validation    │ Validation          │ Validation
            ▼               ▼                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                  CAMADA DE LÓGICA DE NEGÓCIO                     │
│                    src/services/                                 │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │ account_service.py   │  │  transaction_service.py          │ │
│  │                      │  │                                  │ │
│  │ criar_conta()        │  │ criar_transacao()                │ │
│  │ obter_conta()        │  │ obter_transacoes_conta()         │ │
│  │ atualizar_saldo()    │  │ validar saldo, valor positivo    │ │
│  │ listar_contas()      │  │ atualizar saldo da conta         │ │
│  └──────────┬───────────┘  └──────────┬──────────────────────┘ │
└─────────────┼────────────────────────┼──────────────────────────┘
              │                        │
              │ Repository Pattern     │
              ▼                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                   CAMADA DE ACESSO A DADOS                       │
│                 src/db/repository/                               │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │account_repository.py │  │ transaction_repository.py        │ │
│  │                      │  │                                  │ │
│  │ criar_conta()        │  │ criar_transacao()                │ │
│  │ obter_conta()        │  │ obter_transacao()                │ │
│  │ obter_conta_por_cpf()│  │ obter_transacoes_conta()         │ │
│  │ atualizar_conta()    │  │ listar_transacoes()              │ │
│  │ listar_contas()      │  │                                  │ │
│  │ deletar_conta()      │  │                                  │ │
│  └──────────┬───────────┘  └──────────┬──────────────────────┘ │
└─────────────┼────────────────────────┼──────────────────────────┘
              │                        │
              │ CRUD Operations        │
              ▼                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CAMADA DE PERSISTÊNCIA                        │
│                     src/db/                                      │
├──────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  DatabaseManager                        │   │
│  │                  (Em memória)                           │   │
│  │                                                        │   │
│  │  self.contas = {}        (ID -> Account)              │   │
│  │  self.transacoes = {}    (ID -> Transaction)          │   │
│  │                                                        │   │
│  │  models/                                              │   │
│  │  ├── account.py (Account dataclass)                  │   │
│  │  └── transaction.py (Transaction dataclass)          │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ HTTP Response
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                       CLIENTE HTTP                               │
│                      (Resposta JSON)                             │
└──────────────────────────────────────────────────────────────────┘
```

## Autenticação e Segurança

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENTE ENVIA REQUISIÇÃO                  │
│                  /api/v1/auth/login + CPF/Senha              │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│            VALIDAR CREDENCIAIS (Simulado)                    │
│         CPF: 12345678900 | Senha: senha123                  │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                   CRIAR TOKEN JWT                            │
│        core/security.py :: create_token()                    │
│                                                              │
│  Payload: {                                                  │
│    "sub": "12345678900",  (user_id)                         │
│    "exp": 1704854400      (expira em 24h)                   │
│  }                                                           │
│                                                              │
│  Assinado com: HS256 + SECRET_KEY                           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│          RETORNAR TOKEN AO CLIENTE                           │
│                                                              │
│  {                                                           │
│    "access_token": "eyJhbGc...",                            │
│    "token_type": "bearer"                                   │
│  }                                                           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│        CLIENTE ENVIA REQUISIÇÃO COM TOKEN                    │
│                                                              │
│  GET /api/v1/contas/1                                       │
│  Authorization: Bearer eyJhbGc...                           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│        VALIDAR TOKEN (api/dependencies.py)                   │
│     core/security.py :: verify_token()                       │
│                                                              │
│  1. Decodificar JWT                                          │
│  2. Verificar assinatura                                     │
│  3. Verificar expiração                                      │
│  4. Extrair user_id do payload                              │
└───────────────────────────┬──────────────────────────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                  ✓ Válido    ✗ Inválido/Expirado
                     │             │
                     ▼             ▼
            ┌────────────────┐  ┌──────────────────┐
            │ Executar       │  │ Retornar erro 401│
            │ endpoint       │  │ "Token inválido  │
            │                │  │  ou expirado"    │
            └────────────────┘  └──────────────────┘
```

## Fluxo de Transação (Depósito/Saque)

```
┌─────────────────────────────────────────────────────────────────┐
│              CLIENTE ENVIA REQUISIÇÃO                           │
│                                                                 │
│  POST /api/v1/transacoes/depositar                             │
│  {                                                              │
│    "conta_id": 1,                                              │
│    "valor": 500.00,                                            │
│    "descricao": "Depósito de salário"                          │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            VALIDAR TOKEN JWT (Autenticação)                     │
│                          │                                      │
│                    ┌─────┴─────┐                               │
│               ✓ Válido    ✗ Inválido                          │
│                     │          │                               │
└─────────────────────┼──────────┼──────────────────────────────┘
                      ▼          ▼
              ┌─────────────┐  ┌──────────┐
              │ Continuar   │  │ Retornar │
              │             │  │ erro 403 │
              └──────┬──────┘  └──────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          VALIDAR SCHEMA PYDANTIC                                │
│    schemas/transaction.py :: TransactionCreate                  │
│                                                                 │
│  ✓ conta_id > 0                                                │
│  ✓ valor > 0                                                   │
│  ✓ descricao <= 200 caracteres                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    ┌────┴────┐
            ✓ Válido      ✗ Inválido
                   │          │
        ┌──────────┘          └────────────┐
        │                                  │
        ▼                                  ▼
┌────────────────────┐            ┌──────────────────┐
│ Continuar          │            │ Retornar erro 422│
│                    │            │ (Validação)      │
└────────┬───────────┘            └──────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│        OBTER CONTA (account_repository)                         │
│                                                                 │
│  account = await repository.obter_conta(conta_id)              │
│                          │                                      │
│                    ┌─────┴─────┐                               │
│             ✓ Existe    ✗ Não existe                          │
│                   │          │                                 │
└───────────────────┼──────────┼─────────────────────────────────┘
                    ▼          ▼
           ┌──────────────┐  ┌──────────────────┐
           │ Continuar    │  │ Retornar erro 404│
           │              │  │ "Conta não existe│
           └───────┬──────┘  └──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│          VERIFICAR TIPO DE TRANSAÇÃO                            │
│                                                                 │
│  if tipo == DEPOSITO:                                          │
│      novo_saldo = saldo + valor                                │
│  elif tipo == SAQUE:                                           │
│      if saldo < valor:                                         │
│          ✗ Erro: Saldo insuficiente                            │
│      novo_saldo = saldo - valor                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    ┌────┴────┐
              ✓ OK      ✗ Erro
                │           │
        ┌───────┘           └──────────┐
        │                              │
        ▼                              ▼
┌─────────────────────┐        ┌──────────────────┐
│ Atualizar saldo    │        │ Retornar erro 400│
│                    │        │ "Saldo insuficien│
└──────────┬─────────┘        └──────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│      REGISTRAR TRANSAÇÃO                                        │
│                                                                 │
│  Transaction(                                                   │
│      id=novo_id,                                               │
│      conta_id=1,                                               │
│      tipo="deposito",                                          │
│      valor=500.00,                                             │
│      descricao="Depósito de salário",                          │
│      criada_em=datetime.utcnow()                               │
│  )                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│      RETORNAR RESPOSTA DE SUCESSO (201)                        │
│                                                                 │
│  {                                                              │
│    "id": 1,                                                    │
│    "conta_id": 1,                                              │
│    "tipo": "deposito",                                         │
│    "valor": 500.00,                                            │
│    "descricao": "Depósito de salário",                         │
│    "criada_em": "2024-01-08T10:30:00"                         │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Estrutura de Dados em Memória

```
DatabaseManager
│
├─ contas: Dict[int, Account]
│  │
│  ├─ 1 → Account(
│  │      id=1,
│  │      cpf="12345678901",
│  │      titular="João Silva",
│  │      saldo=1500.00,
│  │      criada_em=datetime(...),
│  │      atualizada_em=datetime(...)
│  │    )
│  │
│  └─ 2 → Account(...)
│
├─ transacoes: Dict[int, Transaction]
│  │
│  ├─ 1 → Transaction(
│  │      id=1,
│  │      conta_id=1,
│  │      tipo=TipoTransacao.DEPOSITO,
│  │      valor=500.00,
│  │      descricao="Depósito de salário",
│  │      criada_em=datetime(...)
│  │    )
│  │
│  ├─ 2 → Transaction(
│  │      id=2,
│  │      conta_id=1,
│  │      tipo=TipoTransacao.SAQUE,
│  │      valor=100.00,
│  │      descricao="Saque no caixa",
│  │      criada_em=datetime(...)
│  │    )
│  │
│  └─ 3 → Transaction(...)
│
├─ conta_counter: int = 3 (próximo ID de conta)
└─ transacao_counter: int = 4 (próximo ID de transação)
```

## Dependências Entre Camadas

```
                    ┌─────────────────────┐
                    │   CLIENTE HTTP      │
                    │  (Browser, cURL)    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    ENDPOINTS        │
                    │  (api.v1.endpoints) │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
         ┌──────────────┐ ┌──────────┐ ┌────────────────┐
         │ SCHEMAS      │ │SERVICES  │ │ DEPENDENCIES   │
         │(validação)   │ │(negócio) │ │(autenticação)  │
         └──────┬───────┘ └────┬─────┘ └────────┬───────┘
                │              │                │
                │         ┌────┴────┐           │
                │         │          │          │
                │         ▼          ▼          ▼
                │      ┌────────────────────────────┐
                │      │    REPOSITORIES            │
                │      │ (CRUD, acesso dados)       │
                │      └────────────┬───────────────┘
                │                   │
                └───────────────────┼──────────────┐
                                    │              │
                                    ▼              ▼
                          ┌──────────────────┐ ┌──────────┐
                          │  MODELS          │ │ SECURITY │
                          │(Account, Trans.) │ │(JWT, pwd)│
                          └──────────────────┘ └──────────┘
                                    │
                                    ▼
                          ┌──────────────────────┐
                          │    BANCO DE DADOS    │
                          │  (Em memória)        │
                          └──────────────────────┘
```

---

**Visualização completa da arquitetura da API Bancária**
