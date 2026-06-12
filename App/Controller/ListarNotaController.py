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
            total_itens += float(v_list[2] / 100)
            v_list[2] = f"{v_list[2] / 100:.2f}".replace('.', ',')
            v_list[3] = format_reais(v_list[3])
            faturamento += float(v_list[4] / 100)
            v_list[4] = format_reais(v_list[4])
            
            vendas_formatadas.append(v_list)

        screen_width, screen_height = sg.Window.get_screen_size()
        window_width = min(1200, int(screen_width * 0.92))
        window_height = min(780, int(screen_height * 0.82))

        page_size = 8
        total_rows = len(vendas_formatadas)
        total_pages = max(1, (total_rows + page_size - 1) // page_size)
        current_page = 1

        def get_page_rows(page):
            start = (page - 1) * page_size
            end = start + page_size
            return vendas_formatadas[start:end]

        layout_listagem = [
            [sg.Push(), sg.Image("./icones/vendas_100.png", pad=(0, 0)), sg.Push()],
            [sg.Push(),
             sg.Text(
                 "Listagem de Vendas",
                 font=("Segoe UI", 15, "bold"),
                 pad=((0, 0), (0, 10))
             ),
             sg.Push()],
            [sg.Frame(
                "",
                [[
                    sg.Table(
                        values=get_page_rows(current_page),
                        headings=[
                            "Número da Nota",
                            "Item",
                            "Quantidade",
                            "Valor",
                            "Subtotal"
                        ],
                        key="-TABLE-",
                        auto_size_columns=False,
                        col_widths=[12, 42, 12, 15, 15],
                        justification="center",
                        text_color="#000000",
                        background_color="#FFFFFF",
                        header_background_color="#404040",
                        header_text_color="#FFFFFF",
                        header_font=("Segoe UI", 11, "bold"),
                        font=("Segoe UI", 11),
                        row_height=30,
                        num_rows=page_size,
                        alternating_row_color="#F7F7F7",
                        vertical_scroll_only=True,
                        enable_events=False,
                        expand_x=True,
                        expand_y=True,
                        pad=(0, 0)
                    )
                ]],
                expand_x=True,
                expand_y=True,
                relief=sg.RELIEF_SUNKEN,
                pad=(10, 10)
            )],
            [
                sg.Push(),
                sg.Button("<< Anterior", key="-PREV-", size=(12, 1), font=("Segoe UI", 10)),
                sg.Text(f"Página {current_page}/{total_pages}", key="-PAGE-", font=("Segoe UI", 11, "bold"), pad=(10, 0)),
                sg.Button("Próximo >>", key="-NEXT-", size=(12, 1), font=("Segoe UI", 10)),
                sg.Push()
            ],
            [sg.HorizontalSeparator()],
            [sg.Text(f"Itens: {total_itens:.2f}".replace('.', ','), font=("Segoe UI", 12, "bold"), justification='left'),
             sg.Text(f"Faturamento: R$: {faturamento:.2f}".replace('.', ','), font=("Segoe UI", 12, "bold"), justification='right', pad=((20, 0), 0))],
            [sg.Push(),
             sg.Button(
                 "Fechar", size=(18, 2), font=("Segoe UI", 10, "bold") ),
             sg.Push()]
        ]

        window_listagem = sg.Window(
            "Listagem de Vendas",
            layout_listagem,
            icon="./Icones/nota.ico",
            resizable=True,
            size=(window_width, window_height),
            finalize=True,
            element_justification="center"
        )

        window_listagem["-PREV-"].update(disabled=True)
        window_listagem["-NEXT-"].update(disabled=(total_pages == 1))

        while True:
            event, _ = window_listagem.read()
            if event in (sg.WIN_CLOSED, "Fechar"):
                break
            if event == "-PREV-" and current_page > 1:
                current_page -= 1
                window_listagem["-TABLE-"].update(values=get_page_rows(current_page))
                window_listagem["-PAGE-"].update(f"Página {current_page}/{total_pages}")
                window_listagem["-PREV-"].update(disabled=(current_page == 1))
                window_listagem["-NEXT-"].update(disabled=False)
            elif event == "-NEXT-" and current_page < total_pages:
                current_page += 1
                window_listagem["-TABLE-"].update(values=get_page_rows(current_page))
                window_listagem["-PAGE-"].update(f"Página {current_page}/{total_pages}")
                window_listagem["-NEXT-"].update(disabled=(current_page == total_pages))
                window_listagem["-PREV-"].update(disabled=False)

        window_listagem.close()

    def listar_numeros_notas(self):
        return self.banco.listar_numeros_notas()