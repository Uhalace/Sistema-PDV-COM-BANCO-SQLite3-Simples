import os
import platform
import subprocess
import tempfile
from datetime import datetime

import PySimpleGUI as sg

from App.Functions.format import format_reais
from App.Controller.CadEstabController import CadEstabController
from App.Functions.formtcnpj import format_cnpj as CNP
from App.Model.Banco import Banco


def _obter_dados_estabelecimento():
    banco_estab = Banco()
    estab_controller = CadEstabController(banco_estab)
    estabelecimento = estab_controller.listar_estabelecimento()

    # listar_estabelecimento() usa fetchone() → retorna uma tupla simples, não lista de tuplas
    # Estrutura: (id, nome, CNPJ, telefone, IE, endereco, data_cadastro)
    if estabelecimento:
        dados = {
            'nome': estabelecimento[1],
            'cnpj': CNP(estabelecimento[2]),
            'telefone': estabelecimento[3],
            'ie': estabelecimento[4],
            'endereco': estabelecimento[5],
        }
    else:
        dados = {
            'nome': '',
            'cnpj': '',
            'ie': '',
            'endereco': '',
            'telefone': '',
        }

    banco_estab.fechar_conexao()
    return dados

# else:

# ESTABELECIMENTO_NOME = "Loja Exemplo Ltda."
# ESTABELECIMENTO_CNPJ = "00.000.000/0000-00"
# ESTABELECIMENTO_IE = "123.456"
# ESTABELECIMENTO_ENDERECO = "Rua A, 0 - Centro - Cidade/UF"
# ESTABELECIMENTO_TELEFONE = "(00) 0000-0000"


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
        dados_estab = _obter_dados_estabelecimento()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as arquivo:
            arquivo.write(f"{dados_estab['nome'].center(line_length)}\n")
            arquivo.write(f"{dados_estab['endereco'].center(line_length)}\n")
            arquivo.write(f"CNPJ: {dados_estab['cnpj']}    IE: {dados_estab['ie']}".center(line_length) + "\n")
            arquivo.write(f"TEL: {dados_estab['telefone'].center(line_length - 5)}\n")
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

        # Impressão multiplataforma
        try:
            sistema = platform.system()

            if sistema == "Windows":
                # notepad /p imprime silenciosamente e fecha automaticamente
                try:
                    subprocess.run(["notepad.exe", "/p", arquivo_path], timeout=15)
                except subprocess.TimeoutExpired:
                    pass  # Notepad às vezes demora, mas a impressão já foi enviada

            elif sistema == "Darwin":  # macOS
                subprocess.run(["lpr", arquivo_path], timeout=15)

            elif sistema == "Linux":
                subprocess.run(["lp", arquivo_path], timeout=15)

            else:
                raise OSError(f"Sistema operacional não suportado para impressão: {sistema}")

            sg.popup('A nota foi enviada para impressão.', title='Sucesso', icon="./Icones/nota.ico")

        except OSError as e:
            sg.popup(str(e), title='Erro')
        except Exception as e:
            sg.popup(f'Erro ao imprimir: {e}', title='Erro')
        finally:
            # Remove o arquivo temporário — não deixa .txt salvo
            try:
                os.remove(arquivo_path)
            except Exception:
                pass
    except Exception as e:
        sg.popup(f'Erro ao criar arquivo de impressão: {e}', title='Erro', icon="./Icones/nota.ico")


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
