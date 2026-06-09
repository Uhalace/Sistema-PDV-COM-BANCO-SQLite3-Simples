import PySimpleGUI as sg

from App.Controller.CadastrarNotaController import CadastrarNotaController
from App.Controller.ListarNotaController import ListarNotaController
from App.Controller.ListarEstoqueController import ListarEstoqueControler
from App.Functions.format import format_reais
from App.Model.Banco import Banco
from App.Services.nota_printer import formatar_vendas_para_tabela, imprimir_arquivo_nota
from App.Controller.CadastroEstoqueController import CadastrarEstoqueController


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
        [sg.Button("Cadastrar Estoque", size=(18, 2), font=("Segoe UI", 10, "bold")),
         sg.Button("Listar Estoque", size=(18, 2), font=("Segoe UI", 10, "bold")),
         sg.Button("Sair", size=(18, 2), font=("Segoe UI", 10, "bold"))],
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


def _preparar_dados_notas(banco, filtro=""):
    """Prepara dados das notas com informações detalhadas para exibição"""
    notas_numeros = banco.listar_numeros_notas()
    notas_dados = []
    
    for numero_nota in notas_numeros:
        vendas = banco.imprimir_nota(numero_nota)
        if vendas:
            total_nota = sum(venda[5] for venda in vendas)  # subtotal em centavos
            quantidade_itens = len(vendas)
            
            if filtro.isdigit():
                if str(numero_nota).startswith(filtro):
                    notas_dados.append({
                        'numero': numero_nota,
                        'total': total_nota,
                        'itens': quantidade_itens,
                        'texto': f"{numero_nota:05d}"
                    })
            elif not filtro:
                notas_dados.append({
                    'numero': numero_nota,
                    'total': total_nota,
                    'itens': quantidade_itens,
                    'texto': f"{numero_nota:05d}"
                })
    
    return sorted(notas_dados, key=lambda x: x['numero'], reverse=True)


