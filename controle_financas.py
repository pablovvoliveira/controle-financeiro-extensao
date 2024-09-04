from datetime import datetime, timedelta
import logging

class ControleFinancas:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def adicionar_transacao(self, data, descricao, valor, tipo):
        self.db_manager.adicionar_transacao(data, descricao, valor, tipo)

    def obter_todas_transacoes(self):
        return self.db_manager.obter_todas_transacoes()

    def calcular_totais(self):
        transacoes = self.obter_todas_transacoes()
        total_entradas = sum(t[3] for t in transacoes if t[4] == "Entrada")
        total_saidas = sum(t[3] for t in transacoes if t[4] == "Saída")
        return total_entradas, total_saidas

    def obter_transacoes_periodo(self, data_inicio, data_fim):
        return self.db_manager.obter_transacoes_periodo(data_inicio, data_fim)

    def calcular_totais_periodo(self, data_inicio, data_fim):
        transacoes = self.obter_transacoes_periodo(data_inicio, data_fim)
        total_entradas = sum(t[3] for t in transacoes if t[4] == "Entrada")
        total_saidas = sum(t[3] for t in transacoes if t[4] == "Saída")
        return total_entradas, total_saidas

    def obter_transacao(self, id_transacao):
        return self.db_manager.obter_transacao(id_transacao)

    def atualizar_transacao(self, id_transacao, nova_data, nova_descricao, novo_valor, novo_tipo):
        self.db_manager.atualizar_transacao(id_transacao, nova_data, nova_descricao, novo_valor, novo_tipo)

    def deletar_transacao(self, id_transacao):
        self.db_manager.deletar_transacao(id_transacao)