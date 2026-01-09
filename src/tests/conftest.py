"""Configuração do pytest para os testes da aplicação"""
import pytest
import sys
from pathlib import Path

# Adicionar o diretório src ao path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Resetar o banco de dados antes de cada teste
@pytest.fixture(autouse=True)
def reset_database():
    """Reseta o banco de dados em memória antes de cada teste"""
    from db.session import db
    db.contas.clear()
    db.transacoes.clear()
    db.conta_counter = 1
    db.transacao_counter = 1
    yield
    # Cleanup após o teste
    db.contas.clear()
    db.transacoes.clear()
    db.conta_counter = 1
    db.transacao_counter = 1
