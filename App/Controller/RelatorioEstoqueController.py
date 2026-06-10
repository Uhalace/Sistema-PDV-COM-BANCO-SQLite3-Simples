import os
import webbrowser

import PySimpleGUI as sg
import pandas as pd

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    px = None
    PLOTLY_AVAILABLE = False

class RelatorioEstoque:
    def __init__(self, banco):
        self.banco = banco

    def gerar_relatorio_estoque(self):
        estoque = self.banco.relatorio_estoque()
        if not estoque:
            sg.popup(
                "Não há itens cadastrados no estoque para gerar o relatório.",
                title="Relatório de Estoque",
                icon="./icones/estoque.ico",
            )
            return

        df = pd.DataFrame(estoque, columns=["Item", "Quantidade", "Valor"])
        df["Quantidade"] = df["Quantidade"] / 100
        df["Valor"] = df["Valor"] / 100

        df_display = df.copy()
        df_display["Quantidade"] = df_display["Quantidade"].apply(lambda x: f"{x:.2f}".replace('.', ','))
        df_display["Valor"] = df_display["Valor"].apply(lambda x: f"R$ {x:.2f}")

        total_itens = len(df)
        total_quantidade = df["Quantidade"].sum()
        total_valor = df["Valor"].sum()

        valores_tabela = df_display.values.tolist()

        layout_relatorio = [
            [sg.Push(), sg.Image("./icones/nota_100.png", pad=(0, 0)), sg.Push()],
            [
                sg.Push(),
                sg.Text(
                    "Relatório de Estoque",
                    font=("Segoe UI", 15, "bold"),
                    pad=((0, 0), (0, 10)),
                ),
                sg.Push(),
            ],
            [
                sg.Frame(
                    "Resumo",
                    [
                        [sg.Text(f"Total de itens: {total_itens}", font=("Segoe UI", 11))],
                        [sg.Text(f"Quantidade total: {total_quantidade:.2f}".replace('.', ','), font=("Segoe UI", 11))],
                        [sg.Text(f"Valor total em estoque: R$ {total_valor:.2f}", font=("Segoe UI", 11))],
                    ],
                    expand_x=True,
                )
            ],
            [
                sg.Frame(
                    "Itens em Estoque",
                    [
                        [
                            sg.Table(
                                values=valores_tabela,
                                headings=["Item", "Quantidade", "Valor"],
                                auto_size_columns=False,
                                col_widths=[40, 15, 15],
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
            "Relatório de Estoque",
            layout_relatorio,
            icon="./icones/estoque.ico",
            resizable=True,
            size=(900, 600),
            finalize=True,
            element_justification="center",
        )

        while True:
            event, _ = window_relatorio.read()
            if event in (sg.WIN_CLOSED, "Fechar"):
                break
            if event == "Exportar CSV":
                self._exportar_csv(df)
            elif event == "Abrir Gráfico":
                self._abrir_grafico(df)

        window_relatorio.close()

    def _exportar_csv(self, df):
        caminho = sg.popup_get_file(
            "Salvar relatório como CSV",
            save_as=True,
            file_types=(("CSV Files", "*.csv"),),
            default_extension=".csv",
            icon="./icones/estoque.ico",
        )
        if caminho:
            if not caminho.lower().endswith(".csv"):
                caminho += ".csv"
            df_export = df.copy()
            df_export["Quantidade"] = df_export["Quantidade"].apply(lambda x: f"{x:.2f}".replace('.', ','))
            df_export["Valor"] = df_export["Valor"].apply(lambda x: f"R$ {x:.2f}")
            df_export.to_csv(caminho, index=False, sep=";")
            sg.popup(f"Relatório salvo em:\n{caminho}", title="Exportação concluída", icon="./icones/estoque.ico")

    def _abrir_grafico(self, df):
        if not PLOTLY_AVAILABLE:
            sg.popup_error(
                "A biblioteca Plotly não está disponível para criar o gráfico.",
                title="Relatório de Estoque",
                icon="./icones/estoque.ico",
            )
            return

        estoque_item = df.groupby("Item")["Quantidade"].sum().reset_index()

        fig = px.bar(
            estoque_item,
            x="Item",
            y="Quantidade",
            title="Quantidade em Estoque por Item",
            labels={"Quantidade": "Quantidade", "Item": "Produto"},
        )

        caminho_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Banco", "relatorio_estoque_grafico.html")
        caminho_html = os.path.abspath(caminho_html)
        fig.write_html(caminho_html, auto_open=False)
        webbrowser.open(f"file://{caminho_html}")
        