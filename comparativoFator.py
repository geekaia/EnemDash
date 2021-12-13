
import dash
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


from sqlalchemy import create_engine
db = create_engine('postgresql://postgres:123@localhost/postgres')
# jdbc:postgresql://postgres:123@localhost/postgres
# exception: java.sql.SQLException: Unable to find a suitable driver for jdbc:postgresql://postgres:123@localhost/postgres
app.config['suppress_callback_exceptions'] = True

def getFatores(anoEnem):

    fatoresc = pd.read_sql(
        f"""  select distinct fator, descricao  from fatoresenem where ano='{anoEnem}' order by  descricao asc """,
        con=db)

    fatores = []
    for i, j in zip(fatoresc['fator'], fatoresc['descricao']):
        fatores.append({'label': j, 'value': i})

    return fatores


def getFatoresEnade():

    fatoresc = pd.read_sql(
        f"""  select distinct fator, descricao  from fatorescenso order by  descricao asc """,
        con=db)

    fatores = []
    for i, j in zip(fatoresc['fator'], fatoresc['descricao']):
        fatores.append({'label': j, 'value': i})

    return fatores

app.title = 'Comparação por fator - Enem com o Censo'


dicNotasAnos = { '2018': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2017': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2016': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2015': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2014': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2013': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2012': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NT_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NT_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NT_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NT_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2011': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NT_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NT_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NT_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NT_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2010': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2009': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de Matemática', 'value': 'NU_NOTA_MT'},
    {'label': 'Nota da prova de Linguagens e Códigos', 'value': 'NU_NOTA_LC'},
    {'label': 'Nota da prova de Ciências Humanas', 'value': 'NU_NOTA_CH'},
    {'label': 'Nota da prova de Ciências da Natureza', 'value': 'NU_NOTA_CN'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2008': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2007': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2006': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVO'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2005': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2004': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
], '2003': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
] ,'2002': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
] ,'2001': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
] ,'2000': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
] ,'1999': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
] ,'1998': [
    {'label': 'Nota da prova de redação', 'value': 'NU_NOTA_REDACAO'},
    {'label': 'Nota da prova de objetiva', 'value': 'NU_NOTA_OBJETIVA'},
    {'label': 'Média de todas as provas', 'value': 'mediatodos'},
],
}



