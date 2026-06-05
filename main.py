#========================================================
#        PDV Notas - 2026.1
#========================================================

import os
import tempfile
from datetime import datetime
import PySimpleGUI as sg
from App.Model.Banco import Banco
from App.Functions.format import format_reais
from App.Controller.CadastrarNotaController import CadastrarNotaController
from App.Controller.ListarNotaController import ListarNotaController

ESTABELECIMENTO_NOME = "Loja Exemplo Ltda."
ESTABELECIMENTO_CNPJ = "00.000.000/0000-00"
ESTABELECIMENTO_IE = "123.456"
ESTABELECIMENTO_ENDERECO = "Rua A, 0 - Centro - Cidade/UF"
ESTABELECIMENTO_TELEFONE = "(00) 0000-0000"


def imprimir_arquivo_nota(numero, linhas, total):
    item_width = 24
    qtd_width = 6
    valor_width = 12
    subtotal_width = 14
    line_length = item_width + qtd_width + valor_width + subtotal_width
    now = datetime.now()

    def format_reais_inner(cents):
        return f"R$ {cents / 100:.2f}".replace('.', ',')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as arquivo:
        arquivo.write(f"{ESTABELECIMENTO_NOME.center(line_length)}\n")
        arquivo.write(f"CNPJ: {ESTABELECIMENTO_CNPJ}{'':<{line_length - 7 - len(ESTABELECIMENTO_CNPJ)}}\n")
        arquivo.write(f"IE: {ESTABELECIMENTO_IE}{'':<{line_length - 4 - len(ESTABELECIMENTO_IE)}}\n")
        arquivo.write(f"{ESTABELECIMENTO_ENDERECO.center(line_length)}\n")
        arquivo.write(f"TEL: {ESTABELECIMENTO_TELEFONE.center(line_length - 5)}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"{r'\\Cupom Fiscal\\'.center(line_length)}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"Nº: {numero:<8}DATA: {now:%d/%m/%Y}  HORA: {now:%H:%M:%S}\n")
        arquivo.write("-" * line_length + "\n")
        arquivo.write(f"{'ITEM':<{item_width}}{'QTD':>{qtd_width}}{'V.UNIT':>{valor_width}}{'SUBTOTAL':>{subtotal_width}}\n")
        arquivo.write("-" * line_length + "\n")
        for linha in linhas:
            item = str(linha[0])[:item_width]
            qtd = linha[1]
            valor = linha[2]
            subtotal = linha[3]
            arquivo.write(f"{item:<{item_width}}{qtd:>{qtd_width}}{valor:>{valor_width}}{subtotal:>{subtotal_width}}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"{'TOTAL DA NOTA':<{item_width + qtd_width + valor_width}}{format_reais_inner(total):>{subtotal_width}}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"{'FORMA DE PAGAMENTO: À VISTA'.ljust(line_length)}\n")
        arquivo.write(f"{'Consumidor: ________________________________'.ljust(line_length)}\n")
        arquivo.write(f"{'Assinatura: ________________________________'.ljust(line_length)}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"{'Cupom sem validade fiscal'.center(line_length)}\n")
        arquivo.write("=" * line_length + "\n")
        arquivo_path = arquivo.name

    try:
        os.startfile(arquivo_path, 'print')
        sg.popup('A nota foi enviada para impressão.')
    except Exception as e:
        sg.popup(f'Erro ao imprimir: {e}')


def main():
    banco = Banco()
    cadastrar_nota_controller = CadastrarNotaController(banco)
    listar_nota_controller = ListarNotaController(banco)

    sg.theme('Reddit')
    layout = [
        [sg.Text("PDV Notas", font=("Helvetica", 16))],
        [sg.Button("Cadastrar Nota"),sg.Button("Listar Vendas"), sg.Button("Imprimir Nota")],
        [sg.Button("Sair")],
        [sg.Text("Desenvolvido por: Uhalace de Souza", font=("Helvetica", 10), justification='center', pad=((0, 0), (20, 0)))]
    ]

    window = sg.Window("PDV Notas", layout, size=(400, 300), icon="./icones/nota.ico")

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            break
        elif event == "Cadastrar Nota":
            cadastrar_nota_controller.cadastrar_nota()
        elif event == "Listar Vendas":
            listar_nota_controller.listar_dados()
        elif event == "Imprimir Nota":
            numero_nota = sg.popup_get_text("Digite o número da nota para imprimir:")
            if numero_nota is not None:
                try:
                    numero_nota_int = int(numero_nota)
                    vendas_nota = banco.imprimir_nota(numero_nota_int)
                    if vendas_nota:
                        vendas_formatadas = []
                        total_cents = 0
                        for venda in vendas_nota:
                            v_list = list(venda)
                            quantidade_cents = v_list[3]
                            valor_cents = v_list[4]
                            subtotal_cents = v_list[5]
                            total_cents += subtotal_cents
                            vendas_formatadas.append([
                                str(v_list[2]).strip(),
                                f"{quantidade_cents / 100:.2f}".replace('.', ','),
                                format_reais(valor_cents),
                                format_reais(subtotal_cents)
                            ])

                        layout_impressao = [
                            [sg.Text(f"Nota Fiscal - Número: {numero_nota}", font=("Helvetica", 16))],
                            [sg.Table(values=vendas_formatadas, headings=["Item", "Quantidade", "Valor", "Subtotal"], auto_size_columns=True)],
                            [sg.Text(f"Total da Nota: {format_reais(total_cents)}", font=("Helvetica", 14), justification='right', pad=((0, 0), (10, 0)))],
                            [sg.Button("Imprimir"), sg.Button("Fechar")]
                        ]
                        window_impressao = sg.Window("Imprimir Nota", layout_impressao)
                        while True:
                            event_impressao, _ = window_impressao.read()
                            if event_impressao in (sg.WIN_CLOSED, "Fechar"):
                                break
                            if event_impressao == "Imprimir":
                                imprimir_arquivo_nota(numero_nota, vendas_formatadas, total_cents)
                        window_impressao.close()
                    else:
                        sg.popup("Nenhuma venda encontrada para o número da nota informado.")
                except ValueError:
                    sg.popup("Por favor, insira um número válido para a nota.")

    window.close()
    banco.fechar_conexao()


if __name__ == "__main__":
    main()
