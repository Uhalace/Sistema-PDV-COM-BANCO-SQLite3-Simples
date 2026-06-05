import PySimpleGUI as sg

from App.Controller.CadastrarNotaController import CadastrarNotaController
from App.Controller.ListarNotaController import ListarNotaController
from App.Functions.format import format_reais
from App.Model.Banco import Banco
from App.Services.nota_printer import formatar_vendas_para_tabela, imprimir_arquivo_nota


def criar_janela_principal():
    sg.theme('Reddit')

    layout = [
        [sg.Push(), sg.Image("./Icones/nota_100.png"), sg.Push()],
        [sg.Push(), sg.Text("PDV Notas", font=("Helvetica", 16)), sg.Push()],
        [
            sg.Button("Cadastrar Nota", size=(18, 2), font=("Segoe UI", 10, "bold")),
            sg.Button("Listar Vendas", size=(18, 2), font=("Segoe UI", 10, "bold")),
            sg.Button("Imprimir Nota", size=(18, 2), font=("Segoe UI", 10, "bold"))
        ],
        [sg.Button("Sair", size=(18, 2), font=("Segoe UI", 10, "bold"))],
        [
            sg.Text(
                "Desenvolvido por: Uhalace de Souza",
                font=("Helvetica", 10),
                justification='center',
                pad=((0, 0), (20, 0))
            )
        ]
    ]

    return sg.Window("PDV Notas", layout, size=(500, 400), icon="./Icones/nota.ico")


def selecionar_nota_para_impressao(banco):
    notas = banco.listar_numeros_notas()

    layout_selecao = [
        [sg.Text("Selecione a nota para imprimir:")],
        [
            sg.Listbox(
                values=notas,
                size=(20, min(len(notas), 10)),
                key="-NOTA-"
            )
        ],
        [sg.Button("OK"), sg.Button("Cancelar")]
    ]

    janela_selecao = sg.Window(
        "Selecionar Nota",
        layout_selecao,
        modal=True,
        size=(200, 200),
        icon="./Icones/nota.ico"
    )

    numero_nota = None

    while True:
        evento_sel, valores_sel = janela_selecao.read()

        if evento_sel in (sg.WIN_CLOSED, "Cancelar"):
            break

        if evento_sel == "OK":
            if valores_sel["-NOTA-"]:
                numero_nota = valores_sel["-NOTA-"][0]
                break
            sg.popup("Selecione uma nota.")

    janela_selecao.close()

    return numero_nota


def mostrar_nota_para_impressao(numero_nota, banco):
    try:
        numero_nota_int = int(numero_nota)
    except ValueError:
        sg.popup("Por favor, insira um número válido para a nota.")
        return

    vendas_nota = banco.imprimir_nota(numero_nota_int)
    if not vendas_nota:
        sg.popup("Nenhuma venda encontrada para o número da nota informado.")
        return

    vendas_formatadas, total_cents = formatar_vendas_para_tabela(vendas_nota)

    layout_impressao = [
        [sg.Text(f"Nota Fiscal - Número: {numero_nota}", font=("Helvetica", 16))],
        [
            sg.Table(
                values=vendas_formatadas,
                headings=["Item", "Quantidade", "Valor", "Subtotal"],
                auto_size_columns=True
            )
        ],
        [sg.Text(
            f"Total da Nota: {format_reais(total_cents)}",
            font=("Helvetica", 14),
            justification='right',
            pad=((0, 0), (10, 0))
        )],
        [sg.Button("Imprimir"), sg.Button("Fechar")]
    ]

    window_impressao = sg.Window("Imprimir Nota", layout_impressao, icon="./Icones/nota.ico")

    while True:
        event_impressao, _ = window_impressao.read()
        if event_impressao in (sg.WIN_CLOSED, "Fechar"):
            break
        if event_impressao == "Imprimir":
            imprimir_arquivo_nota(numero_nota, vendas_formatadas, total_cents)

    window_impressao.close()


def main():
    banco = Banco()
    cadastrar_nota_controller = CadastrarNotaController(banco)
    listar_nota_controller = ListarNotaController(banco)
    window = criar_janela_principal()

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            break
        if event == "Cadastrar Nota":
            cadastrar_nota_controller.cadastrar_nota()
        elif event == "Listar Vendas":
            listar_nota_controller.listar_dados()
        elif event == "Imprimir Nota":
            numero_nota = selecionar_nota_para_impressao(banco)
            if numero_nota is not None:
                mostrar_nota_para_impressao(numero_nota, banco)

    window.close()
    banco.fechar_conexao()
