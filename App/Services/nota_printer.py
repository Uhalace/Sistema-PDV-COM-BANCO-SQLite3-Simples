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


def imprimir_arquivo_nota(numero, linhas, total):
    item_width = 24
    qtd_width = 6
    valor_width = 12
    subtotal_width = 14
    line_length = item_width + qtd_width + valor_width + subtotal_width
    now = datetime.now()

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

        for item, qtd, valor, subtotal in linhas:
            arquivo.write(f"{item:<{item_width}}{qtd:>{qtd_width}}{valor:>{valor_width}}{subtotal:>{subtotal_width}}\n")

        arquivo.write("=" * line_length + "\n")
        arquivo.write(f"{'TOTAL DA NOTA':<{item_width + qtd_width + valor_width}}{_format_reais_inner(total):>{subtotal_width}}\n")
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
