"""Configuração do pytest para os testes"""
import sys
from pathlib import Path

# Adicionar o diretório src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
