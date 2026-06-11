import os
import webbrowser

import PySimpleGUI as sg
import pandas as pd

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    px = None
    go = None
    make_subplots = None
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

        estoque_item = (
            df.groupby("Item", as_index=False)[["Quantidade", "Valor"]]
            .sum()
            .sort_values("Quantidade", ascending=False)
        )

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.12,
            subplot_titles=(
                "Quantidade em Estoque por Item",
                "Valor em Estoque por Item",
            ),
        )

        fig.add_trace(
            go.Bar(
                x=estoque_item["Item"],
                y=estoque_item["Quantidade"],
                name="Quantidade",
                marker_color="#4C78A8",
                hovertemplate="<b>%{x}</b><br>Quantidade: %{y:.2f}<extra></extra>",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=estoque_item["Item"],
                y=estoque_item["Valor"],
                name="Valor em Estoque",
                marker_color="#F58518",
                hovertemplate="<b>%{x}</b><br>Valor em estoque: R$ %{y:,.2f}<extra></extra>",
            ),
            row=2,
            col=1,
        )

        fig.update_layout(
            title_text="Análise de Estoque",
            template="plotly_white",
            title_font=dict(size=22, family="Segoe UI", color="#222222"),
            font=dict(family="Segoe UI", size=12, color="#222222"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=70, r=40, t=100, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(245,247,250,1)",
        )

        fig.update_xaxes(
            title_text="Produto",
            tickangle=-45,
            row=2,
            col=1,
            showgrid=False,
        )
        fig.update_yaxes(
            title_text="Quantidade",
            row=1,
            col=1,
            showgrid=True,
            gridcolor="#E1E5ED",
        )
        fig.update_yaxes(
            title_text="Valor (R$)",
            row=2,
            col=1,
            tickprefix="R$ ",
            showgrid=True,
            gridcolor="#E1E5ED",
        )
        fig.update_layout(width=1200, height=820)

        caminho_html = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "Banco",
            "relatorio_estoque_grafico.html",
        )
        caminho_html = os.path.abspath(caminho_html)
        self._salvar_html_impressao(fig, caminho_html, "Relatório de Estoque")
        webbrowser.open(f"file://{caminho_html}")

    def _salvar_html_impressao(self, fig, caminho_html, titulo):
        html = fig.to_html(
            full_html=True,
            include_plotlyjs="cdn",
            default_width="100%",
            default_height=820,
            config={"displayModeBar": False, "responsive": True},
        )

        style = f"""
<style>
body {{ margin: 0; padding: 28px; font-family: 'Segoe UI', sans-serif; background-color: #ffffff; color: #111111; }}
#header {{ text-align: center; margin-bottom: 24px; }}
#header h1 {{ margin: 0; font-size: 32px; letter-spacing: -0.6px; }}
#header p {{ margin: 6px 0 0; font-size: 14px; color: #525252; }}
#print-button {{ position: fixed; top: 18px; right: 18px; z-index: 9999; background: #4C78A8; color: white; border: none; border-radius: 6px; padding: 12px 18px; font-size: 13px; cursor: pointer; box-shadow: 0 8px 20px rgba(0,0,0,0.16); }}
@media print {{
  body {{ margin: 0; padding: 12px; }}
  #print-button {{ display: none !important; }}
  .modebar {{ display: none !important; }}
  .plotly .main-svg {{ background-color: #ffffff !important; }}
}}
</style>
"""
        script = """
<script>
function printReport() {
    window.print();
}
</script>
"""
        header = f"""
<div id=\"header\">
  <h1>{titulo}</h1>
  <p>Gráfico pronto para impressão — use Ctrl+P ou o botão abaixo.</p>
</div>
<button id=\"print-button\" onclick=\"printReport()\">Imprimir</button>
"""
        html = html.replace("<body>", f"<body>\n{style}\n{script}\n{header}\n", 1)

        with open(caminho_html, "w", encoding="utf-8") as arquivo:
            arquivo.write(html)
        