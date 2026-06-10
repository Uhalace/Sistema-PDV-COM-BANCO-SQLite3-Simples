import os
import webbrowser

import PySimpleGUI as sg
import pandas as pd

from App.Functions.format import format_reais

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    px = None
    PLOTLY_AVAILABLE = False


class RelatorioVendas:
    def __init__(self, banco):
        self.banco = banco

    def gerar_relatorio_vendas(self):
        vendas = self.banco.listar_vendas()
        if not vendas:
            sg.popup(
                "Não há vendas registradas para gerar o relatório.",
                title="Relatório de Vendas",
                icon="./icones/nota.ico",
            )
            return

        df = pd.DataFrame(vendas, columns=["id", "Número", "Item", "Quantidade", "Valor", "Subtotal", "Data"])
        df["Quantidade"] = df["Quantidade"] / 100
        df["Valor"] = df["Valor"] / 100
        df["Subtotal"] = df["Subtotal"] / 100

        total_notas = df["Número"].nunique()
        total_itens = len(df)
        total_quantidade = df["Quantidade"].sum()
        total_faturamento = df["Subtotal"].sum()

        df_display = df.copy()
        df_display["Quantidade"] = df_display["Quantidade"].apply(lambda x: f"{x:.2f}".replace('.', ','))
        df_display["Valor"] = df_display["Valor"].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))
        df_display["Subtotal"] = df_display["Subtotal"].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))

        valores_tabela = df_display[["Número", "Item", "Quantidade", "Valor", "Subtotal", "Data"]].values.tolist()

        layout_relatorio = [
            [sg.Push(), sg.Image("./icones/vendas_100.png", pad=(0, 0)), sg.Push()],
            [
                sg.Push(),
                sg.Text(
                    "Relatório de Vendas",
                    font=("Segoe UI", 15, "bold"),
                    pad=((0, 0), (0, 10)),
                ),
                sg.Push(),
            ],
            [
                sg.Frame(
                    "Resumo",
                    [
                        [sg.Text(f"Notas registradas: {total_notas}", font=("Segoe UI", 11))],
                        [sg.Text(f"Itens vendidos: {total_itens}", font=("Segoe UI", 11))],
                        [sg.Text(f"Quantidade total: {total_quantidade:.2f}".replace('.', ','), font=("Segoe UI", 11))],
                        [sg.Text(f"Faturamento total: {format_reais(int(total_faturamento * 100))}", font=("Segoe UI", 11))],
                    ],
                    expand_x=True,
                )
            ],
            [
                sg.Frame(
                    "Vendas Detalhadas",
                    [
                        [
                            sg.Table(
                                values=valores_tabela,
                                headings=["Número", "Item", "Quantidade", "Valor", "Subtotal", "Data"],
                                auto_size_columns=False,
                                col_widths=[12, 36, 12, 14, 14, 18],
                                justification="center",
                                text_color="#000000",
                                background_color="#FFFFFF",
                                header_background_color="#404040",
                                header_text_color="#FFFFFF",
                                header_font=("Segoe UI", 11, "bold"),
                                font=("Segoe UI", 11),
                                row_height=25,
                                num_rows=min(12, len(valores_tabela)),
                                alternating_row_color="#F7F7F7",
                                vertical_scroll_only=True,
                                expand_x=True,
                                expand_y=True,
                                pad=(0, 0),
                            )
                        ]
                    ],
                    expand_x=True,
                    expand_y=True,
                    relief=sg.RELIEF_SUNKEN,
                    pad=(10, 10),
                )
            ],
            [
                sg.Push(),
                sg.Button("Exportar CSV", size=(14, 1), font=("Segoe UI", 10, "bold")),
                sg.Button("Abrir Gráfico", size=(14, 1), font=("Segoe UI", 10, "bold"), disabled=not PLOTLY_AVAILABLE),
                sg.Button("Fechar", size=(14, 1), font=("Segoe UI", 10, "bold")),
                sg.Push(),
            ],
        ]

        window_relatorio = sg.Window(
            "Relatório de Vendas",
            layout_relatorio,
            icon="./icones/nota.ico",
            resizable=True,
            size=(1000, 650),
            finalize=True,
            element_justification="center",
        )

        while True:
            event, _ = window_relatorio.read()
            if event in (sg.WIN_CLOSED, "Fechar"):
                break
            if event == "Exportar CSV":
                self._exportar_csv(df_display)
            elif event == "Abrir Gráfico":
                self._abrir_grafico(df)

        window_relatorio.close()

    def _exportar_csv(self, df_display):
        caminho = sg.popup_get_file(
            "Salvar relatório de vendas como CSV",
            save_as=True,
            file_types=(("CSV Files", "*.csv"),),
            default_extension=".csv",
            icon="./icones/nota.ico",
        )
        if caminho:
            if not caminho.lower().endswith(".csv"):
                caminho += ".csv"
            df_display.to_csv(caminho, index=False, sep=";")
            sg.popup(f"Relatório salvo em:\n{caminho}", title="Exportação concluída", icon="./icones/nota.ico")

    def _abrir_grafico(self, df):
        if not PLOTLY_AVAILABLE:
            sg.popup_error(
                "A biblioteca Plotly não está disponível para criar o gráfico.",
                title="Relatório de Vendas",
                icon="./icones/nota.ico",
            )
            return

        faturamento_item = df.groupby("Item")["Subtotal"].sum().reset_index()
        fig = px.bar(
            faturamento_item,
            x="Item",
            y="Subtotal",
            title="Faturamento por Item",
            labels={"Subtotal": "Valor (R$)", "Item": "Produto"},
        )

        caminho_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Banco", "relatorio_vendas_grafico.html")
        caminho_html = os.path.abspath(caminho_html)
        fig.write_html(caminho_html, auto_open=False)
        webbrowser.open(f"file://{caminho_html}")
