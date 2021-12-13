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

def getEstadoCities(estado, variavel='mediatodos', varLocal="SG_UF_ESC"):
    #conn = sqlite3.connect(enem2018)
    municipio = "NO_MUNICIPIO_ESC"

    if varLocal == 'SG_UF_RESIDENCIA':
        municipio = "NO_MUNICIPIO_RESIDENCIA"
    elif varLocal == 'SG_UF_NASCIMENTO':
        municipio = "NO_MUNICIPIO_NASCIMENTO"
    elif varLocal == 'SG_UF_PROVA':
        municipio = "NO_MUNICIPIO_PROVA"

    data = pd.read_sql(f""" select rank() over(ORDER BY  avg("{variavel.lower()}")  DESC) Ranking,  "{municipio}",  avg("{variavel.lower()}") as Media  from enem2018  where  "{varLocal}"='{estado}' group by "{municipio}" order by Media desc;""", con=db)

    return data

estadoatual='MT'

estadoc = getEstadoCities(estadoatual)

x = [i for i in estadoc['NO_MUNICIPIO_ESC']]
y = [i for i in estadoc['media']]
print("Tam: ", len(x))
print(x)

print("Tam: ", len(y))
print(y)
app.config['suppress_callback_exceptions'] = True

def getEstados(varLocal="SG_UF_ESC"):
    dataestados  = pd.read_sql(f"""select distinct  "{varLocal}" as estado from enem2018 where "{varLocal}" is not null order by "{varLocal}" asc """, con=db)

    valdrop = []


    for i in dataestados['estado'].values:
        valdrop.append({'label': i, 'value': i })

    return valdrop

estadosbrasil = getEstados()

def getCidades(estado, varLocal="SG_UF_ESC"):

    municipio = "NO_MUNICIPIO_ESC"

    if varLocal == 'SG_UF_RESIDENCIA':
        municipio = "NO_MUNICIPIO_RESIDENCIA"
    elif varLocal == 'SG_UF_NASCIMENTO':
        municipio = "NO_MUNICIPIO_NASCIMENTO"
    elif varLocal == 'SG_UF_PROVA':
        municipio = "NO_MUNICIPIO_PROVA"



    dataestados = pd.read_sql(f"""  select distinct "{municipio}" as mun, "CO_MUNICIPIO_ESC" from enem2018 where "{varLocal}"='{estado}' order by "{municipio}" asc;  """, con=db)

    valdrop = []
    for i, j in zip(dataestados['mun'], dataestados['CO_MUNICIPIO_ESC']):
        valdrop.append({'label': i, 'value': j})


    # for i, j in zip(dataestados['NO_MUNICIPIO_ESC'], dataestados['CO_MUNICIPIO_ESC']):
    #     print(i, j)
    return dcc.Dropdown(
                    id='cidadeesc',
                    options=valdrop,
                    value=dataestados['CO_MUNICIPIO_ESC'][0],
                )


import plotly.graph_objects as go
import plotly.figure_factory as ff

fig = go.Figure(go.Bar(
            x=x, y= y))

fig.update_yaxes(range=[300, 800])
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
    html.H1('Desempenho por localidade',
            style={
                'textAlign': 'center',
                #'color': colors['text']
            }),



    dcc.Tabs(id="tabsgrafico", value='tabsgraf', children=[
        dcc.Tab(label='Cidade', value='grafico'),
        dcc.Tab(label='Estado', value='graficoestado'),
        dcc.Tab(label='Ranking', value='tabela'),
        dcc.Tab(label='Escola', value='porescola'),
    ]),
    html.Div(id='tabs-content'),

])

data = pd.read_sql("""
                    select p.Estado, p.Media from (
                        select "SG_UF_ESC" as Estado, avg("mediatodos") as Media from enem2018 where "SG_UF_ESC" is not null group by "SG_UF_ESC"
                        ) p  order by p.Media asc;

                     """, con=db)

