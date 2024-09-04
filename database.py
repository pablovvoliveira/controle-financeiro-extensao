import sqlite3
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_name):
        try:
            db_path = Path(db_name).resolve()
            self.conn = sqlite3.connect(str(db_path))
            self.cursor = self.conn.cursor()
            self.criar_tabela()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY,
                data DATE,
                descricao TEXT,
                valor REAL,
                tipo TEXT
            )
        ''')
        self.conn.commit()

    def adicionar_transacao(self, data, descricao, valor, tipo):
        if isinstance(data, datetime):
            data_str = data.strftime("%Y-%m-%d")
        elif isinstance(data, str):
            try:
                data_str = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                data_str = data  
        else:
            data_str = str(data)
        
        self.cursor.execute('''
            INSERT INTO transacoes (data, descricao, valor, tipo)
            VALUES (?, ?, ?, ?)
        ''', (data_str, descricao, valor, tipo))
        self.conn.commit()

    def obter_todas_transacoes(self):
        self.cursor.execute('SELECT * FROM transacoes ORDER BY data')
        return self.cursor.fetchall()

    def obter_transacoes_periodo(self, data_inicio, data_fim):
        self.cursor.execute('''
            SELECT * FROM transacoes
            WHERE data BETWEEN ? AND ?
            ORDER BY data
        ''', (data_inicio.strftime("%Y-%m-%d"), data_fim.strftime("%Y-%m-%d")))
        return self.cursor.fetchall()

    def obter_transacao(self, id_transacao):
        self.cursor.execute('SELECT * FROM transacoes WHERE id = ?', (id_transacao,))
        return self.cursor.fetchone()

    def atualizar_transacao(self, id_transacao, nova_data, nova_descricao, novo_valor, novo_tipo):
        self.cursor.execute('''
            UPDATE transacoes
            SET data = ?, descricao = ?, valor = ?, tipo = ?
            WHERE id = ?
        ''', (nova_data.strftime("%Y-%m-%d"), nova_descricao, novo_valor, novo_tipo, id_transacao))
        self.conn.commit()

    def deletar_transacao(self, id_transacao):
        self.cursor.execute('DELETE FROM transacoes WHERE id = ?', (id_transacao,))
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def fechar_conexao(self):
        self.conn.close()

    # Método adicionado para análise de dados
    def obter_gastos_por_categoria(self):
        self.cursor.execute("""
            SELECT descricao, SUM(valor) 
            FROM transacoes 
            WHERE tipo='Saída' 
            GROUP BY descricao
        """)
        return self.cursor.fetchall()