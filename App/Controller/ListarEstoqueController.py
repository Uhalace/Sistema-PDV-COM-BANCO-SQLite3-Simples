import PySimpleGUI as sg

class ListarEstoqueControler:
    def __init__(self, banco):
        self.banco = banco

    def listar_estoque(self):
        estoque_brutas = self.banco.listar_estoque()
        estoque_formatado = []
        for estoque in estoque_brutas:
            id_, codigo, item, quantidade, valor, *_ = estoque
            estoque_formatado.append({
                "id": id_,
                "codigo": codigo,
                "item": str(item).strip(),
                "quantidade": quantidade,
                "valor": valor
            })

        page_size = 8
        total_rows = len(estoque_formatado)
        total_pages = max(1, (total_rows + page_size - 1) // page_size)
        current_page = 1

        def format_row(row):
            return [
                row["codigo"],
                row["item"],
                f"{row['quantidade'] / 100:.2f}".replace('.', ','),
                f"{row['valor'] / 100:.2f}".replace('.', ',')
            ]

        def get_page_rows(page):
            start = (page - 1) * page_size
            end = start + page_size
            return [format_row(row) for row in estoque_formatado[start:end]]

        def abrir_edicao(item):
            layout_edicao = [
                [sg.Text("Editar Estoque", font=("Segoe UI", 14, "bold"))],
                [sg.Text("Código:", size=(12, 1)), sg.Input(default_text=item["codigo"], key="codigo")],
                [sg.Text("Item:", size=(12, 1)), sg.Input(default_text=item["item"], key="item")],
                [sg.Text("Quantidade:", size=(12, 1)), sg.Input(default_text=f"{item['quantidade'] / 100:.2f}".replace('.', ','), key="quantidade")],
                [sg.Text("Valor:", size=(12, 1)), sg.Input(default_text=f"{item['valor'] / 100:.2f}".replace('.', ','), key="valor")],
                [sg.Text("", key="msg", text_color="red")],
                [sg.Push(), sg.Button("Salvar", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
            ]

            window_edicao = sg.Window(
                "Editar Estoque",
                layout_edicao,
                modal=True,
                icon="./icones/estoque.ico",
                finalize=True
            )

            while True:
                event_edicao, values_edicao = window_edicao.read()
                if event_edicao in (sg.WIN_CLOSED, "Cancelar"):
                    break
                if event_edicao == "Salvar":
                    try:
                        codigo = int(values_edicao["codigo"])
                        nome_item = str(values_edicao["item"]).strip()
                        if not nome_item:
                            raise ValueError("O nome do item não pode ficar vazio.")

                        quantidade = float(str(values_edicao["quantidade"]).replace(',', '.'))
                        quantidade_int = int(quantidade * 100)

                        valor = float(str(values_edicao["valor"]).replace(',', '.'))
                        valor_int = int(valor * 100)

                        self.banco.atualizar_estoque(item["id"], codigo, nome_item, quantidade_int, valor_int)
                        sg.popup("Item atualizado com sucesso!", title="Sucesso", keep_on_top=True, icon="./icones/estoque.ico")
                        break
                    except ValueError as ve:
                        window_edicao["msg"].update(str(ve))
                    except Exception as e:
                        window_edicao["msg"].update(f"Erro ao atualizar item: {e}")

            window_edicao.close()

        layout_listagem = [
            [sg.Push(), sg.Image("./Icones/nota_100.png", pad=(0, 0)), sg.Push()],
            [sg.Push(),
             sg.Text(
                 "Listagem de Estoque",
                 font=("Segoe UI", 15, "bold"),
                 pad=((0, 0), (0, 10))
             ),
             sg.Push()],
            [sg.Text("Clique em uma linha para editar o item.", font=("Segoe UI", 10), pad=((10, 0), (0, 10)))],
            [sg.Frame(
                "",
                [[
                    sg.Table(
                        values=get_page_rows(current_page),
                        headings=["Código", "Item", "Quantidade", "Valor"],
                        key="-TABLE-",
                        auto_size_columns=False,
                        col_widths=[10, 36, 14, 14],
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
                        enable_events=True,
                        vertical_scroll_only=True,
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
            [
                sg.Push(),
                sg.Button("Editar", key="-EDITAR-", size=(12, 1), font=("Segoe UI", 10)),
                sg.Button("Excluir", key="-EXCLUIR-", size=(12, 1), font=("Segoe UI", 10)),
                sg.Push()
            ],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button("Fechar", size=(18, 2), font=("Segoe UI", 10, "bold")), sg.Push()]
        ]

        window_listagem = sg.Window(
            "Listagem de Estoque",
            layout_listagem,
            icon="./icones/estoque.ico",
            resizable=True,
            size=(900, 600),
            finalize=True,
            element_justification="center"
        )

        window_listagem["-PREV-"].update(disabled=True)
        window_listagem["-NEXT-"].update(disabled=(total_pages == 1))

        def get_selected_item(values):
            selected_rows = values.get("-TABLE-", [])
            if not selected_rows:
                return None
            row_index = selected_rows[0]
            actual_index = (current_page - 1) * page_size + row_index
            if 0 <= actual_index < len(estoque_formatado):
                return estoque_formatado[actual_index]
            return None

        while True:
            event, values = window_listagem.read()
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
            elif event == "-TABLE-":
                pass
            elif event == "-EDITAR-":
                item = get_selected_item(values)
                if item is None:
                    sg.popup("Selecione um item antes de editar.", title="Atenção", keep_on_top=True, icon="./icones/estoque.ico")
                    continue
                abrir_edicao(item)
                estoque_brutas = self.banco.listar_estoque()
                estoque_formatado.clear()
                for estoque in estoque_brutas:
                    id_, codigo, item_codigo, quantidade, valor, *_ = estoque
                    estoque_formatado.append({
                        "id": id_,
                        "codigo": codigo,
                        "item": str(item_codigo).strip(),
                        "quantidade": quantidade,
                        "valor": valor
                    })
                total_rows = len(estoque_formatado)
                total_pages = max(1, (total_rows + page_size - 1) // page_size)
                if current_page > total_pages:
                    current_page = total_pages
                window_listagem["-TABLE-"].update(values=get_page_rows(current_page))
                window_listagem["-PAGE-"].update(f"Página {current_page}/{total_pages}")
                window_listagem["-PREV-"].update(disabled=(current_page == 1))
                window_listagem["-NEXT-"].update(disabled=(current_page == total_pages))
            elif event == "-EXCLUIR-":
                item = get_selected_item(values)
                if item is None:
                    sg.popup("Selecione um item antes de excluir.", title="Atenção", keep_on_top=True, icon="./icones/estoque.ico")
                    continue
                if sg.popup_yes_no(
                    f"Deseja excluir o item '{item['item']}' (código {item['codigo']})?",
                    title="Confirmar Exclusão",
                    keep_on_top=True,
                    icon="./icones/estoque.ico"
                ) == "Yes":
                    self.banco.excluir_estoque(item["id"])
                    sg.popup("Item excluído com sucesso.", title="Sucesso", keep_on_top=True, icon="./icones/estoque.ico")
                    estoque_brutas = self.banco.listar_estoque()
                    estoque_formatado.clear()
                    for estoque in estoque_brutas:
                        id_, codigo, item_codigo, quantidade, valor, *_ = estoque
                        estoque_formatado.append({
                            "id": id_,
                            "codigo": codigo,
                            "item": str(item_codigo).strip(),
                            "quantidade": quantidade,
                            "valor": valor
                        })
                    total_rows = len(estoque_formatado)
                    total_pages = max(1, (total_rows + page_size - 1) // page_size)
                    if current_page > total_pages:
                        current_page = total_pages
                    window_listagem["-TABLE-"].update(values=get_page_rows(current_page))
                    window_listagem["-PAGE-"].update(f"Página {current_page}/{total_pages}")
                    window_listagem["-PREV-"].update(disabled=(current_page == 1))
                    window_listagem["-NEXT-"].update(disabled=(current_page == total_pages))

        window_listagem.close()


