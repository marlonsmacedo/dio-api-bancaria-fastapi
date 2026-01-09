# Guia de Execução e Testes

## ✅ Checklist de Requisitos Atendidos

- ✅ **Cadastro de Transações**: Endpoints POST `/api/v1/transacoes/depositar` e `/api/v1/transacoes/sacar`
- ✅ **Exibição de Extrato**: Endpoint GET `/api/v1/transacoes/extrato/{conta_id}`
- ✅ **Autenticação com JWT**: Implementado em `core/security.py` e `api/dependencies.py`
- ✅ **FastAPI**: Framework principal da aplicação
- ✅ **Modelagem de Dados**: Modelos em `db/models/` com relacionamento conta-transações
- ✅ **Validação de Operações**: 
  - Não permite depósitos/saques negativos
  - Valida saldo para saques
  - Valida CPF único
- ✅ **Segurança**: JWT + Hashing de senha (bcrypt)
- ✅ **Documentação OpenAPI**: Gerada automaticamente (Swagger + ReDoc)

## 🚀 Como Executar

### Passo 1: Instalar Dependências

```bash
# No diretório do projeto
pip install -r requirements.txt
```

### Passo 2: Executar a API

#### Opção A: Com Uvicorn (Desenvolvimento)
```bash
cd src
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Opção B: Diretamente em Python
```bash
cd src
python main.py
```

Você verá a saída:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
```

### Passo 3: Verificar a Saúde da API

```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{"status": "healthy"}
```

## 📚 Documentação Interativa

Abra seu navegador e acesse:

### Swagger UI (Recomendado para testes)
```
http://localhost:8000/docs
```

### ReDoc (Documentação mais legível)
```
http://localhost:8000/redoc
```

## 🧪 Testes Automatizados

### Executar Todos os Testes
```bash
pytest src/tests/ -v
```

Saída esperada:
```
test_auth.py::TestAuth::test_login_success PASSED
test_auth.py::TestAuth::test_login_invalid_credentials PASSED
test_accounts.py::TestAccounts::test_criar_conta_success PASSED
...
======================== 20 passed in 2.34s =========================
```

### Executar Teste Específico
```bash
# Apenas autenticação
pytest src/tests/test_auth.py -v

# Apenas contas
pytest src/tests/test_accounts.py -v

# Apenas transações
pytest src/tests/test_transactions.py -v
```

### Com Cobertura de Código
```bash
pytest src/tests/ --cov=src --cov-report=html
```

Isso gera um arquivo `htmlcov/index.html` com relatório de cobertura.

## 🔐 Credenciais Padrão para Login

```
CPF: 12345678900
Senha: senha123
```

## 📝 Fluxo de Exemplo de Uso

### 1. Fazer Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678900",
    "senha": "senha123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Criar uma Conta
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/v1/contas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "cpf": "12345678901",
    "titular": "Maria Silva",
    "saldo_inicial": 1000.00
  }'
```

Resposta:
```json
{
  "id": 1,
  "cpf": "12345678901",
  "titular": "Maria Silva",
  "saldo": 1000.00,
  "criada_em": "2024-01-08T10:30:00",
  "atualizada_em": "2024-01-08T10:30:00"
}
```

### 3. Fazer um Depósito
```bash
curl -X POST http://localhost:8000/api/v1/transacoes/depositar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "conta_id": 1,
    "valor": 500.00,
    "descricao": "Depósito de salário"
  }'
```

### 4. Fazer um Saque
```bash
curl -X POST http://localhost:8000/api/v1/transacoes/sacar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "conta_id": 1,
    "valor": 100.00,
    "descricao": "Saque no caixa"
  }'
```

### 5. Obter Extrato
```bash
curl -X GET http://localhost:8000/api/v1/transacoes/extrato/1 \
  -H "Authorization: Bearer $TOKEN"
```

## 🎯 Script de Teste Automático

Use o script Python incluído:

```bash
python teste_api.py
```

Ele fará automaticamente:
1. Login
2. Criar uma conta
3. Fazer um depósito
4. Fazer um saque
5. Obter extrato
6. Testar validações

## 📊 Estrutura de Resposta de Erros

### Validação de Dados (422)
```json
{
  "detail": [
    {
      "loc": ["body", "cpf"],
      "msg": "ensure this value has at least 11 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Autenticação Inválida (401)
```json
{
  "detail": "Token inválido ou expirado"
}
```

### Sem Autenticação (403)
```json
{
  "detail": "Not authenticated"
}
```

### Validação de Negócio (400)
```json
{
  "detail": "Saldo insuficiente. Saldo atual: 100.00"
}
```

### Recurso Não Encontrado (404)
```json
{
  "detail": "Conta não encontrada"
}
```

## 💡 Dicas de Desenvolvimento

### Modo Debug
A API já inicia em modo reload (desenvolvimento). Para desativar:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Logs Detalhados
```bash
python -m uvicorn main:app --reload --log-level debug
```

### Mudar Porta
```bash
python -m uvicorn main:app --reload --port 8001
```

### Acessar de Outro Computador
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Então acesse: `http://seu_ip:8000`

## 🔧 Troubleshooting

### Erro: "Module not found"
Certifique-se de estar dentro do diretório `src/`:
```bash
cd src
python -m uvicorn main:app --reload
```

### Erro: "Port already in use"
Use outra porta:
```bash
python -m uvicorn main:app --reload --port 8001
```

### Erro: "No module named 'fastapi'"
Instale as dependências:
```bash
pip install -r requirements.txt
```

### Testes Falhando
Certifique-se de que está no diretório correto:
```bash
# Do diretório raiz do projeto
pytest src/tests/ -v
```

## 📋 Comandos Úteis (com Make)

Se tiver `make` instalado (Unix/Linux/macOS):

```bash
make install         # Instala dependências
make run             # Executa a API
make test            # Executa testes
make test-cov        # Testes com cobertura
make test-auth       # Testes de autenticação
make test-accounts   # Testes de contas
make test-transactions # Testes de transações
```

No Windows, instale `make` via chocolatey:
```bash
choco install make
```

## 🎓 Aprendizado

Durante o desenvolvimento desta API, você praticou:

1. **FastAPI**: Framework web assíncrono
2. **Async/Await**: Programação assíncrona em Python
3. **JWT**: Autenticação segura
4. **Pydantic**: Validação de dados
5. **SQLAlchemy** (preparado): ORM para bancos de dados
6. **Pytest**: Testes automatizados
7. **Arquitetura em Camadas**: Separação de responsabilidades
8. **RESTful Design**: Padrões de API REST
9. **OpenAPI**: Documentação automática
10. **CORS**: Compartilhamento de recursos entre origens

## 🎉 Próximos Passos

Para evoluir este projeto:

- [ ] Integrar com PostgreSQL
- [ ] Implementar paginação
- [ ] Adicionar filtros de busca
- [ ] Implementar rate limiting
- [ ] Adicionar auditoria
- [ ] Configurar logging centralizando
- [ ] Deploy em produção (Docker, AWS, Heroku)
- [ ] Frontend web para consumir a API
- [ ] Autenticação OAuth2
- [ ] Cache com Redis

## 📞 Suporte

Se encontrar problemas:

1. Verifique o [README.md](README.md)
2. Veja a [IMPLEMENTACAO.md](IMPLEMENTACAO.md)
3. Consulte a documentação do FastAPI: https://fastapi.tiangolo.com/
4. Acesse `/docs` ou `/redoc` para entender os endpoints
