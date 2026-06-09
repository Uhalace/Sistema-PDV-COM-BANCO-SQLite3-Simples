import os
import tempfile
from datetime import datetime

import PySimpleGUI as sg

from App.Functions.format import format_reais

ESTABELECIMENTO_NOME = "Loja Exemplo Ltda."
ESTABELECIMENTO_CNPJ = "00.000.000/0000-00"
ESTABELECIMENTO_IE = "123.456"
ESTABELECIMENTO_ENDERECO = "Rua A, 0 - Centro - Cidade/UF"
ESTABELECIMENTO_TELEFONE = "(00) 0000-0000"


def _format_reais_inner(cents):
    return f"R$ {cents / 100:.2f}".replace('.', ',')


def _wrap_text(text, width):
    words = str(text).split()
    lines = []
    current_line = ""

    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def imprimir_arquivo_nota(numero, linhas, total):
    """Imprime a nota em arquivo de texto e envia para impressora"""
    item_width = 30
    qtd_width = 6
    valor_width = 12
    subtotal_width = 12
    line_length = item_width + qtd_width + valor_width + subtotal_width
    now = datetime.now()

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as arquivo:
            arquivo.write(f"{ESTABELECIMENTO_NOME.center(line_length)}\n")
            arquivo.write(f"{ESTABELECIMENTO_ENDERECO.center(line_length)}\n")
            arquivo.write(f"CNPJ: {ESTABELECIMENTO_CNPJ}    IE: {ESTABELECIMENTO_IE}".center(line_length) + "\n")
            arquivo.write(f"TEL: {ESTABELECIMENTO_TELEFONE.center(line_length - 5)}\n")
            arquivo.write("=" * line_length + "\n")
            arquivo.write(f"{'CUPOM FISCAL'.center(line_length)}\n")
            arquivo.write("=" * line_length + "\n")
            arquivo.write(f"Nº: {numero:<8}DATA: {now:%d/%m/%Y}  HORA: {now:%H:%M:%S}\n")
            arquivo.write("-" * line_length + "\n")
            arquivo.write(f"{'ITEM':<{item_width}}{'QTD':>{qtd_width}}{'V.UNIT':>{valor_width}}{'SUBTOTAL':>{subtotal_width}}\n")
            arquivo.write("-" * line_length + "\n")

            for item, qtd, valor, subtotal in linhas:
                wrapped_item = _wrap_text(item, item_width)
                for index, item_line in enumerate(wrapped_item):
                    if index == 0:
                        arquivo.write(
                            f"{item_line:<{item_width}}{str(qtd):>{qtd_width}}{str(valor):>{valor_width}}{str(subtotal):>{subtotal_width}}\n"
                        )
                    else:
                        arquivo.write(f"{item_line:<{item_width}}{'':>{qtd_width}}{'':>{valor_width}}{'':>{subtotal_width}}\n")

            arquivo.write("=" * line_length + "\n")
            arquivo.write(f"{'TOTAL DA NOTA':<{item_width + qtd_width + valor_width}}{_format_reais_inner(total):>{subtotal_width}}\n")
            arquivo.write("=" * line_length + "\n")
            arquivo.write(f"{'FORMA DE PAGAMENTO: À VISTA'.ljust(line_length)}\n")
            arquivo.write("\n")
            arquivo.write(f"{'Consumidor:':<20}{'________________________':<{line_length - 20}}\n")
            arquivo.write(f"{'Assinatura:':<20}{'________________________':<{line_length - 20}}\n")
            arquivo.write("=" * line_length + "\n")
            arquivo.write(f"{'CUPOM SEM VALIDADE FISCAL'.center(line_length)}\n")
            arquivo.write("=" * line_length + "\n")
            arquivo_path = arquivo.name

        # Tenta imprimir o arquivo
        try:
            os.startfile(arquivo_path, 'print')
            sg.popup('A nota foi enviada para impressão.', title='Sucesso')
        except Exception as e:
            # Se falhar, tenta abrir com o programa padrão de texto
            try:
                os.startfile(arquivo_path)
                sg.popup(f'Arquivo criado em: {arquivo_path}\nAbra-o para imprimir.', title='Arquivo Criado')
            except Exception as e2:
                sg.popup(f'Erro ao imprimir: {e2}', title='Erro')
    except Exception as e:
        sg.popup(f'Erro ao criar arquivo de impressão: {e}', title='Erro')


def formatar_vendas_para_tabela(vendas_nota):
    vendas_formatadas = []
    total_cents = 0

    for venda in vendas_nota:
        item = str(venda[2]).strip()
        quantidade_cents = venda[3]
        valor_cents = venda[4]
        subtotal_cents = venda[5]
        total_cents += subtotal_cents

        vendas_formatadas.append([
            item,
            f"{quantidade_cents / 100:.2f}".replace('.', ','),
            format_reais(valor_cents),
            format_reais(subtotal_cents)
        ])

    return vendas_formatadas, total_cents
