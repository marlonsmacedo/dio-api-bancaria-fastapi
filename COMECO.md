# 🎬 Guia Rápido - Primeiros Passos

## ⏱️ 5 Minutos para Começar

### ✅ Passo 1: Instalar (1 minuto)
```bash
pip install -r requirements.txt
```

### ✅ Passo 2: Executar (1 minuto)
```bash
cd src
python -m uvicorn main:app --reload
```

Esperado:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### ✅ Passo 3: Acessar (1 minuto)
Abra seu navegador:
```
http://localhost:8000/docs
```

### ✅ Passo 4: Fazer Login (1 minuto)

1. No Swagger, procure "POST /api/v1/auth/login"
2. Clique em "Try it out"
3. Use as credenciais padrão:
```json
{
  "cpf": "12345678900",
  "senha": "senha123"
}
```
4. Clique "Execute"
5. Copie o `access_token`

### ✅ Passo 5: Testar Endpoints (1 minuto)

Clique no ícone de cadeado ao lado de qualquer endpoint
Colar o token no modal que aparece

Agora pode testar qualquer endpoint! ✨

---

## 🎯 Fluxo Completo de Teste (Passo a Passo)

### 1️⃣ Login
```
Endpoint: POST /api/v1/auth/login
Body: {"cpf": "12345678900", "senha": "senha123"}
Token: Copie para usar nos próximos passos
```

### 2️⃣ Criar Conta
```
Endpoint: POST /api/v1/contas/
Body: {
  "cpf": "12345678901",
  "titular": "João Silva",
  "saldo_inicial": 1000.00
}
Resultado: Conta criada com ID (por exemplo, 1)
```

### 3️⃣ Obter Conta
```
Endpoint: GET /api/v1/contas/1
Resultado: Dados da conta que você criou
```

### 4️⃣ Fazer Depósito
```
Endpoint: POST /api/v1/transacoes/depositar
Body: {
  "conta_id": 1,
  "valor": 500.00,
  "descricao": "Depósito"
}
Resultado: Transação registrada
```

### 5️⃣ Fazer Saque
```
Endpoint: POST /api/v1/transacoes/sacar
Body: {
  "conta_id": 1,
  "valor": 200.00,
  "descricao": "Saque"
}
Resultado: Transação registrada
```

### 6️⃣ Obter Extrato
```
Endpoint: GET /api/v1/transacoes/extrato/1
Resultado: Lista de todas as transações da conta
```

---

## 📋 Checklist de Testes

Marque conforme avança:

- [ ] API iniciada com sucesso
- [ ] Acessou /docs (Swagger)
- [ ] Fez login com sucesso
- [ ] Criou uma conta
- [ ] Obteve dados da conta
- [ ] Fez um depósito
- [ ] Fez um saque
- [ ] Consultou extrato
- [ ] Viu as 2 transações no extrato
- [ ] Testou erro (ex: saque sem saldo)

---

## 🧪 Testes Automatizados (Opcional)

Se quiser executar testes:

### Todos os testes
```bash
pytest src/tests/ -v
```

### Apenas um teste
```bash
pytest src/tests/test_auth.py::TestAuth::test_login_success -v
```

### Com cobertura
```bash
pytest src/tests/ --cov=src --cov-report=html
```

---

## 🛠️ Comandos Úteis

### Se tiver Make instalado
```bash
make run              # Executar API
make test             # Executar testes
make test-cov         # Testes com cobertura
make clean            # Limpar arquivos temporários
```

### Sem Make
```bash
cd src
python -m uvicorn main:app --reload          # Executar
pytest ../tests/ -v                          # Testar
python ../teste_api.py                       # Script teste
```

---

## ⚠️ Problemas Comuns & Soluções

### "Module not found"
```bash
# Certifique-se de estar no diretório src/
cd src
python -m uvicorn main:app --reload
```

### "Port already in use"
```bash
# Use outra porta
python -m uvicorn main:app --reload --port 8001
```

### "No module named 'fastapi'"
```bash
# Instale as dependências
pip install -r requirements.txt
```

### Token não funciona
```bash
# Faça login novamente e copie o novo token
# Verifique que está incluindo no header correto: Authorization: Bearer {token}
```

---

## 📚 Documentação

Depois dos 5 minutos iniciais, leia nesta ordem:

1. **README.md** (20 min) - Visão geral completa
2. **ENDPOINTS.md** (10 min) - Referência rápida
3. **GUIA_EXECUCAO.md** (15 min) - Como executar e testar
4. **IMPLEMENTACAO.md** (30 min) - Arquitetura e padrões
5. **ARQUITETURA.md** (20 min) - Diagramas visuais

---

## 🎓 O que Aprender Depois

1. **Estrutura do Código**
   - Abra `src/main.py` - Entenda o setup FastAPI
   - Abra `src/api/v1/endpoints/auth.py` - Veja um endpoint

2. **Fluxo de Autenticação**
   - `src/core/security.py` - JWT
   - `src/api/dependencies.py` - Validação

3. **Camada de Serviço**
   - `src/services/account_service.py` - Lógica de negócio

4. **Banco de Dados**
   - `src/db/models/` - Estrutura de dados
   - `src/db/repository/` - Acesso a dados

5. **Testes**
   - `src/tests/` - Como testar cada camada

---

## 🎬 Video Tutorial (Se tiver)

Se preferir um guia ainda mais visual:
```bash
python teste_api.py
```

Este script simula um usuário usando a API passo a passo.

---

## 🎯 Próximo Passo Recomendado

**Leia o README.md** - Tem tudo que você precisa saber!

```bash
cat README.md
```

---

## 💡 Dicas

✨ **No Swagger (/docs):**
- Use o ícone de cadeado para adicionar token
- Clique "Try it out" para testar endpoints
- Veja exemplos de resposta em cada endpoint

✨ **Estrutura de Pasta:**
- Cada pasta tem um propósito específico
- Segue arquitetura profissional
- Fácil de expandir com novos features

✨ **Testes:**
- Escritos para validar funcionalidades
- Podem ser executados a qualquer momento
- Garantem que nada quebrou

---

## 🎉 Você Está Pronto!

Agora você tem uma **API Bancária completa** e pode:

✅ Fazer login
✅ Gerenciar contas
✅ Fazer depósitos e saques
✅ Consultar extrato
✅ Ver documentação automática
✅ Executar testes

---

**Divirta-se explorando! 🚀**

Qualquer dúvida, consulte:
- 📖 README.md
- 📖 GUIA_EXECUCAO.md
- 📖 ENDPOINTS.md

---

*Desenvolvido como Desafio DIO - Digital Innovation One*