datapare = pd.read_sql("""
                    select Estado, Abaixo, Acima,  
                        Abaixo/(Abaixo+Acima*1.0)*100 as Abaixop, 
                        Acima/(Abaixo+Acima*1.0)*100 as Acimap, 
                        sum(Abaixo) as totAbaixo, 
                        sum(Abaixo)/(total*1.0)*100 as Abaixopt, 
                        sum(Acima) as totAcima, sum(Acima)/(total*1.0)*100 as Acimapt, total
                        from 
                        (
                            select p.Estado, p.Abaixo, q.Acima, t.total from 

                            (select "SG_UF_ESC" as Estado, count(*) as Abaixo from enem2018 where "mediatodos" < 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC") as p,
                            (select "SG_UF_ESC" as Estado, count(*) as Acima from enem2018 where "mediatodos" >= 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC") as q,
                            (select count(*) as total from enem2018) as t     where   p.Estado=q.Estado                    
                        ) d group by d.Estado, d.Abaixo, d.Acima, d.total; 

                             """, con=db)
datap = pd.read_sql("""

            select p.Estado, Abaixo, Acima, Abaixo/(Abaixo+Acima*1.0)*100 as Abaixop, Acima/(Abaixo+Acima*1.0)*100 as Acimap from (
                     select "SG_UF_ESC" as Estado, count(*) as Abaixo from enem2018 where "mediatodos" < 600 group by "SG_UF_ESC") as p,
                    (select "SG_UF_ESC" as Estado, count(*) as Acima from enem2018 where "mediatodos" >= 600 group by "SG_UF_ESC") as q
                 where p.Estado=q.Estado;

                     """, con=db)

data2 = pd.read_sql("""

            select Estado, label, quant from (
                    (select "SG_UF_ESC" as Estado,'Baixo' as label, count(*) as quant from enem2018 where "mediatodos" < 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC")  union
                    (select "SG_UF_ESC" as Estado, 'Alto' as label, count(*) as quant from enem2018 where "mediatodos" >= 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC") 
                )  t order by t.quant asc;

                     """, con=db)

# print(data2)
grouped = data2.groupby('estado')[['quant']].sum()
grouped = grouped.sort_values(by='quant', ascending=False)

datap = datap.sort_values(by='acimap')
fig = go.Figure(data=[
        go.Bar(name='abaixo', x=datap['estado'], y=datap['abaixop']),
        go.Bar(name='acima', x=datap['estado'], y=datap['acimap'])
    ],

)
fig.update_layout(barmode='group', title="Porcentagem de inscrições Abaixo (< 600) e Acima(>= 600)",
        font=dict(
            size=12
    ))




# @app.callback(
#     dash.dependencies.Output('estadosel', 'children'),
#     [dash.dependencies.Input('estado-dropdown', 'value')])
# def update_output(value):
#     return 'Estado: {}'.format(value)


# estadoc2 = getEstadoCities("MT")
# # print(estadoc2['NO_MUNICIPIO_ESC'])
# # print(estadoc2['media'])
# @app.callback(
#     dash.dependencies.Output('inscriporestado', 'figure'),
#     [dash.dependencies.Input('estado-dropdown', 'value')])
# def update_graph(value):
#
#     estadoc2 = getEstadoCities(value)
#
#     x = [i for i in estadoc2['NO_MUNICIPIO_ESC']]
#     y = [i for i in estadoc2['media']]
#
#     # dataestados = pd.read_sql("""select distinct  "SG_UF_ESC" from enem2018""", con=db)
#     #
#     # valdrop = []
#     #
#     # for i in dataestados['SG_UF_ESC'].values:
#     #     valdrop.append({'label': i, 'value': i})
#
#     print(x)
#     print(y)
#
#     import plotly.graph_objects as go
#     import plotly.figure_factory as ff
#
#     fig = go.Figure(go.Bar(
#         x=x, y=y))
#
#     fig.update_yaxes(range=[400, 600])
#     # fig.show()
#
#     fig.update_layout(height=700,
#                       xaxis=dict(
#                           tickangle=-45,
#                           title_text="Cidade",
#                           title_font={"size": 20},
#                           title_standoff=25),
#                       yaxis=dict(
#                           title_text="Média",
#                           title_standoff=25))
#
#
#
#     return fig

