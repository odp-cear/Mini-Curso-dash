import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_ag_grid as dag
import dash_bootstrap_components as dbc # Necessário: pip install dash-bootstrap-components

# CARREGANDO AS FONTES DE DADOS
url_gapminder = "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
df_gap = pd.read_csv(url_gapminder)
df_csv = pd.read_csv("cidades_pb.csv")
df_excel = pd.read_excel("cidades_pb_excel.xlsx")

# CONFIGURAÇÃO COM TEMA BOOTSTRAP

# Escolhi o tema FLATLY que é moderno e limpo
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server

app.layout = dbc.Container([
    # Título centralizado usando classe do Bootstrap (text-center)
    dbc.Row([
        dbc.Col(html.H3("Visualizador de Dados Profissional", 
                        className="text-center text-success my-4"), width=12)
    ]),
    
    # Parágrafo estilizado
    dbc.Row([
        dbc.Col(html.P("Utilizando o sistema de colunas do Bootstrap para organizar o layout.", 
                       className="text-center mb-4"), width=12)
    ]),

    # Seletor RadioItems organizado em colunas
    dbc.Row([
        dbc.Col([
            html.Label("Escolha a Fonte de Dados:", className="fw-bold"),
            dcc.RadioItems(
                id="seletor-fonte",
                options=[
                    {"label": "Gapminder (URL)", "value": "gap"},
                    {"label": "Cidades PB (CSV)", "value": "csv"},
                    {"label": "Cidades PB (Excel)", "value": "excel"}
                ],
                value="gap",
                inline=True, # No Bootstrap, isso funciona perfeitamente para alinhar
                labelStyle={'marginRight': '20px'}
            )
        ], width={"size": 6, "offset": 3}, className="text-center bg-light p-3 rounded") # Bootstrap divide a tela em 12 partes. Usar tamanho 6 com um deslocamento (offset) de 3 é o jeito "Bootstrap" de centralizar algo perfeitamente.
    ], className="mb-5"),

    # Tabela AG Grid
    dbc.Row([
        dbc.Col([
            dag.AgGrid(
                id="tabela-dinamica",
                columnDefs=[{"field": i} for i in df_gap.columns],
                rowData=df_gap.to_dict("records"),
                defaultColDef={"resizable": True, "sortable": True, "filter": True},
                className="ag-theme-alpine",
                dashGridOptions={"pagination": True, "paginationPageSize": 10},
                style={'height': '400px'}
            )
        ], width=12)
    ])
], fluid=True)

# CALLBACK (Permanece a mesma lógica, o que prova a flexibilidade do Dash)
@app.callback(
    Output("tabela-dinamica", "rowData"),
    Output("tabela-dinamica", "columnDefs"),
    Input("seletor-fonte", "value")
)
def atualizar_fonte(fonte_selecionada):
    if fonte_selecionada == "csv":
        df_atual = df_csv
    elif fonte_selecionada == "excel":
        df_atual = df_excel
    else:
        df_atual = df_gap

    return df_atual.to_dict("records"), [{"field": i} for i in df_atual.columns]


# https://127.0.0.1:8050

# https//localhost:8050

# gunicorn app:server --bind 0.0.0.0:80
if __name__ == "__main__":
    app.run(debug=True)