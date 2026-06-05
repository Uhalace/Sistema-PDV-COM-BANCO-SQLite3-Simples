import PySimpleGUI as sg
from App.Services.nota_printer import imprimir_arquivo_nota, formatar_vendas_para_tabela

class CadastrarNotaController:
    def __init__(self, banco):
        self.banco = banco

    def cadastrar_nota(self):
        layout_cadnota = [
    [sg.Frame(
        "Cadastro de Nota",
        [
            [sg.Text("Número da nota:", size=(15, 1)),
             sg.Input(default_text=str(self.banco.numero_nota_bd()), key="nunota")],

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
     sg.Button("Imprimir Nota", size=(12, 2), key="imprimir"),
     sg.Push()]
     ]

        window_cadnota = sg.Window("Cadastro de Nota", layout_cadnota, modal=True, icon="./icones/nota.ico")

        while True:
            event, values = window_cadnota.read()

            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "imprimir":
                try:
                    numero_nota = int(values["nunota"])
                except (ValueError, TypeError):
                    sg.popup("Por favor, informe um número válido para a nota.", title="Erro", keep_on_top=True, icon="./icones/nota.ico")
                    continue

                vendas_nota = self.banco.imprimir_nota(numero_nota)
                if not vendas_nota:
                    sg.popup("Nenhuma venda encontrada para esta nota.", title="Erro", keep_on_top=True, icon="./icones/nota.ico")
                    continue

                try:
                    linhas, total_cents = formatar_vendas_para_tabela(vendas_nota)
                    imprimir_arquivo_nota(numero_nota, linhas, total_cents)
                    sg.popup("Nota impressa com sucesso!", title="Sucesso", keep_on_top=True, icon="./icones/nota.ico")
                    window_cadnota["nunota"].update(self.banco.numero_nota_bd())
                except Exception as e:
                    sg.popup(f"Erro ao imprimir nota: {e}", title="Erro", keep_on_top=True, icon="./icones/nota.ico")


            if event == "Salvar":
                window_cadnota["msg"].update(text_color="red")

                try:
                    numero_nota = int(values["nunota"])
                except (ValueError, TypeError):
                    window_cadnota["msg"].update("Por favor, insira um número válido para a nota.")
                    continue

                nome_item = str(values["item"]).strip()
                if not nome_item:
                    window_cadnota["msg"].update("Por favor, insira o nome do item.")
                    continue

                try:
                    valor_float = float(str(values["valor"]).replace(',', '.'))
                    valor = int(valor_float * 100)
                except (ValueError, TypeError):
                    window_cadnota["msg"].update("Por favor, insira um número válido para o valor.")
                    continue

                try:
                    quantidade_float = float(str(values["quantidade"]).replace(',', '.'))
                    quantidade = int(quantidade_float * 100)
                except (ValueError, TypeError):
                    window_cadnota["msg"].update("Por favor, insira um número válido para a quantidade.")
                    continue

                subtotal_float = valor_float * quantidade_float
                subtotal = int(subtotal_float * 100)

                self.banco.inserir_venda(numero_nota, nome_item, quantidade, valor, subtotal)
                window_cadnota["msg"].update("Nota cadastrada com sucesso!", text_color="green")

                if sg.popup_yes_no("Deseja cadastrar outro item para a mesma nota?", title="Continuar?", keep_on_top=True) == "No":
                    window_cadnota["nunota"].update(self.banco.numero_nota_bd())
                    window_cadnota["item"].update("")
                    window_cadnota["valor"].update("")
                    window_cadnota["quantidade"].update("")
                    window_cadnota["nunota"].set_focus()
                else:
                    window_cadnota["nunota"].update(numero_nota)
                    window_cadnota["item"].update("")
                    window_cadnota["valor"].update("")
                    window_cadnota["quantidade"].update("")
                    window_cadnota["item"].set_focus()

        window_cadnota.close()