from dash.dependencies import  State


@app.callback(
    dash.dependencies.Output('notaalunos2', 'value'),
    [dash.dependencies.Input('estado-dropdownr', 'value')])
def update_graphDrop2(value):
    return 'mediatodos'


@app.callback(
    dash.dependencies.Output('tabela2', 'figure'),
    [dash.dependencies.Input('notaalunos2', 'value')],
    state=[State('estado-dropdownr', 'value')])
def update_graph233(value, estadolist):

    estadoc2 = getEstadoCities(estadolist, value)



    return ff.create_table(estadoc2.values.tolist())
        # dcc.Graph(
        #             id="inscriporestado",
        #             figure = fig
        #     )

    # dcc.Graph(id='tabela2',
    #                   figure=ff.create_table(getEstadoCities(value).values.tolist())
    #                   )


########################### Selector ########################

########## Seta mediaTodos como default
@app.callback(
    dash.dependencies.Output('estado-local', 'value'),
    [dash.dependencies.Input('estado-dropdown', 'value')])
def update_graphDrop22(value):
    return 'SG_UF_ESC'


@app.callback(
    dash.dependencies.Output('notaalunos', 'value'),
    [dash.dependencies.Input('estado-local', 'value')])
def update_graphLocal(value):
    return 'mediatodos'


@app.callback(
    dash.dependencies.Output('inscriporestado', 'figure'),
    [dash.dependencies.Input('notaalunos', 'value')],
    state=[State('estado-dropdown', 'value'), State('estado-local', 'value')])
def update_graphg2estloc(value, estadoat, varestado):

    estadoc2 = getEstadoCities(estadoat, value)

    x = [i for i in estadoc2['NO_MUNICIPIO_ESC']]
    y = [i for i in estadoc2['media']]

    # dataestados = pd.read_sql("""select distinct  "SG_UF_ESC" from enem2018""", con=db)
    #
    # valdrop = []
    #
    # for i in dataestados['SG_UF_ESC'].values:
    #     valdrop.append({'label': i, 'value': i})

    print(x)
    print(y)

    import plotly.graph_objects as go
    import plotly.figure_factory as ff

    fig = go.Figure(go.Bar(
        x=x, y=y))

    fig.update_yaxes(range=[300, 800])
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