def selecionar_nota_para_impressao(banco):
    """Modal de seleção de nota para impressão com layout padrão do sistema"""
    
    NOTAS_POR_PAGINA = 8
    current_page = 1
    filtro = ""
    numero_nota_selecionada = None
    
    notas_dados_completas = _preparar_dados_notas(banco, filtro)
    
    def get_page_rows(page):
        start = (page - 1) * NOTAS_POR_PAGINA
        end = start + NOTAS_POR_PAGINA
        return notas_dados_completas[start:end]
    
    def criar_valores_tabela(page):
        rows = get_page_rows(page)
        return [[nota['texto'], format_reais(nota['total']), str(nota['itens'])] for nota in rows]
    
    total_rows = len(notas_dados_completas)
    total_pages = max(1, (total_rows + NOTAS_POR_PAGINA - 1) // NOTAS_POR_PAGINA)
    
    screen_width, screen_height = sg.Window.get_screen_size()
    window_width = min(900, int(screen_width * 0.92))
    window_height = min(650, int(screen_height * 0.82))
    
    def criar_layout(page):
        layout = [
            [sg.Push(), sg.Image("./icones/nota_100.png", pad=(0, 0)), sg.Push()],
            [sg.Push(),
             sg.Text(
                 "Seleção de Nota para Impressão",
                 font=("Segoe UI", 15, "bold"),
                 pad=((0, 0), (0, 10))
             ),
             sg.Push()],
            [sg.Push(),
             sg.Text("Filtrar por número:", font=("Segoe UI", 10)),
             sg.InputText(filtro, key="-FILTRO-", size=(15, 1), font=("Segoe UI", 10), enable_events=True),
             sg.Push()],
            [sg.Frame(
                "",
                [[
                    sg.Table(
                        values=criar_valores_tabela(page),
                        headings=["Número", "Total", "Itens"],
                        key="-TABLE-",
                        auto_size_columns=False,
                        col_widths=[15, 20, 12],
                        justification="center",
                        text_color="#000000",
                        background_color="#FFFFFF",
                        header_background_color="#404040",
                        header_text_color="#FFFFFF",
                        header_font=("Segoe UI", 11, "bold"),
                        font=("Segoe UI", 11),
                        row_height=30,
                        num_rows=NOTAS_POR_PAGINA,
                        alternating_row_color="#F7F7F7",
                        vertical_scroll_only=True,
                        enable_events=True,
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
                sg.Text(f"Página {page}/{total_pages}", key="-PAGE-", font=("Segoe UI", 11, "bold"), pad=(10, 0)),
                sg.Button("Próximo >>", key="-NEXT-", size=(12, 1), font=("Segoe UI", 10)),
                sg.Push()
            ],
            [sg.HorizontalSeparator()],
            [sg.Push(),
             sg.Button(
                 "Selecionar", size=(18, 2), font=("Segoe UI", 10, "bold"), button_color=("#FFFFFF", "#27ae60")),
             sg.Button(
                 "Cancelar", size=(18, 2), font=("Segoe UI", 10, "bold"), button_color=("#FFFFFF", "#c0392b")),
             sg.Push()]
        ]
        return layout
    
    window_selecao = sg.Window(
        "Selecionar Nota",
        criar_layout(current_page),
        icon="./icones/nota.ico",
        resizable=True,
        size=(window_width, window_height),
        finalize=True,
        element_justification="center"
    )
    
    window_selecao["-PREV-"].update(disabled=True)
    window_selecao["-NEXT-"].update(disabled=(total_pages == 1))
    
    while True:
        event_sel, valores_sel = window_selecao.read()
        
        if event_sel in (sg.WIN_CLOSED, "Cancelar"):
            break
        
        if event_sel == "-FILTRO-":
            novo_filtro = valores_sel["-FILTRO-"]
            if novo_filtro != filtro:
                filtro = novo_filtro
                notas_dados_completas = _preparar_dados_notas(banco, filtro)
                total_rows = len(notas_dados_completas)
                total_pages = max(1, (total_rows + NOTAS_POR_PAGINA - 1) // NOTAS_POR_PAGINA)
                current_page = 1
                
                window_selecao["-TABLE-"].update(values=criar_valores_tabela(current_page))
                window_selecao["-PAGE-"].update(f"Página {current_page}/{total_pages}")
                window_selecao["-PREV-"].update(disabled=True)
                window_selecao["-NEXT-"].update(disabled=(total_pages == 1))
        
        if event_sel == "-PREV-" and current_page > 1:
            current_page -= 1
            window_selecao["-TABLE-"].update(values=criar_valores_tabela(current_page))
            window_selecao["-PAGE-"].update(f"Página {current_page}/{total_pages}")
            window_selecao["-PREV-"].update(disabled=(current_page == 1))
            window_selecao["-NEXT-"].update(disabled=False)
        
        elif event_sel == "-NEXT-" and current_page < total_pages:
            current_page += 1
            window_selecao["-TABLE-"].update(values=criar_valores_tabela(current_page))
            window_selecao["-PAGE-"].update(f"Página {current_page}/{total_pages}")
            window_selecao["-NEXT-"].update(disabled=(current_page == total_pages))
            window_selecao["-PREV-"].update(disabled=False)
        
        if event_sel == "Selecionar":
            table_values = window_selecao["-TABLE-"].get()
            if table_values:
                # Pega a primeira linha selecionada
                selected_rows = window_selecao["-TABLE-"].SelectedRows
                if selected_rows:
                    row_index = selected_rows[0]
                    rows = get_page_rows(current_page)
                    if row_index < len(rows):
                        numero_nota_selecionada = rows[row_index]['numero']
                        break
            else:
                sg.popup_error("Por favor, selecione uma nota.")
    
    window_selecao.close()
    
    return numero_nota_selecionada


def mostrar_nota_para_impressao(numero_nota, banco):
    try:
        numero_nota_int = int(numero_nota)
    except ValueError:
        sg.popup_error("Por favor, insira um número válido para a nota.", title="Erro")
        return

    vendas_nota = banco.imprimir_nota(numero_nota_int)
    if not vendas_nota:
        sg.popup_error("Nenhuma venda encontrada para o número da nota informado.", title="Erro")
        return

    vendas_formatadas, total_cents = formatar_vendas_para_tabela(vendas_nota)

    screen_width, screen_height = sg.Window.get_screen_size()
    window_width = min(1000, int(screen_width * 0.92))
    window_height = min(650, int(screen_height * 0.82))
    
    layout_impressao = [
        [sg.Push(), sg.Image("./icones/nota_100.png", pad=(0, 0)), sg.Push()],
        [sg.Push(),
         sg.Text(
             "Visualizar Nota para Impressão",
             font=("Segoe UI", 15, "bold"),
             pad=((0, 0), (0, 10))
         ),
         sg.Push()],
        [sg.Frame(
            "",
            [[
                sg.Table(
                    values=vendas_formatadas,
                    headings=["Item", "Quantidade", "Valor", "Subtotal"],
                    auto_size_columns=False,
                    col_widths=[40, 15, 18, 18],
                    justification="center",
                    text_color="#000000",
                    background_color="#FFFFFF",
                    header_background_color="#404040",
                    header_text_color="#FFFFFF",
                    header_font=("Segoe UI", 11, "bold"),
                    font=("Segoe UI", 11),
                    row_height=30,
                    alternating_row_color="#F7F7F7",
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
        [sg.HorizontalSeparator()],
        [sg.Text(f"Nota Fiscal - Número: {numero_nota:05d}", font=("Segoe UI", 11, "bold"), justification='left'),
         sg.Text(
            f"Total da Nota: {format_reais(total_cents)}",
            font=("Segoe UI", 12, "bold"),
            justification='right'
        )],
        [sg.Push(),
         sg.Button(
             "Imprimir", size=(18, 2), font=("Segoe UI", 10, "bold"), button_color=("#FFFFFF", "#27ae60")),
         sg.Button(
             "Fechar", size=(18, 2), font=("Segoe UI", 10, "bold")),
         sg.Push()]
    ]

    window_impressao = sg.Window(
        "Imprimir Nota",
        layout_impressao,
        icon="./icones/nota.ico",
        resizable=True,
        size=(window_width, window_height),
        finalize=True,
        element_justification="center"
    )

    while True:
        event_impressao, _ = window_impressao.read()
        if event_impressao in (sg.WIN_CLOSED, "Fechar"):
            break
        if event_impressao == "Imprimir":
            imprimir_arquivo_nota(numero_nota_int, vendas_formatadas, total_cents)

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
        elif event == "Cadastrar Estoque":
            cadastrar_estoque_controller = CadastrarEstoqueController(banco)
            cadastrar_estoque_controller.cadastrar_estoque()
        elif event == "Listar Estoque":
            listar_estoque_controller = ListarEstoqueControler(banco)
            listar_estoque_controller.listar_estoque()
            
    window.close()
    banco.fechar_conexao()
