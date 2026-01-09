"""Configuração de sessão de banco de dados"""
# Para este exemplo, usaremos um banco de dados em memória
# Em produção, configure com SQLAlchemy e um banco de dados real

class DatabaseManager:
    """Gerenciador de banco de dados em memória"""
    
    def __init__(self):
        self.contas = {}
        self.transacoes = {}
        self.conta_counter = 1
        self.transacao_counter = 1
    
    def obter_proximo_conta_id(self) -> int:
        """Obtém o próximo ID de conta"""
        id_conta = self.conta_counter
        self.conta_counter += 1
        return id_conta
    
    def obter_proximo_transacao_id(self) -> int:
        """Obtém o próximo ID de transação"""
        id_transacao = self.transacao_counter
        self.transacao_counter += 1
        return id_transacao


# Instância global do gerenciador
db = DatabaseManager()
