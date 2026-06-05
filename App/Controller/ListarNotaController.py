import PySimpleGUI as sg
from App.Functions.format import format_reais

class ListarNotaController:
    def __init__(self, banco):
        self.banco = banco

    def listar_dados(self):
        vendas_brutas = self.banco.listar_vendas()
        vendas_formatadas = []

        for venda in vendas_brutas:
            v_list = list(venda)
            v_list.pop(0)
            v_list[0] = str(v_list[0]).strip()
            v_list[1] = str(v_list[1]).strip()
            v_list[2] = f"{v_list[2] / 100:.2f}".replace('.', ',')
            v_list[3] = format_reais(v_list[3])
            v_list[4] = format_reais(v_list[4])
            vendas_formatadas.append(v_list)

        layout_listagem = [
            [sg.Text("Listagem de Vendas", font=("Helvetica", 16), justification='justify')],
            [sg.Table(values=vendas_formatadas, headings=["Número da Nota", "Item", "Quantidade", "Valor", "Subtotal"], auto_size_columns=True, key="-TABLE-", justification='left')],
            [sg.Button("Fechar")]
        ]

        window_listagem = sg.Window("Listagem de Vendas", layout_listagem, icon="./icones/nota.ico", text_justification='justify')

        while True:
            event, _ = window_listagem.read()
            if event in (sg.WIN_CLOSED, "Fechar"):
                break

        window_listagem.close()
