import os
import webbrowser

import PySimpleGUI as sg
import pandas as pd

from App.Functions.format import format_reais

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

        faturamento_item = (
            df.groupby("Item", as_index=False)
            .agg(Quantidade=("Quantidade", "sum"), Subtotal=("Subtotal", "sum"))
            .sort_values("Subtotal", ascending=False)
        )
        faturamento_item = faturamento_item.head(10)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=faturamento_item["Item"],
                y=faturamento_item["Subtotal"],
                name="Faturamento",
                marker_color="#2CA02C",
                hovertemplate="<b>%{x}</b><br>Faturamento: R$ %{y:,.2f}<extra></extra>",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=faturamento_item["Item"],
                y=faturamento_item["Quantidade"],
                name="Quantidade Vendida",
                mode="lines+markers",
                line=dict(color="#FF7F0E", width=3),
                marker=dict(size=8),
                hovertemplate="<b>%{x}</b><br>Quantidade vendida: %{y:.2f}<extra></extra>",
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title_text="Faturamento e Quantidade Vendida por Item",
            template="plotly_white",
            title_font=dict(size=22, family="Segoe UI", color="#222222"),
            font=dict(family="Segoe UI", size=12, color="#222222"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=70, r=40, t=100, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(245,247,250,1)",
        )

        fig.update_xaxes(title_text="Produto", tickangle=-45, showgrid=False)
        fig.update_yaxes(
            title_text="Faturamento (R$)",
            tickprefix="R$ ",
            secondary_y=False,
            showgrid=True,
            gridcolor="#E1E5ED",
        )
        fig.update_yaxes(
            title_text="Quantidade",
            secondary_y=True,
            showgrid=False,
        )
        fig.update_layout(width=1200, height=760)

        caminho_html = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "Banco",
            "relatorio_vendas_grafico.html",
        )
        caminho_html = os.path.abspath(caminho_html)
        self._salvar_html_impressao(fig, caminho_html, "Relatório de Vendas")
        webbrowser.open(f"file://{caminho_html}")

    def _salvar_html_impressao(self, fig, caminho_html, titulo):
        html = fig.to_html(
            full_html=True,
            include_plotlyjs="cdn",
            default_width="100%",
            default_height=760,
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