def getGraficos(varsel, limites="600"):
    data = pd.read_sql(f"""
                         select p.Estado, p.Media from (
                             select "{varsel}" as Estado, avg("mediatodos") as Media from enem2018 where "{varsel}" is not null group by "{varsel}"
                             ) p  order by p.Media asc;

                          """, con=db)

    datapare = pd.read_sql(f"""
                         select Estado, Abaixo, Acima,  
                             Abaixo/(Abaixo+Acima*1.0)*100 as Abaixop, 
                             Acima/(Abaixo+Acima*1.0)*100 as Acimap, 
                             sum(Abaixo) as totAbaixo, 
                             sum(Abaixo)/(total*1.0)*100 as Abaixopt, 
                             sum(Acima) as totAcima, sum(Acima)/(total*1.0)*100 as Acimapt, total
                             from 
                             (
                                 select p.Estado, p.Abaixo, q.Acima, t.total from 

                                 (select "{varsel}" as Estado, count(*) as Abaixo from enem2018 where "mediatodos" < {limites} and "{varsel}" is not null group by "{varsel}") as p,
                                 (select "{varsel}" as Estado, count(*) as Acima from enem2018 where "mediatodos" >= {limites} and "{varsel}" is not null group by "{varsel}") as q,
                                 (select count(*) as total from enem2018) as t  where   p.Estado=q.Estado                    
                             ) d group by d.Estado, d.Abaixo, d.Acima, d.total; 

                                  """, con=db)
    datap = pd.read_sql(f"""

                 select p.Estado, Abaixo, Acima, Abaixo/(Abaixo+Acima*1.0)*100 as Abaixop, Acima/(Abaixo+Acima*1.0)*100 as Acimap from (
                          select "{varsel}" as Estado, count(*) as Abaixo from enem2018 where "mediatodos" < {limites} group by "{varsel}") as p,
                         (select "{varsel}" as Estado, count(*) as Acima from enem2018 where "mediatodos" >= {limites} group by "{varsel}") as q
                      where p.Estado=q.Estado;

                          """, con=db)

    data2 = pd.read_sql(f"""

                 select Estado, label, quant from (
                         (select "{varsel}" as Estado,'Baixo' as label, count(*) as quant from enem2018 where "mediatodos" < {limites} and "{varsel}" is not null group by "{varsel}")  union
                         (select "{varsel}" as Estado, 'Alto' as label, count(*) as quant from enem2018 where "mediatodos" >= {limites} and "{varsel}" is not null group by "{varsel}") 
                     )  t order by t.quant asc;

                          """, con=db)

    # print(data2)
    grouped = data2.groupby('estado')[['quant']].sum()
    grouped = grouped.sort_values(by='quant', ascending=False)

    datap = datap.sort_values(by='acimap')
    fig = go.Figure(data=[
        go.Bar(name='abaixo', x=datap['estado'], y=datap['abaixop']),
        go.Bar(name='acima', x=datap['estado'], y=datap['acimap'])
    ],

    )
    fig.update_layout(barmode='group', title=f"Porcentagem de inscrições Abaixo (< {limites}) e Acima(>= {limites})",
                      font=dict(
                          size=12
                      ))

    return [
        dcc.Graph(
            id="enem-por-estado",
            figure={
                'data': [
                    {'x': [i for i in data['estado']], 'y': [i for i in data['media']], 'type': 'bar'}
                ],
                'layout': {
                    'title': 'Enem por Estado'
                }
            }
        ),
        dcc.Graph(
            id="media-maior-600",
            figure={
                'layout': {
                    'title': f'Porcentagem média >= {limites} por estado - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='acimapt', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='acimapt', ascending=False)['acimapt']], 'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="media-menor-600",
            figure={
                'layout': {
                    'title': f'Porcentagem média < {limites} por estado - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='abaixopt', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='abaixopt', ascending=False)['abaixopt']], 'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="media-totacima-600",
            figure={
                'layout': {
                    'title': f'Total acima >= {limites} por estado - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='totacima', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='totacima', ascending=False)['totacima']], 'type': 'bar'}
                ]
            }
        ),
        dcc.Graph(
            id="media-totmenor-600",
            figure={
                'layout': {
                    'title': f'Total abaixo < {limites} por estado - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='totabaixo', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='totabaixo', ascending=False)['totabaixo']],
                     'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="media-percmaior-600",
            figure={
                'layout': {
                    'title': f'Porcentagem >= {limites} por estado - local - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='acimap', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='acimap', ascending=False)['acimap']], 'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="media-percmenor-600",
            figure={
                'layout': {
                    'title': f'Porcentagem < {limites} por estado - local - descendente'
                },
                'data': [
                    {'x': [i for i in datapare.sort_values(by='abaixop', ascending=False)['estado']],
                     'y': [i for i in datapare.sort_values(by='abaixop', ascending=False)['abaixop']], 'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="inscriporestado",
            figure={
                'layout': {
                    'title': 'Inscrições do Enem por Estado'
                },
                'data': [
                    {'x': [i for i in grouped.index], 'y': [i for i in grouped['quant']], 'type': 'bar'}
                ]

            }
        ),
        dcc.Graph(
            id="estadopercentbaixoalto",
            figure=fig
        )
    ]




@app.callback(Output('tabs-content', 'children'),
              [Input('tabsgrafico', 'value')])
def render_content(tab):
    if tab == 'grafico':
        return html.Div(children=[


            html.H2(children="Desempenho"
                    ),
            html.Label("Estado:"),
            html.Div(
                dcc.Dropdown(
                    id='estado-dropdown',
                    options=estadosbrasil,
                    value='MT',
                )
            ),
            html.Label("Estado:"),
            html.Div(
                dcc.Dropdown(
                    id='estado-local',
                    options=[
                        {'label': 'Da residência', 'value': 'SG_UF_RESIDENCIA'},
                        {'label': 'Da escola de nível médio', 'value': 'SG_UF_ESC'},
                        {'label': 'De nascimento', 'value': 'SG_UF_NASCIMENTO'},
                        {'label': 'Da prova', 'value': 'SG_UF_PROVA'}
                    ],
                    value='SG_UF_ESC',
                )
            ),
            html.Div(
                dcc.RadioItems(
                    id='notaalunos',
                    options=[
                        {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
                        {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
                        {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
                        {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
                        {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
                        {'label': 'Média de todas as provas', 'value': 'mediatodos'},
                    ],
                    value='mediatodos',
                    labelStyle={'display': 'inline-block'}
                )

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
                options=estadosbrasil,
                value='MT',
            )),
            html.H4("Ranking"),
            html.Div(
                dcc.RadioItems(
                    id='notaalunos2',
                    options=[
                        {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
                        {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
                        {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
                        {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
                        {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
                        {'label': 'Média de todas as provas', 'value': 'mediatodos'},
                    ],
                    value='mediatodos',
                    labelStyle={'display': 'inline-block'}
                )

            ),

            dcc.Graph(id='tabela2',
                      figure=ff.create_table(estadoc.values.tolist())
                      )
        ])
    elif tab == 'graficoestado':
        return html.Div([
            html.H3('Ranking por cidade'),
            html.Label("Tipo:"),
            html.Div(dcc.Dropdown(
                id='estado-dropescolaE',
                options=[
                    {'label': 'Por estado da residência', 'value': 'SG_UF_RESIDENCIA'},
                    {'label': 'Por estado da escola', 'value': 'SG_UF_ESC'},
                    {'label': 'Estado de nascimento', 'value': 'SG_UF_NASCIMENTO'},
                    {'label': 'Estado da prova', 'value': 'SG_UF_PROVA'}
                ],
                value='SG_UF_ESC',
            )),
            html.Label("Limite: "),
            html.Div(
                dcc.RadioItems(
                    id='notalimite',
                    options=[
                        {'label': '400 pontos', 'value': '400'},
                        {'label': '500 pontos', 'value': '500'},
                        {'label': '600 pontos', 'value': '600'},
                        {'label': '700 pontos', 'value': '700'},
                        {'label': '800 pontos', 'value': '800'},
                    ],
                    value='600',
                    labelStyle={'display': 'inline-block'}
                )

            ),

            html.Div(id='graficosest', children=getGraficos("SG_UF_ESC"))

            # html.Div(dcc.Dropdown(
            #     id='estado-dropdownr',
            #     options=estadosbrasil,
            #     value='MT',
            # )),
            # html.H4("Ranking"),
            #
        ])
    elif tab == 'porescola':
        fig2 = go.Figure(go.Bar(
            x=[], y=[]))
        return html.Div([
            html.H3('Por escola'),
            html.Label("Estado:"),
            html.Div(
                dcc.Dropdown(
                    id='estado-escolar',
                    options=estadosbrasil,
                    value='MT',
                )
            ),
            html.Label("Cidade escola:"),
            html.Div(id='cidades-escola', children=getCidades('MT', varLocal="SG_UF_ESC")),

            # html.Label("O estado é pela:"),
            # html.Div(
            #     dcc.Dropdown(
            #         id='estado-localescola',
            #         options=[
            #             {'label': 'Residência', 'value': 'SG_UF_RESIDENCIA'},
            #             {'label': 'Escola de nível médio', 'value': 'SG_UF_ESC'},
            #             {'label': 'Nascimento', 'value': 'SG_UF_NASCIMENTO'},
            #             {'label': 'Prova - local', 'value': 'SG_UF_PROVA'}
            #         ],
            #         value='SG_UF_ESC',
            #     )
            # ),
            html.Div(
                dcc.RadioItems(
                    id='notaalunos2escola',
                    options=[
                        {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
                        {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
                        {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
                        {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
                        {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
                        {'label': 'Média de todas as provas', 'value': 'mediatodos'},
                    ],
                    value='mediatodos',
                    labelStyle={'display': 'inline-block'}
                )

            ),

            html.Div(dcc.Graph(
                id="graficoEscolas",
                figure=fig2
            ))
        ])

@app.callback(
    dash.dependencies.Output('notalimite', 'value'),
    [dash.dependencies.Input('estado-dropescolaE', 'value')])
def update_graphDropNotLimEscolaE(varsel):
    ########### Estados da federação ##########
    return "600"



##################################### Por escola #########################################

@app.callback(
    dash.dependencies.Output('estado-localescola', 'value'),
    [dash.dependencies.Input('cidadeesc', 'value')])
def update_graphDropUPLocal(varsel):
    ########### Estados da federação ##########
    return "SG_UF_ESC"

@app.callback(
    dash.dependencies.Output('cidades-escola', 'children'),
    [dash.dependencies.Input('estado-escolar', 'value')])
def update_graphDropCidadeEstado(varsel):
    ########### Estados da federação ##########
    return getCidades(varsel, varLocal="SG_UF_ESC")


@app.callback(
    dash.dependencies.Output('notaalunos2escola', 'value'),
    [dash.dependencies.Input('cidadeesc', 'value')])
def update_graphDropEscolasVar(varsel):
    return "mediatodos"




@app.callback(
    dash.dependencies.Output('graficoEscolas', 'figure'),
    [dash.dependencies.Input('notaalunos2escola', 'value')],
    state=[State('cidadeesc', 'value')]

)
def update_graphDropEscolasCidades(varsel, citycode):
    ########### Estados da federação ##########

    data = pd.read_sql(
        f"""
        select distinct  "CO_MUNICIPIO_ESC", "NO_MUNICIPIO_ESC", e."CO_ESCOLA", esc."NO_ENTIDADE" as noenti,  avg("{varsel}") as media from enem2018 e, escolas2018 esc 
            where  e."CO_ESCOLA"=esc."CO_ENTIDADE" and "CO_MUNICIPIO_ESC"={citycode} group by "CO_MUNICIPIO_ESC", "NO_MUNICIPIO_ESC", "CO_ESCOLA", noenti order by media desc;
        """,
        con=db)



    x = [i for i in data['noenti']]
    y = [i for i in data['media']]

    # dataestados = pd.read_sql("""select distinct  "SG_UF_ESC" from enem2018""", con=db)
    #
    # valdrop = []
    #
    # for i in dataestados['SG_UF_ESC'].values:
    #     valdrop.append({'label': i, 'value': i})


    import plotly.graph_objects as go
    import plotly.figure_factory as ff

    fig = go.Figure(go.Bar(
        x=x, y=y))

    fig.update_yaxes(range=[300, 800])
    # fig.show()

    fig.update_layout(height=700,
                      xaxis=dict(
                          tickangle=-45,
                          title_text="Escola",
                          title_font={"size": 20},
                          title_standoff=25),
                      yaxis=dict(
                          title_text="Média",
                          title_standoff=25))



    return fig







##################################### Por escola #########################################




@app.callback(
    dash.dependencies.Output('graficosest', 'children'),
    [dash.dependencies.Input('notalimite', 'value')], 
    state=[State('estado-dropescolaE', 'value')])
def update_graphDrop2(limites, varsel):
    ########### Estados da federação ##########
    return getGraficos(varsel, limites)





if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8000)
