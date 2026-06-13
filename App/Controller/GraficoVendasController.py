import matplotlib.pyplot as plt
from App.Model.Banco import Banco

class GraficoVendasController:

    def __init__(self):
        self.banco = Banco()

    def gerar_grafico(self, ano: str):
        dados_banco = self.banco.relatorio_vendas(ano)

        dados = {}

        for linha in dados_banco:
            mes = linha[7]
            subtotal = linha[5] / 100

            dados[mes] = dados.get(mes, 0) + subtotal

        meses = list(dados.keys())
        valores = list(dados.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        barras = ax.bar(meses, valores)

        ax.bar_label(barras, fmt='R$ %.2f', padding=3)

        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor Total Arrecadado")
        ax.set_title(f"Relatório de Vendas - {ano}")

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()