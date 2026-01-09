.PHONY: help install run test test-cov test-auth test-accounts test-transactions lint format clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make install          - Instala as dependências"
	@echo "  make run              - Executa a API em desenvolvimento"
	@echo "  make test             - Executa todos os testes"
	@echo "  make test-cov         - Executa testes com cobertura"
	@echo "  make test-auth        - Executa testes de autenticação"
	@echo "  make test-accounts    - Executa testes de contas"
	@echo "  make test-transactions - Executa testes de transações"
	@echo "  make lint             - Executa verificação de código"
	@echo "  make format           - Formata o código"
	@echo "  make clean            - Remove arquivos temporários"

install:
	pip install -r requirements.txt

run:
	cd src && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest src/tests/ -v

test-cov:
	pytest src/tests/ --cov=src --cov-report=html --cov-report=term-missing -v

test-auth:
	pytest src/tests/test_auth.py -v

test-accounts:
	pytest src/tests/test_accounts.py -v

test-transactions:
	pytest src/tests/test_transactions.py -v

lint:
	flake8 src/ --max-line-length=120

format:
	black src/ --line-length=120

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .coverage htmlcov .pytest_cache