app.layout = html.Div([
    html.H1('Comparação por fator - Enem com o Censo',
            style={
                'textAlign': 'center',
                # 'color': colors['text']
            }),
    html.Div(
        dcc.RadioItems(
            id='fonte1',
            options=[
                {'label': 'Enem', 'value': 'enem'},
                {'label': 'Censo', 'value': 'censo'},
            ],
            value='enem',
            labelStyle={'display': 'inline-block'}
        )
    ),
    html.Label("Ano:"),
    html.Div(
        dcc.Dropdown(
            id='anoEnem',
            disabled=False,
            options= [
                {'label' :'Enem 2018', 'value': '2018'},
                {'label' :'Enem 2017', 'value': '2017'},
                {'label' :'Enem 2016', 'value': '2016'},
                {'label' :'Enem 2015', 'value': '2015'},
                {'label' :'Enem 2014', 'value': '2014'},
                {'label' :'Enem 2013', 'value': '2013'},
                {'label' :'Enem 2012', 'value': '2012'},
                {'label' :'Enem 2011', 'value': '2011'},
                {'label' :'Enem 2010', 'value': '2010'},
                {'label' :'Enem 2009', 'value': '2009'},
                {'label' :'Enem 2008', 'value': '2008'},
                {'label' :'Enem 2007', 'value': '2007'},
                {'label' :'Enem 2006', 'value': '2006'},
                {'label' :'Enem 2005', 'value': '2005'},
                {'label' :'Enem 2004', 'value': '2004'},
                {'label' :'Enem 2003', 'value': '2003'},
                {'label' :'Enem 2002', 'value': '2002'},
                {'label' :'Enem 2001', 'value': '2001'},
                {'label' :'Enem 2000', 'value': '2000'},
                {'label' :'Enem 1999', 'value': '1999'},
                {'label' :'Enem 1998', 'value': '1998'},
            ],
            value='2018',
        )
    ),

    html.Label("Fator 1:"),
    html.Div(
        dcc.Dropdown(
            id='caracteristica1',
            options= getFatores('2018')
        )
    ),
    html.Label("Fator 2: "),
    html.Div(
        dcc.RadioItems(
            id='fonte2',
            options=[
                {'label': 'Enem', 'value': 'enem'},
                {'label': 'Censo', 'value': 'censo'},
                {'label': 'PIB', 'value': 'censop'},
                {'label': 'GINI cidades', 'value': 'ginicidades'},
            ],
            value='enem',
            labelStyle={'display': 'inline-block'}
        )

    ),
    html.Div(
        dcc.Dropdown(
            id='caracteristica2',
            options= getFatores('2018')
        )
    ),
    html.Div(
        dcc.RadioItems(
            id='notaalunoscomp',
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
    html.Div(id="graficointeracao", children=[
        dcc.Graph(
            id="enem-por-estado",
            figure={
                'data': [
                    {'x': [1, 2, 3, 4, 5, 6], 'y': [2, 4, 6, 8, 10, 12]}
                ],
                'layout': {
                    'title': 'Enem por Estado'
                }
            }
        )
    ])


])

# id = 'anoEnem',
# disabled = True,
@app.callback(
    dash.dependencies.Output('anoEnem', 'disabled'),
    [dash.dependencies.Input('fonte1', 'value')])
def Enabledisable(valor):
    if valor == 'enem':
        return False
    else:
        return True



# anoEnem
@app.callback(
    dash.dependencies.Output('notaalunoscomp', 'options'),
    [dash.dependencies.Input('anoEnem', 'value')])

def anoVariaveisDesempenho(anoEnem):
    ########### Estados da federação ##########

    return dicNotasAnos[anoEnem]



@app.callback(
    dash.dependencies.Output('caracteristica1', 'options'),
    [dash.dependencies.Input('fonte1', 'value'),
     dash.dependencies.Input('anoEnem', 'value')])
def update_graphDropFonte1(valor, anoEnem):
    ########### Estados da federação ##########

    if valor == 'enem':
        return getFatores(anoEnem)
    else:
        return getFatoresEnade()

#
@app.callback(
    dash.dependencies.Output('fonte2', 'value'),
    [dash.dependencies.Input('caracteristica1', 'value')])
def update_graphDropFonte1343(valor):
    ########### Estados da federação ##########

    return "enem"


@app.callback(
    dash.dependencies.Output('caracteristica2', 'options'),
    [dash.dependencies.Input('fonte2', 'value'),
     dash.dependencies.Input('anoEnem', 'value')])
def update_graphDropFonte2(valor, anoEnem):
    ########### Estados da federação ##########

    if valor == 'enem':
        return getFatores(anoEnem)
    elif valor == 'censop':
        return [{'label': 'Atividade com maior valor adicionado bruto', 'value': 'atividadeprincipal'}, {'label': 'PIB - acima ou abaixo da média', 'value': 'pib'}]
    elif valor == 'ginicidades':
        return [{'label': 'Gini cidades - 2010', 'value': 'ginicidades2010'}]
    else:
        return getFatoresEnade()


def getTitle(x):
    if x == 'atividadeprincipal':
        return 'Atividade com maior valor adicionado bruto'
    else:
        return 'PIB - acima ou abaixo da média'

from dash.dependencies import  State


def toInt(x):
    try:
        ret = int (x)
        return ret
    except:
        return x


@app.callback(
    dash.dependencies.Output('notaalunoscomp', 'value'),
    [dash.dependencies.Input('caracteristica2', 'value')])
def update_graphDropFontesetaMedias(valor):
    ########### Estados da federação ##########

    return "mediatodos"


@app.callback(
    dash.dependencies.Output('graficointeracao', 'children'),
    ### Argumentos
    [dash.dependencies.Input('notaalunoscomp', 'value')],
    state=[State('caracteristica2', 'value'),
           State('caracteristica1', 'value'),
           State('fonte1', 'value'),
           State('fonte2', 'value'), State('anoEnem', 'value')])
def update_graphDropFonte2(avaliacao, valFator2, valFator1, fonte1, fonte2, anoEnem):
    ########### Estados da federação ##########

    tabelasEnem = { '1998': 'enem1998',
                    '1999': 'enem1999',
                    '2000': 'enem2000',
                    '2001': 'enem2001',
                    '2002': 'enem2002',
                    '2003': 'enem2003',
                    '2004': 'enem2004',
                    '2005': 'enem2003',
                    '2006': 'enem2006',
                    '2007': 'enem2007' ,
                    '2008': 'enem2008' ,
                    '2009': 'enem2009',
                    '2010': 'enem2010' ,
                    '2011': 'enem2011' ,
                    '2012': 'enem2012' ,
                    '2013': 'enem2013' ,
                    '2014': 'enem2014' ,
                    '2015': 'enem2015',
                    '2016': 'enem2016',
                    '2017': 'enem2017',
                    '2018': 'enem2018' }

    print("Ano enem: ", anoEnem)
    tabela = tabelasEnem[anoEnem]
    print("Tabela: ", tabela)


    print("Fonte1: ", fonte1)
    print("Fonte2: ", fonte2)
    print("valFator1: ", valFator1)
    print("valFator2: ", valFator2)

    print()

    if valFator2 == None:
        return dcc.Graph(
            id="enem-por-estado",
            figure={
                'data': [
                    {'x': [], 'y': []}
                ],
                'layout': {
                    'title': 'Enem por Estado'
                }
            }
        )
    ### Abaixo ou acima depende da média, caso esteja
    ############ LEMBRAR DE MUDAR PARA A CIDADE DA LOCALIDADE DA ESCOLA E NÃO DA RESIDÊNCIA !!!!!!!!!!!!


    if fonte2 == 'censop':


        # return [{'label': 'Atividade com maior valor adicionado bruto', 'value': 'atividadeprincipal'}, {'label': 'PIB - acima ou abaixo da média', 'value': 'pib'}]


        if valFator2 == 'pib':

            print \
                (f"""  select "{valFator1}" as fator1, (case when pibpercapita >= 21990.76 then 'Alto' else 'Baixo' end ) as fator2, avg({avaliacao}) as media,  count(*) as quant  
                    from {tabela}, escolas2018, pibcidades where  escolas2018."CO_ENTIDADE"={tabela}."CO_ESCOLA" and {tabela}."CO_MUNICIPIO_ESC"=pibcidades.codigomunicipio  and "{valFator1}" is not null 
                group by "{valFator1}", fator2 ; """)
            datafact = pd.read_sql(
                f"""  select "{valFator1}" as fator1, (case when pibpercapita >= 21990.76 then 'Alto' else 'Baixo' end ) as fator2, avg({avaliacao}) as media,  count(*) as quant  
                    from {tabela}, escolas2018, pibcidades where  escolas2018."CO_ENTIDADE"={tabela}."CO_ESCOLA" and {tabela}."CO_MUNICIPIO_ESC"=pibcidades.codigomunicipio  and "{valFator1}" is not null 
                group by "{valFator1}", fator2 ; """,
                con=db)
        else:
            print(
                f"""  select "{valFator1}" as fator1, "{valFator2}" as fator2, avg({avaliacao}) as media,  count(*) as quant from {tabela}, escolas2018, pibcidades where  escolas2018."CO_ENTIDADE"={tabela}."CO_ESCOLA" and {tabela}."CO_MUNICIPIO_ESC"=pibcidades.codigomunicipio  and "{valFator2}" is not null and "{valFator1}" is not null group by "{valFator1}","{valFator2}" ; """)
            datafact = pd.read_sql(
                f"""  select "{valFator1}" as fator1, "{valFator2}" as fator2, avg({avaliacao}) as media,  count(*) as quant from {tabela}, escolas2018, pibcidades where  escolas2018."CO_ENTIDADE"={tabela}."CO_ESCOLA" and {tabela}."CO_MUNICIPIO_ESC"=pibcidades.codigomunicipio  and "{valFator2}" is not null and "{valFator1}" is not null group by "{valFator1}","{valFator2}" ; """,
                con=db)
    elif fonte2 == 'ginicidades':
        # print(f"""  select "{valFator1}" as fator1, "{valFator2}" as fator2, avg({avaliacao}) as media,  count(*) as quant from enem2018, escolas2018 where  escolas2018."CO_ENTIDADE"=enem2018."CO_ESCOLA" and "{valFator2}" is not null and "{valFator1}" is not null group by "{valFator1}","{valFator2}" ; """)

        # datafact = pd.read_sql(
        #     f"""  select "{valFator1}" as fator1, "{valFator2}" as fator2, avg({avaliacao}) as media,  count(*) as quant from enem2018, escolas2018 where  escolas2018."CO_ENTIDADE"=enem2018."CO_ESCOLA" and "{valFator2}" is not null and "{valFator1}" is not null group by "{valFator1}","{valFator2}" ; """,
        #     con=db)

        sqls = f"""select gg.fator1, gg.fator2, avg(gg.media) as media, sum(gg.quant) as quant from  (select n.fator1 as fator1, gni.gini as fator2, n.media as media, gni.quant as quant from 
            (select "{valFator1}" as fator1, "SG_UF_ESC" as  est, avg("mediatodos") as media  from enem2018 where "{valFator1}" is not null group by "{valFator1}",  "SG_UF_ESC" ) n, 
            ( select "SG_UF_ESC" as  est, (case when avg(g.gini) > 0.5513584092537896 then 'Alto' else 'Baixo' end ) as gini, count(*) as quant 
                from {tabela}, ginicidades as g 
                where g.cidade={tabela}."NO_MUNICIPIO_ESC" and  "SG_UF_ESC" is not null group by "SG_UF_ESC") gni 
            where gni.est=n.est) as gg group by gg.fator1, gg.fator2;"""

        print(sqls)

        datafact = pd.read_sql(sqls, con=db)
    else:
        print()
        datafact = pd.read_sql(
            f"""  select "{valFator1}" as fator1, "{valFator2}" as fator2, avg({avaliacao}) as media,  count(*) as quant from {tabela}, escolas2018 where  escolas2018."CO_ENTIDADE"={tabela}."CO_ESCOLA" and "{valFator2}" is not null and "{valFator1}" is not null group by "{valFator1}","{valFator2}" ; """,
            con=db)


    # print(datafact)

    import plotly.express as px
    opcs = []

    ####################### FATOR 1 ############################
    ########## Só irá retornar um valor
    #
    #
    #
    fatorInfo = None
    #
    if fonte1 == 'censo':
        fatorInfo = pd.read_sql(
            f"""  select fator, descricao, niveis from fatorescenso where fator='{valFator1}'; """,
            con=db)
        print("Query1: " ,f"""  select fator, descricao, niveis from fatorescenso where fator='{valFator1}'; """)
    else:
        fatorInfo = pd.read_sql(
            f"""  select fator, descricao, niveis from fatoresenem where fator='{valFator1}'; """,
            con=db)
        print("Query2: ", f"""  select fator, descricao, niveis from fatoresenem where fator='{valFator1}'; """)


    print("Fonte1: ", fonte1)
    print("Fator info: ", fatorInfo)


    ############ Aqui pode dar algum tipo de bug
    if fatorInfo['niveis'][0] is not None:
        niveis = fatorInfo['niveis'][0].split("\n")
        for ni in niveis:
            ops = ni.split("\t")
            opcs.append({ toInt(ops[0]) : ops[1] })

    print("Opções: ", opcs)

    for op in opcs:
        datafact['fator1'][datafact['fator1'] == list(op.keys())[0] ] = list(op.values())[0]



    ############################## FATOR 2 ################################
    opcs = []
    # print("Fator 2: ", fator2)

    fatorInfo2 = None

    fatorInfo2 = pd.read_sql(
        f"""  select fator, descricao, niveis from fatoresenem where fator='{valFator2}'; """,
        con=db)

    if fonte2 == 'censo':
        fatorInfo2 = pd.read_sql(
            f"""  select fator, descricao, niveis from fatorescenso where fator='{valFator2}'; """,
            con=db)
        print("Query1: " ,f"""  select fator, descricao, niveis from fatorescenso where fator='{valFator2}'; """)
    elif fonte2 == 'censop':
        fatorInfo2 = None
    elif fonte2 == 'ginicidades':
        fatorInfo2 = None
    else:
        fatorInfo2 = pd.read_sql(
            f"""  select fator, descricao, niveis from fatoresenem where fator='{valFator2}'; """,
            con=db)
        print("Query2: ", f"""  select fator, descricao, niveis from fatoresenem where fator='{valFator2}'; """)



    print("Fonte1: ", fonte1)
    # print("Tam fatorinf2: ", len(fatorInfo2))
    if fonte2 == 'censo':
        fatorInfo2 = pd.read_sql(
            f"""  select fator, descricao, niveis from fatorescenso where fator='{valFator2}'; """,
            con=db)

    ############ Aqui pode dar algum tipo de bug
    if fatorInfo2 is not None:
        if fatorInfo2['niveis'][0] is not None:
            niveis = fatorInfo2['niveis'][0].split("\n")
            for ni in niveis:
                ops = ni.split("\t")
                opcs.append({toInt(ops[0]): ops[1]})

    print("Opções2: ", opcs)

    for op in opcs:

        datafact['fator2'][datafact['fator2'] == list(op.keys())[0]] = list(op.values())[0]
    #

    ########### FATOR 2 ###########

    fig = px.line(datafact, x="fator2", y="media", color='fator1')
    fig.update_yaxes(automargin=True)

    fig.update_layout(
        # title="Plot Title",
        xaxis_title=getTitle(valFator2) if fatorInfo2 is None else fatorInfo2.descricao[0],
        yaxis_title="Média",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="#7f7f7f"
        # )
    )

    #
    #
    # #fig.show()
    #
    # ########## Bar chart with the same content ###########################
    #
    # import plotly.express as px
    #
    fig2 = px.bar(datafact, x="fator2", y="media", color="fator1")
    fig2.update_layout(barmode='group', xaxis_tickangle=45)
    fig2.update_layout(
        # title="Plot Title",
        xaxis_title= getTitle(valFator2) if fatorInfo2 is None else fatorInfo2.descricao[0],
        yaxis_title="Média",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="#7f7f7f"
        # )
    )
    fig2.update_yaxes(automargin=True)

    #
    #
    fig3 = px.pie(datafact, values='quant', names='fator1', title=f'')
    fig3.update_yaxes(automargin=True)

    fig4 = px.pie(datafact, values='quant', names='fator2', title=f'')
    fig4.update_yaxes(automargin=True)

    fig5 = px.bar(datafact, x="fator2", y="quant", color="fator1")
    fig5.update_layout(barmode='group', xaxis_tickangle=45)
    fig5.update_layout(
        # title="Plot Title",
        xaxis_title=getTitle(valFator2) if fatorInfo2 is None else fatorInfo2.descricao[0],
        yaxis_title="Quantidade",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="#7f7f7f"
        # )
    )
    fig5.update_yaxes(automargin=True)

    return [
        dcc.Graph(
            id = "enem-por-estado",
            figure = fig
        ),
        dcc.Graph(
            id="enem-barit",
            figure=fig2
        ),
        #
        #
        html.Div([
            html.Div([
                html.H3(f'{fatorInfo.descricao[0]}'),
                dcc.Graph(
                    id="pie1",
                    figure=fig3
                ),
            ]),

            html.Div([
                html.H3(f'{fatorInfo2.descricao[0]}' if fatorInfo2 is not None else getTitle(valFator2)),
                dcc.Graph(
                    id="pie1",
                    figure=fig4
                ),
            ]),
        ], className="row"),
        dcc.Graph(
            id="enem-quantclass",
            figure=fig5
        ),

    ]


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8000)
