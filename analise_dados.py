import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

class AnaliseDados:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _get_transacoes(self):
        query = "SELECT data, valor, tipo, descricao FROM transacoes"
        df = pd.read_sql_query(query, self.db_manager.conn)
        df['tipo'] = df['tipo'].str.lower()
        print("Tipos únicos encontrados:", df['tipo'].unique())
        print("Número total de transações:", len(df))
        return df

    def gastos_por_categoria(self):
        df = self._get_transacoes()
        gastos = df[df['tipo'] == 'saída'].groupby('descricao')['valor'].sum()
        fig, ax = plt.subplots(figsize=(6, 3.5))  # Reduzido para 6x3.5 polegadas
        if gastos.empty:
            ax.text(0.5, 0.5, 'Sem dados de gastos disponíveis', ha='center', va='center')
        else:
            wedges, texts, autotexts = ax.pie(gastos.values, autopct='%1.1f%%', textprops=dict(color="w", fontsize=8))
            # Removido o título do gráfico
            plt.setp(autotexts, size=8, weight="bold")
            
            # Adicionar legenda
            ax.legend(wedges, gastos.index,
                      title="Categorias",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1),
                      fontsize=8)
        
        ax.axis('equal')
        plt.tight_layout()
        return fig

    def tendencias_receitas_despesas(self):
        df = self._get_transacoes()
        df['data'] = pd.to_datetime(df['data'])
        df = df.set_index('data')
        receitas = df[df['tipo'] == 'entrada'].resample('D')['valor'].sum()
        despesas = df[df['tipo'] == 'saída'].resample('D')['valor'].sum()
        
        fig, ax = plt.subplots(figsize=(6, 3.5))  # Reduzido para 6x3.5 polegadas
        ax.plot(receitas.index, receitas.values, label='Receitas')
        ax.plot(despesas.index, despesas.values, label='Despesas')
        ax.set_xlabel('Data', fontsize=8)
        ax.set_ylabel('Valor (R$)', fontsize=8)
        ax.legend(fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def balanco_mensal(self):
        df = self._get_transacoes()
        df['data'] = pd.to_datetime(df['data'])
        df['mes'] = df['data'].dt.to_period('M')
        balanco = df.groupby(['mes', 'tipo'])['valor'].sum().unstack(fill_value=0)
        balanco['saldo'] = balanco.get('entrada', 0) - balanco.get('saída', 0)
        return balanco.reset_index()

    def previsao_gastos(self, dias_futuros=30):
        df = self._get_transacoes()
        df['data'] = pd.to_datetime(df['data'])
        df = df[df['tipo'] == 'saída'].sort_values('data')
        
        date_range = pd.date_range(start=df['data'].min(), end=df['data'].max())
        daily_expenses = df.groupby('data')['valor'].sum().reindex(date_range).fillna(0)

        X = np.array(range(len(daily_expenses))).reshape(-1, 1)
        y = daily_expenses.values

        model = LinearRegression()
        model.fit(X, y)

        last_date = daily_expenses.index[-1]
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=dias_futuros)
        X_future = np.array(range(len(daily_expenses), len(daily_expenses) + dias_futuros)).reshape(-1, 1)
        future_expenses = model.predict(X_future)

        fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.plot(daily_expenses.index, daily_expenses.values, label='Gastos Históricos', color='blue', alpha=0.7)
        
        rolling_mean = daily_expenses.rolling(window=7).mean()
        ax.plot(rolling_mean.index, rolling_mean.values, label='Média Móvel (7 dias)', color='red', linewidth=2)
        
        ax.plot(future_dates, future_expenses, label='Previsão', color='green', linestyle='--')

        ax.set_title('Histórico e Previsão de Gastos')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor (R$)')
        ax.legend()
        
        plt.gcf().autofmt_xdate()
        
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(0, ymax * 1.1)

        plt.tight_layout()
        return fig
