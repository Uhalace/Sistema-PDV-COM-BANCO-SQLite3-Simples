import PySimpleGUI as sg
from App.Api.Api import obter_nome_produto

class CadastrarEstoqueController:
    def __init__(self, banco):
        self.banco = banco

    def cadastrar_estoque(self):
        layout_cadestoque = [
            [sg.Frame(
                "Cadastro de Estoque",
                [
                    [sg.Text("Código do item:", size=(15, 1)),
                     sg.Input(key="codigo", focus=True)],

                    [sg.Text("Nome do item:", size=(15, 1)),
                     sg.Input(key="item")],

                    [sg.Text("Valor:", size=(15, 1)),
                     sg.Input(key="valor")],

                    [sg.Text("Quantidade:", size=(15, 1)),
                     sg.Input(key="quantidade")],

                    [sg.Text("", key="msg", text_color="red")]
                ],
                expand_x=True
            )],

            [sg.Push(),
             sg.Button("Salvar", size=(12, 2)),
             sg.Button("Cancelar", size=(12, 2)),
             sg.Push()]
        ]

        window_cadestoque = sg.Window("Cadastro de Estoque", layout_cadestoque, modal=True, icon="./Icones/nota.ico", finalize=True)
        
        window_cadestoque["codigo"].bind("<Return>", "_enter")
        
        window_cadestoque.refresh()
        window_cadestoque["codigo"].set_focus()
        
        while True:
            event, values = window_cadestoque.read()

            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
                
            if event == "codigo_enter":
                codigo = values["codigo"]
                codigo_produto = obter_nome_produto(codigo)
                window_cadestoque["item"].update(codigo_produto)
                window_cadestoque["valor"].set_focus()
                
            if event == "Salvar":
                try:
                    codigo = int(values["codigo"])
                    item = values["item"].strip()
                    valor = str(values["valor"]).replace(',', '.')
                    valor = float(valor)
                    valor = int(valor * 100)

                    quantidade = str(values["quantidade"]).replace(',', '.')
                    quantidade = float(quantidade)
                    quantidade = int(quantidade * 100)

                    if not item:
                        raise ValueError("O nome do item não pode ser vazio.")

                    self.banco.inserir_estoque(codigo, item, quantidade, valor)
                    sg.popup("Item cadastrado com sucesso!", title="Sucesso", keep_on_top=True, icon="./icones/estoque.ico")
                    window_cadestoque.close()
                except ValueError as ve:
                    window_cadestoque["msg"].update(str(ve))
                except Exception as e:
                    window_cadestoque["msg"].update(f"Erro ao cadastrar item: {e}")

        window_cadestoque.close()