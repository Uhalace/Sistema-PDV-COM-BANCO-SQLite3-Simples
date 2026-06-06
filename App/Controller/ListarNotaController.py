import PySimpleGUI as sg
from App.Functions.format import format_reais

class ListarNotaController:
    def __init__(self, banco):
        self.banco = banco

    def listar_dados(self):
        vendas_brutas = self.banco.listar_vendas()
        vendas_formatadas = []
        total_itens = 0
        faturamento = 0
        for venda in vendas_brutas:
            v_list = list(venda)
            v_list.pop(0)
            v_list[0] = str(v_list[0]).strip()
            v_list[1] = str(v_list[1]).strip()
            total_itens += float(v_list[2]/100)
            v_list[2] = f"{v_list[2] / 100:.2f}".replace('.', ',')
            v_list[3] = format_reais(v_list[3])
            faturamento += float(v_list[4]/100)
            v_list[4] = format_reais(v_list[4])
            
            vendas_formatadas.append(v_list)

        layout_listagem = [
    [sg.Push(), sg.Image("./icones/nota_100.png"), sg.Push()],

    [sg.Push(),
     sg.Text(
         "Listagem de Vendas",
         font=("Segoe UI", 18, "bold")
     ),
     sg.Push()],

    [sg.Frame(
        "",
        [[
            sg.Table(
                values=vendas_formatadas,
                headings=[
                    "Número da Nota",
                    "Item",
                    "Quantidade",
                    "Valor",
                    "Subtotal"
                ],
                key="-TABLE-",
                auto_size_columns=False,
                col_widths=[15, 32, 12, 16, 16],
                justification="center",
                text_color="#000000",
                background_color="#FFFFFF",
                header_background_color="#404040",
                header_text_color="#FFFFFF",
                header_font=("Segoe UI", 11, "bold"),
                font=("Segoe UI", 11),
                row_height=30,
                num_rows=15,
                alternating_row_color="#F7F7F7",
                expand_x=True,
                expand_y=True,
                pad=((0, 0), (10, 10))
            )
        ]],
        expand_x=True,
        expand_y=True,
        relief=sg.RELIEF_SUNKEN,
        pad=(10, 10)
    )],

    [sg.HorizontalSeparator()],
    [sg.Text(f"Itens: {total_itens:.2f}".replace('.', ','), font=("Segoe UI", 12, "bold"), justification='left'), 
     sg.Text(f"Faturamento: R$: {faturamento:.2f}".replace('.', ','), font=("Segoe UI", 12, "bold"), justification='left')],

    [sg.Push(),
     sg.Button(
         "Fechar", size=(18, 2), font=("Segoe UI", 10, "bold") ),
     sg.Push()]
]

        window_listagem = sg.Window(
    "Listagem de Vendas",
    layout_listagem,
    icon="./icones/nota.ico",
    resizable=True,
    size=(900, 600),
    finalize=True
)

        while True:
            event, _ = window_listagem.read()
            if event in (sg.WIN_CLOSED, "Fechar"):
                break

        window_listagem.close()

    def listar_numeros_notas(self):
        return self.banco.listar_numeros_notas()