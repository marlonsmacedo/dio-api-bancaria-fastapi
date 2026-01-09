# 📍 Referência Rápida de Endpoints

## Base URL
```
http://localhost:8000
```

## Documentação Interativa
```
GET http://localhost:8000/docs              # Swagger UI
GET http://localhost:8000/redoc             # ReDoc
GET http://localhost:8000/openapi.json      # OpenAPI Schema
```

## Health Check
```
GET http://localhost:8000/                  # Info da API
GET http://localhost:8000/health            # Status
```

---

## 🔐 Autenticação

### Login
```http
POST /api/v1/auth/login

{
  "cpf": "12345678900",
  "senha": "senha123"
}

Resposta 200:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## 💳 Contas

### Criar Conta
```http
POST /api/v1/contas/
Authorization: Bearer {token}

{
  "cpf": "12345678901",
  "titular": "Maria Silva",
  "saldo_inicial": 1000.00
}

Resposta 201:
{
  "id": 1,
  "cpf": "12345678901",
  "titular": "Maria Silva",
  "saldo": 1000.00,
  "criada_em": "2024-01-08T10:30:00",
  "atualizada_em": "2024-01-08T10:30:00"
}
```

### Obter Conta
```http
GET /api/v1/contas/{conta_id}
Authorization: Bearer {token}

Exemplo: GET /api/v1/contas/1

Resposta 200:
{
  "id": 1,
  "cpf": "12345678901",
  "titular": "Maria Silva",
  "saldo": 1000.00,
  "criada_em": "2024-01-08T10:30:00",
  "atualizada_em": "2024-01-08T10:30:00"
}
```

### Listar Contas
```http
GET /api/v1/contas/
Authorization: Bearer {token}

Resposta 200:
[
  {
    "id": 1,
    "cpf": "12345678901",
    "titular": "Maria Silva",
    "saldo": 1000.00,
    "criada_em": "2024-01-08T10:30:00",
    "atualizada_em": "2024-01-08T10:30:00"
  },
  ...
]
```

---

## 💰 Transações

### Realizar Depósito
```http
POST /api/v1/transacoes/depositar
Authorization: Bearer {token}

{
  "conta_id": 1,
  "valor": 500.00,
  "descricao": "Depósito de salário"
}

Resposta 201:
{
  "id": 1,
  "conta_id": 1,
  "tipo": "deposito",
  "valor": 500.00,
  "descricao": "Depósito de salário",
  "criada_em": "2024-01-08T10:35:00"
}
```

### Realizar Saque
```http
POST /api/v1/transacoes/sacar
Authorization: Bearer {token}

{
  "conta_id": 1,
  "valor": 100.00,
  "descricao": "Saque no caixa"
}

Resposta 201:
{
  "id": 2,
  "conta_id": 1,
  "tipo": "saque",
  "valor": 100.00,
  "descricao": "Saque no caixa",
  "criada_em": "2024-01-08T10:40:00"
}
```

### Obter Extrato
```http
GET /api/v1/transacoes/extrato/{conta_id}
Authorization: Bearer {token}

Exemplo: GET /api/v1/transacoes/extrato/1

Resposta 200:
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

---

## 🔍 Códigos de Status HTTP

| Status | Significado | Exemplo |
|--------|-------------|---------|
| 200 | OK | GET bem-sucedido |
| 201 | Created | POST bem-sucedido |
| 400 | Bad Request | Validação falhou |
| 401 | Unauthorized | Token inválido/faltando |
| 403 | Forbidden | Sem autenticação |
| 404 | Not Found | Recurso não existe |
| 422 | Unprocessable Entity | Erro Pydantic |

---

## 📋 Headers Necessários

### Autenticação
```
Authorization: Bearer {access_token}
```

### Content Type (para POST/PUT)
```
Content-Type: application/json
```

---

## 🧪 Teste com cURL

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678900","senha":"senha123"}'
```

### Criar Conta
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/v1/contas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "cpf":"12345678901",
    "titular":"Maria Silva",
    "saldo_inicial":1000.00
  }'
```

### Depositar
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/v1/transacoes/depositar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "conta_id":1,
    "valor":500.00,
    "descricao":"Depósito de salário"
  }'
```

### Sacar
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/v1/transacoes/sacar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "conta_id":1,
    "valor":100.00,
    "descricao":"Saque no caixa"
  }'
```

### Obter Extrato
```bash
TOKEN="seu_token_aqui"

curl -X GET http://localhost:8000/api/v1/transacoes/extrato/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Obter Conta
```bash
TOKEN="seu_token_aqui"

curl -X GET http://localhost:8000/api/v1/contas/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Listar Contas
```bash
TOKEN="seu_token_aqui"

curl -X GET http://localhost:8000/api/v1/contas/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Teste com Python

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    json={"cpf": "12345678900", "senha": "senha123"}
)
token = response.json()["access_token"]

# 2. Criar conta
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/v1/contas/",
    json={
        "cpf": "12345678901",
        "titular": "Maria Silva",
        "saldo_inicial": 1000.00
    },
    headers=headers
)
conta = response.json()

# 3. Fazer depósito
response = requests.post(
    f"{BASE_URL}/api/v1/transacoes/depositar",
    json={
        "conta_id": conta["id"],
        "valor": 500.00,
        "descricao": "Depósito"
    },
    headers=headers
)

# 4. Fazer saque
response = requests.post(
    f"{BASE_URL}/api/v1/transacoes/sacar",
    json={
        "conta_id": conta["id"],
        "valor": 100.00,
        "descricao": "Saque"
    },
    headers=headers
)

# 5. Obter extrato
response = requests.get(
    f"{BASE_URL}/api/v1/transacoes/extrato/{conta['id']}",
    headers=headers
)
extrato = response.json()
print(f"Extrato: {extrato}")
```

---

## 🔐 Credenciais Padrão

```
CPF: 12345678900
Senha: senha123
```

---

## 📊 Exemplo de Fluxo Completo

```
1. POST /api/v1/auth/login
   ↓ (retorna token)
   
2. POST /api/v1/contas/
   ↓ (cria conta com saldo 0)
   
3. POST /api/v1/transacoes/depositar
   ↓ (adiciona R$ 1000)
   
4. POST /api/v1/transacoes/sacar
   ↓ (remove R$ 200)
   
5. GET /api/v1/transacoes/extrato/{id}
   ↓ (mostra 2 transações: depósito + saque)
   
6. GET /api/v1/contas/{id}
   ↓ (mostra saldo final: R$ 800)
```

---

## ⚠️ Erros Comuns

### 403 Forbidden
```
Causa: Token faltando ou inválido
Solução: Faça login primeiro e inclua o token no header
```

### 404 Not Found
```
Causa: Conta não existe
Solução: Verifique o ID da conta ou crie uma nova
```

### 400 Bad Request
```
Causa: Saldo insuficiente ou validação falhou
Solução: Verifique o valor da transação e saldo
```

### 422 Unprocessable Entity
```
Causa: Validação Pydantic falhou
Solução: Verifique o formato dos dados enviados
```

---

## 📚 Links Úteis

- 📖 [README.md](README.md) - Guia principal
- 📖 [IMPLEMENTACAO.md](IMPLEMENTACAO.md) - Detalhes técnicos
- 📖 [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md) - Como executar
- 📖 [ARQUITETURA.md](ARQUITETURA.md) - Diagramas
- 🐍 [FastAPI Docs](https://fastapi.tiangolo.com/)

---

**Última Atualização**: 08 de Janeiro de 2026
**Versão da API**: 1.0.0
