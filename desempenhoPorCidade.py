import dash
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

options = [
    {"label": "New York City", "value": "NYC"},
    {"label": "Montreal", "value": "MTL"},
    {"label": "San Francisco", "value": "SF"},
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


import sqlite3
import pandas as pd

enem2018 = "/home/geekaia/microdados/databases/enem2018.sqlite"
conn = sqlite3.connect(enem2018)
c = conn.cursor()

from sqlalchemy import create_engine
db = create_engine('postgresql://postgres:123@localhost/postgres')


########### Estados da federação ##########

def getEstadoCities(estado):
    conn = sqlite3.connect(enem2018)
    data = pd.read_sql(f""" select rank() over(ORDER BY  avg("mediatodos")  DESC) Ranking,  "NO_MUNICIPIO_RESIDENCIA",  avg("mediatodos") as Media  from enem2018  where  "SG_UF_RESIDENCIA"='{estado}' group by "NO_MUNICIPIO_RESIDENCIA" order by Media desc;""", con=db)

    return data

estadoatual='MT'

estadoc = getEstadoCities(estadoatual)

x = [i for i in estadoc['NO_MUNICIPIO_RESIDENCIA']]
y = [i for i in estadoc['media']]
print("Tam: ", len(x))
print(x)

print("Tam: ", len(y))
print(y)
app.config['suppress_callback_exceptions'] = True


dataestados  = pd.read_sql("""select distinct  "SG_UF_RESIDENCIA" from enem2018""", con=db)

valdrop = []


for i in dataestados['SG_UF_RESIDENCIA'].values:
    valdrop.append({'label': i, 'value': i })



import plotly.graph_objects as go
import plotly.figure_factory as ff

fig = go.Figure(go.Bar(
            x=x, y= y))

fig.update_yaxes(range=[400, 600])
# fig.show()

fig.update_layout( height=700,
    xaxis = dict(
        tickangle = -45,
        title_text = "Cidade",
        title_font = {"size": 20},
        title_standoff = 25),
    yaxis = dict(
        title_text = "Média",
        title_standoff = 25))
#
#fig.show()





app.layout = html.Div([
    html.H1('Desempenho por Estado',
            style={
                'textAlign': 'center',
                #'color': colors['text']
            }),


    html.H1(id='estadosel',
            style={
                'textAlign': 'left',
                #'color': colors['text']
            }),
    dcc.Tabs(id="tabsgrafico", value='tabsgraf', children=[
        dcc.Tab(label='Gráfico', value='grafico'),
        dcc.Tab(label='Tabela', value='tabela'),
    ]),
    html.Div(id='tabs-content'),

])

# @app.callback(
#     dash.dependencies.Output('estadosel', 'children'),
#     [dash.dependencies.Input('estado-dropdown', 'value')])
# def update_output(value):
#     return 'Estado: {}'.format(value)


@app.callback(
    dash.dependencies.Output('inscriporestado', 'figure'),
    [dash.dependencies.Input('estado-dropdown', 'value')])
def update_graph(value):

    estadoc2 = getEstadoCities(value)

    x = [i for i in estadoc2['NO_MUNICIPIO_RESIDENCIA']]
    y = [i for i in estadoc2['media']]

    dataestados = pd.read_sql("""select distinct  "SG_UF_RESIDENCIA" from enem2018""", con=db)

    valdrop = []

    for i in dataestados['SG_UF_RESIDENCIA'].values:
        valdrop.append({'label': i, 'value': i})

    import plotly.graph_objects as go
    import plotly.figure_factory as ff

    fig = go.Figure(go.Bar(
        x=x, y=y))

    fig.update_yaxes(range=[400, 600])
    # fig.show()

    fig.update_layout(height=700,
                      xaxis=dict(
                          tickangle=-45,
                          title_text="Cidade",
                          title_font={"size": 20},
                          title_standoff=25),
                      yaxis=dict(
                          title_text="Média",
                          title_standoff=25))



    return fig

@app.callback(
    dash.dependencies.Output('tabela2', 'figure'),
    [dash.dependencies.Input('estado-dropdownr', 'value')])
def update_graph2(value):

    estadoc2 = getEstadoCities(value)



    return ff.create_table(estadoc2.values.tolist())
        # dcc.Graph(
        #             id="inscriporestado",
        #             figure = fig
        #     )

    # dcc.Graph(id='tabela2',
    #                   figure=ff.create_table(getEstadoCities(value).values.tolist())
    #                   )

@app.callback(Output('tabs-content', 'children'),
              [Input('tabsgrafico', 'value')])
def render_content(tab):
    if tab == 'grafico':
        return html.Div(children=[


            html.H1(children="Desempenho por cidade",
                    style={
                        'textAlign': 'center',
                        #'color': colors['text']
                    }
                    ),
            dcc.Dropdown(
                id='estado-dropdown',
                options=valdrop,
                value='MT',
            ),
            html.Div(dcc.Graph(
                    id="inscriporestado",
                    figure = fig
            ))
        ])
    elif tab == 'tabela':
        return html.Div([
            html.H3('Ranking por cidade'),
            html.Div(dcc.Dropdown(
                id='estado-dropdownr',
                options=valdrop,
                value='MT',
            )),
            html.H4("Ranking"),

            dcc.Graph(id='tabela2',
                      figure=ff.create_table(estadoc.values.tolist())
                      )
        ])




#
# app.layout = html.Div(children=[
#     html.H1(children="Desempenho por cidade",
#             style={
#                 'textAlign': 'center',
#                 #'color': colors['text']
#             }
#             ),
#     html.Div(dcc.Graph(
#             id="inscriporestado",
#             figure = fig
#     )),
#     html.Div( dcc.Graph( id='tabela2',
#         figure=ff.create_table(estadoc.values.tolist(), height=500)
#                          ))
# ])



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8000)
