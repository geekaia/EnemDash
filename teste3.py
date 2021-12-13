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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine


db = create_engine('postgresql://postgres:123@localhost/postgres')

val=1


def getX():
    sql = "select * from grafico; "
    # print(sql)
    res = db.execute(sql)
    # for i in res:
    #     print(i)
    x = []

    for i in res:
        x.append(i[1])

    return x

def getY():
    global val
    sql = "select * from grafico; "
    # print(sql)
    res = db.execute(sql)
    # for i in res:
    #     print(i)
    x = []

    for i in res:
        x.append(i[2]*val)


    val = val + 1

    return x


print(getX())

print(getY())
print(getY())
print(getY())



app.layout = html.Div(children=[
    html.H1(children="Fator Estado",
            style={
                'textAlign': 'center',

            }
            ),
    html.Button('Click Me', id='my-button'),
    dcc.Graph(
        id="enem-por-estado",
        figure = {
            'data': [
                {'x': getX(), 'y': getY(), 'type': 'bar'}
            ],
            'layout': {
                'title': 'Enem por Estado'
            }
        }
    )]
)

@app.callback(dash.dependencies.Output('enem-por-estado', 'figure'),
              [Input('my-button', 'n_clicks')])
def on_click(n_clicks):
    return {
            'data': [
                {'x': getX(), 'y': getY(), 'type': 'bar'}
            ],
            'layout': {
                'title': 'Enem por Estado'
            }
        }



if __name__ == '__main__':
    app.run_server(debug=True)
